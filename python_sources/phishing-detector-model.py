#!/usr/bin/env python
# coding: utf-8

# # Loading Data and Packages

# In[ ]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib
from sklearn import preprocessing
import sklearn.model_selection as ms
import sklearn.metrics as sklm
import numpy.random as nr
import scipy.stats as ss
import math

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#importing data
Housing_Data = pd.read_csv('housing.csv')


# # Analysing Data 

# In[ ]:


Housing_Data.describe()


# In[ ]:


print('\nthe columns are - \n')
[print(i,end='.\t\n') for i in Housing_Data.columns.values]


# In[ ]:


Housing_Data.head()


# In[ ]:


Housing_Data.dtypes


# # Impute missing data

# In[ ]:


Housing_Data.isnull().sum()


# In[ ]:


#Filling the nulls in total_bedrooms with the mean

Housing_Data = Housing_Data.fillna(Housing_Data.mean())


# In[ ]:


# checking for nulls again

Housing_Data.isnull().sum()


# # Clean Data
# 

# Drop features which are ID

# In[ ]:


## Dropping feature column Social_Security_No which would not contribute to the prediction

Housing_Data.drop('Social_Security_No', axis = 1, inplace = True)


# In[ ]:


## Checking columns after dropping id feature
print('\nthe columns are - \n')
[print(i,end='.\t\n') for i in Housing_Data.columns.values]
print(Housing_Data.shape)


# There are now 20336 rows and 10 columns in the dataset

# # Visualizing Data

# # Categorical Data  - Feature Engineering / Transformation

# In[ ]:


Housing_Data.ocean_proximity.value_counts()


# In[ ]:


sns.countplot(Housing_Data.ocean_proximity)


# In[ ]:


def plot_box(Housing_Data, col, col_y = 'median_house_value'):
    sns.set_style("whitegrid")
    sns.boxplot(col, col_y, data=Housing_Data)
    plt.xlabel(col) # Set text for the x axis
    plt.ylabel(col_y)# Set text for y axis
    plt.show()
    
plot_box(Housing_Data, 'ocean_proximity') 


# Notice that there are only five houses with Ocean Proximity value Island.  
# It is likely that this category will not have statistically significant difference in predicting house price. 
# It is clear that this category needs to be aggregated with another suitable category
# 
# The code in the cell below uses a Python dictionary to recode the number of Ocean Proximity categories into a smaller number categories. 
# 

# In[ ]:


ocean_proximity_categories = {'<1H OCEAN':'<1H_OCEAN', 'INLAND':'INLAND', 
                    'NEAR OCEAN':'NEAR_OCEAN_ISLAND', 'ISLAND':'NEAR_OCEAN_ISLAND',
                    'NEAR BAY':'NEAR BAY'}
Housing_Data['ocean_proximity'] = [ocean_proximity_categories[x] for x in Housing_Data['ocean_proximity']]
Housing_Data['ocean_proximity'].value_counts()


# In[ ]:


#Categorical variable Ocean_proximity
new_val = pd.get_dummies(Housing_Data.ocean_proximity)


# In[ ]:


new_val.head()


# In[ ]:


Housing_Data[new_val.columns] = new_val


# In[ ]:


Housing_Data.describe()


# # Correlation 

# In[ ]:


Housing_Data.corr()


# In[ ]:


plt.figure(figsize=(15,12))
sns.heatmap(Housing_Data.corr(), annot=True)


# The light colour boxes have high correlations

# # Numeric Features  - Feature Engineering / Transformation

# In[ ]:


Housing_Data.hist(figsize=(15,12))


# In[ ]:


## Function to plot conditioned histograms
def cond_hists(df, plot_cols, grid_col):
    import matplotlib.pyplot as plt
    import seaborn as sns
    ## Loop over the list of columns
    for col in plot_cols:
        grid1 = sns.FacetGrid(df, col=grid_col)
        grid1.map(plt.hist, col, alpha=.7)
    return grid_col


num_cols = ['housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
cond_hists(Housing_Data, num_cols, 'ocean_proximity')


# In[ ]:


Housing_Data.drop('ocean_proximity', axis = 1, inplace = True)


# Examine this series of conditioned plots. 
# There is a consistent difference in the distributions of the numeric features conditioned on the categories of Ocean proximity. 
# The Near Bay category is distributed differently from the other categories of Ocean proximity.

# # Transforming numeric features

# 
# To improve performance of machine learning models transformations of the values are often applied. 
# Typically, transformations are used to make the relationships between variables more linear. 
# In other cases, transformations are performed to make distributions closer to Normal, or at least more symmetric. 
# These transformations can include taking logarithms, exponential transformations and power transformations.
# 
# In this case, we will transform the label, the price of the house. 

# In[ ]:


def hist_plot(vals, lab):
    ## Distribution plot of values
    sns.distplot(vals)
    plt.title('Histogram of ' + lab)
    plt.xlabel('Value')
    plt.ylabel('Density')
    
#labels = np.array(Housing_Data['median_house_value'])
hist_plot(Housing_Data['median_house_value'], 'median_house_value')


# The distribution of median_house_value is both quite skewed to the left. 
# Given the skew and the fact that there are no values less than or equal to zero, a log transformation might be appropriate.

# In[ ]:


Housing_Data['log_median_house_value'] = np.log(Housing_Data['median_house_value'])
hist_plot(Housing_Data['log_median_house_value'], 'log_median_house_value')


# The distribution of the logarithm of price is more symmetric, but still shows some multimodal tendency and skew. 
# Nonetheless, this is an improvement so we will use these values as our label.

# # 2d hexbin plots and 1d histograms for Transformed variable

# In[ ]:


def plot_desity_2d(Housing_Data, cols, col_y = 'log_median_house_value', kind ='kde'):
    for col in cols:
        sns.set_style("whitegrid")
        sns.jointplot(col, col_y, data=Housing_Data, kind=kind)
        plt.xlabel(col) # Set text for the x axis
        plt.ylabel(col_y)# Set text for y axis
        plt.show()


num_cols = ['housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
plot_desity_2d(Housing_Data, num_cols, kind = 'hex')  


# # Modelling and Predictions

# In[ ]:


from sklearn import preprocessing
convert = preprocessing.StandardScaler() 


# In[ ]:


X = Housing_Data.drop(['log_median_house_value'], axis=1)
y = Housing_Data.log_median_house_value


# In[ ]:


X = convert.fit_transform(X.values)
y = convert.fit_transform(y.values.reshape(-1,1)).flatten() 


# In[ ]:


X


# In[ ]:


y


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test,y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=10) 


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib
from sklearn.cluster import  KMeans


# In[ ]:



#==============================================================================
# Fitting the Linear Regression algo to the Training set
#==============================================================================
from sklearn.linear_model import LinearRegression
Linear_Reg = LinearRegression()
Linear_Reg.fit (X_train, y_train)


# In[ ]:


Linear_Reg_Predit = Linear_Reg.predict(X_test)


# In[ ]:


print(Linear_Reg_Predit)


# In[ ]:


from sklearn.metrics import mean_squared_error


# In[ ]:


print("Root Mean Squared Error for test data with Linear Regression  is "+str(np.sqrt(mean_squared_error(y_test,Linear_Reg_Predit))))


# In[ ]:


#==============================================================================
# Fitting the Decision Tree Regressor algo to the Training set
#==============================================================================
from sklearn.tree import DecisionTreeRegressor
DecisionTree_reg = DecisionTreeRegressor()
DecisionTree_reg.fit(X_train,y_train)


# In[ ]:


DecisionTree_Reg_Predit = DecisionTree_reg.predict(X_test)


# In[ ]:


print("Root Mean Squared Error for test data with Decision Tree Regression  is "+str(np.sqrt(mean_squared_error(y_test,DecisionTree_Reg_Predit))))


# In[ ]:


#==============================================================================
# Fitting the Random Forest Regressor algo to the Training set
#==============================================================================
from sklearn.ensemble import RandomForestRegressor
Random_forest_reg = RandomForestRegressor()
Random_forest_reg.fit(X_train,y_train)


# In[ ]:


Random_forest_Reg_Predit = Random_forest_reg.predict(X_test)


# In[ ]:


print("Root Mean Squared Error for test data with Random Forest Regression  is "+str(np.sqrt(mean_squared_error(y_test,Random_forest_Reg_Predit))))


# # Choosing the Best Model 
# #Decision Tree Regressor has the best accuracy as the RMSE is the lowest amoung the three models
