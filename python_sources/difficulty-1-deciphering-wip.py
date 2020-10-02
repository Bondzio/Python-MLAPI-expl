#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 7.5]
import numpy as np
import pandas as pd
import string
from collections import Counter
from Crypto.Cipher import *
from cryptography import *
import hashlib, hmac, secrets, base64
from sympy import primerange
import os
train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')


# code borrowed from https://www.kaggle.com/jazivxt/enigma-layers-template , thanks!

# In[ ]:


level_one = train[train['difficulty']==1].copy()
level_one['ciphertext'] = level_one['ciphertext'].map(lambda x: str(x)[:300])
hist = Counter(' '.join(level_one['ciphertext'].astype(str).values))
cph = pd.DataFrame.from_dict(hist, orient='index').reset_index()
cph.columns = ['ciph', 'ciph_freq']
cph = cph.sort_values(by='ciph_freq', ascending=False).reset_index(drop=True)
cph.plot(kind='bar')


# In[ ]:


# num chars in level 1 cipher
cph['ciph_freq'].sum()


# In[ ]:


from sklearn.datasets import fetch_20newsgroups
news = fetch_20newsgroups(subset='train')


# In[ ]:


news.keys()


# In[ ]:


news['data'][0:5]


# In[ ]:


plain = news['data'][:1420]


# In[ ]:


plain_char_sample = Counter(' '.join(plain))
pt = pd.DataFrame.from_dict(plain_char_sample, orient='index').reset_index()
pt.columns = ['char', 'freq']
pt = pt.sort_values(by='freq', ascending=False).reset_index(drop=True)
pt.plot(kind='bar')


# In[ ]:


# num plain chars in news sample, very rough now
pt['freq'].sum()


# In[ ]:


fq_comp=cph
fq_comp['char']=pt['char']
fq_comp['freq']=pt['freq']
fq_comp.head(10)


# In[ ]:


fq_comp.plot(kind='bar')


# so far level one is consistent with a monoalphabetic substitution, probably combined with transposition. 
# looks like something weird is going on with the spaces... but we can check

# In[ ]:


more_plain = news['data'][:10000]


# In[ ]:


more = Counter(' '.join(more_plain))
mpt = pd.DataFrame.from_dict(more, orient='index').reset_index()
mpt.columns = ['char', 'freq']
mpt = mpt.sort_values(by='freq', ascending=False).reset_index(drop=True)


# In[ ]:


mpt['freq'].sum()


# In[ ]:


fq_comp2=cph
fq_comp2['char']=mpt['char']
fq_comp2['freq']=mpt['freq']
fq_comp2['ratio']=fq_comp2['freq']/fq_comp2['ciph_freq']
fq_comp2.head(10)


# In[ ]:


fq_comp2['ratio'].plot(kind='bar')


# this is mostly consistent with a simple substitution, something weird is going on with a few of the chars though, the highest and lowest ratios are way outside the rest, but level one and the sample plaintext are probably not totally comprable, still, clues.

# In[ ]:


fq_comp2[['ciph', 'char', 'ratio']].sort_values(by='ratio', ascending=False)


# In[ ]:


#chars by frequency from this limited sample
fmap=pd.Series(fq_comp2.char.values, fq_comp2.ciph.values).to_dict()
fmap


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# 
