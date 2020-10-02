#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import warnings
warnings.filterwarnings('ignore')


# In[ ]:


pd.set_option('display.max_column',None)


# In[ ]:


car_data = pd.read_csv("../input/vehicle-dataset-from-cardekho/car data.csv")


# In[ ]:


print("No of rows:",car_data.shape[0])
print("No of columns:",car_data.shape[1])


# In[ ]:


car_data.head()


# In[ ]:


### In this data set we are going to predict price in lakhs 
car_data.info()


# In[ ]:


car_data.nunique()


# In[ ]:


car_data.describe(exclude='O')


# #### In the data set we had a car collection from 2013-2018 of 98 different models
# #### in this Kms 75% data are bvelow 50k(total km drived) but we had a max value of 5lakhs
# #### This might be a Yellow board (not only for private use) and selling price is almost 
# #### 50% reduced then the cost price and also we can infer that Luxury car above 10lakhs
# #### had a very huge drop in selling price  and the reason behind that is Rich people
# #### usually won't prefer Second hand Luxury cars

# In[ ]:


car_data[car_data['Present_Price']>50]


# In[ ]:


np.unique(car_data['Car_Name'])


# In[ ]:


car_data['Years_old']=2020-car_data['Year']


# In[ ]:


### Top 10 car in our data for sales
plt.figure(figsize=(15,10))
sns.countplot(car_data['Car_Name'], palette='spring_r', 
              order=pd.value_counts(car_data['Car_Name']).iloc[:10].index)
plt.title('Market Segment Types', weight='bold')
plt.xlabel('Market Segment', fontsize=12)
plt.ylabel('Count', fontsize=12)


# In[ ]:


car_data[['Selling_Price','Present_Price']].plot(kind='line')
plt.ylabel('Price in lakhs',fontsize=10)
plt.xlabel('index')


# In[ ]:



k = list(map(float.__truediv__,(car_data['Present_Price']-car_data['Selling_Price']),car_data['Present_Price']))
car_data['Pct_decresed_per_yr'] = list(map(float.__truediv__,k*1000,car_data['Years_old']))
car_data['Pct_decresed_per_yr'] = car_data['Pct_decresed_per_yr'].apply(lambda x: round(x*100,3))


# In[ ]:


car_data.head()#.drop('Pct_decresed',inplace=True,axis=1)


# In[ ]:


### Df shows pct of car amount decreasing per year
pct_dec=pd.DataFrame(car_data.groupby('Car_Name').mean()['Pct_decresed_per_yr'].nlargest(20))
pct_dec.style.background_gradient(cmap='hsv_r')


# In[ ]:


### pct decresed from descending order
pct_dec=pd.DataFrame(car_data.groupby('Car_Name').mean()['Pct_decresed_per_yr'].nsmallest(20))
pct_dec.style.background_gradient(cmap='YlGn',subset=["Pct_decresed_per_yr"])


# In[ ]:


plt.figure(figsize=(10,10))
sns.distplot(car_data['Pct_decresed_per_yr'])
plt.title("Pct wise distribution plot",fontsize=15,weight='bold')
plt.ylabel('%% of vehicle')
plt.tight_layout()


# In[ ]:


car_data.head(2)


# In[ ]:


car_data['Years_old'] = car_data['Years_old'].astype(float)
car_data['Kms_Driven'] = car_data['Kms_Driven'].astype(float)


# In[ ]:



car_data['Kms_driven_per_yr']=list(map(float.__truediv__,car_data['Kms_Driven'],car_data['Years_old']))
car_data['Kms_driven_per_yr'] = car_data['Kms_driven_per_yr'].apply(lambda x: round(x,2))
car_data['Avg_kms_driven_per_month'] = car_data['Kms_driven_per_yr'].apply(lambda x: round(x/12,2))
car_data['Avg_kms_driven_per_day'] = car_data['Kms_driven_per_yr'].apply(lambda x: round(x/365,2))


# In[ ]:


car_data


# In[ ]:


### Df shows Avg of Vehicle running per day based on Company 
pct_dec=pd.DataFrame(car_data.groupby('Car_Name').mean()['Avg_kms_driven_per_day'].nlargest(20))
pct_dec.style.background_gradient(cmap='hsv_r')


# In[ ]:


car_data['Car_Name'] = car_data['Car_Name'].str.replace('Honda Activa 4G','Activa 4g')


# In[ ]:


### Df shows Avg of Vehicle running per day based on Company 
pct_dec=pd.DataFrame(car_data.groupby('Car_Name').mean()['Avg_kms_driven_per_day'].nsmallest(20))
pct_dec.style.background_gradient(cmap='hsv_r')


# In[ ]:


plt.figure(figsize=(15,8))
car_data['Year'].value_counts().iloc[:10,].plot(kind='bar',cmap='viridis')
plt.title('Most selling model in our datasetd',fontsize=15)
plt.xlabel('Year',fontsize=10)
plt.ylabel('No of vehicle',fontsize=10)


# In[ ]:


car_data.head(2)


# In[ ]:


sns.pairplot(car_data)


# ## Model Building

# In[ ]:


car_model = car_data.drop(['Car_Name','Year','Kms_driven_per_yr','Avg_kms_driven_per_month'],axis=1)


# In[ ]:


### Label encoding

from sklearn.preprocessing import LabelEncoder
lbe = LabelEncoder()


# In[ ]:


car_model['Fuel_Type'] = lbe.fit_transform(car_model['Fuel_Type'])
car_model['Seller_Type'] = lbe.fit_transform(car_model['Seller_Type'])
car_model['Transmission'] = lbe.fit_transform(car_model['Transmission'])


# In[ ]:


X = car_model.iloc[:,1:]
y = car_model['Selling_Price']


# In[ ]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()


# In[ ]:


column=X.columns
fitted = sc.fit_transform(X)
X = pd.DataFrame(fitted,columns=column)


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y ,random_state=42,test_size=.25)


# In[ ]:


# Random Forest Model Building
from sklearn.ensemble import RandomForestRegressor
rf_model = RandomForestRegressor(min_samples_leaf = 6, min_samples_split=6,
                                  n_estimators = 100)

# fit the model
estimator= rf_model.fit(X_train, y_train)
#Predict Model
predict_rf = rf_model.predict(X_test)


# In[ ]:


from sklearn.metrics import mean_squared_error,r2_score
print("MSE value is : ",mean_squared_error(y_test,predict_rf))
print("r2  value is : ",r2_score(y_test,predict_rf))
r2 = r2_score(y_test,predict_rf)
n = len(X_test)
k = X_test.shape[1]
adj_r2_score = 1 - (((1- r2)*(n-1)) / (n - k - 1))
print("adj_r2_score  value is : ",adj_r2_score)


# In[ ]:


plt.scatter(y_test,predict_rf)
plt.xlabel('actual')
plt.ylabel('predict')


# In[ ]:


X_test.iloc[1,:]


# In[ ]:





# In[ ]:




