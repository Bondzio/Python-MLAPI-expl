#!/usr/bin/env python
# coding: utf-8

# ## Introduction
# 
# This notebook aims to introduce a standard way of 
# 
#  1. loading the data into python notebook 
#  2. Visual and identify issues
#  3. Pre-process the data e.g., variable transformation, normalization and etc. 

# In[ ]:


## Load packages
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

get_ipython().run_line_magic('matplotlib', 'inline')
from ggplot import *


# In[ ]:


## Load data into Python

alldata = pd.read_csv('../input/creditcard.csv')


# ## Step 1: Take a peak
# 
# Now take a peak at what's in the data. This including how many rows and columns and what are they. 

# In[ ]:


## What is in the data
print(alldata.columns)
print(alldata.shape)


# In[ ]:


alldata.head()


# ### Take necessary transformations
# 
#  1. Class is our dependent variable. It is coded as 0 and 1. Sometimes, we want it to be coded as Y/N. And other times, we want it to be either numeric or factor data types. 
#  2. Usually when dollar is one of the fields, it is skewed as a lognormal distribution. We can take a log transformation. But when 0 is in the data, we can add 0.5 so that the transformation can be completed. 

# In[ ]:


## Add dummy variable Source 
## And convert known class type variables 

alldata['Source']='Train'
alldata['Class']=alldata['Class'].astype(object)
alldata['ClassInt']=alldata['Class'].astype(int)
alldata['ClassYN']=['Y' if x == 1 else 'N' for x in alldata.Class]
alldata['LogAmt']=np.log(alldata.Amount+0.5)


# In[ ]:


## Numerical and Categorical data types
alldata_dtype=alldata.dtypes
display_nvar = len(alldata.columns)
alldata_dtype_dict = alldata_dtype.to_dict()
alldata.dtypes.value_counts()


# ## Step 2: Data Visualization
# 
# ### Variable Description
# 
# I wrote this function with intension to compare train/test data and check if some variable is illy behaved. It is modified a little to fit this dataset to compared between normal/fraud subset. 
# 
# It can be applied to both numeric and object data types:
# 
#  1. When the data type is object, it will output the value count of each categories
#  2. When the data type is numeric, it will output the quantiles
#  3. It also seeks any missing values in the dataset

# In[ ]:


def var_desc(dt):
    print('--------------------------------------------')
    for c in alldata.columns:
        if alldata[c].dtype==dt:
            t1 = alldata[alldata.Class==0][c]
            t2 = alldata[alldata.Class==1][c]
            if dt=="object":
                f1 = t1[pd.isnull(t1)==False].value_counts()
                f2 = t2[pd.isnull(t2)==False].value_counts()
            else:
                f1 = t1[pd.isnull(t1)==False].describe()
                f2 = t2[pd.isnull(t2)==False].describe()
            m1 = t1.isnull().value_counts()
            m2 = t2.isnull().value_counts()
            f = pd.concat([f1, f2], axis=1)
            m = pd.concat([m1, m2], axis=1)
            f.columns=['NoFraud','Fraud']
            m.columns=['NoFraud','Fraud']
            print(dt+' - '+c)
            print('UniqValue - ',len(t1.value_counts()),len(t2.value_counts()))
            print(f.sort_values(by='NoFraud',ascending=False))
            print()

            m_print=m[m.index==True]
            if len(m_print)>0:
                print('missing - '+c)
                print(m_print)
            else:
                print('NO Missing values - '+c)
            if dt!="object":
                if len(t1.value_counts())<=10:
                    c1 = t1.value_counts()
                    c2 = t2.value_counts()
                    c = pd.concat([c1, c2], axis=1)
                    f.columns=['NoFraud','Fraud']
                    print(c)
            print('--------------------------------------------')


# In[ ]:


var_desc('int64')


# In[ ]:


var_desc('float64')


# ### Correlation
# 
# Correlation is useful to find peers of input field so we are aware when building models, either to transform them (principal component) or remove one of the two. 
# 
# In this particular data, it is told that all the V-variables are already principal components. So correlation is not useful to inspect the data. It can be verified below to see correlation coefficient of 0 for those V-variables. 
# 
# But one thing we can do is to find some correlation between V-variables and Class. Recall now that coding Class into a integer data type would be useful. 

# In[ ]:


# Top 10 correlated variables
corrmat = alldata.corr()
k = 8 #number of variables for heatmap
cols = corrmat.nlargest(k, 'ClassInt')['ClassInt'].index
cm = np.corrcoef(alldata[cols].values.T)
f, ax = plt.subplots(figsize=(8, 8))
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()


# ### Distribution
# 
# This is my favorite plot to inspect the data and it always gives hints on what are the important variables in your model. 
# 
# Violin plot with split between Fraud and Normal data will clear show some distinctions of V-variable distributions, and these V-variables are the keys to classify Fraud records. 

# In[ ]:


## Violin plot of the same numeric variables

dt = 'float64'
sel_col = alldata.columns[alldata.dtypes==dt]

plt.figure(figsize=(12,len(sel_col)*4))
gs = gridspec.GridSpec(len(sel_col),1)
for i, cn in enumerate(alldata[sel_col]):
    ax = plt.subplot(gs[i])
    data_1  = pd.concat([alldata[cn], alldata.ClassYN], axis=1)
    data_2  = pd.melt(data_1,id_vars=cn)
    sns.violinplot( x=cn, y='variable', hue="value"
                   ,data=data_2, palette="Set2", split=True
                   ,inner="quartile")
    ax.set_xlabel('')
    ax.set_title('Violin plot of : ' + str(cn))
plt.show()

    


# ## Step 3: Feature Engineering
# 
# Now with all the inspection we've done. We can help the *machine* to create some variables to predict the outcome. Feature engineering is to make additional variables as input features. I usually take the following steps, 
# 
#  1. Covert numeric variable to factors when there are only a few levels for the numeric values;
#  2. Transform skewed variable, for example, we already did for Amount 
#  3. Treat extremely small categories: usually we can merge them, or re-code them.. We don't have to worry it in this problem as there are no categorical variables
#  4. Treat missing data: this can be a big issue for some problems. We can randomly assign a value, impute, assign an average, or create a dummy variable for those missing records. In this problem, we don't have to worry as there are no missing values. 

# In[ ]:


## Treating skewed continuous data - transformation
## already did it


# ## Step 4: Prepare train, validation, test dataset
# 
#  1. Remove unnecessary fields
#  2. Normalize numeric fields
#  3. Think about splitting, how to split between train/test, is ensemble/stacking needed? How to split between stage 1, 2, and 3 stacking?

# In[ ]:


## Remove unnessary columns
list_col_rm = ['Amount','Class','Source','ClassYN']
list_col_keep = alldata.columns.difference(list_col_rm)
print(list_col_keep)


# In[ ]:


## normalize numeric variables
##
excl_cols = ['ClassInt']
alldata_dtype_dict = alldata.dtypes.to_dict()
for c in alldata.columns:
    if c in list_col_keep and c not in excl_cols and alldata_dtype_dict[c]!='object':
        print('----------------------')
        print(c , alldata_dtype_dict[c])
        alldata[c] = (alldata[c]-alldata[c].mean())/(alldata[c].std())
print()
print(alldata.head())


# In[ ]:


## Data Sampling, we do a 80/20 split on train/test.. 
## will talk about stacking later on. 
trainY = alldata[alldata.Class==1].sample(frac=0.8)
trainN = alldata[alldata.Class==0].sample(frac=0.8)
train = pd.concat([trainY, trainN], axis = 0)
test  = alldata.loc[~alldata.index.isin(train.index)]
print(train.shape)
print(test.shape)


# In[ ]:


## Save processed data
## so I can download into a new notebook to build models
import pickle
file_obj = open('./data.p', 'wb') 
pickle.dump([train, test, list_col_keep], file_obj) 
file_obj.close()


# ### I will start a new notebook to build models 

# In[ ]:




