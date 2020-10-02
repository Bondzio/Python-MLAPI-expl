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
import sklearn.model_selection as sklearn

# Any results you write to the current directory are saved as output.


# In[ ]:


#load the lending club data as per the assignment 1 instructions
total_data=pd.read_csv("../input/loan.csv", low_memory=False)


# In[ ]:


#checking the data
total_data.head(n=5)


# In[ ]:


#only keep data for loans whose status is fully paid or default
data=total_data[(total_data.loan_status=='Fully Paid')|(total_data.loan_status=='Default')]
data['loan_status'].head(n=7)


# In[ ]:


#create new binary target variable
data['target']=(data['loan_status']=='Fully Paid')


# In[ ]:


#checking new variable target
data['target'].head(n=7)


# In[ ]:


#return the shape of the data (observations and columns/variables)
data.shape


# In[ ]:


#---------------------------------------------------------------Task 1---------------------------------------------------
#(how many record are there?)
len(data)


# In[ ]:


#----------------------------------------Task 2_----------------------------------------------------------------------


# In[ ]:


#import matplotlib.pyplot
import matplotlib.pyplot as plt


# In[ ]:


#plot the hystogram
plt.hist(data.loan_amnt, bins=50)


# In[ ]:


#Calculate mean, median, max and std of loan amount and funded amount via a loop
loans=['loan_amnt','funded_amnt']
for x in loans:
    print('The mean '+x+' is '+str(data[loans][x].mean()))
    print('The median '+x+' is '+str(data[loans][x].median()))
    print('The maximum '+x+' is '+str(data[loans][x].max()))
    print('The standard deviation '+x+' is '+str(data[loans][x].std()))


# In[ ]:


#alternative calculation
np.mean(data['loan_amnt'])


# In[ ]:


# compute median
data.loan_amnt.median()


# In[ ]:


# compute maximum
data.loan_amnt.max()


# In[ ]:


# compute standard deviation
data.loan_amnt.std()


# In[ ]:


#------------------------------------------Task 3------------------------------------------------------------------------


# In[ ]:


#mean of short and long term loans
data.groupby(by='term').int_rate.mean() #2 different terms: 36 and 60 months


# In[ ]:


#stdv of short and long term loans 
data.groupby(by='term').int_rate.std()


# In[ ]:


#boxplot the interest rate depending on the term
data.boxplot('int_rate',by='term',figsize=(7,7))


# In[ ]:


#---------------------------------------------------TASK 4 -----------------------------------------------------------------------


# In[ ]:


#Average int_rate depending on the debt grade
data.groupby(by='grade').int_rate.mean()


# In[ ]:


#average int_rate of the grade with the highest avg interest rate
data.groupby(by='grade').int_rate.mean().max()


# In[ ]:


#(Alternative)
max(data.groupby(by='grade').int_rate.mean())


# In[ ]:


#--------------------------------------------------------TASK 5-------------------------------------------------------------------


# In[ ]:


#Proportion (in percent) of loans in default
(1-data['target'].mean())*100


# In[ ]:


#creating default rate variable
data['default']=(1-data['target'])*100


# In[ ]:


#how does the default rate differs depending on grade
data.groupby(by='grade').default.mean()
#it grows as the grade goes down (except for grade G that is 0%)


# In[ ]:


#how does the interest rate differs depending on grade
data.groupby(by='grade').int_rate.mean()
#it grows as the grade goes down


# In[ ]:


#create variable yield (I define yield as the total amount collected from interest divided by the funded amount...)
# Also, I assume the interest rate provided is annual interest rate and there is no partial capital repayments; all capital is repaid at maturity)

data['short_t']=(data['term']==' 36 months')
data['long_t']=(data['term']==' 60 months')

data['r_yield']=(data['int_rate']*data['short_t']*3+data['int_rate']*data['long_t']*5)*data['target']


# In[ ]:


#cheking
print(data['r_yield'].mean())
print(data['term'].head())
print(data['int_rate'].head())
print(data['r_yield'].head())


# In[ ]:


#highest realized yield for any debt grade
data.groupby(by='grade').r_yield.max()


# In[ ]:


#---------------------------------------------------Task 6----------------------------------------------------------------------------


# In[ ]:


#number of records per aplication type 
data.groupby(by='application_type').size()

#It does not make much sens to use this feature for prediction beacause the vast mayority of the observations are of one type


# In[ ]:


#------------------------------------------------------------Task 7-------------------------------------------------------


# In[ ]:


#construc the model subdataset of selected features with dummy variables for the categorical variables
model_var=data[['loan_amnt','funded_amnt','funded_amnt_inv','term','int_rate','emp_length','addr_state',
             'verification_status','purpose','policy_code']]
model_var_dum=pd.get_dummies(model_var,columns=['term','emp_length','addr_state','verification_status','purpose'])


# In[ ]:


#shape of the new datasets
print(model_var.shape) # the original model has: 104+ observations, 10 variables
print(model_var_dum.shape) # the model with the dummy variables: 104+ obsevations, 86 variables


# In[ ]:


#Set the dependent variable 
target=data[['target']]
print(target.shape)
target_dum=pd.get_dummies(target)
print(target_dum.shape)


# In[ ]:


#-------------------------------------------------------------Task 8-----------------------------------------------------------------


# In[ ]:


#split data using sklearn train_test_split (test size = .33, random state= 42)
X_train, X_test, y_train, y_test= sklearn.train_test_split(model_var_dum, 
                                                           target_dum,
                                                           train_size=0.33,
                                                           random_state=42)


# In[ ]:


#shape of X.train and others
X_train.shape, y_train.shape, X_test.shape, y_test.shape


# In[ ]:


#-----------------------------------------------------Task 9---------------------------------------------------------------------------------------------------------


# In[ ]:


#import the relevant commands from sklearn library
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import metrics


# In[ ]:


#train the using Random Forest Classifier (n_estimators=100,max_depth=4,random_state=42)
rf_model=RandomForestClassifier(n_estimators=100,max_depth=4,random_state=42)


# In[ ]:


#Fit the model to the training data
rf_model.fit(X_train,y_train)


# In[ ]:


#Predict target and calculate the accuracy score
target_pred=rf_model.predict(X_test)

metrics.accuracy_score(y_test,target_pred)


# In[ ]:


#-----------------------------------------------Task 10---------------------------------------------------------------------------------


# In[ ]:


#repeat task 7-10 using total_data instead of data... and changing names accordingly
#(This is, remove the first step we took after importing the dataset. Where we removed all applicants with loan status other than
# fully paid and default)


# In[ ]:


#The prediction accuracy will be lower since the data in which we were working before, was overwhelmingly-representated by the Fully paid loan status
#as oposed to the other alternative (Default)... so, basically the model "could" predict that all the aplicants (in that sample) would
#fully pay and the accuracy would still be high (probably thats what is happening)
#The model prediction applied to the whole data (All loan status), would test the real prediction power!

