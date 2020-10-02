#!/usr/bin/env python
# coding: utf-8

# # RAPIDS KNN categorial average predicted Distance, can it be used as features?
# Reference: https://www.kaggle.com/cdeotte/rapids-knn-30-seconds-0-938

# In[ ]:


import sys
get_ipython().system('cp ../input/rapids/rapids.0.12.0 /opt/conda/envs/rapids.tar.gz')
get_ipython().system('cd /opt/conda/envs/ && tar -xzvf rapids.tar.gz > /dev/null')
sys.path = ["/opt/conda/envs/rapids/lib/python3.6/site-packages"] + sys.path
sys.path = ["/opt/conda/envs/rapids/lib/python3.6"] + sys.path
sys.path = ["/opt/conda/envs/rapids/lib"] + sys.path 
get_ipython().system('cp /opt/conda/envs/rapids/lib/libxgboost.so /opt/conda/lib/')


# In[ ]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.stats import mode
from sklearn.metrics import f1_score, accuracy_score
from cuml.neighbors import KNeighborsClassifier, NearestNeighbors
# import cuml; cuml.__version__

def batching(df, batch_size):
    df['group'] = df.groupby(df.index//batch_size, sort=False)['signal'].agg(['ngroup']).values
    df['group'] = df['group'].astype(np.uint16)
    return df



def read_data():
    train = pd.read_csv('/kaggle/input/data-without-drift/train_clean.csv', dtype={'time': np.float32, 'signal': np.float32, 'open_channels':np.int32})
    test  = pd.read_csv('/kaggle/input/data-without-drift/test_clean.csv', dtype={'time': np.float32, 'signal': np.float32})
    return train, test

def lag_data(df):
    df['fut_3']=df.groupby('group')['signal'].shift(-3)*0.25
    df['fut_3']=df.groupby('group')['signal'].shift(-2)*0.5
    df['fut_1']=df.groupby('group')['signal'].shift(-1)*1.0
    df['current']=df['signal']*4.0
    df['lag_1']=df.groupby('group')['signal'].shift(1)*1.0
    df['lag_2']=df.groupby('group')['signal'].shift(2)*0.5
    df['lag_3']=df.groupby('group')['signal'].shift(3)*0.25
    return df

batch = 1000


train, test = read_data()
train=batching(train,batch)
test=batching(test,batch)
train=lag_data(train)
test=lag_data(test)

all_groups=train.group.unique()
np.random.shuffle(all_groups)
group_num=len(all_groups)

features=['fut_3', 'fut_1', 'current','lag_1', 'lag_2', 'lag_3']
print('done')


# In[ ]:


get_ipython().run_cell_magic('time', '', "\nKNN = 100\n\nfor g in range(5):\n    print('Infering group %i'%g)\n    \n    # TRAIN DATA\n    data = train[~train.group.isin(all_groups[int(group_num/5*g):int(group_num/5*(g+1))])]\n    X_train = data[features].values\n    y_train = data.open_channels.values\n\n    # TRAIN PRE\n    data = train[train.group.isin(all_groups[int(group_num/5*g):int(group_num/5*(g+1))])]\n    X_train_pre_all=data.values\n    X_train_pre = data[features].values\n    y_train_pre = data.open_channels.values\n    \n    # TEST\n    data = test\n    X_test_all=data.values\n    X_test = data[features].values\n    \n    print('data all set')\n    model = NearestNeighbors(n_neighbors=KNN)\n    model.fit(X_train)\n    print('model fitted')\n    \n    distances, indices=model.kneighbors(X_train_pre)\n    print('xtrain predicted')\n\n    temp=y_train[indices.astype(int)]\n    for i in range(11):\n        temp_re=np.array(distances*[temp==i][0]).mean(axis=1)\n        temp_re=temp_re.reshape(temp_re.shape[0],1)\n        if i!=0:\n            train_pre_temp=np.hstack((train_pre_temp,temp_re))\n        else:\n            train_pre_temp=np.hstack((X_train_pre_all,temp_re))\n    train_pre_temp=np.hstack((train_pre_temp,y_train_pre.reshape(y_train_pre.shape[0],1)))\n    \n    try:train_pre=np.vstack((train_pre,train_pre_temp))\n    except:train_pre=train_pre_temp\n    print('xtrain stacked')\n    \n    distances, indices=model.kneighbors(X_test)\n    print('xtest predicted')\n    temp=y_train[indices.astype(int)]\n    for i in range(11):\n        temp_re=np.array(distances*[temp==i][0]).mean(axis=1)\n        temp_re=temp_re.reshape(temp_re.shape[0],1)\n        if i!=0:\n            test_pre_temp=np.hstack((test_pre_temp,temp_re))\n        else:\n            test_pre_temp=np.hstack((X_test_all,temp_re))\n    \n    try:test_pre=np.vstack((test_pre,test_pre_temp))\n    except:test_pre=test_pre_temp\n    print('xtest stacked')\n    \n    ")


# In[ ]:


# temp=y_train[indices.astype(int)]
# for i in range(11):
#     temp_re=np.array(distances*[temp==i][0]).mean(axis=1)
#     temp_re=temp_re.reshape(temp_re.shape[0],1)
#     if i!=0:
#         train_pre_temp=np.hstack((train_pre_temp,temp_re))
#     else:
#         train_pre_temp=np.hstack((X_train_pre_all,temp_re))
# train_pre_temp=np.hstack((train_pre_temp,y_train_pre.reshape(y_train_pre.shape[0],1)))

# try:train_pre=np.vstack((train_pre,train_pre_temp))
# except:train_pre=train_pre_temp
# print('xtrain stacked')

# distances, indices=model.kneighbors(X_test)
# print('xtest predicted')
# temp=y_train[indices.astype(int)]
# for i in range(11):
#     temp_re=np.array(distances*[temp==i][0]).mean(axis=1)
#     temp_re=temp_re.reshape(temp_re.shape[0],1)
#     if i!=0:
#         test_pre_temp=np.hstack((test_pre_temp,temp_re))
#     else:
#         test_pre_temp=np.hstack((X_test,temp_re))

# try:test_pre=np.vstack((test_pre,test_pre_temp))
# except:test_pre=test_pre_temp
# print('xtest stacked')



# In[ ]:


# temp=['ave_distance_%s'%x for x in range(11)]
# col=['time', 'signal', 'open_channels', 'group', 'fut_3', 'fut_1', 'current','lag_1', 'lag_2', 'lag_3']+temp+['open_channels']
# col


# In[ ]:


# temp=y_train[indices.astype(int)]
# for i in range(11):
#     temp_re=np.array(distances*[temp==i][0]).mean(axis=1)
#     temp_re=temp_re.reshape(temp_re.shape[0],1)
#     if i!=0:
#         train_pre_temp=np.hstack((train_pre_temp,temp_re))
#     else:
#         train_pre_temp=np.hstack((X_train_pre_all,temp_re))
# train_pre_temp=np.hstack((train_pre_temp,y_train_pre.reshape(y_train_pre.shape[0],1)))

# try:train_pre=np.vstack((train_pre,train_pre_temp))
# except:train_pre=train_pre_temp
# print('xtrain stacked')


# In[ ]:


part_len=int(len(test_pre)/5)
test_pre_temp=test_pre[:part_len]
for i in range(1,5):
    test_pre_temp+=test_pre[part_len*i:part_len*(i+1)]
test_pre_temp/=5


# In[ ]:


np.save('knn_y_prob_train.npy',train_pre)
np.save('knn_y_prob_test.npy',test_pre_temp)


# In[ ]:


# sub = pd.read_csv('../input/liverpool-ion-switching/sample_submission.csv')
# sub.open_channels = test_predtest_pred
# sub.to_csv('submission.csv',index=False,float_format='%.4f')

# res=200
# plt.figure(figsize=(20,5))
# plt.plot(sub.time[::res],sub.open_channels[::res])
# plt.show()

