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


# ### Importing Visualization Tools

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# ### Loading Dataset

# In[ ]:


data = pd.read_csv('/kaggle/input/tvmarketing-dataset/tvmarketing.csv')
data.head()


# ### Exploring datasets

# In[ ]:


data.info()


# In[ ]:


print('Total no. of Rows: {}\nTotal no. of columns: {}'.format(data.shape[0],data.shape[1]))


# In[ ]:


data.describe()


# In[ ]:


sns.distplot(data['TV'],bins=30)


# In[ ]:


sns.distplot(data['Sales'])


# In[ ]:


sns.scatterplot(data['TV'],data['Sales']).set_title('TV vs Sales ScatterPlot')


# In[ ]:


x1 = data['TV'] #Independent
y = data['Sales'] #dependent


# In[ ]:


import statsmodels.api as sm

x = sm.add_constant(x1)
result = sm.OLS(y,x).fit()
result.summary()


# * Here Adj. $R^2$ == 0.612
# Hence, our Regression Model explained about **60.0%** variability of the data

# In[ ]:


yhat = 7.0326 + 0.0475*x1
plt.scatter(x1,y)
fig = plt.plot(x1,yhat,c='red',label='Linear Regression')


# ### Predicting the Sales

# In[ ]:


pd.options.display.float_format = '{:.2f}'.format
predictions = pd.DataFrame({'const':[1,1,1,1],'TV':[123,141,256,175]})
predictions['predictions'] = result.predict(predictions)
predictions.drop('const',axis=1)


# In[ ]:




