#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

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


import pandas as pd
import numpy as np


# In[ ]:


def reduce_mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.        
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
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
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df


# In[ ]:


train_data_filepath = '../input/pubg-finish-placement-prediction/train_V2.csv'
train_data = pd.read_csv(train_data_filepath)
train_data = reduce_mem_usage(train_data)


# In[ ]:


test_data_filepath = '../input/pubg-finish-placement-prediction/test_V2.csv'
test_data = pd.read_csv(test_data_filepath)
test_data = reduce_mem_usage(test_data)


# In[ ]:


train_data.shape


# In[ ]:


test_data.shape


# In[ ]:


train_data.head()


# In[ ]:


test_data.head(5)


# In[ ]:


train_data.describe()


# In[ ]:


train_data.dtypes


# In[ ]:


train_data.isna().any()


# In[ ]:


train_data['Id'].nunique()


# In[ ]:


train_data['groupId'].nunique()


# In[ ]:


train_data['matchId'].nunique()


# In[ ]:


#Match Type : There are 3 Game Modes in the Game - Solo,Duo,Squad


# In[ ]:


train_data["matchType"]


# In[ ]:


train_data.groupby(["matchType"]).count()


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[ ]:


train_data.groupby('matchId')['matchType'].first().value_counts().plot.bar()


# In[ ]:


#Mapping


# In[ ]:


new_train_data = train_data
def mapthematch(data):
    mapping = lambda y:'solo' if ('solo' in y) else 'duo' if ('duo' in y) or ('crash' in y) else 'squad'
    data['matchType'] = data['matchType'].apply(mapping)
    return(new_train_data)
data = mapthematch(new_train_data)

data.groupby('matchId')['matchType'].first().value_counts().plot.bar()


# In[ ]:


#Finding a cheating match


# In[ ]:


data[data['winPlacePerc'].isnull()]


# In[ ]:


data.drop(2744604,inplace = True)
data[data['winPlacePerc'].isnull()]


# In[ ]:


data['matchType'].hist(bins=20)


# In[ ]:


data['matchDuration'].hist(bins=50)


# In[ ]:


#Minimum Match Duration

data['matchDuration'].min()


# In[ ]:


#Maximum Match Duration

data['matchDuration'].max()


# In[ ]:


#Normalizing the data

#Normalizing the Kills Column

data['killsNormalization'] = data['kills']*((100-data['kills'])/100 +1)


# In[ ]:


#Normalizing the Damage Dealt Column

data['damageDealtNormalization'] = data['damageDealt']*((100-data['damageDealt'])/100+1)


# In[ ]:


#Normalizing the MAX Place column

data['maxPlaceNormalization'] = data['maxPlace']*((100-data['maxPlace'])/100+1)


# In[ ]:


#Normalizing the Match Duration Column

data['matchDurationNormalization'] = data['matchDuration']*((100-data['matchDuration'])/100+1)


# In[ ]:


new_normalized_column = data[['Id','matchDuration','matchDurationNormalization','maxPlace','maxPlaceNormalization','kills','killsNormalization','damageDealt','damageDealtNormalization']]


# In[ ]:


new_normalized_column


# In[ ]:


#Total Distance Travelled

data['totalDistancetravelled'] = data['rideDistance'] + data['walkDistance'] + data['swimDistance']
data['totalDistancetravelled']


# In[ ]:


# Head Shot Feature

data['headshot_rate'] = data['headshotKills']/data['kills']
data['headshot_rate']


# In[ ]:


data


# In[ ]:


data['killswithoutMovinganytime'] = ((data['kills'] >0) & (data['totalDistancetravelled']==0))
data['killswithoutMovinganytime']


# In[ ]:


data[data['killswithoutMovinganytime']==True].shape


# In[ ]:


data[data['killswithoutMovinganytime']==True].head(5)


# In[ ]:


#Remove Outliers
data.drop(data[data['killswithoutMovinganytime']==True].index,inplace=True)


# In[ ]:


#Visualizing Longest Kill and try to find out what are the Outlier we have


# In[ ]:


import seaborn as sn

plt.figure(figsize=(14,8))
sn.distplot(data['longestKill'])
plt.show()


# In[ ]:


display(data[data['longestKill']>= 900].shape)
data[data['longestKill']>= 900].head(10)


# In[ ]:


#Removing Outliers
data.drop(data[data['longestKill']>= 900].index,inplace=True)


# In[ ]:


data.shape


# In[ ]:


data['winPlacePerc']


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# In[ ]:


data.columns


# In[ ]:


#thought of using damageDealtNormalization but it seems like it contains null values, So working these features
x = data[['Id','killsNormalization','maxPlaceNormalization','matchDurationNormalization','totalDistancetravelled']]
y = data['winPlacePerc']


# In[ ]:


train_X , test_X , train_y , test_y = train_test_split(x,y,test_size=0.2,random_state=42)


# In[ ]:


model = LinearRegression()
model.fit(train_X,train_y)


# In[ ]:


model.score(test_X,test_y)


# In[ ]:


predicted_vals = model.predict(test_X)


# In[ ]:


predicted_vals

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error
mae(predicted_vals,test_y)


# In[ ]:


from sklearn.neighbors import KNeighborsRegressor


# In[ ]:


neigh = KNeighborsRegressor(n_neighbors=30)
neigh.fit(train_X,train_y)


# In[ ]:


neigh.score(test_X,test_y)


# In[ ]:


pred_vals = neigh.predict(test_X)


# In[ ]:


mae(pred_vals,test_y)


# In[ ]:


output = pd.DataFrame({'Id' : test_y,'winPlacePerc' : pred_vals})
output


# In[ ]:


from sklearn import metrics
print('Mean Absolute Error:' , metrics.mean_absolute_error(pred_vals,test_y))
print('Mean Squared Error:' , metrics.mean_squared_error(pred_vals,test_y))


# In[ ]:


output.to_csv('submission.csv',index=False)


# In[ ]:




