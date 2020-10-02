#!/usr/bin/env python
# coding: utf-8

# # Introduction
# website phishing dataset problem.
# Fitting Naive Bayes and creating confusion matrix of predicted values and real values I was able to get  78.81% accuracy.
# 

# # STEP #0: Import Libraries

# In[6]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# # STEP #1: IMPORT DATASET

# In[7]:


train=pd.read_csv('../input/Website Phishing.csv')
train.head(10)


# In[8]:


a=len(train[train.Result==0])
b=len(train[train.Result==-1])
c=len(train[train.Result==1])
print(a,"times 0 repeated in Result")
print(b,"times -1 repeated in Result")
print(c,"times 1 repeated in Result")


# # STEP #2: Explore /Visualze Data set

# In[9]:


sns.countplot(train['Result'])


# In[10]:


sns.heatmap(train.corr(),annot=True)


# In[11]:


sns.pairplot(train)


# In[12]:


train.info()
train.describe()


# In[13]:


X=train.drop('Result',axis=1).values 
y=train['Result'].values


# In[14]:


print(X)


# In[15]:


# transform the labels to 0's , 1's and -1's
from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
y = enc.fit_transform(y)

for i in range(0, len(X)):
    X[i] = enc.fit_transform(X[i])


# In[16]:


X


# # STEP #3: Prepare the Data for Training / Data Cleaning

# In[17]:


sns.heatmap(train.isnull(),cmap='Blues')


# # STEP #4: Model Training

# In[18]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=10)

# Show the results of the split
print("Training set has {} samples.".format(X_train.shape[0]))
print("Testing set has {} samples.".format(X_test.shape[0]))


# In[19]:


from sklearn.naive_bayes import MultinomialNB

#create Naive Bayes object
model=MultinomialNB(alpha=1.0)

#Train the model using training data 
model.fit(X_train,y_train)


# # STEP #5: Model Testing

# In[20]:


#import Evaluation metrics 
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
 
#Test the model using testing data
predictions = model.predict(X_test)


# In[21]:


from sklearn.metrics import confusion_matrix,classification_report
cm=confusion_matrix(y_test,predictions)
sns.heatmap(cm,annot=True)


# In[22]:


print("f1 score is ",f1_score(y_test,predictions,average='weighted'))
print("matthews correlation coefficient is ",matthews_corrcoef(y_test,predictions))

#secondary metric,we should not consider accuracy score because the classes are imbalanced.

print('****************************************************************************************')
print("The accuracy of your Naive bayes on testing data is: ",100.0 *accuracy_score(y_test,predictions))
print('****************************************************************************************')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




