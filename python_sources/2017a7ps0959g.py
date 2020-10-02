#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
sys.path.append('/kaggle/input/eval-lab-1-f464-v2/')


# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt


# In[ ]:


df = pd.read_csv('/kaggle/input/eval-lab-1-f464-v2/train.csv')
df.head()


# In[ ]:


#checking for missing values
df.isnull().any()


# In[ ]:


#filling voids
df.fillna(value = df.mean(), inplace = True)
df.head()


# In[ ]:


df.isnull().any().any()


# In[ ]:


corr = df.corr()
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
plt.figure(figsize=(10,10))
with sns.axes_style("white"):
    ax = sns.heatmap(corr, mask=mask, vmax=.3, square=True, annot = True, center = 0)


# In[ ]:


#creating feature datasets x, label dataset y 
from sklearn.preprocessing import label_binarize
arr = df.to_numpy()
x = np.delete(arr, [0,10,13], axis = 1)
x
y= np.delete(arr, [0,1,2,3,4,5,6,7,8,9,10,11,12], axis = 1)
type(y)
y = np.array([int(i) for i in y])


# In[ ]:


test = pd.read_csv('/kaggle/input/eval-lab-1-f464-v2/test.csv')

#filling NaNs
test.fillna(value = test.mean(), inplace = True)

test.isnull().any().any()


# In[ ]:


#final test dataset x_test
x_test = np.delete(test.to_numpy(), [0,10,13], axis = 1)


# In[ ]:


#splitting datasets
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=42)


# In[ ]:


from sklearn.ensemble import ExtraTreesClassifier
clf2 = ExtraTreesClassifier(n_estimators = 450, max_depth = None, random_state = 0)
clf2.fit(X_train,y_train)


# In[ ]:


result2 = clf2.predict(X_test)


# In[ ]:


accuracy_score(y_test, result2)


# In[ ]:


#fitting on complete dataset
clf2.fit(x,y)


# In[ ]:


ans = clf2.predict(x_test)


# In[ ]:


# for submission4.csv
sub = pd.DataFrame()
sub['id'] = test['id']
sub['rating'] = ans
sub.to_csv('submission4.csv', sep = ',')


# In[ ]:


#for submission3.csv
clf3 = ExtraTreesClassifier(n_estimators = 200, max_depth = None, random_state = 0)
clf3.fit(X_train,y_train)


# In[ ]:


result3 = clf3.predict(X_test)


# In[ ]:


accuracy_score(y_test, result3)


# In[ ]:


clf3.fit(x,y)


# In[ ]:


ans2 = clf3.predict(x_test)


# In[ ]:


sub1 = pd.DataFrame()


# In[ ]:


sub1['id'] = test['id']
sub1['rating'] = ans2
sub.to_csv('submission3.csv', sep = ',')


# In[ ]:




