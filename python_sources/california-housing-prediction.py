#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
Cal_house_file_path= '../input/california-housing-prices/housing.csv'
Cal_house_data= pd.read_csv(Cal_house_file_path)
Cal_house_data.info()


# In[ ]:


Cal_house_data.head()


# Lets analyse this data closely. First let's check for missing values.

# In[ ]:


Cal_house_data.isnull().sum()


# Since total_bedrooms contains missing values, we must clean the data. We have two options: 1) Because it only has 207 rows out of 20640 that are missing, we can just drop the rows that have missing values. Or 2) we can use imputation. 

# It's more simple just to drop the rows so let's make a dataframe of just dropping the 207 rows of null values

# In[ ]:


#dropping rows with null
Cal_house_data_nonull= Cal_house_data.dropna(axis = 0, how ='any')
print("Cal_house_data length:", len(Cal_house_data), "\nCal_house_data_nonull length:",  
       len(Cal_house_data_nonull), "\nNumber of rows dropped: ", 
       (len(Cal_house_data)-len(Cal_house_data_nonull))) 


# Now let't see if imputation is an option to do. But I have a hunch that putting the median value wouldn't be too accurate so lets see if theres another variable that we can corelate with the sale value.
Breaking down the distributions of each column data:
# Coordinate and Price Distribution:

# In[ ]:


plt.figure(figsize=(14,12))
plt.scatter(Cal_house_data['longitude'],Cal_house_data['latitude'],c=Cal_house_data['median_house_value'],s=Cal_house_data['population']/10, cmap='inferno')
plt.colorbar()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Coodinates of Houses and Their Median House Value')
plt.show()


# This graph makes sense as the top [10 most expensive cities in California](https://moneyinc.com/most-expensive-cities-in-california-in-2019/) are San Francisco, Newport Beach, San Jose, Oakland, Santa Cruz, Napa, Montecito, Los Angeles, Santa Barbara, and San Diego.

# Now, because sale price is what we are truly looking for as the output, let's analyse the distribution of the data.

# In[ ]:


plt.figure(figsize=(15,5))
sns.distplot(Cal_house_data['median_house_value'],color='blue')
plt.xlabel('Median House Value')
plt.title('Distribution of Median House Value')
plt.show()


# It looks like there are outliers at around median_house_value 500000. Let's take out the outliers then.

# In[ ]:


Cal_house_data[Cal_house_data['median_house_value']>450000]['median_house_value'].value_counts().head()
Cal_house_data_outlier=Cal_house_data.loc[Cal_house_data['median_house_value']<500001,:]
plt.figure(figsize=(15,5))
sns.distplot(Cal_house_data_outlier['median_house_value'], color = 'blue')
plt.xlabel('Median House Value')
plt.title('Distribution of Median House Value with Outliers Taken Out')
plt.show()


# Now lets look at the population column data:

# In[ ]:


plt.figure(figsize=(10,5))
sns.boxplot(y='population',data=Cal_house_data_outlier)
plt.ylabel('Population')
plt.title('Distribution of Population Data')
plt.plot


# We can se that there are also outliers in the population data. Let's see how many outliers there are.

# In[ ]:


Cal_house_data_outlier[Cal_house_data_outlier['population']>15000]['population'].value_counts().head()


# Let's take out those outliers.

# In[ ]:


Cal_house_value_and_pop_outliers=Cal_house_data_outlier.loc[Cal_house_data['median_house_value']<15037,:]
Cleaned_cal_house=Cal_house_value_and_pop_outliers
plt.figure(figsize=(10,5))
sns.boxplot(y='population',data=Cleaned_cal_house)
plt.ylabel('Population')
plt.title('Distribution of Population Data without Outliers')
plt.plot


# Now that we've cleaned the data of most outliers let's see the correlation between all the variables. 

# In[ ]:


Cleaned_cal_house= Cleaned_cal_house.dropna(axis = 0, how ='any')
plt.figure(figsize=(11,7))
sns.heatmap(cbar=False,annot=True,data=Cleaned_cal_house.corr()*100,cmap='coolwarm')
plt.title('Corelation Matrix')
plt.show()


# Time to Preprocess Data

# In[ ]:


Cleaned_cal_house=pd.concat([pd.get_dummies(Cleaned_cal_house['ocean_proximity'],drop_first=True),Cleaned_cal_house],axis=1).drop('ocean_proximity',axis=1)
Cleaned_cal_house['income per working population']=Cleaned_cal_house['median_income']/(Cleaned_cal_house['population']-Cleaned_cal_house['households'])
Cleaned_cal_house['bed per house']=Cleaned_cal_house['total_bedrooms']/Cleaned_cal_house['total_rooms']
Cleaned_cal_house['h/p']=Cleaned_cal_house['households']/Cleaned_cal_house['population']
def type_building(x):
    if x<=10:
        return "new"
    elif x<=30:
        return 'mid old'
    else:
        return 'old'
Cleaned_cal_house=pd.concat([Cleaned_cal_house,pd.get_dummies(Cleaned_cal_house['housing_median_age'].apply(type_building),drop_first=True)],axis=1)
x=Cleaned_cal_house.drop('median_house_value',axis=1).values
y=Cleaned_cal_house['median_house_value'].values


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_valid,y_train,y_valid=train_test_split(x,y,test_size=0.3,random_state=0)


# In[ ]:


from sklearn.preprocessing import MinMaxScaler
ms=MinMaxScaler()
X_train=ms.fit_transform(X_train)
X_valid=ms.transform(X_valid)


# In[ ]:


from scipy import stats
from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV
my_model_xgb = XGBRegressor(objective = 'neg_mean_squared_error')
param_dist = {'n_estimators': stats.randint(150, 500),
              'learning_rate': stats.uniform(0.01, 0.07),
              'max_depth': [3, 4, 5, 6, 7, 8, 9],
              'colsample_bytree': stats.uniform(0.5, 0.45),
              'min_child_weight': [1, 2, 3]
             }

model_xgb_crossval = RandomizedSearchCV(my_model_xgb, param_distributions = param_dist, n_iter = 25, scoring = 'neg_mean_squared_error', error_score = 0, verbose = 3, n_jobs = -1)

model_xgb_crossval.fit(X_train, y_train)
from sklearn.metrics import mean_squared_error
model_xgb_crossval_fitted = model_xgb_crossval.predict(X_valid)


# In[ ]:


mae_2 = mean_squared_error(predictions_2, y_valid)


# In[ ]:


print("Mean Absolute Error:" , mae_2)


# In[ ]:




