#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))


# In[ ]:


data = pd.read_csv('../input/Video_Games_Sales_as_at_30_Nov_2016.csv')
data.info()


# In[ ]:


data.head()


# In[ ]:


data[data.isnull().any(axis=1)]

df=data.dropna()


# In[ ]:


v1=df[['Name','Platform','Publisher','Developer','Rating']]


# In[ ]:


df1=df.drop('Name',axis=1)


# In[ ]:


platform_dis_sales=df1.pivot_table(values=['NA_Sales','EU_Sales','JP_Sales','Other_Sales'],
                
                index=['Platform','Year_of_Release'],
                aggfunc=np.sum
               )


# In[ ]:


platform_tol_sales=df1.groupby(['Platform','Year_of_Release'])['Global_Sales'].sum()


# In[ ]:


platform_tol_sales=platform_tol_sales.unstack().T


# In[ ]:


platform_tol_sales.ix[2000:,[ 'PS', 'PS2', 'PS3', 'PS4', 'PSP', 'PSV']].plot()


# In[ ]:


platform_tol_sales.ix[2000:,[ 'Wii', 'WiiU', 'X360', 'XB', 'XOne']].plot()


# In[ ]:


platform_tol_sales.ix[2000:,[ 'PC']].plot()


# the top 10 company of the Game production

# In[ ]:


df_count=df1.groupby(['Publisher'])['Platform'].count()
_df_count=df_count.sort_values(ascending=False).head(10)
_df_count.plot(kind='bar')


# the high avg score company

# In[ ]:


df1['User_Score']=pd.to_numeric(df1['User_Score'])
df1.groupby(['Publisher'])['User_Score'].mean().sort_values(ascending=False).head(10)


# In[ ]:


df1['User_Score']=pd.to_numeric(df1['User_Score'])


# In[ ]:


ww


# In[ ]:




