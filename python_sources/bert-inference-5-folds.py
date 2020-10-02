#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
import tokenizers
import string
import torch
import transformers
import torch.nn as nn
from torch.nn import functional as F
from tqdm import tqdm
import re


# In[ ]:


MAX_LEN = 160
TRAIN_BATCH_SIZE = 32
VALID_BATCH_SIZE = 16
EPOCHS = 15
BERT_PATH = "../input/bert-base-uncased/"
MODEL_PATH = "model.bin"
TRAINING_FILE = "../input/train_folds.csv"
TOKENIZER = tokenizers.BertWordPieceTokenizer(
    f"{BERT_PATH}/vocab.txt", 
    lowercase=True
)


# In[ ]:


class TweetModel(transformers.BertPreTrainedModel):
    def __init__(self, conf):
        super(TweetModel, self).__init__(conf)
        self.bert = transformers.BertModel(conf)
        self.drop_out = nn.Dropout(0.1)
        self.l0 = nn.Linear(768 * 2, 2)
        torch.nn.init.normal_(self.l0.weight, std=0.02)
    
    def forward(self, ids, mask, token_type_ids):
        _, _, out = self.bert(
            ids,
            attention_mask=mask,
            token_type_ids=token_type_ids
        )

        out = torch.cat((out[-1], out[-2]), dim=-1)
        out = self.drop_out(out)
        logits = self.l0(out)

        start_logits, end_logits = logits.split(1, dim=-1)

        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)

        return start_logits, end_logits


# In[ ]:


def process_data(tweet, selected_text, sentiment, tokenizer, max_len):    
    tweet = " ".join(str(tweet).split())
    selected_text = " ".join(str(selected_text).split())

    len_st = len(selected_text)
    idx0 = None
    idx1 = None
    for ind in (i for i, e in enumerate(tweet) if e == selected_text[0]):
        if tweet[ind: ind+len_st] == selected_text:
            idx0 = ind
            idx1 = ind + len_st
            break

    char_targets = [0] * len(tweet)
    if idx0 != None and idx1 != None:
        for ct in range(idx0, idx1):
            char_targets[ct] = 1
    
    tok_tweet = tokenizer.encode(tweet)
    input_ids_orig = tok_tweet.ids[1:-1]
    tweet_offsets = tok_tweet.offsets[1:-1]
    
    target_idx = []
    for j, (offset1, offset2) in enumerate(tweet_offsets):
        if sum(char_targets[offset1: offset2]) > 0:
            target_idx.append(j)
    
    targets_start = target_idx[0]
    targets_end = target_idx[-1]

    sentiment_id = {
        'positive': 3893,
        'negative': 4997,
        'neutral': 8699
    }
    
    input_ids = [101] + [sentiment_id[sentiment]] + [102] + input_ids_orig + [102]
    token_type_ids = [0, 0, 0] + [1] * (len(input_ids_orig) + 1)
    mask = [1] * len(token_type_ids)
    tweet_offsets = [(0, 0)] * 3 + tweet_offsets + [(0, 0)]
    targets_start += 3
    targets_end += 3

    padding_length = max_len - len(input_ids)
    if padding_length > 0:
        input_ids = input_ids + ([0] * padding_length)
        mask = mask + ([0] * padding_length)
        token_type_ids = token_type_ids + ([1] * padding_length)
        tweet_offsets = tweet_offsets + ([(0, 0)] * padding_length)
    
    return {
        'ids': input_ids,
        'mask': mask,
        'token_type_ids': token_type_ids,
        'targets_start': targets_start,
        'targets_end': targets_end,
        'orig_tweet': tweet,
        'orig_selected': selected_text,
        'sentiment': sentiment,
        'offsets': tweet_offsets
    }


class TweetDataset:
    def __init__(self, tweet, sentiment, selected_text):
        self.tweet = tweet
        self.sentiment = sentiment
        self.selected_text = selected_text
        self.tokenizer = TOKENIZER
        self.max_len = MAX_LEN
    
    def __len__(self):
        return len(self.tweet)

    def __getitem__(self, item):
        data = process_data(
            self.tweet[item], 
            self.selected_text[item], 
            self.sentiment[item],
            self.tokenizer,
            self.max_len
        )

        return {
            'ids': torch.tensor(data["ids"], dtype=torch.long),
            'mask': torch.tensor(data["mask"], dtype=torch.long),
            'token_type_ids': torch.tensor(data["token_type_ids"], dtype=torch.long),
            'targets_start': torch.tensor(data["targets_start"], dtype=torch.long),
            'targets_end': torch.tensor(data["targets_end"], dtype=torch.long),
            'orig_tweet': data["orig_tweet"],
            'orig_selected': data["orig_selected"],
            'sentiment': data["sentiment"],
            'offsets_start': torch.tensor([x for x, _ in data["offsets"]], dtype=torch.long),
            'offsets_end': torch.tensor([x for _, x in data["offsets"]], dtype=torch.long)
        }


# In[ ]:


def calculate_jaccard_score(
    original_tweet, 
    target_string, 
    sentiment_val, 
    idx_start, 
    idx_end, 
    offsets_start, 
    offsets_end,
    verbose=False):

    offsets = list(zip(offsets_start, offsets_end))
    
    if idx_end < idx_start:
        idx_end = idx_start
    
    filtered_output  = ""
    original_tweet_sp = " ".join(original_tweet.split())
    for ix in range(idx_start, idx_end + 1):
        if offsets[ix][0] == 0 and offsets[ix][1] == 0:
            continue
        filtered_output += original_tweet_sp[offsets[ix][0]: offsets[ix][1]]
        if (ix+1) < len(offsets) and offsets[ix][1] < offsets[ix+1][0]:
            filtered_output += " "

    filtered_output = filtered_output.replace(" .", ".")
    filtered_output = filtered_output.replace(" ?", "?")
    filtered_output = filtered_output.replace(" !", "!")
    filtered_output = filtered_output.replace(" ,", ",")
    filtered_output = filtered_output.replace(" ' ", "'")
    filtered_output = filtered_output.replace(" n't", "n't")
    filtered_output = filtered_output.replace(" 'm", "'m")
    filtered_output = filtered_output.replace(" do not", " don't")
    filtered_output = filtered_output.replace(" 's", "'s")
    filtered_output = filtered_output.replace(" 've", "'ve")
    filtered_output = filtered_output.replace(" 're", "'re")

    if sentiment_val == "neutral":
        filtered_output = original_tweet

    if sentiment_val != "neutral" and verbose == True:
        if filtered_output.strip().lower() != target_string.strip().lower():
            print("********************************")
            print(f"Output= {filtered_output.strip()}")
            print(f"Target= {target_string.strip()}")
            print(f"Tweet= {original_tweet.strip()}")
            print("********************************")

    jac = 0
    return jac, filtered_output


# In[ ]:


df_test = pd.read_csv("../input/tweet-sentiment-extraction/test.csv")
df_test.loc[:, "selected_text"] = df_test.text.values


# In[ ]:


device = torch.device("cuda")
model_config = transformers.BertConfig.from_pretrained(BERT_PATH)
model_config.output_hidden_states = True


# In[ ]:


model1 = TweetModel(conf=model_config)
model1.to(device)
model1.load_state_dict(torch.load("../input/tweet-bert-base/model_0.bin"))
model1.eval()

model2 = TweetModel(conf=model_config)
model2.to(device)
model2.load_state_dict(torch.load("../input/tweet-bert-base/model_1.bin"))
model2.eval()

model3 = TweetModel(conf=model_config)
model3.to(device)
model3.load_state_dict(torch.load("../input/tweet-bert-base/model_2.bin"))
model3.eval()

model4 = TweetModel(conf=model_config)
model4.to(device)
model4.load_state_dict(torch.load("../input/tweet-bert-base/model_3.bin"))
model4.eval()

model5 = TweetModel(conf=model_config)
model5.to(device)
model5.load_state_dict(torch.load("../input/tweet-bert-base/model_4.bin"))
model5.eval()


# In[ ]:


final_output = []


# In[ ]:


test_dataset = TweetDataset(
        tweet=df_test.text.values,
        sentiment=df_test.sentiment.values,
        selected_text=df_test.selected_text.values
    )

data_loader = torch.utils.data.DataLoader(
    test_dataset,
    shuffle=False,
    batch_size=VALID_BATCH_SIZE,
    num_workers=1
)


with torch.no_grad():
    tk0 = tqdm(data_loader, total=len(data_loader))
    for bi, d in enumerate(tk0):
        ids = d["ids"]
        token_type_ids = d["token_type_ids"]
        mask = d["mask"]
        sentiment = d["sentiment"]
        orig_selected = d["orig_selected"]
        orig_tweet = d["orig_tweet"]
        targets_start = d["targets_start"]
        targets_end = d["targets_end"]
        offsets_start = d["offsets_start"].numpy()
        offsets_end = d["offsets_end"].numpy()

        ids = ids.to(device, dtype=torch.long)
        token_type_ids = token_type_ids.to(device, dtype=torch.long)
        mask = mask.to(device, dtype=torch.long)
        targets_start = targets_start.to(device, dtype=torch.long)
        targets_end = targets_end.to(device, dtype=torch.long)

        outputs_start1, outputs_end1 = model1(
            ids=ids,
            mask=mask,
            token_type_ids=token_type_ids
        )
        
        outputs_start2, outputs_end2 = model2(
            ids=ids,
            mask=mask,
            token_type_ids=token_type_ids
        )
        
        outputs_start3, outputs_end3 = model3(
            ids=ids,
            mask=mask,
            token_type_ids=token_type_ids
        )
        
        outputs_start4, outputs_end4 = model4(
            ids=ids,
            mask=mask,
            token_type_ids=token_type_ids
        )
        
        outputs_start5, outputs_end5 = model5(
            ids=ids,
            mask=mask,
            token_type_ids=token_type_ids
        )
        outputs_start = (outputs_start1 + outputs_start2 + outputs_start3 + outputs_start4 + outputs_start5) / 5
        outputs_end = (outputs_end1 + outputs_end2 + outputs_end3 + outputs_end4 + outputs_end5) / 5
        
        outputs_start = torch.softmax(outputs_start, dim=1).cpu().detach().numpy()
        outputs_end = torch.softmax(outputs_end, dim=1).cpu().detach().numpy()
        jaccard_scores = []
        for px, tweet in enumerate(orig_tweet):
            selected_tweet = orig_selected[px]
            tweet_sentiment = sentiment[px]
            jaccard_score, output_sentence = calculate_jaccard_score(
                original_tweet=tweet,
                target_string=selected_tweet,
                sentiment_val=tweet_sentiment,
                idx_start=np.argmax(outputs_start[px, :]),
                idx_end=np.argmax(outputs_end[px, :]),
                offsets_start=offsets_start[px, :],
                offsets_end=offsets_end[px, :]
            )
            jaccard_scores.append(jaccard_score)
            final_output.append(output_sentence)


# In[ ]:





# In[ ]:





# In[ ]:


sample = pd.read_csv("../input/tweet-sentiment-extraction/sample_submission.csv")
sample.loc[:, 'selected_text'] = final_output
sample.to_csv("submission.csv", index=False)


# In[ ]:


sample.head()


# In[ ]:




