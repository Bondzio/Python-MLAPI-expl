#!/usr/bin/env python
# coding: utf-8

# Lower Back Pain is universal human issue. Almost everyone has it some point of time.  Pain that last for 3 months or more is considered chronic.
# 
# Typical sources of low back pain include:
# 
# * The large nerve roots in the low back that go to the legs may be irritated
# * The smaller nerves that supply the low back may be irritated
# * The large paired lower back muscles (erector spinae) may be strained
# * The bones, ligaments or joints may be damaged
# * An intervertebral disc may be degenerating
# 
# An irritation or problem with any of these structures can cause lower back pain and/or pain that radiates or is referred to other parts of the body. Many lower back problems also cause back muscle spasms, which don't sound like much but can cause severe pain and disability.
# 
# While lower back pain is extremely common, the symptoms and severity of lower back pain vary greatly. A simple lower back muscle strain might be excruciating enough to necessitate an emergency room visit, while a degenerating disc might cause only mild, intermittent discomfort.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

import os
print(os.listdir("../input"))

sns.set(style="whitegrid", color_codes=True)
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Load Dataset

# In[ ]:


columns =  ['Pelvic Incidence','Pelvic Tilt','Lumbar Lordosis Angle',            'Sacral Slope','Pelvic Radius','Degree Spondylolisthesis',            'Pelvic Slope','Direct Tilt','Thoracic Slope',            'Servical Tilt','Sacrum Angle','Scoliosis Slope','Class']

spines = pd.read_csv('../input/Dataset_spine.csv',                     header=0,names= columns,usecols=range(0,13))

spines.head(6).T


# ## Exploratory Data Analysis

# In[ ]:


print ('No of Observations : {}'.format(spines.shape[0]))
print ('No of Features :{}'.format (spines.shape[1] -1))


# In[ ]:


print("Features with Missing counts:\n{}".format(spines.isnull().sum()))


# In[ ]:


sns.countplot(x = "Class", data = spines)
plt.title('Class Variable Distribution')
plt.show()


# In[ ]:


spines.describe().T


# In[ ]:


spines.hist(figsize=(12,12),bins = 20)
plt.title("Features Distribution")
plt.show()


# In[ ]:


spines.boxplot(figsize=(16,6))
plt.title("Features Value Ranges")
plt.ylim(ymax=200)
plt.xticks(rotation=45,)
plt.show()


# In[ ]:


fig,ax = plt.subplots(nrows = 3, ncols=4, figsize=(16,10))
row = 0
col = 0
for i in range(len(spines.columns) -1):
    if col > 3:
        row += 1
        col = 0
    axes = ax[row,col]
    sns.boxplot(x = spines['Class'], y = spines[spines.columns[i]],ax = axes)
    col += 1
plt.tight_layout()
# plt.title("Individual Features by Class")
plt.show()


# ### Split dataset and and Normalized

# In[ ]:


normalizer = Normalizer()
X_normalized = normalizer.fit_transform(spines.iloc[:,0:12].values)
X_train_norm, X_test_norm,y_train_norm,y_test_norm = train_test_split(    X_normalized,spines['Class'].values,test_size=0.40,random_state = 1)
# without transformation
X_train, X_test,y_train,y_test = train_test_split(    spines.iloc[:,0:12].values,spines['Class'].values,test_size=0.40,random_state = 1)


# In[ ]:


def knn(train_features,train_predictor, test_features,test_predictor, k_value):
    train_accuracy = []
    test_accuracy = []
    for k in k_value:
        clf = KNeighborsClassifier(n_neighbors=k).fit(train_features,train_predictor)
        train_accuracy.append(clf.score(train_features,train_predictor))
        test_accuracy.append(clf.score(test_features,test_predictor))

    plt.plot(k_value,train_accuracy, label = 'Train', color = 'blue')
    plt.plot(k_value,test_accuracy, label = 'Test', color = 'red')
    plt.title('Train-Test Accuracy Plot')
    plt.xlabel('Nearest Neighbors counts')
    plt.ylabel('Model Accuracy')
    plt.legend()


# In[ ]:


# Normalized data
k_values = range(1,21)
knn(X_train_norm, y_train_norm,X_test_norm,y_test_norm,k_values)
plt.title("KNN - With Normalized transformation")
plt.show()


# In[ ]:


clf = KNeighborsClassifier(n_neighbors=12).fit(X_train_norm, y_train_norm)
print('Training Set Accuracy at (K = 12) ==> \t{:.4}'.format(                        clf.score(X_train_norm, y_train_norm)))
print('Test Set Accuracy at (K = 12) ==> \t{:.4}'.format(                        clf.score(X_test_norm, y_test_norm)))


# In[ ]:


# raw data
k_values = range(1,21)
knn(X_train, y_train,X_test,y_test,k_values)
plt.title("KNN - Without transformation")
plt.show()


# **Conclusion:**
# After normalization, we can see that the variance in the test and the training has been reduced significantly and provide pretty similar result with less noise. 
