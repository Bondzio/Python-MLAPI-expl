#!/usr/bin/env python
# coding: utf-8

# ## Satander Predict Value Challenge

# We do here basic preprocessing, feature selection and modelling.

# In[ ]:


#Various imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_selection import RFE, SelectFromModel,mutual_info_regression,VarianceThreshold
from sklearn.metrics import mean_squared_log_error,accuracy_score
from sklearn.decomposition import PCA
from lightgbm import LGBMRegressor
import zipfile
from sklearn.model_selection import train_test_split
from tqdm import tqdm 
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
sns.set_style('whitegrid')


# In[ ]:


# data import 
df_train = pd.read_csv('../input/train.csv')


# ### Data exploration

# The data is composed of only numerical features

# In[ ]:


df_train.head()


# A large part of algorithm compute distance, so it is necessary to bring all features to some even playing ground. If not, too large features will have a greater impact on the prediction than tiny features, which maybe contains important information.

# In[ ]:


#scale data using Min Max scaler
scaler = MinMaxScaler()
df_train[df_train.columns[2:]] = scaler.fit_transform(df_train[df_train.columns[2:]])
df_train.head()


# In[ ]:


# No missing data 
print(df_train.isnull().any().value_counts())


# Use Log on the target, we don't really care about the exact transaction value, but mostly about the general volume. The Log transform the target column to more grouped values.

# In[ ]:


X = df_train.drop(['ID','target'],axis=1)
y = np.log1p(df_train.target)
# y = df_train.target


# Some features have the same value for all entries, meaning they do not carry any information, we can drop them.

# In[ ]:


#complete zeros feature
# There is a lot of columns that are always the same value, drop them
# col_drop = X.iloc[:,np.where(np.all(X==0,axis=0) == True)[0]].columns
# X = X.drop(col_drop.values,axis=1)

# def drop_novar(X):
#     col_drop = X.columns[X.nunique() == 1]
#     X_dropped = X.drop(col_drop,axis=1)
#     return X_dropped
# X = drop_novar(X)
# print(X.shape)


# ### Feature selection and Modelling

# In[ ]:


def run_rf(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=500,n_jobs=-1)
    rf.fit(X_train,y_train)
    pred_test = rf.predict(X_test)
    pred_train = rf.predict(X_train)
    print('Test error: ',mean_squared_log_error(y_test,pred_test))
    print('Train error: ',mean_squared_log_error(y_train,pred_train))
    print('Test error: ',mean_squared_log_error(np.expm1(y_test),np.expm1(pred_test)))
    return rf 

def run_lgb(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lgb = LGBMRegressor(n_estimators=1500,n_jobs=-1,max_depth=10,learning_rate=0.005,metric='rmse')
    lgb.fit(X_train,y_train)
    pred_test = lgb.predict(X_test)
    pred_train = lgb.predict(X_train)
    print('Test error: ',mean_squared_log_error(y_test,pred_test))
    print('Train error: ',mean_squared_log_error(y_train,pred_train))
    print('Test error: ',mean_squared_log_error(np.expm1(y_test),np.expm1(pred_test)))
    return lgb

def custom_select(model,X,num_features):
    #credit to https://www.kaggle.com/alexpengxiao/preprocessing-model-averaging-by-xgb-lgb-1-39
    col = pd.DataFrame({'importance': model.feature_importances_, 'feature': X.columns}).sort_values(
                        by=['importance'], ascending=False)[:num_features]['feature'].values
    return X[col]

def plot_imp(model):
    imp = sorted(model.feature_importances_,reverse=True)
    plt.figure(figsize=(15,6)) # tune this to your aesthetical preference :)
    sns.lineplot(np.array(range(len(imp))),imp)
    plt.title('Feature importance plot')
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.show()


# In[ ]:


# run lgb on all features
get_ipython().run_line_magic('time', 'lgb_all = run_lgb(X,y)')


# In[ ]:


plot_imp(lgb_all)


# We can see that most of the features are not addding any value to the prediction, a lot of features are not even considered by the model. Let's select 1200 most important features

# In[ ]:


#run lgb on 1200 selected
X4 = custom_select(lgb_all,X,1200)
print(X4.shape)

get_ipython().run_line_magic('time', 'lgb_select = run_lgb(X4,y)')


# We reduced the compuation time significantly ! and didn't lose so much accuracy.

# In[ ]:


plot_imp(lgb_select)


# We can also ask sklearn to do it for us, using SelectFromModel function. It is implemented for every model that has a coef_ or a feature_importance_ attribute

# In[ ]:


# run on feature selected by SKLEARN
model = SelectFromModel(lgb_all, prefit=True)
X3 = model.transform(X)
print(X3.shape)
get_ipython().run_line_magic('time', 'lgb_select2 = run_lgb(X3,y)')


# In[ ]:


plot_imp(lgb_select2)


# PCA is a nice way to reduce the feature space, it transforms the feature space while maximizing the variance of the data. We guess there is approximately 1200 main features but this value can be tuned according to the empirical data. Note that after PCA you do not have the same features than before, but some kind of decomposition of the feature matrix into principal components. We try this to catch the most information we can from the features.

# In[ ]:


# select 1200 best features using PCA
pca = PCA(n_components=900)
X_pca = pca.fit_transform(X)
X_pca.shape


# In[ ]:


get_ipython().run_line_magic('time', 'lgb_pca = run_lgb(X_pca,y)')


# In[ ]:


plot_imp(lgb_pca)


# We can also select features by thresholding the variance. Here it is only filtering so we keep the same features than before

# In[ ]:


#compute var 
var_ser = np.var(X,axis=0)

plt.figure(figsize=(12,6))
sns.lineplot(np.array(range(len(var_ser))),sorted(var_ser))
plt.title('Variance plot')
plt.xlabel('Features')
plt.ylabel('Variance')
plt.show()


# In[ ]:


#filtering by variance, choose the threshold wisely
col_var = var_ser[var_ser >= 0.0005].index.values
X_var = X[col_var]
print(X_var.shape)


# In[ ]:


#run lgb on variance selected features
get_ipython().run_line_magic('time', 'lgb_var = run_lgb(X_var,y)')


# In[ ]:


plot_imp(lgb_var)


# The big winner of this part is SelectFromModel function that optimize the feature selection and computation time.

# Statistical features

# In[ ]:


def add_stat_feat(X):
    X['mean'] = np.mean(X,axis=1)
    X['median'] = np.median(X,axis=1)
    X['std']  = np.std(X,axis=1)
    X['max'] = np.max(X,axis=1)
    X['min'] = np.min(X,axis=1)
    X['skew'] = X.skew(axis=1)
    X['kurtosis'] = X.kurtosis(axis=1)
    return X


# In[ ]:


X = add_stat_feat(X)
lgb_ex = run_lgb(X,y)


# In[ ]:


model2 = SelectFromModel(lgb_ex, prefit=True)
X4 = model2.transform(X)
print(X4.shape)
get_ipython().run_line_magic('time', 'lgb_select3 = run_lgb(X4,y)')


# ### Submission

# In[ ]:


# load data in chunks 
best_model = lgb_select3
chunk_size = 1000
test = pd.read_csv(('../input/test.csv'),chunksize=chunk_size)
    
preds = []
IDs = []
for chunk in test:
    chunk[chunk.columns[1:]] = scaler.fit_transform(chunk.drop('ID',axis=1))
    features = model2.transform(add_stat_feat(chunk.drop('ID',axis=1)))
    preds = np.append(preds,best_model.predict(features))
    IDs += list(chunk['ID'])


# In[ ]:


sub_pred = np.expm1(preds)
sub = pd.DataFrame()
sub['ID'] = IDs
sub['target'] = sub_pred
sub.to_csv('submission.csv',index=False)

