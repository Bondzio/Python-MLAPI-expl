#!/usr/bin/env python
# coding: utf-8

# # Imports

# ## Packages

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import math
import seaborn as sns
from scipy.stats import skew
from scipy.special import boxcox1p
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


# ## Files

# In[ ]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')
houses = pd.concat([train, test], sort=False, ignore_index=True) #Combining both sets into a main 'houses' data set.


# # Data Cleaning

# ## Missing Values

# This section is aimed at handling all missing values in the 'houses' data set.

# In[ ]:


# Return column names and their respective percentage of missing values, if such percentage is postive.
output = []
for column in houses.columns.values:
    naPercent = sum(houses[column].isna())/len(houses[column])*100
    if naPercent > 0:
        output = output + [[column, naPercent]]
output = pd.DataFrame(output)
output.columns = ('Variable', 'naPercent')
output = output.sort_values(by = 'naPercent')
output.plot.bar(x='Variable', y='naPercent', legend = False)
plt.xlabel('Variables')
plt.ylabel('Percentage of missing values (%)')
plt.title(r'MISSING VALUES FOR EACH VARIABLE')


# ### Possible 'NA' Categories

# The 'data_description' file tells us that some categorical variables can take on 'NA' (a string) as a possible value. This section deals with such variables by changing the missing values to 'NA', where appropriate.

# In[ ]:


# Properties without alley access.
houses.loc[houses['Alley'].isna(), 'Alley'] = 'NA'
# When all five categorical basement columns are simultaneously missing, change to 'NA' for no basement.
houses.loc[(houses['BsmtQual'].isna()) & (houses['BsmtCond'].isna()) & (houses['BsmtExposure'].isna())
       & (houses['BsmtFinType1'].isna()) & (houses['BsmtFinType2'].isna()),
      ('BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2')] = 'NA'
# If a house has zero fireplaces and fireplace quality is missing, then change fireplace quality to 'NA'.
houses.loc[(houses['FireplaceQu'].isna()) & (houses['Fireplaces']==0), 'FireplaceQu'] = 'NA'
# If a house has zero pool area and pool quality is missing, then change pool quality to 'NA'.
houses.loc[(houses['PoolArea']==0) & (houses['PoolQC'].isna()), 'PoolQC'] = 'NA'
# Due to the high proportion of the 'Fence' column being missing, and the absence of any other fence-related variables, all
# missing values are assumed to be the absence of a fence and are changed to 'NA'.
houses.loc[houses['Fence'].isna(), 'Fence'] = 'NA'
# Due to the high proportion of the 'MiscFeature' column being missing, and the absence of any other elevator-, other-, shed-
# and tennis court-related variables, all missing values are assumed to be the absence of a miscellaneous feature and are
# changed to 'NA'.
houses.loc[houses['MiscFeature'].isna(), 'MiscFeature'] = 'NA'


# ### Feature by Feature

# This section deals with the remaining features on a case-by-case basis, and handles the missing values in each.

# In[ ]:


# Examining missing 'Electrical' houses in terms of electricity-related features.
houses[houses['Electrical'].isna()].loc[:, ('MSZoning', 'Utilities', 'Heating', 'CentralAir', 'Electrical')]


# All above indicate the presence of electricy, so the missing value in this column is erroneous and will be replaced by the modal class.

# In[ ]:


# Displaying houses with missing kitchen quality to establish if they do indeed have kitchens.
houses[houses['KitchenQual'].isna()].loc[:, ('KitchenQual', 'KitchenAbvGr')]


# This house does have a kitchen and so the missing value will be replaced by the associated modal class. For the two features above, it was easy to evaluate whether or not missing values need to be replaced by the modal class or not; however, the remaining features are not as easy to inspect. As a result, the rest of the missing values in each feature will be replaced by the respective modal class, including the two features we inspected above.

# In[ ]:


# Replacing the missing values of the appropriate features with the associated modal class.
for column in ['MSZoning', 'Utilities', 'Exterior1st', 'Exterior2nd', 'Electrical', 'KitchenQual', 'Functional',
              'SaleType']:
    houses.loc[houses[column].isna(), column] = houses[column].mode()[0]


# 'LotFrontage' is a numerical variable, so missing values might need to be replaced by its median or mean. As a result, the distribution of this feature needs to be inspected.

# In[ ]:


# Visually establishing the skewness of 'LotFrontage'.
plt.hist(houses[houses['LotFrontage'].notna()].loc[:, 'LotFrontage'])
plt.xlabel('Lot frontage')
plt.ylabel('Count')
plt.title(r'LOT FRONTAGE DISTRIBUTION')
plt.savefig('lotFrontageDistribution.png')


# 'LotFrontage' is seemingly skewed, so any missing values of this feature should be replaced by its median and not its mean.

# In[ ]:


# Replacing the missing values of 'LotFrontage' by its median.
houses.loc[houses['LotFrontage'].isna(), 'LotFrontage'] = houses['LotFrontage'].median()


# Below, we take care of the masonry veneer area and type features.

# In[ ]:


# For houses with zero masonry veneer area and missing masonry veneer type, masonry veneer type becomes 'None'.
houses.loc[(houses['MasVnrArea']==0) & (houses['MasVnrType'].isna()), 'MasVnrType'] = 'None'
# Checking if houses with zero masonry veneer area all have 'None' as masonry veneer type.
houses[(houses['MasVnrArea']==0) & (houses['MasVnrType']!='None')].loc[:, ('MasVnrArea', 'MasVnrType')]


# In[ ]:


# Determining the mode for 'MasVnrArea'.
houses['MasVnrArea'].mode()[0]


# In[ ]:


# Determining the modal class for 'MasVnrType'.
houses.groupby('MasVnrType').count()['Id']


# It is much more likely that the erroneous houses with zero masonry veneer area and masonry veneer types other than 'None' should have 'None' as masonry veneer type, since 0.0 is the mode for masonry veneer area but neither 'BrkFace' nor 'Stone' are the modal class of masonry veneer type.

# In[ ]:


# Replacing the erronoeus masonry veneer type with 'None'.
houses.loc[(houses['MasVnrArea']==0) & (houses['MasVnrType']!='None'), 'MasVnrType'] = 'None'
# Replacing the remaining missing values of masonry veneer area and type with the mode and modal class, respectively.
houses.loc[houses['MasVnrArea'].isna(), 'MasVnrArea'] = 0
houses.loc[houses['MasVnrType'].isna(), 'MasVnrType'] = 'None'


# Below, we take care of the basement-related features.

# In[ ]:


# Return all basement-related features with missing values.
houses.loc[(houses['BsmtQual'].isna()) | (houses['BsmtCond'].isna()) | (houses['BsmtExposure'].isna()) |
           (houses['BsmtFinType1'].isna()) | (houses['BsmtFinSF1'].isna()) | (houses['BsmtFinType2'].isna()) |
           (houses['BsmtFinSF2'].isna()) | (houses['BsmtUnfSF'].isna()) | (houses['TotalBsmtSF'].isna())].loc[:, 
           ('BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinSF1', 'BsmtFinType2', 'BsmtFinSF2',
            'BsmtUnfSF', 'TotalBsmtSF')]


# In[ ]:


# Determine the indices of the above houses.
indices = houses.loc[(houses['BsmtQual'].isna()) | (houses['BsmtCond'].isna()) | (houses['BsmtExposure'].isna()) |
           (houses['BsmtFinType1'].isna()) | (houses['BsmtFinSF1'].isna()) | (houses['BsmtFinType2'].isna()) |
           (houses['BsmtFinSF2'].isna()) | (houses['BsmtUnfSF'].isna()) | (houses['TotalBsmtSF'].isna())].loc[:, 
           ('BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinSF1', 'BsmtFinType2', 'BsmtFinSF2',
            'BsmtUnfSF', 'TotalBsmtSF')].index.values
# House with index 2120 seemingly does not have a basement, so the numerical basement-related features of this house are
# changed to zero.
houses.loc[2120, ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF')] = 0
# Determining the modal class for 'BsmtQual'.
houses.groupby('BsmtQual').count()['Id']


# In[ ]:


# There are two modal classes for this feature, so instead determine the modal class of 'BsmtQual' by only for the 10 houses
# displayed above.
houses.iloc[indices, :].groupby('BsmtQual').count()['Id']


# In[ ]:


# Changing the missing values of 'BsmtQual' to the 2nd modal class since this particular group of erroneous houses has a higher
# chance of having 'Gd' as 'BsmtQual'.
houses.loc[(houses['BsmtQual'].isna()), 'BsmtQual'] = 'Gd'
# Replacing the missing values of the numerical basement-related features with their respective modes, since from above one
# can see that these houses do indeed have basements.
for column in ['BsmtCond', 'BsmtExposure', 'BsmtFinType2']:
    houses.loc[houses[column].isna(), column] = houses[column].mode()[0]
# Displaying the houses with missing 'BsmtFullBath' to see if they do indeed have basements.
houses[houses['BsmtFullBath'].isna()].iloc[:, 30:39]


# In[ ]:


# Displaying the houses with missing 'BsmtHalfBath' to see if they do indeed have basements.
houses[houses['BsmtHalfBath'].isna()].iloc[:, 30:39]


# In[ ]:


# Houses with missing basement 'BsmtHalfBath' or 'BsmtFullBath' seemingly do not have basements, so these features for these
# houses should be changed to 0.
houses.loc[houses['BsmtHalfBath'].isna(), 'BsmtHalfBath'] = 0
houses.loc[houses['BsmtFullBath'].isna(), 'BsmtFullBath'] = 0
# Return column names and their respective percentage of missing values, if such percentage is postive.
output = []
for column in houses.columns.values:
    naPercent = sum(houses[column].isna())/len(houses[column])*100
    if naPercent > 0:
        output = output + [[column, naPercent]]
output = pd.DataFrame(output)
output.columns = ('Variable', 'naPercent')
output = output.sort_values(by = 'naPercent')
output.plot.bar(x='Variable', y='naPercent', legend = False)
plt.xlabel('Variables')
plt.ylabel('Percentage of missing values (%)')
plt.title(r'MISSING VALUES FOR EACH VARIABLE')


# Below, we take care of the garage-related features.

# In[ ]:


# If all the categorical and numerical garage-related features are missing and equal to zero, respectively, then change the
# categorical features to 'NA' to indicate the absence of a garage.
houses.loc[(houses['GarageType'].isna()) & (houses['GarageYrBlt'].isna()) & (houses['GarageFinish'].isna()) &
          (houses['GarageCars']==0) & (houses['GarageArea']==0) & (houses['GarageQual'].isna()) &
          (houses['GarageCond'].isna()), ('GarageType', 'GarageYrBlt', 'GarageFinish', 'GarageQual', 'GarageCond')] = 'NA'
# Return all garage-related features if any are missing.
houses.loc[(houses['GarageType'].isna()) | (houses['GarageYrBlt'].isna()) | (houses['GarageFinish'].isna()) |
          (houses['GarageCars'].isna()) | (houses['GarageArea'].isna()) | (houses['GarageQual'].isna()) |
          (houses['GarageCond'].isna()), ('GarageType', 'GarageYrBlt', 'GarageFinish',
                                          'GarageCars', 'GarageArea', 'GarageQual', 'GarageCond')]


# First row: modal classes will be used to replace the missing values since this house seemingly does have a garage.
# Second row: non-sensical to replace six column values; more likely that the garage type column is erroneous and the house actually has no garage. Consequently, replace all of the catagorical features and numerical features with 'NA' and zero, respectively.

# In[ ]:


houses.loc[2576, ('GarageType', 'GarageYrBlt', 'GarageFinish', 'GarageQual', 'GarageCond')] = 'NA'
houses.loc[2576, ('GarageCars', 'GarageArea')] = 0
for column in ['GarageYrBlt', 'GarageFinish', 'GarageQual', 'GarageCond']:
    houses.loc[houses[column].isna(), column] = houses[column].mode()[0]


# In[ ]:


# Return houses with missing pool quality.
houses[houses['PoolQC'].isna()].loc[:, ('PoolArea', 'PoolQC')]


# In[ ]:


# Determining the mode for 'PoolArea'.
houses['PoolArea'].mode()[0]


# In[ ]:


# Determining the modal class for 'PoolQC'.
houses.groupby('PoolQC').count()['Id']


# Evidently, it is far more likely that a house does not have a pool, i.e. that pool area is zero and pool quality is 'NA'. Below will let us investigate pools with non-zero area.

# In[ ]:


# Return pool-related features for pools with non-zero area, sorted by pool area.
houses[houses['PoolArea']!=0].loc[:, ('PoolArea', 'PoolQC')].sort_values('PoolArea')


# After 'NA', there are two modal classes for pool quality. For pools with non-zero area, these two modal classes do not show any pattern. Consequently, it makes more sense to replace missing pool quality values with the second mode that is less extreme, i.e. with 'Gd' as opposed to 'Ex'.

# In[ ]:


houses.loc[houses['PoolQC'].isna(), 'PoolQC'] = 'Gd'
# Return column names and their respective percentage of missing values, if such percentage is postive.
for column in houses.columns.values:
    naPercent = sum(houses[column].isna())/len(houses[column])*100
    if naPercent > 0:
        print(column, round(naPercent, 2))


# These are the original test houses which should not have any value in 'SalePrice', so we will leave these missing values unchanged.

# # Feature Validity

# In[ ]:


# Changing the necessary features from integers to categories.
houses.loc[:, 'MSSubClass'] = pd.Categorical(houses['MSSubClass']) 
houses.loc[:, 'OverallQual'] = pd.Categorical(houses['OverallQual']) 
houses.loc[:, 'OverallCond'] = pd.Categorical(houses['OverallCond'])
houses.loc[:, 'MSSubClass'] = houses['MSSubClass'].astype(str)


# In[ ]:


# Return the unique vlaues of 'MSZoning'.
list(houses['MSZoning'].unique())


# In[ ]:


# Return houses with the erroneous 'C (all)' category in 'MSZoning', as well as their associated 'BedroomAbvGr' columns to
# establish whether or not these houses have bedrooms.
houses[houses['MSZoning']=='C (all)'].loc[:, ('MSZoning', 'BedroomAbvGr')].head()


# In[ ]:


# The houses above cannot be commercial since they all have bedrooms, so change 'C (all)' to the modal class.
houses.loc[(houses['MSZoning'] == 'C (all)'), 'MSZoning'] = houses['MSZoning'].mode()[0]
# Return the unique vlaues of 'BldgType'.
sorted(list(houses['BldgType'].unique()))


# In[ ]:


# Change the erroneous 'Twnhs' values to 'TwnhsI' (simply a 'typo').
houses.loc[houses['BldgType'] == 'Twnhs', 'BldgType'] = 'TwnhsI'
# Return the unique vlaues of 'GarageYrBlt'.
houses['GarageYrBlt'].unique()


# In[ ]:


# Changing erroneous value of 2207.0 to 2007 (a 'typo').
houses.loc[houses['GarageYrBlt']==2207.0, 'GarageYrBlt'] = 2007


# # Feature Characteristics

# ## Correlation

# One of the assumptions of linear regression is that all features must be uncorrelated with one another, so we establish the correlation between features (if any) and remove these features.

# In[ ]:


# Return features and their correlation if the correlation between two fetaures is >|0.65|.
m = houses.corr()
for i in range(len(m)):
    for j in range(len(m)):
        if (m.iloc[i,j] < -0.65 or m.iloc[i,j] > 0.65) and m.iloc[i,j]!=1:
            print(m.columns[i], '-', m.columns[j], ': ', m.iloc[i,j])
# Plot a heatmap showing the correlation between all variables in our data set.
plt.figure(figsize=[30,15])
sns.heatmap(houses.corr(), annot=True, cmap="YlGnBu")
plt.title('HEATMAP')
# Save this figure.
plt.savefig('heatmap.png')


# In[ ]:


# Removing highly-correlated features.
houses.drop(['GarageArea','1stFlrSF','TotRmsAbvGrd','2ndFlrSF'], axis=1, inplace=True)


# ## Outliers

# In[ ]:


# Plot a pairplot of all numerical features in our data set.
numericalColumns = ['LotFrontage','LotArea','YearBuilt','YearRemodAdd','MasVnrArea','BsmtFinSF1','BsmtFinSF2',
                    'BsmtUnfSF','TotalBsmtSF','LowQualFinSF','GrLivArea','WoodDeckSF','OpenPorchSF',
                    'EnclosedPorch','3SsnPorch','ScreenPorch','PoolArea','MiscVal']
sns.pairplot(houses.loc[:, numericalColumns]).savefig("pairplot.png")
plt.title(r'PAIRPLOT OF NUMERICAL VARIABLES')
# Save this figure.
plt.savefig('pairplot.png')


# It is difficult to see much from the figure due to its size, so any evaluation of this figure should be done using the saved image of the figure for zooming in and out purposes. After visual inspection of the pairplot, one can easily establish outliers.

# In[ ]:


# Return all outlying houses with outlying values established visually from the above pairplot.
outliers = list(houses.loc[houses['LotFrontage'] > 250].index.values)
outliers = outliers + list(houses.loc[houses['BsmtFinSF1'] > 5000].index.values)
outliers = outliers + list(houses.loc[houses['TotalBsmtSF'] > 6000].index.values)
outliers = outliers + list(houses.loc[houses['LowQualFinSF'] > 1000].index.values)
outliers = outliers + list(houses.loc[houses['WoodDeckSF'] > 1250].index.values)
outliers = outliers + list(houses.loc[houses['EnclosedPorch'] > 800].index.values)
outliers = outliers + list(houses.loc[houses['BsmtFinSF1'] > 5000].index.values)
outliers = list(set(outliers))
houses.loc[outliers, ('Id', 'LotFrontage', 'BsmtFinSF1', 'TotalBsmtSF', 'LowQualFinSF', 'WoodDeckSF', 'EnclosedPorch', 'BsmtFinSF1')]


# In[ ]:


# Remove all outlying houses from the training set.
# houses = houses.loc[(houses['Id']!=935) & (houses['Id']!=1299)]


# When removing the outliers, it became difficult to run the chosen models due to erroneous values like infinity and NaN in the training data set. As a result, we chose to keep the outliers, hence the above block of code being a comment.

# ## Feature Normality

# Where normality of features is not an assumption of linear regression, it can make models perform better. As a result, features that are too skewed are scaled using the Box Cox method.

# In[ ]:


# Determine which features are significantly skewed in distribution.
skew = houses.select_dtypes(include = ['int64','float64']).apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
skew_df = pd.DataFrame({'Skew':skew})
skewed_df = skew_df[(skew_df['Skew']>0.5) | (skew_df['Skew']<-0.5)]
skewedColumns = list(skewed_df.index.values)
skewedColumns.remove('SalePrice')
# Apply the Box Cox method of scaling to these skewed features.
lam = 0.1
for column in skewedColumns:
    houses[column] = boxcox1p(houses[column], lam)


# # Pre-Processing

# In[ ]:


# Use one-hot encoding on categorical features (dummy variables).
houses = pd.get_dummies(houses, prefix = 'D_')
# Split the whole data set back into training and test data sets.
train = houses[:len(train)]
test = houses[len(train):]
# Take the log of sale price due to its large range.
log = np.log(train['SalePrice'])
# Split the training set into X (a data set of features only) and y (sale price, the dependent variable).
train = train.drop('SalePrice', axis = 1)
train.loc[:, 'SalePrice'] = log
train = train.drop('Id', axis=1)
test = test.drop('Id', axis=1)
X = train.drop('SalePrice', axis=1)
y = train['SalePrice']
# Drop the sale price column in the test set, since this set never had values for this variable and are currently all NaNs.
test = test.drop('SalePrice', axis=1)
# Only used for the original 'Id' column, so that the final output CSV file can be created.
test1 = pd.read_csv('../input/test.csv')


# Having scaled features can make a model perform better. Since the training set still has outliers, the sklear Robust Scaler will be used because this scaler scales features and performs well with outliers. 

# In[ ]:


# Scaling variables.
sc = RobustScaler()
X = sc.fit_transform(X)
test = sc.transform(test)


# # Models

# ## Decision Tree

# In[ ]:


# Running a decision tree on our data set.
decisionTreeModel = DecisionTreeRegressor()
dt = decisionTreeModel.fit(X, y)
# Compute the R-squared.
decisionTreeModel.score(X, y)


# In[ ]:


# Use the model to predict the sale price of the test set.
predictions = dt.predict(test)
# Take the exponential of the predictions due to the log originally being taken.
predictions = np.exp(predictions)
# Save the predictions and their associated IDs to a CSV file.
predictions = pd.DataFrame(np.array([list(test1.iloc[:, 0].values), list(predictions)]))
predictions = predictions.T
predictions.columns = ['Id', 'SalePrice']
predictions = predictions.astype({'Id': int, 'SalePrice': float})
predictions = predictions.set_index('Id')
predictions.to_csv(r'DecisionTree.csv')


# ## Random Forest

# In[ ]:


# Running a random forest on our data set.
randomforestModel = RandomForestRegressor(n_estimators = 10)
rf = randomforestModel.fit(X, y)
# Compute the R-squared.
randomforestModel.score(X, y)


# In[ ]:


# Use the model to predict the sale price of the test set.
predictions = rf.predict(test)
# Take the exponential of the predictions due to the log originally being taken.
predictions = np.exp(predictions)
# Save the predictions and their associated IDs to a CSV file.
predictions = pd.DataFrame(np.array([list(test1.iloc[:, 0].values), list(predictions)]))
predictions = predictions.T
predictions.columns = ['Id', 'SalePrice']
predictions = predictions.astype({'Id': int, 'SalePrice': float})
predictions = predictions.set_index('Id')
predictions.to_csv(r'RandomForest.csv')


# ## LASSO

# In[ ]:


# Running the LASSO method on our data set.
lassoModel = linear_model.Lasso(alpha=0.001, max_iter=1000000)
lasso = lassoModel.fit(X, y)
# Compute the R-squared.
lassoModel.score(X, y)


# In[ ]:


# Use the model to predict the sale price of the test set.
predictions = lasso.predict(test)
# Take the exponential of the predictions due to the log originally being taken.
predictions = np.exp(predictions)
# Save the predictions and their associated IDs to a CSV file.
predictions = pd.DataFrame(np.array([list(test1.iloc[:, 0].values), list(predictions)]))
predictions = predictions.T
predictions.columns = ['Id', 'SalePrice']
predictions = predictions.astype({'Id': int, 'SalePrice': float})
predictions = predictions.set_index('Id')
predictions.to_csv(r'Lasso.csv')


# ## Ridge Regression

# In[ ]:


# Running ridge regression on our data set.
ridgeModel = linear_model.Ridge(alpha=0.001, max_iter=1000000)
ridge = ridgeModel.fit(X, y)
# Compute the R-squared.
ridgeModel.score(X, y)


# In[ ]:


# Use the model to predict the sale price of the test set.
predictions = ridge.predict(test)
# Take the exponential of the predictions due to the log originally being taken.
predictions = np.exp(predictions)
# Save the predictions and their associated IDs to a CSV file.
predictions = pd.DataFrame(np.array([list(test1.iloc[:, 0].values), list(predictions)]))
predictions = predictions.T
predictions.columns = ['Id', 'SalePrice']
predictions = predictions.astype({'Id': int, 'SalePrice': float})
predictions = predictions.set_index('Id')
predictions.to_csv(r'RidgeRegression.csv')


# ## Linear Regression

# Conventional linear regression is not compatable with our data once the sklearn Robust Scaler was used. As a result, we use the original cleaned data before the Robust Sclaler was used, to run linear regression.

# In[ ]:


# Split the whole data set back into training and test data sets.
train = houses[:len(train)]
test = houses[len(train):]
# Take the log of sale price due to its large range.
log = np.log(train['SalePrice'])
# Split the training set into X (a data set of features only) and y (sale price, the dependent variable).
train = train.drop('SalePrice', axis = 1)
train.loc[:, 'SalePrice'] = log
train = train.drop('Id', axis=1)
test = test.drop('Id', axis=1)
X = train.drop('SalePrice', axis=1)
y = train['SalePrice']
# Drop the sale price column in the test set, since this set never had values for this variable and are currently all NaNs.
test = test.drop('SalePrice', axis=1)
# Only used for the original 'Id' column, so that the final output CSV file can be created.
test1 = pd.read_csv('../input/test.csv')


# In[ ]:


# Running linear regression on our data set.
linearRegressionModel = LinearRegression()
lm = linearRegressionModel.fit(X, y)
# Compute the R-squared.
linearRegressionModel.score(X, y)


# In[ ]:


# Use the model to predict the sale price of the test set.
predictions = lm.predict(test)
# Take the exponential of the predictions due to the log originally being taken.
predictions = np.exp(predictions)
# Save the predictions and their associated IDs to a CSV file.
predictions = pd.DataFrame(np.array([list(test1.iloc[:, 0].values), list(predictions)]))
predictions = predictions.T
predictions.columns = ['Id', 'SalePrice']
predictions = predictions.astype({'Id': int, 'SalePrice': float})
predictions = predictions.set_index('Id')
predictions.to_csv(r'LinearRegression.csv')

