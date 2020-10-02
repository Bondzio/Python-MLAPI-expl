#!/usr/bin/env python
# coding: utf-8

# <h1>Data Analysis of Google App's Rating</h1>

# In[ ]:


import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


df_apps=pd.read_csv("../input/google-play-store-apps/googleplaystore.csv")
df_reviews=pd.read_csv("../input/google-play-store-apps/googleplaystore_user_reviews.csv")


# In[ ]:


df_apps.head()


# In[ ]:


df_apps.columns=["app","category","rating","reviews","size","installs","type","price","content_rating","genres","last_updated","current_ver","android_ver"]


# In[ ]:


df_apps.drop(["size","last_updated","current_ver","android_ver"],axis=1,inplace=True)


# In[ ]:


df_apps.isnull().sum()


# In[ ]:


df_apps[df_apps.rating >5]


# In[ ]:


df_apps.drop([10472],inplace=True)


# In[ ]:


def impute_median(series):
    return series.fillna(series.median())


# In[ ]:


df_apps.rating =df_apps["rating"].transform(impute_median)


# In[ ]:


print(df_apps["type"].mode())


# In[ ]:


df_apps["type"].fillna(str(df_apps["type"].mode().values[0]),inplace=True)


# In[ ]:


df_apps["price"]=df_apps["price"].apply(lambda x:str(x).replace('$','')if '$' in str(x) else str(x))
df_apps["price"]=df_apps["price"].apply(lambda x: float(x))
df_apps["reviews"]=pd.to_numeric(df_apps["reviews"],errors="coerce")


# In[ ]:


df_apps["installs"]=df_apps["installs"].apply(lambda x: str(x).replace('+','') if '+' in str(x) else str(x))
df_apps["installs"]=df_apps["installs"].apply(lambda x: str(x).replace(',','') if ',' in str(x) else str(x))
df_apps["installs"]=df_apps["installs"].apply(lambda x: float(x))


# In[ ]:


df_apps.head()


# In[ ]:


df_apps.tail()


# In[ ]:


df_apps.isnull().sum()


# In[ ]:


df_apps.content_rating.unique()


# In[ ]:


df_apps['content_rating'] = df_apps['content_rating'].map({'Everyone': 'child','Teen':'everyone','Everyone 10+':'teenager','Mature 17+':'adults','Adults only 18+':'adults','Unrated':'unrated'})


# In[ ]:


df_apps.shape


# In[ ]:


df_apps.info()


# In[ ]:


df_apps.describe()


# In[ ]:


df_apps = df_apps.sort_values(by=["installs"], ascending=False)
df_apps['rank']=tuple(zip(df_apps.installs))
df_apps['rank']=df_apps.groupby('installs',sort=False)['rank'].apply(lambda x : pd.Series(pd.factorize(x)[0])).values
df_apps.head()


# In[ ]:


df_apps.drop(["rank"],axis=1,inplace=True)


# In[ ]:


df_apps.reset_index(inplace=True,drop=True)
df_apps.head(10)


# In[ ]:


df_apps[df_apps.content_rating=='unrated']


# In[ ]:


#create a new dataframe
data=pd.DataFrame(df_apps.iloc[:,3:5])
data.head(3)


# In[ ]:


labels = df_apps.content_rating.value_counts().index
colors = ['pink','r','g','orange','black']
explode = [0,0,0,0,0]
sizes = df_apps.content_rating.value_counts().values

# visual 
plt.figure(0,figsize = (6,7))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Apps According to Content Rating',color = 'blue',fontsize = 15)
plt.show()


# In[ ]:


labels = df_apps.type.value_counts().index
colors = ["g","r"]
explode = [0,0]
sizes = df_apps.type.value_counts().values

# visual 
plt.figure(0,figsize = (6,7))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Apps According to Type',color = 'blue',fontsize = 15)
plt.show()


# In[ ]:


df_apps.head(2)


# In[ ]:


xcat = df_apps.app[df_apps.category == 'SOCIAL']
plt.subplots(figsize=(10,10))
wordcloud = WordCloud(
                          background_color='white',
                          width=512,
                          height=384
                         ).generate(" ".join(xcat))
plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('graph.png')

plt.show()


# In[ ]:


labels = df_apps.category.value_counts().index
colors = ["black","gray","silver","whitesmoke","rosybrown",
          "firebrick","red","darksalmon","sienna","sandybrown",
          "bisque","tan","moccasin","floralwhite","gold",
          "darkkhaki","olivedrab","palegreen","lightseagreen","darkcyan",
          "deepskyblue","lime","tomato","mediumpurple","maroon",
          "coral","olive","yellowgreen","violet","crimson",
          "pink","seashell","azure"]
explode = [0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0,0,
           0,0,0]
sizes = df_apps.category.value_counts().values

# visual 
plt.figure(0,figsize = (18,18))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Apps According to Category',color = 'blue',fontsize = 15)
plt.show()

