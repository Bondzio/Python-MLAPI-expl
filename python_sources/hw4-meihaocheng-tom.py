#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# default libraries
import numpy as np
import pandas as pd

# for data preprocessing
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# for classifier models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold, cross_val_score
import xgboost as xgb

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
# matplotlib inline

# for models evaluation
from sklearn.metrics import confusion_matrix, accuracy_score


# # Ingest

# In[ ]:


data = pd.read_csv('/kaggle/input/eating-health-module-dataset/ehresp_2014.csv')
data.head()


# In[ ]:


data.shape


# # Cleaning and exploration
# 

# ### Clean

# In[ ]:


def init_check(df):
    """
    A function to make initial check for the dataset including the name, data type, 
    number of null values and number of unique varialbes for each feature.
    
    Parameter: dataset(DataFrame)
    Output : DataFrame
    """
    columns = df.columns    
    lst = []
    for feature in columns : 
        dtype = df[feature].dtypes
        num_null = df[feature].isnull().sum()
        num_unique = df[feature].nunique()
        lst.append([feature, dtype, num_null, num_unique])
    
    check_df = pd.DataFrame(lst)
    check_df.columns = ['feature','dtype','num_null','num_unique']
    check_df = check_df.sort_values(by='dtype', axis=0, ascending=True)
    
    return check_df


# In[ ]:


init_check(df=data)


# In[ ]:


def categorical_encoding(df, categorical_cloumns, encoding_method):
    """
    A function to encode categorical features to a one-hot numeric array (one-hot encoding) or 
    an array with value between 0 and n_classes-1 (label encoding).
    
    Parameters:
        df (pd.DataFrame) : dataset
        categorical_cloumns  (string) : list of features 
        encoding_method (string) : 'one-hot' or 'label'
    Output : pd.DataFrame
    """
    
    if encoding_method == 'label':
        print('You choose label encoding for your categorical features')
        encoder = LabelEncoder()
        encoded = df[categorical_cloumns].apply(encoder.fit_transform)
        return encoded
    
    elif encoding_method == 'one-hot':
        print('You choose one-hot encoding for your categorical features') 
        encoded = pd.DataFrame()
        for feature in categorical_cloumns:
            dummies = pd.get_dummies(df[feature], prefix=feature)
            encoded = pd.concat([encoded, dummies], axis=1)
        return encoded


# In[ ]:


categorical_columns = data.select_dtypes(include=['float64']).columns


# In[ ]:


encoded=categorical_encoding(df=data,categorical_cloumns=categorical_columns, encoding_method='label')


# In[ ]:


data = data.drop(columns=categorical_columns, axis=1)
data = pd.concat([data, encoded], axis=1)
data.head()


# ### Visualizing

# In[ ]:


data.hist(bins = 10, figsize=(18, 16), color="#2c5af2")


# In[ ]:


for a in ['eufinlwgt','erbmi','ertpreat','ertseat','euwgt']:
    ax=plt.subplots(figsize=(6,3))
    ax=sns.distplot(data[a])
    title="Histogram of " + a
    ax.set_title(title, fontsize=12)
    plt.show()


# ### Feature engineering

# In[ ]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
data_scaled=pd.DataFrame(scaler.fit_transform(data))
data_scaled.columns=data.columns
data_scaled.index=data.index


# In[ ]:


data_scaled.describe()


# # Modelling

# ### PCA

# In[ ]:


from sklearn.decomposition import PCA
n_components=37
pca = PCA(n_components=n_components)
pca.fit(data_scaled)


# In[ ]:


plt.subplots(figsize=(10,8))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance');


# In[ ]:


explained_variance_ratio = pca.explained_variance_ratio_ 
cum_explained_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
lst = []
for i in range (0, n_components):
  lst.append([i+1, round(explained_variance_ratio[i],6), cum_explained_variance_ratio[i]])

pca_predictor = pd.DataFrame(lst)
pca_predictor.columns = ['Component', 'Explained Variance', 'Cumulative Explained Variance']
pca_predictor


# In[ ]:


pca = PCA(n_components=8)
pca.fit(data_scaled)
explained_variance_ratio = pca.explained_variance_ratio_
singular_values = pca.singular_values_    


# In[ ]:


data_transformed = pca.fit_transform(data_scaled)
data_transformed.shape


# In[ ]:


data_transformed


# ###  K-Means

# In[ ]:


plt.subplots(figsize=(10,8))
plt.scatter(data_transformed[:,[0]], data_transformed[:,[1]])


# In[ ]:


from sklearn.cluster import KMeans

n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters, random_state=123)
kmeans.fit(data_transformed)


# In[ ]:


cluster_labels = kmeans.labels_
cluster_labels


# In[ ]:


ax=plt.subplots(figsize=(10,5))
ax=sns.countplot(cluster_labels)
title="Histogram of Cluster Counts"
ax.set_title(title, fontsize=12)
plt.show()


# In[ ]:


data['X'] = data_transformed[:,[0]]
data['Y'] = data_transformed[:,[1]]
data['cluster'] = cluster_labels
ax=plt.subplots(figsize=(10,10))
ax = sns.scatterplot(x='X', y='Y',hue='cluster', legend="full", palette="Set1", data=data)


# ## Although I have retained 8 dimensions, after categorization, only two dimensions of the scatter plot can still see the points of different classes come together, so I kept the code for my wrong visualization process.

# # GMM

# In[ ]:


from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=8).fit(data_transformed)
labels = gmm.predict(data_transformed)
plt.scatter(data_transformed[:, 0],data_transformed[:, 1], c=labels, s=40, cmap='viridis');


# ### Comparison of clusters' stats

# In[ ]:


def cluster_stats(columns):
    output = pd.DataFrame({'cluster':[ i for i in range(n_clusters)]})
    for column in columns:
        lst = []
        for i in range(n_clusters):
            mean = data[data['cluster'] == i].describe()[column]['mean']
            lst.append([i, round(mean,2)])
        df = pd.DataFrame(lst)
        df.columns = ['cluster', column]
        output = pd.merge(output, df, on='cluster', how='outer')
    return output


# In[ ]:


columns =data_scaled.columns
cluster_stats(columns)


# # Conclusion

# 1. Using  PCA and K-Means methods can effectively classify data.
# 2. By comparison of clusters' stats, I am able to find out the differences between the categories.
# 3. Although it is only when the dimension is reduced to 2 or 3 dimensions, the visualization can be well achieved. However, I found that when I can't drop to such a low dimension, I can only see the distribution of the data in these two dimensions.
