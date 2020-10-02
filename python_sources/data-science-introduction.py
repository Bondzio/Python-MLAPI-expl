#!/usr/bin/env python
# coding: utf-8

# **Part-1: Introduction to Python**

# ![](https://i.etsystatic.com/9993958/r/il/d2bc14/1526829006/il_794xN.1526829006_lg0b.jpg)

# In this noteboook I'll analyse Iris Species Dataset

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Read the Iris data from Csv
iris=pd.read_csv("/kaggle/input/iris/Iris.csv")


# In[ ]:


# Display content of Iris data 
iris.info()


# In[ ]:


#Data overview
iris.describe()


# In[ ]:


#Data correlation
iris.corr()


# High correlation between the PetalWidthCm and PetalLengthCm.
# Negative correlation between the SepalWidthCm and SepalLenght and Petalx

# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


#correlation map
f,ax = plt.subplots(figsize=(8, 8))
sns.heatmap(iris.corr(), annot=True, lw=.5, fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


iris.head(10), iris.tail(10)


# In[ ]:


iris


# In[ ]:


iris.columns


# In[ ]:


iris["Species"].unique()


# In[ ]:


# Scatter Plot 
# x = PetalWidthCm, y = PetalLengthCm
iris.plot(kind='scatter', x='PetalWidthCm', y='PetalLengthCm',alpha = 0.5)
plt.xlabel('PetalWidthCm')              # label = name of label
plt.ylabel('PetalLengthCm')
plt.title('Petal Width vs Lenght Graph')            # title = title of plot


# In[ ]:


iris.PetalLengthCm.plot(figsize=(15,15), kind="line",color="g", label="PetalL", lw=2, alpha=0.5, grid=True)
iris.PetalWidthCm.plot(color="r", label="PetalW", lw=2, alpha=0.5, grid=True, ls="-.")
iris.SepalLengthCm.plot(color="y", label="SepalL", lw=2, alpha=0.5, grid=True,ls="--")
iris.SepalWidthCm.plot(color="b", label="SepalW", lw=2, alpha=0.5, grid=True)
plt.legend(loc="upper right")
plt.xlabel("x axis")
plt.ylabel("y axis")
plt.title("Line Plot")
plt.show()


# In[ ]:


#Histogram diagram of Iris-virginica
#bins=number of bars in fig.
iris1=iris.drop("Id", axis=1)
iris1[101:].plot(kind="hist", bins=50, figsize=(8,8))


# In[ ]:


#Histogram diagram of Iris-setosa
#bins=number of bars in fig.
iris1[:50].plot(kind="hist", bins=50, figsize=(8,8))


# In[ ]:


#Histogram diagram of Iris-versicolor
#bins=number of bars in fig.
iris1[51:100].plot(kind="hist", bins=50, figsize=(8,8))


# In[ ]:


seri=iris["SepalLengthCm"]
df=iris[["SepalLengthCm"]]


# In[ ]:


print(type(seri))
print(type(df))


# In[ ]:


iris[iris.SepalLengthCm>7.4]


# In[ ]:


iris[(iris.SepalLengthCm>7.4) & (iris.PetalLengthCm<6.7)]


# In[ ]:


iris[np.logical_and(iris["SepalLengthCm"]>7.4, iris["PetalLengthCm"]<6.7)]


# In[ ]:


#Add new features to the DataFrame
iris["TotalLenght"]=iris["SepalLengthCm"]+iris["PetalLengthCm"]
iris["TotalWidth"]=iris["SepalWidthCm"]+iris["PetalWidthCm"]
iris


# In[ ]:


iris.TotalLenght.plot(kind="hist", bins=50, figsize=(8,8))


# In[ ]:


iris.TotalWidth.plot(kind="hist", bins=50, figsize=(8,8))


# In[ ]:


#Adding new column to Dataframe with using if and for loop
iris["Compare"]=[1 if i>14 or j>=6 else 0 for i,j in zip(iris.TotalLenght,iris.TotalWidth)]
iris


# In[ ]:


iris[iris.Compare==1]


# In[ ]:




