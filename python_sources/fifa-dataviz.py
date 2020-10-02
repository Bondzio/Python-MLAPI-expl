#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df=pd.read_csv('../input/data.csv')


# In[ ]:


sns.distplot(df.Age)


# In[ ]:


df.head()
#list_age=[]
#for k in df.Age:
#pd.cut(df.value, range(0, 105, 10), right=False, labels=labels)
df['Age_Cat']=pd.cut(df.Age,[15,18,21,25,30,35,40,50],labels=['15-18','18-21','21-25','25-30','30-35','35-40','40-50'])   
#df=df.join(pd.get_dummies(test_age,prefix='age'))


# In[ ]:


df.head(40)


# In[ ]:


sns.distplot(df.Overall);


# In[ ]:


g=sns.catplot(x='Age_Cat',y='Overall',data=df,kind='violin',hue='Preferred Foot',split=True);
g.fig.suptitle('Overall by age categories');
g.fig.set_size_inches(10,10);


# In[ ]:


#plt.figure(figsize=(10,10))
g=sns.catplot(x='Preferred Foot',y='Overall',data=df[df['Overall']>80],kind='box')
g.fig.set_size_inches(10,10)


# In[ ]:


g=sns.catplot(x='Position',y='Overall',data=df,kind='boxen')
g.fig.set_size_inches(10,6)


# In[ ]:


df_best=df.sort_values(by='Overall',axis=0,ascending=False).head(20)


# In[ ]:


df_best.head()


# In[ ]:


plt.figure(figsize=(10,10))
h=sns.countplot(x='Nationality',data=df_best)
h.set_title('Best players country');


# In[ ]:


df.groupby(by='Nationality')['Overall'].mean().sort_values(ascending=False).head(30)


# In[ ]:


df[df['Nationality']=='France'].Overall.mean()

