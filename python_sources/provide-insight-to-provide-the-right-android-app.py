#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import pylab as pl
from datetime import datetime

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# Read the data set

# In[ ]:


df = pd.read_csv('../input/googleplaystore.csv')

pd.options.display.max_rows = 50
pd.options.display.max_columns = 10

df.head()

df.describe()


# Clean the dataset.

# In[ ]:


print('Total number of apps: ', len(df))
print(df.isnull().sum())

df.drop_duplicates(subset='App', inplace=True)
df = df[df.Rating.notnull()]
df = df[df['Android Ver'].notnull()]
df = df[df['Current Ver'].notnull()]

df.drop_duplicates(subset='App', inplace=True)
print('Total number of apps: ', len(df))
print(df.isnull().sum())


# Show the variables in the dataframe.

# In[ ]:


df['Reviews'] = df.Reviews.astype(int) 

df['Price'] = df.Price.apply(lambda x: x.replace('$', '') if '$' in x else x) # contains dollar sign. Should be transormed more.
df['Price'] = df.Price.astype(float) 

# chaining example in transformation with lambda
# log added for scaling the feature
df['Installs'] = df.Installs.apply(lambda x: np.log(int(x.replace('+', '').replace(',', ''))))

# transformation of size, including log for scaling the feature
df['Size'] = df['Size'].apply(lambda x: str(x).replace('Varies with device', 'NaN') if 'Varies with device' in str(x) else x)
df['Size'] = df['Size'].apply(lambda x: str(x).replace('M', '') if 'M' in str(x) else x)
df['Size'] = df['Size'].apply(lambda x: str(x).replace(',', '') if ',' in str(x) else x)
df['Size'] = df['Size'].apply(lambda x: float(str(x).replace('k', '')) / 1000 if 'k' in str(x) else x)
df['Size'] = df.Size.astype(float) 
df['Size'] = np.log(df['Size'])

# transformation to date format
df['Last Updated'] = df['Last Updated'].apply(lambda x: pd.to_datetime(x) if pd.notnull(x) else '')

df.info(verbose=True)
df.describe()


# Start to visualize.

# In[ ]:


pl.figure(figsize=(12,5))
pl.title("Distribution rating")
ax = sns.distplot(df["Rating"], color = 'r')


# And now the scatter plot

# In[ ]:


pl.figure(figsize = (12,10))

pl.scatter(df["Rating"],
            df["Reviews"],
            linewidths=1, c = "b")
pl.xlabel("Rating")
pl.ylabel("Reviews")
pl.title("scatter rating and reviews")
pl.show()


# In[ ]:


pl.figure(figsize = (12,10))

pl.scatter(df["Installs"],
            df["Rating"],s = 5,
            linewidths=1, c = "b")
pl.xlabel("Installs")
pl.ylabel("Rating")
pl.title("scatter installs and rating")
pl.show()


# In[ ]:


pl.figure(figsize = (12,10))

pl.scatter(df["Installs"],
            df["Price"],s = 5,
            linewidths=1, c = "b")
pl.xlabel("Installs")
pl.ylabel("Price")
pl.title("scatter installs and price")
pl.show()


# In[ ]:


pl.figure(figsize = (12,10))

pl.scatter(df["Installs"],
            df["Size"],s = 5,
            linewidths=1, c = "b")
pl.xlabel("Installs")
pl.ylabel("Size")
pl.title("scatter installs and size")
pl.show()


# And now the pairplot for the same variables: rating, reviews, price, size and iinstalls:

# In[ ]:


#sns.pairplot(df, vars["Rating", "Reviews", "Price", "Size", "Installs"])
#df = df[(df.installs !=0) & (df.reviews!=0)].dropna()
#df = df['Installs'][df.Installs!=0].dropna()
impute_value = df['Installs'].median
#df = df['Installs'][df.Installs!=0].fillna(impute_value)
#df = df['Reviews'][df.Reviews!=0].dropna()
df = df[(df.Installs !=0) & (df.Reviews!=0)].dropna()

cols = ["Rating", "Reviews", "Price", "Size", "Installs", "Type"]
#cols = ["Rating", "Price", "Size", "Installs"]

dfcols = df[cols]
sns.pairplot(dfcols, hue="Type" )


# And the boxplot

# In[ ]:


sns.boxplot(y="Rating", x="Installs", data=df, palette = 'pink')


# And the correlation heatmap:

# In[ ]:


#cm = np.corrcoef(df[cols].values.T)
#sns.set(font_scale = 1.7)
#hm = sns.heatmap(cm,cbar = True, annot = True,square = True, fmt = '.2f', annot_kws = {'size':15}, yticklabels = cols, xticklabels = cols)

# create correlation matrix
corr = df.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# draw heatmap
sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, mask=mask)


# Group by category and show in historgram.

# In[ ]:


grouped = df.groupby(['Category'])['Installs'].mean()

grouped.plot.bar()

