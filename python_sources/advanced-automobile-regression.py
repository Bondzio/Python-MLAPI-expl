#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score   # for mean ,vairance and diff from pred and actual
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


get_ipython().system('ls "../input/"')


# #### This data set consists of three types of entities: (a) the specification of an auto in terms of various characteristics, (b) its assigned insurance risk rating, (c) its normalized losses in use as compared to other cars. The second rating corresponds to the degree to which the auto is more risky than its price indicates. Cars are initially assigned a risk factor symbol associated with its price. Then, if it is more risky (or less), this symbol is adjusted by moving it up (or down) the scale. Actuarians call this process "symboling". A value of +3 indicates that the auto is risky, -3 that it is probably pretty safe.
# 
# #### The third factor is the relative average loss payment per insured vehicle year. This value is normalized for all autos within a particular size classification (two-door small, station wagons, sports/speciality, etc...), and represents the average loss per car per year.

# In[ ]:


#import data set
df=pd.read_csv('../input/automobile-from-california/imports-85.csv')
df.head()


# #### Exploration Dataset to know null values

# In[ ]:


# print bool if any  index in train set have null value every rows = df['gas'].isnull()
# df.gas.isnull().any() print if exist at least one value is null 

df.gas.isnull()


# In[ ]:


df.isnull().any()  # for every colum print bool if exist at least one value is null

df.dtypes  # print every data type in data set object rep ---> string not int , not float


# In[ ]:


# Exist '?' in columns in dataset .. so add columns in dataset from description file  

col=['symboling','normalized_losses','make','fuel_type','aspiration','num_of_doors','body_style','drive_wheels','engine_locatio','wheel_base'
     ,'length','width','height','curb_weight','engine_type','num_of_cylinders','engine_size','fuel_system'
     ,'bore','stroke','compression_ratio','horsepower','peak_rpm','city_mpg','highway_mpg','price']


# In[ ]:


df.index
# header -1 remove header na_values='?' replace  ? by NAN and add cloum(names) to headrer
df=pd.read_csv('../input/automobile-from-california/imports-85.csv',header =None,na_values='?',names=col) 


# In[ ]:


df.head()


# #### Second step remove NaN values from Dataset with :
# 1. by Mean 
# 2. by remove row from data
# 3. take random values from dataset column

# In[ ]:


print(df.isnull().any())
#df.columns[df.isnull().any]   print columns that has misssing data "NAN"
print(df[df.columns[df.isnull().any()]].isnull().sum()) # print the summation if train points has missing values


# In[ ]:


# print every missing data with her column and row 
df[df.isnull().any(axis=1)][df.columns[df.isnull().any()]] 


# #### droping not necessary colummns(Attributes)

# In[ ]:


df.drop(['make','symboling','normalized_losses'],axis=1,inplace=True)   #drop un unsed values in data 
df.head()


# ### missing data and change it by good value to predict perfect  [](http://)

# In[ ]:


df[df.num_of_doors.isnull()] # print missing values bt row , column in num_of_doors
df.num_of_doors[df.body_style=='sedan'].value_counts()   #take value of another attribute and get high count of num_of_doors 
df.loc[27,'num_of_doors']='four'   #change the value of missing data to the highest value predict in another attribute of data
df.loc[63,'num_of_doors']='four'


# In[ ]:


df[df.bore.isnull()]
df.bore.fillna(df.bore.mean(),inplace=True) #replave the missing data by mean of bore by using fillna method

df[df.stroke.isnull()]         #the change missing data to depenent data only not to y
 
df.stroke.fillna(df.stroke.mean(),inplace=True)

df.horsepower.fillna(df.horsepower.mean(),inplace=True)

df.peak_rpm.fillna(df.peak_rpm.mean(),inplace=True)

df.drop(df[df.price.isnull()].index,axis=0,inplace=True)      #if exist any missing data in Y delte it and delet trainging point all

df[df.columns[df.isnull().any()]].isnull().sum() #this line to check if exist any missing data or not


# ####   Encoding the text 'Categorical values'  
# 1. first method by your hand
# 2. second method by get dummies from pandas lib

# In[ ]:


# first method
df.num_of_cylinders.value_counts()      #for num_of_cylinders
df.loc[df.num_of_cylinders=='two','num_of_cylinders']=2
df.loc[df.num_of_cylinders=='four','num_of_cylinders']=4
df.loc[df.num_of_cylinders=='five','num_of_cylinders']=5
df.loc[df.num_of_cylinders=='six','num_of_cylinders']=6
df.loc[df.num_of_cylinders=='seven','num_of_cylinders']=7
df.loc[df.num_of_cylinders=='eight','num_of_cylinders']=8
df.loc[df.num_of_cylinders=='twelve','num_of_cylinders']=12
df.loc[df.num_of_cylinders=='three','num_of_cylinders']=3


# In[ ]:


#Seond method
col=['body_style','drive_wheels','engine_locatio','engine_type','fuel_system','num_of_doors','aspiration',
     'fuel_type']
df=pd.get_dummies(df,columns=col,drop_first=True)


# ### divide trainging set to train and test

# In[ ]:


train,test=train_test_split(df,test_size=0.2,random_state=0)


# In[ ]:


y_train=train.price
y_test=test.price
train.drop('price',axis=1,inplace=True)
test.drop('price',axis=1,inplace=True)


# ### Make Model LinearRegression

# In[ ]:


regressor=LinearRegression()
regressor.fit(train,y_train)

y_pred=regressor.predict(test)


# In[ ]:


actual_data=np.array(y_test)
for i in range(len(y_pred)):
    expl=((actual_data[i]-y_pred[i])/actual_data[i])*100.0
    print('Actual Value ${:,.2f},Predicted value ${:,.2f} (%{:,.2f})'.format(actual_data[i],y_pred[i],expl))


# ### calc perforamnce of Data in train and test

# In[ ]:


#calc perforamnce of Data in train and test
r_square=r2_score(y_test,y_pred)*100.0  #in LinearRegression not exist accuracy exist the r2_square to calc diff**2 between predict and actual 
r_train=r2_score(y_train,regressor.predict(train))*100.0
print('Accuracy of Test,Predict  Data  is %{:,.2f}'.format(r_square))
print('Accuracy of Train Data is %{:,.2f}'.format(r_train))


# ### plotting data

# In[ ]:


plt.scatter(y_pred,y_test,color='blue')
plt.title('Automobile Data set represntation')
plt.show()


# In[ ]:




