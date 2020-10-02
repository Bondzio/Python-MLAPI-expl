#!/usr/bin/env python
# coding: utf-8

# # Machine Learning Practice with Categorical Variables on Forbes Highest Paid Athletes Data from 1990 - 2019

# From sklearn we are importing classes in order to split our data and predict outcomes. 
# We will approach this data and performing predictions on it in three different ways: 
# 1) Dropping categorical variables columns 
# 2) Label encoding categorical variables 
# 3) One Hot Encoding categorical variables 
# And we will test which one is the best approach by finding mean absolute error 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


data = pd.read_csv('/kaggle/input/forbes-highest-paid-athletes-19902019/Forbes Richest Atheletes (Forbes Richest Athletes 1990-2019).csv')
data


# Below I am calculating the time value of money with inflation data. Using the Consumer Price Index (CPI) from 1991 to 2019 and so on. With this I use the formula 
#     **Final value = Initial value * CPI final/CPI initial**
# I was able to get the CPI from each year and plug it into the formula above. So based on the year, the for loop below outputs a list of the Net Present Value for each salary, and now we have the value of each salary for the year 2019 which is the last year this data was collected. We can now make predictions on the net present value of the earnings.

# In[ ]:


inflation_data = {'cpi_per_year': [53.2, 56.45, 58.18, 59.87, 61.51, 63.16, 64.76, 66.92, 68.05, 
                                  69.15, 71.01, 73.41, 74.55, 76.32, 77.76, 80.29, 83.03, 85.14, 88.62, 
                                  88.7, 91.11, 92.47, 95.21, 96.87, 98.33, 99.07, 99.79, 101.86, 104.01, 106], 
                 'year': [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                          2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
                         2018, 2019]}
inflation_df = pd.DataFrame(inflation_data, columns=['year', 'cpi_per_year'])
inflation_df


# In[ ]:


npv = []
for year, dollars in zip(data['Year'], data['earnings ($ million)']): 
    for yr, cpi in zip(inflation_data['year'], inflation_data['cpi_per_year']):
        if year == yr: 
            dollars = dollars*((inflation_df.at[29, 'cpi_per_year'])/cpi)
            npv.append(round(dollars, 2))
data['npv'] = npv
data
    


# Here we are seeing how many values in each column of the data are null or do not have something in them, this is so we can get a sense of how much we are missing and if it might skew the predictions

# In[ ]:


data.isnull().sum()


# We can see that there are 24 values out of 2328 total values in the dataset that are null. This is not so many to where it would have a large effect, but as you can see from the dataset printed out above are are some non-null character values that also might have a strange effect on our predictions. The simplest way to deal with this is by dropping the column. 

# In[ ]:


# Going to drop columns with missing values 
cols_with_missing = [col for col in data.columns
                     if data[col].isnull().any()]
data = data.drop(cols_with_missing, axis=1)

# We are also going to drop these two columns because they are not relevant to what we are trying to predict 
# The 'Nationality' column has other complications that come with splitting the data so it must be dropped 
data = data.drop(['Name', 'Nationality'], axis=1)
data


# In[ ]:


#Here we are putting the sports all in lowercase because they were previously in both upper and lower 
#which made for a larger number of unique values, by putting them all in lowercase there are less unique values
data['Sport'] = data['Sport'].astype(str).str.lower()
data['Sport'].unique()


# In[ ]:


# this is our prediction target
y = data['npv']

#these are our 'features', or columns used to determine the earnings of each athlete, used to make predictions
forbes_features = ['Current Rank', 'Sport', 'Year']
X = data[forbes_features]

# Divide data into training and validation subsets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)


# In[ ]:


# Get list of categorical variables
s = (X_train.dtypes == 'object')
object_cols = list(s[s].index)

print("Categorical variables:")
print(object_cols)
#Since we dropped the other categorical variable columns which included 'Name' and 'Nationality',
#we should expect the 'Sport' column to be the only column containing categorical variables 


# The way we have split the data, it follows that the valid data is a subset of the training data. If the valid data was not a subset of the training data it would throw an error because label encoder would not have made labels for any data that it had not seen before, so you would still have unencoded categorical variables in your valid data. This is the reason why the 'Nationality' column needed to be dropped.

# In[ ]:


print('Unique values in "Sport" training data: ', X_train['Sport'].unique())
print('\nUnique values in "Sport" valid data: ', X_valid['Sport'].unique())


# In[ ]:


#We only have one column for this iteration, but if you wanted to incorporate 'Nationality' or another
#categorical variable column, then this iteration would be useful to check if you will later find errors 
#when using label encoding

for col in object_cols: 
    if set(X_valid[col]).issubset(set(X_train[col])):
        good_label_cols = col
    
print("Categorical variables that can be used in label encoding: ", good_label_cols)
#print("Categorical variables to be dropped: ", bad_label_cols)


# Method 1) Dropping categorical variables:

# In[ ]:


# Try dropping categorical variables 

#Define function to compare approaches 
def compare(X_train, X_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=100,random_state=0)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return mean_absolute_error(y_valid, preds)

drop_X_train = X_train.select_dtypes(exclude=['object'])
drop_X_valid = X_valid.select_dtypes(exclude=['object'])

print('MAE from dropping categorical variable columns:')
print(compare(drop_X_train, drop_X_valid, y_train, y_valid))
    


# Method 2) Label Encoding categorical variables:

# In[ ]:


label_X_train = X_train.copy()
label_X_valid = X_valid.copy()


# Apply label encoder to each column with categorical data
label_encoder = LabelEncoder()
for col in object_cols:
    label_X_train[col] = label_encoder.fit_transform(X_train[col])
    label_X_valid[col] = label_encoder.transform(X_valid[col])
print('MAE from label encoding:')
print(compare(label_X_train, label_X_valid, y_train, y_valid))


# Method 3) One Hot Encoding categorical variables:

# In[ ]:


from sklearn.preprocessing import OneHotEncoder

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)

print("MAE from Approach 3 (One-Hot Encoding):") 
print(compare(OH_X_train, OH_X_valid, y_train, y_valid))


# As seen above, Method 1 of dropping categorical variable columns is the most accurate because its mean absolute error is the least. Below we are building the model using the data with the dropped categorical variable columns.

# In[ ]:


y_valid = y_valid.tolist()


# In[ ]:




# predict the data based on the original prediction target and dropped categorical features

drop_X_train = X_train.select_dtypes(exclude=['object'])
drop_X_valid = X_valid.select_dtypes(exclude=['object'])


    # Defining our model: using RandomForestRegressor 
model = RandomForestRegressor(n_estimators=100,random_state=0)
    # Fitting the model with the training data 
model.fit(drop_X_train, y_train)
    # Making predictions based on validation data 
predictions = model.predict(drop_X_valid)
data = {"Prediction": predictions}
drop_df = pd.DataFrame(data, columns=['Prediction'])
drop_df['Outcome'] = y_valid
drop_df['Percent Error'] = round((abs((drop_df['Outcome']) - (drop_df['Prediction']))/(drop_df['Outcome']))*100, 2)
drop_df['Correct?'] = drop_df['Percent Error'] < 5
drop_df = drop_df[['Outcome', 'Prediction', 'Percent Error', 'Correct?']]
drop_df





# In[ ]:



def percentCorrect(df): 
    true_count = 0
    false_count = 0
    total_count = 0
    for answer in df['Correct?']: 
        if answer == True: 
            true_count += 1
            total_count += 1
        else: 
            false_count += 1
            total_count += 1
    print('Percent true = ', (round((true_count/total_count)*100, 2)), '%')
    print('Percent false = ', (round((false_count/total_count)*100, 2)), '%')
percentCorrect(drop_df)
            


# In[ ]:


# Defining our model: using RandomForestRegressor 
model = RandomForestRegressor(n_estimators=100,random_state=0)
# Fitting the model with the training data 
model.fit(label_X_train, y_train)
# Making predictions based on validation data 
predictions = model.predict(label_X_valid)
data = {"Prediction": predictions}
label_df = pd.DataFrame(data, columns=['Prediction'])
label_df['Outcome'] = y_valid
label_df['Percent Error'] = round((abs((label_df['Outcome']) - (label_df['Prediction']))/(label_df['Outcome']))*100, 2)
label_df['Correct?'] = label_df['Percent Error'] < 5
label_df = label_df[['Outcome', 'Prediction', 'Percent Error', 'Correct?']]
label_df

# sports_df = pd.DataFrame(X_train['Sport'].unique(), columns=['list_sports'])
# sports_df['list_encoded_sports'] = label_encoder.fit_transform(sports_df.list_sports)
# sports_df


# In[ ]:


percentCorrect(label_df)


# Predictions using One Hot Encoding method:

# In[ ]:


# Defining our model: using RandomForestRegressor 
model = RandomForestRegressor(n_estimators=100,random_state=0)
# Fitting the model with the training data 
model.fit(OH_X_train, y_train)
# Making predictions based on validation data 
predictions = model.predict(OH_X_valid)
data = {"Prediction": predictions}
new_df = pd.DataFrame(data, columns=['Prediction'])
new_df['Outcome'] = y_valid
new_df['Percent Error'] = round((abs((new_df['Outcome']) - (new_df['Prediction']))/(new_df['Outcome']))*100, 2)
new_df['Correct?'] = new_df['Percent Error'] < 5
new_df = new_df[['Outcome', 'Prediction', 'Percent Error', 'Correct?']]
new_df


# In[ ]:


percentCorrect(new_df)

