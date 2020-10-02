#!/usr/bin/env python
# coding: utf-8

# <h1 align="center" style="color:#6699ff"> DataCamp IEEE Fraud Detection </h1>

# <h1 align="center" style="color:#6699ff"> IEEE Data Minification </h1>

# <img src="https://github.com/DataCampM2DSSAF/suivi-du-data-camp-equipe-tchouacheu_toure_niang_chokki/blob/master/img/credit-card-fraud-detection.png?raw=true" width="800" align="right">

# #  <a style="color:#6699ff"> Team </a>
# - <a style="color:#6699ff">Mohamed NIANG </a>
# - <a style="color:#6699ff">Fernanda Tchouacheu </a>
# - <a style="color:#6699ff">Hypolite Chokki </a>

# # <a style="color:#6699ff">  Table of Contents</a> 
# 
# <a style="color:#6699ff"> I. Load Data</a>
# 
# <a style="color:#6699ff"> II. Memory Reducing</a>
# 
# <a style="color:#6699ff"> III. Lablel Encode</a>
# 
# <a style="color:#6699ff"> IV. Data Minification</a>

# # <a style="color:#6699ff"> I. Load Data</a>

# In[ ]:


# General imports
import numpy as np
import pandas as pd
import os, warnings, datetime, math

from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')

os.chdir('/kaggle/input/ieeecis-fraud-detection') # Set working directory
print(os.listdir('/kaggle/input/ieeecis-fraud-detection'))


# In[ ]:


# Data load
train_df = pd.read_csv('train_transaction.csv')
test_df = pd.read_csv('test_transaction.csv')
test_df['isFraud'] = 0

train_identity = pd.read_csv('train_identity.csv')
test_identity = pd.read_csv('test_identity.csv')

print('Load Data')


# # <a style="color:#6699ff"> II. Memory Reducing</a>

# In[ ]:


# Memory Reducer
def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2    
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)    
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df


# In[ ]:


# Base check

for df in [train_df, test_df, train_identity, test_identity]:
    original = df.copy()
    df = reduce_mem_usage(df)

    for col in list(df):
        if df[col].dtype!='O':
            if (df[col]-original[col]).sum()!=0:
                df[col] = original[col]
                print('Bad transformation', col)


# # <a style="color:#6699ff"> III. Label Encode</a>

# In[ ]:


# card4, card6, ProductCD
# Converting Strings to ints(or floats if nan in column) using frequency encoding
# We will be able to use these columns as category or as numerical feature

for col in ['card4', 'card6', 'ProductCD']:
    print('Encoding', col)
    temp_df = pd.concat([train_df[[col]], test_df[[col]]])
    col_encoded = temp_df[col].value_counts().to_dict()   
    train_df[col] = train_df[col].map(col_encoded)
    test_df[col]  = test_df[col].map(col_encoded)
    print(col_encoded)


# In[ ]:


# M columns
# Converting Strings to ints(or floats if nan in column)

for col in ['M1','M2','M3','M5','M6','M7','M8','M9']:
    train_df[col] = train_df[col].map({'T':1, 'F':0})
    test_df[col]  = test_df[col].map({'T':1, 'F':0})

for col in ['M4']:
    print('Encoding', col)
    temp_df = pd.concat([train_df[[col]], test_df[[col]]])
    col_encoded = temp_df[col].value_counts().to_dict()   
    train_df[col] = train_df[col].map(col_encoded)
    test_df[col]  = test_df[col].map(col_encoded)
    print(col_encoded)


# # <a style="color:#6699ff"> IV. Data Minification</a>

# In[ ]:


def train_minify_identity_df(df):

    df['id_12'] = df['id_12'].map({'Found':1, 'NotFound':0})
    df['id_15'] = df['id_15'].map({'New':2, 'Found':1, 'Unknown':0})
    df['id_16'] = df['id_16'].map({'Found':1, 'NotFound':0})

    df['id_23'] = df['id_23'].map({'TRANSPARENT':4, 'IP_PROXY':3, 'IP_PROXY:ANONYMOUS':2, 'IP_PROXY:HIDDEN':1})

    df['id_27'] = df['id_27'].map({'Found':1, 'NotFound':0})
    df['id_28'] = df['id_28'].map({'New':2, 'Found':1})

    df['id_29'] = df['id_29'].map({'Found':1, 'NotFound':0})

    df['id_35'] = df['id_35'].map({'T':1, 'F':0})
    df['id_36'] = df['id_36'].map({'T':1, 'F':0})
    df['id_37'] = df['id_37'].map({'T':1, 'F':0})
    df['id_38'] = df['id_38'].map({'T':1, 'F':0})

    df['id_34'] = df['id_34'].fillna(':0')
    df['id_34'] = df['id_34'].str.split(':',1).notnull().astype(np.int8)
    df['id_34'] = np.where(df['id_34']==0, np.nan, df['id_34'])
    
    df['id_33'] = df['id_33'].fillna('0x0')
    df['id_33_0'] = df['id_33'].apply(lambda x: x.split('x')[0]).astype(int)
    df['id_33_1'] = df['id_33'].apply(lambda x: x.split('x')[1]).astype(int)
    df['id_33'] = np.where(df['id_33']=='0x0', np.nan, df['id_33'])

    df['DeviceType'].map({'desktop':1, 'mobile':0})
    return df


# In[ ]:


train_identity = train_minify_identity_df(train_identity)


# In[ ]:


# Identity columns

def test_minify_identity_df(df):
    
    df['DeviceType'].map({'desktop':1, 'mobile':0})
    return df


# In[ ]:


test_identity = test_minify_identity_df(test_identity)


# In[ ]:


for col in ['id_33']:
    train_identity[col] = train_identity[col].fillna('unseen_before_label')  
    
    le = LabelEncoder()
    le.fit(list(train_identity[col]))
    train_identity[col] = le.transform(train_identity[col])


# In[ ]:


# Final check

for df in [train_df, test_df, train_identity, test_identity]:
    original = df.copy()
    df = reduce_mem_usage(df)

    for col in list(df):
        if df[col].dtype!='O':
            if (df[col]-original[col]).sum()!=0:
                df[col] = original[col]
                print('Bad transformation', col)


# In[ ]:


# Full minification for fast tests

for df in [train_df, test_df, train_identity, test_identity]:
    df = reduce_mem_usage(df)


# In[ ]:


# Export

train_df.to_pickle('/kaggle/working/train_transaction.pkl')
test_df.to_pickle('/kaggle/working/test_transaction.pkl')

train_identity.to_pickle('/kaggle/working/train_identity.pkl')
test_identity.to_pickle('/kaggle/working/test_identity.pkl')

