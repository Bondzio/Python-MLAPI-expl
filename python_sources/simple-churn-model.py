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

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


PATH = '../input/dsb_2019/'

product_master = pd.read_csv(PATH+'product_master.csv')
training_data = pd.read_csv(PATH+'training_data.csv')
customer_master = pd.read_csv(PATH+'customer_master.csv')


# Training Data

# In[ ]:


training_data.head()


# > Simple Churn Model: Check the range of data available

# In[ ]:


print('Minimum date is', min(training_data.Bill_Date))
print('Maximum date is',max(training_data.Bill_Date))


# Lets assume we are building a churn model for the last 3 months, so we need to look at the data before 3 months, ie; 3 months prior to 15th September ( aka the observation window) and see if the person comes back in the next 3 months (The performance window). 
# 
# So observation window here is **1st January 2016 - 15th June 2018**
#    Performance window here is **16th June 2018 - 15th September 2018**

# Lets build a model with just 1 variable, the customer's number of visits previously. To see if we can predict correctly whether the person will come back or not in the next 3 months

# In[ ]:



counts = training_data.groupby(['Customer_Id']).Bill_Date.nunique()
counts.name = 'Number of Previous Visits'


# In[ ]:





# In[ ]:


#Churn Definition: If the customer has not come in the performance window, we mark 1 else 0. Ie, whether his last visit occurs before the performance window

y_var = training_data.groupby(['Customer_Id']).Bill_Date.max() < '2018-06-16'
y_var.name = 'Churned'
y_var


# In[ ]:


Dataset = counts.to_frame().join(y_var)
Dataset.head(100)


# Usual hygeine, divide into train and test and see if we can predict who has churned

# In[ ]:


# Distribution of customers who have churned or not
Dataset.Churned.value_counts()


# In[ ]:


# Model fitting
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

from sklearn.linear_model import LogisticRegression
from sklearn import metrics

# Dependent variable

X = Dataset['Number of Previous Visits']
y = Dataset['Churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
logreg = LogisticRegression()

X_train= X_train.values.reshape(-1, 1)
X_test= X_test.values.reshape(-1, 1)
y_train = y_train.values.reshape(-1, 1)
y_test = y_test.values.reshape(-1, 1)

logreg.fit(X_train, y_train)


# In[ ]:


y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))


# In[ ]:


from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()


# In[ ]:


output = logreg.predict(X.values.reshape(-1,1))
output = pd.DataFrame(output)
output['Customer_Id'] = X.index
output.to_csv('Output.csv',index = False)

