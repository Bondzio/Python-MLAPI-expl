#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing the fundamental libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv('../input/17k-apple-app-store-strategy-games/appstore_games.csv')


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


df.describe()


# In[ ]:


plt.figure(figsize=(12,6))
sns.heatmap(df.isnull(),cbar=False,yticklabels=False,cmap='viridis')


# In[ ]:


df.drop(['URL','ID'],axis=1,inplace=True)


# In[ ]:


df.head()


# **Exploratory data analysis of single varibales**

# In[ ]:


plt.figure(figsize=(12,6))
ax = sns.countplot(data=df,x='Average User Rating')
ax.set_xlabel('Average user rating')
ax.set_ylabel('Count')
ax.plot()


# **The most frequent rating is 4.5**

# In[ ]:


plt.rcParams['figure.figsize'] = (18, 10)
ax= sns.kdeplot(df['User Rating Count'],alpha=0.4,shade=True)
ax.set_xlabel('User Rating count')
ax.set_ylabel('Count')
ax.plot()


# In[ ]:



plt.rcParams['figure.figsize'] = (18, 10)
ax = sns.kdeplot(df['Price'], shade = True, linewidth = 5, bw=1.5,color = 'm')
ax.set_ylabel('Count', fontsize = 20)
ax.set_xlabel('Price', fontsize = 20)
plt.show()


# In[ ]:


df['Size2'] = round(df['Size']/1000000,1)


# In[ ]:


ax = sns.kdeplot(df['Size2'],shade=True,linewidth=5)
ax.set_xlabel('Size')
ax.set_ylabel('count')
plt.show()


# **Most of the app size is between 0 to 500Mb**

# In[ ]:


df['Developer'].value_counts()[:20].plot(kind='bar')


# **Bivariate analysis**

# In[ ]:


ax= sns.regplot(y='Average User Rating',x='Price',data= df)
ax.set_ylabel('Average user rating')
ax.set_xlabel('Price')
plt.show()


# In[ ]:


ax = sns.regplot(x='Size',y='Average User Rating',data = df)
ax.set_xlabel('Size')
ax.set_ylabel('Average User Rating')
plt.show()


# In[ ]:


g = sns.FacetGrid(df , col='Age Rating', height=6)
g.map(sns.countplot,'Average User Rating')


# In[ ]:


paid = df[df['Price']>0]
free = df[df['Price']==0]
fig, ax = plt.subplots(1,2,figsize=(16,8))
sns.countplot(data=paid, y='Average User Rating',ax=ax[0],palette='plasma')
ax[0].set_xlabel('Paid')
ax[0].set_ylabel('Count')

sns.countplot(data=free, y= 'Average User Rating',ax=ax[1],palette='coolwarm')
ax[1].set_xlabel('Free')
ax[1].set_ylabel('Count')


# In[ ]:


plt.rcParams['figure.figsize'] = (18,10)
sns.heatmap(df.corr(),annot=True,cmap='plasma')


# In[ ]:


review = df.sort_values(by='User Rating Count', ascending=False)[['Name', 'Price', 'Average User Rating', 'Size', 'User Rating Count', 'Icon URL']].head(10)
review.iloc[:, 0:-1]


# **Most reviewed Games are**
# * Clash of Clans
# * Clash royale
# * PUBG  mobile

# # Overall best games are:
# 

# In[ ]:


overall = df.sort_values(by=['Average User Rating', 'User Rating Count'], ascending=False)[['Name','Average User Rating','Size','User Rating Count']]
overall.iloc[:, 0:-1].head(10)


# **Data Cleaning and Transformation**

# In[ ]:


df.drop(['Subtitle','Icon URL','Description'],axis=1,inplace=True)


# In[ ]:


df['Age Rating'] = df['Age Rating'].str.replace('+','')


# In[ ]:


df['Age Rating']=pd.to_numeric(df['Age Rating'])


# In[ ]:


df['Size']=df['Size']/1024/1024
df['Size']= pd.qcut(df['Size'],q=5,labels=False)


# In[ ]:


df['Release_Date'] = pd.to_datetime(df['Original Release Date'], format ='%d/%m/%Y')
df['Current Version Release Date'] = pd.to_datetime(df['Current Version Release Date'], format ='%d/%m/%Y')
df['Release_Year'] = df['Release_Date'].dt.year
df['Release_Month'] = df['Release_Date'].dt.month
df = df.drop(['Original Release Date'], axis = 1)


# In[ ]:


df['Primary Genre'].value_counts()


# In[ ]:


genres = df['Genres'].str.split(',')


# In[ ]:


genres


# In[ ]:




