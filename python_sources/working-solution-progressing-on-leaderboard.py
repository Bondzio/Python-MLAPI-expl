#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns

# Any results you write to the current directory are saved as output.


# In[ ]:


train_df = pd.read_csv("../input/covid19-global-forecasting-week-2/train.csv")
test_df = pd.read_csv("../input/covid19-global-forecasting-week-2/test.csv")


# In[ ]:


train_df.head(50)


# In[ ]:


'''
from pandas_profiling import ProfileReport
train_profile = ProfileReport(train_df, title='Pandas Profiling Report', html={'style':{'full_width':True}})
train_profile
'''


# In[ ]:


train_df.info()


# In[ ]:


common_value = "UNKNOWN"

# Replacing all the Province_State that are null by the Country_Region values
train_df.Province_State.fillna(train_df.Country_Region, inplace=True)
test_df.Province_State.fillna(test_df.Country_Region, inplace=True)

# Handling the Date column
# 1. Converting the object type column into datetime type
train_df.Date = train_df.Date.apply(pd.to_datetime)
test_df.Date = test_df.Date.apply(pd.to_datetime)

# 2. Creating new features
#train_df['ReportDay_year'] = train_df['Date'].dt.year #Not required this column because all the data is of this year
train_df['ReportDay_month'] = train_df['Date'].dt.month
train_df['ReportDay_week'] = train_df['Date'].dt.week
train_df['ReportDay_day'] = train_df['Date'].dt.day 

#test_df['ReportDay_year'] = test_df['Date'].dt.year
test_df['ReportDay_month'] = test_df['Date'].dt.month
test_df['ReportDay_week'] = test_df['Date'].dt.week
test_df['ReportDay_day'] = test_df['Date'].dt.day


# In[ ]:


#Dropping the date column
train_df.drop("Date", inplace = True, axis = 1)
test_df.drop("Date", inplace = True, axis = 1)


# In[ ]:


train_df.Province_State.value_counts()


# In[ ]:



from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

train_df.Country_Region = le.fit_transform(train_df.Country_Region)
train_df['Province_State'] = le.fit_transform(train_df['Province_State'])

test_df.Country_Region = le.fit_transform(test_df.Country_Region)
test_df['Province_State'] = le.fit_transform(test_df['Province_State'])


# In[ ]:


'''
def one_hot(df, cols):
    """
    @param df pandas DataFrame
    @param cols a list of columns to encode 
    @return a DataFrame with one-hot encoding
    """
    i = 0
    for each in cols:
        #print (each)
        dummies = pd.get_dummies(df[each], prefix=each, drop_first= True)
        if i == 0: 
            print (dummies)
            i = i + 1
        df = pd.concat([df, dummies], axis=1)
    return df
'''


# In[ ]:


'''
#Handling categorical data

objList = train_df.select_dtypes(include = "object").columns
train_df = one_hot(train_df, objList) 
test_df = one_hot(test_df, objList) 

print (train_df.shape)
'''


# In[ ]:


'''
# Removing duplicate entries
train_df = train_df.loc[:,~train_df.columns.duplicated()]
test_df = test_df.loc[:,~test_df.columns.duplicated()]
print (test_df.shape)
'''


# In[ ]:


'''
# Dropping the object type columns
train_df.drop(objList, axis=1, inplace=True)
test_df.drop(objList, axis=1, inplace=True)
print (train_df.shape)
'''


# In[ ]:


'''
train_df.select_dtypes(include = "object").columns
#So, no columns with object data is there. Our data is ready for training
'''


# In[ ]:


test_df.info()


# In[ ]:


X_train = train_df.drop(["Id", "ConfirmedCases", "Fatalities"], axis = 1)

Y_train_CC = train_df["ConfirmedCases"] 
Y_train_Fat = train_df["Fatalities"] 

#X_test = test_df.drop(["ForecastId"], axis = 1)
X_test = test_df.drop(["ForecastId"], axis = 1) 


# In[ ]:


#print (type(Y_train_CC))
#X_train_CC.info()


# In[ ]:


'''
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import make_scorer, r2_score, mean_squared_log_error

n_folds = 5
cv = KFold(n_splits = 10, shuffle=True, random_state=42).get_n_splits(X_train.values)

def test_model(model, colName):   
    msle = make_scorer(mean_squared_log_error)
    if colName == "CC":
        #print ("In")
        rmsle = np.sqrt(cross_val_score(model, X_train, Y_train_CC, cv=cv, scoring = msle))
    elif colName == "Fat": 
        rmsle = np.sqrt(cross_val_score(model, X_train, Y_train_Fat, cv=cv, scoring = msle))
    #print (rmsle)
    score_rmsle = [rmsle.mean()]
    return score_rmsle

def test_model_r2(model, colName):
    r2 = make_scorer(r2_score)
    if colName == "CC":
        r2_error = cross_val_score(model, X_train, Y_train_CC, cv=cv, scoring = r2)
    elif colName == "Fat": 
        r2_error = cross_val_score(model, X_train, Y_train_Fat, cv=cv, scoring = r2)
    score_r2 = [r2_error.mean()]
    return score_r2
'''


# In[ ]:


from sklearn.model_selection import ShuffleSplit, cross_val_score
skfold = ShuffleSplit(random_state=7)


# In[ ]:



#1.Ridge Regression

#Model import 

from sklearn.linear_model import Ridge

#train classifier
reg_CC = Ridge(alpha=1.0)
reg_Fat = Ridge(alpha=1.0)

#Cross Validation to calculate the score
score_CC = cross_val_score(reg_CC, X_train, Y_train_CC, cv = skfold)
score_Fat = cross_val_score(reg_Fat, X_train, Y_train_Fat, cv = skfold)

#rmsle_svm = test_model_r2(clf_svm, "CC")

#Print the scores
print (score_CC.mean(), score_Fat.mean())


# In[ ]:



#2.Lasso Regression

#Model import 

from sklearn import linear_model

#train classifier
reg_CC = linear_model.Lasso(alpha=0.1)
reg_Fat = linear_model.Lasso(alpha=0.1)

#Cross Validation to calculate the score
score_CC = cross_val_score(reg_CC, X_train, Y_train_CC, cv = skfold)
score_Fat = cross_val_score(reg_Fat, X_train, Y_train_Fat, cv = skfold)

#rmsle_svm = test_model_r2(clf_svm, "CC")

#Print the scores
print (score_CC.mean(), score_Fat.mean())


# In[ ]:



#3. SVM

#Model import 

from sklearn import svm

#train classifier
reg_CC = svm.SVC()
reg_Fat = svm.SVC()

#Cross Validation to calculate the score
score_CC = cross_val_score(reg_CC, X_train, Y_train_CC, cv = skfold)
score_Fat = cross_val_score(reg_Fat, X_train, Y_train_Fat, cv = skfold)

#Print the scores
print (score_CC.mean(), score_Fat.mean())


# In[ ]:



#3. ElasticNet

#Model import 
from sklearn.linear_model import ElasticNet

#train classifier
reg_CC = ElasticNet(random_state=0)
reg_Fat = ElasticNet(random_state=0)

#Cross Validation to calculate the score
score_CC = cross_val_score(reg_CC, X_train, Y_train_CC, cv = skfold)
score_Fat = cross_val_score(reg_Fat, X_train, Y_train_Fat, cv = skfold)

#Print the scores
print (score_CC.mean(), score_Fat.mean())


# In[ ]:



#5. LinearRegression

#Model import 

from sklearn.linear_model import LinearRegression

#train classifier
reg_CC = LinearRegression()
reg_Fat = LinearRegression()

#Cross Validation to calculate the score
score_CC = cross_val_score(reg_CC, X_train, Y_train_CC, cv = skfold)
score_Fat = cross_val_score(reg_Fat, X_train, Y_train_Fat, cv = skfold)

#Print the scores
print (score_CC.mean(), score_Fat.mean())


# In[ ]:


'''
#1. SVM algorithm
from sklearn import svm
clf_svm_CC = svm.SVC()
clf_svm_Fat = svm.SVC()

r_svm_CC = test_model(clf_svm_CC, "CC")
r_svm_Fat = test_model(clf_svm_Fat, "Fat")

#rmsle_svm = test_model_r2(clf_svm, "CC")

print (r_svm_CC, r_svm_Fat)
'''


# In[ ]:


'''
#2. Decision Tree 
from sklearn.tree import DecisionTreeRegressor

clf_dtR_CC = DecisionTreeRegressor(max_depth=5, random_state=51)
clf_dtR_Fat = DecisionTreeRegressor(max_depth=5, random_state=51)

rmsle_dtR_CC = test_model(clf_dtR_CC, "CC")
rmsle_dtR_Fat = test_model(clf_dtR_Fat, "Fat")

#print (rmsle_dtR_CC, test_model_r2(clf_dtR_CC, "CC"))

print (rmsle_dtR_CC, rmsle_dtR_Fat)
'''


# In[ ]:


'''
#3. Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor

clf_rFR_CC = RandomForestRegressor(max_depth=5, random_state=51)
clf_rFR_Fat = RandomForestRegressor(max_depth=5, random_state=51)

rmsle_rFR_cc = test_model(clf_rFR_CC, "CC")

rmsle_rFR_fat = test_model(clf_rFR_Fat, "Fat")

print (rmsle_rFR_cc, rmsle_rFR_fat)
'''


# In[ ]:


'''
#4. Adaboost regressor

from sklearn.ensemble import AdaBoostRegressor
clf_aBR_CC = AdaBoostRegressor(random_state=51, n_estimators=1000)
clf_aBR_Fat = AdaBoostRegressor(random_state=51, n_estimators=1000)

rmsle_aBR_CC = test_model(clf_aBR_CC, "CC")
rmsle_aBR_Fat = test_model(clf_aBR_Fat, "Fat")

print (rmsle_aBR_CC, rmsle_aBR_Fat)
'''


# In[ ]:



#5. BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor

clf_bgr_CC = BaggingRegressor(base_estimator = DecisionTreeRegressor())
clf_bgr_Fat = BaggingRegressor(base_estimator = DecisionTreeRegressor())

rmsle_bgr_CC = test_model(clf_bgr_CC, "CC")
rmsle_bgr_Fat = test_model(clf_bgr_Fat, "Fat")

print (rmsle_bgr_CC, rmsle_bgr_Fat)


# In[ ]:


'''
#6. Voting Regressor
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor

reg1 = BaggingRegressor(random_state=1, n_estimators=10)
reg2 = RandomForestRegressor(random_state=1, n_estimators=10)
reg3 = DecisionTreeRegressor()

clf_vr_CC = VotingRegressor(estimators=[('b', reg1), ('rf', reg2), ('dt', reg3)])
clf_vr_Fat = VotingRegressor(estimators=[('b', reg1), ('rf', reg2), ('dt', reg3)])

rmsle_vr_CC = test_model(clf_vr_CC, "CC")
rmsle_vr_Fat = test_model(clf_vr_Fat, "Fat")

print (rmsle_vr_CC, rmsle_vr_Fat)
'''


# In[ ]:


#print (X_train_CC.shape, X_train_Fat.shape, X_test.shape)


# In[ ]:


reg_CC.fit(X_train, Y_train_CC)
Y_pred_CC = reg_CC.predict(X_test) 

reg_Fat.fit(X_train, Y_train_Fat)
Y_pred_Fat = reg_Fat.predict(X_test) 


# In[ ]:


print (Y_pred_Fat)


# In[ ]:


df_out = pd.DataFrame({'ForecastId': [], 'ConfirmedCases': [], 'Fatalities': []})
soln = pd.DataFrame({'ForecastId': test_df.ForecastId, 'ConfirmedCases': Y_pred_CC, 'Fatalities': Y_pred_Fat})
df_out = pd.concat([df_out, soln], axis=0)
df_out.ForecastId = df_out.ForecastId.astype('int')


# In[ ]:


df_out.to_csv('submission.csv', index=False)
print("Your submission was successfully saved!")


# In[ ]:


'''
# Hyper parameter 

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

param_grid = {
              'n_estimators':[10, 30, 50, 100,250,500,750,1000,1250,1500,1750],
              'max_samples':[2,4,6,8,10,20,40,60,100],
              "max_features": [0.5, 1.0],
              'n_jobs':[-2, -1, 1, 2, 3, 4, 5],
              "bootstrap_features": [True, False]
             }

asdf = BaggingRegressor()

#clf_CC = GridSearchCV(asdf, param_grid=param_grid, scoring='r2' )
#clf_Fat = GridSearchCV(asdf, param_grid=param_grid, scoring='r2')
clf_CC = RandomizedSearchCV(asdf, param_grid, scoring='r2'  )
clf_Fat = RandomizedSearchCV(asdf, param_grid, scoring='r2'  )

clf_CC.fit(X_train, Y_train_CC)
clf_Fat.fit(X_train, Y_train_Fat)

print(clf_CC.best_estimator_)
'''


# In[ ]:


#print(clf_Fat.best_estimator_)


# Please upvote if you like this solution
