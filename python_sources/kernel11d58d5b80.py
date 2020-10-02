#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import math


# In[ ]:


datingdata=pd.read_csv('../input/Speed Dating Data.csv',encoding="ISO-8859-1")
print(datingdata.head())
print(datingdata['prob'].head())


# In[ ]:


fielddata=datingdata.groupby('field').agg({'prob':np.mean}).sort_values(by='prob',ascending=False)
fielddata[:20].plot(kind='barh')
fielddata=fielddata.sort_values(by='prob',ascending=True)
fielddata[:20].plot(kind='barh')


# In[ ]:


datingdata.groupby("age_o").agg({'prob':np.mean}).plot(kind='barh')


# In[ ]:


genderage=datingdata.groupby(['gender','age_o']).agg({'prob':np.mean}).unstack()
sns.heatmap(genderage)


# In[ ]:


datingdata.groupby(['from']).agg({'prob':np.mean}).plot(kind='barh')


# In[ ]:


datingdata.groupby('race_o').agg({'prob':np.mean}).plot(kind='barh')


# In[ ]:


incomelist=[]
for i in range(len(datingdata)):
    if(type(datingdata['income'][i])==np.float):
        incomelist.append(np.NaN)
    else:
        incomelist.append(float(datingdata['income'][i].replace(',','')))
incomeprob=pd.DataFrame({
    'income':pd.Series(incomelist),
    'prob':datingdata['prob'],
    'gender':datingdata['gender']
}).dropna()
plt.scatter(incomeprob[incomeprob['gender']==0]['income'],incomeprob[incomeprob['gender']==0]['prob'],c='b')
plt.scatter(incomeprob[incomeprob['gender']==1]['income'],incomeprob[incomeprob['gender']==1]['prob'],c='r')

