#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


        # Any results you write to the current directory are saved as output.


# In[ ]:


# Required Libraries
import numpy as np
import pandas as pd
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
plt.rc("font", size=20)
import category_encoders as ce
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn import model_selection
from sklearn import preprocessing
from sklearn import tree, ensemble, svm, naive_bayes, neighbors, discriminant_analysis, neural_network
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from xgboost import XGBClassifier
import gc
import plotly.offline as py#visualization
py.init_notebook_mode(connected=True)#visualization
import plotly.graph_objs as go#visualization
import plotly.tools as tls#visualization
import plotly.figure_factory as ff#visualization


# ### Read the data in to Pandas Data Frame object

# In[ ]:


data_df = pd.read_csv('/kaggle/input/telco-customer-churn/WA_Fn-UseC_-Telco-Customer-Churn.csv')
data_df.head()


# ### Data Overview
# ###### Observation: 
# 1. We see that there are no Missing Values
# 2. Except Senior Citizen, Tenure, Monthly Charge and  Total Charge, rest of the 16 features are Categorical.
# 3. Unique column indicate, number of unique values in per feature vector.
# 4. For Example, Gender Feature vector has 2 unique Values --> 'Male', 'Female'

# In[ ]:


print ("Rows     : " ,data_df.shape[0])
print ("Columns  : " ,data_df.shape[1])
print ("\nFeatures : \n" ,data_df.columns.tolist())
print ("\nMissing values :  ", data_df.isnull().sum().values.sum())
print ("\nUnique values :  \n",data_df.nunique())


# ### Data Cleaning
# Replace spaces in Total Charges Feature with Nan and drop all the rows correspoding to Null values

# In[ ]:


#Replacing spaces with null values in total charges column
data_df['TotalCharges'] = data_df["TotalCharges"].replace(" ",np.nan)
    
#Dropping null values from total charges column which contain .15% missing data 
data_df = data_df[data_df["TotalCharges"].notnull()]
data_df = data_df.reset_index()[data_df.columns]

#convert to float type
data_df["TotalCharges"] = data_df["TotalCharges"].astype(float)

# Reduced Data Set Size
print ("Rows     : " ,data_df.shape[0])
print ("Columns  : " ,data_df.shape[1])


# ### Exploratory Data Analysis
# 
# 1. We observe that, 1869 customers out of 7032 were subjected to attrition.
# 2. We have an Unblanaced Data Set.

# In[ ]:


print(data_df['Churn'].value_counts())
churn = len(data_df[data_df['Churn']==1])
not_churn = len(data_df[data_df['Churn']==0])
pct_not_churn = not_churn/(data_df.shape[0])
pct_churn = churn/(data_df.shape[0])
sns.countplot(x='Churn', data=data_df, label="Number of Customers", palette='hls')


# #### Observation 1: 
# 1. Nearly, equla Male and Female Customers
# 2. We observe that, both Male and Female are equivalent in classifying the churn and non-churn customers.
# 3. Nearly, 25% of Male and 26% of Female are non-churn customers.
# 4. Majoriy on the churn customers have No Dependents and Partners.
# 5. Further Step Could be derive family size of the customer and considered as one feature.
# 

# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 2), (0, 0))

data_df.Churn[data_df.gender == "Male"].value_counts(normalize=True).plot(kind="bar", alpha=0.5, title ='Churn Vs Male')

plt.subplot2grid((1, 2), (0, 1))

data_df.Churn[data_df.gender == "Female"].value_counts(normalize=True).plot(kind="bar", alpha=0.5, 
                                                                            title ='Churn Vs Female', color='orange')


# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 2), (0, 0))

data_df.Partner[data_df.Churn == "Yes"].value_counts().plot(kind="bar", alpha=0.5, title ='Partner Vs Churn Customers')

plt.subplot2grid((1, 2), (0, 1))

data_df.Partner[data_df.Churn == "No"].value_counts().plot(kind="bar", alpha=0.5, 
                                                                            title ='Partner Vs Non-Churn Customers', color='orange')


# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 2), (0, 0))

data_df.Dependents[data_df.Churn == "Yes"].value_counts().plot(kind="bar", alpha=0.5, title ='Dependents Vs Churn Customers')

plt.subplot2grid((1, 2), (0, 1))

data_df.Dependents[data_df.Churn == "No"].value_counts().plot(kind="bar", alpha=0.5, 
                                                                            title ='Dependents Vs Non-Churn Customers', color='orange')


# ### Observation 2:
# 1. Most of the Non-Chrun Customers have No - Multiple Lines,Device Protection, TechSupport, OnlineBackup, OnlineSecurity, StreamingTV, StreamingMovies.
# 2. A possible featire engineering step could be consider customers with No phone/internet service as No.

# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 3), (0, 0))

data_df.Churn[data_df.MultipleLines == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='Churn Vs MultipleLines-Yes')


plt.subplot2grid((1, 3), (0, 1))

data_df.Churn[data_df.MultipleLines == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='Churn Vs MultipleLines-No')

plt.subplot2grid((1, 3), (0, 2))

data_df.Churn[data_df.MultipleLines == 'No phone service'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='green',
                                                                              title='Churn Vs MultipleLines-No phone service')


# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 3), (0, 0))

data_df.Churn[data_df.OnlineBackup == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='Churn Vs OnlineBackup-Yes')


plt.subplot2grid((1, 3), (0, 1))

data_df.Churn[data_df.OnlineBackup == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='Churn Vs OnlineBackup-No')

plt.subplot2grid((1, 3), (0, 2))

data_df.Churn[data_df.OnlineBackup == 'No internet service'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='green',
                                                                              title='Churn Vs OnlineBackup-No internet service')


# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 3), (0, 0))

data_df.Churn[data_df.OnlineSecurity == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='Churn Vs OnlineSecurity-Yes')


plt.subplot2grid((1, 3), (0, 1))

data_df.Churn[data_df.OnlineSecurity == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='Churn Vs OnlineSecurity-No')

plt.subplot2grid((1, 3), (0, 2))

data_df.Churn[data_df.OnlineSecurity == 'No internet service'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='green',
                                                                              title='Churn Vs OnlineSecurity-No internet service')


# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 3), (0, 0))

data_df.Churn[data_df.TechSupport == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='Churn Vs TechSupport-Yes')


plt.subplot2grid((1, 3), (0, 1))

data_df.Churn[data_df.TechSupport == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='Churn Vs TechSupport-No')

plt.subplot2grid((1, 3), (0, 2))
data_df.Churn[data_df.TechSupport == 'No internet service'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='green',
                                                                              title='Churn Vs TechSupport-No internet service')


# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 3), (0, 0))

data_df.Churn[data_df.StreamingTV == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='Churn Vs StreamingTV-Yes')


plt.subplot2grid((1, 3), (0, 1))

data_df.Churn[data_df.StreamingTV == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='Churn Vs StreamingTV-No')

plt.subplot2grid((1, 3), (0, 2))
data_df.Churn[data_df.StreamingTV == 'No internet service'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='green',
                                                                              title='Churn Vs StreamingTV-No internet service')


# In[ ]:


fig = plt.figure(figsize=[18,7])
plt.subplot2grid((1, 3), (0, 0))

data_df.Churn[data_df.StreamingMovies == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='Churn Vs StreamingMovies-Yes')


plt.subplot2grid((1, 3), (0, 1))

data_df.Churn[data_df.StreamingMovies == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='Churn Vs StreamingMovies-No')

plt.subplot2grid((1, 3), (0, 2))
data_df.Churn[data_df.StreamingMovies == 'No internet service'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='green',
                                                                              title='Churn Vs StreamingMovies-No internet service')


# ### Observation 3:
# 1. Customers with loger contracts One/Two year are non-churn customers.
# 2. Greater than 80% of Churn Customers have Month-to-month Contract.

# In[ ]:


fig = plt.figure(figsize=[18,7])

plt.subplot2grid((1, 2), (0, 0))

data_df.Contract[data_df.Churn == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='Contract vs Churn-Yes')


plt.subplot2grid((1, 2), (0, 1))

data_df.Contract[data_df.Churn == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='Contract Vs Churn-No')


# ### Observation 4:
# 1. Most of the Churn Customers had payment method as - 'Electronic Check'
# 2. Susbequently lesser Churn customers in remaining method.
# 3. In the case of Non-Churn Customers, payment method is equally distributed.
# 4. Credit card - Method is most favourable

# In[ ]:


fig = plt.figure(figsize=[18,7])

plt.subplot2grid((1, 2), (0, 0))

data_df.PaymentMethod[data_df.Churn == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='PaymentMethod vs Churn-Yes')


plt.subplot2grid((1, 2), (0, 1))

data_df.PaymentMethod[data_df.Churn == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='PaymentMethod Vs Churn-No')


# In[ ]:


fig = plt.figure(figsize=[18,7])

plt.subplot2grid((1, 2), (0, 0))

data_df.PaperlessBilling[data_df.Churn == 'Yes'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='red', 
                                                                  title='Paperlessbilling vs Churn Customers')


plt.subplot2grid((1, 2), (0, 1))

data_df.PaperlessBilling[data_df.Churn == 'No'].value_counts(normalize=True).plot(kind="bar", alpha=0.5, color='orange',
                                                                title='Paperlessbilling Vs Non-Churn Customers')


# ### Data Engineering - Conversion of Categorical to Numerical

# In[ ]:


def convert_data(data):
    
    data.loc[data.gender == 'Male', 'gender'] = 1
    data.loc[data.gender == 'Female', 'gender'] = 0
        
    data.loc[data.MultipleLines == 'Yes', 'MultipleLines'] = 1
    data.loc[data.MultipleLines == 'No', 'MultipleLines'] = 0
    data.loc[data.MultipleLines == 'No phone service', 'MultipleLines'] = 2
    
    data.loc[data.InternetService == 'Fiber optic', 'InternetService'] = 1
    data.loc[data.InternetService == 'No', 'InternetService'] = 0
    data.loc[data.InternetService == 'DSL', 'InternetService'] = 2
    
    
    data.loc[data.Partner == 'Yes', 'Partner'] = 1
    data.loc[data.Partner == 'No', 'Partner'] = 0
    
    data.loc[data.Dependents == 'Yes', 'Dependents'] = 1
    data.loc[data.Dependents == 'No', 'Dependents'] = 0
    
    data.loc[data.PhoneService == 'Yes', 'PhoneService'] = 1
    data.loc[data.PhoneService == 'No', 'PhoneService'] = 0
    
    #replace 'No internet service' to No for the following columns
    replace_cols = [ 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                    'TechSupport','StreamingTV', 'StreamingMovies']
    for i in replace_cols : 
        data[i]  = data[i].replace({'No internet service' : 'No'})
        
    data.loc[data.OnlineSecurity == 'Yes', 'OnlineSecurity'] = 1
    data.loc[data.OnlineSecurity == 'No', 'OnlineSecurity'] = 0

    
    data.loc[data.OnlineBackup == 'Yes', 'OnlineBackup'] = 1
    data.loc[data.OnlineBackup == 'No', 'OnlineBackup'] = 0
    
    data.loc[data.DeviceProtection == 'Yes', 'DeviceProtection'] = 1
    data.loc[data.DeviceProtection == 'No', 'DeviceProtection'] = 0

    
    data.loc[data.TechSupport == 'Yes', 'TechSupport'] = 1
    data.loc[data.TechSupport == 'No', 'TechSupport'] = 0

    
    
    data.loc[data.StreamingTV == 'Yes', 'StreamingTV'] = 1
    data.loc[data.StreamingTV == 'No', 'StreamingTV'] = 0

    
    data.loc[data.StreamingMovies == 'Yes', 'StreamingMovies'] = 1
    data.loc[data.StreamingMovies == 'No', 'StreamingMovies'] = 0

    
    data.loc[data.PaperlessBilling == 'Yes', 'PaperlessBilling'] = 1
    data.loc[data.PaperlessBilling == 'No', 'PaperlessBilling'] = 0
    
    data.loc[data.Contract == 'Two year', 'Contract'] = 1
    data.loc[data.Contract == 'Month-to-month', 'Contract'] = 0
    data.loc[data.Contract == 'One year', 'Contract'] = 2
    
    data.loc[data.PaymentMethod == 'Mailed check', 'PaymentMethod'] = 1
    data.loc[data.PaymentMethod == 'Electronic check', 'PaymentMethod'] = 0
    data.loc[data.PaymentMethod == 'Bank transfer (automatic)', 'PaymentMethod'] = 2
    data.loc[data.PaymentMethod == 'Credit card (automatic)', 'PaymentMethod'] = 3
    
    data.loc[data.Churn == 'Yes', 'Churn'] = 1
    data.loc[data.Churn == 'No', 'Churn'] = 0
    
    data = data.drop('customerID', axis=1)
    return data

    
data_df = convert_data(data_df)


# In[ ]:


data_df.head()


# ### Strength of the Features

# In[ ]:


X = data_df.drop(['Churn'], axis=1)
y = data_df.Churn
model = ExtraTreesClassifier()
model.fit(X,y)
print(model.feature_importances_) #use inbuilt class feature_importances of tree based classifiers
#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(20).plot(kind='barh')


# In[ ]:


corr = data_df.corr()
corr.style.background_gradient(cmap='coolwarm')


# ### Building a Model
# 1. We performed Data cleaning and Data Exploration tasks.
# 2. Feature Engineering is not covered in this notebook
# 3. We build strong classification models and Output the accuracy score.
# 4. After identifying the best classifier for this problem, we can proceed to hyper parameter tuning Grid Search/Random Grid Search/Bayesian Optimization.
# 5. To measure performances we consider 10-fold CV score.

# In[ ]:


X = data_df.drop(['Churn'], axis=1)
y = data_df.Churn

target = data_df.Churn.values

X = (X - X.min())/ X.max()


# In[ ]:


names = ['KNN', 'LR', 'DT', 'RF', 'SVM', 'GNB', 'AB', 'QDA', 'NN', 'XGB']
# Classifiers
classifier_lr = LogisticRegression()
classifier_knn = neighbors.KNeighborsClassifier(3)
classifier_tree = tree.DecisionTreeClassifier(random_state=1234, max_depth=7, min_samples_split=2)
classifier_RF = ensemble.RandomForestClassifier(random_state=1234, max_depth=7, min_samples_split=2)
classifier_svm = svm.SVC(gamma='auto')
calssifier_gnb = naive_bayes.GaussianNB()
classifier_ab = ensemble.AdaBoostClassifier()
classifier_qda = discriminant_analysis.QuadraticDiscriminantAnalysis()
classifiers_nn = neural_network.MLPClassifier(alpha=10**-3, max_iter=1000)
classifers_xgb = XGBClassifier(learning_rate=0.1, n_estimators=140, max_depth=5, min_child_weight=3, 
                               gamma=0.2, subsample=0.6, colsample_bytree=1.0, 
                               objective='binary:logistic', nthread=4, scale_pos_weight=1, seed=27)
classifers = [classifier_knn, classifier_lr, classifier_tree, classifier_RF, classifier_svm, 
              calssifier_gnb, classifier_ab, classifier_qda, classifiers_nn, classifers_xgb]


# In[ ]:


cols = ['Classifier', 'Accuracy Score']
df_report = pd.DataFrame(columns=cols)
i = 0
for name, model in zip(names, classifers):
    scores = model_selection.cross_val_score(model, 
                                             X, y, scoring='accuracy', cv=50, verbose=0)
    df_report.loc[i] = [name, np.around(scores.mean(), decimals=5)]
    i += 1


# ## Result:
# 1. Logistic Regression and SVM have greater performances
# 2. KNN Performs the Lowest.

# In[ ]:


df_report.head(10)


# In[ ]:




