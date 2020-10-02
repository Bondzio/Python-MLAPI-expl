#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[2]:


df = pd.read_csv('../input/StudentsPerformance.csv')
df.head()


# In[3]:


df.info()


# In[4]:


df.isnull().sum()


# In[5]:


import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
sns.countplot(df['gender'])


# In[6]:


fig=plt.figure(figsize=(20,6))
ax1=plt.subplot(131)
ax2=plt.subplot(132)
ax3=plt.subplot(133)
sns.barplot(x='race/ethnicity',y='math score',hue='gender',data=df,ax=ax1)
sns.barplot(x='race/ethnicity',y='reading score',hue='gender',data=df,ax=ax2)
sns.barplot(x='race/ethnicity',y='writing score',hue='gender',data=df,ax=ax3)


# In[7]:


fig=plt.figure(figsize=(20,6))
ax1=plt.subplot(131)
ax2=plt.subplot(132)
ax3=plt.subplot(133)
sns.barplot(x='parental level of education',y='math score',hue='gender',data=df,ax=ax1)
sns.barplot(x='parental level of education',y='reading score',hue='gender',data=df,ax=ax2)
sns.barplot(x='parental level of education',y='writing score',hue='gender',data=df,ax=ax3)
for ax in fig.axes:
    plt.sca(ax)
    plt.xticks(rotation=90)


# In[8]:


fig=plt.figure(figsize=(20,6))
ax1=plt.subplot(131)
ax2=plt.subplot(132)
ax3=plt.subplot(133)
sns.barplot(x='gender',y='math score',data=df,ax=ax1)
sns.barplot(x='gender',y='reading score',data=df,ax=ax2)
sns.barplot(x='gender',y='writing score',data=df,ax=ax3)


# In[9]:


df.rename(columns={'math score':'math_score','writing score':'writing_score','reading score':'reading_score'},inplace=True)


# In[10]:


sns.jointplot(x=np.arange(1,483),y=df[df['gender']=='male'].math_score,color='lime',alpha=0.8)
sns.jointplot(x=np.arange(1,519),y=df[df['gender']=='female'].math_score,color='red',alpha=0.8)


# In[11]:


df['race/ethnicity'].unique()


# In[12]:


sns.jointplot(x=np.arange(1,191),y=df[(df['race/ethnicity']=='group B')].reading_score,color='k',kind='kde')


# In[13]:


sns.jointplot(x=np.arange(1,191),y=df[(df['race/ethnicity']=='group B')].reading_score,color='k').plot_joint(sns.kdeplot, n_levels=10)


# In[14]:


values=df.groupby('parental level of education').math_score.mean().values
values1=df.groupby('parental level of education').reading_score.mean().values
labels=df.groupby('parental level of education').math_score.mean().reset_index().iloc[0:6,0]
labels1=df.groupby('parental level of education').reading_score.mean().reset_index().iloc[0:6,0]
explode=[0,0,0,0,0,0.1]
values1


# In[15]:


plt.pie(values,labels=labels,explode=explode,autopct='%1.1f%%')


# In[16]:


plt.pie(values1,labels=labels1,explode=explode,autopct='%1.1f%%')


# In[17]:


sns.lmplot(x='reading_score',y='math_score',data=df,palette='A52E29')


# In[22]:


ax=plt.figure(figsize=(10,5))
ax1=plt.subplot(121)
ax2=plt.subplot(122)
sns.kdeplot(df['math_score'],ax=ax1)
sns.kdeplot(df['reading_score'],ax=ax2)


# In[25]:


sns.kdeplot(df['math_score'],shade=True,color='r')
sns.kdeplot(df['reading_score'],shade=True,color='b')


# In[26]:


sns.kdeplot(df['reading_score'],df['writing_score'])


# In[28]:


sns.kdeplot(df['reading_score'],df['writing_score'])


# In[29]:


sns.kdeplot(df['reading_score'],df['math_score'])


# In[36]:


sns.kdeplot(df['math_score'],bw=0.20)


# In[39]:


sns.heatmap(df.corr(),vmin=0,vmax=1,annot=True)


# In[54]:


corr=df.corr()
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.2, center=0,square=True, linewidths=.5,annot=True, cbar_kws={"shrink": .5})


# In[ ]:





# In[ ]:





# In[ ]:




