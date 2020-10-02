#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
import warnings
import random
import torch 
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from sklearn.model_selection import StratifiedKFold
import tokenizers
from transformers import RobertaModel, RobertaConfig
from tqdm import tqdm

warnings.filterwarnings('ignore')


# In[ ]:


seed=42


# In[ ]:


class TweetDataset(torch.utils.data.Dataset):
    def __init__(self, df, max_len=96):
        self.df = df
        self.max_len = max_len
        self.labeled = 'selected_text' in df
        self.tokenizer = tokenizers.ByteLevelBPETokenizer(
            vocab_file='../input/roberta-base/vocab.json', 
            merges_file='../input/roberta-base/merges.txt', 
            lowercase=True,
            add_prefix_space=True)

    def __getitem__(self, index):
        data = {}
        row = self.df.iloc[index]
        
        ids, masks, tweet, offsets = self.get_input_data(row)
        data['ids'] = ids
        data['masks'] = masks
        data['tweet'] = tweet
        data['offsets'] = offsets
        
        if self.labeled:
            start_idx, end_idx = self.get_target_idx(row, tweet, offsets)
            data['start_idx'] = start_idx
            data['end_idx'] = end_idx
        
        return data

    def __len__(self):
        return len(self.df)
    
    def get_input_data(self, row):
        tweet = " " + " ".join(row.text.lower().split())
        encoding = self.tokenizer.encode(tweet)
        sentiment_id = self.tokenizer.encode(row.sentiment).ids
        ids = [0] + sentiment_id + [2, 2] + encoding.ids + [2]
        offsets = [(0, 0)] * 4 + encoding.offsets + [(0, 0)]
                
        pad_len = self.max_len - len(ids)
        if pad_len > 0:
            ids += [1] * pad_len
            offsets += [(0, 0)] * pad_len
        
        ids = torch.tensor(ids)
        masks = torch.where(ids != 1, torch.tensor(1), torch.tensor(0))
        offsets = torch.tensor(offsets)
        
        return ids, masks, tweet, offsets
        
    def get_target_idx(self, row, tweet, offsets):
        selected_text = " " +  " ".join(row.selected_text.lower().split())

        len_st = len(selected_text) - 1
        idx0 = None
        idx1 = None

        for ind in (i for i, e in enumerate(tweet) if e == selected_text[1]):
            if " " + tweet[ind: ind+len_st] == selected_text:
                idx0 = ind
                idx1 = ind + len_st - 1
                break

        char_targets = [0] * len(tweet)
        if idx0 != None and idx1 != None:
            for ct in range(idx0, idx1 + 1):
                char_targets[ct] = 1

        target_idx = []
        for j, (offset1, offset2) in enumerate(offsets):
            if sum(char_targets[offset1: offset2]) > 0:
                target_idx.append(j)

        start_idx = target_idx[0]
        end_idx = target_idx[-1]
        
        return start_idx, end_idx
        
def get_train_val_loaders(df, train_idx, val_idx, batch_size=8):
    train_df = df.iloc[train_idx]
    val_df = df.iloc[val_idx]

    train_loader = torch.utils.data.DataLoader(
        TweetDataset(train_df), 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=2,
        drop_last=True)

    val_loader = torch.utils.data.DataLoader(
        TweetDataset(val_df), 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=2)

    dataloaders_dict = {"train": train_loader, "val": val_loader}

    return dataloaders_dict

def get_test_loader(df, batch_size=32):
    loader = torch.utils.data.DataLoader(
        TweetDataset(df), 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=2)    
    return loader


# In[ ]:


class TweetModel(nn.Module):
    def __init__(self):
        super(TweetModel, self).__init__()
        
        config = RobertaConfig.from_pretrained(
            '../input/roberta-base/config.json', output_hidden_states=True)    
        self.roberta = RobertaModel.from_pretrained(
            '../input/roberta-base/pytorch_model.bin', config=config)
        self.dropout = nn.Dropout(0.5)
        self.conv1 = nn.Conv1d(in_channels=768, out_channels=768, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(in_channels=768, out_channels=64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv1d(in_channels=768, out_channels=768, kernel_size=3, padding=1)
        self.conv4 = nn.Conv1d(in_channels=768, out_channels=64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64, 1)
        self.fc2 = nn.Linear(64, 1)
        nn.init.normal_(self.fc1.weight, std=0.02)
        nn.init.normal_(self.fc1.bias, 0)
        nn.init.normal_(self.fc2.weight, std=0.02)
        nn.init.normal_(self.fc2.bias, 0)
        nn.init.xavier_normal_(self.conv1.weight)
        nn.init.xavier_normal_(self.conv2.weight)
        nn.init.xavier_normal_(self.conv3.weight)
        nn.init.xavier_normal_(self.conv4.weight)

    def forward(self, input_ids, attention_mask):
        _, _, hs = self.roberta(input_ids, attention_mask)
         
        x = torch.stack([hs[-1], hs[-2], hs[-3], hs[-4]])
        x = torch.mean(x, 0)
        x = self.dropout(x)
        
        x1=x.permute(0,2,1)
        x1 = self.conv1(x1)
        x1 = self.conv2(F.leaky_relu(x1))
        x1 = x1.permute(0,2,1)
        x1 = self.fc1(x1)
        start_logits = x1.squeeze(-1)
        
        x2 = x.permute(0,2,1)
        x2 = self.conv3(x2)
        x2 = self.conv4(F.leaky_relu(x2))
        x2 = x2.permute(0,2,1)
        x2 = self.fc2(x2)
        end_logits = x2.squeeze(-1)
                
        return start_logits, end_logits


# In[ ]:


def loss_fn(start_logits, end_logits, start_positions, end_positions):
    ce_loss = nn.CrossEntropyLoss()
    start_loss = ce_loss(start_logits, start_positions)
    end_loss = ce_loss(end_logits, end_positions)    
    total_loss = start_loss + end_loss
    return total_loss


# In[ ]:


def get_selected_text(text, start_idx, end_idx, offsets):
    selected_text = ""
    for ix in range(start_idx, end_idx + 1):
        selected_text += text[offsets[ix][0]: offsets[ix][1]]
        if (ix + 1) < len(offsets) and offsets[ix][1] < offsets[ix + 1][0]:
            selected_text += " "
    return selected_text

def jaccard(str1, str2): 
    a = set(str1.lower().split()) 
    b = set(str2.lower().split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def compute_jaccard_score(text, start_idx, end_idx, start_logits, end_logits, offsets):
    start_pred = np.argmax(start_logits)
    end_pred = np.argmax(end_logits)
    if start_pred > end_pred:
        pred = text
    else:
        pred = get_selected_text(text, start_pred, end_pred, offsets)
        
    true = get_selected_text(text, start_idx, end_idx, offsets)
    
    return jaccard(true, pred)


# In[ ]:


def train_model(model, dataloaders_dict, criterion, optimizer, num_epochs, filename):
    model.cuda()

    for epoch in range(num_epochs):
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            epoch_loss = 0.0
            epoch_jaccard = 0.0
            
            for data in (dataloaders_dict[phase]):
                ids = data['ids'].cuda()
                masks = data['masks'].cuda()
                tweet = data['tweet']
                offsets = data['offsets'].numpy()
                start_idx = data['start_idx'].cuda()
                end_idx = data['end_idx'].cuda()

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):

                    start_logits, end_logits = model(ids, masks)

                    loss = criterion(start_logits, end_logits, start_idx, end_idx)
                    
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                    epoch_loss += loss.item() * len(ids)
                    
                    start_idx = start_idx.cpu().detach().numpy()
                    end_idx = end_idx.cpu().detach().numpy()
                    start_logits = torch.softmax(start_logits, dim=1).cpu().detach().numpy()
                    end_logits = torch.softmax(end_logits, dim=1).cpu().detach().numpy()
                    
                    for i in range(len(ids)):                        
                        jaccard_score = compute_jaccard_score(
                            tweet[i],
                            start_idx[i],
                            end_idx[i],
                            start_logits[i], 
                            end_logits[i], 
                            offsets[i])
                        epoch_jaccard += jaccard_score
                    
            epoch_loss = epoch_loss / len(dataloaders_dict[phase].dataset)
            epoch_jaccard = epoch_jaccard / len(dataloaders_dict[phase].dataset)
            
            print('Epoch {}/{} | {:^5} | Loss: {:.4f} | Jaccard: {:.4f}'.format(
                epoch + 1, num_epochs, phase, epoch_loss, epoch_jaccard))
        
        if epoch<2:
            jaccard_check=epoch_jaccard
            torch.save(model.state_dict(), filename)
            print('Saving model')
        elif epoch_jaccard>jaccard_check:
            jaccard_check=epoch_jaccard
            torch.save(model.state_dict(), filename)
            print('Saving model')
        else:
            print('Stopping iteration')
            break


# In[ ]:


num_epochs = 10
batch_size = 32
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)


# In[ ]:


get_ipython().run_cell_magic('time', '', "\ntrain_df = pd.read_csv('../input/tweet-sentiment-extraction/train.csv')\ntrain_df['text'] = train_df['text'].astype(str)\ntrain_df['selected_text'] = train_df['selected_text'].astype(str)\n\nfor fold, (train_idx, val_idx) in enumerate(skf.split(train_df, train_df.sentiment), start=1): \n    print(f'Fold: {fold}')\n\n    model = TweetModel()\n    optimizer = optim.AdamW(model.parameters(), lr=4e-5, betas=(0.9, 0.999))\n    criterion = loss_fn    \n    dataloaders_dict = get_train_val_loaders(train_df, train_idx, val_idx, batch_size)\n\n    train_model(\n        model, \n        dataloaders_dict,\n        criterion, \n        optimizer, \n        num_epochs,\n        f'roberta_fold{fold}.pth')")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\ntest_df = pd.read_csv('../input/tweet-sentiment-extraction/test.csv')\ntest_df['text'] = test_df['text'].astype(str)\ntest_loader = get_test_loader(test_df)\npredictions = []\nmodels = []\nfor fold in range(skf.n_splits):\n    model = TweetModel()\n    model.cuda()\n    model.load_state_dict(torch.load(f'roberta_fold{fold+1}.pth'))\n    model.eval()\n    models.append(model)\n\nfor data in test_loader:\n    ids = data['ids'].cuda()\n    masks = data['masks'].cuda()\n    tweet = data['tweet']\n    offsets = data['offsets'].numpy()\n\n    start_logits = []\n    end_logits = []\n    for model in models:\n        with torch.no_grad():\n            output = model(ids, masks)\n            start_logits.append(torch.softmax(output[0], dim=1).cpu().detach().numpy())\n            end_logits.append(torch.softmax(output[1], dim=1).cpu().detach().numpy())\n\n    start_logits = np.mean(start_logits, axis=0)\n    end_logits = np.mean(end_logits, axis=0)\n    for i in range(len(ids)):    \n        start_pred = np.argmax(start_logits[i])\n        end_pred = np.argmax(end_logits[i])\n        if start_pred > end_pred:\n            pred = tweet[i]\n        else:\n            pred = get_selected_text(tweet[i], start_pred, end_pred, offsets[i])\n        predictions.append(pred)")


# In[ ]:


sub_df = pd.read_csv('../input/tweet-sentiment-extraction/sample_submission.csv')
sub_df['selected_text'] = predictions
sub_df['selected_text'] = sub_df['selected_text'].apply(lambda x: x.replace('!!!!', '!') if len(x.split())==1 else x)
sub_df['selected_text'] = sub_df['selected_text'].apply(lambda x: x.replace('..', '.') if len(x.split())==1 else x)
sub_df['selected_text'] = sub_df['selected_text'].apply(lambda x: x.replace('...', '.') if len(x.split())==1 else x)
sub_df.to_csv('submission.csv', index=False)
sub_df.head()

