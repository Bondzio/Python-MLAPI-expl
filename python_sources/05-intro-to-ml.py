#!/usr/bin/env python
# coding: utf-8

# [**Machine Learning Micro Course Homepage**](https://www.kaggle.com/learn/intro-to-machine-learning)
# 
# [Open this Notebook in Kaggle](https://www.kaggle.com/mahendrabishnoi2/05-intro-to-ml)
# 
# ---

# # Basic Data Exploration
# 
# ## Using Pandas to Get Familiar with Data
# We'll look at data about home prices in Melbourne, Australia.

# In[ ]:


import pandas as pd


# In[ ]:


import os
os.listdir("../input/")


# In[ ]:


# set filepath of dataset to a variable
melbourne_filepath = "../input/melbourne-housing-snapshot/melb_data.csv"

# read the data and store into DataFrame
melbourne_data = pd.read_csv(melbourne_filepath)

# show some statistics about data (numerical variables)
melbourne_data.describe()


# In[ ]:


melbourne_data.head()


# Exercises of this tutorial are solved [here](https://www.kaggle.com/mahendrabishnoi2/exercise-explore-your-data)
# 
# ---

# # First Machine Learning Model
# 
# ## Selecting Data for Modelling
# There are a lot of columns in `melbourne_data`. So first we will print all column names and then select a few columns to use for training our first model.

# In[ ]:


import pandas as pd

melbourne_file_path = '../input/melbourne-housing-snapshot/melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path) 
# show all fields/columns in melbourne_data DataFrame
melbourne_data.columns


# In[ ]:


# Melbourne Housing Data has some missing values
# For now we will drop missing values

melbourne_data = melbourne_data.dropna(axis=0)


# In[ ]:


# selecting the prediction target
y = melbourne_data.Price


# In[ ]:


# choosing features
melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']


# In[ ]:


X = melbourne_data[melbourne_features]


# In[ ]:


X.describe()


# In[ ]:


X.head()


# ---

# ## Building Model

# In[ ]:


from sklearn.tree import DecisionTreeRegressor

# define model, define random_state to reproduce same results
melbourne_model = DecisionTreeRegressor(random_state=1)

# fit model
melbourne_model.fit(X, y)


# In[ ]:


# Making predictions

print("Making predictions for the following 5 houses")
print(X.head())
print("\nThe predictions are: ")
print(melbourne_model.predict(X.head()))


# Exercises of this tutorial are solved [here](https://www.kaggle.com/mahendrabishnoi2/exercise-your-first-machine-learning-model)
# 
# ---

# # Model Validation
# Measuring quality of the model.
# 
# First of all create a model.

# In[ ]:


# Data Loading Code Hidden Here
import pandas as pd

# Load data
melbourne_file_path = '../input/melbourne-housing-snapshot/melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path) 
# Filter rows with missing price values
filtered_melbourne_data = melbourne_data.dropna(axis=0)
# Choose target and features
y = filtered_melbourne_data.Price
melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'BuildingArea', 
                        'YearBuilt', 'Lattitude', 'Longtitude']
X = filtered_melbourne_data[melbourne_features]

from sklearn.tree import DecisionTreeRegressor
# Define model
melbourne_model = DecisionTreeRegressor()
# Fit model
melbourne_model.fit(X, y)


# Now calculate mean absolute error:

# In[ ]:


from sklearn.metrics import mean_absolute_error

predicted_prices = melbourne_model.predict(X)
mean_absolute_error(y, predicted_prices)


# ## train_test_split

# In[ ]:


from sklearn.model_selection import train_test_split

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)

# Define Model
melbourne_model = DecisionTreeRegressor(random_state=0)
# Fit Model
melbourne_model.fit(train_X, train_y)

# Predict on Validation Data
predicted_prices = melbourne_model.predict(val_X)
# Print Mean Absolute Error on Validation Data
print(mean_absolute_error(val_y, predicted_prices))


# Exercises of this tutorial are solved [here](https://www.kaggle.com/mahendrabishnoi2/exercise-model-validation)
# 
# ---

# # Underfitting and Overfitting
# 
# **Overfitting**: When a model matches the training data almost perfectly, but does poorly in validation and other new data. 
# 
# **Underfitting**: When a model fails to capture important distinctions and patterns in the data, so it performs poorly even in training data.
# 
# Since we care about accuracy on new data, which we estimate from our validation data, we want to find the sweet spot between underfitting and overfitting. Visually, we want the low point of the (red) validation curve.
# <img src="http://i.imgur.com/2q85n9s.png"/>

# In[ ]:


# Now we will use "max_leaf_nodes" parameter of "DecisionTreeRegressor" to set depth of tree
# and compare results of different values of "max_leaf_nodes"

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return mae


# In[ ]:


import pandas as pd
    
# Load data
melbourne_file_path = '../input/melbourne-housing-snapshot/melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path) 
# Filter rows with missing values
filtered_melbourne_data = melbourne_data.dropna(axis=0)
# Choose target and features
y = filtered_melbourne_data.Price
melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'BuildingArea', 
                        'YearBuilt', 'Lattitude', 'Longtitude']
X = filtered_melbourne_data[melbourne_features]

from sklearn.model_selection import train_test_split

# split data into training and validation data, for both features and target
train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)


# In[ ]:


# compare mae with different values of "max_leaf_nodes"

for max_leaf_nodes in [5, 50, 500, 5000]:
    mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
    print(f"Max leaf nodes: {max_leaf_nodes}\t\tMean Absolute Error: {mae:.0f}")


# Exercises of this tutorial are solved [here](https://www.kaggle.com/mahendrabishnoi2/exercise-underfitting-and-overfitting)
# 
# ---

# # Random Forests
# The random forest uses many trees, and it makes a prediction by averaging the predictions of each component tree. It generally has much better predictive accuracy than a single decision tree and it works well with default parameters.

# In[ ]:


import pandas as pd
    
# Load data
melbourne_file_path = '../input/melbourne-housing-snapshot/melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path) 
# Filter rows with missing values
melbourne_data = melbourne_data.dropna(axis=0)
# Choose target and features
y = melbourne_data.Price
melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'BuildingArea', 
                        'YearBuilt', 'Lattitude', 'Longtitude']
X = melbourne_data[melbourne_features]

from sklearn.model_selection import train_test_split

# split data into training and validation data, for both features and target
# The split is based on a random number generator. Supplying a numeric value to
# the random_state argument guarantees we get the same split every time we
# run this script.
train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)


# In[ ]:


# we will import "RandomForestRegressor" class instead of "DecisionTreeRegressor"

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

forest_model = RandomForestRegressor(random_state=1)
forest_model.fit(train_X, train_y)
melb_pred = forest_model.predict(val_X)
mae = mean_absolute_error(melb_pred, val_y)
print(f"{mae:.0f}")


# Exercises of this tutorial are solved [here](https://www.kaggle.com/mahendrabishnoi2/exercise-random-forests)
# 
# ---

# In[ ]:




