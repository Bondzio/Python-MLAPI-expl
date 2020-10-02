#!/usr/bin/env python
# coding: utf-8

# # INTRODUCTION
# * **In this kernel,we will see Principal Component Analysis (PCA).**

# In[ ]:


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


# In[ ]:


from sklearn.datasets import load_iris


# In[ ]:


iris = load_iris()
data = iris.data
feature_names = iris.feature_names
y = iris.target


# In[ ]:


df = pd.DataFrame(data, columns=feature_names)
df["sinif"] = y
x = data


# # Applying PCA

# In[ ]:


from sklearn.decomposition import PCA

#We reduce the number of feature from 4 to 2 with 3% data loss.
pca = PCA(n_components = 2,whiten = True)#whiten =>to normalize feature
pca.fit(x)#fit the model
x_pca = pca.transform(x)#and apply the model


# In[ ]:


print("variance ratio: ",pca.explained_variance_ratio_)


# In[ ]:


print("sum: ",sum(pca.explained_variance_ratio_))


# * **As you can see, I have 97 percent of my data.**

# In[ ]:


df["p1"] = x_pca[:,0] #principle component(P1)
df["p2"] = x_pca[:,1] #second component(P2)


# * **Now, we can visualize our data easily.**

# In[ ]:


color = ["red","green","blue"]

import matplotlib.pyplot as plt
for each in range(3):
    plt.scatter(df.p1[df.sinif == each],df.p2[df.sinif == each],color = color[each],label = iris.target_names[each])
plt.legend()
plt.xlabel("p1")
plt.ylabel("p2")
plt.show()


# # Conclusion
# * **If you like it, Please upvote my kernel.**
# * **If you have any question, I will happy to hear it.**
