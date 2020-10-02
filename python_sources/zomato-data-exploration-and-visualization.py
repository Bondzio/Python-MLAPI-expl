#!/usr/bin/env python
# coding: utf-8

# # Zomato - A Exercise in Data Exploration and Visualization

# Zomato is a online food delivery app and Bengaluru is one of the most digitally enabled cities in India, a huge number of city population uses the services of Zomato to find its next meal of the day.

# The data below is useful as it can answer so many questions which matter to me personally as a dweller of the city who is highly reliant on the app.

# Please <b>UPVOTE</b> the notebook if you find it fun, it helps me publish more such work.
# As always any comments are welcome, let me know if you have a question in your mind which I can help answer through the data.
# 

# ### Comments and Pizzas are always welcome.. :-)
# ### Stay Hungry ! Stay Foolish !

# In[1]:


# Lets load the libraries
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp


# # Loading and Understanding Data

# In[2]:


# Load the data
df = pd.read_csv('../input/zomato.csv')
print('Shape of Original Dataset is : {}'.format(df.shape))


# In[3]:


# Print Sample data
df.sample(5)


# In[4]:


# As we are not going to use URL, Address and Phone number, lets drop it, also we already have ratings, so need of review list
df = df.drop(['url','address','phone','reviews_list','menu_item'],axis=1)
df.columns


# In[5]:


# Extract rating as number from
df['rating'] = df['rate'].str.split('/',n=2,expand=True)[0]
df = df.drop('rate',axis=1)


# In[6]:


# Put Cuisines and Dish Likes into Lists
df['dish_liked'] = df['dish_liked'].str.split(',')
df['cuisines'] = df['cuisines'].str.split(',')
df[['dish_liked','cuisines']].head()


# In[7]:


# Print percent of null values in each columns
print('Percentage of Null Values in each column')
print('-----------------------------------------')
((df.isna()*1).sum()/len(df))*100


# In[8]:


# Print Data types of each columns
print('Data Type of Each column')
print('--------------------------')
df.dtypes


# ## Data Cleaning and Standardization

# In[9]:


# make non numeric values as null
df['rating'] = df['rating'].apply(lambda x: None if x in ('NEW',None,'-') else float(x))


# In[10]:


# If  null values are there in Dish Likes and Cuisines, fill them with empty, as some places can have not major dishes
df[['dish_liked','cuisines']] = df[['dish_liked','cuisines']].fillna(value='')


# In[11]:


# Drop the null values, as rating are target column we cant use rows which dont have rating itself
df = df.dropna()


# In[12]:


# Rename columns with simpler names for use
df.rename(columns={'approx_cost(for two people)': 'approx_cost','listed_in(type)':'type','listed_in(city)':'Area'},inplace=True)
df.columns


# In[13]:


# Convert data type of approx cost from character to numeric
df['approx_cost'] = df['approx_cost'].str.replace(',','').apply(lambda x:float(x))


# In[14]:


print('Percentage of Null Data after modification')
print('-------------------------------------------')
((df.isna()*1).sum()/len(df))*100


# In[15]:


print('Data Type of Each column after modification')
print('---------------------------------------------')
df.dtypes


# In[16]:


print('Shape of Cleaned Dataset is : {}'.format(df.shape))


# ## Exploratory Data Analysis and Visualization

# In[17]:


df.head()


# In[18]:


# Lets look at distribution of Continues variables
fig = plt.figure(figsize=(14,10))
ax1 = fig.add_subplot(3,2,1)
ax2 = fig.add_subplot(3,2,2)
sns.distplot(df['votes'],ax=ax1)
sns.boxplot(df['votes'],ax=ax2)
ax3 = fig.add_subplot(3,2,3)
ax4 = fig.add_subplot(3,2,4)
sns.distplot(df['approx_cost'],ax=ax3)
sns.boxplot(df['approx_cost'],ax=ax4)
ax5 = fig.add_subplot(3,2,5)
ax6 = fig.add_subplot(3,2,6)
sns.distplot(df['rating'],ax=ax5)
sns.boxplot(df['rating'],ax=ax6)


# In[19]:


# Lets look at distribution of Online Orders and Table Booking Variables
fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)
sns.countplot(x=df['online_order'],ax=ax1)
sns.countplot(x=df['book_table'],ax=ax2)
plt.yticks(rotation=45)


# In[20]:


# Lets look at distribution of Location Variable
fig = plt.figure(figsize=(10,20))
ax1 = fig.add_subplot(1,1,1)
sns.countplot(y=df['location'],ax=ax1)
p = plt.xticks(rotation=30)


# In[21]:


# Lets look at distribution of Categorical Variable
fig = plt.figure(figsize=(10,20))
ax1 = fig.add_subplot(1,1,1)
sns.countplot(y=df['Area'],ax=ax1)
p = plt.xticks(rotation=30)


# In[22]:


# Lets look at distribution of restaurant type Variables
fig = plt.figure(figsize=(10,20))
ax1 = fig.add_subplot(1,1,1)
sns.countplot(y=df['rest_type'],ax=ax1)


# In[23]:


# Lets look at distribution of Type Variable
fig = plt.figure(figsize=(4,4))
ax1 = fig.add_subplot(1,1,1)
sns.countplot(x=df['type'],ax=ax1)
plt.xticks(rotation=30)


# ### Multivariant Analysis

# In[24]:


# Rating v/s Online Order
fig = plt.figure(figsize=(10,3))
ax1 = fig.add_subplot(1,1,1)
sns.boxplot(x=df['rating'],y=df['online_order'])


# In[25]:


# Lets perform Hypothisis Testing to confirm if there is a significant difference between 2 means
a = df[df['online_order'] == 'Yes']['rating']
b = df[df['online_order'] == 'No']['rating']
t_value,p_value = sp.stats.ttest_ind(a,b)
print('Students T-Test Performed')
print('T Value : {}'.format(t_value))
print('p Value : {}'.format(p_value))
if p_value < 0.05:
    print('There is a significant Difference in Mean rating of Places accepting online orders vs the ones not accepting')
else:
    print('There is no significant Difference in Mean rating of Places online orders vs the ones not accepting')


# In[26]:


# Rating v/s Table Booking
fig = plt.figure(figsize=(10,3))
ax1 = fig.add_subplot(1,1,1)
sns.boxplot(x=df['rating'],y=df['book_table'])


# In[27]:


# Lets perform Hypothisis Testing to confirm if there is a significant difference between 2 means
a = df[df['book_table'] == 'Yes']['rating']
b = df[df['book_table'] == 'No']['rating']
t_value,p_value = sp.stats.ttest_ind(a,b)
print('Students T-Test Performed')
print('T Value : {}'.format(t_value))
print('p Value : {}'.format(p_value))
if p_value < 0.05:
    print('There is a significant Difference in Mean rating of Places allowing table booking vs the ones not')
else:
    print('There is no significant Difference in Mean rating of Places allowing table vs the ones not accepting')


# In[28]:


# Rating v/s Table Booking
fig = plt.figure(figsize=(10,4))
ax1 = fig.add_subplot(1,1,1)
sns.scatterplot(x=df['rating'],y=df['votes'],ax=ax1)
slope,inter,r_value,p_value,std_err = sp.stats.linregress(x=df['rating'],y=df['votes'])
x = np.array(df['rating'])
y = np.array(df['rating'].apply(lambda y:y*slope + inter))
ax1.plot(x,y)
plt.legend(labels=['slope : {}\nIntercept : {}\nR-Value : {}\nP-Value : {}\nstd-err : {}'.format(slope,inter,r_value,p_value,std_err),],loc=2)
print('There is a strong Relation between Rating vs Votes, better places get more votes')
print('-----------------------------------------------------------------------------------')


# In[29]:


# Rating v/s Approx Cost
fig = plt.figure(figsize=(10,4))
ax1 = fig.add_subplot(1,1,1)
sns.scatterplot(x=df['rating'],y=df['approx_cost'],ax=ax1)
slope,inter,r_value,p_value,std_err = sp.stats.linregress(x=df['rating'],y=df['approx_cost'])
x = np.array(df['rating'])
y = np.array(df['rating'].apply(lambda y:y*slope + inter))
ax1.plot(x,y)
plt.legend(labels=['slope : {}\nIntercept : {}\nR-Value : {}\nP-Value : {}\nstd-err : {}'.format(slope,inter,r_value,p_value,std_err),],loc=2)
print('There is a strong Relation between Rating vs ApproxCost, better places are as expected, costly')
print('------------------------------------------------------------------------------------------------')


# In[30]:


# Lets find what are the most popular cuisies in Bengaluru and Most Liked Dishes
cuisines = []
dishes = []
for i in df['cuisines']:
    for j in i:
        cuisines.append(j)
for i in df['dish_liked']:
    for j in i:
        dishes.append(j)

cuisines = pd.Series(cuisines)
dishes = pd.Series(dishes)
print('Total number of Cuisines in data : {}'.format(len(cuisines)))
print('Total number of Dishes in data : {}'.format(len(dishes)))


# In[33]:


# Find top 20 most popular cuisine types
top20_cuisines = cuisines.str.strip().value_counts().head(20)
fig = plt.figure(figsize=(8,10))
ax1 = fig.add_subplot(1,1,1)
sns.barplot(x=top20_cuisines.values,y=top20_cuisines.index)


# In[35]:


# Find top 50 most popular dishes in town, now this is what digital people of Bengaluru prefer.
top50_dishes = dishes.str.strip().value_counts().head(50)
fig = plt.figure(figsize=(8,12))
ax1 = fig.add_subplot(1,1,1)
sns.barplot(x=top50_dishes.values,y=top50_dishes.index)
print('East of West, idly & Dosa is the Best.. No Matter what this stupied data says')
print('------------------------------------------------------------------------------')


# In[36]:


# Top Location in town to get good food.
top_places = df.groupby('Area')['rating'].median().sort_values(ascending=False)
print('Top Locations in bengaluru to find food..')
print('If you can reach there, after navigating through traffic!!!!')
print('----------------------------------------------------------')
pd.DataFrame(top_places)


# In[37]:


# Top rated restaurant types
top_types = df.groupby('type')['rating'].median().sort_values(ascending=False)
top_types


# ### Alright Floks ! thats all for today, will add more if i get any new ideas..
# ### Let me know in comments if you have any in your mind.

# In[ ]:




