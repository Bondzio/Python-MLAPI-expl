#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
import os
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

#from subprocess import check_output
#print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df_train = pd.read_csv("../input/train_users_2.csv")
#df_train.head(n=5)
df_train.sample(n=5)


# In[ ]:


df_test = pd.read_csv("../input/test_users.csv")
df_test.sample(n=5)


# In[ ]:


df_all = pd.concat((df_train, df_test), axis = 0, ignore_index = True) #nhap chung 2 bo du lieu
df_all.head(n=5)


# In[ ]:


df_all.drop('date_first_booking', axis=1, inplace = True)


# In[ ]:


df_all.sample(n=5)


# In[ ]:


df_all['date_account_created'] = pd.to_datetime(df_all['date_account_created'], format='%Y-%m-%d')
df_all.sample(n=5)


# In[ ]:


df_all['timestamp_first_active'] = pd.to_datetime(df_all['timestamp_first_active'], format='%Y%m%d%H%M%S')
df_all.sample(n=5)


# In[ ]:


#function de lay tuoi trong khoang tu 15 toi 90 tuoi, ngoai khoang do dua ve NaN
def remove_age_outliers(x, min_value = 15, max_value = 90):
    if np.logical_or(x <= min_value, x >= max_value):
        return np.nan
    else:
        return x   


# In[ ]:


#apply function tren df

df_all['age'] = df_all['age'].apply(lambda x: remove_age_outliers(x) if (not np.isnan(x)) else x)
df_all['age'].fillna(-1, inplace = True)
df_all['age'].sample(n = 5)


# In[ ]:


#age dang o float, chuyen qua int
df_all.age = df_all.age.astype(int)
df_all.sample(n=5)


# In[ ]:


def check_NaN_Values_in_df(df):
    for col in df:
        nan_count = df[col].isnull().sum()
        
        if nan_count != 0:
            print (col + " =>" + str(nan_count) + " NaN Values")


# In[ ]:


check_NaN_Values_in_df(df_all)


# In[ ]:


df_all['first_affiliate_tracked'].fillna(-1,  inplace = True)
check_NaN_Values_in_df(df_all)


# In[ ]:


df_all.drop('timestamp_first_active', axis=1, inplace =  True)
df_all.sample(n=5)


# In[ ]:


df_all.drop('language', axis=1, inplace=True)


# In[ ]:


df_all = df_all[df_all['date_account_created'] > '2013-02-01']
df_all.sample(n=5)


# In[ ]:


if not os.path.exists("output"):
    os.makedirs("output")

df_all.to_csv("output/cleaned.csv", sep=",", index = False)

