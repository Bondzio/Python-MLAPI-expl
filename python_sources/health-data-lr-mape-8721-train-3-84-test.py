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


# In[ ]:


health_df=pd.read_csv("../input/Big_Cities_Health_Data_Inventory.csv")
health_df.shape


# In[ ]:


health_df.describe()


# In[ ]:


health_df.info()


# In[ ]:


sum_value=health_df.isna().sum()
print("=========Null Value========")
print(sum_value)
print("=========Null Percentage=======")
print((sum_value)/len(health_df)*100)


# In[ ]:


health_df[health_df.duplicated()]


# In[ ]:


health_df.columns


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


health_df.head(20)


# In[ ]:


health_df.nunique()


# In[ ]:


num_var=['Year','Value']
cat_var=[]
for i in health_df.columns:
    if i not in num_var:
        cat_var.append(i)
cat_var


# In[ ]:


categorical=['Indicator Category','Gender','Race/ Ethnicity','Year']
fig, ax = plt.subplots(2, 2, figsize=(30, 40))
for variable, subplot in zip(categorical, ax.flatten()):
    cp=sns.countplot(health_df[variable], ax=subplot,order = health_df[variable].value_counts().index)
    cp.set_title(variable,fontsize=40)
    for label in subplot.get_xticklabels():
        label.set_rotation(90)
        label.set_fontsize(36)                
    for label in subplot.get_yticklabels():
        label.set_fontsize(36)        
        cp.set_ylabel('Count',fontsize=40)    
plt.tight_layout()


# **Above subplot was created inspired by Reference "https://towardsdatascience.com/how-to-perform-exploratory-data-analysis-with-seaborn-97e3413e841d".
# 
# Observation:
# 
# From Dataset we draw subplot, we get to know distribution count of categorical variables 
# 
# 1) with indicator category , we see following order
# 
#     1) HIV/AIDS
#     2) Injury & violence
#     3) Nutrition,Physical activity & obesity
#     4) Infectious Disease
#     5) Cancer
#     6) Maternal and child health
#     7) Behavioural health / abuse
#     8) Food safety
#     9) Life Expectancy
#     10) Demographics 
#     11) Tobacco
# 2) with Gender category, we see distribution is more on both, followed by female and male
# 
# 3) with Race category , we see distribution falls in below order
# 
#     1) All
#     2) White
#     3) Black
#     4) Hispanic
#     5) Asian
#     6) Other
#     7) Native American
#     8) Multiracial
#     9) American indian
#     
# 4) with respect to year category , we see more death in 2012 followed by 2013,2011,2010 & 2014    
# 
# **

# In[ ]:


plt.figure(figsize=(25,12))
cp=sns.countplot(x=health_df['Place'],data=health_df,order = health_df['Place'].value_counts().index)
cp.set_xticklabels(cp.get_xticklabels(),rotation=90,fontsize=18)
cp.set_xlabel('Year',fontsize=15)
cp.set_ylabel('Count',fontsize=18)


# we see more data in place category. From the data , We see that we can extract new feature state and see distribution for state variable

# In[ ]:


#health_df['Place'].value_counts()
health_df['State']=health_df['Place'].apply(lambda x: x.split(",")).str[1]


# In[ ]:


plt.figure(figsize=(25,12))
cp=sns.countplot(x=health_df['State'],data=health_df,order = health_df['State'].value_counts().index)
cp.set_xticklabels(cp.get_xticklabels(),rotation=90,fontsize=18)
cp.set_xlabel('State',fontsize=15)
cp.set_ylabel('Count',fontsize=18)


# **CA state has more death followed by TX,AZ,FL,NY....**

# In[ ]:


plt.figure(figsize=(25,12))
cp=sns.countplot(x=health_df['Year'],data=health_df)
cp.set_xticklabels(cp.get_xticklabels(),rotation=90,fontsize=18)
cp.set_xlabel('Year',fontsize=15)
cp.set_ylabel('Count',fontsize=18)


# In[ ]:


plt.figure(figsize=(25,12))
cp=sns.countplot(x=health_df['Indicator Category'],data=health_df,hue=health_df['Gender'],order = health_df['Indicator Category'].value_counts().index)
cp.set_xticklabels(cp.get_xticklabels(),rotation=90,fontsize=18)
cp.set_xlabel('Year',fontsize=15)
cp.set_ylabel('Count',fontsize=18)


# In[ ]:


plt.figure(figsize=(20, 10))
sns.boxplot(data=health_df)


# **Above graph shows that there is no relationship between gender and Indicator. however for some value like Cancer, we see more female prone to it than male. Sameway for maternal health it has only female value which is obvious here**

# In[ ]:


# Importing necessary package for creating model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score


# In[ ]:


cat_col=['Indicator Category','Gender','State','Race/ Ethnicity','Year']
num_col=['Value']
num_col


# In[ ]:


print(health_df.shape)
health_df_nona=health_df[(health_df['Value'].isna()==False) & (health_df['Value']!=0)]
health_df_nona.shape


# In[ ]:


# one-hot encoding

one_hot=pd.get_dummies(health_df_nona[cat_col])
health_procsd_df=pd.concat([health_df_nona[num_col],one_hot],axis=1)
health_procsd_df.head(10)


# In[ ]:


health_procsd_df.isna().sum()


# In[ ]:


#using one hot encoding
X=health_procsd_df.drop(columns=['Value'])
y=health_procsd_df[['Value']]


# In[ ]:


train_X, test_X, train_y, test_y = train_test_split(X,y,test_size=0.3,random_state=1234)


# In[ ]:


model = LinearRegression()

model.fit(train_X,train_y)


# In[ ]:


# Print Model intercept and co-efficent
print("Model intercept",model.intercept_,"Model co-efficent",model.coef_)


# In[ ]:


cdf = pd.DataFrame(data=model.coef_.T, index=X.columns, columns=["Coefficients"])
cdf


# In[ ]:


# Print various metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score

print("Predicting the train data")
train_predict = model.predict(train_X)
print("Predicting the test data")
test_predict = model.predict(test_X)
print("MAE")
print("Train : ",mean_absolute_error(train_y,train_predict))
print("Test  : ",mean_absolute_error(test_y,test_predict))
print("====================================")
print("MSE")
print("Train : ",mean_squared_error(train_y,train_predict))
print("Test  : ",mean_squared_error(test_y,test_predict))
print("====================================")
import numpy as np
print("RMSE")
print("Train : ",np.sqrt(mean_squared_error(train_y,train_predict)))
print("Test  : ",np.sqrt(mean_squared_error(test_y,test_predict)))
print("====================================")
print("R^2")
print("Train : ",r2_score(train_y,train_predict))
print("Test  : ",r2_score(test_y,test_predict))
print("MAPE")
print("Train : ",np.mean(np.abs((train_y - train_predict) / train_y)) * 100)
print("Test  : ",np.mean(np.abs((test_y - test_predict) / test_y)) * 100)


# In[ ]:


#Plot actual vs predicted value
plt.figure(figsize=(10,7))
plt.title("Actual vs. predicted expenses",fontsize=25)
plt.xlabel("Actual Value",fontsize=18)
plt.ylabel("Predicted Value", fontsize=18)
plt.scatter(x=test_y,y=test_predict)


# **Model is not predicting value correctly inspite of cleaned outlier (value=0 or nan). After removing nan or value=0 able to correct MAPE value which gives Infinity one. Need to futher pre-process data to achieve better result**

# In[ ]:


len(train_predict[train_predict==0])


# In[ ]:


test_predict


# In[ ]:


#cat_var_main=['Indicator Category','Gender','Race/ Ethnicity','Place']
#fig, ax = plt.subplots(3, 4, figsize=(20, 10))
#for variable, subplot in zip(cat_var, ax.flatten()):
    #sns.countplot(health_df[variable], ax=subplot)
    #for label in subplot.get_xticklabels():
        #label.set_rotation(90)


# In[ ]:


#sns.countplot(data=health_df,y=health_df["Value"])
#health_df.groupby("Indicator Category").agg('mean','median','mode')
#agg_funcs = dict(Size='size', Sum='sum', Mean='mean', Std='std', Median='median')
#health_df.set_index(['Indicator Category','State']).stack().shape
agg_func=dict(Count='count',Avg='mean',Median='median',Deviation='std',Min='min',Max='max')
health_df.groupby("Indicator Category").agg({
        'Value': agg_func,
    }).sort_values(('Value', 'Count'))


# In[ ]:


plt.figure(figsize=(30, 20))
sns.boxplot(data=health_df,x=health_df["Indicator Category"],y=health_df["Value"])


# In[ ]:


plt.figure(figsize=(30, 20))
cp=sns.boxplot(data=health_df,x=health_df["Indicator Category"],y=health_df["Value"],showfliers=False)
cp.set_xticklabels(cp.get_xticklabels(),rotation=90,fontsize=18)
#cp.set_yticklabels(cp.get_yticklabels(),fontsize=18)
cp.set_xlabel("Race/ Ethnicity",fontsize=15)
cp.set_ylabel('Value',fontsize=18)


# In[ ]:


agg_func=dict(Count='count',Avg='mean',Median='median',Deviation='std',Min='min',Max='max')
health_df.groupby("State").agg({
        'Value': agg_func,
    }).sort_values(('Value', 'Count'))


# In[ ]:


plt.figure(figsize=(30, 20))
sns.boxplot(data=health_df,x=health_df["State"],y=health_df["Value"])


# In[ ]:


plt.figure(figsize=(30, 20))
cp=sns.boxplot(data=health_df,x=health_df["State"],y=health_df["Value"],showfliers=False)
cp.set_xticklabels(cp.get_xticklabels(),rotation=90,fontsize=18)
#cp.set_yticklabels(cp.get_yticklabels(),fontsize=18)
cp.set_xlabel("Race/ Ethnicity",fontsize=15)
cp.set_ylabel('Value',fontsize=18)


# In[ ]:


agg_func=dict(Count='count',Avg='mean',Median='median',Deviation='std',Min='min',Max='max')
health_df.groupby("Gender").agg({
        'Value': agg_func,
    }).sort_values(('Value', 'Count'))


# In[ ]:


plt.figure(figsize=(30, 20))
sns.boxplot(data=health_df,x=health_df["Gender"],y=health_df["Value"])


# In[ ]:


plt.figure(figsize=(30, 20))
cp=sns.boxplot(data=health_df,x=health_df["Gender"],y=health_df["Value"],showfliers=False)
cp.set_xticklabels(cp.get_xticklabels(),rotation=90,fontsize=18)
#cp.set_yticklabels(cp.get_yticklabels(),fontsize=18)
cp.set_xlabel("Race/ Ethnicity",fontsize=15)
cp.set_ylabel('Value',fontsize=18)


# In[ ]:


agg_func=dict(Count='count',Avg='mean',Median='median',Deviation='std',Min='min',Max='max')
health_df.groupby("Race/ Ethnicity").agg({
        'Value': agg_func,
    }).sort_values(('Value', 'Count'))


# In[ ]:


plt.figure(figsize=(30, 20))
sns.boxplot(data=health_df,x=health_df["Race/ Ethnicity"],y=health_df["Value"])


# **Since outlier spoils visualization, we can show it filtering outliers using showfliers=False**

# In[ ]:


plt.figure(figsize=(30, 20))
cp=sns.boxplot(data=health_df,x=health_df["Race/ Ethnicity"],y=health_df["Value"],showfliers=False)
cp.set_xticklabels(cp.get_xticklabels(),rotation=90,fontsize=18)
#cp.set_yticklabels(cp.get_yticklabels(),fontsize=18)
cp.set_xlabel("Race/ Ethnicity",fontsize=15)
cp.set_ylabel('Value',fontsize=18)


# In[ ]:


agg_func=dict(Count='count',Avg='mean',Median='median',Deviation='std',Min='min',Max='max')
health_df.groupby("Year").agg({
        'Value': agg_func,
    }).sort_values(('Value', 'Count'))


# In[ ]:


len(health_procsd_df[health_procsd_df.Value==0])


# In[ ]:


health_df.head(10)


# **Now we can compare value against two categorical variable. Crosstab gives good way to compare two categorical value with Target value. Various usage of crosstab was inspired by below link**
# 
# https://pbpython.com/pandas-crosstab.html

# In[ ]:


pd.crosstab(health_df["State"],health_df["Indicator Category"], values=health_df.Value, aggfunc=['mean'],dropna=False,margins=True,margins_name="Total Mean")


# In[ ]:


pd.crosstab(health_df["State"],health_df["Indicator Category"], values=health_df.Value, aggfunc='median',dropna=False,margins=True,margins_name="Total Mean")


# In[ ]:


pd.crosstab(health_df["Race/ Ethnicity"],health_df["Indicator Category"], values=health_df.Value, aggfunc='mean',dropna=False,margins=True,margins_name="Total Mean")


# In[ ]:


pd.crosstab(health_df["Race/ Ethnicity"],health_df["Indicator Category"], values=health_df.Value, aggfunc='median',dropna=False,margins=True,margins_name="Total Mean")


# In[ ]:


table=pd.crosstab(health_df["Gender"],health_df["Indicator Category"], values=health_df.Value, aggfunc='mean',dropna=False,margins=True,margins_name="Total Mean")
table


# In[ ]:


pd.crosstab(health_df["Gender"],health_df["Indicator Category"], values=health_df.Value, aggfunc='median',dropna=False,margins=True,margins_name="Total Mean")


# **Clearly we see outliers there when we do comparison between mean and median values**

# In[ ]:


health_df[health_df.duplicated()==True]


# In[ ]:


lower_bnd = lambda x: x.quantile(0.25) - 1.5 * ( x.quantile(0.75) - x.quantile(0.25) )
upper_bnd = lambda x: x.quantile(0.75) + 1.5 * ( x.quantile(0.75) - x.quantile(0.25) )


# In[ ]:


health_df.shape


# In[ ]:


health_df_clean = health_df[(health_df["Value"] >= lower_bnd(health_df["Value"])) & (health_df["Value"] <= upper_bnd(health_df["Value"])) ] 


# In[ ]:


health_df_clean.shape


# In[ ]:


print(health_df_clean.shape)
health_df_clean_nona=health_df_clean[(health_df_clean['Value'].isna()==False) & (health_df_clean['Value']!=0)]
health_df_clean_nona.shape


# In[ ]:


# one-hot encoding

one_hot=pd.get_dummies(health_df_clean_nona[cat_col])
health_procsd_df=pd.concat([health_df_clean_nona[num_col],one_hot],axis=1)
health_procsd_df.head(10)


# In[ ]:


#using one hot encoding
X=health_procsd_df.drop(columns=['Value'])
y=health_procsd_df[['Value']]


# In[ ]:


train_X, test_X, train_y, test_y = train_test_split(X,y,test_size=0.3,random_state=1234)


# In[ ]:


model = LinearRegression()

model.fit(train_X,train_y)


# In[ ]:


# Print Model intercept and co-efficent
print("Model intercept",model.intercept_,"Model co-efficent",model.coef_)


# In[ ]:


# Print various metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score

print("Predicting the train data")
train_predict = model.predict(train_X)
print("Predicting the test data")
test_predict = model.predict(test_X)
print("MAE")
print("Train : ",mean_absolute_error(train_y,train_predict))
print("Test  : ",mean_absolute_error(test_y,test_predict))
print("====================================")
print("MSE")
print("Train : ",mean_squared_error(train_y,train_predict))
print("Test  : ",mean_squared_error(test_y,test_predict))
print("====================================")
import numpy as np
print("RMSE")
print("Train : ",np.sqrt(mean_squared_error(train_y,train_predict)))
print("Test  : ",np.sqrt(mean_squared_error(test_y,test_predict)))
print("====================================")
print("R^2")
print("Train : ",r2_score(train_y,train_predict))
print("Test  : ",r2_score(test_y,test_predict))
print("MAPE")
print("Train : ",np.mean(np.abs((train_y - train_predict) / train_y)) * 100)
print("Test  : ",np.mean(np.abs((test_y - test_predict) / test_y)) * 100)


# In[ ]:


#Plot actual vs predicted value
plt.figure(figsize=(10,7))
plt.title("Actual vs. predicted expenses",fontsize=25)
plt.xlabel("Actual Value",fontsize=18)
plt.ylabel("Predicted Value", fontsize=18)
plt.scatter(x=test_y,y=test_predict)


# In[ ]:


chk_val=pd.DataFrame(pd.np.column_stack([test_y,test_predict]))
chk_val[2]=(chk_val[0]-chk_val[1])
chk_val


# In[ ]:


agg_func=dict(Count='count',Avg='mean',Median='median',Deviation='std',Min='min',Max='max')
health_df.groupby(["Indicator Category","Race/ Ethnicity"]).agg({
        'Value': agg_func,
    }).sort_values(('Value', 'Count'))


# **We will try to implement knn for this Linear regression to see how accuracy calculated**

# In[ ]:


from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size = 0.3, random_state = 100)
y_train=np.ravel(y_train)
y_test=np.ravel(y_test)


# In[ ]:


k = 5
#Train Model and Predict  
neigh = KNeighborsRegressor(n_neighbors = k).fit(X_train,y_train)
neigh


# In[ ]:


### Predicting
#we can use the model to predict the test set:

yhat = neigh.predict(X_test)
yhat[0:5]


# In[ ]:


mean_squared_error(y_test,yhat)


# In[ ]:


yhat_train = neigh.predict(X_train)
yhat_train[0:5]


# In[ ]:


mean_squared_error(y_train,yhat_train)


# **I Tried increase K value from 3 to 11 and found that k-value lower for K=5 . will try to validate same in elbow curve**

# In[ ]:




