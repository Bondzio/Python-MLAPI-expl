#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# Fuel economy is measured in mpg miles per gallon in automobile industry. Fuel consumption is a relevant information that impacts areas such as economy or air pollution.
# 
# The purpose of this notebook is to predict mpg with K-fold, XGBoost and the mpg dataset.

# In[ ]:


import xgboost as xgb # extreme gradient boosting
import pandas as pd # data structures
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra, arrays
import seaborn as sns # statistical data visualization


# In[ ]:


df = pd.read_csv('../input/auto-mpg.csv')
df.head(5)


# **Data evaluation**

# In[ ]:


df.shape


# In[ ]:


df.sort_values('mpg',ascending=True).head(5)


# In[ ]:


df.sort_values('mpg',ascending=False).head(10)


# There are missing values in horsepower (renault lecar deluxe) and car name provides more information (diesel type)

# Remove incomplete rows

# In[ ]:


df.dtypes


# In[ ]:


df['horsepower'].unique()


# In[ ]:


df = df[df['horsepower'] != '?']


# In[ ]:


df['horsepower'] = df['horsepower'].astype('float')
df.dtypes


# Create new column for diesel type as it affects fuel consumption

# In[ ]:


df['diesel'] = (df['car name'].str.contains('diesel')).astype(int)


# In[ ]:


df.loc[df['diesel']==1]


# In[ ]:


df.shape


# In[ ]:


df.describe()


# **Data preparation**

# Split data into labels and features

# In[ ]:


labels = np.array(df['mpg'])
features = df.drop('mpg', axis=1)


# Create train (75%) and test (25%) sets

# In[ ]:


from sklearn.model_selection import train_test_split

(train_features_f,test_features_f,train_labels,test_labels) = train_test_split(features, 
                                                                               labels, 
                                                                               test_size=0.25, 
                                                                               random_state=4)


# Remove car name and diesel columns to have only continuous features

# In[ ]:


train_features_cont = train_features_f.drop(['car name','diesel'], axis=1)
test_features_cont = test_features_f.drop(['car name','diesel'], axis=1)


# Standarize continuous features and then add binary diesel column

# In[ ]:


from sklearn import preprocessing

scaler = preprocessing.StandardScaler().fit(train_features_cont)

train_features = np.append(scaler.transform(train_features_cont), 
                           train_features_f['diesel'][:,None], 
                           axis=1)
test_features = np.append(scaler.transform(test_features_cont), 
                          test_features_f['diesel'][:,None], 
                          axis=1)


# In[ ]:


print('Shapes')
print('Train features: {0} \nTrain labels: {1}'.format(train_features.shape,
                                                       train_labels.shape))
print('Test features: {0} \nTest labels: {1}'.format(test_features.shape,
                                                     test_labels.shape))


# **K-fold cross-validation**

# In[ ]:


from sklearn.model_selection import KFold
K = 4 # num splits
kf = KFold(n_splits=K)


# K-fold and XGBoost models. feature importance graphs are plot

# In[ ]:


from sklearn import metrics

xgb_predictions = []

for j, (train_index, val_index) in enumerate(kf.split(train_features)):
    partial_train_data,val_data = train_features[train_index],train_features[val_index]
    partial_train_targets,val_targets = train_labels[train_index],train_labels[val_index]

    feature_names=['cylinders','displacement','horsepower','weight',
                   'acceleration','model year','origin','diesel']
    
    d_train = xgb.DMatrix(partial_train_data, partial_train_targets, 
                          feature_names=feature_names)
    d_val = xgb.DMatrix(val_data, val_targets, feature_names=feature_names)
    d_test = xgb.DMatrix(test_features, feature_names=feature_names)
    
    watchlist = [(d_train, 'train'), (d_val, 'val')]
    
    xgb_params = {'min_child_weight': 1, 'eta': 0.3, 'colsample_bytree': 0.9, 
                  'max_depth': 3, 'subsample': 0.9, 'lambda': 1., 
                  'nthread': -1, 'booster' : 'gbtree', 'silent': 1,
                  'eval_metric': 'rmse', 'objective': 'reg:linear'}
    
    model = xgb.train(xgb_params, d_train, 100, watchlist, early_stopping_rounds=2,
                      maximize=False, verbose_eval=0)
    
    xgb_prediction = model.predict(d_test)
    
    xgb_predictions.append(list(xgb_prediction))
    
    print('Fold {0} rmse: {1}'.format(j+1,np.sqrt(metrics.mean_squared_error(xgb_prediction, 
                                                                             test_labels))))
    
    xgb.plot_importance(model, height=0.7) 


# **mpg predicitons**

# In[ ]:


preds = [np.mean([x[i] for x in xgb_predictions]) for i in range(len(xgb_predictions[0]))]

results = pd.DataFrame({'car name': test_features_f['car name'], 
                        'label mpg': test_labels, 
                        'prediction': preds})


# In[ ]:


results.head(10)


# oldsmobile cutlass ciera (diesel) has a mpg of 38, quite far from predicted 23. Research on internet shows combined mpg is 26 for this car, not 38
