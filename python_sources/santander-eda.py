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

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


random_state = 42
np.random.seed(random_state)
df_train = pd.read_csv('../input/train.csv')
df_test = pd.read_csv('../input/test.csv')


# In[ ]:


features = ["var_{}".format(i) for i in range(200)]


# In[ ]:


plt.figure(figsize=[16,9])
sns.heatmap(df_train[features].corr())


# In[ ]:


plt.figure(figsize=[16,9])
sns.heatmap(df_test[features].corr())


# In[ ]:


plt.figure(figsize=[16,9])
df_train.boxplot()


# In[ ]:


plt.figure(figsize=[16,9])
df_test.boxplot()


# In[ ]:


df_train.drop_duplicates().shape


# In[ ]:


names = []
for i in range(30, 50):
    names.append("var_{}".format(i))


# In[ ]:


plt.figure(figsize=[16,9])
sns.heatmap(df_train[names].corr())


# In[ ]:


plt.figure(figsize=[16,9])
df_train[names].boxplot()


# In[ ]:


sns.boxplot(df_train["var_45"])


# In[ ]:


sns.boxplot(df_test["var_45"])


# In[ ]:


def plot_feature_scatter(df1, df2, features):
    i = 0
    sns.set_style('whitegrid')
    plt.figure()
    fig, ax = plt.subplots(4,4,figsize=(14,14))

    for feature in features:
        i += 1
        plt.subplot(4,4,i)
        plt.scatter(df1[feature], df2[feature], marker='+')
        plt.xlabel(feature, fontsize=9)
    plt.show();


# In[ ]:


features = ["var_{}".format(i) for i in range(200)]


# In[ ]:


c = 0
for j in range(16, 200, 16):
    plot_feature_scatter(df_train,df_test, features[c:j])
    c += 16


# In[ ]:


print(df_train.target.value_counts())
frac = (df_train.target.value_counts()[1]/df_train.target.value_counts()[0])*100
print("The fraction of 'True' is " + str(frac) + " %")


# In[ ]:


sns.boxplot(df_train["var_68"])


# In[ ]:


sns.boxplot(df_test["var_68"])


# In[ ]:


def plot_feature_boxplot(df, features):
    i = 0
    sns.set_style('whitegrid')
    plt.figure()
    fig, ax = plt.subplots(4,4,figsize=(14,14))

    for feature in features:
        i += 1
        plt.subplot(4,4,i)
        sns.boxplot(df[feature])
        plt.xlabel(feature, fontsize=9)
    plt.show();


# In[ ]:


c = 0
for j in range(16, 200, 16):
    plot_feature_boxplot(df_train, features[c:j])
    c += 16


# In[ ]:


c = 0
for j in range(16, 200, 16):
    plot_feature_boxplot(df_test, features[c:j])
    c += 16


# In[ ]:


even_vars = ["var_{}".format(i) for i in range(0,200,2)]
odd_vars = ["var_{}".format(i) for i in range(1,200,2)]


# In[ ]:


plt.figure(figsize=[16,9])
sns.heatmap(df_train[even_vars].corr())


# In[ ]:


plt.figure(figsize=[16,9])
sns.heatmap(df_train[odd_vars].corr())


# In[ ]:


for j in range(0,191,10):
    sns.heatmap(df_train[["var_{}".format(i) for i in range(j,j+10)]])
    plt.show()


# In[ ]:


df_train.var_125.nunique(), df_train.var_71.nunique(), df_train.var_103.nunique(), df_train.var_91.nunique(), df_train.var_68.nunique()


# In[ ]:


def plot_feature_distplot(df, features):
    i = 0
    sns.set_style('whitegrid')
    plt.figure()
    fig, ax = plt.subplots(4,4,figsize=(14,14))

    for feature in features:
        i += 1
        plt.subplot(4,4,i)
        sns.distplot(df[feature])
        plt.xlabel(feature, fontsize=9)
    plt.show();


# **Train Distribution**

# In[ ]:


c = 0
for j in range(16, 200, 16):
    plot_feature_distplot(df_train, features[c:j])
    c += 16

plot_feature_distplot(df_train, features[c:])


# **Test Distribution**

# In[ ]:


c = 0
for j in range(16, 200, 16):
    plot_feature_distplot(df_test, features[c:j])
    c += 16

plot_feature_distplot(df_test, features[c:])


# In[ ]:


s = df_train[features].shape


# In[ ]:


i = 0
plt.figure(figsize=[16,16])

for feature in features:
    plt.subplot(4,4,i+1)
    plt.plot(list(range(s[0])), df_train[feature].values)
    plt.xlabel(feature)
    i += 1
    if i == 16:
        i = 0
        plt.show();
        plt.figure(figsize=[16,16])


# In[ ]:


plt.figure(figsize=[16,16])
for i in range(16):
    plt.subplot(4,4,i+1)
    plt.plot(list(range(s[1])), df_train[features].iloc[i].values, "orange")
    plt.plot(list(range(s[1])), df_test[features].iloc[i].values, "blue")
    plt.xlabel("line {}".format(i))
plt.show();


# **Well, let's try to sort lines**

# In[ ]:


plt.figure(figsize=[16,16])
for i in range(16):
    plt.subplot(4,4,i+1)
    plt.plot(list(range(s[1])), sorted(df_train[features].iloc[i].values), "orange")
    plt.plot(list(range(s[1])), sorted(df_test[features].iloc[i].values), "blue")
    plt.legend(["train", "test"])
    plt.xlabel("line {}".format(i))
plt.show();


# **Looks interesting. Each sorted line is similar to another.**

# In[ ]:




