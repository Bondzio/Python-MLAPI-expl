#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


train=pd.read_csv('../input/train.csv')
test=pd.read_csv('../input/test.csv')
train.head()
#train.shape


# In[ ]:


train['src']='train'
test['src']='test'
data=pd.concat([train,test],ignore_index=True)
data.shape


# In[ ]:


data.isnull().sum()


# In[ ]:


data.Item_Outlet_Sales.plot(kind='hist',bins=100)


# In[ ]:


plt.figure(1)
plt.subplot(131)
data.Item_Weight.plot(kind='hist',bins=50,figsize=(18,6),title='Weight')
plt.subplot(132)
data.Item_Visibility.plot(kind='hist',bins=50,title='Visibility',color='r')
plt.subplot(133)
data.Item_MRP.plot(kind='hist',bins=100,title='MRP',color='g')


# In[ ]:


data.Item_Fat_Content.value_counts().plot(kind='bar')


# In[ ]:


tdf=data.Item_Fat_Content.isin(['LF','Low Fat'])
tdf=tdf[tdf==True]
for i in tdf.index:
    data.at[i,'Item_Fat_Content']='low fat'
#data[dat.i.ipynb_checkpoints/ynb_checkpoints/ipynb_checkpoints/.Item_Fat_Content=='reg']['Item_Fat_Content']='Regular'


# In[ ]:


tdf=data.Item_Fat_Content.isin(['Regular','reg'])
tdf=tdf[tdf==True]
for i in tdf.index:
    data.at[i,'Item_Fat_Content']='regular'


# In[ ]:


data.Item_Fat_Content.value_counts().plot(kind='bar',title='Fat')


# In[ ]:


plt.figure(2)
plt.subplot(131)
data.Item_Type.value_counts().plot(kind='bar',title='Item Type',figsize=(18,6))
plt.subplot(132)
data.Outlet_Identifier.value_counts().plot(kind='bar',title='Out_Id')
plt.subplot(133)
data.Outlet_Size.value_counts().plot(kind='bar',title='Out_size')


# In[ ]:


plt.figure(3)
plt.subplot(131)
data.Outlet_Establishment_Year.value_counts().plot(kind='bar',title='Out Year',figsize=(21,6))
plt.subplot(132)
data.Outlet_Type.value_counts().plot(kind='bar',title='out type')
plt.subplot(133)
data.Outlet_Location_Type.value_counts().plot(kind='bar',title='out loc')


# In[ ]:


train=data.iloc[1:train.shape[0]]


# In[ ]:


plt.rcParams['figure.figsize']=(21,6)
plt.subplot(131)
plt.ylabel('sales')
plt.scatter(train.Item_MRP,train.Item_Outlet_Sales,color='g')
plt.subplot(132)
plt.tight_layout()
plt.legend()
plt.scatter(train.Item_Weight,train.Item_Outlet_Sales)
plt.subplot(133)
plt.scatter(train.Item_Visibility,train.Item_Outlet_Sales,color='y')


# In[ ]:



plt.rcParams['figure.figsize']=(12,6)
train.groupby('Item_Type')[['Item_Type','Item_Outlet_Sales']].mean().sort_values(ascending=False,by='Item_Outlet_Sales').plot(kind='bar',color='r')
train.groupby('Item_Fat_Content')[['Item_Fat_Content','Item_Outlet_Sales']].mean().sort_values(ascending=False,by='Item_Outlet_Sales').plot(kind='bar')
train.groupby('Outlet_Identifier')[['Outlet_Identifier','Item_Outlet_Sales']].mean().sort_values(ascending=False,by='Item_Outlet_Sales').plot(kind='bar',color='g')


# In[ ]:


plt.rcParams['figure.figsize']=(20,8)
pl=sns.violinplot(x='Item_Type',y='Item_Outlet_Sales',data=train,linewidth=0.5,width=1)
_=pl.set_xticklabels(labels=train.Item_Type.unique(),rotation=30)
#train.groupby('Item_Fat_Content')[['Item_Fat_Content','Item_Outlet_Sales']].mean().sort_values(ascending=False,by='Item_Outlet_Sales').plot(kind='box')
#train.groupby('Outlet_Identifier')[['Outlet_Identifier','Item_Outlet_Sales']].mean().sort_values(ascending=False,by='Item_Outlet_Sales').plot(kind='box',color='g')


# In[ ]:


pl=sns.violinplot(x='Item_Fat_Content',y='Item_Outlet_Sales',data=train,linewidth=0.5,width=1)
_=pl.set_xticklabels(labels=train.Item_Fat_Content.unique(),rotation=30)


# In[ ]:


pl=sns.violinplot(x='Outlet_Identifier',y='Item_Outlet_Sales',data=train,linewidth=0.5,width=1)
_=pl.set_xticklabels(labels=train.Outlet_Identifier.unique(),rotation=30)


# In[ ]:



pl=sns.violinplot(x='Outlet_Size',y='Item_Outlet_Sales',data=train,)


# In[ ]:


pl=sns.violinplot(x='Outlet_Location_Type',y='Item_Outlet_Sales',data=train,)


# In[ ]:



pl=sns.violinplot(x='Outlet_Type',y='Item_Outlet_Sales',data=train,)


# In[ ]:


train.isnull().sum()


# In[ ]:


wei=data.groupby('Item_Type').Item_Weight.mean()


# In[ ]:


for name in data.Item_Type.unique():
    df=data[(data.Item_Type==name) & (data.Item_Weight.isnull())]
    for k in list(df.index):
        data.at[k,'Item_Weight']=wei[name]


# In[ ]:


wei=data.groupby('Item_Type').Item_Visibility.mean()


# In[ ]:


for name in data.Item_Type.unique():
    df=data[(data.Item_Type==name) & (data.Item_Visibility==0)]
    for k in list(df.index):
        data.at[k,'Item_Visibility']=wei[name]


# In[ ]:


train[train.Item_Visibility==0]


# In[ ]:


train.Item_Visibility.plot(kind='hist',bins=100)


# In[ ]:


psd=data.groupby('Outlet_Type')['Outlet_Size'].value_counts()


# In[ ]:


df=data[data.Outlet_Size.isnull()]
for k in list(df.index):
    if data.at[k,'Outlet_Type'] in ['Grocery Store','Supermarket Type1']:
        data.at[k,'Outlet_Size']='Small'
    else:
        data.at[k,'Outlet_Size']='Medium'


# In[ ]:


data['Item_Type_Combined'] = data['Item_Identifier'].apply(lambda x: x[0:2])
data['Item_Type_Combined'] = data['Item_Type_Combined'].map({'FD':'Food',
                                                             'NC':'Non-Consumable',
                                                             'DR':'Drinks'})
data.Item_Type_Combined.value_counts()


# In[ ]:


data['Outlet_Years']=2018-data.Outlet_Establishment_Year


# In[ ]:


from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
data['Outlet']=le.fit_transform(data.Outlet_Identifier)
var_mod = ['Item_Fat_Content','Outlet_Location_Type','Outlet_Size','Item_Type_Combined','Outlet_Type','Outlet']
le = LabelEncoder()
for i in var_mod:
    data[i] = le.fit_transform(data[i].astype(str))


# In[ ]:


data = pd.get_dummies(data, columns=['Item_Fat_Content','Outlet_Location_Type','Outlet_Size','Outlet_Type',
                              'Item_Type_Combined','Outlet'])


# In[ ]:


data.columns


# In[ ]:


data.drop(['Item_Type','Outlet_Establishment_Year'],axis=1,inplace=True)


# In[ ]:


train = data.loc[data['src']=="train"]
test = data.loc[data['src']=="test"]


# In[ ]:


test.drop(['Item_Outlet_Sales','src'],axis=1,inplace=True)


# In[ ]:


train.to_csv("train_modified.csv",index=False)
test.to_csv("test_modified.csv",index=False)


# In[ ]:


train.drop(['src'],axis=1,inplace=True)


# In[ ]:


train.dtypes


# In[ ]:


target = 'Item_Outlet_Sales'
IDcol = ['Item_Identifier','Outlet_Identifier']


# In[ ]:


predictors = [x for x in train.columns if x not in [target]+IDcol]


# In[ ]:


from sklearn.linear_model import LinearRegression
le=LinearRegression()
le.fit(train[predictors],train[target])


# In[ ]:


pred=le.predict(test)


# In[ ]:





# In[ ]:




