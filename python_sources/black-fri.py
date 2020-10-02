#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input/"))

# Any results you write to the current directory are saved as output.


# In[ ]:


train=pd.read_csv("../input/train.csv")
test=pd.read_csv("../input/test.csv")
#sub=pd.read_csv("sample_submission_AN0dlrC.csv")


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


print(train.shape , test.shape)


# In[ ]:


#del test["Comb"]


# In[ ]:


train.info()


# In[ ]:


train["source"]='train'
test["source"]='test'
df = pd.concat([train,test], ignore_index = True, sort = False)


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


df.isnull().sum()/df.shape[0]*100


# In[ ]:


import seaborn as sns
sns.set_style('darkgrid')


# In[ ]:


sns.relplot(x="Product_Category_1", y="Purchase", data=df);


# In[ ]:


#df.pop("Product_Category_2")
#df.pop("Product_Category_3")


# In[ ]:


pivot = train.pivot_table(index='Product_Category_2', values="Purchase", aggfunc=np.mean)
pivot.plot(kind='bar', color='blue',figsize=(12,7))
plt.xlabel("Product_Category_2")
plt.ylabel("Purchase")
plt.show


# In[ ]:


df["Product_Category_2"]=df["Product_Category_2"].fillna(1)


# In[ ]:


Occupation_pivot = train.pivot_table(index='Product_Category_1', values="Purchase", aggfunc=np.mean)
Occupation_pivot.plot(kind='bar', color='blue',figsize=(12,7))
plt.xlabel("Product_Category_1")
plt.ylabel("Purchase")
plt.show


# In[ ]:


condition = df.index[(df.Product_Category_1.isin([19,20])) & (df.source == "train")]
df = df.drop(condition)


# In[ ]:


pivot = train.pivot_table(index='Product_Category_3', values="Purchase", aggfunc=np.mean)
pivot.plot(kind='bar', color='blue',figsize=(12,7))
plt.xlabel("Product_Category_3")
plt.ylabel("Purchase")
plt.show


# In[ ]:


df["Product_Category_3"]=df["Product_Category_3"].fillna(1)


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


df.apply(lambda x: len(x.unique()))


# In[ ]:


df["Age"].value_counts()


# In[ ]:


pivot = df.pivot_table(index='Age', values="Purchase", aggfunc=np.mean)
pivot.plot(kind='bar', color='blue',figsize=(12,7))
plt.xlabel("Age")
plt.ylabel("Purchase")
plt.show


# In[ ]:


pivot = df.pivot_table(index='Stay_In_Current_City_Years', values="Purchase", aggfunc=np.mean)
pivot.plot(kind='bar', color='blue',figsize=(12,7))
plt.xlabel("Stay_In_Current_City_Years")
plt.ylabel("Purchase")
plt.show


# In[ ]:


from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()

df["Gender"]=le.fit_transform(df["Gender"])
df["Age"]=le.fit_transform(df["Age"])


# In[ ]:


df["City_Category"]=le.fit_transform(df["City_Category"])


# In[ ]:


df = pd.get_dummies(df, columns=['Stay_In_Current_City_Years'])


# In[ ]:


df['Product_ID'] = df['Product_ID'].factorize()[0]


# In[ ]:


df.shape


# In[ ]:


df.head()


# In[ ]:


df1=df.groupby(["User_ID"])["Purchase"].mean()
df1=df1.reset_index()
df1=df1.rename(columns={'Purchase':'avg_orders'})


# In[ ]:


df1.head()


# In[ ]:


df = pd.merge(df, df1,  how='left', left_on=['User_ID'], right_on = ['User_ID'])


# In[ ]:


df.info()


# In[ ]:


def getCountVar(compute_df, count_df, var_name):
    grouped_df = count_df.groupby(var_name)
    count_dict = {}
    for name, group in grouped_df:
        count_dict[name] = group.shape[0]
    count_list = []
    for index, row in compute_df.iterrows():
        name = row[var_name]
        count_list.append(count_dict.get(name, 0))
    return count_list


# In[ ]:


df["User_ID_Count"] = getCountVar(df, df, "User_ID")
df["Age_Count"] =getCountVar(df, df, "Age")
df["Occupation_Count"] =getCountVar(df, df, "Occupation")
df["Product_Category_1_Count"] =getCountVar(df, df,"Product_Category_1")
#df["Product_Category_2_Count"] =getCountVar(df, df, "Product_Category_2")
#df["Product_Category_3_Count"] =getCountVar(df, df,"Product_Category_3")
df["Product_ID_Count"] =getCountVar(df, df, "Product_ID")


# In[ ]:


df["Product_Category_2_Count"] =getCountVar(df, df, "Product_Category_2")
df["Product_Category_3_Count"] =getCountVar(df, df,"Product_Category_3")


# In[ ]:


df.head()


# In[ ]:


train = df.loc[df["source"]=="train"]
test = df.loc[df["source"]=="test"]


# In[ ]:


test.drop(["source"],axis=1,inplace=True)
train.drop(["source"],axis=1,inplace=True)


# In[ ]:


print(train.shape,test.shape)


# In[ ]:


del test["Purchase"]


# In[ ]:


y=train["Purchase"]
del train["Purchase"]
x=train


# In[ ]:


print(x.shape,test.shape)


# In[ ]:


import xgboost as xgb


# In[ ]:


params = {}
params["objective"] = "reg:linear"
params["eta"] = 0.03
params["min_child_weight"] = 10
params["subsample"] = 0.8
params["colsample_bytree"] = 0.7
params["silent"] = 1
params["max_depth"] = 10
#params["max_delta_step"]=2
params["seed"] = 0
 #params['eval_metric'] = "auc"
plst4 = list(params.items())
num_rounds4 = 1100

import xgboost as xgb
xgdmat=xgb.DMatrix(x,y)

final_gb4=xgb.train(plst4,xgdmat,num_rounds4)

tesdmat=xgb.DMatrix(test)
y_pred=final_gb4.predict(tesdmat)


# In[ ]:


y_pred


# In[ ]:


sub=pd.read_csv("../input/test.csv")


# In[ ]:


sub.head()


# In[ ]:


sub=sub.iloc[:,[0,1]]


# In[ ]:


sub["Purchase"]=y_pred


# In[ ]:


j=0
for x in sub["Purchase"]:
    if(x<0):
        sub["Purchase"][j]=12
    j+=1  


# In[ ]:


sub.head()


# In[ ]:


sub.to_csv("output.csv",index=False)


# In[ ]:




