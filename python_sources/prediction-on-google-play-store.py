#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


g_data=pd.read_csv('/kaggle/input/google-play-store-apps/googleplaystore.csv')


# In[ ]:


g_data.head()


# In[ ]:


g_data.shape


# In[ ]:


g_data.describe()


# In[ ]:


g_data.boxplot()


# In[ ]:


g_data.hist()


# In[ ]:


g_data.info()  #inspecting the columns having missing values


# In[ ]:


g_data.isnull()


# In[ ]:


g_data.isnull().sum() #counts the no. of missing values in each column


# In[ ]:


g_data.columns


# In[ ]:


g_data[g_data.Rating > 5]  #getting the outlier visualised from boxplot


# In[ ]:


g_data.drop([10472],inplace=True) #removing the row that holds outlier


# In[ ]:


g_data[10470:10479]


# In[ ]:


g_data.boxplot()


# In[ ]:


g_data.hist()


# In[ ]:


def impute_median(series):
    return series.fillna(series.median()) 


# In[ ]:


g_data.Rating=g_data['Rating'].transform(impute_median) #fills missing numerical values with median


# In[ ]:


g_data.isnull().sum()


# In[ ]:


g_data['Type'].fillna(str(g_data['Type'].mode().values[0]),inplace=True)
g_data['Current Ver'].fillna(str(g_data['Current Ver'].mode().values[0]),inplace=True)
g_data['Android Ver'].fillna(str(g_data['Android Ver'].mode().values[0]),inplace=True) #fills missing values in categorical data


# In[ ]:


g_data.isnull().sum() 


# In[ ]:


g_data['Price']=g_data['Price'].apply(lambda x: str(x).replace('$','')if '$'in str(x)else str(x))
g_data['Price']=g_data['Price'].apply(lambda x: float(x))
g_data['Reviews']=pd.to_numeric(g_data['Reviews'],errors='coerce')


# In[ ]:


g_data['Installs']=g_data['Installs'].apply(lambda x: str(x).replace('+','')if '+'in str(x)else str(x))
g_data['Installs']=g_data['Installs'].apply(lambda x: str(x).replace(',','')if ','in str(x)else str(x))
g_data['Installs']=g_data['Installs'].apply(lambda x: float(x))


# In[ ]:


g_data.head(10)


# In[ ]:


g_data.describe()


# In[ ]:


grp=g_data.groupby('Category')
x=grp['Rating'].agg(np.mean)
y=grp['Price'].agg(np.sum)
z=grp['Reviews'].agg(np.mean)
print(x)
print(y)
print(z)


# In[ ]:


plt.plot(y,'ro')


# In[ ]:


plt.figure(figsize=(20,7))
plt.plot(x,'ro',color='b')
plt.xticks(rotation=90)
plt.title('Categorywise Rating')
plt.xlabel('Categories --->')
plt.ylabel('Rating --->')
plt.show()


# In[ ]:


plt.figure(figsize=(20,7))
plt.plot(y,'ro',color='g')
plt.xticks(rotation=90)
plt.title('Categorywise Pricing')
plt.xlabel('Categories --->')
plt.ylabel('Pricing --->')
plt.show()


# In[ ]:


plt.figure(figsize=(20,7))
plt.plot(y,'r--',color='g')
plt.xticks(rotation=90)
plt.title('Categorywise Pricing')
plt.xlabel('Categories --->')
plt.ylabel('Pricing --->')
plt.show()


# In[ ]:


plt.figure(figsize=(20,7))
plt.plot(z,'ro',color='cyan')
plt.xticks(rotation=90)
plt.title('Categorywise Reviews')
plt.xlabel('Categories --->')
plt.ylabel('Reviews --->')
plt.show()


# In[ ]:


plt.figure(figsize=(20,7))
plt.plot(z,'g-',color='cyan')
plt.xticks(rotation=90)
plt.title('Categorywise Reviews')
plt.xlabel('Categories --->')
plt.ylabel('Reviews --->')
plt.show()


# In[ ]:


plt.figure(figsize=(20,7))
plt.plot(z,'bs',color='cyan')
plt.xticks(rotation=90)
plt.title('Categorywise Reviews')
plt.xlabel('Categories --->')
plt.ylabel('Reviews --->')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




