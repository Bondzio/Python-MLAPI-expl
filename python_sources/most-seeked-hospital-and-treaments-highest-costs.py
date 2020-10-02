#!/usr/bin/env python
# coding: utf-8

# ## Hospital Charges
# <br/>
# #### Data posted at kaggle - short analysis

# **Importing libraries & Data**

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


DF = pd.read_csv('../input/inpatientCharges.csv')


# Checking DF shape and features

# In[ ]:


print (DF.shape)


# In[ ]:


DF.ftypes


# applying few qol changes: <br/>
# - making easier to work with feature names <br/>
# - fixing data types

# In[ ]:


DF.columns=['drg', 'id', 'name','address', 'city', 'state','zip', 'region',
            'discharges', 'avg_covered_charges','avg_total_payments', 'avg_medicare_payments']


# In[ ]:


DF['id']=DF['id'].apply(str)
DF['zip']=DF['zip'].apply(str)
DF['avg_covered_charges']=(DF['avg_covered_charges'].map(lambda x: x.strip('$'))).apply(float)
DF['avg_medicare_payments']=(DF['avg_medicare_payments'].map(lambda x: x.strip('$'))).apply(float)
DF['avg_total_payments']=(DF['avg_total_payments'].map(lambda x: x.strip('$'))).apply(float)


# In[ ]:


DF.ftypes


# In[ ]:



for i in DF[['id','name','address']]:
    print (i,len(set(DF[i])))


# Okay. <br/> We have different size arrays for 'id', 'name', 'address'. <br/>
# That might be pointing to some data issue.

# In[ ]:


A=DF[['id','address']].groupby('id')['address'].nunique()
B=DF[['id','address']].groupby('address')['id'].nunique()

A2=DF[['id','name']].groupby('id')['name'].nunique()
B2=DF[['id','name']].groupby('name')['id'].nunique()


# In[ ]:


A[A>1].head()


# In[ ]:


B[B>1].head()


# In[ ]:


A2[A2>1].head()


# In[ ]:


B2[B2>1].head()


# Okay.
# So a few addresses have more than 1 hospital at it.
# And a few different hospitals have the same name.
# 
# Something to keep in mind. When analyzing the data always refer to id instead of name or other feature.

# ### First plots

# defining parameters

# In[ ]:


fs=20;
size=50;
text_opts={'fontsize':fs,'fontweight':'bold'};


# discharge counts

# In[ ]:


dummy_DF=DF[['id','discharges','name']];

h=dummy_DF.groupby('id')['discharges'].sum().sort_values(ascending=False)[:size]
x=dummy_DF[:size].index
labels=dummy_DF[:size].name

plt.figure(figsize=(20,10));

plt.bar(height=h, left=x, align='center');

plt.xticks(x,labels,rotation='vertical', fontsize=fs/2);

plt.xlim([-1,size])
plt.yticks(**text_opts);
plt.grid(which='both');

plt.title('discharge count per hospital\n top %s counts' %size, **text_opts);


# top conditions counts

# In[ ]:


dummy_DF=DF[['drg','name','discharges']];

h=dummy_DF.groupby('drg')['discharges'].sum().sort_values(ascending=False)[:size]
x=dummy_DF[:size].index
labels=h[:size].index

plt.figure(figsize=(20,10));

plt.bar(height=h, left=x, align='center');

plt.xticks(x,labels,rotation='vertical', fontsize=fs/2);

plt.xlim([-1,size])
plt.yticks(**text_opts);
plt.grid(which='both');

plt.title('condition count\n top %s counts' %size, **text_opts);


# In[ ]:


dummy_DF=DF[['drg','name','avg_covered_charges']];

h=dummy_DF.groupby('drg')['avg_covered_charges'].median().sort_values(ascending=False)[:size]
x=dummy_DF[:size].index
labels=h[:size].index

plt.figure(figsize=(20,10));

plt.bar(height=h, left=x, align='center');

plt.xticks(x,labels,rotation='vertical', fontsize=fs/2);

plt.xlim([-1,size])
plt.yticks(**text_opts);
plt.grid(which='both');

plt.title('median avg_covered_charges cost\n top %s most expensive' %size, **text_opts);


# In[ ]:


dummy_DF=DF[['drg','name','avg_total_payments']];

h=dummy_DF.groupby('drg')['avg_total_payments'].median().sort_values(ascending=False)[:size]
x=dummy_DF[:size].index
labels=h[:size].index

plt.figure(figsize=(20,10));

plt.bar(height=h, left=x, align='center');

plt.xticks(x,labels,rotation='vertical', fontsize=fs/2);

plt.xlim([-1,size])
plt.yticks(**text_opts);
plt.grid(which='both');

plt.title('median avg_total_payments cost\n top %s most expensive' %size, **text_opts);


# In[ ]:



dummy_DF=DF[['drg','name','avg_medicare_payments']];

h=dummy_DF.groupby('drg')['avg_medicare_payments'].median().sort_values(ascending=False)[:size]
x=dummy_DF[:size].index
labels=h[:size].index

plt.figure(figsize=(20,10));

plt.bar(height=h, left=x, align='center');

plt.xticks(x,labels,rotation='vertical', fontsize=fs/2);

plt.xlim([-1,size])
plt.yticks(**text_opts);
plt.grid(which='both');

plt.title('median avg_medicare_payments cost\n top %s most expensive' %size, **text_opts);


# In[ ]:




