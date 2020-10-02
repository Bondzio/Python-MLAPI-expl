#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
sns.set(style='white', palette='deep')
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Importing dataset
df = pd.read_csv('/kaggle/input/fuel-consumption/FuelEconomy.csv')
df.head()


# In[ ]:


#Analysing dataset with padas profiling
from pandas_profiling import ProfileReport
profile = ProfileReport(df, title='Fuel Consumption Datasets', html={'style':{'full_width':True}})


# In[ ]:


profile


# In[ ]:


#Dataset info
df.info()


# In[ ]:


#Dataset statistic
df.describe()


# In[ ]:


#Plotting features with matplotlib
fig=plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.set_title('Fuel Economy', fontsize=15)
ax.scatter(df['Horse Power'].values,df['Fuel Economy (MPG)'].values,marker='o', color='r', alpha=1, linewidth=1, 
            edgecolor='k', label='one')
ax.set_xlabel('{} (HP)'.format(df.columns[0]), fontsize=15)
ax.set_ylabel('{} (MPG)'.format(df.columns[1]), fontsize=15)
ax.grid(b=True, which='major', linestyle='--')
ax.tick_params(axis='both', labelsize=15, labelcolor='k')


# In[ ]:


#Plotting features with seaborn
sns.jointplot(x=df.columns[0], y=df.columns[1], data=df)
sns.pairplot(df)
sns.lmplot(x=df.columns[0], y=df.columns[1], data=df, palette='deep')


# In[ ]:


#Splitting Data
X=df.drop('Fuel Economy (MPG)', axis=1)
y=df['Fuel Economy (MPG)']


# In[ ]:


#Splitting the Dataset into the training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
X_train.shape, X_test.shape, y_train.shape,y_test.shape


# In[ ]:


#Feature scaling
from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
X_train = pd.DataFrame(sc_x.fit_transform(X_train), columns=X.columns.values)
X_test = pd.DataFrame(sc_x.transform(X_test), columns=X.columns.values)


# # Model Building 
# ## Comparing Models

# In[ ]:


## Multiple Linear Regression Regression
from sklearn.linear_model import LinearRegression
lr_regressor = LinearRegression(fit_intercept=True)
lr_regressor.fit(X_train, y_train)

print('Linear Model Coefficient (m): ', lr_regressor.coef_)
print('Linear Model Coefficient (b): ', lr_regressor.intercept_)


# In[ ]:


# Predicting Test Set Multiple Linear Regression Regression
y_pred = lr_regressor.predict(X_test)
from sklearn import metrics
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)

results = pd.DataFrame([['Multiple Linear Regression', mae, mse, rmse, r2]],
               columns = ['Model', 'MAE', 'MSE', 'RMSE', 'R2 Score'])


# In[ ]:


#Plotting Train set and predictions
plt.scatter(X_train, y_train, color = 'gray')
plt.plot(X_train, lr_regressor.predict(X_train), color = 'red')
plt.ylabel('{} (MPG)'.format(df.columns[1]))
plt.xlabel('{} (HP)'.format(df.columns[0]))
plt.title('Fuel Economy (Training dataset)')


# In[ ]:


#Plotting Test set and predictions
plt.scatter(X_test, y_test, color = 'gray')
plt.plot(X_test, lr_regressor.predict(X_test), color = 'red')
plt.ylabel('{} (MPG)'.format(df.columns[1]))
plt.xlabel('{} (HP)'.format(df.columns[0]))
plt.title('Fuel Economy (Test dataset)')


# In[ ]:


## Polynomial Regressor
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree = 2)
X_poly = poly_reg.fit_transform(X_train)
lr_poly_regressor = LinearRegression(fit_intercept=True)
lr_poly_regressor.fit(X_poly, y_train)

# Predicting Test Set
y_pred = lr_poly_regressor.predict(poly_reg.fit_transform(X_test))
from sklearn import metrics
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)

model_results = pd.DataFrame([['Polynomial Regression', mae, mse, rmse, r2]],
               columns = ['Model', 'MAE', 'MSE', 'RMSE', 'R2 Score'])

results = results.append(model_results, ignore_index = True)


# In[ ]:


## Decision Tree Regression
from sklearn.tree import DecisionTreeRegressor
dt_regressor = DecisionTreeRegressor(random_state=0)
dt_regressor.fit(X_train, y_train)

# Predicting Test Set
y_pred = dt_regressor.predict(X_test)
from sklearn import metrics
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)

model_results = pd.DataFrame([['Decision Tree Regression', mae, mse, rmse, r2]],
               columns = ['Model', 'MAE', 'MSE', 'RMSE', 'R2 Score'])

results = results.append(model_results, ignore_index = True)


# In[ ]:


## Random Forest Regression
from sklearn.ensemble import RandomForestRegressor
rf_regressor = RandomForestRegressor(n_estimators=300, random_state=0)
rf_regressor.fit(X_train,y_train)

# Predicting Test Set
y_pred = rf_regressor.predict(X_test)
from sklearn import metrics
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)

model_results = pd.DataFrame([['Random Forest Regression', mae, mse, rmse, r2]],
               columns = ['Model', 'MAE', 'MSE', 'RMSE', 'R2 Score'])

results = results.append(model_results, ignore_index = True)


# In[ ]:


## Ada Boosting
from sklearn.ensemble import AdaBoostRegressor
ad_regressor = AdaBoostRegressor()
ad_regressor.fit(X_train, y_train)

# Predicting Test Set
y_pred = ad_regressor.predict(X_test)
from sklearn import metrics
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)

model_results = pd.DataFrame([['AdaBoost Regressor', mae, mse, rmse, r2]],
               columns = ['Model', 'MAE', 'MSE', 'RMSE', 'R2 Score'])

results = results.append(model_results, ignore_index = True)


# In[ ]:


##Gradient Boosting
from sklearn.ensemble import GradientBoostingRegressor
gb_regressor = GradientBoostingRegressor()
gb_regressor.fit(X_train, y_train)

# Predicting Test Set
y_pred = gb_regressor.predict(X_test)
from sklearn import metrics
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)

model_results = pd.DataFrame([['GradientBoosting Regressor', mae, mse, rmse, r2]],
               columns = ['Model', 'MAE', 'MSE', 'RMSE', 'R2 Score'])

results = results.append(model_results, ignore_index = True)


# In[ ]:


##Xg Boosting
from xgboost import XGBRegressor
xgb_regressor = XGBRegressor()
xgb_regressor.fit(X_train, y_train)

# Predicting Test Set
y_pred = xgb_regressor.predict(X_test)
from sklearn import metrics
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)

model_results = pd.DataFrame([['XGB Regressor', mae, mse, rmse, r2]],
               columns = ['Model', 'MAE', 'MSE', 'RMSE', 'R2 Score'])

results = results.append(model_results, ignore_index = True)


# In[ ]:


##Ensemble Voting regressor
from sklearn.ensemble import VotingRegressor
voting_regressor = VotingRegressor(estimators= [('lr', lr_regressor),
                                                  ('lr_poly', lr_poly_regressor),
                                                  ('dt', dt_regressor),
                                                  ('rf', rf_regressor),
                                                  ('ad', ad_regressor),
                                                  ('gr', gb_regressor),
                                                  ('xg', xgb_regressor)])

for clf in (lr_regressor,lr_poly_regressor,dt_regressor,
            rf_regressor, ad_regressor,gb_regressor, xgb_regressor, voting_regressor):
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    print(clf.__class__.__name__, metrics.r2_score(y_test, y_pred))

# Predicting Test Set
y_pred = voting_regressor.predict(X_test)
from sklearn import metrics
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)

model_results = pd.DataFrame([['Ensemble Voting', mae, mse, rmse, r2]],
               columns = ['Model', 'MAE', 'MSE', 'RMSE', 'R2 Score'])

results = results.append(model_results, ignore_index = True)  


# In[ ]:


#The Best Classifier
print('The best regressor is:')
print('{}'.format(results.sort_values(by='R2 Score',ascending=False).head(5)))


# In[ ]:


#Applying K-fold validation
from sklearn.model_selection import cross_val_score
def display_scores (scores):
    print('Scores:', scores)
    print('Mean:', scores.mean())
    print('Standard:', scores.std())

lin_scores = cross_val_score(estimator=lr_poly_regressor, X=X_train, y=y_train, 
                             scoring= 'neg_mean_squared_error',cv=10)
lin_rmse_scores = np.sqrt(-lin_scores)
display_scores(lin_rmse_scores)


# In[ ]:


# Analyzing Coefficients
pd.concat([pd.DataFrame(X_train.columns, columns = ["features"]),
           pd.DataFrame(np.transpose(lr_poly_regressor.coef_), columns = ["coef"])
           ],axis = 1)


# In[ ]:




