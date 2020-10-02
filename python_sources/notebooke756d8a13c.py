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

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv("../input/creditcard.csv")


# In[ ]:


df['Class'].value_counts()


# In[ ]:


df.describe()


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


#df=df.drop(['Time','Amount'], axis=1)


# In[ ]:


X= df.drop(['Class'] , axis = 1)
Y= df.Class
from sklearn.model_selection import train_test_split
X_train, X_test,Y_train,Y_test = train_test_split(X,Y, test_size = 0.10, random_state=0)


# In[ ]:


from sklearn.metrics import classification_report, roc_auc_score, roc_curve, auc

def roc_curve_acc(Y_test, Y_pred):
    false_positive_rate, true_positive_rate, thresholds = roc_curve(Y_test, Y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, 'b',label='AUC = %0.2f'% roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.svm import SVC


# In[ ]:


RF=RandomForestClassifier()
RF.fit(X_train, Y_train)
Y_pred=RF.predict(X_test)


# In[ ]:


print('roc_auc_score: %0.3f'% roc_auc_score(Y_pred,Y_test))


# In[ ]:


print("Random Forest Classifier report \n", classification_report(Y_pred,Y_test))
print('roc_auc_score: %0.3f'% roc_auc_score(Y_pred,Y_test))
roc_curve_acc(Y_test, Y_pred)


# In[ ]:



import pyttsx

