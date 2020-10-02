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


# read db

# In[ ]:


df = pd.read_csv('../input/saudi-arabia-bookingcom/project3_df1.csv')
df 


# show columns

# In[ ]:


df.columns


# show dtypes include ='object'

# In[ ]:


df.select_dtypes(include='object').columns


# In[ ]:


df.isnull().any()


# In[ ]:


df.City


# In[ ]:


df.City.isnull()


# In[ ]:


any([True, True, True]), any([True, False, True]), any([False, False, False])


# In[ ]:


all([True, True, True]), all([True, False, True]), all([False, False, False])


# In[ ]:


df.isnull().sum()


# In[ ]:


df.shape


# In[ ]:


for col in df.columns:
    if df[col].isnull().any():
        print(col, df[col].isnull().sum())


# In[ ]:


for col in df.columns:
    if df[col].dtype == 'object':
        print(col)


# In[ ]:


for col in df.columns:
    if df[col].dtype == 'int64' or df[col].dtype == 'float64':
        print(col)


# In[ ]:


# Get list of categorical variables
s = (df.dtypes == 'object')
print(s)
object_cols = list(s[s].index)

print("Categorical variables:")
print(object_cols)


# In[ ]:


df_num = df.select_dtypes(exclude='object')
df_num


# In[ ]:


df_cat = df[object_cols]
df_cat


# In[ ]:


import matplotlib.pyplot as plt # plotting
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()


# In[ ]:


def plotCorrelationMatrix(df, graphWidth):
    filename = df.dataframeName
    df = df.dropna('columns') # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()


# In[ ]:


def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()


# In[ ]:


nRowsRead = 1000 
df1 = pd.read_csv('../input/saudi-arabia-bookingcom/project3_df1.csv', delimiter=',', nrows = nRowsRead)
df1.dataframeName = '../input/saudi-arabia-bookingcom/project3_df1.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


df1.head(5)


# In[ ]:


plotPerColumnDistribution(df, 10, 5)


# In[ ]:


plotCorrelationMatrix(df1, 8)


# In[ ]:


plotScatterMatrix(df1, 18, 10)

