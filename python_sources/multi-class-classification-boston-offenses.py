#!/usr/bin/env python
# coding: utf-8

# ### More information. My [GitHub](https://github.com/OleksandrKosovan/predicting-boston-offense)

# # Import

# In[ ]:


import numpy as np
import pandas as pd


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB


# In[ ]:


from lightgbm import LGBMClassifier
#import xgboost as xgb


# In[ ]:


from sklearn.cross_validation import train_test_split


# In[ ]:


from sklearn.metrics import f1_score


# # Functions

# In[ ]:


# DecisionTreeClassifier

def function_DecisionTreeClassifier(X_train, Y_train, X_test, Y_test):
    
    # fit
    dec_tree = DecisionTreeClassifier()
    dec_tree = dec_tree.fit(X_train, Y_train)

    # predict
    dec_tree_pred = dec_tree.predict(X_test)
    
    # score
    dec_tree_score = f1_score(Y_test, dec_tree_pred, average=None)
    dec_tree_score_micro = f1_score(Y_test, dec_tree_pred, average='micro')
    
    return dec_tree_score, dec_tree_score_micro


# In[ ]:


# ExtraTreeClassifier

def function_ExtraTreeClassifier(X_train, Y_train, X_test, Y_test):
    
    # fit
    ext_tree = ExtraTreeClassifier()
    ext_tree = ext_tree.fit(X_train, Y_train)

    # predict
    ext_tree_pred = ext_tree.predict(X_test)
    
    # score
    ext_tree_score = f1_score(Y_test, ext_tree_pred, average=None)
    ext_tree_score_micro = f1_score(Y_test, ext_tree_pred, average='micro')
    
    return ext_tree_score, ext_tree_score_micro


# In[ ]:


# RandomForestClassifier

def function_RandomForestClassifier(X_train, Y_train, X_test, Y_test):
    
    # fit
    ran_for = RandomForestClassifier()
    ran_for = ran_for.fit(X_train, Y_train)

    # predict
    ran_for_pred = ran_for.predict(X_test)
    
    # score
    ran_for_score = f1_score(Y_test, ran_for_pred, average=None)
    ran_for_score_micro = f1_score(Y_test, ran_for_pred, average='micro')
    
    return ran_for_score, ran_for_score_micro


# In[ ]:


# LGBMClassifier

def function_LGBMClassifier(X_train, Y_train, X_test, Y_test):
    
    # fit
    lgbm = LGBMClassifier()
    lgbm = lgbm.fit(X_train, Y_train)

    # predict
    lgbm_pred = lgbm.predict(X_test)
    
    # score
    lgbm_score = f1_score(Y_test, lgbm_pred, average=None)
    lgbm_score_micro = f1_score(Y_test, lgbm_pred, average='micro')
    
    return lgbm_score, lgbm_score_micro


# In[ ]:


# BernoulliNB

def function_BernoulliNB(X_train, Y_train, X_test, Y_test):
    
    # fit
    bernoulli = BernoulliNB()
    bernoulli = bernoulli.fit(X_train, Y_train)

    # predict
    bernoulli_pred = bernoulli.predict(X_test)
    
    # score
    bernoulli_score = f1_score(Y_test, bernoulli_pred, average=None)
    bernoulli_score_micro = f1_score(Y_test, bernoulli_pred, average='micro')
    
    return bernoulli_score, bernoulli_score_micro


# In[ ]:


# KNeighborsClassifier

def function_KNeighborsClassifier(X_train, Y_train, X_test, Y_test):
    
    # fit
    kn = KNeighborsClassifier()
    kn = kn.fit(X_train, Y_train)

    # predict
    kn_pred = kn.predict(X_test)
    
    # score
    kn_score = f1_score(Y_test, kn_pred, average=None)
    kn_score_micro = f1_score(Y_test, kn_pred, average='micro')
    
    return kn_score, kn_score_micro


# In[ ]:


# GaussianNB

def function_GaussianNB(X_train, Y_train, X_test, Y_test):
    
    # fit
    gaus = GaussianNB()
    gaus = gaus.fit(X_train, Y_train)

    # predict
    gaus_pred = gaus.predict(X_test)
    
    # score
    gaus_score = f1_score(Y_test, gaus_pred, average=None)
    gaus_score_micro = f1_score(Y_test, gaus_pred, average='micro')
    
    return gaus_score, gaus_score_micro


# # Data

# In[ ]:


df = pd.read_csv('../input/data.csv')


# In[ ]:


df = df.drop('Unnamed: 0',1)
df = df.drop('Unnamed: 0.1',1)
df = df.drop('Unnamed: 0.1.1',1)


# In[ ]:


df.columns


# In[ ]:


df = df[[
    'DAY_OF_WEEK', 
    'DISTRICT', 
    'HOUR', 
    'Lat', 
    'Long', 
    'MONTH',
    'REPORTING_AREA', 
    'Day', 
    'Night', 
    'ToNight', 
    'ToDay', 
    'temperatureMin', 
    'temperatureMax', 
    'precipitation', 
    'snow',
    'temperatureDifference', 
    'clust_50', 
    'clust_100', 
    'clust_200',
    'Universities_colleges_distance_25',
    'Universities_colleges_distance_min',
    'Universities_colleges_number_near', 
    'Public_schools_distance_25',
    'Public_schools_distance_min', 
    'Public_schools_number_near',
    'Non-Public_schools_distance_25', 
    'Non-Public_schools_distance_min',
    'Non-Public_schools_number_near',
    'OFFENSE_CODE_GROUP'
]]


# In[ ]:


df.isnull().sum()


# In[ ]:


df['OFFENSE_CODE_GROUP'].value_counts().head(11)


# In[ ]:


list_offense_code_group = (
    'Motor Vehicle Accident Response',
    'Larceny',
    'Medical Assistance',
    'Simple Assault',
    'Violations',
    'Investigate Person',
    'Vandalism',
    'Drug Violation',
    'Larceny From Motor Vehicle',
    'Towed'
)


# In[ ]:


df_model = pd.DataFrame()


# In[ ]:


i = 0

while i < len(list_offense_code_group):

    df_model= df_model.append(df.loc[df['OFFENSE_CODE_GROUP'] == list_offense_code_group[i]])
    
    i+=1


# In[ ]:


df.shape


# In[ ]:


df_model.shape


# In[ ]:


df_model.columns


# In[ ]:


# DAY_OF_WEEK

df_model['DAY_OF_WEEK'] = df_model['DAY_OF_WEEK'].map({
    'Tuesday':2, 
    'Saturday':6, 
    'Monday':1, 
    'Sunday':7, 
    'Thursday':4, 
    'Wednesday':3,
    'Friday':5
})

df_model['DAY_OF_WEEK'].unique()


# In[ ]:


df_model.fillna(0, inplace = True)


# In[ ]:


df_model.isnull().sum()


# In[ ]:


y = df_model['OFFENSE_CODE_GROUP']


# In[ ]:


y.unique()


# In[ ]:


y = y.map({
    'Motor Vehicle Accident Response':1, 
    'Larceny':2, 
    'Medical Assistance':3,
    'Simple Assault':4, 
    'Violations':5, 
    'Investigate Person':6, 
    'Vandalism':7,
    'Drug Violation':8, 
    'Larceny From Motor Vehicle':9, 
    'Towed':10
})


# In[ ]:


x = df_model.drop('OFFENSE_CODE_GROUP', 1)


# In[ ]:


x.columns


# # Split data

# In[ ]:


# Split dataframe into random train and test subsets

X_train, X_test, Y_train, Y_test = train_test_split(
    x,
    y, 
    test_size = 0.1,
    random_state=42
)

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)


# # Modeling

# In[ ]:


function_DecisionTreeClassifier(X_train, Y_train, X_test, Y_test)


# In[ ]:


function_ExtraTreeClassifier(X_train, Y_train, X_test, Y_test)


# In[ ]:


function_RandomForestClassifier(X_train, Y_train, X_test, Y_test)


# In[ ]:


function_LGBMClassifier(X_train, Y_train, X_test, Y_test)


# In[ ]:


function_BernoulliNB(X_train, Y_train, X_test, Y_test)


# In[ ]:


function_KNeighborsClassifier(X_train, Y_train, X_test, Y_test)


# In[ ]:


function_GaussianNB(X_train, Y_train, X_test, Y_test)


# In[ ]:




