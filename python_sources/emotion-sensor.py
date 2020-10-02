#!/usr/bin/env python
# coding: utf-8

# **EMOTION SENSOR**
# 
# 
# 
# 
# This is the small analysis of 7 basic emotions*(Disgust, Surprise ,Neutral ,Anger ,Sad ,Happy and Fear)*in the 1104 English words.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv("/kaggle/input/emotions-sensor-data-set/Andbrain_DataSet.csv")


# In[ ]:


data.info()


# In[ ]:


data.corr()


# In[ ]:


#correlation map 
f,ax = plt.subplots(figsize=(20,20))
sns.heatmap(data.corr(),annot = True, linewidths = 0.6, fmt = ".4f", ax=ax)
plt.show()


# In[ ]:


data.head(15)


# In[ ]:


data.columns


# In[ ]:


data.surprise.plot(kind="line",color="purple",label="surprise",linewidth=1,alpha=0.3,grid=True,linestyle="-")
data.anger.plot(color="red",label = "anger", linewidth = 1,alpha=0.5,linestyle=":")
plt.legend(loc="upper right")
plt.xlabel("words")
plt.ylabel("values")
plt.title("Emotions Sensor")
plt.show()


# In[ ]:


### Scatter Plot
data.plot(kind="scatter",x="sad",y="happy",alpha=.3,color="green")
plt.xlabel("Sad")
plt.ylabel("Happy")
plt.title("Sad-Happy Scatter Plot")


# In[ ]:


# Histogram
data.fear.plot(kind="hist",bins=100,figsize=(20,20))
plt.show()


# In[ ]:


x= data["disgust"]>0.08
data[x]


# In[ ]:


data[(data["sad"]>.07)&(data["happy"]>.07)]


# In[ ]:


threshold = sum(data["anger"])/len(data["anger"])
data["anger_level"] = ["high" if i>threshold else "low" for i in data["anger"]]
data.loc[:50,["anger_level","anger","word"]]

