#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


df_meals = pd.read_csv('/kaggle/input/nys-meals-served-by-the-office-for-the-aging/meals-served-by-the-office-for-the-aging-beginning-1974.csv')
df_meals.info()


# In[ ]:


get_ipython().system('pip install cufflinks')
import cufflinks as cf
cf.go_offline()


# In[ ]:


_=pd.pivot_table(df_meals, index='Year', values='Meal Units Served', 
               aggfunc=np.sum).iplot(kind='barh', dimensions=(800,500), title='Total Meal Units Served')


# In[ ]:


_=pd.pivot_table(df_meals, index='Meal Type', values='Meal Units Served', 
               aggfunc=np.sum).iplot(kind='bar', dimensions=(500,500), title='Total Meal Units Served')


# In[ ]:


pd.pivot_table(df_meals, index='Year',columns='Meal Type', values='Meal Units Served', 
               aggfunc=np.sum).iplot()


# In[ ]:


df_meals.groupby(by=['County Name']).agg({'Meal Units Served':sum}).nlargest(5, columns='Meal Units Served')


# In[ ]:


df_meals.groupby(by=['Year','County Name']).agg({'Meal Units Served':sum}).nlargest(5, columns='Meal Units Served')


# In[ ]:


df_meals.groupby(by=['Year','County Name', 'Meal Type']).agg({'Meal Units Served':sum}).nlargest(5, columns='Meal Units Served')


# In[ ]:


#https://markhneedham.com/blog/2015/01/25/python-find-the-highest-value-in-a-group/
df_meals.groupby(by=['County Name']).max()['Meal Units Served']


# In[ ]:


#https://markhneedham.com/blog/2015/01/25/python-find-the-highest-value-in-a-group/
df_meals.groupby(by=['Year']).max()['Meal Units Served']


# In[ ]:


#https://markhneedham.com/blog/2015/01/25/python-find-the-highest-value-in-a-group/
df_meals.groupby(by=['Meal Type']).max()['Meal Units Served']

