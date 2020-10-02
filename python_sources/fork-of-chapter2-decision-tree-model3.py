#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf


# In[ ]:


#Import the dataset
churn_data = pd.read_csv('../input/churn_data.csv')
churn_data.head() #Printing first 5 rows of the dataset


# In[ ]:


# Check the data summary
churn_data.describe()


# In[ ]:


# Define X, y, which are IV and DV (Independent variable and dependent variable)
X=churn_data[['title','paymentMethod','couponDiscount','purchaseValue','giftwrapping','throughAffiliate','shippingFees','dvd','blueray','vinyl','videogame','videogameDownload','tvEquiment','prodOthers','prodSecondHand']]
y=churn_data['returnCustomer']


# In[ ]:


# Sklearn is a very popular package in maching learning, we will often use this
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


#Tell the model there are two categorical variables: title, paymentMethod
X=pd.get_dummies(X)

#Set 50% of the data as test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

#Decision tree
Tree = DecisionTreeClassifier(random_state=0,class_weight='balanced',max_depth=2)
Model = Tree.fit(X_train, y_train)


# In[ ]:


y_pred = Model.predict(X_test)
#test your model on new test data and show accuracy
print(Model.score(X_test, y_test))


# In[ ]:


# See accuracy in a table
pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True)


# In[ ]:


from sklearn.metrics import roc_curve, auc, roc_auc_score
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
auc(false_positive_rate, true_positive_rate)


# In[ ]:





# In[ ]:




