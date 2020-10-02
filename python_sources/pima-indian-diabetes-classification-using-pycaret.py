#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # **Solving Diabetic problem with Pycaret library**

# importing data and assign it to df

# In[ ]:


df=pd.read_csv('/kaggle/input/pima-indians-diabetes-database/diabetes.csv')


# In[ ]:


df.columns


# In[ ]:


df.info


# In[ ]:


df.duplicated().sum() #checking for any duplicate record


# In[ ]:


#Frequency Distribution of dtypes
df.dtypes.value_counts().plot(kind='barh')


# In[ ]:


#Balanced dataset or not
print(df.Outcome.value_counts())
df.Outcome.value_counts().plot(kind='barh')


# In[ ]:


#We will define a fuction to give basic stats information

def simple_stats(df):
    b = pd.DataFrame()
    b['Missing value'] = df.isnull().sum()
    b['N unique value'] = df.nunique()
    b['min value'] = df.min()
    b['max value'] = df.max()
    b['Mean']=df.mean().T
    b['Median']=df.median().T
    b['Mode']=df.mode().T[0]
    b['Skewness'] = df.skew()
    b['dtype'] = df.dtypes
    return b

raw_stats=simple_stats(df)
raw_stats


# From above following observations can conclude:
# 
# After looking mean and median and mode and histogram we came to know that most of features are skewed just because of the zero values concentration on one side, and having some outliers
# On following columns, a value of zero does not make sense and thus indicates missing value.
# Glucose
# BloodPressure
# SkinThickness
# Insulin
# BMI
# 
# It is better to replace zeros with NaN as to replace NaN with suitable values would be easier.

# **Missing value treatment**

# In[ ]:


df_copy = df.copy(deep = True)
#replace zero values as nan in relevent columns
for i in df_copy[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']]:
    df_copy[i].replace(0, np.nan, inplace= True)
stats_with_NAN=simple_stats(df_copy)
stats_with_NAN


# *Lets do some visualization*

# In[ ]:


import seaborn as sns

sns.pairplot(df_copy, hue='Outcome')#,palette="husl")


# In[ ]:


sns.scatterplot(x = df_copy['Glucose'], y = df_copy['Age'], hue = "Outcome",
                    data = df_copy)


# In[ ]:



sns.scatterplot(x = df_copy['Glucose'], y = df_copy['Insulin'], hue = "Outcome",
                    data = df_copy)
sns.jointplot('Glucose','Insulin',data = df_copy,kind='hex',color = "g")


# In[ ]:


df_copy.head()


# In[ ]:


# !pip install pycaret


# In[ ]:


from pycaret.classification import *


# In[ ]:


#we will separate our train and test data.

data = df_copy.sample(frac=0.80, random_state=786)
data_unseen = df_copy.drop(data.index).reset_index(drop=True)
data.reset_index(drop=True, inplace=True)

print('Train Data for Modeling: ' + str(data.shape))
print('Test Data For Predictions: ' + str(data_unseen.shape))


# In[ ]:


#lets make setup required for claasification for using pycaret library
setup = setup(data = data, target = 'Outcome', session_id=123,normalize=True, remove_outliers=True, outliers_threshold=0.05)


# In[ ]:


compare_models()


# In[ ]:


#lets create Extreme Gradient boosting
lgb=create_model('lightgbm')


# In[ ]:


#now lets hypertune with pycaret
tuned_lgb=tune_model('lightgbm',n_iter=200)


# In[ ]:


plot_model(tuned_lgb, plot = 'confusion_matrix')


# In[ ]:


plot_model(tuned_lgb, plot = 'auc')


# In[ ]:


plot_model(tuned_lgb, plot = 'pr')


# In[ ]:


predict_model(estimator=tuned_lgb,data=data_unseen)


# # **we have seen its so simple to train models using pycaret for beginners**
