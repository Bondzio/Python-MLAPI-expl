#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Import Dataset
dataset = pd.read_csv("../input/housing.csv")
dataset.head() # Print first 5 observations from dataset using head()


# In[ ]:


# Check in which column contains nan values
dataset.isnull().any()


# "total_bedrooms" contains nan values sothat it is showing True

# In[ ]:


# Separate features and labels
features = dataset.iloc[:,:-1].values
label = dataset.iloc[:,-1].values.reshape(-1,1)


# In[ ]:


# Perform Imputation with strategy=mean
from sklearn.preprocessing import Imputer
imputerNaN = Imputer(missing_values="NaN",strategy="mean",axis=0)
features[:,[4]] = imputerNaN.fit_transform(features[:,[4]])


# In[ ]:


# Perform Label Encoding and Onehot Encding on categorical values present in the features
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
features[:,8] = LabelEncoder().fit_transform(features[:,8])
features = OneHotEncoder(categorical_features=[8]).fit_transform(features).toarray()


# ## Multivariate Regression

# In[ ]:


X,y=features,label # Purpose of this copying variables is that trees doesn't requires scaling while others "may be"
# Split into training set and testing set in every model building cause of "random_state" present in the "train_test_split"
from sklearn.model_selection import train_test_split as tts
X_train,X_test,y_train,y_test = tts(X,y,test_size=0.2,random_state=28)


# In[ ]:


# Multivariate Linear Regression
from sklearn.linear_model import LinearRegression
model_multivariate = LinearRegression()
model_multivariate.fit(X_train,y_train)


# In[ ]:


# Perform prediction and model score
y_pred = model_multivariate.predict(X_test)
from sklearn.metrics import r2_score,mean_squared_error
print("Model Score for Training data: {}".format(model_multivariate.score(X_train,y_train)))
print("Model Score for Testing data: {}".format(r2_score(y_test,y_pred)))
print("Root Mean Squared Error is {}".format(np.sqrt(mean_squared_error(y_test,y_pred))))


# ## Decision Tree Regression

# In[ ]:


X,y=features,label # Purpose of this copying variables is that trees doesn't requires scaling while others "may be"
# Split into training set and testing set in every model building cause of "random_state" present in the "train_test_split"
from sklearn.model_selection import train_test_split as tts
X_train,X_test,y_train,y_test = tts(X,y,test_size=0.2,random_state=5)


# In[ ]:


# Decision Tree Regression
from sklearn.tree import DecisionTreeRegressor
model_decision = DecisionTreeRegressor(random_state=48)
model_decision.fit(X_train,y_train)


# In[ ]:


# Perform prediction and model score
y_pred = model_decision.predict(X_test)
from sklearn.metrics import r2_score
print("Model Score for Training data: {}".format(model_decision.score(X_train,y_train)))
print("Model Score for Testing data: {}".format(r2_score(y_test,y_pred)))
print("Root Mean Squared Error is {}".format(np.sqrt(mean_squared_error(y_test,y_pred))))


# ## Random Forest Regression

# In[ ]:


X,y=features,label # Purpose of this copying variables is that trees doesn't requires scaling while others "may be"
# Split into training set and testing set in every model building cause of "random_state" present in the "train_test_split"
from sklearn.model_selection import train_test_split as tts
X_train,X_test,y_train,y_test = tts(X,y,test_size=0.2,random_state=5)


# In[ ]:


# Random Forest Tree Regression
from sklearn.ensemble import RandomForestRegressor
model_random = RandomForestRegressor(n_estimators=35,random_state=15)
model_random.fit(X_train,y_train.ravel())


# In[ ]:


# Perform prediction and model score
y_pred = model_random.predict(X_test)
from sklearn.metrics import r2_score
print("Model Score for Training data: {}".format(model_random.score(X_train,y_train)))
print("Model Score for Testing data: {}".format(r2_score(y_test,y_pred)))
print("Root Mean Squared Error is {}".format(np.sqrt(mean_squared_error(y_test,y_pred))))


# ## Support Vector Regression

# In Support Vector Machine scaling giving more better predictions.

# In[ ]:


X,y=features,label # Purpose of this copying variables is that trees doesn't requires scaling while others "may be"
# Split into training set and testing set in every model building cause of "random_state" present in the "train_test_split"
from sklearn.model_selection import train_test_split as tts
X_train,X_test,y_train,y_test = tts(X,y,test_size=0.2,random_state=24)


# In[ ]:


# Perform Scaling
from sklearn.preprocessing import StandardScaler
X_train = StandardScaler().fit_transform(X_train)
X_test = StandardScaler().fit_transform(X_test)
y_train = StandardScaler().fit_transform(y_train).ravel()
y_test = StandardScaler().fit_transform(y_test).ravel()


# In[ ]:


# Support Vector Regression
from sklearn.svm import SVR
model_svr = SVR(kernel="rbf")
model_svr.fit(X_train,y_train.ravel())


# In[ ]:


# Perform prediction and model score
y_pred = model_svr.predict(X_test)
from sklearn.metrics import r2_score
print("Model Score for Training data: {}".format(model_svr.score(X_train,y_train)))
print("Model Score for Testing data: {}".format(r2_score(y_test,y_pred)))
print("Root Mean Squared Error is {}".format(np.sqrt(mean_squared_error(y_test,y_pred))))


# #### I will go with the Support Vector Regression for this dataset cause It has minimum and accptable than other model's root mean square value

# ## Linear Regression with "median_income" feature and "median_house_value" label

# In[ ]:


# Separate the single feature from dataset and label from dataset
X = dataset.median_income.values.reshape(-1,1)
y = dataset.median_house_value.values.reshape(-1,1)


# In[ ]:


# Split into training set and test set
from sklearn.model_selection import train_test_split as tts
X_train,X_test,y_train,y_test = tts(X,y,test_size=0.2,random_state=33)


# In[ ]:


# Perform Scaling
from sklearn.preprocessing import StandardScaler
X_train = StandardScaler().fit_transform(X_train)
X_test = StandardScaler().fit_transform(X_test)
y_train = StandardScaler().fit_transform(y_train).ravel()
y_test = StandardScaler().fit_transform(y_test).ravel()


# In[ ]:


# Linear Regression
from sklearn.linear_model import LinearRegression
model_linear = LinearRegression()
model_linear.fit(X_train,y_train.ravel())


# In[ ]:


# Perform prediction and model score
y_pred = model_linear.predict(X_test)
from sklearn.metrics import r2_score
r2_score(y_test,y_pred)


# In[ ]:


# lot the graph for Training set and Testing set and see the visualization of the dataset
plt.style.use("ggplot")
plt.figure(figsize=(20,15))

plt.subplot(1,2,1)
plt.title("Training Data")
plt.scatter(X_train,y_train,color="red")
plt.plot(X_train,model_linear.predict(X_train),color="blue")
plt.xlabel("Median Income")
plt.ylabel("Median House Value")
plt.legend()

plt.subplot(1,2,2)
plt.title("Testing Data")
plt.scatter(X_test,y_test,color="red")
plt.plot(X_test,y_pred,color="blue")
plt.xlabel("Median Income")
plt.ylabel("Median House Value")

plt.show()


# ## As you can see the independent varible is scattered so that getting less accurate results

# # Apply PCA on dataset for dimensionality reduction

# In[ ]:


from seaborn import pairplot as pp
pp(dataset,x_vars=["housing_median_age","total_rooms","total_bedrooms","population","households","median_income"],y_vars="median_house_value")


# ### As you can see in this pairplots that independent variables are scattered in coordinate system.

# In[ ]:


X = features
features = pd.DataFrame(features) # For PCA features should be in DataFrame sothat converting
from sklearn.decomposition import PCA
housing_features_pca = PCA()
housing_features_pca.fit(features.iloc[:,8:10]) #Column8:"total_rooms" and Column9:"total_bedrooms"
housing_features_pca.explained_variance_ratio_


# #### By testing explained variance ratio we can say that total_bedrooms is less important than total_rooms
