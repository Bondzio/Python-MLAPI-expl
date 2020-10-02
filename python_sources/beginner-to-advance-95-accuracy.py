#!/usr/bin/env python
# coding: utf-8

# # Contents:
# 
# 1. Import Libraries
# 2. Import DataSets
# 3. Handle Missing Value
# 4. Exploratory Data Analysis(EDA)
# 5. Feature selection
# 6. Feature Engineering
# 7. Train Xgboost Classifier
# 8. Artificial Intelligence
# 
# XgBoost - 92% Accuracy, AI - 95% Accuracy
# 
# **check my beginners nodebook to know why i aaplied feature enginnering and Xgboost Classifier:**
# [Beginners Notebook-90% Accuracy][1] 
# 
# [1]: https://www.kaggle.com/harshkothari21/beginners-notebook-90-accuracy

# # Import Libraries

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
plt.style.use('seaborn')


# # Import Datasets

# In[ ]:


train = pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')
test = pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')
y = train['SalePrice']


# In[ ]:


train.shape


# In[ ]:


test.shape


# # Handle Missing Values

# In[ ]:


sns.heatmap(train.isnull(),yticklabels=False, cmap='plasma')


# In[ ]:


train.isnull().sum().sort_values(ascending=False)[0:19]


# In[ ]:


test.isnull().sum().sort_values(ascending=False)[0:33]


# ### Drop columns with too much missing values
# Plus there is so much features to analyse that it may be better to concentrate on the ones which can give us real insights. Also I tried including these features in model but score was not up do the mark

# In[ ]:


columns = ['Alley', 'MiscFeature', 'Fence', 'GarageYrBlt']

train.drop(columns=columns, inplace=True)
test.drop(columns=columns, inplace=True)
train['PoolQC'] = train['PoolQC'].fillna('None')
test['PoolQC'] = test['PoolQC'].fillna('None')

train.drop(columns=['Id'], inplace=True)


# ### Use mean for filling null values for numerical features

# In[ ]:


columns = ['LotFrontage', 'GarageCars', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF',  'TotalBsmtSF', 'GarageArea']

for item in columns:
    train[item] = train[item].fillna(train[item].mean())
    test[item] = test[item].fillna(test[item].mean())


# ### Use mode for filling null values for categorical features

# In[ ]:


columns = ['BsmtCond', 'BsmtQual', 'FireplaceQu', 'GarageType', 'GarageCond', 'GarageFinish', 'GarageQual', 'MSZoning',
           'MasVnrType', 'MasVnrArea', 'BsmtExposure','BsmtFinType2', 'BsmtFinType1', 'Electrical',  'Utilities',
           'BsmtFullBath', 'BsmtHalfBath', 'Functional', 'SaleType', 'Exterior2nd', 'Exterior1st', 'KitchenQual']

for item in columns:
    train[item] = train[item].fillna(train[item].mode()[0])
    test[item] = test[item].fillna(test[item].mode()[0])


# ### Checking for missing values if any!

# In[ ]:


train.isnull().any().any()


# In[ ]:


test.isnull().any().any()


# # Exploratory Data Analysis(EDA)

# In[ ]:


sns.distplot(train['SalePrice'], bins=100);


# With this information we can see that the prices are skewed right and some outliers lies above ~500,000. We will eventually want to get rid of the them to get a normal distribution of the independent variable (`SalePrice`) for machine learning.

# **Data Frame with only numerical features**

# In[ ]:


df_num = train.select_dtypes(include = ['float64', 'int64'])
df_num.head()


# ### Take Top strongly correlated values with SalePrice:
# 
# **I tried Selecting Top 10 features and trained my model but score was not up to the mark**

# In[ ]:


df_num_corr = df_num.corr()['SalePrice'][:-1]
golden_features_list = df_num_corr[abs(df_num_corr) >= 0].sort_values(ascending=False)
golden_features_list


# Correlation by itself does not always explain the relationship between data so ploting them could even lead us to new insights and in the same manner, check that our correlated values have a linear relationship to the `SalePrice`.

# In[ ]:


for i in range(0, len(df_num.columns), 5):
    sns.pairplot(data=df_num,
                x_vars=df_num.columns[i:i+5],
                y_vars=['SalePrice'])


# if we look closely at the data we can see that a lot of data points are located on `x = 0` which may indicate the absence of such feature in the house.

# ### Let's examine feature by correlation matrix

# In[ ]:


corr = df_num.drop('SalePrice', axis=1).corr() # We already examined SalePrice correlations
plt.figure(figsize=(12, 10))

sns.heatmap(corr[(corr >= 0.5) | (corr <= -0.4)], 
            cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
            annot=True, annot_kws={"size": 8}, square=True);


# **Let's examine Non Numerical Features**

# In[ ]:


df_not_num = train.select_dtypes(include = ['O'])


# In[ ]:


fig, axes = plt.subplots(round(len(df_not_num.columns) / 3), 3, figsize=(12, 30))

for i, ax in enumerate(fig.axes):
    if i < len(df_not_num.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=df_not_num.columns[i], alpha=0.7, data=df_not_num, ax=ax)

fig.tight_layout()


# We can see that some categories are predominant for some features such as `Utilities`, `Heating`, `GarageCond`, `Functional`... These features may not be relevant for our predictive model

# Let's Just exclude that features from our model

# In[ ]:


golden_features_list1 = list(df_not_num.columns)


# In[ ]:


excluded_features = ['GarageCond', 'Functional', 'Heating', 'BsmtFinType2', 'RoofMatl', 'Street', 'Utilities']

for item in excluded_features:
    golden_features_list1.remove(item)


# # Feature selection

# In[ ]:


golden_features_list = list(golden_features_list.index)


# In[ ]:


golden_features_list.extend(golden_features_list1)


# In[ ]:


train = train[golden_features_list]


# In[ ]:


test = test[golden_features_list]


# # Feature Engineering

# We will be using onehot encoding technique for feature engineering 

# In[ ]:


final_df = pd.concat([train, test], axis=0)


# In[ ]:


final_df.shape


# **Ensuring null values is any**

# In[ ]:


final_df.isnull().any().any()


# In[ ]:


def One_hot_encoding(columns):
    df_final=final_df
    i=0
    for fields in columns:
        df1=pd.get_dummies(final_df[fields],drop_first=True)
        
        final_df.drop([fields],axis=1,inplace=True)
        if i==0:
            df_final=df1.copy()
        else:           
            df_final=pd.concat([df_final,df1],axis=1)
        i=i+1
       
        
    df_final=pd.concat([final_df,df_final],axis=1)
        
    return df_final


# In[ ]:


df_final = One_hot_encoding(golden_features_list1)


# In[ ]:


df_final.shape


# In[ ]:


df_final = df_final.loc[:,~df_final.columns.duplicated()]


# In[ ]:


df_final.shape


# In[ ]:


df_Train=df_final.iloc[:1460,:]
df_Test=df_final.iloc[1460:,:]


# In[ ]:


my_temp = pd.concat([df_Train,y],axis=1)
#my_temp.to_csv('train_conv_1.csv',index=False)
#df_Test.to_csv('test_conv_1.csv',index=False)


# # Train Xgboost Classifier

# In[ ]:


import xgboost


# ### If you want know how I selected best parameter for XgBosst(HyperParameter Tunning): 
# 
# [Beginners Notebook-90% Accuracy][1] 
# 
# [1]: https://www.kaggle.com/harshkothari21/beginners-notebook-90-accuracy

# In[ ]:


regressor = xgboost.XGBRegressor(base_score=0.25, booster='gbtree', colsample_bylevel=1,
             colsample_bynode=1, colsample_bytree=1, gamma=0, gpu_id=-1,
             importance_type='gain', interaction_constraints='',
             learning_rate=0.1, max_delta_step=0, max_depth=2,
             min_child_weight=1, missing=None, monotone_constraints='()',
             n_estimators=900, n_jobs=0, num_parallel_tree=1,
             objective='reg:squarederror', random_state=0, reg_alpha=0,
             reg_lambda=1, scale_pos_weight=1, subsample=1, tree_method='exact',
             validate_parameters=1, verbosity=None)


# In[ ]:


regressor.fit(df_Train,y);


# In[ ]:


y_pred = regressor.predict(df_Test)


# In[ ]:


y_pred


# In[ ]:


pred=pd.DataFrame(y_pred)
samp = pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')
sub = pd.concat([samp['Id'],pred], axis=1)
sub.columns=['Id','SalePrice']


# In[ ]:


sub


# In[ ]:


#sub.to_csv('My_sub3.csv',index=False)


# # Artificial Intelligence
# 
# **Below csv files have all features with applied feature engineering. If you want to know in detail, check my notebook :**
# 
# [Beginners Notebook-90% Accuracy][1] 
# 
# [1]: https://www.kaggle.com/harshkothari21/beginners-notebook-90-accuracy

# In[ ]:


df_train = pd.read_csv('../input/my-data/train_conv.csv')
df_test = pd.read_csv('../input/my-data/test_conv.csv')


# In[ ]:


sub.drop(['Id'],axis=1, inplace=True)
df_Test=pd.concat([df_test,sub],axis=1)


# In[ ]:


df_Train=pd.concat([df_train,df_Test],axis=0)


# In[ ]:


X_train=df_Train.drop(['SalePrice'],axis=1)
y_train=df_Train['SalePrice']


# In[ ]:


from keras import backend as K
def root_mean_squared_error(y_true, y_pred):
        return K.sqrt(K.mean(K.square(y_pred - y_true)))


# In[ ]:


import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LeakyReLU,PReLU,ELU
from keras.layers import Dropout


# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(output_dim = 50, init = 'he_uniform',activation='relu',input_dim = 174))

# Adding the second hidden layer
classifier.add(Dense(output_dim = 25, init = 'he_uniform',activation='relu'))

# Adding the third hidden layer
classifier.add(Dense(output_dim = 50, init = 'he_uniform',activation='relu'))
# Adding the output layer
classifier.add(Dense(output_dim = 1, init = 'he_uniform'))

# Compiling the ANN
classifier.compile(loss=root_mean_squared_error,optimizer='Adamax')

# Fitting the ANN to the Training set
model_history=classifier.fit(X_train.values, y_train.values,validation_split=0.20, batch_size = 10, nb_epoch = 1000)


# In[ ]:


ann_pred=classifier.predict(df_Test.drop(['SalePrice'],axis=1).values)


# In[ ]:


ann_pred


# In[ ]:


ann_pred=pd.DataFrame(ann_pred)
samp = pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')
sub = pd.concat([samp['Id'],ann_pred], axis=1)
sub.columns=['Id','SalePrice']


# In[ ]:


#sub.to_csv('My_sub_final.csv',index=False)

