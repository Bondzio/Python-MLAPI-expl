#!/usr/bin/env python
# coding: utf-8

# # # This is a notebook that address models and open questions related to COVID-19

# # Prepare data

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import glob
import json
import re
import scipy as sc
import warnings

import matplotlib.pyplot as plt
import os


# In[ ]:


root_path = '/kaggle/input/CORD-19-research-challenge/'
metadata_path = f'{root_path}/metadata.csv'
meta_df = pd.read_csv(metadata_path, dtype={
    'pubmed_id': str,
    'Microsoft Academic Paper ID': str, 
    'doi': str
})
meta_df.head()
meta_df.info()


# In[ ]:


meta_df.head()


# # Get data from Prepared data. This data is created in another notebook in kaggle I made.
# 
# Cite:
# https://www.kaggle.com/nike0good/population-studies-that-related-to-covid-19

# In[ ]:


df=pd.read_csv('../input/covid19prepareddata/Prepared_data.csv')
df.head()
df.info()


# # Check the keywords of the problems.

# Specifically, we want to know what the literature reports about:
# 
# - How can we measure changes in COVID-19_s behavior in a **human host** as the virus **evolves** over time_
# - **Human immune** response to COVID-19
# - What is known about **adaptations** (mutations) of the virus_.csv
# - Studies to monitor **potential adaptations**
# - Are there studies about **phenotypic change**?
# - **Changes** in COVID-19 as the **virus evolves**
# - What **regional** **genetic variations** (mutations) exist
# - What do models for **transmission predict**?
# - **Serial Interval** (time between symptom onset in infector-infectee pair)
# - Efforts to develop **qualitative assessment frameworks**
# 

# In[ ]:


task1="""Specifically, we want to know what the literature reports about:Specifically, we want to know what the literature reports about:

How can we measure changes in COVID-19_s behavior in a human host as the virus evolves over time_
Human immune response to COVID-19
What is known about adaptations (mutations) of the virus_.csv
Studies to monitor potential adaptations
Are there studies about phenotypic change?
Changes in COVID-19 as the virus evolves
What regional genetic variations (mutations) exist
What do models for transmission predict?
Serial Interval (time between symptom onset in infector-infectee pair)
Efforts to develop qualitative assessment frameworks"""


# In[ ]:


task=[task1]
query=[]
for i in range(len(task)):
    task[i]=task[i].split("\n")
    query.append(task[i][2:])
print(query)


# In[ ]:


get_ipython().system('pip install -U sentence-transformers')


# In[ ]:


from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

warnings.filterwarnings("ignore")
model = SentenceTransformer('bert-base-nli-mean-tokens')
    


# In[ ]:


query_embeddings=[]
for i in range(len(query)):
    query_embeddings.append(model.encode(query[i]))


# In[ ]:


df.reset_index(drop = True, inplace = True)
df['abstract_summary']
abstract_summary_embeddings = model.encode(df['abstract_summary'])


# In[ ]:


def getfile_insensitive(path):
    directory, filename = os.path.split(path)
    directory, filename = (directory or '.'), filename.lower()
    for f in os.listdir(directory):
        newpath = os.path.join(directory, f)
        if os.path.isfile(newpath) and f.lower() == filename:
            return newpath

def isfile_insensitive(path):
    return getfile_insensitive(path) is not None

sample_document='4_models_and_open_questions'


# In[ ]:


scores=[]
def formatting(_topdf):
    _topdf.rename(columns={'journal':'Journal'},inplace=True)
    _topdf.rename(columns={'url':'Study Link'},inplace=True)
    _topdf.rename(columns={'publish_time':'Date'},inplace=True)
    _topdf.rename(columns={'title':'Study'},inplace=True)
    
    return _topdf
for tsk in range(len(task)):
    
    for prob, query_embedding in zip(query[tsk], query_embeddings[tsk]):
        dis = sc.spatial.distance.cdist([query_embedding], abstract_summary_embeddings, "cosine")[0]
        #print(dis)
        results = zip(range(len(dis)), dis)
        results = sorted(results, key=lambda x: x[1])
        #print("Query:", prob)
        #print("Answer:" )
        scores.append(1-results[0][1])
        #print(df['abstract'][results[0][0]].strip(), "\n(Score: %.4f)" % (1-results[0][1]),"\n")
        k=50
        #print(results[:k])
        topk=results[:k]
        id,id_v=zip(*topk)
        topData=df.iloc[1]
        _topdf = df.iloc[list(id), :]
        _topdf = formatting(_topdf)
        csv_str=prob.replace('?','_')+'.csv'
        #print(csv_str)
        path1 = f'{root_path}Kaggle/target_tables/{sample_document}/'+csv_str
        path1 = f'{path1}'
        print(path1)
        if (isfile_insensitive(path1)):
            path1=getfile_insensitive(path1)
            q_df = pd.read_csv(path1)
            print("exist!")
        else:      
            path1 = f'{root_path}Kaggle/target_tables/{sample_document}/'
            path1 = os.path.join(path1,os.listdir(path1)[-1])
            q_df = pd.read_csv(path1)
            q_df.drop(q_df.index,inplace=True)
        #print(path1)
        q_df.head()
        q_df
        #print(len(q_df))
        #print(len(_topdf))
        #print(q_df.columns)
        res_df = pd.merge(q_df, _topdf, how='outer', on=['Study','Study Link','Date','Journal'])[q_df.columns[1:]]
        #print(len(res_df))
        res_df.info()
        res_csv=r'/kaggle/output/'+ csv_str
        print(res_csv)
        res_df.to_csv( csv_str, index = True)


# @inproceedings{Population studies that related to COVID-19, author = {Hang, Wu}, title = {Population studies that related to COVID-19}, year = {2020}, month = {June}, url = {\url{https://www.kaggle.com/nike0good/population-studies-that-related-to-covid-19} } }
