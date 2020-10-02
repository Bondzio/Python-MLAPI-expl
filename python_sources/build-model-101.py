#!/usr/bin/env python
# coding: utf-8

# # Build Model 101

# ### With this notebook, the model was build using titanic competition data. Variables with missing data are not used.It is a step in ***my learning journey*** towards how to build a simple model.

# ### Load the libraries

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
sns.set()

import warnings
warnings.filterwarnings("ignore")


# ### Load the dataset

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
train = pd.read_csv("../input/titanic/train.csv")
test= pd.read_csv("../input/titanic/test.csv")


# In[ ]:


df = train
df.head()


# In[ ]:


print(df.info())


# In[ ]:


print('Any missing values?')
df.isnull().sum()


# In[ ]:


# Class distribution
print(df.groupby('Survived').size())
print('')
print(df.Survived.value_counts(normalize=True))

# Plot of class distribution
sns.countplot(df['Survived'], label="Count");


# ### Correlation matrix

# In[ ]:


sns.set(font_scale=1.25)  
correlation_matrix = df.corr()
plt.figure(figsize=(10,10))
ax = sns.heatmap(correlation_matrix, vmax=1, square=True,annot=True,cmap='RdYlGn',annot_kws={'size': 13})
plt.title('Correlation matrix between the features')
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.show()


# In[ ]:


y = df.Survived
X = df.drop(['Survived','Sex','Name','Ticket','Cabin','Embarked'],axis=1)


# In[ ]:


print('Any missing values?')
X.isnull().sum()


# In[ ]:


X = df.drop(['Survived','Sex','Name','Ticket','Cabin','Embarked','Age'],axis=1)


# In[ ]:


seed = 1
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)


# In[ ]:


print('Data file  :', X.shape, y.shape)
print('Train data :', X_train.shape, y_train.shape)
print('Test data  :', X_test.shape, y_test.shape)


# ### Building the model
# 

# In[ ]:


from sklearn import preprocessing 
Standardisation = preprocessing.StandardScaler()
clf = LogisticRegression(random_state=seed)
X_scaled = preprocessing.scale(X_train)
X_test_scaled=preprocessing.scale(X_test)
X_train=X_scaled
X_test=X_test_scaled
clf.fit(X_train, y_train)


# In[ ]:


# Find the predictions first:
train_pred = clf.predict(X_train)
test_pred  = clf.predict(X_test)

print('Train acc:', clf.score(X_train, y_train))
print('Train acc:', accuracy_score(y_train, train_pred))
print('Test acc :', clf.score(X_test, y_test))


# In[ ]:


# The intercept
clf.intercept_


# In[ ]:


# All coefficients
clf.coef_


# In[ ]:


probs = clf.predict_proba(X_test)

data = {'Actual'   : y_test,
        'Predicted': test_pred,
        'Prob(0)'  : probs[:,0],
        'Prob(1)'  : probs[:,1]  
        }

dfprobs = pd.DataFrame (data)
dfprobs.sample(15)

