#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### Import OS 
#Import pandas as pd
#import geopy.distance 
#from geopy.distance import vincenty
#import seaborn as sns
#from matplotlib import pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D : For plotting 3d Graphs 
#import numpy as np

#Features added : 
#1. distance : Distance in miles 
#2. distance_in_kms
#3. ridetype : solo, double or shared
#4. pickup_month : month wise distribution of rides
#5. pickup_year : year wise distribution of rides 
#6. pickup_week : Week wise distribution of rides
#7. pickup_hour : Hourly distribution of rides

#Graphs 

#1. Correlation Graph for distance, passenger & fare.
#2. Bar plot displaying number for Ride Type: Solo, Double or Shared.
#3. Pair Grid : for preferred ride type on the basis of distance, passenger & fare.
#4. 3D Scatter Plot: displaying number of passengers & charges distributed as per the year.
#5. 3D Scatter Plot: displaying number of passengers & charges distributed as per the month.
#6. 3D Scatter Plot: displaying year wise charges per ride as per the hour
#7. barh Plot: Displaying mean charges month wise. 
#8. 3D Scatter Plot: Fare Amount as per Years, Months & Weeks.
#9. Bar Plot: Total Revenue generated from 2009 to 2015 every year.
#10. Pie Chart: Total Revenue generated every month from 2009 to 2015.
#11. barh Plot: Total Day wise revenue generated from 2009 to 2016 

#Test Prediction Models 
#1. Decision Tree 
#2. Random Forest 
#3. Linear Regression 
#4. Linear Support Vector Regression 
#5. KNN 
#6. Gradient Boosting 
#7. XGBoost 
#8. CatBoost Regressor = RMSE


# In[ ]:


import os 
os.chdir("../input")
os.listdir()


# In[ ]:


import pandas as pd


# In[ ]:


df = pd.read_csv("train.csv", nrows = 5000, parse_dates = ["pickup_datetime"]) # the whole data takes about 5 minutes
#Limiting it to 90000 rows, loading takes less than a minute


# In[ ]:


#Understanding the stucture of the DF 
df.columns  #Column names 


# In[ ]:


df.shape    #Number of rows & columns 


# In[ ]:


df.dtypes   #TYPES OF COLUMNS 


# In[ ]:


df.info()   #COMPLETE INFORMATION ABOUT THE DF


# In[ ]:


df.columns.values


# In[ ]:


df.head()


# In[ ]:


df.tail()


# In[ ]:


df.fare_amount.head()


# In[ ]:


df.isnull().sum() #Takes about 1 minute
#out of 55423855 entries only 376 is null. We can ignore these null values 


# In[ ]:


df.dtypes


# In[ ]:


df.describe()


# In[ ]:


df.isnull().sum()


# In[ ]:


#removing outliers for latitude & longitude
df = df.drop(((df[df['pickup_latitude']<-90])|(df[df['pickup_latitude']>90])).index, axis=0)


# In[ ]:


#Adding distance travelled using Vincenty. 
#Installed geopy using "pip install geopy" in anaconda terminal
import geopy.distance 
from geopy.distance import vincenty

def pandasVincenty(df):
    '''calculate distance (m) between two lat&long points using the Vincenty formula '''

    return vincenty((df.pickup_latitude, df.pickup_longitude), (df.dropoff_latitude, df.dropoff_longitude)).km


df['distance_in_kms'] =  df.apply(lambda r: pandasVincenty(r), axis=1)


# In[ ]:


df.describe()


# In[ ]:


df.head()


# In[ ]:


#Can do reverse geocoding using gmaps. Its paid for more than 1000 records
#from pygeocoder import Geocoder


# In[ ]:


#results = Geocoder.reverse_geocode(df['pickup_latitude'][0], df['pickup_longitude'][0])


# In[ ]:


df.distance_in_kms.describe()


# In[ ]:


df.distance_in_kms.describe()


# In[ ]:


df.groupby('passenger_count')['fare_amount', 'distance_in_kms'].mean()


# In[ ]:


#Fare per Kms
df.fare_amount.sum()/df.distance_in_kms.sum()


# In[ ]:


df.head()


# In[ ]:


#Categorising ride_type on the basis of number of passengers into : none, solo, share

df['ridetype'] = pd.cut(df.passenger_count, [0,1,2,6], labels=["solo","double","shared"])


# In[ ]:


df.dtypes


# In[ ]:


df.head(10)


# In[ ]:


#Formation of new table with columns: fare_amount, passenger_count, ridetype, distance

n_df = df[['fare_amount','passenger_count','ridetype','distance_in_kms']].copy()


# In[ ]:


n_df.head()


# In[ ]:


corr = n_df.corr()


# In[ ]:


import seaborn as sns
from matplotlib import pyplot as plt
plt.figure(figsize = (10,10))
sns.heatmap(corr, annot = True, annot_kws = {'size':15})


# In[ ]:


plt.figure(figsize = (10,10))
sns.countplot(x='ridetype', hue = 'passenger_count', data = n_df)


# In[ ]:


g = sns.PairGrid(n_df, hue="ridetype")
g = g.map_diag(plt.hist)
g = g.map_offdiag(plt.scatter)
g = g.add_legend()


# In[ ]:


#Adding month columns 
df['pickup_month'] = df['pickup_datetime'].dt.month


# In[ ]:


df.head()


# In[ ]:


#Adding Year Column 
df['pickup_year'] = df['pickup_datetime'].dt.year


# In[ ]:


df.head()


# In[ ]:


#Adding day column
df['pickup_day'] = df['pickup_datetime'].dt.weekday_name


# In[ ]:


df.head()


# In[ ]:


#Adding week column
df['pickup_week'] = df['pickup_datetime'].dt.week


# In[ ]:


df.head()


# In[ ]:


#Adding Hour Column
df['pickup_hour'] = df['pickup_datetime'].dt.hour


# In[ ]:


df.head()


# In[ ]:


#Relation between Passenger count, Fare & Year
from mpl_toolkits.mplot3d import Axes3D

threedee = plt.figure(figsize = (15,10)).gca(projection  = '3d')
threedee.scatter(df.index, df['fare_amount'], df['passenger_count'], c = df['pickup_year'])
threedee.set_xlabel('Index')
threedee.set_ylabel('Charges Per Ride')
threedee.set_zlabel('Number Of Passengers')
plt.show()


# In[ ]:


df.head()


# In[ ]:


threedee = plt.figure(figsize = (15,10)).gca(projection  = '3d')
threedee.scatter(df.index, df['fare_amount'], df['pickup_month'], c =df['pickup_month'])
threedee.set_xlabel('Index')
threedee.set_ylabel('Charges Per Ride')
threedee.set_zlabel('Month')
plt.show()


# In[ ]:


threedee = plt.figure(figsize = (15,10)).gca(projection  = '3d')
threedee.scatter(df['pickup_hour'], df['fare_amount'], df['pickup_year'], c=df['pickup_hour'])
threedee.set_xlabel('Pickup Hour')
threedee.set_ylabel('Charges Per Ride')
threedee.set_zlabel('Years')
plt.show()


# In[ ]:


#Mean fare monthwiswe 
plt.figure(figsize = (12,10))
#plt.barh(df['pickup_month'], df['fare_amount'])
df.groupby('pickup_month')['fare_amount'].mean().plot(kind = 'barh')
plt.xlabel('Mean Fare Amount')
plt.ylabel('Month wise distribution from 2009 to 2015')


# In[ ]:


threedee = plt.figure(figsize = (15,10)).gca(projection  = '3d')
threedee.scatter(df['pickup_year'], df['pickup_month'], df['pickup_week'], c = df['pickup_hour'], marker ='+')
threedee.set_xlabel('Year')
threedee.set_ylabel('Month')
threedee.set_zlabel('Week')
plt.show()


# In[ ]:


#group by year 
plt.figure(figsize = (12,10))
df.groupby(['pickup_year'])['fare_amount'].sum().plot(kind = 'bar')
plt.xlabel('Years from 2009 to 2015')
plt.ylabel('Total Revenue Generated Per Year')


# In[ ]:


#group by month 
plt.figure(figsize = (12,10))
df.groupby(['pickup_month'])['fare_amount'].sum().plot(kind = 'pie')
plt.xlabel('Pickup Every Month')
plt.ylabel('Revenue Generated Every Month Over the Years')


# In[ ]:


#Pickup Revenue Generated Day wise to know which day of the week has generaed maximum revenue over the years 
plt.figure(figsize = (12,10))
df.groupby(['pickup_day'])['fare_amount'].sum().plot(kind = 'barh')
plt.xlabel('Revenue Generated')
plt.ylabel('Day wise distribution of total revenue over the years')


# In[ ]:


df.head()


# In[ ]:


df.dtypes


# In[ ]:


#one-hot encode the data using pandas get_dummies

#df = pd.get_dummies(df)


# In[ ]:


df.head()


# In[ ]:


#Saving the features to a list  
#df_list = list(df.columns)
df.dtypes


# In[ ]:


#Coverting the df to to an array
#df = np.array(df)

#Creating Train & Test Data 

factors = df[['pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','passenger_count']]

response = df['fare_amount']


# In[ ]:


from sklearn.model_selection import train_test_split

testSize = 0.2

trainFactors, testFactors, trainResponse, testResponse = train_test_split(factors, response, test_size = testSize, random_state = 42)


# # 1.Decision Tree 

# In[ ]:


from sklearn import tree
dtr_model = tree.DecisionTreeRegressor(criterion = 'mse')


# In[ ]:


#Fitting of Decision Tree 

dtr_model.fit(trainFactors, trainResponse)


# In[ ]:


#DTR Score 
dtrscore = dtr_model.score(trainFactors, trainResponse)
dtrscore


# In[ ]:


#make predictions 

dtr_prediction = dtr_model.predict(testFactors)
dtr_prediction[0:10]


# # 2. Random Forest 

# In[ ]:


from sklearn.ensemble import RandomForestRegressor 

rf_model = RandomForestRegressor(n_estimators=10, min_samples_split = 2, verbose = True, random_state = 82)


# In[ ]:


#Fitting the Random Forest Model 
rf_model.fit(trainFactors, trainResponse)


# In[ ]:


#Score of Random Forest 
rfscore = rf_model.score(trainFactors, trainResponse)
rfscore


# In[ ]:


#Random Forest Prediction 
rf_prediction = rf_model.predict(testFactors)
rf_prediction[0:10]


# # 3. Linear Regression 

# In[ ]:


from sklearn.linear_model import LinearRegression
lr_model = LinearRegression()

lr_model.fit(trainFactors, trainResponse)
lrscore = lr_model.score(trainFactors, trainResponse)
lrscore


# In[ ]:


lr_prediction = lr_model.predict(testFactors)
lr_prediction[0:10]


# # 4. Linear Support Vector Regression 

# In[ ]:


from sklearn.svm import LinearSVR

lsvr_model = LinearSVR(random_state = 42)
lsvr_model.fit(trainFactors, trainResponse)
lsvrscore = lsvr_model.score(trainFactors, trainResponse)
print("Linear Support Vector Regression Score is : ", lsvrscore)


# In[ ]:


lsvr_prediction = lsvr_model.predict(testFactors)
lsvr_prediction[0:10]


# # 5. KNN 
# 
# 

# In[ ]:


from sklearn.neighbors import KNeighborsRegressor

knr_model = KNeighborsRegressor(n_neighbors = 6)
knr_model.fit(trainFactors, trainResponse)
knrscore = knr_model.score(trainFactors, trainResponse)
print("K-nearest Neighbors Regression Score : ",knrscore)


# In[ ]:


knr_prediction = knr_model.predict(testFactors)
knr_prediction[0:10]


# # 6. Gradient Boosting

# In[ ]:


from sklearn.ensemble import GradientBoostingRegressor

gbr_model = GradientBoostingRegressor(n_estimators = 100, learning_rate=1.0, max_depth = 1, random_state = 42)
gbr_model.fit(trainFactors, trainResponse)
gbrscore = gbr_model.score(trainFactors, trainResponse)
gbrscore


# In[ ]:


gbr_prediction = gbr_model.predict(testFactors)
gbr_prediction[0:10]


# # 7. XGBoost 

# In[ ]:


from xgboost import XGBRegressor

xgb_model = XGBRegressor(depth = 16, learning_rate = 0.5, loss_function = 'RMSE')
xgb_model.fit(trainFactors, trainResponse)
xgbscore = xgb_model.score(trainFactors, trainResponse)
xgbscore


# In[ ]:


xgb_prediction = xgb_model.predict(testFactors)
xgb_prediction[0:10]


# In[ ]:


#spot Check 

spotCheck = 410
print("Decision Tree Regression: \n Predicted Fare:  {}  \n   Actual Fare:  {} \n Decision Tree Regression Score :  ".format(dtr_prediction[spotCheck], testResponse[spotCheck]),dtrscore)
print("\nRandom Forest Regression : \n Predicted Fare: {} \n Actual Fare: {} \n Random Forest Score : ".format(rf_prediction[spotCheck], testResponse[spotCheck]),rfscore)
print("\nLinear Regression  : \n Predicted Fare: {} \n Actual Fare : {}\n Linear Regression Score :  ".format(lr_prediction[spotCheck], testResponse[spotCheck]),lrscore)
print("\nLinear Support Vector Regression: \n Predicted Fare : {}  \n Actual Fare : {} \n SVR Score : ".format(lsvr_prediction[spotCheck], testResponse[spotCheck]), lsvrscore)
print("\nK Nearest Neighnors Regression : \n Predicted Fare : {} \n Actual Fare : {} \n KNN Score : ".format(knr_prediction[spotCheck], testResponse[spotCheck]), knrscore)
print("\nGradient Boosting Regression : \n Predicted Fare : {} \n Actual Fare : {} \n Gradient Boosting Score : ".format(gbr_prediction[spotCheck], testResponse[spotCheck]), gbrscore)
print("\nXGBoost Regression : \n Predicted Fare : {}  \n Actual Fare : {}  \n XGBoost Score :  ".format(xgb_prediction[spotCheck], testResponse[spotCheck]), xgbscore)


# # Using Cat Boost Regressor with loss_function = RMSE

# In[ ]:


#import catboost as ctb
#cbr_model = ctb.CatBoostRegressor(depth = 16, learning_rate = 0.5, loss_function = 'RMSE')


# In[ ]:


#cbr_model.fit(trainFactors, trainResponse)


# In[ ]:


#cbr_score = cbr_model.score(trainFactors, trainResponse)
#cbr_score


# In[ ]:


#cbr_prediction = cbr_model.predict(testFactors)
#cbr_prediction[0:10]


# # Using test.csv

# In[ ]:


os.listdir()


# In[ ]:


test_df = pd.read_csv("test.csv")


# In[ ]:


test_df.shape


# In[ ]:


test_df.info()


# In[ ]:


#Setting the Best Model 
bestModel = xgb_model


# In[ ]:


predictFactors = test_df[['pickup_longitude','pickup_latitude', 'dropoff_longitude','dropoff_latitude','passenger_count']]
predictFare = bestModel.predict(predictFactors)


# In[ ]:


predictedResults = pd.DataFrame(predictFare)


# In[ ]:


#predictedResults.to_csv('final_Predictions.csv')


# In[ ]:


predictedResults.head(10)


# In[ ]:




