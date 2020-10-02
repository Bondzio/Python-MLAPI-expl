#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math


# In[5]:


data_df = pd.read_csv('../input/train.csv')


# In[6]:


def make_data(data_df):
    visits = list(data_df['visits'])
    for idx, v in enumerate(visits):
        visits[idx] = [int(s) for s in v.split()]
    return visits


# In[7]:


visits = make_data(data_df)


# In[8]:


def client_days(data):
    return [int((d-1)%7) for d in data][::-1]
def client_weeks(data):
    return [158 - int((d+6)//7) for d in data][::-1]


# In[9]:


def init_weights(d):
    w_n = [math.pow((float((d-i)/d+1)),1.5) for i in range(d)]
    w = [float(w_n[i]/sum(w_n)) for i in range(d)]
    return w


# In[10]:


d = 157 # 1099/7
w = init_weights(d)


# In[11]:


def predict_for_client(data, w):
    weeks = client_weeks(data)
    days = client_days(data)
    p_j = [0.0] * 7
    for i, w_i in enumerate(weeks):
        p_j[days[i]] += w[w_i-1]
    p = [1.0] * 7
    for i in range(7):
        p[i] = p_j[i]
    for i in range(1, 7):
        for j in range(i):
            p[i] *= (1 - p_j[j])
    return p           


# In[12]:


proba = [predict_for_client(client, w) for client in visits]
y = np.argmax(np.asarray(proba), axis=1)


# In[14]:


with open('solution.csv', 'w') as f:
    f.write('id,nextvisit\n')
    for idx, label in enumerate(y):
        f.write(str(idx+1)+', '+str(label+1)+'\n')


# In[ ]:




