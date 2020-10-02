#!/usr/bin/env python
# coding: utf-8

# # Stater Pytorch TPU Google Colab
# 
# Hi every one this kernal based on [@abhishek](https://www.kaggle.com/abhishek)  keranl [bert-multi-lingual-tpu-training-8-cores-w-valid](https://www.kaggle.com/abhishek/bert-multi-lingual-tpu-training-8-cores-w-valid)  .
# 
# Same kernal setup in google colab free TPU 
# ### Colab Notebook : https://colab.research.google.com/drive/1CQMC6N6ZvbR0eB_hcEOutSlBKjNZjqOt
# 
# In this colab notebook steup three things :
# 
# 1. Download kaggle dataset to google colab.
# 2. Run the @abhishek sir model 
# 3. Upload trained weights to the kaggle dataset.
# 
# 

# ### Model

# In[ ]:


get_ipython().run_cell_magic('writefile', 'model.py', '\nimport os\nimport torch\nimport pandas as pd\nfrom scipy import stats\nimport numpy as np\n\nfrom tqdm import tqdm\nfrom collections import OrderedDict, namedtuple\nimport torch.nn as nn\nfrom torch.optim import lr_scheduler\nimport joblib\n\nimport logging\nimport transformers\nfrom transformers import AdamW, get_linear_schedule_with_warmup, get_constant_schedule\nimport sys\nfrom sklearn import metrics, model_selection\n\nimport warnings\nimport torch_xla\nimport torch_xla.debug.metrics as met\nimport torch_xla.distributed.data_parallel as dp\nimport torch_xla.distributed.parallel_loader as pl\nimport torch_xla.utils.utils as xu\nimport torch_xla.core.xla_model as xm\nimport torch_xla.distributed.xla_multiprocessing as xmp\nimport torch_xla.test.test_utils as test_utils\nimport warnings\n\nwarnings.filterwarnings("ignore")\n\n\nclass BERTBaseUncased(nn.Module):\n    def __init__(self, bert_path):\n        super(BERTBaseUncased, self).__init__()\n        self.bert_path = bert_path\n        self.bert = transformers.BertModel.from_pretrained(self.bert_path)\n        self.bert_drop = nn.Dropout(0.3)\n        self.out = nn.Linear(768 * 2, 1)\n\n    def forward(\n            self,\n            ids,\n            mask,\n            token_type_ids\n    ):\n        o1, o2 = self.bert(\n            ids,\n            attention_mask=mask,\n            token_type_ids=token_type_ids)\n        \n        apool = torch.mean(o1, 1)\n        mpool, _ = torch.max(o1, 1)\n        cat = torch.cat((apool, mpool), 1)\n\n        bo = self.bert_drop(cat)\n        p2 = self.out(bo)\n        return p2\n    \nclass BERTDatasetTraining:\n    def __init__(self, comment_text, targets, tokenizer, max_length):\n        self.comment_text = comment_text\n        self.tokenizer = tokenizer\n        self.max_length = max_length\n        self.targets = targets\n\n    def __len__(self):\n        return len(self.comment_text)\n\n    def __getitem__(self, item):\n        comment_text = str(self.comment_text[item])\n        comment_text = " ".join(comment_text.split())\n\n        inputs = self.tokenizer.encode_plus(\n            comment_text,\n            None,\n            add_special_tokens=True,\n            max_length=self.max_length,\n        )\n        ids = inputs["input_ids"]\n        token_type_ids = inputs["token_type_ids"]\n        mask = inputs["attention_mask"]\n        \n        padding_length = self.max_length - len(ids)\n        \n        ids = ids + ([0] * padding_length)\n        mask = mask + ([0] * padding_length)\n        token_type_ids = token_type_ids + ([0] * padding_length)\n        \n        return {\n            \'ids\': torch.tensor(ids, dtype=torch.long),\n            \'mask\': torch.tensor(mask, dtype=torch.long),\n            \'token_type_ids\': torch.tensor(token_type_ids, dtype=torch.long),\n            \'targets\': torch.tensor(self.targets[item], dtype=torch.float)\n        }\n\n    \ndef loss_fn(outputs, targets):\n    return nn.BCEWithLogitsLoss()(outputs, targets.view(-1, 1))\n\ndef train_loop_fn(data_loader, model, optimizer, device, scheduler=None):\n    model.train()\n\n    total_loss = 0\n\n    for bi, d in enumerate(data_loader):\n        ids = d["ids"]\n        mask = d["mask"]\n        token_type_ids = d["token_type_ids"]\n        targets = d["targets"]\n\n        ids = ids.to(device, dtype=torch.long)\n        mask = mask.to(device, dtype=torch.long)\n        token_type_ids = token_type_ids.to(device, dtype=torch.long)\n        targets = targets.to(device, dtype=torch.float)\n\n        optimizer.zero_grad()\n        outputs = model(\n            ids=ids,\n            mask=mask,\n            token_type_ids=token_type_ids\n        )\n\n        loss = loss_fn(outputs, targets)\n\n        total_loss += loss\n\n        if bi % 100 == 0:\n            xm.master_print(f\'bi={bi}, loss={loss}\')\n\n        loss.backward()\n        xm.optimizer_step(optimizer)\n        if scheduler is not None:\n            scheduler.step()\n\ndef eval_loop_fn(data_loader, model, device):\n    model.eval()\n    fin_targets = []\n    fin_outputs = []\n    for bi, d in enumerate(data_loader):\n        ids = d["ids"]\n        mask = d["mask"]\n        token_type_ids = d["token_type_ids"]\n        targets = d["targets"]\n\n        ids = ids.to(device, dtype=torch.long)\n        mask = mask.to(device, dtype=torch.long)\n        token_type_ids = token_type_ids.to(device, dtype=torch.long)\n        targets = targets.to(device, dtype=torch.float)\n\n        outputs = model(\n            ids=ids,\n            mask=mask,\n            token_type_ids=token_type_ids\n        )\n\n        targets_np = targets.cpu().detach().numpy().tolist()\n        outputs_np = outputs.cpu().detach().numpy().tolist()\n        fin_targets.extend(targets_np)\n        fin_outputs.extend(outputs_np)    \n\n    return fin_outputs, fin_targets\n\n\nmx = BERTBaseUncased(bert_path="bert-base-multilingual-uncased")\ndf_train1 = pd.read_csv("input/jigsaw-toxic-comment-train.csv", usecols=["comment_text", "toxic"]).fillna("none")\ndf_train2 = pd.read_csv("input/jigsaw-unintended-bias-train.csv", usecols=["comment_text", "toxic"]).fillna("none")\ndf_train = pd.concat([df_train1, df_train2], axis=0).reset_index(drop=True)\n#df_train = df_train_full.sample(frac=1).reset_index(drop=True)\n\ndf_valid = pd.read_csv(\'input/validation.csv\')\n\ntokenizer = transformers.BertTokenizer.from_pretrained("bert-base-multilingual-uncased", do_lower_case=True)\n\n\ndef _run():\n\n    MAX_LEN = 192\n    TRAIN_BATCH_SIZE = 64\n    EPOCHS = 5\n\n    train_targets = df_train.toxic.values\n    valid_targets = df_valid.toxic.values\n\n    train_dataset = BERTDatasetTraining(\n        comment_text=df_train.comment_text.values,\n        targets=train_targets,\n        tokenizer=tokenizer,\n        max_length=MAX_LEN\n    )\n\n    train_sampler = torch.utils.data.distributed.DistributedSampler(\n          train_dataset,\n          num_replicas=xm.xrt_world_size(),\n          rank=xm.get_ordinal(),\n          shuffle=True)\n\n    train_data_loader = torch.utils.data.DataLoader(\n        train_dataset,\n        batch_size=TRAIN_BATCH_SIZE,\n        sampler=train_sampler,\n        drop_last=True,\n        num_workers=4\n    )\n\n    valid_dataset = BERTDatasetTraining(\n        comment_text=df_valid.comment_text.values,\n        targets=valid_targets,\n        tokenizer=tokenizer,\n        max_length=MAX_LEN\n    )\n\n    valid_sampler = torch.utils.data.distributed.DistributedSampler(\n          valid_dataset,\n          num_replicas=xm.xrt_world_size(),\n          rank=xm.get_ordinal(),\n          shuffle=False)\n    \n\n    valid_data_loader = torch.utils.data.DataLoader(\n        valid_dataset,\n        batch_size=32,\n        sampler=valid_sampler,\n        drop_last=False,\n        num_workers=4\n    )\n\n    device = xm.xla_device()\n    model = mx.to(device)\n\n    param_optimizer = list(model.named_parameters())\n    no_decay = [\'bias\', \'LayerNorm.bias\', \'LayerNorm.weight\']\n    optimizer_grouped_parameters = [\n        {\'params\': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], \'weight_decay\': 0.001},\n        {\'params\': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], \'weight_decay\': 0.0}]\n\n    \n    lr = 0.4 * 1e-5 * xm.xrt_world_size()\n    num_train_steps = int(len(train_dataset) / TRAIN_BATCH_SIZE / xm.xrt_world_size() * EPOCHS)\n    xm.master_print(f\'num_train_steps = {num_train_steps}, world_size={xm.xrt_world_size()}\')\n\n    optimizer = AdamW(optimizer_grouped_parameters, lr=lr)\n    scheduler = get_linear_schedule_with_warmup(\n        optimizer,\n        num_warmup_steps=0,\n        num_training_steps=num_train_steps\n    )\n\n    for epoch in range(EPOCHS):\n        para_loader = pl.ParallelLoader(train_data_loader, [device])\n        train_loop_fn(para_loader.per_device_loader(device), model, optimizer, device, scheduler=scheduler)\n\n        para_loader = pl.ParallelLoader(valid_data_loader, [device])\n        o, t = eval_loop_fn(para_loader.per_device_loader(device), model, device)\n        auc = metrics.roc_auc_score(np.array(t) >= 0.5, o)\n        xm.save(model.state_dict(), f"drive/My Drive/Toxic_Comment_Classification_epoch_{epoch}_auc_{auc}.bin")\n        xm.master_print(f\'AUC = {auc}\')\n        \n        \n# Start training processes\ndef _mp_fn(rank, flags):\n    torch.set_default_tensor_type(\'torch.FloatTensor\')\n    a = _run()\n\nFLAGS={}\nxmp.spawn(_mp_fn, args=(FLAGS,), nprocs=8, start_method=\'fork\')')


# ## Inference

# In[ ]:


import os
import torch
import pandas as pd
from scipy import stats
import numpy as np
import pandas as pd

from tqdm import tqdm
from collections import OrderedDict, namedtuple
import torch.nn as nn
from torch.optim import lr_scheduler
import joblib

import logging
import transformers
import sys


# In[ ]:


class BERTBaseUncased(nn.Module):
    def __init__(self, bert_path):
        super(BERTBaseUncased, self).__init__()
        self.bert_path = bert_path
        self.bert = transformers.BertModel.from_pretrained(self.bert_path)
        self.bert_drop = nn.Dropout(0.3)
        self.out = nn.Linear(768 * 2, 1)

    def forward(
            self,
            ids,
            mask,
            token_type_ids
    ):
        o1, o2 = self.bert(
            ids,
            attention_mask=mask,
            token_type_ids=token_type_ids)
        
        apool = torch.mean(o1, 1)
        mpool, _ = torch.max(o1, 1)
        cat = torch.cat((apool, mpool), 1)

        bo = self.bert_drop(cat)
        p2 = self.out(bo)
        return p2

class BERTDatasetTest:
    def __init__(self, comment_text, tokenizer, max_length):
        self.comment_text = comment_text
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.comment_text)

    def __getitem__(self, item):
        comment_text = str(self.comment_text[item])
        comment_text = " ".join(comment_text.split())

        inputs = self.tokenizer.encode_plus(
            comment_text,
            None,
            add_special_tokens=True,
            max_length=self.max_length,
        )
        ids = inputs["input_ids"]
        token_type_ids = inputs["token_type_ids"]
        mask = inputs["attention_mask"]
        
        padding_length = self.max_length - len(ids)
        
        ids = ids + ([0] * padding_length)
        mask = mask + ([0] * padding_length)
        token_type_ids = token_type_ids + ([0] * padding_length)
        
        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long)
        }


# In[ ]:


df = pd.read_csv("../input/jigsaw-multilingual-toxic-comment-classification/test.csv")


# In[ ]:


tokenizer = transformers.BertTokenizer.from_pretrained("../input/bert-base-multilingual-uncased/", do_lower_case=True)


# In[ ]:


device = "cuda"
model = BERTBaseUncased(bert_path="../input/bert-base-multilingual-uncased/").to(device)
model.load_state_dict(torch.load("../input/tcc-bert-weights/Toxic_Comment_Classification_epoch_1_auc_0.81.bin"))
model.eval()


# In[ ]:


valid_dataset = BERTDatasetTest(
        comment_text=df.content.values,
        tokenizer=tokenizer,
        max_length=192
)

valid_data_loader = torch.utils.data.DataLoader(
    valid_dataset,
    batch_size=64,
    drop_last=False,
    num_workers=4,
    shuffle=False
)


with torch.no_grad():
    fin_outputs = []
    for bi, d in tqdm(enumerate(valid_data_loader)):
        ids = d["ids"]
        mask = d["mask"]
        token_type_ids = d["token_type_ids"]

        ids = ids.to(device, dtype=torch.long)
        mask = mask.to(device, dtype=torch.long)
        token_type_ids = token_type_ids.to(device, dtype=torch.long)

        outputs = model(
            ids=ids,
            mask=mask,
            token_type_ids=token_type_ids
        )

        outputs_np = outputs.cpu().detach().numpy().tolist()
        fin_outputs.extend(outputs_np)


# In[ ]:


df_en = pd.read_csv("../input/test-en-df/test_en.csv")

valid_dataset = BERTDatasetTest(
        comment_text=df_en.content_en.values,
        tokenizer=tokenizer,
        max_length=192
)

valid_data_loader = torch.utils.data.DataLoader(
    valid_dataset,
    batch_size=64,
    drop_last=False,
    num_workers=4,
    shuffle=False
)

with torch.no_grad():
    fin_outputs_en = []
    for bi, d in tqdm(enumerate(valid_data_loader)):
        ids = d["ids"]
        mask = d["mask"]
        token_type_ids = d["token_type_ids"]

        ids = ids.to(device, dtype=torch.long)
        mask = mask.to(device, dtype=torch.long)
        token_type_ids = token_type_ids.to(device, dtype=torch.long)

        outputs = model(
            ids=ids,
            mask=mask,
            token_type_ids=token_type_ids
        )

        outputs_np = outputs.cpu().detach().numpy().tolist()
        fin_outputs_en.extend(outputs_np)


# In[ ]:


df_en2 = pd.read_csv("../input/jigsaw-multilingual-toxic-test-translated/jigsaw_miltilingual_test_translated.csv")

valid_dataset = BERTDatasetTest(
        comment_text=df_en2.translated.values,
        tokenizer=tokenizer,
        max_length=192
)

valid_data_loader = torch.utils.data.DataLoader(
    valid_dataset,
    batch_size=64,
    drop_last=False,
    num_workers=4,
    shuffle=False
)

with torch.no_grad():
    fin_outputs_en2 = []
    for bi, d in tqdm(enumerate(valid_data_loader)):
        ids = d["ids"]
        mask = d["mask"]
        token_type_ids = d["token_type_ids"]

        ids = ids.to(device, dtype=torch.long)
        mask = mask.to(device, dtype=torch.long)
        token_type_ids = token_type_ids.to(device, dtype=torch.long)

        outputs = model(
            ids=ids,
            mask=mask,
            token_type_ids=token_type_ids
        )

        outputs_np = outputs.cpu().detach().numpy().tolist()
        fin_outputs_en2.extend(outputs_np)


# In[ ]:


fin_outputs_en = [item for sublist in fin_outputs_en for item in sublist]
fin_outputs_en2 = [item for sublist in fin_outputs_en2 for item in sublist]
fin_outputs = [item for sublist in fin_outputs for item in sublist]


# In[ ]:


sample = pd.read_csv("../input/jigsaw-multilingual-toxic-comment-classification/sample_submission.csv")
sample.loc[:, "toxic"] = (np.array(fin_outputs) + np.array(fin_outputs_en) + np.array(fin_outputs_en2)) / 3.0
sample.to_csv("submission.csv", index=False)


# In[ ]:


sample.head()


# In[ ]:





# In[ ]:




