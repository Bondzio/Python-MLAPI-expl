#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_profiling
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics


# In[ ]:


train_df = pd.read_csv('../input/train.csv')
test_df = pd.read_csv('../input/test.csv')
submission_df = pd.read_csv('../input/sample_submission.csv')


# In[ ]:


# Checking for outliers
plt.scatter(train_df.GrLivArea,train_df.SalePrice)
plt.xlabel('GrLiveArea')
plt.ylabel('SalePrice')
plt.title('Outliers')
plt.show()


# - with large space and less price is something mischiveous 
# - removing all the outliers is not recommended it may have impact on the output so lets make the model robust and regularize

# In[ ]:


train_df = train_df.drop(train_df[(train_df.GrLivArea > 4000)&(train_df.SalePrice < 300000)].index,axis=0)
target = train_df.SalePrice


# In[ ]:


# Checking for outliers
plt.scatter(train_df.GrLivArea,target)
plt.xlabel('GrLiveArea')
plt.ylabel('SalePrice')
plt.title('Outliers')
plt.show()


# In[ ]:


train_df.drop(['SalePrice'],axis=1,inplace=True)


# In[ ]:


# Lets concatenate Train and Test data to a dataframe df
df = pd.concat([train_df,test_df],axis=0)


# In[ ]:


df.head()


# In[ ]:


#Checking all the missing values in complete data
nullValue = pd.DataFrame(df.isnull().sum())
df.columns.map(lambda x : print(nullValue.loc[x]))


# #### As per the explanation from the document provided 
# - there are few columns in which NAN holds a meaning and  lets replace them with proper meaning
# - LotFrontage   :   this is a numeric field so lets fill it with the median
# - Alley         :   if NA then the meaning is no access lets fill it with No access
# - MasVnrType    :   if NA then its none type
# - MasVnrArea    :   Since this is an area numeric value if Na then we can fill it with 0
# - BsmtQual      :   fill with Nobase
# - BsmtCond      :   fill with Nobase
# - BsmtExposure  :   fill with Nobase
# - BsmtFinSF1    :   fill with zero
# - BsmtFinSF2    :   fill with zero
# - BsmtFinType1  :   fill with nobase
# - BsmtFinType2  :   fill with nobase
# - BsmtFullBath  :   fill with zero
# - BsmtHalfBath  :   fill with zero
# - BsmtUnfSF     :   fill with zero
# - Electrical    :   Since there is no meaning for NA lets fill /it with most occurence ie mode
# - Exterior1st   :   fill with Mode(frequent) or predictive
# - Exterior2nd   :   fill with Mode(frequent) or predictive
# - Functional    :   fill with Mode(frequent) or predictive
# - GarageArea    :   Fill with zero
# - GarageCars    :   fill with zero
# - FireplaceQu   :   fill with no fireplace
# - GarageType    :   fill with no garage
# - GarageYrBlt   :   lets use predictive imputing here
# - GarageFinish  :   fill with no garage
# - GarageQual    :   fill with No garage
# - GarageCond    :   fill with no garage
# - PoolQC        :   fill with no pool
# - Fence         :   fill with no fence
# - MiscFeature   :   fill none feature
# - KitchenQual   :   fill with Mode(frequent) or predictive
# - SaleType      :   fill with Mode
# - TotalBsmtSF   :   fill with zero
# - Utilities     :   fill with Mode
# 
# 

# ### Imputing Missing values

# In[ ]:


train_size = train_df.shape[0]
test_size = test_df.shape[0]
print(train_size,test_size)


# In[ ]:


# lets fill all Na's with meaning no such feature with a common term None because we can define a function .
def filla(feature,typo):
    '''typo define if the feature to be filled with none or 0'''
    df[feature].fillna('NONE',inplace=True) if typo else df[feature].fillna(0,inplace=True)


# In[ ]:


# lets fill the actually missing data
df.LotFrontage.fillna(df.LotFrontage.median(),inplace=True)


# In[ ]:


# lets fill the missing data with frequent occurred value
df.Electrical.fillna(df.Electrical.mode()[0],inplace=True)
df.Exterior1st.fillna(df.Exterior1st.mode()[0],inplace=True)
df.Exterior2nd.fillna(df.Exterior2nd.mode()[0],inplace=True)
df.Functional.fillna(df.Functional.mode()[0],inplace=True)
df.KitchenQual.fillna(df.KitchenQual.mode()[0],inplace=True)
df.SaleType.fillna(df.SaleType.mode()[0],inplace=True)
df.Utilities.fillna(df.Utilities.mode()[0],inplace=True)


# In[ ]:


# These are the features where missing values need to be filled with None and zeros
Nonefeatures = ['Alley','MasVnrType','BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2',
               'FireplaceQu','GarageType','GarageFinish','GarageQual','GarageCond','PoolQC','Fence','MiscFeature']
Zerofeatures = ['MasVnrArea','BsmtFinSF1','BsmtFinSF2','BsmtFullBath','BsmtHalfBath',
               'BsmtUnfSF','GarageArea','GarageCars','GarageYrBlt','TotalBsmtSF']


# In[ ]:


for nonefeature in Nonefeatures:
    filla(nonefeature,True)
for zerofeature in Zerofeatures:
    filla(zerofeature,False)


# - Lets check if there is a mismatch in datatype and also seggregate them into numerical and categorical variables

# In[ ]:


df.info()


# In[ ]:


# Seggregating data types into two different lists
Catefeatures = [x for x in df.columns if str(df[x].dtypes) == 'object']
Numfeatures = [x for x in df.columns if str(df[x].dtypes) != 'object']


# In[ ]:


# lets check the numerical features if any variable is categorical with numeric values
#these are the variables identified as categorical which has numerical representation
cate_num =['MSSubClass','OverallQual','OverallCond','BsmtFullBath','BsmtHalfBath','FullBath','HalfBath',
'BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces','GarageCars','MoSold','YrSold']


# In[ ]:


# lets remove this categorical variables from Numerical features
for features in cate_num:
    Numfeatures.remove(features)
    Catefeatures.append(features)


# #### Lets check the normality of the target variable

# In[ ]:


# lets see the normality of the target element
from scipy import stats
from scipy.stats import norm, skew


# In[ ]:


plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
sns.distplot(target,fit=norm)
plt.subplot(1,2,2)
stats.probplot(target,plot=plt)
plt.show()
plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
sns.distplot(np.sqrt(target),fit=norm)
plt.subplot(1,2,2)
stats.probplot(np.sqrt(target),plot=plt)
plt.show()
plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
sns.distplot(np.cbrt(target),fit=norm)
plt.subplot(1,2,2)
stats.probplot(np.cbrt(target),plot=plt)
plt.show()
plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
sns.distplot(np.log(target),fit=norm)
plt.subplot(1,2,2)
stats.probplot(np.log(target),plot=plt)
plt.show()


# - there is some skewness in the distribution

# - seems like now the skewness got corrected little bit

# In[ ]:


# since the logarithm is following almost normality let take it as target variable
target_ln = np.log(target)


# In[ ]:


# lets check the skewness in the data
skewness = df[Numfeatures].apply(lambda x : skew(x)).sort_values(ascending=False)
skewness_df = pd.DataFrame({'skew':skewness})
skewness_df.head()


# In[ ]:


# lets reduce the skewness by transforming using boxcox 
skewed =  skewness_df[abs(skewness_df['skew']) > 0.75]
from scipy.special import boxcox1p
skewed_features = skewed.index
lam = 0.15
for fea in skewed_features:
    df[fea] = boxcox1p(df[fea],lam)
    


# In[ ]:


df_cate = pd.get_dummies(df[Catefeatures],drop_first=True)


# In[ ]:


#Concatenating numerical features and categorical features into a single dataframe
df_new = pd.concat([df[Numfeatures],df_cate],axis=1)


# In[ ]:


# lets divide the dataframe into test and train
train_df = df_new[df_new.Id<1461]
test_df = df_new[df_new.Id>1460]


# lets find the outliers using ridg and elastic algorithms
# 

# In[ ]:


from sklearn.linear_model import RidgeCV,Ridge,ElasticNet
from sklearn.model_selection import KFold, cross_val_score
ridge = Ridge(alpha=10)
ridge.fit(train_df, target_ln)
np.sqrt(-cross_val_score(ridge, train_df, target_ln, cv=5, scoring="neg_mean_squared_error")).mean()


# In[ ]:


y_pred = ridge.predict(train_df)
resid = target_ln - y_pred
mean_resid = resid.mean()
std_resid = resid.std()
z = (resid - mean_resid) / std_resid
z = np.array(z)
outliers1 = np.where(abs(z) > abs(z).std() * 3)[0]
outliers1


# In[ ]:


plt.figure(figsize=(6, 6))
plt.scatter(target_ln, y_pred)
plt.scatter(target_ln.iloc[outliers1], y_pred[outliers1])
plt.plot(range(10, 15), range(10, 15), color="red")


# Lets use Elastic regression

# In[ ]:


er = ElasticNet(alpha=0.001, l1_ratio=0.58)
er.fit(train_df, target_ln)
np.sqrt(-cross_val_score(ridge, train_df, target_ln, cv=5, scoring="neg_mean_squared_error")).mean()


# In[ ]:


y_pred = er.predict(train_df)
resid = target_ln - y_pred
mean_resid = resid.mean()
std_resid = resid.std()
z = (resid - mean_resid) / std_resid
z = np.array(z)
outliers2 = np.where(abs(z) > abs(z).std() * 3)[0]
outliers2


# In[ ]:


plt.figure(figsize=(6, 6))
plt.scatter(target_ln, y_pred)
plt.scatter(target_ln.iloc[outliers2], y_pred[outliers2])
plt.plot(range(10, 15), range(10, 15), color="red")


# the points where the two algorithms predict poor results are  considered as outliers

# In[ ]:


outliers = []
for i in outliers1:
    for j in outliers2:
        if i == j:
            outliers.append(i)


# In[ ]:


train = pd.concat([train_df,target],axis=1)
train = train.drop(outliers)
target = train.SalePrice
target_ln = np.log(target)


# In[ ]:


train_df = train.drop(['SalePrice','Id'],axis=1)
test_df.drop(['Id'],axis=1,inplace=True)


# In[ ]:


# Lets Build model to predict the value
#lets start with ensemble randomforest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(criterion='mse')


# In[ ]:


#param = {
#    'max_depth':[2,3,5,7,9],
#    'n_estimators':[100,200,300,400,500,600,700,750,800]
#}
#rf_cv = GridSearchCV(estimator=rf,param_grid=param,verbose=True)


# In[ ]:


trainx,testx,trainy,testy = train_test_split(train_df,target_ln,test_size=0.2)


# In[ ]:


rf_cv = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=9,
           max_features='auto', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=1, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=750, n_jobs=None,
           oob_score=False, random_state=None, verbose=0, warm_start=False)
rf_cv.fit(trainx,trainy)


# In[ ]:


#print(rf_cv.best_estimator_)
#print('_'*40)
#print(rf_cv.best_params_)


# In[ ]:


train_predict = rf_cv.predict(trainx)
test_predict = rf_cv.predict(testx)


# In[ ]:


print(np.sqrt(metrics.mean_squared_error(trainy,train_predict)))
print(np.sqrt(metrics.mean_squared_error(testy,test_predict)))


# In[ ]:


trains_predict = rf_cv.predict(train_df)


# In[ ]:


sns.distplot(target_ln,color='green')
sns.distplot(trains_predict,color='red')
plt.show()


# In[ ]:


submission_df.head()


# In[ ]:


#now fitting the model on entire train data
#rf_cv = GridSearchCV(estimator=rf,param_grid=param,verbose=True)
rf_cv_1 = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=9,
           max_features='auto', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=1, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=500, n_jobs=None,
           oob_score=False, random_state=10, verbose=0, warm_start=False)
rf_cv_1.fit(train_df,target_ln)


# In[ ]:


#rf_cv.best_estimator_


# In[ ]:


test_df_predict = rf_cv_1.predict(test_df)


# In[ ]:


submission_df['SalePrice'] = np.exp(test_df_predict)


# In[ ]:


submission_df.to_csv('House_sale_submission.csv',index=False)


# ##### above gives me a score of 0.146 RMSE and position of 2638

# # lets try other models

# In[ ]:


from sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler,StandardScaler
from mlxtend.regressor import StackingCVRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor


# In[ ]:


#Validation function
n_folds = 5
kfolds = KFold(n_splits=10, shuffle=True, random_state=10)
def cv_rmse(model, X=train_df):
    rmse = np.sqrt(-cross_val_score(model, X, target_ln, scoring="neg_mean_squared_error", cv=kfolds))
    return (rmse)


# - Lasson Regression

# - to remove larger values of outlier RobustScaler is much usefull

# In[ ]:


alphas_alt = [14.5, 14.6, 14.7, 14.8, 14.9, 15, 15.1, 15.2, 15.3, 15.4, 15.5]
alphas2 = [5e-05, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008]
e_alphas = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007]
e_l1ratio = [0.8, 0.85, 0.9, 0.95, 0.99, 1]


# In[ ]:


lasso = make_pipeline(RobustScaler(),LassoCV(max_iter=1e7,alphas=alphas2,random_state=10,cv=kfolds))


# In[ ]:


ridge = make_pipeline(RobustScaler(), RidgeCV(alphas=alphas_alt, cv=kfolds))


# In[ ]:


elasticnet = make_pipeline(RobustScaler(), ElasticNetCV(max_iter=1e7, alphas=e_alphas, cv=kfolds, l1_ratio=e_l1ratio))


# In[ ]:


svr = make_pipeline(RobustScaler(), SVR(C= 20, epsilon= 0.008, gamma=0.0003,))


# In[ ]:


#param_gradient = {
#    'learning_rate' :[0.01,0.03,0.05,0.06],
#    'n_estimators':[1000,2000,3000,3500],
#    'max_depth':[3,4,5],
#    'min_samples_leaf':[5,10,15,20],
#    'min_samples_split':[5,10,15]
#}
#gbr_cv = GridSearchCV(estimator=GradientBoostingRegressor(max_features='sqrt',loss='huber'),
#                      param_grid=param_gradient,
#                     verbose=True)
#gbr_cv.fit(train_df,target_ln)
#gbr = GradientBoostingRegressor(n_estimators=3000, 
#                                learning_rate=0.05, 
#                                max_depth=4, 
#                                max_features='sqrt', 
#                                min_samples_leaf=15, 
#                                min_samples_split=10, 
#                                loss='huber', 
#                                random_state =42) 


# In[ ]:


gbr = GradientBoostingRegressor(n_estimators=3000, 
                                learning_rate=0.05, 
                                max_depth=4, 
                                max_features='sqrt', 
                                min_samples_leaf=15, 
                                min_samples_split=10, 
                                loss='huber')
   


# In[ ]:


#gbr_cv.best_params_


# In[ ]:


lightgbm = LGBMRegressor(objective='regression', 
                                       num_leaves=4,
                                       learning_rate=0.01, 
                                       n_estimators=5000,
                                       max_bin=200, 
                                       bagging_fraction=0.75,
                                       bagging_freq=5, 
                                       bagging_seed=7,
                                       feature_fraction=0.2,
                                       feature_fraction_seed=7,
                                       verbose=-1,
                                       )


# In[ ]:


xgboost = XGBRegressor(learning_rate=0.01,n_estimators=3460,
                                     max_depth=3, min_child_weight=0,
                                     gamma=0, subsample=0.7,
                                     colsample_bytree=0.7,
                                     objective='reg:linear', nthread=-1,
                                     scale_pos_weight=1, seed=27,
                                     reg_alpha=0.00006)


# In[ ]:


stack_gen = StackingCVRegressor(regressors=(ridge, lasso, elasticnet, gbr, xgboost, lightgbm),
                                meta_regressor=xgboost,
                                use_features_in_secondary=True)


# In[ ]:


score = cv_rmse(ridge)
print("Ridge: ",score.mean(), score.std())

score = cv_rmse(lasso)
print("LASSO: ",score.mean(), score.std() )

score = cv_rmse(elasticnet)
print("elastic ",score.mean(), score.std() )

score = cv_rmse(svr)
print("SVR: ",score.mean(), score.std() )

score = cv_rmse(lightgbm)
print("lightgbm:",score.mean(), score.std() )

score = cv_rmse(gbr)
print("gbr_cv: ",score.mean(), score.std() )

score = cv_rmse(xgboost)
print("xgboost: ",score.mean(), score.std())


# In[ ]:


X=train_df
y = target_ln
print('stack_gen')
stack_gen_model = stack_gen.fit(np.array(X), np.array(y))

print('elasticnet')
elastic_model_full_data = elasticnet.fit(X, y)

print('Lasso')
lasso_model_full_data = lasso.fit(X, y)

print('Ridge')
ridge_model_full_data = ridge.fit(X, y)

print('Svr')
svr_model_full_data = svr.fit(X, y)

print('GradientBoosting')
gbr_model_full_data = gbr.fit(X, y)

print('xgboost')
xgb_model_full_data = xgboost.fit(X, y)

print('lightgbm')
lgb_model_full_data = lightgbm.fit(X, y)


# In[ ]:


# the coeffiecents are more or less are scores of the respective models.
def blend_models_predict(X):
    return ((0.1 * elastic_model_full_data.predict(X)) +             (0.05 * lasso_model_full_data.predict(X)) +             (0.1 * ridge_model_full_data.predict(X)) +             (0.1 * svr_model_full_data.predict(X)) +             (0.1 * gbr_model_full_data.predict(X)) +             (0.15 * xgb_model_full_data.predict(X)) +             (0.1 * lgb_model_full_data.predict(X)) +             (0.3 * stack_gen_model.predict(np.array(X))))


# In[ ]:


print('RMSLE score on train data:')
print(np.sqrt(metrics.mean_squared_error(y, blend_models_predict(X))))


# In[ ]:


stacked_sales = np.floor(np.expm1(blend_models_predict(test_df)))


# In[ ]:


submission_df['SalePrice'] = stacked_sales


# In[ ]:


submission_df.to_csv('stacked_prediction.csv',index=False)


# In[ ]:





# In[ ]:




