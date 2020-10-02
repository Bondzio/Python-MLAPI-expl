#!/usr/bin/env python
# coding: utf-8

# This is a simple kernel, where we preprocess the dataset and then train a logistics regression and XGBClassifier in order to classify possible churning customers. 

# ****
# First we import data processing libraries and check the data for missing and duplicate values.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

data = pd.read_csv('../input/WA_Fn-UseC_-Telco-Customer-Churn.csv')

#check for missing data
missing_data = data.isnull().sum(axis=0).reset_index()
missing_data.head(10)


# In[ ]:


#check for duplicates
duplicates = data.duplicated().sum(axis=0)
print(duplicates == True)


# There is no missing or duplicate data, so we move on to analysis of the features to examine which could be the most interesting ones. We plot the features using **seaborn**.

# In[ ]:


#plot features in relation to Churn
for i, predictor in enumerate(data.drop(columns=['Churn', 'TotalCharges', 'MonthlyCharges'])):#['gender', 'PhoneService', 'MultipleLines', 'InternetService','SeniorCitizen', 'tenure', 'Contract', 'PaperlessBilling', 'PaymentMethod']):
    plt.figure(i)
    sns.countplot(data=data, x=predictor, hue='Churn')

sns.lmplot(data=data, x='TotalCharges', y='MonthlyCharges', hue='Churn',fit_reg=False)


# **Choosing predictors**
# Good predictors seem to be *Dependents, tenure, PhoneService, InternetService, InternetServices extras (but not streaming), Contract, Billing/PaymentMethod.* From Total/MonthlyCharges it looks that *MonthlyCharges* is a better predictor of churn - the higher the charge the more likely is the customer to churn.
# 
# 
# In the next code section we drop the columns that look like weak predictors and use encoding techniques to encode the categorical variables. We will use numerical encoding as well as one hot encoding, since some of the categorical variables have clear hierarchy (good for numeric encoding) and some do not. 

# In[ ]:


#data preprocessing
#aggregate and encode categorical variables
from sklearn.preprocessing import LabelEncoder

#custID only serves to identify the customer, should have no influence on the propensity to churn
#also drop other weak predictors
data = data.drop(columns=['customerID','StreamingMovies',"StreamingTV", 'gender', 'TotalCharges', 'MultipleLines'])

#change the value 'No internet service' in the internet addon variables to 'No' as they signify the same thing 
encodedData = data.replace(to_replace='No internet service', value='No')

#one hot encode categorical variables that do not have explicit hierarchy - 'InternetService', 'PaymentMethod', 'Contract'
ohe_data = pd.get_dummies(encodedData,columns=['InternetService', 'PaymentMethod', 'Contract'])

#encode the rest of categorical variables to numeric
encodedData = ohe_data.apply(lambda x: LabelEncoder().fit_transform(x) if x.dtype == 'object' else x)


# Maybe there is correlation between number of activated addon services and the propensity to churn? Families vs. Individuals? Let's see.

# In[ ]:


#add features that aggregate some of the columns to better analyze their influence
encodedData['famSize'] = encodedData[['Partner', 'Dependents']].sum(axis=1)
encodedData['InternetServicesAddons'] = encodedData[['OnlineSecurity','OnlineBackup',
                                                    'DeviceProtection', 'TechSupport']].sum(axis=1)
#analyze the aggregated variables
plt.figure()
sns.countplot(data=encodedData, x='famSize', hue='Churn')
plt.figure()
sns.countplot(data=encodedData, x='InternetServicesAddons', hue='Churn')


# It appers that there is a relationship between size of the customers family, the number of internet services they use and the likelihood to churn.
# 
# We have selected independent variables we believe have influence on the churn (dependent variable), the next step is to train some classification models and evaluate them. We will use traditional** logisitics regression **as well as **gradient boosted random forest** and use ROC curve as a metric to see which performs better.  We will also test a 3 sets of predictors.

# In[ ]:


#train and validate classifier
from sklearn import linear_model, metrics
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

#define dependent variable
y = encodedData.Churn

#define sets of predictors

#in this set we will use the aggregated variables for internet service addons and family size
X = encodedData.drop(columns=['Churn', 'OnlineSecurity','OnlineBackup','DeviceProtection',
                                'TechSupport'])

#here we will not use the aggregated variables
X2 = encodedData.drop(columns=['famSize', 'InternetServicesAddons','Churn'])

d = {0: "X", 1: "X2"}

for i, predictors in enumerate([X, X2]):
    print('Results with predictors %s:' % d[i])
    xTrain, xTest, yTrain, yTest = train_test_split(predictors,y)

    #train and evaluate linear model
    linearModel = linear_model.LogisticRegression() 
    linearModel.fit(xTrain, yTrain)

    predictionsLinear = linearModel.predict(xTest)

    fpr, tpr, t = metrics.roc_curve(yTest, predictionsLinear)
    auroc = metrics.auc(fpr, tpr)

    print("AUC of Linear Model: %f" % (auroc))

    XGBeval = {}
    #train and evaluate XGBModel using a number of trees as a parameter
    #we also use a greedier learning_rate and maxdepth to try and better fit the data altough we risk overfitting
    for n in range(10, 200, 10):
        xgbModel = XGBClassifier(maxdepth=9, n_estimators=n, learning_rate=0.1, seed=42)
        xgbModel.fit(xTrain, yTrain)

        predictionsXGB = xgbModel.predict(xTest)

        fprX, tprX, tX = metrics.roc_curve(yTest, predictionsXGB)
        aurocX = metrics.auc(fprX, tprX)
        XGBeval[aurocX] = n
    best = max(XGBeval.keys())
    print("best performing XGBModel -> AUC : %f, trees = %d" % (best, XGBeval[best]))


# The classifiers are fairly close in performance with the  predictor sets making only small difference.
# That being said, with ROC at ~0.7 the performance could likely be improved.
# 
# **Things to contemplate:**
# * using an automated technique to select best features and to optimize the XGBModel
