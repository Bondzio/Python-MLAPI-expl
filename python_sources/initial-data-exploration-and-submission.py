#!/usr/bin/env python
# coding: utf-8

# # Initial Data Exploration
# 
# ### Competition
# 
# In this competition, you will predict palm oil harvest productivity with data provided by AGROPALMA. The dataset contains information about palm trees, their harvest dates, atmospheric data during development of the plants and soil characteristics of the fields where the trees are located in.
# 
# http://www.agropalma.com.br/
# 
# ### What is palm oil?
# 
# Palm oil is an important and versatile vegetable oil which is used as a raw material for both food and non-food industries.
# 
# * Palm oil trees can grow up to 20 metres tall with an average life of 25 years.
# * Palm oil grows across or 10 degrees north / south of the equator.
# * The tree starts to bear fresh fruit bunches (FFBs) after three years.
# * The oil palm tree is also know as Elaeis Guineensis.
# * Each individual piece of fruit on fruit bunch contains 50% oil.
# * The nut, referred to as a kernel, at the centre of each piece of fruit, is where palm kernel oil is extracted from.
# * Palm oil can be harvested 12 months of the year.
# * Each tree can produce 10 tonnes of fresh fruit bunches per hectare.
# * On average 3.9 tonnes of crude palm oil and 0.5 tonnes of palm kernel oil can be extracted per hectare.
# * Leftover fibre from the palm kernel mill process provides a product called palm kernel expeller. This is used in animal feed, but can also be used to make products like paper or fertilizer.
# * Palm oil requires 10 times less land than other oil-producing crops.
# * It is entirely GM free
# 
# ### Objective
# 
# The purpose of this notebook is to perform the initial exploration of the presented data. Identify patterns, most important variables and distributions.
# 
# * Data analysis
# * Data visualization
# * Creating the Basic Model
# * Submission File Creation
# 
# Kaggle: https://www.kaggle.com/c/kddbr-2018

# ## Data Analisys
# 
# We will visualize the variables and datasets present in the competition to understand some existing patterns.

# In[ ]:


#!pip install seaborn==0.9.0


# In[ ]:


import pandas as pd
import numpy as np
import os 

import plotly.plotly as py
import plotly.graph_objs as go

from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

import warnings
warnings.filterwarnings('ignore')


# In[ ]:





# In[ ]:


# Private DataSet path: ../input/kddbr2018dataset/kddbr-2018-dataset/dataset. This dataset is the same of competitions
#
path = '../input/kddbr2018dataset/kddbr-2018-dataset/dataset/'
print(os.listdir(path))


# ### **train.csv** and **test.csv**
# 
# Basic data containing palm tree information

# In[ ]:


df_train = pd.read_csv(path+'train.csv')
df_test  = pd.read_csv(path+'test.csv')
df_all   = pd.concat([df_train, df_test])

print(df_train.shape, df_test.shape, df_all.shape)
df_all.head(3)


# In[ ]:


def to_date(df):
    return pd.to_datetime((df.harvest_year*10000+df.harvest_month*100+1)                                  .apply(str),format='%Y%m%d')
# Add date variable 
for d in [df_train, df_test, df_all]:
    d['date'] = to_date(d)


# #### #production
# 
# Analisys of the variable production

# In[ ]:


sns.distplot(df_all.production, hist=False, color="g",rug=True, kde_kws={"shade": True})
#sns.boxplot(x="production", y="field", data=df_train, palette="vlag")


# In[ ]:


print("Mean: ", df_all.production.mean())


# The #production is normalized betwenn [0,1] with mean 0.16. 

# In[ ]:


#df_all = df_all[(df_all.production < (df_all.production.mean()+df_all.production.std()*4)) | (df_all.production.isna())]


# In[ ]:


#data = [go.Scatter(x=df_all.date, y=df_all.production)]
#py.iplot(data)

f, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='date', y="production", data=df_all, palette="tab10", linewidth=2.5)

sns.despine(left=True)


# Average production per date follows a pattern. The end and beginning of the year is always low production, growing throughout the year until reaching peak production.
# 
# The year of 2011 had the highest peak of production of the entire time series, which has been growing over the years.

# In[ ]:


#df_all = df_all[df_all.harvest_year >= 2006]
df_all.shape


# It may be necessary to remove the data before 2006 because the production pattern has changed dramatically. This information prior to 2006 may bring noise, a better analysis should be made

# #### Production per month

# In[ ]:


f, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='harvest_month', y="production", data=df_all)

sns.despine(left=True)


# An everage of production in the year from month to month. It follows an increase in the year util the peak of production in month 10 and a sudden fall

# In[ ]:


mean_production = df_all.groupby(['harvest_month']).mean()['production'].reset_index()
mean_production.columns = ['harvest_month', 'production_mean']
mean_production

print(mean_production.shape)
mean_production.head(2)


# #### Production per age
# 
# With each harp the palmetto is a certain age. The production may vary with age, I also believe that some types of palm trees can only be harvested in a period of age

# In[ ]:


f, ax = plt.subplots(figsize=(12, 6))
#sns.lineplot(x='age', y="production", data=df_group, palette="tab10", linewidth=2.5)
sns.lineplot(x='age', y="production", data=df_all, palette="tab10", linewidth=2.5)

sns.despine(left=True)


# The plant reaches its maximum production at 15 years of age. Decreasing after this period. But depende the type

# #### Production per type
# 
# The 'type' of train/test is not established in the documentation, but, I will try to understand this variable.
# 

# In[ ]:


df_all.type.unique()


# In[ ]:


f, ax = plt.subplots(figsize=(12, 6))
#print(df_all.groupby(['type'])['date'].count())
sns.countplot(x="type", palette="tab10", data=df_all)


# Most of the production is carried out using the type 5.

# In[ ]:


ordered_days = df_all.type.value_counts().index
g = sns.FacetGrid(df_all, row="type", row_order=ordered_days, height=1.7, aspect=4,)
g.map(sns.distplot, "production", hist=False, rug=True, kde_kws={"shade": True});


# The production distribution by type is different. Although the predominant type is even type = 5, it may make sense to separate one model for each type.

# In[ ]:


type_prod = df_all.groupby(['date', 'type']).mean()['production'].reset_index()

print(mean_production.shape)
mean_production.head(2)

# Initialize a grid of plots with an Axes for each walk
grid = sns.FacetGrid(type_prod, col="type", hue="type", palette="tab10",
                     col_wrap=3, height=2.5)

grid.map(plt.plot, "date", "production")

grid.fig.tight_layout(w_pad=1)
sns.despine(left=True)


# The productive cycle and data are also different by type. This may reinforce the idea of separating forecast models by type.

# In[ ]:


f, ax = plt.subplots(figsize=(12, 6))
#sns.lineplot(x='age', y="production", data=df_group, palette="tab10", linewidth=2.5)
sns.lineplot(x='age', y="production", data=df_all, hue='type', palette="tab10", linewidth=2.5, legend='full')

sns.despine(left=True)


# Regarding age, apparently some types are only harvested at a certain age, that is, not all types have coliros during the clinical of 25 years. Only type 1 has production over 25 years.

# #### #field
# 
# field: an anonymous id given to each field in the dataset

# In[ ]:


df_all.field.unique()


# In[ ]:


f, ax = plt.subplots(figsize=(12, 6))
sns.countplot(x="field", data=df_all)


# Field 0 has the largest number of production records. Let's map some fields in time to identify if the pattern changes a lot in relation to the general.

# In[ ]:


fields    = [0, 9, 27] 
df_filter = df_all[df_all.field.isin(fields)]

f, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='date', y="production", data=df_filter, hue='field', palette="tab10", linewidth=2.5, legend='full')

sns.despine(left=True)


# In[ ]:


field_prod = df_all.groupby(['date', 'field']).mean()['production'].reset_index()

# Initialize a grid of plots with an Axes for each walk
grid = sns.FacetGrid(field_prod, col="field", hue="field", palette="tab10",
                     col_wrap=6, height=2.5)

grid.map(plt.plot, "date", "production")

grid.fig.tight_layout(w_pad=1)
sns.despine(left=True)


# Some changes, but the default is apparently the same as previously shown. Apparently all fields have production in the dataset presented for the period.

# In[ ]:





# In[ ]:


f, ax = plt.subplots(figsize=(12, 6))

# Draw a nested boxplot to show bills by day and time
sns.boxplot(x="field", y="production", data=df_all)
sns.despine(offset=10, trim=True)


# The average production per field is similar. Few variations.

# ### field_*.csv
# 
# These files hold atmospheric data from January 2002 to December 2017, and can be used to estimate the weather conditions during the development of the plant. Notice that weather does influence the production. Using only a single month prior to harvest is probably too little data. Participants should decide how far back in the past they want to look when training models.
# 
# 

# In[ ]:


# read
df_field = pd.read_csv(path+'field-0.csv')
df_field['field'] = 0
for i in range(1, 28):
    _df_field = pd.read_csv(path+'field-{}.csv'.format(i))
    _df_field['field'] = i
    df_field = pd.concat([df_field, _df_field])

# remove duplicates
df_field = df_field.drop_duplicates()

# Group 
df_field = df_field.groupby(['month', 'year', 'field']).mean().reset_index()
print(df_field.shape)
df_field.head()


# In[ ]:


# df_all
df_all   = pd.merge(df_all, df_field, left_on=['harvest_year', 'harvest_month','field'], 
                    right_on=['year', 'month', 'field'], how='inner').reset_index()

print(df_all.shape)
df_all.head()


# In[ ]:


df_all.columns


# In[ ]:


f, ax = plt.subplots(figsize=(10, 10))
features  = ['temperature', 'dewpoint',
               'windspeed', 'Soilwater_L1', 'Soilwater_L2', 'Soilwater_L3',
               'Soilwater_L4', 'Precipitation']
corr = df_all[features+['production']].corr()

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, annot=True, linewidths=.5,cmap="YlGnBu")


# An important point is that the variables Soilwater_l * have high correlation between each other and with the variable dewpoint. I do not think it's necessary to use all.

# In[ ]:


# Features i will duplicate with the past months
features  = ['temperature', 'dewpoint', 'windspeed', 'Precipitation', 'Soilwater_L1']

df_all    = df_all.drop(columns=['Soilwater_L2', 'Soilwater_L3','Soilwater_L4'])


# In[ ]:


#df_all2 = df_all.copy()
df_all.head()


# Relationship between the thermal variables, in the case this relation is for the harvest month itself. There is a good chance that previous months have relations with future production as well, it is necessary to investigate this relationship and how far it extends.

# In[ ]:


df_group = df_all.groupby(['field', 'date']).mean().reset_index()[['field', 'date', 'production'] + features ]
df_group = df_group.sort_values(['field', 'date'])
print(df_group.shape)
df_group.head()


# In[ ]:


# Collect shift values of variables in all features time
period = 2

new_features = {}
for f in features:
    new_features[f] = []
    for i in range(1, period):
        new_features[f].append('{}_{}'.format(f, i))
        df_group['{}_{}'.format(f, i)] = df_group[f].shift(i).fillna(df_group[f].mean())
        #df_group['{}_{}'.format(f, i)] = df_group[f].rolling(i, min_periods=1).mean().fillna(df_group.temperature.mean())


# Correlation analysis of the production variable with each variable in time. Uses a period of 11 months, a complete annual cycle. Each month is related to the correlation of production

# In[ ]:


fig = plt.figure(figsize=(18, 8))

for i in range(1, len(features)+1):
    ax1 = fig.add_subplot(240+i)
    
    f = features[i-1]
    f_filter = [f] + new_features[f]+['production']
    corr    = df_group[f_filter].corr()
    g = sns.barplot(x=[i-1 for i in range(1, period+1)], y=corr['production'].values[:-1], palette="YlGnBu", ax=ax1)
    plt.title(f)
    plt.xticks(rotation=45)
plt.show() #corr['production'].keys().values[:-1]


# In[ ]:


df_all.head()


# In[ ]:


df_group= df_group.drop(features+['production'], axis=1)
df_group.head()


# In[ ]:


df_all = df_all.drop(['index', 'month', 'year'], axis=1)
df_all = pd.merge(df_all, df_group, left_on=['field', 'date'], right_on=['field','date'], how='inner').reset_index()

print(df_all.shape)
df_all.head()


# ### soil_data.csv
# 
# Information on the soil on which each field is

# In[ ]:


df_soil = pd.read_csv(path+'soil_data.csv')
print(df_soil.shape)
df_soil.head()


# In[ ]:


# Join datasets
df_all_soil = pd.merge(df_all, df_soil, on='field', how='inner')
print(df_all_soil.shape)
df_all_soil.head()


# In[ ]:


f, ax = plt.subplots(figsize=(10, 10))
features  = list(df_soil.columns.values) + ['production']
corr      = df_all_soil[features].corr()

#Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, linewidths=.5,cmap="YlGnBu")


# ### Feature Importance Measures
# 
# Find the main features for the production target. Uses a RandomRorest to identify features
# 

# In[ ]:


df_all.columns


# In[ ]:


## Import the random forest model.
from sklearn.ensemble import RandomForestRegressor

## This line instantiates the model. 
rf = RandomForestRegressor() 

# data
df      = df_all_soil[~df_all_soil.production.isna()]
X_train = df.drop(['production', 'date', 'Id', 'index'], axis=1)
y_train = df.production.values

## Fit the model on your training data.
rf.fit(X_train, y_train) 


# In[ ]:


# feature_importances
feature_importances = pd.DataFrame(rf.feature_importances_, 
                                   index = X_train.columns, 
                                   columns=['importance']).sort_values('importance', ascending=False).reset_index()
feature_importances.head(3)


# In[ ]:


size = 50
f, ax = plt.subplots(figsize=(10, 10))
sns.barplot(x="importance", y='index', data=feature_importances.head(size), palette="rocket")


# Apparently the features coming from *soil_data.csv* do not have much relevance to the model. I think using only the field field is a better feature than adding 73 features of *soil_data.csv*

# ## Base Model 
# 
# #### Creation of a baseline model to finalize the competition submission pipeline. The idea is to create the most basic for future improvements.

# In[ ]:


from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import sklearn.model_selection


# #### Prepare Dataset

# In[ ]:


# Load Dataset
# y~X
df_train = df_all_soil[~df_all_soil.production.isna()]
X        = df_train.drop(['production', 'date', 'Id'], axis=1)

#Filter importance
features = list(feature_importances['index'].values)[:15]
X        = X[features]
# y
y        = df.production.values

# normalize
scaler = StandardScaler()
norm_X = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(norm_X, y, test_size=0.2, random_state=1)
(X_train.shape, X_test.shape)


# #### Train Model

# In[ ]:


base_model = RandomForestRegressor()
base_model.fit(X_train, y_train)


# In[ ]:


y_hat = base_model.predict(X_test)

score_mae = sklearn.metrics.mean_absolute_error(y_test, y_hat)
r2        = sklearn.metrics.r2_score(y_test, y_hat)

#MAE score 0.04333937538802412
print("MAE score", score_mae)


# In[ ]:


sns.jointplot(x=y_test, y=y_hat, kind="reg", color="m", height=7)
#sns.scatterplot(y=(y_test-y_hat), x=[i for i in range(len(y_test))], ax=ax2)


# In[ ]:


#df_all.to_csv('dataset/df_all.csv')


# ### Submission
# 
# It makes the predict of the basic model and creates the sample to substrate in kaggle, finishing the complete pipeline

# In[ ]:


df_test = df_all[df_all.production.isna()]
print(df_test.shape)
df_test.tail(2)


# Build test dataset to predict 

# In[ ]:


#Filter importance
X  = df_test[features]
X  = scaler.transform(X) # normalize

# y
y = df.production.values


# In[ ]:


prod = base_model.predict(X) 
prod[:10]


# In[ ]:


## create a submission.csv
import math
f = open('submission.csv', 'w')
f.write("Id,production\n")
for i in range(len(df_test.Id.values)):
    _id = df_test.Id.values[i]
    p   = math.fabs(prod[i])
    f.write("{},{}\n".format(_id, p))
f.close()


# #### Create a file *submission.csv*

# ...to be continued

# In[ ]:





# In[ ]:




