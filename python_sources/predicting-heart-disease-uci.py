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


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.cm import rainbow
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


train=pd.read_csv(r"/kaggle/input/heart-disease-uci/heart.csv")


# In[ ]:


train


# In[ ]:


train.describe(include='all')


# In[ ]:


train.count()#this normally used to find the null values


# # Feature selection

# In[ ]:


import seaborn as sns
#get correlations of each features in dataset
corrmat = train.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(train[top_corr_features].corr(),annot=True,cmap="RdYlGn")


# # Data preprocessing

# In[ ]:


df=pd.get_dummies(train,columns=['sex','cp','restecg','slope','ca','thal','exang','fbs'],drop_first=True)


# In[ ]:


df


# # Feature Scalling

# In[ ]:


from sklearn.preprocessing import StandardScaler
standardScaler = StandardScaler()
columns_to_scale = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
df[columns_to_scale] = standardScaler.fit_transform(df[columns_to_scale])


# In[ ]:


df


# In[ ]:


y=df['target']
X=df.drop(['target'],axis=1)


# # Knn

# In[ ]:


# find the best n_neighbors
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
knn_scores = []
for k in range(1,21):
    knn_classifier = KNeighborsClassifier(n_neighbors = k)
    score=cross_val_score(knn_classifier,X,y,cv=10)
    knn_scores.append(score.mean())


# In[ ]:


#plot the K Neighbors Classifier scores for different K values
plt.plot([k for k in range(1, 21)], knn_scores, color = 'red')
for i in range(1,21):
    plt.text(i, knn_scores[i-1], (i,int( knn_scores[i-1]*100)))
plt.xticks([i for i in range(1, 21)])
plt.xlabel('Number of Neighbors (K)')
plt.ylabel('Scores')
plt.title('K Neighbors Classifier scores for different K values')


# In[ ]:


knn_classifier = KNeighborsClassifier(n_neighbors = 7)
score=cross_val_score(knn_classifier,X,y,cv=10)


# In[ ]:


# check for accuracy
score.mean()*100  


# # Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier

randomforest_classifier= RandomForestClassifier(n_estimators=12)

score=cross_val_score(randomforest_classifier,X,y,cv=10)


# In[ ]:


score.mean()*100


# # Decision Tree

# In[ ]:


from sklearn.tree import DecisionTreeClassifier


# In[ ]:


decisiontree_classifier= DecisionTreeClassifier( 
            criterion = "gini", random_state = 100, 
            max_depth = 3, min_samples_leaf = 5)


# In[ ]:


score=cross_val_score(decisiontree_classifier,X,y,cv=10)


# In[ ]:


score.mean()*100


# In[ ]:





# In[ ]:




