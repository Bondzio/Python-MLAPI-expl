#!/usr/bin/env python
# coding: utf-8

# I wasn't fan of the previous visualizations as I like to see the nice smooth functions as I suspect there will be a lot of probability "guessing" in this contest.  So I like to see the distributions as smooth functions.  
# 
# Sometimes my code is clunky, but it got the job done fairly quick.  Please enjoy. If you are in a hurry drop the iterations from a million to 100,000.  You won't loose much, but the mathematician in me likes smoothness.  My therapist calls it "OCD
# 
# edit: Hat Tip to Toby Cheese for more efficient code! Give him upvotes

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

horse=np.maximum(0, np.random.normal(5, 2, 1000000))
ball = np.maximum(0, 1 + np.random.normal(1,0.3,1000000))
bike = np.maximum(0, np.random.normal(20,10,1000000))
train = np.maximum(0, np.random.normal(10,5,1000000))
coal = 47 * np.random.beta(0.5,0.5,1000000)
book = np.random.chisquare(2,1000000)
doll= np.random.gamma(5,1,1000000)
block = np.random.triangular(5,10,20,1000000)
gloves=np.random.rand(1000000)
for index in range(len(gloves)):
    if gloves[index]<0.3:
        gloves[index]=3+np.random.rand(1)[0]
    else:
        gloves[index]=np.random.rand(1)[0]
        






# Any results you write to the current directory are saved as output.


# In[ ]:


data=pd.DataFrame({'horse':horse,'ball':ball,'bike':bike,'train':train,'block':block,'doll':doll,'coal':coal,'book':book,'gloves':gloves})
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
colnames=list(data.columns.values)
for i in colnames:
        facet = sns.FacetGrid(data,aspect=2)
        facet.map(sns.distplot,i,bins=100,kde=False,norm_hist=True)
        facet.add_legend()


# In[ ]:


items=[ball, bike, block, book, coal, doll, gloves,horse, train]

for i in range(len(items)):
    sorted_data = np.sort(items[i])  


    plt.step(sorted_data, np.arange(sorted_data.size)/sorted_data.size) 
    plt.title(colnames[i])
    plt.show()

