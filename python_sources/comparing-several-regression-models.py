#!/usr/bin/env python
# coding: utf-8

# 

# 

# # Reading Data

# In[ ]:


#let's start with importing the libraries we need to:
# 1- read and manipulate data:
import pandas as pd
import numpy as np
# 2- visualize data and graphs
import matplotlib.pyplot as plt


# In[ ]:


#Now lets read the data 
raw_data = pd.read_csv('../input/housesalesprediction/kc_house_data.csv')
#Now lets explore our data: 
raw_data.head(10)


# ## Data Preprocessing

# In[ ]:


#lets check for missing data:
missing_data_print={}
missing_data_print['column_name']=[]
missing_data_print['Missing Entries']=[]
for elt in raw_data.columns:
    missing_data_print['column_name'].append(elt)
    missing_data_print['Missing Entries'].append(raw_data[elt].isna().sum())
missing_data_print=pd.DataFrame(missing_data_print)
missing_data_print


# ## Features

# 

# In[ ]:


hist = raw_data.hist(bins=100,color='red',figsize=(16, 16))


# 

# In[ ]:


#so we have 21 columns our target column is the price 
#because we are trying to creat a model that predicts the sell price of a house
y=raw_data['price']
X=raw_data.drop(['price','id'],axis=1)

#we can easily notice that all data are either integers or floats except for the selling date
#therefore I propose to convert this column into an integer column
#actually the selling date (column date) are of type string with the format yyyymmddT000000 
#so I propose to keep only the forme yyyymmdd and then convert this string into integer
#with this form we will be able to represent the date with integer while keeping the order relation between the dates
# first january 2015 will be coded 20150101 while first april 2016 will be coded 20160401 and thus we keep 
# the relation ship of first april 2016 is more recently (>) than first of january 2015
X['date']=X['date'].apply(lambda x : int(x[0:8]))

#we have a column named yr_built which indicates the year of built of the house 
#this column is not so pertinent since the houses are selled on different dates
#I propose to replace the year of built with the age of the house at the selling date
#I will name this column (age)
X['age']=X['date']//10000 - X['yr_built']

#we have a column named yr_renovated that indicates the year of renovation of the house
#this column is equal to zero in the cases the renovation is never done
#I propose to change this column by a column that I name (yrs_since_renovation) 
#this column will contains the years since last renovation before selling the house
X['yrs_since_renovation'] = X.apply(lambda x : min(x['date']//10000-x['yr_renovated'],x['age']),axis=1)


# In[ ]:


df=X[['yr_built','age','yr_renovated','yrs_since_renovation']]
hist = df.hist(bins=100,color='red',figsize=(16, 16))


# You can notice that the histogram of age is almost an anti symetric replicate of the yr_built histogram. The histogram that describes the number of years since renovation is different from the yr_renovated which represents almost two classes, the first has a value 0 for houses that were never renovated and a second class around the 20th-21st century. As for yrs_since_renovation is quite identical to the histogram of age (which is expected from the formula used to compute this feature). I think using the two new features will not cause a big difference. 
# We will see this later. In the following sections, all used methods are used for both old (yr_built and yr_renovated) and new (age, yrs_since_renovation) features.

# In[ ]:


plt.figure(figsize=(16, 16))
i=1
for elt in X.columns :
    plt.subplot(7,3,i)
    plt.scatter(X[elt],y)
    plt.xlim((X[elt].min(),X[elt].max()))
    plt.xlabel(elt)
    plt.ylabel('price u.m.')
    i+=1

plt.tight_layout(0.05)
plt.show()


# The obtained plots do not give too much information. We can not be sure about our observation, but we can assume the following:
# * The number of bedrooms seems to have an influence on the price. As shown in the plot, the price tends to be higher when the number of bedrooms is near 5. 
# * The number of bathrooms seems to have the same influence as that of the bedrooms. The price tends to be higher when the number of bathrooms is between 3 and 5. 
# * The interior living space (sqft_living) seems to directly influence the price. The larger the living space the higher the price tends to be. The same can be said for the space above the ground, the basement space, the interior space of the 15 nearest neighbors and for the level of construction and design (sqft_above, sqft_basement, sqft_living15, and grade).
# * Sqft_lot and sqft_lot15 represent respectively the space of the land and the space of the land of the nearest 15 neighbors. These two elements indicates two tendencies for the price. It seems like the price is higher when they are low and then it gradually regain hight when they get bigger. Well this can mean that we are dealing with two types of housing (apartments/big building and big houses/mansions).
# 

# In[ ]:


f = plt.figure(figsize=(19, 15))
df=pd.concat([X, y], axis=1)
plt.matshow(df.corr(), fignum=f.number)
plt.xticks(range(df.shape[1]), df.columns, fontsize=14, rotation=90)
plt.yticks(range(df.shape[1]), df.columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.title('Correlation Matrix', fontsize=16,y=-0.08)
plt.show()


# ## Preparing the training and the test sets

# In[ ]:


from sklearn.model_selection import train_test_split
X_mod=X.drop(['yr_built','yr_renovated'],axis=1)
X_mtrain, X_mtest, y_train, y_test = train_test_split(X_mod.values,y.values,test_size=0.2,random_state=0)
X_nor=X.drop(['yrs_since_renovation','age'],axis=1)
X_train, X_test, y_train, y_test = train_test_split(X_nor.values,y.values,test_size=0.2,random_state=0)
####


# ## Defining the Metrics

# In[ ]:


from sklearn.metrics import mean_squared_error,r2_score
from math import sqrt


# ## Defining the Results Table

# In[ ]:


Results = {}
Results['Method']=[]
Results['R2-score']=[]
Results['RMSE']=[]


# ## Defining the Predictions Table

# In[ ]:


Predictions = pd.DataFrame()
Predictions['Ground Truth'] = y_test


# # Simple Linear Regression

# In[ ]:


from sklearn.linear_model import LinearRegression
#with new features
SLR = LinearRegression()
SLR.fit(X_mtrain,y_train)
y_pred = SLR.predict(X_mtest)
Results['Method'].append("SLR with new features")
Results['R2-score'].append(r2_score(y_test,y_pred))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred)))
#with old features
SLR_nor = LinearRegression()
SLR_nor.fit(X_train,y_train)
y_pred2 = SLR_nor.predict(X_test)
Results['Method'].append("SLR with old features")
Results['R2-score'].append(r2_score(y_test,y_pred2))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred2)))
#saving the predictions
Predictions['SLR_new_F']=y_pred
Predictions['SLR_old_F']=y_pred2


# # Multiple Linear Regression

# ## For New Features

# ### Data Adaptation
# 

# In[ ]:


#we are going to eliminate variables that won't make a difference 
#we add the constant variable x_0
X_Ttrain = np.append(np.ones((len(X_mtrain),1)).astype(int),X_mtrain,1)
X_Ttest = np.append(np.ones((len(X_mtest),1)).astype(int),X_mtest,1)


# ### Step-by-Step Backward Elimination

# In[ ]:


import statsmodels.api as sm
#our X_optimal is initialized to X_Ttrain
X_opt=X_Ttrain[:,:]


# In[ ]:


#Step 1 :Fit the ALL IN model
model_MLR=sm.OLS(endog=y_train,exog=X_opt).fit()
model_MLR.summary()


# 

# In[ ]:


Column_to_delete=6
columns_to_keep=[]
for elt in range(X_opt.shape[1]):
    if elt != Column_to_delete :
        columns_to_keep.append(elt)
X_opt = X_opt[:,columns_to_keep]
X_Ttest = X_Ttest[:,columns_to_keep]
X_opt.shape


# In[ ]:


model_MLR=sm.OLS(endog=y_train,exog=X_opt).fit()
model_MLR.summary()


# 

# In[ ]:


from sklearn.linear_model import LinearRegression
#with new features
SLR = LinearRegression()
#Do not forget to take out the constant otherwise you'll get lower R-squared
X_opt=X_opt[:,1:]
SLR.fit(X_opt,y_train)
X_Ttest=X_Ttest[:,1:]
y_pred = SLR.predict(X_Ttest)
Results['Method'].append("Multi-LR with new features")
Results['R2-score'].append(r2_score(y_test,y_pred))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred)))


# ## For Old Features

# ### Data Adaptation

# In[ ]:


#we are going to eliminate variables that won't make a difference 
#we add the constant variable x_0
X_Ttrain = np.append(np.ones((len(X_train),1)).astype(int),X_train,1)
X_Ttest = np.append(np.ones((len(X_test),1)).astype(int),X_test,1)


# ### Step-by-Step Backward Elimination

# In[ ]:


import statsmodels.api as sm
#our X_optimal is initialized to X_Ttrain
X_opt=X_Ttrain[:,:]


# In[ ]:


#Step 1 :Fit the ALL IN model
model_MLR=sm.OLS(endog=y_train,exog=X_opt).fit()
model_MLR.summary()


# 

# In[ ]:


from sklearn.linear_model import LinearRegression
#with new features
SLR = LinearRegression()
X_opt=X_opt[:,1:]
SLR.fit(X_opt,y_train)
X_Ttest=X_Ttest[:,1:]
y_pred = SLR.predict(X_Ttest)
Results['Method'].append("Multi-LR with old features")
Results['R2-score'].append(r2_score(y_test,y_pred))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred)))


# # Support Vector Regression

# ## Data Min-Max Normalization

# In[ ]:


from sklearn.preprocessing import MinMaxScaler
X_mod_Scaler = MinMaxScaler()
X_mtrain_s=X_mod_Scaler.fit_transform(X_mtrain)
X_mtest_s = X_mod_Scaler.transform(X_mtest)

X_Scaler = MinMaxScaler()
X_train_s=X_Scaler.fit_transform(X_train)
X_test_s = X_Scaler.transform(X_test)

y_Scaler = MinMaxScaler()
y_train_s=y_Scaler.fit_transform(y_train.reshape(-1,1))
y_train_s=y_train_s.reshape(len(y_train),)
y_test_s=y_Scaler.transform(y_test.reshape(-1,1))
y_test_s=y_test_s.reshape(len(y_test),)


# ## The regression

# In[ ]:


from sklearn.svm import SVR
#with new features
svr_RBF = SVR(kernel='rbf',gamma='auto')
svr_RBF.fit(X_mtrain_s,y_train_s.reshape(17290,))
y_pred_s = svr_RBF.predict(X_mtest_s)
y_pred = y_Scaler.inverse_transform(y_pred_s.reshape(-1,1))
Results['Method'].append("Guassian SVR with new features")
Results['R2-score'].append(r2_score(y_test,y_pred))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred)))

#with old features
svr_RBF2 = SVR(kernel='rbf',gamma='auto')
svr_RBF2.fit(X_train_s,y_train_s.reshape(17290,))
y_pred_s2 = svr_RBF2.predict(X_test_s)
y_pred2 = y_Scaler.inverse_transform(y_pred_s2.reshape(-1,1))
Results['Method'].append("Guassian SVR with old features")
Results['R2-score'].append(r2_score(y_test,y_pred2))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred2)))

#Saving Predictions
Predictions['Gaussian_SVR_new_F']=y_pred.reshape(len(y_test),)
Predictions['Gaussian_SVR_old_F']=y_pred2.reshape(len(y_test),)


# # Decision Tree Regression

# In[ ]:


#using decision tree
from sklearn.tree import DecisionTreeRegressor
#With new features
DTR = DecisionTreeRegressor(random_state=0)
DTR.fit(X_mtrain,y_train)
y_pred = DTR.predict(X_mtest)
Results['Method'].append("DTR with new features")
Results['R2-score'].append(r2_score(y_test,y_pred))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred)))

#with old features
DTR_2 = DecisionTreeRegressor(random_state=0)
DTR_2.fit(X_train,y_train)
y_pred2 = DTR.predict(X_test)
Results['Method'].append("DTR with old features")
Results['R2-score'].append(r2_score(y_test,y_pred2))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred2)))

DecisionTreesRegressionsPredictions=pd.DataFrame()
Predictions['DTR_new_F']=y_pred
Predictions['DTR_old_F']=y_pred2


# # Random Forest Regression

# ## Ensemble Learning

# ## Random Forest with 100 Tree

# In[ ]:


#random forest
from sklearn.ensemble import RandomForestRegressor
#with new features
RFR_mod = RandomForestRegressor(n_estimators=100,random_state=0)
RFR_mod.fit(X_mtrain,y_train)
y_pred = RFR_mod.predict(X_mtest)
Results['Method'].append("100Tree_RFR with new features")
Results['R2-score'].append(r2_score(y_test,y_pred))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred)))

#with old features
RFR_nor = RandomForestRegressor(n_estimators=100,random_state=0)
RFR_nor.fit(X_train,y_train)
y_pred2 = RFR_nor.predict(X_test)
Results['Method'].append("100Tree_RFR with old features")
Results['R2-score'].append(r2_score(y_test,y_pred2))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred2)))

#saving predictions
Predictions['100T_RFR_new_F']=y_pred
Predictions['100T_RFR_old_F']=y_pred2


# ## Random Forest with 200 Tree

# In[ ]:


#with new features
RFR_mod_2 = RandomForestRegressor(n_estimators=200,random_state=0)
RFR_mod_2.fit(X_mtrain,y_train)
y_pred = RFR_mod_2.predict(X_mtest)
Results['Method'].append("200Tree_RFR with new features")
Results['R2-score'].append(r2_score(y_test,y_pred))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred)))
#with old features
RFR_nor_2 = RandomForestRegressor(n_estimators=200,random_state=0)
RFR_nor_2.fit(X_train,y_train)
y_pred2 = RFR_nor_2.predict(X_test)
Results['Method'].append("200Tree_RFR with old features")
Results['R2-score'].append(r2_score(y_test,y_pred2))
Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred2)))

#saving predictions
Predictions['200T_RFR_new_F']=y_pred
Predictions['200T_RFR_old_F']=y_pred2


# # K-Nearest Neighbors

# ## Data Min-Max Normalization

# In[ ]:


from sklearn.preprocessing import MinMaxScaler
X_mod_Scaler = MinMaxScaler()
X_mtrain_s=X_mod_Scaler.fit_transform(X_mtrain)
X_mtest_s = X_mod_Scaler.transform(X_mtest)

X_Scaler = MinMaxScaler()
X_train_s=X_Scaler.fit_transform(X_train)
X_test_s = X_Scaler.transform(X_test)

y_Scaler = MinMaxScaler()
y_train_s=y_Scaler.fit_transform(y_train.reshape(-1,1))
y_train_s=y_train_s.reshape(len(y_train),)
y_test_s=y_Scaler.transform(y_test.reshape(-1,1))
y_test_s=y_test_s.reshape(len(y_test),)


# ## K-NN Regressions

# In[ ]:


from sklearn.neighbors import KNeighborsRegressor
#for different k values example [1,10,50]
k_values =[1,10,20,50]
for k in k_values:
    #New Features
    k_nn=KNeighborsRegressor(n_neighbors = k)
    k_nn.fit(X_mtrain, y_train)  
    y_pred=k_nn.predict(X_mtest)
    Results['Method'].append("K=({})_NN with new features".format(k))
    Results['R2-score'].append(r2_score(y_test,y_pred))
    Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred)))
    k_nn_2=KNeighborsRegressor(n_neighbors = k)
    k_nn_2.fit(X_train, y_train)  
    y_pred2=k_nn_2.predict(X_test)
    Results['Method'].append("K=({})_NN with old features".format(k))
    Results['R2-score'].append(r2_score(y_test,y_pred2))
    Results['RMSE'].append(sqrt(mean_squared_error(y_test,y_pred2)))
    


# # Comparison of the obtained results

# ## Algorithms performances

# In[ ]:


Results_DF = pd.DataFrame(Results)
Results_DF


# ## Predictions

# In[ ]:


Predictions.head(10)


# # Conclusion

# ## Future Work

# In[ ]:




