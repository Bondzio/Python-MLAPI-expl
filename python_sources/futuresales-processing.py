#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load


get_ipython().run_line_magic('matplotlib', 'inline')
import itertools
from time import sleep

import gc
from pathlib2 import Path
from tqdm import tqdm_notebook

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:



items = pd.read_csv('../input/competitive-data-science-predict-future-sales/items.csv')
shops = pd.read_csv('../input/competitive-data-science-predict-future-sales/shops.csv')
item_categories = pd.read_csv('../input/competitive-data-science-predict-future-sales/item_categories.csv')
train = pd.read_csv('../input/competitive-data-science-predict-future-sales/sales_train.csv')
test  = pd.read_csv('../input/competitive-data-science-predict-future-sales/test.csv')
sample_submission=pd.read_csv('../input/competitive-data-science-predict-future-sales/sample_submission.csv')

groupby_cols = ['date_block_num', 'shop_id', 'item_id']


# In[ ]:


train[(train.shop_id == 32) & (train.item_id == 2973) & (train.date_block_num == 4) & (
            train.item_price > 0)].item_price.median()
train = train[train.item_price < 100000]
train = train[train.item_cnt_day < 1001]

median = train[(train.shop_id == 32) & (train.item_id == 2973) & (train.date_block_num == 4) & (
            train.item_price > 0)].item_price.median()
train.loc[train.item_price < 0, 'item_price'] = median


# In[ ]:


train.loc[train.shop_id == 0, 'shop_id'] = 57
test.loc[test.shop_id == 0, 'shop_id'] = 57
train.loc[train.shop_id == 1, 'shop_id'] = 58
test.loc[test.shop_id == 1, 'shop_id'] = 58
train.loc[train.shop_id == 10, 'shop_id'] = 11
test.loc[test.shop_id == 10, 'shop_id'] = 11


# In[ ]:


test['date_block_num'] = 34


# # **Adding new features**

# In[ ]:


category = items[['item_id', 'item_category_id']].drop_duplicates()
category.set_index(['item_id'], inplace=True)
category = category.item_category_id
train['category'] = train.item_id.map(category)
category
train


# In[ ]:


item_categories['meta_category'] = item_categories.item_category_name.apply(lambda x: x.split(' ')[0])
item_categories['meta_category'] = pd.Categorical(item_categories.meta_category).codes
item_categories.set_index(['item_category_id'], inplace=True)
meta_category = item_categories.meta_category
train['meta_category'] = train.category.map(meta_category)


# In[ ]:


train


# In[ ]:


shops['city'] = shops.shop_name.apply(lambda x: str.replace(x, '!', '')).apply(lambda x: x.split(' ')[0])
shops['city'] = pd.Categorical(shops['city']).codes
city = shops.city
train['city'] = train.shop_id.map(city)


# In[ ]:


year = pd.concat([train.date_block_num, train.date.apply(lambda x: int(x.split('.')[2]))], axis=1).drop_duplicates()
year.set_index(['date_block_num'], inplace=True)
year = year.date.append(pd.Series([2015], index=[34]))


# In[ ]:


month = pd.concat([train.date_block_num, train.date.apply(lambda x: int(x.split('.')[1]))], axis=1).drop_duplicates()
month.set_index(['date_block_num'], inplace=True)
month = month.date.append(pd.Series([11], index=[34]))


# In[ ]:


all_shops_items = []

for block_num in train['date_block_num'].unique():
    unique_shops = train[train['date_block_num'] == block_num]['shop_id'].unique()
    unique_items = train[train['date_block_num'] == block_num]['item_id'].unique()
    all_shops_items.append(np.array(list(itertools.product([block_num], unique_shops, unique_items)), dtype='int32'))

df = pd.DataFrame(np.vstack(all_shops_items), columns=groupby_cols, dtype='int32')
df = df.append(test, sort=True)


# In[ ]:


df['ID'] = df.ID.fillna(-1).astype('int32')
df['year'] = df.date_block_num.map(year)
df['month'] = df.date_block_num.map(month)
df['category'] = df.item_id.map(category)
df['meta_category'] = df.category.map(meta_category)
df['city'] = df.shop_id.map(city)
train['category'] = train.item_id.map(category)


# In[ ]:


df


# In[ ]:


get_ipython().run_cell_magic('time', '', "\ngb = train.groupby(by=groupby_cols, as_index=False).agg({'item_cnt_day': ['sum']})\ngb.columns = [val[0] if val[-1] == '' else '_'.join(val) for val in gb.columns.values]\ngb.rename(columns={'item_cnt_day_sum': 'target'}, inplace=True)\ndf = pd.merge(df, gb, how='left', on=groupby_cols)\n\ngb = train.groupby(by=['date_block_num', 'item_id'], as_index=False).agg({'item_cnt_day': ['sum']})\ngb.columns = [val[0] if val[-1] == '' else '_'.join(val) for val in gb.columns.values]\ngb.rename(columns={'item_cnt_day_sum': 'target_item'}, inplace=True)\ndf = pd.merge(df, gb, how='left', on=['date_block_num', 'item_id'])\n\ngb = train.groupby(by=['date_block_num', 'shop_id'], as_index=False).agg({'item_cnt_day': ['sum']})\ngb.columns = [val[0] if val[-1] == '' else '_'.join(val) for val in gb.columns.values]\ngb.rename(columns={'item_cnt_day_sum': 'target_shop'}, inplace=True)\ndf = pd.merge(df, gb, how='left', on=['date_block_num', 'shop_id'])\n\ngb = train.groupby(by=['date_block_num', 'category'], as_index=False).agg({'item_cnt_day': ['sum']})\ngb.columns = [val[0] if val[-1] == '' else '_'.join(val) for val in gb.columns.values]\ngb.rename(columns={'item_cnt_day_sum': 'target_category'}, inplace=True)\ndf = pd.merge(df, gb, how='left', on=['date_block_num', 'category'])\n\ngb = train.groupby(by=['date_block_num', 'item_id'], as_index=False).agg({'item_price': ['mean', 'max']})\ngb.columns = [val[0] if val[-1] == '' else '_'.join(val) for val in gb.columns.values]\ngb.rename(columns={'item_price_mean': 'target_price_mean', 'item_price_max': 'target_price_max'}, inplace=True)\ndf = pd.merge(df, gb, how='left', on=['date_block_num', 'item_id'])")


# In[ ]:


df['target_price_mean'] = np.minimum(df['target_price_mean'], df['target_price_mean'].quantile(0.99))
df['target_price_max'] = np.minimum(df['target_price_max'], df['target_price_max'].quantile(0.99))

df.fillna(0, inplace=True)
df['target'] = df['target'].clip(0, 20)
df['target_zero'] = (df['target'] > 0).astype('int32')


# In[ ]:


df


# In[ ]:


get_ipython().run_cell_magic('time', '', "\nfor enc_cols in [['shop_id', 'category'], ['shop_id', 'item_id'], ['shop_id'], ['item_id']]:\n\n    col = '_'.join(['enc', *enc_cols])\n    col2 = '_'.join(['enc_max', *enc_cols])\n    df[col] = np.nan\n    df[col2] = np.nan\n\n    for d in tqdm_notebook(df.date_block_num.unique()):\n        f1 = df.date_block_num < d\n        f2 = df.date_block_num == d\n\n        gb = df.loc[f1].groupby(enc_cols)[['target']].mean().reset_index()\n        enc = df.loc[f2][enc_cols].merge(gb, on=enc_cols, how='left')[['target']].copy()\n        enc.set_index(df.loc[f2].index, inplace=True)\n        df.loc[f2, col] = enc['target']\n\n        gb = df.loc[f1].groupby(enc_cols)[['target']].max().reset_index()\n        enc = df.loc[f2][enc_cols].merge(gb, on=enc_cols, how='left')[['target']].copy()\n        enc.set_index(df.loc[f2].index, inplace=True)\n        df.loc[f2, col2] = enc['target']\n")


# In[ ]:




def downcast_dtypes(df):
    float32_cols = [c for c in df if df[c].dtype == 'float64']
    int32_cols = [c for c in df if df[c].dtype in ['int64', 'int16', 'int8']]

    df[float32_cols] = df[float32_cols].astype(np.float32)
    df[int32_cols] = df[int32_cols].astype(np.int32)

    return df


# In[ ]:


df.fillna(0, inplace=True)
df = downcast_dtypes(df)


# In[ ]:



get_ipython().run_cell_magic('time', '', "\nshift_range = [1, 2, 3, 4, 5, 12]\n\nshifted_columns = [c for c in df if 'target' in c]\n\nfor shift in tqdm_notebook(shift_range):\n    shifted_data = df[groupby_cols + shifted_columns].copy()\n    shifted_data['date_block_num'] = shifted_data['date_block_num'] + shift\n\n    foo = lambda x: '{}_lag_{}'.format(x, shift) if x in shifted_columns else x\n    shifted_data = shifted_data.rename(columns=foo)\n\n    df = pd.merge(df, shifted_data, how='left', on=groupby_cols).fillna(0)\n    df = downcast_dtypes(df)\n\n    del shifted_data\n    gc.collect()\n    sleep(1)\n")


# In[ ]:


df['target_trend_1_2'] = df['target_lag_1'] - df['target_lag_2']
df['target_predict_1_2'] = df['target_lag_1'] * 2 - df['target_lag_2']

df['target_trend_3_4'] = df['target_lag_1'] + df['target_lag_2'] - df['target_lag_3'] - df['target_lag_4']
df['target_predict_3_4'] = (df['target_lag_1'] + df['target_lag_2']) * 2 - df['target_lag_3'] - df['target_lag_4']

df['target_item_trend_1_2'] = df['target_item_lag_1'] - df['target_item_lag_2']
df['target_item_trend_3_4'] = df['target_item_lag_1'] + df['target_item_lag_2'] - df['target_item_lag_3'] - df['target_item_lag_4']
df['target_shop_trend_1_2'] = df['target_shop_lag_1'] - df['target_shop_lag_2']
df['target_shop_trend_3_4'] = df['target_shop_lag_1'] + df['target_shop_lag_2'] - df['target_shop_lag_3'] - df['target_shop_lag_4']


# In[ ]:


df = downcast_dtypes(df)
df.to_pickle('df.pkl')


# In[ ]:




