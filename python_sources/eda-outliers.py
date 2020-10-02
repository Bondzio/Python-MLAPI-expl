#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os, subprocess
import seaborn as sns
import matplotlib.pyplot as plt
print(os.listdir("../input"))


# ## Load Training Data

# In[2]:


fpath = "../input/sales_train.csv.gz"
dtype = {"date_block_num": "int8",
         "item_id": "uint16",
         "shop_id": "int8",
         "item_price": "float64",
         "item_cnt_day": "int16"}
df_Train = pd.read_csv(fpath, compression="gzip", parse_dates=["date"], dtype=dtype,
                       date_parser=lambda x: pd.to_datetime(x, format="%d.%m.%Y"))
df_Train["month"] = df_Train["date"].dt.month
df_Train["day"] = df_Train["date"].dt.day


# In[3]:


fpath = "../input/test.csv.gz"
dtype = {"item_id": "uint16",
         "shop_id": "int8",}
df_Test = pd.read_csv(fpath, dtype=dtype, index_col="ID")


# In[4]:


target_shops = df_Test["shop_id"].unique()
target_items = df_Test["item_id"].unique()


# ## The distribution of item_cnt_day
# ---
# * We can see that some items are sold crazely at some point

# In[5]:


df_Train["item_cnt_day"].plot(figsize=(10, 6));


# We see that some shops are very good at selling some products

# In[6]:


q = (df_Train["item_cnt_day"] >= 20)&(df_Train["shop_id"].isin(target_shops))&(df_Train["item_id"].isin(target_items))
df_Train[q].groupby("shop_id").agg({"item_id": "nunique"}).sort_values("item_id", ascending=False).head()


# We can see item are very easy to be sold more than others

# In[7]:


df_Train[q].groupby("item_id").agg({"shop_id": "nunique"}).sort_values("shop_id", ascending=False).head()


# ## Aggregate cnt by month
# ---
# * Each item enters the market at different time
# * Some item are easier to be sold than others

# In[8]:


target_col = "item_cnt_day"
df_CNT = df_Train.groupby(["shop_id", "item_id", "date_block_num"]).agg({target_col: "sum"}).reset_index()
# Clipping
df_CNT.loc[df_CNT[target_col]>20, target_col] = 20
df_CNT.loc[df_CNT[target_col]<0, target_col] = 0


# In[9]:


_, ax = plt.subplots(1, 1, figsize=(20, 6))
q = (df_CNT["item_id"]==3731)&(df_CNT["shop_id"].isin(target_shops))
sns.heatmap(df_CNT[q].pivot("shop_id", "date_block_num", "item_cnt_day"), ax=ax);


# In[10]:


_, ax = plt.subplots(1, 1, figsize=(20, 6))
q = (df_CNT["item_id"]==20949)&(df_CNT["shop_id"].isin(target_shops))
sns.heatmap(df_CNT[q].pivot("shop_id", "date_block_num", "item_cnt_day"), ax=ax);


# ## Distribution between CNT mean and std over all month

# In[11]:


temp = df_CNT.groupby(["shop_id", "item_id"]).agg({"item_cnt_day": ["std", "mean"]}).dropna()
temp.columns = ["CNT_STD", "CNT_MEAN"]


# In[12]:


temp.plot.scatter("CNT_MEAN", "CNT_STD");


# In[ ]:




