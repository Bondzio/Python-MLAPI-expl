#!/usr/bin/env python
# coding: utf-8

# **First Real Competition**
# This is my first real competition that I will be entering and working on. I've worked on the Titanic and the Housing competitions in the past. I'm new both to programming and data science, but I figure the best way to learn is to just do it. I'm not expecting to win, but being in a competition with a firm deadline will provide more impetus to me to learn. I'd like to give a shout out to Will Koerhsen for his kernel: https://www.kaggle.com/willkoehrsen/start-here-a-gentle-introduction. I modified his code and have been using it to learn on my own here.
# 
# 
# 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from scipy import stats
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Imputer
import warnings
from sklearn.decomposition import PCA
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


train_data = pd.read_csv("../input/application_train.csv")
test_data = pd.read_csv("../input/application_test.csv")
train_data.columns


# In[ ]:


print('Training data shape: ', train_data.shape)
train_data.head()


# In[ ]:


train_data['TARGET'].value_counts()


# In[ ]:


train_data['TARGET'].astype(int).plot.hist();


# In[ ]:


# Function to calculate missing values by column# Funct 
def missing_values_table(df):
        # Total missing values
        mis_val = df.isnull().sum()
        
        # Percentage of missing values
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        
        # Make a table with the results
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        
        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        
        # Sort the table by percentage of missing descending
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        
        # Print some summary information
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        
        # Return the dataframe with missing information
        return mis_val_table_ren_columns


# In[ ]:


missing_values_table(train_data)


# In[ ]:


# Create a label encoder object
le = LabelEncoder()
le_count = 0

# Iterate through the columns
for col in train_data:
    if train_data[col].dtype == 'object':
        # If 2 or fewer unique categories
        if len(list(train_data[col].unique())) <= 2:
            # Train on the training data
            le.fit(train_data[col])
            # Transform both training and testing data
            train_data[col] = le.transform(train_data[col])
            test_data[col] = le.transform(test_data[col])
            
            # Keep track of how many columns were label encoded
            le_count += 1
            
print('%d columns were label encoded.' % le_count)


# In[ ]:


# one-hot encoding of categorical variables
train_data = pd.get_dummies(train_data)
test_data = pd.get_dummies(test_data)

print('Training Features shape: ', train_data.shape)
print('Testing Features shape: ', test_data.shape)


# In[ ]:


train_labels = train_data['TARGET']

# Align the training and testing data, keep only columns present in both dataframes
train_data, test_data = train_data.align(test_data, join = 'inner', axis = 1)

# Add the target back in
train_data['TARGET'] = train_labels

print('Training Features shape: ', train_data.shape)
print('Testing Features shape: ', test_data.shape)


# In the Gentle Introduction, at this point, Will went back to his EDA without any dimensionality reduction. What follows is my attempt at dimensionality reduction before proceeding.

# In[ ]:


# Make an instance of the Model
pca = PCA(.95)


# In[ ]:


pca.fit(train_data)


# In[ ]:




