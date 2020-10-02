#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
data=pd.read_csv('../input/zomato-bangalore-restaurants/zomato.csv')


# In[ ]:


data.head()


# In[ ]:


data.columns


# In[ ]:


data.reviews_list[0]


# In[ ]:





# In[ ]:





# In[ ]:


data.drop(columns=['url','phone','address'],inplace=True)


# In[ ]:


data.head()
data.drop(columns=['menu_item'],inplace=True,axis=1)


# In[ ]:


data.head()


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


data.isnull().sum()


# In[ ]:


data.drop(columns=['reviews_list'],inplace=True,axis=1)


# In[ ]:


data.columns


# In[ ]:


data.rate


# In[ ]:


data['rate'].value_counts()
data['rate'].isnull().sum()


# In[ ]:


data['rate']=data['rate'].apply(lambda x: str(x).split('/')[0])


# In[ ]:


data.rate


# In[ ]:


data.columns


# In[ ]:


data=data.rename(columns={"approx_cost(for two people)":"avg_cost","listed_in(type)":"meal_type","listed_in(city)" : "city"})


# In[ ]:


data.columns


# In[ ]:


data.name.value_counts()


# In[ ]:


data.online_order.value_counts()


# In[ ]:


data.book_table.value_counts()


# In[ ]:


data.rate.value_counts()


# In[ ]:


data.votes.value_counts()


# In[ ]:


data.location.value_counts()


# In[ ]:


data.rest_type.value_counts()


# In[ ]:


data.dish_liked.value_counts()


# In[ ]:


data.cuisines.value_counts()


# In[ ]:





# In[ ]:


data.avg_cost.value_counts()


# In[ ]:


data.avg_cost.value_counts()


# In[ ]:


data.meal_type.value_counts()


# In[ ]:


len(data.city.value_counts())


# In[ ]:


data.drop(columns=['location'],inplace=True,axis=1)


# In[ ]:


data.columns


# In[ ]:


data.isnull().sum()


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context("paper",font_scale=2,rc={"font-size":20,"axes.titlesize":25,"axes.labelsize": 20})
sns.catplot(data=data,kind='count',x='online_order')
plt.title("Number of resturants that take order online")
plt.show()


# In[ ]:


sns.set_context("paper",font_scale=2,rc={"font-size":20,"axes.titlesize":25,"axes.labelsize": 20})
sns.catplot(data=data,kind='count',x='book_table')
plt.title("Number of resturants that have option yo book table online")
plt.show()


# In[ ]:


sns.set_context("paper",font_scale=1,rc={"font-size":3,"axes.titlesize":3,"axes.labelsize": 3})
sns.catplot(data=data,kind="count",x="meal_type")
#plt.title("No. of resturants according to meal type")
plt.show()


# In[ ]:


sns.set_context("paper", font_scale = 1, rc={"font.size": 3,"axes.titlesize": 5,"axes.labelsize": 2})   
b = sns.catplot(data = data, kind = 'count', x = 'city')
plt.title('Number of restaurants in each city')
b.set_xticklabels(rotation = 90)
plt.show()


# In[ ]:


a=list(data['rate'])


# In[ ]:


for i in range(0,len(a)):
    if a[i]=='nan':
        a[i]='unrated'
    if a[i]=='-':
        a[i]='unrated'
    if a[i]=='NEW':
        a[i]='unrated'


# In[ ]:


data['rate']=a


# In[ ]:


data['rate'].value_counts()


# In[ ]:


a = list(data['rate'])
for i in range(0, len(a)):
    if a[i] == 'unrated':
        a[i] = None
    else :
        a[i] = float(a[i])
data['rate'] = a


# In[ ]:


sns.set_context("paper",font_scale=1,rc={"font.size": 20,"axes.titlesize": 25,"axes.labelsize": 20})
b=sns.catplot(data=data,kind='count',x='rate',order=data['rate'].value_counts().index)
plt.title("Number of restuarants for each rating")
b.set_xticklabels(rotation=90)
plt.show()


# In[ ]:


# Plotting count plot of rest_type
sns.set_context("paper", font_scale = 1, rc = {"font.size": 5,"axes.titlesize": 5,"axes.labelsize": 2})   
b = sns.catplot(data = data, kind = 'count', x = 'rest_type', order = data['rest_type'].value_counts().index)
plt.title('Number of restaurants for each type')
b.set_xticklabels(rotation = 90)
plt.show()

# count plot of top 10
sns.set_context("paper", font_scale = 1, rc = {"font.size": 20,"axes.titlesize": 25,"axes.labelsize": 20})   
b = sns.catplot(data = data, kind = 'count', x = 'rest_type', order = data['rest_type'].value_counts().head(10).index)
plt.title('Number of restaurants for each type')
b.set_xticklabels(rotation = 90)
plt.show()

# count plot of type last 10
sns.set_context("paper", font_scale = 1, rc = {"font.size": 20,"axes.titlesize": 25,"axes.labelsize": 20})   
b = sns.catplot(data = data, kind = 'count', x = 'rest_type', order = data['rest_type'].value_counts().tail(10).index)
plt.title('Number of restaurants for each type')
b.set_xticklabels(rotation = 90)
plt.show()


# In[ ]:


sns.set_context("paper", font_scale = 1, rc = {"font.size": 20,"axes.titlesize": 25,"axes.labelsize": 20})   
b = sns.catplot(data = data, kind = 'count', x = 'avg_cost', order = data['avg_cost'].value_counts().tail(10).index)
plt.title('Number of restaurants for each type')
b.set_xticklabels(rotation = 90)
plt.show()


# In[ ]:


data.info()


# In[ ]:


data.describe()


# In[ ]:


plt.figure(figsize=(12,6))
data['city'].value_counts()[:10].plot(kind='pie')
plt.title("Location pie",weight='bold')


# In[ ]:


data['avg_cost'].value_counts()[:20]


# In[ ]:


plt.figure(figsize=(12,8))
data['avg_cost'].value_counts()[:20].plot(kind='pie')
plt.title('Avg cost in Restaurent for 2 people', weight = 'bold')
plt.show()


# In[ ]:


dishes_data = data[data.dish_liked.notnull()]
dishes_data.dish_liked = dishes_data.dish_liked.apply(lambda x:x.lower().strip())
dishes_data.isnull().sum()


# In[ ]:


dishes_data


# In[ ]:


dishes_count=[]
for i in dishes_data.dish_liked:
    for t in i.split(','):
        t=t.strip()
        dishes_count.append(t)


# In[ ]:


plt.figure(figsize=(12,8))
pd.Series(dishes_count).value_counts()[:20].plot(kind='bar',color='c')
plt.title("most 20 liked dishes in banglore",weight='bold')
plt.show()


# In[ ]:


data['rate'].isnull().sum()


# In[ ]:


data.rate


# In[ ]:


data['rate'] = data['rate'].replace('NEW',np.NaN)
data['rate'] = data['rate'].replace('-',np.NaN)
data.dropna(how = 'any', inplace = True)


# In[ ]:


data.rate.hist(color='red')
plt.axvline(x= data.rate.mean(),ls='--',color='yellow')
plt.title('Average Rating for Bangalore Restaurants',weight='bold')
plt.xlabel('Rating')
plt.ylabel('No of Restaurants')
print(data.rate.mean())


# In[ ]:


f,ax=plt.subplots(figsize=(18,8))
g = sns.pointplot(x=data["rest_type"], y=data["rate"], data=data)
g.set_xticklabels(g.get_xticklabels(), rotation=90)
plt.title('Restaurent type vs Rate', weight = 'bold')
plt.show()


# In[ ]:


cuisines_data=data[data.cuisines.notnull()]
cuisines_data.cuisines= cuisines_data.cuisines.apply(lambda x:x.lower().strip())


# In[ ]:


cuisines_count=[]
for i in cuisines_data.cuisines:
    for j in i.split(','):
        j=j.strip()
        cuisines_count.append(j)


# In[ ]:


plt.figure(figsize=(12,8))
pd.Series(cuisines_count).value_counts()[:10].plot(kind='bar',color='r')
plt.title('Cuisines and count of them in restuarants')
plt.show()


# In[ ]:


data['online_order']= pd.get_dummies(data.online_order, drop_first=True)
data['book_table']= pd.get_dummies(data.book_table, drop_first=True)
data


# In[ ]:


data['rest_type'] = data['rest_type'].str.replace(',' , '') 
data['rest_type'] = data['rest_type'].astype(str).apply(lambda x: ' '.join(sorted(x.split())))
data['rest_type'].value_counts().head()
data['cuisines'] = data['cuisines'].str.replace(',' , '') 
data['cuisines'] = data['cuisines'].astype(str).apply(lambda x: ' '.join(sorted(x.split())))
data['cuisines'].value_counts().head()


# In[ ]:


from sklearn.preprocessing import LabelEncoder
T = LabelEncoder()                 
data['city'] = T.fit_transform(data['city'])
data['rest_type'] = T.fit_transform(data['rest_type'])
data['cuisines'] = T.fit_transform(data['cuisines'])


# In[ ]:


data["avg_cost"] = data["avg_cost"].str.replace(',' , '') 
data["avg_cost"] = data["avg_cost"].astype('float')
data.head()


# In[ ]:


#y = data['rate']
x = data.drop(['rate','name'],axis = 1)


# In[ ]:


x.shape
y.shape


# In[ ]:





# In[ ]:


from sklearn.preprocessing import StandardScaler


# In[ ]:


from sklearn.preprocessing import StandardScaler
num_values1=data.select_dtypes(['float64','int64']).columns
scaler = StandardScaler()
scaler.fit(data[num_values1])
data[num_values1]=scaler.transform(data[num_values1])


# In[ ]:


data.head()


# In[ ]:


x = data.drop(['dish_liked'],axis = 1)


# In[ ]:


data.head()


# In[ ]:





# In[ ]:





# In[ ]:


x.head()


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(x,y,test_size = 0.3,random_state = 33)
x = data.drop(['dish_liked','name','meal_type'],axis = 1)
x


# In[ ]:


from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor()
rfr.fit(X_train,y_train)
y_pred_rfr = rfr.predict(X_test)

