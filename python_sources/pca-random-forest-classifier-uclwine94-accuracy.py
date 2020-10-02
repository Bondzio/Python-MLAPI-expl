#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os 
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# Any results you write to the current directory are saved as output.


#  # As i was facing  file not found error so i get current working directory and absolute path of file

# In[ ]:


os.path.abspath('../input/wine.data')
os.getcwd()


# # Import Wine Dataset

# 

# In[ ]:


working_dir='/kaggle/input/wine.data'
dataset=pd.read_csv(working_dir)


# In[ ]:


#getting X and Y(target) from data
X=dataset.iloc[:,1:14].values
y=dataset.iloc[:,0].values


# In[ ]:


dataset.head()


# In[ ]:


Col_name=['Customer_Segment','Malic_Acid','Ash','Ash_Alcanity','Magnesium','Total_Phenols','Flavanoids','Nonflavanoid_Phenols','Proanthocyanins','Color_Intensity','Hue','OD280','Proline','Alcohol']


# In[ ]:


dataset.columns=Col_name


# In[ ]:


dataset.head(10)


# In[ ]:


dataset.describe()


# # Visualizing

# In[ ]:


plt.figure(figsize=(16,10))
sns.heatmap(dataset.corr(),annot=True)
plt.show()


# In[ ]:


dataset.info()


#  # splitting the dataset into the Training set and Test set

# In[ ]:



from sklearn.model_selection import train_test_split
X_train,X_test, y_train,y_test=train_test_split(X,y ,test_size=0.2,random_state=0) 


# # Feature Scaling

# In[ ]:




from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)


# # Applying Princinpal Component Analysis

# In[ ]:


from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
explained_variance = pca.explained_variance_ratio_
print(explained_variance)


# # Fitting RandomForst Classifier to the Training set

# In[ ]:



from sklearn.ensemble import RandomForestClassifier
classifier =RandomForestClassifier (n_estimators=10,criterion='entropy',random_state = 0)
classifier.fit(X_train, y_train)


#  # Predicting the Test set results

# In[ ]:


y_pred = classifier.predict(X_test)


# # Making the Confusion Matrix

# In[ ]:



from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


# # Calculating Accuracy

# In[ ]:


from sklearn.metrics import accuracy_score
accuracy=accuracy_score(y_test, y_pred)
print(accuracy)


# In[ ]:


from matplotlib.colors import ListedColormap
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green', 'blue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green', 'blue'))(i), label = j)
plt.title('Random Forest classifier (Training set)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()


# In[ ]:


# Visualising the Test set results
from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green', 'blue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green', 'blue'))(i), label = j)
plt.title('random forest classifier(Test set)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()


# In[ ]:




