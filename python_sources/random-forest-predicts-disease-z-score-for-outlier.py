#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


df = pd.read_csv("../input/heart-disease-uci/heart.csv")


# In[ ]:


df.shape


# In[ ]:


#No null values in the data
df.isnull().mean()


# In[ ]:


sns.pairplot(df)


# In[ ]:


#Confirms the presence of outliers, example in trestbps, chol etc.
fig, ax = plt.subplots(figsize=(10,5))
sns.boxplot(df['chol'])


# In[ ]:


fig, ax = plt.subplots(figsize=(10,5))
sns.boxplot(df['trestbps'])


# In[ ]:


#Confirms the presence of outliers
fig, ax = plt.subplots(figsize=(10,10))
ax.scatter(df['age'], df['chol'])
ax.set_xlabel('Age')
ax.set_ylabel('Chol')
plt.show()


# In[ ]:


#Using z-score to find outliers
from scipy import stats
import numpy as np
z = np.abs(stats.zscore(df))
threshold = 3
print(np.where(z > 3))


# In[ ]:


#Removing outliers
df = df[(z < 3).all(axis=1)]


# In[ ]:


df.shape
#5 percent data is lost due to removal of outliers which is sort of acceptable.


# In[ ]:


df['target'].value_counts()


# In[ ]:


y = df['target']
X = df.drop(['target'], axis = 1)


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.25,random_state = 0)


# In[ ]:


classifier = DecisionTreeClassifier(max_depth = 3,random_state=1)
classifier.fit(X_train,y_train)
y_pred = classifier.predict(X_test)
confusion_matrix(y_test,y_pred)


# In[ ]:


print("Accuracy:- ",accuracy_score(y_test,y_pred))
cv_score = cross_val_score(classifier,X,y,cv=10)
print("Cross validation score ",cv_score.mean())


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
for est in [5,10,50,100,500,1000,2000,5000]:
    classifier = RandomForestClassifier(n_estimators=est,random_state=0)
    classifier.fit(X_train,y_train)
    y_pred = classifier.predict(X_test)
    confusion_matrix(y_test,y_pred)
    print('Estimator:-',est)
    print("Accuracy:- ",accuracy_score(y_test,y_pred))
    cv_dec_tree_clf = cross_val_score(classifier,X,y,cv=10)
    print("Cross validation score ",cv_dec_tree_clf.mean())
    

