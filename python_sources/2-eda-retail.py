#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


counties = pd.read_csv("../input/counties.csv")
test_data =pd.read_csv('../input/test.csv')


# In[ ]:


counties.head()


# ## Data Cleaning and EDA
# 
# * Replace Null value
# * Remove Outliers 
# 

# In[ ]:


from pandas import DataFrame
#Checking for missing values

numerical_features = counties.select_dtypes(include=[np.number]).columns.tolist()

Missing_values=DataFrame(counties).isnull().sum().sort_values(ascending=False)
print("Missing_values")
print(Missing_values)

#Imputing missing values with median

for column in numerical_features:
    counties[column]=counties[column].fillna(counties[column].median())

#Checking for missing values

Missing_values_new=DataFrame(counties).isnull().sum().sort_values(ascending=False)
print("Missing_values after imputation")
print(Missing_values_new)


# In[ ]:


counties.describe()


# In[ ]:


# Data Cleaning for test Data

from pandas import DataFrame
#Checking for missing values

numerical_features = test_data.select_dtypes(include=[np.number]).columns.tolist()

Missing_values=DataFrame(test_data).isnull().sum().sort_values(ascending=False)
print("Missing_values")
print(Missing_values)

#Imputing missing values with median

for column in numerical_features:
    test_data[column]=test_data[column].fillna(test_data[column].median())

#Checking for missing values

Missing_values_new=DataFrame(test_data).isnull().sum().sort_values(ascending=False)
print("Missing_values after imputation")
print(Missing_values_new)


# In[ ]:


test_data.describe()


# ###  EDA on Access

# In[ ]:


Access = counties[['LACCESS_POP10','LACCESS_LOWI10','LACCESS_HHNV10','is_store_decline']]
Access.head()


# In[ ]:


#Check Correlation matrix
sns.set(style="white")

corr = Access.corr()


# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(7, 7))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmax=.3, center=0,annot=True,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


# In[ ]:


counties[['LACCESS_POP10','LACCESS_LOWI10','LACCESS_HHNV10']].hist(figsize=(16, 10), bins=50, xlabelsize=8, ylabelsize=8);


# ### EDA on Stores

# In[ ]:


stores = counties[['GROC09','GROCPTH09','SUPERC09','SUPERCPTH09','CONVS09','CONVSPTH09','SPECS09','SPECSPTH09','SNAPS12','SNAPSPTH12','is_store_decline']]


# In[ ]:


idx = pd.IndexSlice
mask = stores.loc[:,'CONVS09']==0
stores[mask] = 1


# In[ ]:


stores[stores['CONVS09']==0]


# In[ ]:


#stores['Stores_with_Snap_benefits'] = stores['SNAPS12'] / stores['GROC09']
#stores['SPECS09_with_Snap_benefits'] = stores['SNAPS12'] / stores['SPECS09']
stores['CONVS09_with_Snap_benefits'] = stores['SNAPS12'] / stores['CONVS09']
#stores['SUPERC09_with_Snap_benefits'] = stores['SNAPS12'] / stores['SUPERC09']
#stores['stores_with_grocery'] = stores['GROC09'] + stores['CONVS09']
stores['total_stores_snap_benefits'] = stores['SNAPS12'] / (stores['GROC09']+ stores['CONVS09']+ stores['SPECS09'])
stores.head()


# In[ ]:


#Check Correlation matrix
sns.set(style="white")

corr = stores.corr()


# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(15, 15))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmax=.3, center=0,annot=True,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


# In[ ]:


counties[['GROC09','GROCPTH09','SUPERC09','SUPERCPTH09','CONVS09','CONVSPTH09','SPECS09','SPECSPTH09','SNAPS12','SNAPSPTH12','is_store_decline']].hist(figsize=(16, 10), bins=50, xlabelsize=8, ylabelsize=8);


# ### EDA on Health

# In[ ]:


health=counties[['PCT_DIABETES_ADULTS08','PCT_OBESE_ADULTS08','RECFAC09','is_store_decline']]
health.head()


# In[ ]:


#Check Correlation matrix
sns.set(style="white")

corr = health.corr()


# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(6, 6))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmax=.3, center=0,annot=True,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


# In[ ]:


counties[['PCT_DIABETES_ADULTS08','PCT_OBESE_ADULTS08','RECFAC09','is_store_decline']].hist(figsize=(16, 10), bins=50, xlabelsize=8, ylabelsize=8);


# ## EDA on Socioeconomic Characteristics
# 

# In[ ]:


social=counties[['MEDHHINC15','METRO13','POPLOSS10','POVRATE15','PERPOV10','is_store_decline']]
social.head()


# In[ ]:


#Check Correlation matrix
sns.set(style="white")

corr = social.corr()


# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(8, 8))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmax=.3, center=0,annot=True,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


# In[ ]:


counties[['MEDHHINC15','METRO13','POPLOSS10','POVRATE15','PERPOV10','is_store_decline']].hist(figsize=(16, 10), bins=50, xlabelsize=8, ylabelsize=8);


# ## EDA on Bureau of Economic Analysis (BEA) data
# 

# In[ ]:


BEA = counties[['POP_2009','Per_Cap_2009','Personal_income_2009','is_store_decline']]
BEA['pop_per_store'] = BEA['POP_2009'] /( stores['GROC09']+ stores['CONVS09']+ stores['SPECS09'])


# In[ ]:


#Check Correlation matrix
sns.set(style="white")

corr = BEA.corr()


# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(8, 8))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmax=.3, center=0,annot=True,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


# ## Feature engineering 
# 
# As per the EDA we can make below 2 new features 
# 
# * Population per store - pop_per_store
# * SNAP authorised convienient store - CONVS09_with_Snap_benefits
# * Total SNAP authorised store - total_stores_snap_benefits

# In[ ]:


# Make zero value Non-Zero to avoid Infynity value
counties['CONVS09']=counties['CONVS09'].apply(lambda x: 1 if x == 0 else x)


# In[ ]:


counties['pop_per_store'] = counties['POP_2009'] /( counties['GROC09']+ counties['CONVS09']+ counties['SPECS09'])
counties['CONVS09_with_Snap_benefits'] = counties['SNAPS12'] / counties['CONVS09']
counties['total_stores_snap_benefits'] = counties['SNAPS12'] / (counties['GROC09']+ counties['CONVS09']+ counties['SPECS09'])


# In[ ]:


counties = counties[['FIPS','State','County','GROC09','GROCPTH09','SUPERC09','SUPERCPTH09','CONVS09','CONVSPTH09','SPECS09','SPECSPTH09','SNAPS12','SNAPSPTH12','is_store_decline','LACCESS_POP10','LACCESS_LOWI10','LACCESS_HHNV10','PCT_DIABETES_ADULTS08','PCT_OBESE_ADULTS08','RECFAC09','MEDHHINC15','METRO13','POPLOSS10','POVRATE15','PERPOV10','POP_2009','Per_Cap_2009','Personal_income_2009','pop_per_store','CONVS09_with_Snap_benefits','total_stores_snap_benefits' ]]


# In[ ]:


counties.head()


# In[ ]:


#Check if there is any Inf value
counties[counties['total_stores_snap_benefits']==np.inf]


# In[ ]:


counties.to_csv('model.csv',index=False)


# In[ ]:


# Make zero value Non-Zero to avoid Infynity value
test_data['CONVS14']=test_data['CONVS14'].apply(lambda x: 1 if x == 0 else x)


# In[ ]:


test_data[test_data['CONVS14'] ==0]


# In[ ]:


test_data['pop_per_store'] = test_data['Pop_2014'] /( test_data['GROC14']+ test_data['CONVS14']+ test_data['SUPERC14'])
test_data['CONVS14_with_Snap_benefits'] = test_data['SNAPS16'] / test_data['CONVS14']
test_data['total_stores_snap_benefits'] = test_data['SNAPS16'] / (test_data['GROC14']+ test_data['CONVS14']+ test_data['SPECS14'])


# In[ ]:


test_data[test_data['total_stores_snap_benefits']==np.inf]


# In[ ]:


test_data.head()


# In[ ]:


test_data.to_csv('test.csv',index=False)


# ## Observation 
# 
# * Cant detect any outliers 
# * Replaced missing value to median

# In[ ]:




