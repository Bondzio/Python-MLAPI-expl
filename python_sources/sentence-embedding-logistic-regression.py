#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install -U sentence-transformers')
get_ipython().system('pip install biobert-embedding')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session



import seaborn as sns

import os
import sys
import tensorflow as tf
from biobert_embedding import downloader
from biobert_embedding.embedding import BiobertEmbedding
from sentence_transformers import SentenceTransformer,models

import torch
from torch.utils.data import DataLoader


from tqdm import tqdm

import math


# In[ ]:


## only trained on mnli, for sentence similarity

model_path = downloader.get_BioBert("google drive")
## downloading biobert


# In[ ]:


text="the recombinant protein reported here, together with the detailed structural information, might also be useful to others developing sars-cov-2 diagnostics and/or therapeutics."

biobert = BiobertEmbedding(model_path)

word_embeddings = biobert.word_vector(text)
sentence_embedding = biobert.sentence_vector(text)

print("Text Tokens: ", biobert.tokens)
#Text Tokens:  ['the', 'recombinant', 'protein', 'reported', 'here', ',', 'together', 'with', 'the', 'detailed', 'structural', 'information', ',', 'might', 'also', 'be', 'useful', 'to', 'others', 'developing', 'sars', '-', 'cov', '-', '2', 'diagnostics', 'and', '/', 'or', 'therapeutics', '.']

print ('Shape of Word Embeddings: %d x %d' % (len(word_embeddings), len(word_embeddings[0])))
# Shape of Word Embeddings: 31 x 768

print("Shape of Sentence Embedding = ",len(sentence_embedding))
# Shape of Sentence Embedding =  768


# In[ ]:


from sentence_transformers import models,losses
from sentence_transformers import SentenceTransformer,SentencesDataset
from sklearn.model_selection import train_test_split


# In[ ]:


df_mancon=pd.read_csv("/kaggle/input/mancon-corpus-cleaned/manconcorpus_sent_pairs.tsv",sep="\t").rename(columns={"guid":"pairID",
                                                                                                                 "text_a":"sentence1",
                                                                                                                 "text_b":"sentence2"}) ## manconcorp

df_snli=pd.read_csv("/kaggle/input/stanford-natural-language-inference-corpus/snli_1.0_train.csv") ## stanford nli

df_multinli=pd.read_csv("/kaggle/input/multinlicleaned/MultiNLI_cleaned.csv").drop("Unnamed: 0",axis=1)


# In[ ]:


df_nli=pd.concat([df_multinli[['gold_label','sentence1','sentence2','pairID']],
                    df_snli[['gold_label','sentence1','sentence2','pairID']]]).rename(columns={"gold_label":"label"})
## this has snli+multinli
df_nli=df_nli[df_nli['label']!="-"]
df_nli=df_nli.dropna(how="any").reset_index(drop=True) ## removing rows with null values


# In[ ]:


from sentence_transformers.readers import InputExample
from sentence_transformers.evaluation import *


# In[ ]:


class NLIDataReader(object):
    def __init__(self,dataframe):
        self.df=dataframe.copy()
    def get_examples(self,max_examples=0):
        s1=self.df["sentence1"].values
        s2=self.df["sentence2"].values
        labels=self.df["label"].values
        guid=self.df["pairID"].values
        examples = []
        for sentence_a, sentence_b, label, guid_id in zip(s1, s2, labels, guid):

            examples.append(InputExample(guid=guid_id, texts=[sentence_a, sentence_b], label=self.map_label(label)))

            if 0 < max_examples <= len(examples):
                break

        return examples
    
    
    
    @staticmethod
    def get_labels():
        return {"contradiction": 0, "entailment": 1, "neutral": 2}

    def get_num_labels(self):
        return len(self.get_labels())

    def map_label(self, label):
        return self.get_labels()[label.strip().lower()]


# In[ ]:


def get_labels():
        return {"contradiction": 0, "entailment": 1, "neutral": 2}


# In[ ]:


df_nlitrain,df_nlitest=train_test_split(df_nli,test_size=0.2,random_state=42)
df_nlitest,df_nlival=train_test_split(df_nlitest,test_size=0.5,random_state=42)

df_mancontrain,df_mancontest=train_test_split(df_mancon,test_size=0.2,random_state=42)
df_mancontest,df_manconval=train_test_split(df_mancontest,test_size=0.5,random_state=42)


# In[ ]:


model_save_path="/kaggle/input/model-weights-sbert-trained-on-these-data/model_mnli_mancon/model_mnli_mancon" # trained on mnli + part mancon, for sentence similarity
model = SentenceTransformer(model_save_path)

sentence_embeddings = model.encode([text])
print("Shape of Sentence Embedding = ",len(sentence_embedding))


# In[ ]:


sentence_embeddings


# In[ ]:


get_ipython().run_cell_magic('capture', '', "df_mancontest['sentence1_embedding']=df_mancontest['sentence1'].apply(lambda x: np.array(model.encode([x])[0]))\ndf_mancontest['sentence2_embedding']=df_mancontest['sentence2'].apply(lambda x: np.array(model.encode([x])[0]))")


# In[ ]:


get_ipython().run_cell_magic('capture', '', "df_mancon['sentence1_embedding']=df_mancon['sentence1'].apply(lambda x: np.array(model.encode([x])[0]))\ndf_mancon['sentence2_embedding']=df_mancon['sentence2'].apply(lambda x: np.array(model.encode([x])[0]))")


# In[ ]:


df_mancon['cosine_sim']=df_mancon.apply(lambda x: np.dot(x['sentence1_embedding'],x['sentence2_embedding'])/
                                                (np.linalg.norm(x['sentence1_embedding'])*np.linalg.norm(x['sentence2_embedding'])),axis=1)


# In[ ]:


ax=sns.boxplot(x="label",y="cosine_sim",data=df_mancon)


# In[ ]:


sns.countplot(df_mancon['label'])


# In[ ]:


df_mancon['vector']=df_mancon.apply(lambda x: np.array(x.sentence1_embedding.tolist()+x.sentence2_embedding.tolist()),axis=1)


# In[ ]:


df_mancon['target']=df_mancon['label'].apply(lambda x:get_labels()[x])


# In[ ]:


from sklearn.linear_model import LogisticRegression


# In[ ]:


train_data=df_mancon['vector'].values
train_data = np.vstack(train_data[:][:])
train_target=df_mancon['target'].values


# In[ ]:


logreg=LogisticRegression()
logreg.fit(train_data,train_target)


# In[ ]:


get_ipython().run_cell_magic('capture', '', "df_mancontest['sentence1_embedding']=df_mancontest['sentence1'].apply(lambda x: np.array(model.encode([x])[0]))\ndf_mancontest['sentence2_embedding']=df_mancontest['sentence2'].apply(lambda x: np.array(model.encode([x])[0]))\ndf_mancontest['cosine_sim']=df_mancontest.apply(lambda x: np.dot(x['sentence1_embedding'],x['sentence2_embedding'])/\n                                                (np.linalg.norm(x['sentence1_embedding'])*np.linalg.norm(x['sentence2_embedding'])),axis=1)\ndf_mancontest['vector']=df_mancontest.apply(lambda x: np.array(x.sentence1_embedding.tolist()+x.sentence2_embedding.tolist()),axis=1)\ndf_mancontest['target']=df_mancontest['label'].apply(lambda x:get_labels()[x])\n\ntest_data=df_mancontest['vector'].values\ntest_data = np.vstack(test_data[:][:])\ntest_target=df_mancontest['target'].values")


# In[ ]:


test_result=logreg.predict(test_data)


# In[ ]:


ax=sns.boxplot(x="label",y="cosine_sim",data=df_mancontest)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report


# In[ ]:


confusion_matrix(test_target,test_result)


# In[ ]:


print(classification_report(test_target,test_result))


# In[ ]:


sample_df=pd.read_excel("/kaggle/input/annotation-drug-similarity/new_annotations_05072020.xlsx")


# In[ ]:


sample_df.columns


# In[ ]:


contradiction_df.columns


# In[ ]:


contradiction_df=sample_df[["paper1_cord_uid","paper2_cord_uid","claim_1","claim_2","label"]]
contradiction_df.rename(columns={"claim_1":"sentence1","claim_2":"sentence2"},inplace=True)
contradiction_df.label.unique()


# In[ ]:


contradiction_df.label=contradiction_df.label.apply(lambda x:"neutral" if "Neutral" in x else "contradiction" 
                                                              if "Contradiction" in x else "entailment" 
                                                              if "Entailment" in x else np.nan)


# In[ ]:


contradiction_df.head()


# In[ ]:


contradiction_df=contradiction_df[~contradiction_df.label.isna()]


# In[ ]:


get_ipython().run_cell_magic('capture', '', "contradiction_df['sentence1_embedding']=contradiction_df['sentence1'].apply(lambda x: np.array(model.encode([x])[0]))\ncontradiction_df['sentence2_embedding']=contradiction_df['sentence2'].apply(lambda x: np.array(model.encode([x])[0]))\ncontradiction_df['vector']=contradiction_df.apply(lambda x: np.array(x.sentence1_embedding.tolist()+x.sentence2_embedding.tolist()),axis=1)\ncontradiction_df['target']=contradiction_df['label'].apply(lambda x:get_labels()[x])\n\ntest_data_final=contradiction_df['vector'].values\ntest_data_final = np.vstack(test_data_final[:][:])\ntest_target=contradiction_df['target'].values")


# In[ ]:


contradiction_df['cosine_sim']=contradiction_df.apply(lambda x: np.dot(x['sentence1_embedding'],x['sentence2_embedding'])/
                                                (np.linalg.norm(x['sentence1_embedding'])*np.linalg.norm(x['sentence2_embedding'])),axis=1)


# In[ ]:


ax=sns.boxplot(x="label",y="cosine_sim",data=contradiction_df)


# In[ ]:


test_result=logreg.predict(test_data_final)


# In[ ]:


print(classification_report(test_target,test_result))


# In[ ]:


get_labels()


# In[ ]:


contradiction_df['predicted']=test_result


# In[ ]:


contradiction_df.to_csv("Result_annotation.csv",index=False)


# In[ ]:




