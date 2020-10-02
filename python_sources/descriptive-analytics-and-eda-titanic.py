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


# # Import the Libraries

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set_style('whitegrid')
import missingno as msno


# # Import the Data

# In[ ]:


train  = pd.read_csv('/kaggle/input/titanic/train.csv')
# tt = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/test.csv')


# # Lowercase the columns of the data 

# In[ ]:


train.columns = map(str.lower, train.columns)


# # 1. Descriptive Analysis

# ## Shape and size

# In[ ]:


train.shape


# In[ ]:


train.size


# ## 1. 1. Lets look at the data

# In[ ]:


train.head()


# ## 1. 2. **Columns of the data**

# In[ ]:


train.columns


# ## 1. 3. Info gives information about the types of data present in our data set

# In[ ]:


train.info()


# ## 1. 4. Describe your Data
Describe gives us the information about the mean, Median, Standard Deviation, inter-quartile range (Measure of Variability) and Minimum and Maximum values in each column. 
PS - Describe only gives information about the numerical data.
# In[ ]:


train.describe()


# ## 1.5. Spread of Data - variance

# In[ ]:


col = train.columns
for i in col:
    skewness = np.array(train[col].skew())
    kurtosis = np.array(train[col].kurt())
    mean = np.array(train[col].mean())
    median = np.array(train[col].median())
    variance = np.array(train[col].var())
    
    data_frame = pd.DataFrame({'skewness':skewness,
                               'kurtosis':kurtosis, 
                               'Mean':mean,
                               'Median':median, 
                               'variance':variance},
                              
                              index=num_features,
                              columns={'skewness',
                                       'kurtosis',
                                       'Mean',
                                       'Median',
                                       'variance'})
print(data_frame)


# In[ ]:


num_features = ['passengerid', 'survived', 'pclass', 'age', 'sibsp', 'parch', 'fare' ]
sns.pairplot(train[num_features])


#  ## Modality - Measure of number of peaks

# # Exploratory Data Analysis

# ## Quick Summary of the Categorical Features

# In[ ]:



def categorical_feature_summarized(dataframe, x=None, y=None, hue=None, palette='Set1', verbose=True):
    '''
    
    helper function that gives a quick summary of a given column of categorical data
    
    Arguments
    =============
    dataframe: pandas df
    x: str, horizontal axis to plot the label of categorical data
    y: str, vertical xis to plot hte label of the categorical data
    hue: str, if you want to comparer it to any other variable
    palette: array-like, color of the graph/plot
    
    
    Returns
    ==============
    Quick summary of the categorical data
    
    
    '''
    
    if x==None:
        column_interested = y
        
    else:
        column_interested = x
    series = dataframe[column_interested]
    print(series.describe())
    print('mode', series.mode())
    
    if verbose:
        print('='*80)
        print(series.value_counts())
        
        
    sns.countplot(x=x, y=y, hue=hue, data=dataframe, palette = palette)
    plt.show()
    
    '''
    
    categorical_summarized does is it takes in a dataframe, together with some input arguments and 
    outputs the following:
        1. The count, mean, std, min, max, and quartiles for numerical data or
        2. the count, unique, top class, and frequency of the top class for non-numerical data.
        3. Class frequencies of the interested column, if verbose is set to 'True'
        4. Bar graph of the count of each class of the interested column
    
    '''


# In[ ]:


for i in train.columns:
    categorical_feature_summarized(train, x=i)


# ## Correlation

# In[ ]:


train.corr()['survived'].sort_values(ascending=False)


# Passenger Class and Fare Play a vital role in the survival of the passenger

# ## Heatmap

# In[ ]:


#Heatmap
def heatmap(df):
    
    '''
    this function takes data frame a input and returns the
    heatmap as output.
    
    Arguments
    ====================
    df : Dataframe or Series 
    
    
    Returns
    ===========
    heatmap
    '''
    corr = df.corr()   #create a correlation df
    fig,ax = plt.subplots(figsize = (10,10))   # create a blank canvas
    colormap = sns.diverging_palette(220,10, as_cmap=True)   #Generate colormap
    sns.heatmap(corr, cmap=colormap, annot=True, fmt='.2f')   #generate heatmap with annot(display value) and place floats in map
#    plt.xticks(range(len(corr.columns)), corr.columns);   #apply  xticks(labels of features)
#    plt.yticks(range(len(corr.columns)), corr.columns)   #apply yticks (labels of features)
    plt.show()
    


# In[ ]:


heatmap(train)


# ## Missing Values

# In[ ]:


train.isna().sum()


# Only Age, Cabin and Embarked have missing values

# In[ ]:


print('total missing values: ', train.isna().sum().sum(), 'out of', train.size, 'total entries') 


# In[ ]:


msno.heatmap(train)


# In[ ]:




