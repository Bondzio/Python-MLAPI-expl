#!/usr/bin/env python
# coding: utf-8

#  #                             *Analysis in Airbnb dataset in Lisbon*

# __Project for fall semester 2017 on "Problem Solving Environments and Applications in Data Science"__
# 
# 
# **Authors:**  
#     Christinakis Ioannis, 
#     Foufikos Evangelos,
#     Ntontis Christos
#     

# ## Contents

# 1. Preproccesing Dataset
# 2. Plot dataset's variables 
# 
#  1. find avg Price according vs room's type
#  2. find avg Price according vs neighborhood and how many booked there
#  3. plot reviews vs prices
#  4. plot reviews vs overall satisfaction
#  5. plot overall satisfaction vs price
#  
#  
# 3. Use Linear Regression with and without PCA to predict prices with one hot encoding for caterigal variables
# 4. Use Logistic Regression with and without PCA to predict overall satisfaction with one hot encoding for categorical variables
# 5. Repeat step 3 and 4 with label encoding
#     

# In[ ]:


# Import needed libraries
import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn import datasets
from sklearn import cross_validation
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from collections import Counter
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt
from collections import Counter


# In[ ]:



data= pd.read_csv('../input/airbnb_lisbon_1480_2017-07-27.csv', header=0)
# replace NaN values with 0
data.fillna(0, inplace = True)

#Extract prices from the table
price = data['price']
prices = []

#convert prices from strings to float
for p in price:
    p = float(p)
    prices.append(p)
    
data['price'] = prices

#drop data that dont contain information
data = data[data.bedrooms > 0]
data = data[data.price  > 0]
data = data[data.accommodates  > 0]
data = data[data.price < 700]


# In[ ]:


data.head()


# # Categorize different listings based on room_type

# In[ ]:


roomType = data.groupby('room_type').room_id.count()
roomType = roomType.reset_index()
roomType = roomType.rename(columns = {'id':'number_Of_Listings'})
roomType


# In[ ]:


matplotlib.style.use('ggplot')

room = data.room_type
r = Counter(room)

room = pd.DataFrame.from_dict(r, orient = 'index').sort_values(by = 0)
room.columns = ['room_type']



# In[ ]:


room.plot.pie(y = 'room_type', 
                 colormap = 'Blues_r', 
                 figsize = (10,10), 
                 fontsize = 20, autopct = '%.2f',
                 legend = False,
                 title = 'Room Type Distribution')


# # Average prices for each type of listing

# In[ ]:


avgPrice = data.groupby('room_type').price.mean()
avgPrice = avgPrice.reset_index()
avgPrice = avgPrice.rename(columns = {'price':'average_Price'})


# In[ ]:



avgPrice


# In[ ]:


average_price = sum(data.price) / float(len(data.price))
# standard deviation to compare 
std = np.std(data.price)


# In[ ]:


print("Overall Average Price:", average_price)
print ("standard deviation: " + str(std))


# # Average prices for each type of listing according to neighborhoods

# In[ ]:


#neighborhood frequency
neighborhood = Counter(data['neighborhood'])


neighborhood_prices = data[['neighborhood', 'price']]
neighborhood_prices.columns = ['neighborhood', 'price']

neighborhood_prices = neighborhood_prices[neighborhood_prices['neighborhood'].isin(neighborhood)]

# group by neighbourhood and find the mean price for each of them
neighborhood_prices_group = neighborhood_prices.groupby('neighborhood')
neighborhood_prices = neighborhood_prices_group['price'].agg(np.mean)

neighborhood_prices = neighborhood_prices.reset_index()
neighborhood_prices['number of listings'] = neighborhood.values()


# In[ ]:


neighborhood_prices


# In[ ]:


nh_df = pd.DataFrame.from_dict(neighborhood, orient = 'index').sort_values(by = 0)
nh_df.plot(kind = 'bar', color = 'LightBlue', figsize = (15,8), title = 'SF Neighborhood Frequency', legend = False)


# In[ ]:


price_review = data[['reviews', 'price']].sort_values(by = 'price')

price_review.plot(x = 'price', y = 'reviews', style = 'o', figsize =(12,8), legend = False, title = 'Reviews based on Price')
plt.xlim(-20, 750)


# In[ ]:



overall_satisfaction_review = data[['reviews', 'overall_satisfaction']].sort_values(by = 'overall_satisfaction')

overall_satisfaction_review.plot(x = 'overall_satisfaction', y = 'reviews', style = 'o', figsize =(12,8), legend = False,
                  title = 'Reviews based on Overall_satisfaction')
plt.xlim(-1, 6)


# In[ ]:


overall_satisfaction_price = data[['price', 'overall_satisfaction']].sort_values(by = 'price')

overall_satisfaction_price.plot(x = 'price', y = 'overall_satisfaction', style = 'o', figsize =(12,8), legend = False,
                  title = 'Overall_satisfaction based on Price')


# # Data preprocessing 

# In[ ]:


new_data = data[['price',
           'room_type',
           'accommodates',
           #'bathrooms',
           #'bedrooms',
           'reviews',
           'neighborhood',
           'overall_satisfaction']]


lb_nh = LabelEncoder()
lb_rt = LabelEncoder()

#one hot encoding
oh_neighborhood = pd.get_dummies(new_data.neighborhood).astype(int)
oh_room_type = pd.get_dummies(new_data.room_type).astype(int)

#label encoding 
le_neighborhood = lb_nh.fit_transform(new_data["neighborhood"])
le_room_type = lb_rt.fit_transform(new_data['room_type'])

# drop the original columns and replace them with indicator columns
new_data = new_data.drop(['room_type','neighborhood'], axis = 1)
le_data = pd.DataFrame(new_data)

le_neighborhood = pd.DataFrame(le_neighborhood)
le_room_type = pd.DataFrame(le_room_type)
le_data = pd.concat((new_data, le_room_type, le_neighborhood), axis = 1)
le_data.columns = ['price',
           'accommodates',
           #'bathrooms',
           #'bedrooms',
           'reviews',
           'overall_satisfaction',
           'room_type',
           'neighborhood']

new_data = pd.concat((new_data, oh_room_type, oh_neighborhood), axis = 1)
le_data = le_data.dropna(axis=0, how='any')
new_data = new_data[:le_data.shape[0]]


# In[ ]:


new_data.head() #ONE-HOT Encoded Data


# In[ ]:


le_data.head() #LABEL Encoded Data


# # PCA  using ONE HOT encoding

# In[ ]:


#split the data and set price as target variable
y = new_data['price']
X = new_data.drop(['price'],axis=1)

#standarize the dataset
X_std = StandardScaler().fit_transform(X)

# call PCA 
pca = PCA(n_components = 30)
pca.fit(X_std)
print('Components:\n ', pca.components_)
print('Explained Variance Ratio:\n ', pca.explained_variance_ratio_)


# In[ ]:


#plot explained variance 
plt.bar(range(pca.explained_variance_ratio_.shape[0]), pca.explained_variance_ratio_, alpha = 0.5, 
        align = 'center', label = 'individual explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.ylim(0, 0.2)
plt.legend(loc = 'best')
plt.tight_layout()


# In[ ]:


s1 = sum(pca.explained_variance_ratio_[:17])
s2 = sum(pca.explained_variance_ratio_[17:])


# In[ ]:


# dimensionality reduction, keeping only
# 17 principal component
pca = PCA(n_components = 17)
X_pca = pca.fit_transform(X_std)
# inverse transform to obtain the projected data
X_new = pca.inverse_transform(X_pca)


# In[ ]:


print("Percentage of information on the components that we keep:",s1,"\nPercentage of information of the components that we discard:",s2)
print("original shape:   ", X.shape)
print("transformed shape:", X_pca.shape)


# ###  Linear Regression with/without PCA (one hot encoding)

# In[ ]:


import time
split_data = new_data.drop(['price'], axis = 1)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(split_data,
                                                y, 
                                                test_size=0.3,
                                                train_size = 0.7,
                                                random_state=13)
pipe1 = Pipeline([
    ('standardize', StandardScaler()),
    ('pca', PCA(n_components = 17)),
    ('linear', linear_model.LinearRegression())
])
pipe1.fit(X_train, y_train)
y_pred1 = pipe1.predict(X_test)

linear_reg_error1 = metrics.median_absolute_error(y_test, y_pred1) 

# pipeline without PCA
pipe2 = Pipeline([
    ('standardize', StandardScaler()),
    ('linear', linear_model.LinearRegression())
])
start = time.time()
pipe2.fit(X_train, y_train)
y_pred2 = pipe2.predict(X_test)

linear_reg_error2 = metrics.median_absolute_error(y_test, y_pred2) 


# In[ ]:


print ("Linear Regression's price deviation with PCA: " + str(linear_reg_error1))
print ("Linear Regression's price deviation without PCA: " + str(linear_reg_error2))


# In[ ]:


from sklearn.metrics import r2_score
print("R-squared Error with PCA:",r2_score(y_test,y_pred1))
print("R-squared Error without PCA:",r2_score(y_test,y_pred2))


# ###  Logistic Regression with/without PCA (one hot)

# In[ ]:


y = round(new_data['overall_satisfaction'])
split_data = new_data.drop(['overall_satisfaction'], axis = 1)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(split_data,
                                                y, 
                                                test_size=0.3,
                                                train_size = 0.7,
                                                random_state=13)
pipe1 = Pipeline([
    ('standardize', StandardScaler()),
    ('pca', PCA(n_components = 17)),
    ('logistic', linear_model.LogisticRegression(C = 1e5))
])
start = time.time()

pipe1.fit(X_train, y_train)
y_pred1 = pipe1.predict(X_test)
end = time.time()
print(end - start)

# pipeline without PCA
pipe2 = Pipeline([
    ('standardize', StandardScaler()),
    ('logistic', linear_model.LogisticRegression(C = 1e5))
])
start = time.time()

pipe2.fit(X_train, y_train)
y_pred2 = pipe2.predict(X_test)
end = time.time()
print(end - start)


# In[ ]:



print('Logistic Regression Accuracy with PCA:',sum(y_test == y_pred1)," / ", sum(y_test==y_test) ,'=' , sum(y_test == y_pred1)/sum(y_test==y_test)*100 , "%\n")
print('Logistic Regression Accuracy without PCA:',sum(y_test == y_pred2)," / ", sum(y_test==y_test) ,'=' , sum(y_test == y_pred2)/sum(y_test==y_test)*100 , "%\n")


# # PCA using Label encoding

# In[ ]:


y = le_data['price']
X = le_data.drop(['price'],axis=1)
#standarize the dataset
X_std = StandardScaler().fit_transform(X)

# call PCA specifying we only want the

pca = PCA(n_components =5)
pca.fit(X_std)

# important information
print('Components:\n ', pca.components_)
print('Explained Variance Ratio:\n ', pca.explained_variance_ratio_)


# In[ ]:


s1 = sum(pca.explained_variance_ratio_[:3])
s2 = sum(pca.explained_variance_ratio_[3:])


# In[ ]:


plt.bar(range(pca.explained_variance_ratio_.shape[0]), pca.explained_variance_ratio_, alpha = 0.5, 
        align = 'center', label = 'individual explained variance')

plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.ylim(0, 1)
plt.legend(loc = 'best')
plt.tight_layout()


# In[ ]:



# dimensionality reduction, keeping only
# the first principal component
pca = PCA(n_components = 3)
X_pca = pca.fit_transform(X_std)

# inverse transform to obtain the projected data
# and compare with the original
X_new = pca.inverse_transform(X_pca)


# In[ ]:


print("original shape:   ", X.shape)
print("transformed shape:", X_pca.shape)
print("Percentage of information on the components that we keep:",s1,"\nPercentage of information of the components that we discard:",s2)


# ###  Linear Regression with/without PCA (label encoding)

# In[ ]:


import time

start = time.time()
split_data = le_data.drop(['price'], axis = 1)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(split_data,
                                                y, 
                                                test_size=0.3,
                                                train_size = 0.7,
                                                random_state=13)
pipe1 = Pipeline([
    ('standardize', StandardScaler()),
    ('pca', PCA(n_components = 4)),
    ('linear', linear_model.LinearRegression())
])
pipe1.fit(X_train, y_train)
y_pred1 = pipe1.predict(X_test)

linear_reg_error1 = metrics.median_absolute_error(y_test, pipe1.predict(X_test)) 

# pipeline without PCA

pipe2 = Pipeline([
    ('standardize', StandardScaler()),
    ('linear', linear_model.LinearRegression())
])
pipe2.fit(X_train, y_train)
y_pred2 = pipe2.predict(X_test)

linear_reg_error2 = metrics.median_absolute_error(y_test, pipe2.predict(X_test)) 


# In[ ]:


print ("Linear Regression deviation with PCA: " + str(linear_reg_error1))
print ("Linear Regression deviation without PCA: " + str(linear_reg_error2))


# In[ ]:


from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

print("R-squared Error with PCA:",r2_score(y_test,y_pred1))
print("R-squared Error without PCA:",r2_score(y_test,y_pred2))


# ###  Logistic Regression with/without PCA (label encoding)

# In[ ]:


y = round(le_data['overall_satisfaction'])
split_data = le_data.drop(['overall_satisfaction'], axis = 1)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(split_data,
                                                y, 
                                                test_size=0.3,
                                                train_size = 0.7,
                                                random_state=13)
pipe1 = Pipeline([
    ('standardize', StandardScaler()),
    ('pca', PCA(n_components = 4)),
    ('logistic', linear_model.LogisticRegression(C = 1e5))
])

start = time.time()
pipe1.fit(X_train, y_train)
y_pred1 = pipe1.predict(X_test)
end = time.time()
print(end - start)

# pipeline without PCA
pipe2 = Pipeline([
    ('standardize', StandardScaler()),
    ('logistic', linear_model.LogisticRegression(C = 1e5))
])
start = time.time()

pipe2.fit(X_train, y_train)
y_pred2 = pipe2.predict(X_test)
end = time.time()
print(end - start)


# In[ ]:


print('Logistic Regression Accuracy with PCA:',sum(y_test == y_pred1)," / ", sum(y_test==y_test) ,'=' , sum(y_test == y_pred1)/sum(y_test==y_test)*100 , "%\n")
print('Logistic Regression Accuracy without PCA:',sum(y_test == y_pred2)," / ", sum(y_test==y_test) ,'=' , sum(y_test == y_pred2)/sum(y_test==y_test)*100 , "%\n")


# 
# # Conclusion
# In this data analysis project, I analyzed some of the most popular trends given the Airbnb's data on listings in Lisbon.
# 
# Summarized findings:

# | Method  |      Accuracy (%)    | Dimensions | Execution Time |
# |----------|:-------------:|:-------------:|-------------:
# | Logistic Regression (ONE HOT) |  72.41 | (11998, 33) | 0.74 |
# | Logistic Regression with PCA (ONE HOT)  |    50.3   | (11998, 17) | 0.23 |
# | Logistic Regression (LABEL) |  72.61 | (11998, 8) | 0.16 |
# | Logistic Regression with PCA (LABEL)  |    65.1   | (11998, 4) | 0.12 |

# | Method  |      Deviation (in Euros)    | R-squared Error
# |----------|:-------------:|-------------:|
# | Linear Regression (ONE HOT) |  20.54 | 0.32 |
#     | Linear Regression with PCA (ONE HOT)  |   22.6   | 0.20 |
# | Linear Regression (LABEL) |  19.7 | 0.32 |
# | Linear Regression with PCA (LABEL)  |    20.4 | 0.30 |
# 
