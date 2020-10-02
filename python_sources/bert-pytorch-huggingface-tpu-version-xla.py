#!/usr/bin/env python
# coding: utf-8

# ### This kernel is forked from https://www.kaggle.com/theoviel/bert-pytorch-huggingface-starter
# - Thanks for sharing https://www.kaggle.com/theoviel

# In[ ]:


get_ipython().system('curl https://raw.githubusercontent.com/pytorch/xla/master/contrib/scripts/env-setup.py -o pytorch-xla-env-setup.py')
get_ipython().system('python pytorch-xla-env-setup.py --apt-packages libomp5 libopenblas-dev')


# In[ ]:


import gc
import os
import time
import math
import random
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from datetime import date
from transformers import *
from sklearn.metrics import *
from tqdm.notebook import tqdm

import torch
import torch.nn as nn
import torch.utils.data
import torch.nn.functional as F
import torch_xla


from torch import Tensor
from torch.optim import *
from torch.nn.modules.loss import *
from torch.optim.lr_scheduler import * 
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.sampler import RandomSampler


# In[ ]:


def seed_everything(seed):
    """
    Seeds basic parameters for reproductibility of results
    
    Arguments:
        seed {int} -- Number of the seed
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# In[ ]:


seed = 2020
seed_everything(seed)


# # Data

# In[ ]:


MODEL_PATHS = {
    'bert-multi-cased': '../input/bertconfigs/multi_cased_L-12_H-768_A-12/multi_cased_L-12_H-768_A-12/',
}


# In[ ]:


DATA_PATH = '../input/jigsaw-multilingual-toxic-comment-classification/'

df_val = pd.read_csv(DATA_PATH + 'validation-processed-seqlen128.csv')
df_test =  pd.read_csv(DATA_PATH + 'test-processed-seqlen128.csv')
df_train = pd.read_csv(DATA_PATH + 'jigsaw-toxic-comment-train-processed-seqlen128.csv')


# In[ ]:


sns.countplot(df_train['toxic'])
plt.title('Target repartition on training data')
plt.show()


# In[ ]:


class JigsawDataset(Dataset):
    """
    Torch dataset for training and validating
    """
    def __init__(self, df):
        super().__init__()
        self.df = df 
        self.word_ids = np.array([word_ids[1:-1].split(', ') for word_ids in df['input_word_ids']]).astype(int)
        
        try:
            self.y = df['toxic'].values
        except KeyError: # test data
            self.y = np.zeros(len(df))

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        return torch.tensor(self.word_ids[idx]), torch.tensor(self.y[idx])


# # Model

# In[ ]:


TRANSFORMERS = {
    "bert-multi-cased": (BertModel, BertTokenizer, "bert-base-uncased"),
}


# In[ ]:


class Transformer(nn.Module):
    def __init__(self, model, num_classes=1):
        """
        Constructor
        
        Arguments:
            model {string} -- Transformer to build the model on. Expects "camembert-base".
            num_classes {int} -- Number of classes (default: {1})
        """
        super().__init__()
        self.name = model

        model_class, tokenizer_class, pretrained_weights = TRANSFORMERS[model]

        bert_config = BertConfig.from_json_file(MODEL_PATHS[model] + 'bert_config.json')
        bert_config.output_hidden_states = True
        
        self.transformer = BertModel(bert_config)

        self.nb_features = self.transformer.pooler.dense.out_features

        self.pooler = nn.Sequential(
            nn.Linear(self.nb_features, self.nb_features), 
            nn.Tanh(),
        )

        self.logit = nn.Linear(self.nb_features, num_classes)

    def forward(self, tokens):
        """
        Usual torch forward function
        
        Arguments:
            tokens {torch tensor} -- Sentence tokens
        
        Returns:
            torch tensor -- Class logits
        """
        _, _, hidden_states = self.transformer(
            tokens, attention_mask=(tokens > 0).long()
        )

        hidden_states = hidden_states[-1][:, 0] # Use the representation of the first token of the last layer

        ft = self.pooler(hidden_states)

        return self.logit(ft)


# # Training

# In[ ]:


def fit(model, train_dataset, val_dataset, epochs=1, batch_size=8, warmup_prop=0, lr=5e-4):
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    optimizer = AdamW(model.parameters(), lr=lr)
    
    num_warmup_steps = int(warmup_prop * epochs * len(train_loader))
    num_training_steps = epochs * len(train_loader)
    
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps)

    loss_fct = nn.BCEWithLogitsLoss(reduction='mean').cuda()
    
    for epoch in range(epochs):
        model.train()
        start_time = time.time()
        
        optimizer.zero_grad()
        avg_loss = 0
        
        for step, (x, y_batch) in tqdm(enumerate(train_loader), total=len(train_loader)): 
            
            y_pred = model(x.to(device))
            
            loss = loss_fct(y_pred.view(-1).float(), y_batch.float().to(device))
            loss.backward()
            avg_loss += loss.item() / len(train_loader)

            xm.optimizer_step(optimizer, barrier=True)
            #optimizer.step()
            scheduler.step()
            model.zero_grad()
            optimizer.zero_grad()
                
        model.eval()
        preds = []
        truths = []
        avg_val_loss = 0.

        with torch.no_grad():
            for x, y_batch in tqdm(val_loader):                
                y_pred = model(x.to(device))
                loss = loss_fct(y_pred.detach().view(-1).float(), y_batch.float().to(device))
                avg_val_loss += loss.item() / len(val_loader)
                
                probs = torch.sigmoid(y_pred).detach().cpu().numpy()
                preds += list(probs.flatten())
                truths += list(y_batch.numpy().flatten())
            score = roc_auc_score(truths, preds)
            
        
        dt = time.time() - start_time
        lr = scheduler.get_last_lr()[0]
        print(f'Epoch {epoch + 1}/{epochs} \t lr={lr:.1e} \t t={dt:.0f}s \t loss={avg_loss:.4f} \t val_loss={avg_val_loss:.4f} \t val_auc={score:.4f}')


# In[ ]:


import torch_xla
import torch_xla.core.xla_model as xm


# In[ ]:


model = Transformer("bert-multi-cased")
device = xm.xla_device()
model = model.to(device)


# In[ ]:


epochs = 3
batch_size = 32
warmup_prop = 0.1
lr = 1e-4


# In[ ]:


df_train.shape


# In[ ]:


n = 10000  # I do not train on the entier data as it will take too long (for now)
train_dataset = JigsawDataset(df_train.sample(n))
#train_dataset = JigsawDataset(df_train)


# In[ ]:


val_dataset = JigsawDataset(df_val)
test_dataset = JigsawDataset(df_test)


# In[ ]:


fit(model, train_dataset, val_dataset, epochs=epochs, batch_size=batch_size, warmup_prop=warmup_prop, lr=lr)


# # Predicting

# In[ ]:


def predict(model, dataset, batch_size=64):
    """
    Usual predict torch function
    
    Arguments:
        model {torch model} -- Model to predict with
        dataset {torch dataset} -- Dataset to get predictions from
    
    Keyword Arguments:
        batch_size {int} -- Batch size (default: {32})
    
    Returns:
        numpy array -- Predictions
    """

    model.eval()
    preds = np.empty((0, 1))
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    with torch.no_grad():
        for x, _ in tqdm(loader):
            probs = torch.sigmoid(model(x.to(device))).detach().cpu().numpy()
            preds = np.concatenate([preds, probs])
            
    return preds


# In[ ]:


pred_val = predict(model, val_dataset)


# In[ ]:


score = roc_auc_score(df_val['toxic'], pred_val)
print(f'Scored {score:.4f} on validation data')


# In[ ]:


pred_test = predict(model, test_dataset)


# In[ ]:


sub = pd.read_csv(DATA_PATH + 'sample_submission.csv')
sub['toxic'] = pred_test
sub.to_csv('submission.csv', index=False)
sub.head()


# ### Training with TPU is faster thant Training with GPU
# ### 150s 1epoch -> 100s 1epoch

# In[ ]:




