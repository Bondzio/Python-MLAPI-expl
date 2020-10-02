#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib
from pandas.plotting import scatter_matrix


get_ipython().run_line_magic('matplotlib', 'inline')


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# ## Dataset columns
# * **Rank** - Rank by median earnings (the dataset is ordered by this column).
# * **Major_code** - Major code.
# * **Major** - Major description.
# *     **Major_category** - Category of major.
# *     **Total** - Total number of people with major.
# *     **Sample_size** - Sample size (unweighted) of full-time.
# *     **Men** - Male graduates.
# *     **Women** - Female graduates.
# *     **ShareWomen** - Women as share of total.
# *     **Employed** - Number employed.
# *     **Median** - Median salary of full-time, year-round workers.
# *     **Low_wage_jobs** - Number in low-wage service jobs.
# *     **Full_time** - Number employed 35 hours or more.
# *     **Part_time** - Number employed less than 35 hours.
# 

# In[ ]:


recent_grads = pd.read_csv('/kaggle/input/fivethirtyeight-college-majors-dataset/recent-grads.csv')


# In[ ]:


recent_grads.head()


# In[ ]:


recent_grads.describe()


# ## Dataset cleaning

# In[ ]:


raw_data_count = recent_grads.iloc[:,0].count()
print("Total rows BEFORE dropping NAs: ",raw_data_count)
recent_grads = recent_grads.dropna()
print("Total rows AFTER dropping NAs: ",recent_grads.iloc[:,0].count())


# # Scatter plots
# 

# In[ ]:


ax=recent_grads[recent_grads['Median']<=80000][recent_grads['Sample_size']<=500].plot(x='Sample_size', y='Median', kind='scatter', figsize=(10,7))
ax.set_title('Sample_size vs. Median')


# In[ ]:


ax=recent_grads.plot(x='Sample_size', y='Unemployment_rate', kind='scatter', figsize=(10,7))
ax.set_title('Sample_size vs. Unemployment_rate')


# In[ ]:


ax=recent_grads.plot(x='Full_time', y='Median', kind='scatter', figsize=(10,7))
ax.set_title('Full_time vs. Median')


# In[ ]:


ax=recent_grads.plot(x='ShareWomen', y='Unemployment_rate', kind='scatter', figsize=(10,7))
ax.set_title('ShareWomen vs. Unemployment_rate')


# In[ ]:


ax=recent_grads[recent_grads['Median']<=80000].plot(x='Men', y='Median', kind='scatter', figsize=(10,7))
ax.set_title('Men vs. Median')


# In[ ]:


ax=recent_grads[recent_grads['Median']<=80000][recent_grads['Women']<=180000].plot(x='Women', y='Median', kind='scatter', figsize=(10,7))
ax.set_title('Women vs. Median')


# # Histograms

# In[ ]:


recent_grads['Sample_size'].hist(bins=10, range=(0,1500), figsize=(12,8))


# In[ ]:


recent_grads['Median'].hist(bins=15, range=(23000,75000), figsize=(12,8))


# In[ ]:


recent_grads['Employed'].hist(bins=20, range=(0,150000), figsize=(12,8))


# In[ ]:


recent_grads['Full_time'].hist(bins=15, range=(0,180000), figsize=(12,8))


# In[ ]:


recent_grads['ShareWomen'].hist(bins=18, range=(0,1), figsize=(12,8))


# In[ ]:


recent_grads['Unemployment_rate'].hist(bins=22, range=(0,0.2), figsize=(12,8))


# In[ ]:


recent_grads['Men'].hist(bins=12, range=(0,140000), figsize=(12,8))


# In[ ]:


recent_grads['Women'].hist(bins=12, range=(0,140000), figsize=(12,8))


# # Scatter matrix plots

# In[ ]:


from pandas.plotting import scatter_matrix

no_outliers_for_scatter_matrix = recent_grads[recent_grads['Median']<=85000][recent_grads['Sample_size']<=3000]

scatter_matrix(no_outliers_for_scatter_matrix[['Sample_size', 'Median']], figsize=(20,20))


# In[ ]:


no_outliers_for_scatter_matrix = recent_grads[recent_grads['Median']<=85000][recent_grads['Sample_size']<=3000]

scatter_matrix(no_outliers_for_scatter_matrix[['Sample_size', 'Median', 'Unemployment_rate']], figsize=(20,20))


# # Barplots

# In[ ]:


recent_grads[:10].plot.bar(x='Major', y='ShareWomen', figsize=(12,8))


# In[ ]:


recent_grads[:10].plot.bar(x='Major', y='Unemployment_rate', figsize=(12,8))


# In[ ]:




