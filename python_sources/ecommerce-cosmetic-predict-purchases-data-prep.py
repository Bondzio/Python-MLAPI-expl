#!/usr/bin/env python
# coding: utf-8

# ## PREPARE Data for classification
# * predict at time of view or addition tocart if user will purchase each product or not 
# * this is about setting up the data & targets
# * This pipeline can also be applied to : https://www.kaggle.com/mkechinov/ecommerce-behavior-data-from-multi-category-store
# * Feature engineering will be done extnerally
# 
# * another target possible - will an item be removed from cart ? 

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


# define dtypes on loading data  - will speed up and reduce memory use
categorical_dtypes = {
    'event_type':'category', 'product_id':'category',
    'category_id':'category',
       'category_code':'category', 'brand':'category', 
    'user_id':'category', 'user_session':'category'
}


# In[ ]:


### setting the dtype on import to categorical doesn't work when concatenating.. 
df = pd.concat([pd.read_csv("/kaggle/input/ecommerce-events-history-in-cosmetics-shop/2019-Oct.csv",dtype=categorical_dtypes)
                ,pd.read_csv("/kaggle/input/ecommerce-events-history-in-cosmetics-shop/2019-Nov.csv",dtype=categorical_dtypes)])

df['event_time'] = pd.to_datetime(df['event_time'],infer_datetime_format=True)


# add joint key for user + product (Could also add user + category)
df["user_product"] = (df['user_id'].astype(str)+df['product_id'].astype(str)).astype('category').cat.codes


## categorical/label encoding of the IDs (instead of string - save memory/file size):
### we still need to define ats categoircal due to the concatenation of the input files
df['user_session'] = df['user_session'].astype('category').cat.codes.astype('category')
df['user_session'] = df['user_session'].astype('category').cat.codes.astype('category')
df['user_id'] = df['user_id'].astype('category').cat.codes.astype('category')
df['category_id'] = df['category_id'].astype('category').cat.codes.astype('category')
df['product_id'] = df['product_id'].astype('category').cat.codes.astype('category')


print(df.shape)
df.head()


# In[ ]:




## categorical/label encoding of the IDs (instead of string - save memory/file size):
### we still need to define ats categoircal due to the concatenation of the input files
df['user_session'] = df['user_session'].astype('category').cat.codes.astype('category')
df['user_session'] = df['user_session'].astype('category').cat.codes.astype('category')
df['user_id'] = df['user_id'].astype('category').cat.codes.astype('category')
df['category_id'] = df['category_id'].astype('category').cat.codes.astype('category')
df['product_id'] = df['product_id'].astype('category').cat.codes.astype('category')


# In[ ]:


df["event_type"].value_counts()


# In[ ]:


df["product_id"].value_counts().describe()


# In[ ]:


df.columns


# In[ ]:


df.drop(["event_time"],axis=1).nunique()


# # Target:
# * For each product the user viewed  or (depending on problem definition) added to cart , get combinations and predict if there was purchase.
# * Additional possible proxy target - did user add item to cart.
# 
# 
# * Q: Do we want to consider multiple user purchases of the same item? If so then we would want to not drop duplicates across sessions. For now, we will assume that the defined session seperates the data ok
# 
# 
#     * https://stackoverflow.com/questions/42854801/including-missing-combinations-of-values-in-a-pandas-groupby-aggregation
#     
#     
# * get all conbinations then fillna 0 :
#     * https://stackoverflow.com/questions/31786881/adding-values-for-missing-data-combinations-in-pandas

# In[ ]:


## get all "positive events" , then later we'll add 0s
df_targets = df.loc[df["event_type"].isin(["cart","purchase"])].drop_duplicates(subset=['event_type', 'product_id',
                                                                                        'price', 'user_id',
                                                                                        'user_session'])

print(df_targets.shape)
df_targets.tail()


# In[ ]:


## not filtering by price (discount?) doesn't change much
df_targets.drop_duplicates(subset=['event_type', 'product_id', 'user_id', 'user_session']).shape[0]


# ## Target: For items added to basked: Predict if they will be purchased in that session
# 
# * Different from predicting if they will be purchased in the future
# * Much less class imbalance.
# * Ignore possible target of items being deleted from session
# 
# * Could also be modelled as recomender problem (+- explicit/implicit (`lightFM`)) /: 1 : added, -1: removed from shopping cart, 0: not purchased "yet" or not added to cart
# 
#     * https://stackoverflow.com/questions/31786881/adding-values-for-missing-data-combinations-in-pandas    * 

# In[ ]:


## ## could also do this with np.where  ;  or stack + inindex ; or with a join (on filtered rows containing purhcase and fillna(0))

# # df2["purchase"] = (df2["event_type"]=="purchase").astype(int)

# df2["purchase"] = np.where(df2["event_type"]=="purchase",1,0)

## https://stackoverflow.com/questions/48175172/assign-a-pandas-series-to-a-groupby-operation


# In[ ]:


## laziest option - add a row where purchased, groupby(max), then keep rows at time of added to cart

# df_targets["purchased"] = (df_targets["event_type"]=="purchase").astype(int) #np.where() ## only kept 1s - bug ..

df_targets["purchased"] = np.where(df_targets["event_type"]=="purchase",1,0)
print(df_targets.shape)
df_targets["purchased"].describe()


# In[ ]:


df_targets["purchased"] = df_targets.groupby(["user_session","product_id"])["purchased"].transform("max")
df_targets["purchased"].describe()


# In[ ]:


# keep only rows with the time of addition to cart  = time of prediction
## also, drop duplicates for cases of multiple purchases of same it or readding (only a small amount - a few hundred such cases)
df_targets = df_targets.loc[df_targets["event_type"]=="cart"].drop_duplicates(["user_session","product_id","purchased"])

print(df_targets.shape)
df_targets["purchased"].describe()


# ## optional: Feature engineering

# In[ ]:





# # Export

# In[ ]:


df.to_csv("ecom_cosmetics_timeSeries.csv.gz",index=False,compression="gzip")

# output a sample of targets for modelling speed
df_targets.drop(["event_type"],axis=1).sample(frac=0.35).to_csv("ecom_cosmetics_cart_purchase_labels.csv.gz",index=False,compression="gzip")

