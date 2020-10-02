#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import dask.dataframe as dd
from dask_ml.preprocessing import DummyEncoder
import numpy as np
import altair as alt
import seaborn as sns
import math

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
from sklearn import metrics

from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans

from sklearn.linear_model import LinearRegression
from sklearn import svm


plt.style.use('ggplot')


# # Crime Classification in San Francisco
# ## Multi-class classification
# https://www.kaggle.com/c/sf-crime
# 
# "From 1934 to 1963, San Francisco was infamous for housing some of the world's most notorious criminals on the inescapable island of Alcatraz.
# 
# Today, the city is known more for its tech scene than its criminal past. But, with rising wealth inequality, housing shortages, and a proliferation of expensive digital toys riding BART to work, there is no scarcity of crime in the city by the bay.
# 
# From Sunset to SOMA, and Marina to Excelsior, this competition's dataset provides nearly 12 years of crime reports from across all of San Francisco's neighborhoods. Given time and location, you must predict the category of crime that occurred."
# 
# 
# ![image.png](attachment:image.png)

# In[ ]:


# 878049 rows x 9 columns
data = pd.read_csv('../input/crimetrain/crimetrain.csv', parse_dates=["Dates"])
# train = pd.read_csv('crimetrain.csv')
data.head()


# In[ ]:


data.info()


# In[ ]:


print("Num of Categories: ", data['Category'].nunique())
print("Num of Descripts: ", data['Descript'].nunique())


# In[ ]:


data.Resolution.unique()


# - TREA = Trespassing or loitering near posted industrial property

# # Exploratory Data Analysis

# In[ ]:


encodeddata = pd.read_csv('../input/crimetrain/crimetrain.csv')
labelencoder = LabelEncoder()
for col in encodeddata.columns:
    encodeddata[col] = labelencoder.fit_transform(encodeddata[col])


# In[ ]:


plt.figure(figsize = (16,5))
ax = sns.heatmap(encodeddata.corr(), annot=True)


# ## What is the most popular crime?

# In[ ]:


data = pd.read_csv('../input/crimetrain/crimetrain.csv', parse_dates=['Dates'])


# In[ ]:


popcrime = data.groupby('Category').count().reset_index()
popcrime = popcrime.drop(['Dates', 'Descript', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X'], axis=1)
popcrime = popcrime.rename(columns={'Y':'count'}).sort_values(by='count', ascending=False)
popcrime.plot.bar(x='Category', y='count', figsize=(15, 8))
plt.ylabel("count")


# ## What district is the most dangerous?

# In[ ]:


dangerous = data.groupby('PdDistrict').count().reset_index()
dangerous = dangerous.drop(['Dates', 'Category', 'Descript', 'DayOfWeek', 'Resolution', 'Address', 'X'], axis=1)
dangerous = dangerous.rename(columns={'Y':'num_of_crimes'}).sort_values(by='num_of_crimes', ascending=False)
dangerous.plot.bar(x='PdDistrict', y='num_of_crimes', figsize=(10, 5))
plt.ylabel('Number of Crimes')


# ## PdDistrict and Category

# In[ ]:


# cpddist = data.groupby(['Category', 'PdDistrict']).count().reset_index()
# for category in cpddist['Category'].unique():
#     ddata = cpddist[cpddist['Category'] == category]
#     ddata.plot.bar(x='PdDistrict', y='Dates') # doesn't matter which, just looking at count
#     plt.xlabel(category)
#     plt.ylabel('Count')


# ## Percentage of crime by PdDistrict

# In[ ]:


data.head()


# In[ ]:


# adding a total column
perct = pd.crosstab([data.Category], data.PdDistrict).reset_index()
perct['total'] = perct.sum(axis=1)

# calculating percent for each row        
for district in data.PdDistrict.unique():
    perct[district+'%'] = perct.apply(lambda perct: perct[district]/perct.total*100, axis=1)

# dropping unncessary columns
perct = perct.drop(['BAYVIEW', 'CENTRAL', 'INGLESIDE', 'MISSION', 'NORTHERN', 'PARK', 'RICHMOND', 'SOUTHERN', 'TARAVAL', 'TENDERLOIN', 'total'], axis=1)
perct.head()


# In[ ]:


perct.plot.bar(x='Category', y=['NORTHERN%', 'PARK%', 'INGLESIDE%', 'BAYVIEW%', 'RICHMOND%', 'CENTRAL%', 'TARAVAL%', 'TENDERLOIN%', 'MISSION%', 'SOUTHERN%'], stacked=True, figsize=(21,10))
plt.ylabel('% of PdDistrict')


# In[ ]:


perct.plot.bar(x='Category', y=['NORTHERN%', 'PARK%', 'INGLESIDE%', 'BAYVIEW%', 'RICHMOND%', 'CENTRAL%', 'TARAVAL%', 'TENDERLOIN%', 'MISSION%', 'SOUTHERN%'], figsize=(21,10))
plt.ylabel('% of PdDistrict')


# In[ ]:


# what district is the hightest for prostitution? --it's hard to tell looking at the graph so let's pull up the table
p = data[data['Category'] == 'PROSTITUTION'].groupby(['Category', 'PdDistrict']).count().reset_index().sort_values(by='Dates', ascending=False)
p = p.drop(['Dates', 'Descript', 'DayOfWeek', 'Resolution', 'Address', 'X'], axis=1)
p = p.rename(columns={'Y':'count'}).sort_values(by='count', ascending=False)
p


# ### Takeaways
# - PdDistrict may not be the best indicator of Category, but there are definitely some PdDistricts where certain crimes occur more so than others

# ## Category and Descript

# In[ ]:


descript = data.groupby(['Category', 'Descript']).count().reset_index()
descript = descript.drop(['Dates', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X'], axis=1)
descript = descript.rename(columns={'Y':'count'}).sort_values(by='count', ascending=False)
descript.head(n=10)


# ## Time Series  

# In[ ]:


timedata = pd.read_csv('../input/crimetrain/crimetrain.csv', parse_dates=['Dates'])


# In[ ]:


timedata['Dates_year'] = timedata['Dates'].dt.year
timedata['Dates_month'] = timedata['Dates'].dt.month
timedata['Dates_day'] = timedata['Dates'].dt.day
timedata['Dates_hour'] = timedata['Dates'].dt.hour

fig, ((axis1,axis2),(axis3,axis4)) = plt.subplots(nrows=2, ncols=2)
fig.set_size_inches(18,6)

sns.countplot(data=timedata, x='Dates_year', ax=axis1)
sns.countplot(data=timedata, x='Dates_month', ax=axis2)
sns.countplot(data=timedata, x='Dates_day', ax=axis3)
sns.countplot(data=timedata, x='Dates_hour', ax=axis4)


# ### Takeaways
# - Why are the number of crimes for 2015 so low?
# - Number of crimes relatively the same from day to day except for the first of the month and the 31 (because not all months have 31 days)
# - Crimes by hour pretty interesting. Descreases from midnight to 5:00am and steadily increases from 8:00am to 6:00pm with a spike at noon

# In[ ]:


# cpddist = data.groupby(['Category', 'DayOfWeek']).count().reset_index()
# for category in cpddist['Category'].unique():
#     ddata = cpddist[cpddist['Category'] == category]
#     ddata.plot.bar(x='DayOfWeek', y='Dates')
#     plt.xlabel(category)
#     plt.ylabel('Count')


# ## Number of cases bi-weekly

# In[ ]:


timedata['Dates_week'] = timedata['Dates'].dt.week
weekly = timedata[['Dates_week', 'Dates_year']]
weekly = pd.crosstab([weekly.Dates_week], weekly.Dates_year).reset_index()
grab_dates = weekly.iloc[:, 1:]
weekly.plot(x='Dates_week', y=grab_dates.columns, figsize=(20, 8))


# ### Takeaways
# - The dataset does not contain data past June 2015
# - Crime seems to decrease just a bit in the beginning of summer

# ## Number of cases hourly by PdDistrict

# In[ ]:


hourly = timedata[['Dates_hour', 'PdDistrict']]
hourly = pd.crosstab([hourly.Dates_hour], hourly.PdDistrict).reset_index()
grab_dists = hourly.iloc[:, 1:]
hourly.plot(x='Dates_hour', y=grab_dists.columns, figsize=(20, 8))
# plt.xticks(np.arange(min(x), max(x)+1, 1.0))


# In[ ]:


hourly = timedata[['Dates_hour', 'PdDistrict']]
pd.crosstab([hourly.Dates_hour], hourly.PdDistrict).reset_index().sort_values(by='SOUTHERN', ascending=False).head()


# ### Takeaways
# - The number of crimes fall between midnight and 5:00am for each district
# - Number of crimes increases from 5:00am to 8:00am, level off for a little bit until noon
# - The number of crimes jumps up around noon
# - The greatest number of crimes occur around 6:00pm
# - Ingleside seems to be the only (sort of) anomaly 

# ## Top 10 address with the most crimes across the years

# In[ ]:


addryear = timedata[(timedata.Address == '800 Block of BRYANT ST') | (timedata.Address == '800 Block of MARKET ST') | 
             (timedata.Address == '2000 Block of MISSION ST') | (timedata.Address == '1000 Block of POTRERO AV') | 
             (timedata.Address == '900 Block of MARKET ST') | (timedata.Address == '0 Block of TURK ST') |
             (timedata.Address == '0 Block of 6TH ST') | (timedata.Address == '300 Block of ELLIS ST') |
             (timedata.Address == '400 Block of ELLIS ST') | (timedata.Address == '16TH ST / MISSION ST')]
addressyear = addryear[['Dates_year', 'Address']]
addressyear = pd.crosstab([addryear.Dates_year], addryear.Address).reset_index()
grab_addresses = addressyear.iloc[:, 1:]
addressyear.plot(x='Dates_year', y=grab_addresses.columns, figsize=(20, 9))
plt.ylabel('Number of Crimes')


# In[ ]:


timedata.groupby(['Category', 'PdDistrict', 'Address']).count().reset_index().sort_values(by='Dates', ascending=False)


# ### Takeaways
# - The number of crimes by address stays relatively the same (at least for the top 10 most crime ridden areas) over the years except for 800 Block of BRYANT ST and 800 Block of MARKET ST whicy appear to have a lot of peeks and valleys. This may have to do with the fact that both of these addresses are part of the Southern district--the distict known for having the most criminal actitivity.

# # Testing

# In[ ]:


datareorder = data[['Category', 'Descript', 'Dates', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X', 'Y']]
datareorder.head(n=1)


# In[ ]:


labelencoder = LabelEncoder()
for col in datareorder.columns:
    datareorder[col] = labelencoder.fit_transform(datareorder[col])
datareorder.head()


# ## GaussianNB

# In[ ]:


from sklearn.naive_bayes import GaussianNB
model_naive = GaussianNB()


# In[ ]:


X = datareorder.iloc[:, 1:] 
y = datareorder.iloc[:, 0]


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# In[ ]:


X_train


# In[ ]:


model_naive.fit(X_train, y_train)
nb_pred = model_naive.predict(X_test)


# In[ ]:


accuracy_score(y_test, nb_pred)


# In[ ]:


confusion_matrix(y_test, nb_pred)
# true positive, false negative
# false positive, true negative


# In[ ]:


print(classification_report(y_test, nb_pred, target_names = data['Category'].unique()))


# ## Decision Trees

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
model_tree = DecisionTreeClassifier(max_features="auto")


# In[ ]:


model_tree.fit(X_train, y_train)
tree_pred = model_tree.predict(X_test)


# In[ ]:


accuracy_score(y_test, tree_pred)


# In[ ]:


confusion_matrix(y_test, tree_pred)


# In[ ]:


print(classification_report(y_test, tree_pred, target_names=data['Category'].unique()))


# ## Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
model_forest = RandomForestClassifier(max_features="auto") # max_features=20


# In[ ]:


model_forest.fit(X_train, y_train)
forest_pred = model_forest.predict(X_test)


# In[ ]:


accuracy_score(y_test, forest_pred)


# In[ ]:


x = confusion_matrix(y_test, forest_pred)
for item in x:
    print(x)


# In[ ]:


print(classification_report(y_test, forest_pred, target_names=data['Category'].unique()))


# ## Does one-hot encoding improve results?

# In[ ]:


data.head()


# #### Must use dask because of memory error that occurs with pandas

# In[ ]:


dask = dd.read_csv("../input/crimetrain/crimetrain.csv", parse_dates=['Dates'])
# dropping some columns because memory errors are still occuring. Dropping Descript because keeping it 
# feels like cheating anyway, as well as DayOfWeek, X, and Y. Dropping Category so dask doesn't one hot encode it
dask = dask.drop(['Category', 'Descript', 'DayOfWeek', 'X', 'Y'], axis=1)
# telling dask what columns are categorical for one hot
dask = dask.categorize(columns=['PdDistrict', 'Resolution', 'Address'])
# moving columns around
dask = dask[['Dates', 'PdDistrict', 'Resolution', 'Address']]


# In[ ]:


dask.columns


# In[ ]:


# one hot encoding categorical data
enc = DummyEncoder(["PdDistrict", "Resolution", "Address"])


# In[ ]:


enc


# In[ ]:


dask = enc.fit_transform(dask)


# In[ ]:


dask.columns


# In[ ]:


# prints every column in dask
# cols = list(dask.columns[0:])
# cols
# dask[cols].compute()


# In[ ]:


# the kernel keeps dying here
# Xoh = dask 
# yoh = datareorder.iloc[:, 0]
# Xoh_train, Xoh_test, yoh_train, yoh_test = train_test_split(Xoh, yoh, test_size=0.2)


# In[ ]:


# model_forest.fit(X_train, y_train)
# forest_pred = model_forest.predict(X_test)


# The kernel keeps dying everytime I try to split the data into a train and test set. Seeing if labeling encoding the data improves results will have to wait until another time.

# ## How does dropping the Descript column (the column having the highest correlation with Category) compare to the previous Random Forest model?

# In[ ]:


dropDes = datareorder.drop(["Descript"], axis=1)
dropDes.head()


# In[ ]:


XdropDes = dropDes.iloc[:, 1:] 
ydropDes = dropDes.iloc[:, 0]


# In[ ]:


XdropDes_train, XdropDes_test, ydropRes_train, ydropDes_test = train_test_split(XdropDes, ydropDes, test_size=0.2)


# In[ ]:


model_forestDropDes = RandomForestClassifier(max_features="auto") # max_features=20
model_forestDropDes.fit(XdropDes, ydropDes)
forest_predDropDes = model_forestDropDes.predict(XdropDes_test)


# In[ ]:


accuracy_score(ydropDes_test, forest_predDropDes)


# In[ ]:


confusion_matrix(ydropDes_test, forest_predDropDes)


# In[ ]:


# print(classification_report(ydropDes_test, forest_predDropDes, target_names=data['Category'].unique()))


# ## Summary

# Out of the GaussianNB, Decision Tree, and Random Forest classifiers, the Random Forest Classifier performed the best concerning accuracy with a score of .92 (remarkably better than the Gaussian's and Decision Tree's .44 and .77 respectively), and most likely the confusion matrix as well, though it is difficult to be certain as the confusion matrix is so big that it is hard to print out in a readable format. Additionally, after removing the Descript column, the Random Forest classifier did noteably worse (accuracy score of .84) as expected given that Descript had the highest correlation with the Category variable that we were trying to predict. One hot encoding everything still needs to be desired as well as attempting to classify the data using SVM and Logistic Regression.

# In[ ]:




