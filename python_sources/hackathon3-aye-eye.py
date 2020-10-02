#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Installing libraries
get_ipython().system('pip install regressors')

import numpy as np 
import pandas as pd 
import os
import statsmodels.formula.api as sm
import statsmodels.sandbox.tools.cross_val as cross_val
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model as lm
from regressors import stats
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score,cross_val_predict, LeaveOneOut

print(os.listdir("../input"))


# In[5]:


d = pd.read_csv("../input/train.csv")
d['space'] = ' '
d['Time2'] = d['Date'] + d['space'] + d['Time']
d.head()


# In[6]:


d = d.drop(columns=['Id','Date','Time'])
d.head()


# In[7]:


print(d.dtypes)


# In[8]:


d['Time3'] = pd.to_datetime(d['Time2'])
d['Time4'] = pd.to_timedelta(d.Time3).dt.total_seconds().astype(int)
print(d.dtypes)
d.head()


# In[9]:


d = d.drop(columns=['Time2','Time3','space'])
d.head()


# In[10]:


#checking for null/NaN values
print("Check for NaN/null values:\n", d.isnull().values.any())
print("Number of NaN/null values:\n", d.isnull().sum())


# In[11]:


weather = d["Weather"]
print("Value Count:\n",d["Weather"].value_counts())
print("-------------------")
season = d["Season"]
print("Value Count:\n",season.value_counts())
print("-------------------")


# In[12]:


#d = pd.get_dummies(d, prefix=['Weather'], columns=['Weather'])
#d.head()


# In[13]:


d['Weather'] = d['Weather'].map({'Clear': 0, 'Cloudy': 1, 'Light Rain':2, 'Heavy Rain':3})
d['Season'] = d['Season'].map({'Spring': 0, 'Summer': 1, 'Winter':2, 'Fall':3})
d.head()


# In[14]:


# d = d.drop(columns=['Weather','Season'])
# d.head()
d=d.dropna()
print(d.dtypes)


# In[15]:


corr = d.corr().abs().unstack().sort_values()
pd.set_option('display.max_rows', None)  
print (corr)


# In[16]:


#checking for null/NaN values
print("Check for NaN/null values:\n", d.isnull().values.any())
print("Number of NaN/null values:\n", d.isnull().sum())


# In[ ]:





# In[ ]:





# In[ ]:





# # Forward Selection - Main effects 

# In[17]:


from mlxtend.feature_selection import SequentialFeatureSelector as sfs


# In[18]:


inputDF = d.loc[:, d.columns != 'Demand']
outputDF = d[["Demand"]]

model = sfs(LinearRegression(),k_features=5,forward=True,verbose=2,cv=5,n_jobs=-1,scoring='r2')
model.fit(inputDF,outputDF)
#this is only showing main effects


# In[19]:


#Selected feature index.
model.k_feature_idx_


# In[20]:


#Column names for the selected feature.
model.k_feature_names_


# # Backward Selection - main effects 

# In[21]:


inputDF = d.loc[:, d.columns != 'Demand']
outputDF = d[["Demand"]]

backwardmodel = sfs(LinearRegression(),k_features=5,forward=False,verbose=2,cv=5,n_jobs=-1,scoring='r2')
#forward changed to false
backwardmodel.fit(inputDF,outputDF)
#this is only showing main effects


# In[22]:


#Selected feature index.
backwardmodel.k_feature_idx_


# In[23]:


#Column names for the selected feature.
backwardmodel.k_feature_names_


# In[24]:


print(d.columns.values)


# In[25]:


#kFCV: Scikit-Learn
inputDF = d.loc[:, d.columns != 'Demand']
outputDF = d[["Demand"]]
model = LinearRegression()
kf = KFold(5, shuffle=True, random_state=42).get_n_splits(inputDF)
rmse = np.sqrt(-cross_val_score(model, inputDF, outputDF, scoring="neg_mean_squared_error", cv = kf))
print(rmse.mean())
results = model.fit(inputDF,outputDF)


# In[ ]:





# In[ ]:





# In[ ]:





# In[26]:


select=list(d.columns.values)
max_rsq = 0.1
for primary in range(0,10):
    if primary==8:
        continue
    for secondary in range(1,5):
        string = "Demand ~ np.power(" + select[primary] +", "+ str(secondary) +")"   # np.power(Temp,4)
        res_trial = sm.ols(formula=string,data=d).fit()
        if res_trial.rsquared>max_rsq:
            max_rsq= res_trial.rsquared
            print('\n\n',string,'----->' ,res_trial.summary())


# In[ ]:





# In[27]:


select=list(d.columns.values)
max_rsq = 0.1
for primary in range(0,10):
    if primary==8:
        continue
    for secondary in range(primary,10):
        if secondary==8:
            continue
        for tertiary in range(secondary,10):
            if tertiary==8:
                continue
            for quaternary in range(tertiary,10):
                if quaternary==8:
                    continue
                string = "Demand ~ " + select[primary] + "*" +select[secondary]+"*"+select[tertiary]+"*"+select[quaternary]
                res_trial = sm.ols(formula=string,data=d).fit()
                if res_trial.rsquared>max_rsq:
                    max_rsq = res_trial.rsquared
                    print('\n\n',string,'----->' ,res_trial.summary())


# In[ ]:





# In[28]:


res = sm.ols(formula="Demand ~  Season*AdoptedTemperature*Humidity*Time4 + Temperature*AdoptedTemperature*Humidity*Time4 +Temperature*Season*Humidity*Time4+  Temperature*WindSpeed*Humidity*Time4 +Weather*AdoptedTemperature*Humidity*Time4 +  Weather*Temperature*Humidity*Time4 + Weather*Temperature*Season*Humidity + IsWorkingDay*WindSpeed*AdoptedTemperature*Humidity + IsWorkingDay*Temperature*Humidity*Time4 + IsWorkingDay*Temperature*AdoptedTemperature*Humidity + IsWorkingDay*Temperature*Season*Humidity + IsWorkingDay*Weather*AdoptedTemperature*Humidity + IsHoliday*Temperature*Humidity*Time4 + np.power(AdoptedTemperature,2) +AdoptedTemperature*Humidity*Time4+Temperature*Humidity*Time4+WindSpeed*AdoptedTemperature*Temperature +Humidity*Time4+IsHoliday+I(Weather*Weather) +Temperature + IsWorkingDay*Temperature  + Season + Temperature + Time4 * Season*Temperature + Weather*Humidity + np.power(Temperature,9)+ np.power(Temperature,8)",data=d).fit()
print(res.summary())


# ## Trial 2

# In[29]:


# import itertools

# stuff = ['IsHoliday', 'IsWorkingDay' ,'Weather','Temperature', 'WindSpeed' ,'Season',
#          'AdoptedTemperature', 'Humidity' ,'Time4']
# max_rsq = 0.3
# b=d[["Demand"]].values
# rmse_min=200
# for L in range(4, len(stuff)+1):
#     print(L)
#     a0=('+','*')
#     operationer=np.matlib.repmat(a0,1,L)
#     operationer=list(chain.from_iterable(operationer))
#     for subset in itertools.combinations(stuff, L):
#             for microset in itertools.combinations(operationer, L-1):
#                 result = [None]*(len(subset)+len(microset))
#                 result[::2] = subset
#                 result[1::2] = microset
# #                 print(''.join(result))
#                 tempo = ''.join(result)
#                 string = "Demand ~ " + tempo
#                 res_trial = sm.ols(formula=string,data=d).fit()
#                 a=res_trial.predict(d).values
#                 rmse = np.sqrt(((a-b) ** 2).mean())
#                 if rmse<rmse_min:
#                     rmse_min = rmse
# #                     max_rsq = res_trial.rsquared
#                     print('\n\n',string,'----->' ,rmse)

        
# # ('IsHoliday', 'IsWorkingDay', 'Weather')


# In[ ]:





# In[32]:


import itertools

# stuff = ['IsHoliday', 'IsWorkingDay' ,'Weather','Temperature', 'WindSpeed' ,'Season',
#          'AdoptedTemperature', 'Humidity' ,'Time4']
# max_rsq = 0.3
# for L in range(2, len(stuff)+1):
#     print(L)
#     for subset in itertools.combinations(stuff, L):
#             testing = subset[0]
#             for i in range(1, len(subset)):
#                 testing = testing + "*" + subset[i]
#             string = "Demand ~ " + testing
#             res_trial = sm.ols(formula=string,data=d).fit()
#             if res_trial.rsquared>max_rsq:
#                 max_rsq = res_trial.rsquared
#                 print('\n\n',string,'----->' ,res_trial.summary())
        
        
# ('IsHoliday', 'IsWorkingDay', 'Weather')


# In[33]:



stuff = ['IsHoliday', 'IsWorkingDay' ,'Weather','Temperature', 'WindSpeed' ,'Season']
for L in range(4, 6):
    for subset in itertools.permutations(stuff, L):
        print(subset)
    


# In[ ]:





# In[34]:



res = sm.ols(formula="Demand ~  IsHoliday+IsWorkingDay+WindSpeed ",data=d).fit()
# print(res_trial.predict(d))
# print(d[["Demand"]])
a=res.predict(d).values
b=d[["Demand"]].values
print(np.sqrt(((a-b) ** 2).mean()))


# In[ ]:





# In[ ]:





# In[ ]:


# res = sm.ols(formula="Demand~IsHoliday*IsWorkingDay*Time4 +  Weather*Temperature*WindSpeed*Season*AdoptedTemperature*Humidity+np.power(Temperature,5) ",data=d).fit()
# print(res.summary())


# In[ ]:





# In[ ]:





# # Predictions

# In[35]:


d2 = pd.read_csv("../input/test.csv")
d2['space'] = ' '
d2['Time2'] = d2['Date'] + d2['space'] + d2['Time']
d2 = d2.drop(columns=['Id','Date','Time'])
d2['Time3'] = pd.to_datetime(d2['Time2'])
d2['Time4'] = pd.to_timedelta(d2.Time3).dt.total_seconds().astype(int)
d2 = d2.drop(columns=['Time2','Time3','space'])
d2['Weather'] = d2['Weather'].map({'Clear': 0, 'Cloudy': 1, 'Light Rain':2, 'Heavy Rain':3})
d2['Season'] = d2['Season'].map({'Spring': 0, 'Summer': 1, 'Winter':2, 'Fall':3})
# print(d.dtypes)
# print(d.head())
# print(d2.head())
d2.head()


# In[36]:


ypred = res.predict(d2)
print(ypred.astype(int))


# In[38]:



submissionDF = pd.DataFrame({"Id": range(0,3000),"Demand":ypred.astype(int)})
submissionDF.to_csv('Submissionv1.csv',index=False)


# In[39]:


print(submissionDF)


# In[ ]:





# In[ ]:





# ## Prediction using sklearn

# In[ ]:


yp2 = model.predict(d2.loc[:, :])
print(yp2)


# In[ ]:


print(yp2.shape)


# In[ ]:


yp2_sk=pd.DataFrame({'Id':range(0,3000),'Demand':yp2[:,0]})


# In[ ]:


# submissionDF_sk = pd.DataFrame({'Id':range(0,3000),'Demand':yp2[:,0].astype(int)})
# submissionDF_sk.to_csv('Submissionv_sk.csv',index=False)


# In[ ]:


# print(submissionDF_sk)

