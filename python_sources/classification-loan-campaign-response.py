#!/usr/bin/env python
# coding: utf-8

# In[ ]:



# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
#import pydot, graphviz
from IPython.display import Image  
from sklearn.externals.six import StringIO  
from sklearn.tree import export_graphviz
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


# In[ ]:


df = pd.read_csv('../input/loan-campaign/PL_XSELL.csv')


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


df.shape


# In[ ]:


df.TARGET.value_counts()


# ## Tableau Insights
# 

# In[ ]:


from IPython.display import Image
Image("../input/tableau-insights/Capture.PNG")


# In[ ]:


from IPython.display import Image
Image("../input/tableau-insights/Capture1.PNG")


# In[ ]:


from IPython.display import Image
Image("../input/tableau-insights/Capture2.PNG")


# In[ ]:


from IPython.display import Image
Image("../input/tableau-insights/Capture4.PNG")


# In[ ]:


from IPython.display import Image
Image("../input/tableau-insights/Capture5.PNG")


# In[ ]:


X = df.drop(['CUST_ID','GENDER','OCCUPATION','AGE_BKT','ACC_TYPE','ACC_OP_DATE','random','TARGET'],axis=1)
y = df['TARGET']


# In[ ]:


from imblearn.over_sampling import SMOTE

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

print("Number transactions X_train dataset: ", X_train.shape)
print("Number transactions y_train dataset: ", y_train.shape)
print("Number transactions X_test dataset: ", X_test.shape)
print("Number transactions y_test dataset: ", y_test.shape)


# In[ ]:


print("Before OverSampling, counts of label '1': {}".format(sum(y_train==1)))
print("Before OverSampling, counts of label '0': {} \n".format(sum(y_train==0)))

sm = SMOTE(random_state=2)
X_train_res, y_train_res = sm.fit_sample(X_train, y_train.ravel())

print('After OverSampling, the shape of train_X: {}'.format(X_train_res.shape))
print('After OverSampling, the shape of train_y: {} \n'.format(y_train_res.shape))

print("After OverSampling, counts of label '1': {}".format(sum(y_train_res==1)))
print("After OverSampling, counts of label '0': {}".format(sum(y_train_res==0)))


# In[ ]:


y_train.ravel()


# In[ ]:


#!pip install imblearn


# In[ ]:


pd.DataFrame(data=X_train_res,columns=X_train.columns)


# In[ ]:


d=pd.DataFrame({'Target':y_train_res})
d.Target.value_counts()


# ### Decision Tree

# In[ ]:


dt_default = DecisionTreeClassifier(max_depth=5)
dt_default.fit(X_train_res, y_train_res)


# In[ ]:


y_pred_default = dt_default.predict(X_test)
print(accuracy_score(y_test, y_pred_default))#after sampling
print(classification_report(y_test, y_pred_default))


# In[ ]:


print(confusion_matrix(y_test,y_pred_default))


# In[ ]:


y_accuracy = accuracy_score(y_test,y_pred_default)
print("Accuracy : {}".format(y_accuracy*100))


# In[ ]:


#Sensitivity = TP/(FN+TP)
Sensitivity = 36/(739+36)
print("Sensitivity : {}".format(Sensitivity))


# In[ ]:


#Specificity = TN/(TN+FP)
Specificity = 5205/(5205+20)
print("Specificity : {}".format(Specificity))


# ### Logistic Regression

# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.3, random_state = 2)
X_train.head()


# In[ ]:


LR1 = LogisticRegression()
LR1.fit(X_train_res,y_train_res)
y_pred = LR1.predict(X_test)


# In[ ]:


y_cm = metrics.confusion_matrix(y_test,y_pred)
y_cm


# In[ ]:


y_acc = metrics.accuracy_score(y_test,y_pred)
print("Accuracy : {}".format(y_acc*100))


# In[ ]:


#Sensitivity = TP/(FN+TP)
Sensitivity = 1/(774+1)
print("Sensitivity : {}".format(Sensitivity))


# In[ ]:


#Specificity = TN/(TN+FP)
Specificity = 5225/(5225+0)
print("Specificity : {}".format(Specificity))

