#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importing the required modules
import numpy as np 
import pandas as pd 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df=pd.read_csv("../input/googleplaystore.csv")
print(df.columns)
print("="*80)
print(df.head())


# In[ ]:


print(df['Category'].unique())
print("="*80)
print(df['Type'].unique())
print("="*80)
print(df['Content Rating'].unique())
print("="*80)
print(df['Genres'].unique())


# **There is one numeric value in Category and also Genre column details seems same to Category**

# In[ ]:


df.drop('Genres',axis=1,inplace=True)
df = df.drop(df[ df['Category'] == '1.9' ].index, axis=0)


# **Deleting duplicate values from 'App' column if any**

# In[ ]:


data=df.drop_duplicates(subset=['App'])
data.info()


# **From above it seems like there are some Null values also in the data**

# In[ ]:


data['Rating'].fillna(0)
data['Content Rating'].fillna(method='ffill')
data['Current Ver'].fillna(1)
data['Android Ver'].fillna(method='bfill')
data['Type'].fillna('Free')
pass


# In[ ]:


#print(df['Type'].unique())
data.info()


# In[ ]:


sns.set_context({"figure.figsize": (20, 5)})
c=sns.countplot(x="Category",data=data, palette = "Set3",order=reversed(data['Category'].value_counts().index))
c.set_xticklabels(c.get_xticklabels(), rotation=-65, ha="left")
c.set_yticklabels(c.get_yticklabels(), rotation=0, ha="right") #just to check
plt.title('Count of app in different category',size = 40)


# **Most of the apps belong to the Category of Family with games being the second.**
# 1.  In the above plotting if you ommit 'reversed' than the plot will be in decresing order and omitting order will result in no sequence.
# 2. You can also change the colour of the plot by changing the values of the palette Set (1 -3) with 1 being dark and 3 being light**
# 3. https://seaborn.pydata.org/generated/seaborn.countplot.html

# In[ ]:


data.groupby('Category').mean()['Rating'].plot("barh",figsize=(10,13),title ="Rating in difft Category");


# **From above it seems the ratings of all the app are near about same only.**
# 
# **Let see which category has got the max and min ratings**

# In[ ]:


#print(data.groupby("Category").mean().max())

sdf=data.groupby("Category").mean()
sdf['Cat']=sdf.index

print("The category which got the Max rating :",sdf['Rating'].idxmax())
print("The category which got the Min rating :",sdf['Rating'].idxmin())

sx=sdf.loc[sdf['Rating'].idxmax()]               #This will retunr entire row of the max value
si=sdf.loc[sdf['Rating'].idxmin()] 

#print(type(sx))                   #Series

print("Mean rating for",sdf['Rating'].idxmax(),"is : ",sx['Rating'])
print("Mean rating for",sdf['Rating'].idxmin(),"is :",si['Rating'])


#df[df['Rating'] == df['Rating'].max()]       #This one will list all rows that have max Rating


#  **DATING category have the least and  EVENTS have the max rating**

# In[ ]:


sns.set_context({"figure.figsize": (20, 5)})
c=sns.countplot(x="Content Rating",hue='Type',data=data, palette = "Set1",order=reversed(data['Content Rating'].value_counts().index))
c.set_xticklabels(c.get_xticklabels(), rotation=0, ha="right")
plt.title('Apps by there content ratings',size = 40)


# **Most of the apps belongs to the categoy of 'Everyone' and are freely avilable **

# In[ ]:


data['Installs']=data['Installs'].apply(lambda x : str(x).replace('+',''))
data['Installs']=data['Installs'].apply(lambda x : str(x).replace(',',''))
print(data['Installs'].unique())


# **Replacing ** '+'** and ** ',' ** from the Installs columns**

# In[ ]:


data.groupby('Installs')['Rating'].mean().plot("barh",figsize=(10,13),title ="Rating vs Installs");


# **The apps which have moderate installs have less rating compared to the max and min installs. Observe the pattern "C"  in the grapch**

# In[ ]:





# In[ ]:




