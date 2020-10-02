#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
package_dir = "../input/ppbert/pytorch-pretrained-BERT/pytorch_pretrained_bert/"
sys.path.append(package_dir)


# In[ ]:


from __future__ import absolute_import, division, print_function
import torch.utils.data
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import warnings
from pytorch_pretrained_bert import BertTokenizer, BertForSequenceClassification, BertConfig, BertAdam

warnings.filterwarnings(action='once')
device = torch.device('cuda')


# In[ ]:


## Function to convert sentence into tokenized format

def convert_lines(example, max_seq_length, tokenizer):
    max_seq_length -=2
    all_tokens =[]
    longer = 0
    for text in tqdm(example):
        tokens_a = tokenizer.tokenize(text)
        if len(tokens_a) > max_seq_length:
            tokens_a = tokens_a[:max_seq_length]
            longer += 1
        one_token = tokenizer.convert_tokens_to_ids(["[CLS]"]+tokens_a+["[SEP]"]) +[0] * (max_seq_length - len(tokens_a))
        all_tokens.append(one_token)
    return np.array(all_tokens)


# In[ ]:


MAX_SEQUENCE_LENGTH = 220
SEED  = 7 
BATCH_SIZE = 32
BERT_MODEL_PATH = '../input/bert-pretrained-models/uncased_l-12_h-768_a-12/uncased_L-12_H-768_A-12/'


# In[ ]:


np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True


# In[ ]:


bert_config = BertConfig('../input/bert-inference/bert/bert_config.json')
tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_PATH, cache_dir = None, do_lower_case = True)


# In[ ]:


# reading test dataset
test_df = pd.read_csv("../input/jigsaw-unintended-bias-in-toxicity-classification/test.csv")
test_df['comment_text'] = test_df['comment_text'].astype('str')
X_test = convert_lines(example = test_df["comment_text"].fillna("DUMMY_VALUE"), max_seq_length = MAX_SEQUENCE_LENGTH, tokenizer = tokenizer)


# In[ ]:


model = BertForSequenceClassification(bert_config , num_labels = 1)
model.load_state_dict(torch.load('../input/bert-inference/bert/bert_pytorch.bin'))
model.to(device)
for param in model.parameters():
    param.requires_grad = False
model.eval()


# In[ ]:


test_preds = np.zeros(len(X_test))
test = torch.utils.data.TensorDataset(torch.tensor(X_test, dtype = torch.long))
test_loader =  torch.utils.data.DataLoader(test,batch_size = 32, shuffle = False)
tk0 = tqdm(test_loader)
for i, (x_batch,) in enumerate(tk0):
    pred = model(x_batch.to(device), attention_mask = (x_batch > 0).to(device), labels = None)
    test_preds[i*32:(i+1)*32] = pred[:,0].detach().cpu().squeeze().numpy()
test_pred = torch.sigmoid(torch.tensor(test_preds)).numpy().ravel()


# In[ ]:


submission = pd.DataFrame.from_dict({
    'id':test_df['id'],
    'prediction':test_pred
})
submission.to_csv("submission.csv", index = False)


# In[ ]:


submission.head()


# Reference:
# https://www.kaggle.com/abhishek/pytorch-bert-inference/notebook
