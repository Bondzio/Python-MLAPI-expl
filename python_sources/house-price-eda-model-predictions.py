#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)


# Here's a brief version of what you'll find in the data description file.
# 
# * SalePrice - the property's sale price in dollars. This is the target variable that you're trying to predict.
# * MSSubClass: The building class
# * MSZoning: The general zoning classification
# * LotFrontage: Linear feet of street connected to property
# * LotArea: Lot size in square feet
# * Street: Type of road access
# * Alley: Type of alley access
# * LotShape: General shape of property
# * LandContour: Flatness of the property
# * Utilities: Type of utilities available
# * LotConfig: Lot configuration
# * LandSlope: Slope of property
# * Neighborhood: Physical locations within Ames city limits
# * Condition1: Proximity to main road or railroad
# * Condition2: Proximity to main road or railroad (if a second is present)
# * BldgType: Type of dwelling
# * HouseStyle: Style of dwelling
# * OverallQual: Overall material and finish quality
# * OverallCond: Overall condition rating
# * YearBuilt: Original construction date
# * YearRemodAdd: Remodel date
# * RoofStyle: Type of roof
# * RoofMatl: Roof material
# * Exterior1st: Exterior covering on house
# * Exterior2nd: Exterior covering on house (if more than one material)
# * MasVnrType: Masonry veneer type
# * MasVnrArea: Masonry veneer area in square feet
# * ExterQual: Exterior material quality
# * ExterCond: Present condition of the material on the exterior
# * Foundation: Type of foundation
# * BsmtQual: Height of the basement
# * BsmtCond: General condition of the basement
# * BsmtExposure: Walkout or garden level basement walls
# * BsmtFinType1: Quality of basement finished area
# * BsmtFinSF1: Type 1 finished square feet
# * BsmtFinType2: Quality of second finished area (if present)
# * BsmtFinSF2: Type 2 finished square feet
# * BsmtUnfSF: Unfinished square feet of basement area
# * TotalBsmtSF: Total square feet of basement area
# * Heating: Type of heating
# * HeatingQC: Heating quality and condition
# * CentralAir: Central air conditioning
# * Electrical: Electrical system
# * 1stFlrSF: First Floor square feet
# * 2ndFlrSF: Second floor square feet
# * LowQualFinSF: Low quality finished square feet (all floors)
# * GrLivArea: Above grade (ground) living area square feet
# * BsmtFullBath: Basement full bathrooms
# * BsmtHalfBath: Basement half bathrooms
# * FullBath: Full bathrooms above grade
# * HalfBath: Half baths above grade
# * Bedroom: Number of bedrooms above basement level
# * Kitchen: Number of kitchens
# * KitchenQual: Kitchen quality
# * TotRmsAbvGrd: Total rooms above grade (does not include bathrooms)
# * Functional: Home functionality rating
# * Fireplaces: Number of fireplaces
# * FireplaceQu: Fireplace quality
# * GarageType: Garage location
# * GarageYrBlt: Year garage was built
# * GarageFinish: Interior finish of the garage
# * GarageCars: Size of garage in car capacity
# * GarageArea: Size of garage in square feet
# * GarageQual: Garage quality
# * GarageCond: Garage condition
# * PavedDrive: Paved driveway
# * WoodDeckSF: Wood deck area in square feet
# * OpenPorchSF: Open porch area in square feet
# * EnclosedPorch: Enclosed porch area in square feet
# * 3SsnPorch: Three season porch area in square feet
# * ScreenPorch: Screen porch area in square feet
# * PoolArea: Pool area in square feet
# * PoolQC: Pool quality
# * Fence: Fence quality
# * MiscFeature: Miscellaneous feature not covered in other categories
# * MiscVal: $Value of miscellaneous feature
# * MoSold: Month Sold
# * YrSold: Year Sold
# * SaleType: Type of sale
# * SaleCondition: Condition of sale

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# ## READING DATA

# In[ ]:


#reading test and train data
data = pd.read_csv('../input/home-data-for-ml-course/train.csv',index_col='Id')
test = pd.read_csv('../input/home-data-for-ml-course/test.csv',index_col='Id')


# In[ ]:


#check the train data
data.head()


# In[ ]:


data.info()


# In[ ]:


#missing values
missing = data.isnull().sum()
missing = missing[missing>0]
missing.sort_values(inplace=True)
missing.plot.bar()


# We have 81 columns, 5 of them have around %50 missing value.

# In[ ]:


print(missing)


# **I am going to explore the numerical column and categorical columns separetly...**

# ## Numerical Columns

# In[ ]:


#Let's going to start with numerical columns
print('Numerical colums:  \n', data.select_dtypes(exclude=['object']).columns)


# In[ ]:


print('Number of Numerical Columns: \n', len(data.select_dtypes(exclude=['object']).columns))


# In[ ]:



print('Statistic of Numerical Columns: \n', data.select_dtypes(exclude=['object']).describe())


# ### Target Column 

# In[ ]:


target = data.SalePrice
plt.figure(figsize=(10,10))

plt.subplot(2,2,1)
plt.title('Distribution of SalePrice')
sns.distplot(target)

plt.subplot(2,2,2)
plt.title('Distribution of Log-Transformed SalePrice')
sns.distplot(np.log(target))


# In[ ]:


numerical_features = data.select_dtypes(exclude=['object']).drop(['SalePrice'], axis=1).copy()
#numerical_features.head()


# In[ ]:


print(numerical_features .columns)


# In[ ]:


fig = plt.figure(figsize=(12,18))
for i in range(len(numerical_features.columns)):
    fig.add_subplot(9,4,i+1)
    sns.distplot(numerical_features.iloc[:,i].dropna())
    plt.xlabel(numerical_features.columns[i])
plt.tight_layout()
plt.show()


# In[ ]:


fig = plt.figure(figsize=(12,18))
for i in range(len(numerical_features.columns)):
    fig.add_subplot(9,4,i+1)
    sns.boxplot(y=numerical_features.iloc[:,i])

plt.tight_layout()
plt.show()


# ### Bivariate analysis - scatter plots for target versus numerical attributes

# In[ ]:


fig = plt.figure(figsize=(12,18))
for i in range(len(numerical_features.columns)):
    fig.add_subplot(9,4,i+1)
    sns.scatterplot(numerical_features.iloc[:,i],target)
plt.tight_layout()
plt.show()


# ### How are numeric features related to SalePrice

# In[ ]:



correlation_num = data.select_dtypes(exclude='object').corr()
plt.figure(figsize=(30,14))
plt.title('Correlation between each feature related to size and SalePrice')
sns.heatmap(data=correlation_num, annot=True)


# In[ ]:


#For better understanding I would like yp plot the corr> 0.80
correlation_num = data.select_dtypes(exclude='object').corr()
plt.figure(figsize=(30,14))
plt.title('Correlation between each feature related to size and SalePrice')
sns.heatmap(data=correlation_num>0.80, annot=True)


# **This following columns highly correlated with each other**
# * 1stFlrSF - TotalBsmtSF
# * GarageYrBlt - YearBuilt
# * TotRmsAbvGrd - GrLivArea
# * YearRemodAdd - GarageYrBlt

# ## Exploring Categorical Columns
# 

# In[ ]:


print(data.select_dtypes(include='object').columns)


# In[ ]:


#shows the count, unique value and frequent values and top values in categorical data
print(data.select_dtypes(include='object').describe())


# In[ ]:


categorical = data.select_dtypes(include=('object'))
print(data.select_dtypes(include=('object')).isnull().sum() )


# In[ ]:


print(data.select_dtypes(include='object').nunique())


# In[ ]:


fig = plt.figure(figsize=(18,8))
sns.boxplot(x=data.Neighborhood, y=target)
plt.xticks(rotation=90)
plt.show()


# In[ ]:


fig = plt.figure(figsize=(18,8))
sns.boxplot(x=data.Street , y=target)
plt.xticks(rotation=90)
plt.show()


# In[ ]:


fig = plt.figure(figsize=(12,6))
sns.boxplot(x=data.KitchenQual, y=target)

plt.show()


# In[ ]:


fig = plt.figure(figsize=(18,8))
sns.boxplot(x=data.Exterior1st, y=target)
plt.xticks(rotation=90)
plt.show()


# ### Data cleaning & Preprocessing

# In[ ]:


#BEfore handling missing values let's copy our data

data_copy = data.copy()
data_copy[:50]


# In[ ]:


print(data_copy.select_dtypes(include='object').isnull().sum())


# **Data Cleaning Process **
# * Remove the hight correlated data witch cause data lekeage.
#     * Excluding GarageArea - highly (0.88) correlated with GarageCars, which has a higher corr with Price
#     * Excluding GarageYrBlt - highly (0.83) correlated with YearBuilt
# * A few columns has low correlation with saleprice but I would like combine the a few of them with creating a few column
#     * TotalSF' = 'TotalBsmtSF' + '1stFlrSF' + '2ndFlrSF'
#     * 'Total_sqr_footage' = 'BsmtFinSF1' + features'BsmtFinSF2' +'1stFlrSF''2ndFlrSF'
#     * 'Total_Bathrooms' = 'FullBath' + (0.5 * 'HalfBath') +'BsmtFullBath' + (0.5 * 'BsmtHalfBath')
#     * 'Total_porch_sf' = 'OpenPorchSF' + '3SsnPorch' +'EnclosedPorch'+ 'ScreenPorch' +'WoodDeckSF'
# * Create new features: If the data in the columns more then zero it will go with True(1) otherwise false(0)
#     * new['haspool'] = data['PoolArea'].apply(lambda x: 1 if x > 0 else 0)
#     * new['has2ndfloor'] = data['2ndFlrSF'].apply(lambda x: 1 if x > 0 else 0)
#     * new['hasgarage'] = data['GarageArea'].apply(lambda x: 1 if x > 0 else 0)
#     * new['hasbsmt'] = data['TotalBsmtSF'].apply(lambda x: 1 if x > 0 else 0)
#     * new['hasfireplace'] = data['Fireplaces'].apply(lambda x: 1 if x > 0 else 0)
#     
#  * Remove the column already used and hight correlated 
#  * Deal with categorical data and remove athe column more than 10 categorical vaalues .
#     
# * We need to deal with  LotFrontage, LotFrontage with the mean value using Simple 

# **Data Cleaning Process **
# * Remove the hight correlated data witch cause data lekeage.
#     * Excluding GarageArea - highly (0.88) correlated with GarageCars, which has a higher corr with Price
#     * Excluding GarageYrBlt - highly (0.83) correlated with YearBuilt
# * A few columns has low correlation with saleprice but I would like combine the a few of them with creating a few column
#     * TotalSF' = 'TotalBsmtSF' + '1stFlrSF' + '2ndFlrSF'
#     * 'Total_sqr_footage' = 'BsmtFinSF1' + features'BsmtFinSF2' +'1stFlrSF''2ndFlrSF'
#     * 'Total_Bathrooms' = 'FullBath' + (0.5 * 'HalfBath') +'BsmtFullBath' + (0.5 * 'BsmtHalfBath')
#     * 'Total_porch_sf' = 'OpenPorchSF' + '3SsnPorch' +'EnclosedPorch'+ 'ScreenPorch' +'WoodDeckSF'
# * Create new features: If the data in the columns more then zero it will go with True(1) otherwise false(0)
#     * new['haspool'] = data['PoolArea'].apply(lambda x: 1 if x > 0 else 0)
#     * new['has2ndfloor'] = data['2ndFlrSF'].apply(lambda x: 1 if x > 0 else 0)
#     * new['hasgarage'] = data['GarageArea'].apply(lambda x: 1 if x > 0 else 0)
#     * new['hasbsmt'] = data['TotalBsmtSF'].apply(lambda x: 1 if x > 0 else 0)
#     * new['hasfireplace'] = data['Fireplaces'].apply(lambda x: 1 if x > 0 else 0)
#     
#  * Remove the column already used and hight correlated 
#  * Deal with categorical data and remove athe column more than 10 categorical vaalues .
#      * ['Neighborhood', 'Exterior1st', 'Exterior2nd']
#     
# * We need to deal with  LotFrontage, LotFrontage with the mean value using Simple '']

# In[ ]:


data_copy['TotalSF'] = data_copy['TotalBsmtSF'] + data_copy['1stFlrSF'] +data_copy['2ndFlrSF']
data_copy['Total_Bathrooms'] = data_copy['FullBath'] + (0.5* data_copy['HalfBath']) + data_copy['BsmtFullBath'] + (0.5* data_copy['BsmtHalfBath'])
data_copy['Total_sqrt_footage'] = data_copy['BsmtFinSF1'] +data_copy['BsmtFinSF2'] + data_copy['1stFlrSF']+data_copy['2ndFlrSF']
data_copy['Total_porch_SF'] = data_copy['OpenPorchSF'] + data_copy['3SsnPorch'] +data_copy['EnclosedPorch'] +  data_copy['ScreenPorch'] + data_copy['WoodDeckSF']


# In[ ]:


#do the same process for test data
test['TotalSF'] = test['TotalBsmtSF'] + test['1stFlrSF'] +test['2ndFlrSF']
test['Total_Bathrooms'] = test['FullBath'] + (0.5* test['HalfBath']) + test['BsmtFullBath'] + (0.5* test['BsmtHalfBath'])
test['Total_sqrt_footage'] = test['BsmtFinSF1'] +test['BsmtFinSF2'] + test['1stFlrSF']+test['2ndFlrSF']
test['Total_porch_SF'] = test['OpenPorchSF'] + test['3SsnPorch'] +test['EnclosedPorch'] +  test['ScreenPorch'] + test['WoodDeckSF']


# In[ ]:


#new features 
data_copy['haspool'] = data_copy['PoolArea'].apply(lambda x:1 if x>0 else 0)
data_copy['has2ndFloor'] = data_copy['2ndFlrSF'].apply(lambda x:1 if x>0 else 0)
data_copy['hasgarage'] = data_copy['GarageArea'].apply(lambda x:1 if x>0 else 0)
data_copy['hasbsmt'] = data_copy['TotalBsmtSF'].apply(lambda x:1 if x>0 else 0)
data_copy['hasfireplace'] = data_copy['Fireplaces'].apply(lambda x:1 if x>0 else 0)


# In[ ]:


#do same process for test data
test['haspool'] = test['PoolArea'].apply(lambda x:1 if x>0 else 0)
test['has2ndFloor'] = test['2ndFlrSF'].apply(lambda x:1 if x>0 else 0)
test['hasgarage'] = test['GarageArea'].apply(lambda x:1 if x>0 else 0)
test['hasbsmt'] = test['TotalBsmtSF'].apply(lambda x:1 if x>0 else 0)
test['hasfireplace'] = test['Fireplaces'].apply(lambda x:1 if x>0 else 0)


# In[ ]:


#add_count_colum_with more the 10 fetures
import category_encoders as ce
count_cat_colums = ['Neighborhood', 'Exterior1st','Exterior2nd']

count_enc = ce.TargetEncoder(cols=count_cat_colums)
count_enc.fit(data_copy[count_cat_colums], data_copy.SalePrice)

data_copy = data_copy.join(count_enc.transform(data_copy[count_cat_colums]).add_suffix('_count'))
test = test.join(count_enc.transform(test[count_cat_colums]).add_suffix('_count'))


# In[ ]:


#add a buildg year as a new feture
import datetime
now = datetime.datetime.now()
building_age = now.year - data_copy['YearBuilt']
data_copy['building_age'] = now.year - data_copy['YearBuilt']
test['building_age'] = now.year - test['YearBuilt']


# In[ ]:


# Remove outliers based on observations on scatter plots against SalePrice:
data_copy = data_copy.drop(data_copy['LotFrontage']
                                     [data_copy['LotFrontage']>200].index)
data_copy = data_copy.drop(data_copy['LotArea']
                                     [data_copy['LotArea']>100000].index)
data_copy = data_copy.drop(data_copy['BsmtFinSF1']
                                     [data_copy['BsmtFinSF1']>4000].index)
data_copy = data_copy.drop(data_copy['TotalBsmtSF']
                                     [data_copy['TotalBsmtSF']>6000].index)
data_copy = data_copy.drop(data_copy['1stFlrSF']
                                     [data_copy['1stFlrSF']>4000].index)
data_copy = data_copy.drop(data_copy.GrLivArea
                                     [(data_copy['GrLivArea']>4000) & 
                                      (data_copy.SalePrice<300000)].index)
data_copy = data_copy.drop(data_copy.LowQualFinSF
                                     [data_copy['LowQualFinSF']>550].index)


# In[ ]:


data_copy.head()


# In[ ]:


#remove_columns = ['GarageArea','Neighborhood', 'Exterior1st','Exterior2nd','GarageYrBlt']
remove_columns = ['MiscVal', 'MSSubClass', 'MoSold', 'YrSold','GarageArea', 'GarageYrBlt', 'TotRmsAbvGrd']


# In[ ]:


#before remove the columns copy the data frame
data_copy_second = data_copy.copy()


# In[ ]:


data_copy_second.head()


# In[ ]:


data_copy_second = data_copy_second.drop(remove_columns, axis=1)


# In[ ]:


data_copy_second.head()


# In[ ]:


y = data_copy_second.SalePrice
X = data_copy_second.drop('SalePrice', axis=1)


# In[ ]:


#X.info()


# In[ ]:


from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import LogisticRegression #logistic regression
from sklearn.linear_model import LinearRegression
from sklearn import svm #support vector Machine
from sklearn.ensemble import RandomForestClassifier #Random Forest
from sklearn.neighbors import KNeighborsClassifier #KNN
from sklearn.naive_bayes import GaussianNB #Naive bayes
from sklearn.tree import DecisionTreeClassifier #Decision Tree
from sklearn.model_selection import train_test_split #training and testing data split
from sklearn import metrics #accuracy measure
from sklearn.metrics import confusion_matrix #for confusion matrix
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import GradientBoostingRegressor


# In[ ]:


train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1,test_size=0.2)


# In[ ]:


#to find out columns has the more then 10 unique values
categorical_cols = [cname for cname in X.columns if 
                    X[cname].dtype == "object"]

numrical_cols = [cname for cname in X.columns if
                 X[cname].dtype in ['int64','float64']]
my_cols = numrical_cols + categorical_cols

X_train = train_X[my_cols].copy()
X_valid = val_X[my_cols].copy()
X_test = test[my_cols].copy()


# In[ ]:



from sklearn.linear_model import LogisticRegression #logistic regression
from sklearn import svm #support vector Machine
from sklearn.ensemble import RandomForestClassifier #Random Forest
from sklearn.neighbors import KNeighborsClassifier #KNN
from sklearn.naive_bayes import GaussianNB #Naive bayes
from sklearn.tree import DecisionTreeClassifier #Decision Tree
from sklearn.model_selection import train_test_split #training and testing data split
from sklearn import metrics #accuracy measure
from sklearn.metrics import confusion_matrix #for confusion matrix

 
numrical_transform = Pipeline(steps=[
    ('num_imputer', SimpleImputer(strategy='constant')),
    ('num_scaler', RobustScaler())
    ])

categorical_transform = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numrical_transform, numrical_cols),       
        ('cat',categorical_transform,categorical_cols),
        ])


# In[ ]:


#model = RandomForestRegressor(n_estimators=100, random_state=0)

model =XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
             colsample_bynode=1, colsample_bytree=1, gamma=0,
             importance_type='gain', learning_rate=0.1, max_delta_step=0,
             max_depth=3, min_child_weight=1, missing=None, n_estimators=900,
             n_jobs=1, nthread=None, objective='reg:linear', random_state=0,
             reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
             silent=None, subsample=1, verbosity=1)
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model',model),
                      ])

clf.fit(X_train, train_y)
preds = clf.predict(X_valid)
score = mean_absolute_error(val_y, preds)
print('MAE: ', score)


# In[ ]:


scores=[]
#classifiers = ['Linear Svm', 'Radial Svm', 'Logistic Regression', 'KNN', 'Decision Tree', 'Random Forest']
#models = [svm.SVC(kernel='linear'), svm.SVC(kernel='rbf'), LogisticRegression(solver='liblinear'), KNeighborsClassifier(n_neighbors=9), 
 #         DecisionTreeClassifier(),  RandomForestClassifier(n_estimators=100)]

classifiers = ['XGBRegressor','Linear_Regression','Lasso','Ridge','Elastic','Gradient']
models =[XGBRegressor(n_estimators=1000, learning_rate=0.05), LinearRegression(),Lasso(alpha=0.0005, random_state=5), 
         Ridge(alpha=0.002, random_state=5),ElasticNet(alpha=0.02, random_state=5, l1_ratio=0.7),
         GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=4, random_state=5)]

for i in models:
    model  = i
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model',model),
                      ])
    clf.fit(X_train, train_y)
    preds = clf.predict(X_valid)
    score = mean_absolute_error(val_y, preds)
    scores.append( score)
    print(classifiers, scores)
new_models_data_frame = pd.DataFrame({'Score': scores}, index=classifiers)
new_models_data_frame
    


# In[ ]:


from sklearn.model_selection import GridSearchCV
model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
estimator = range(100, 1000, 100)
learning_r = [0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
hyper = {'n_estimators':estimator, 'learning_rate':learning_r}
model = GridSearchCV(estimator=XGBRegressor(), param_grid=hyper, verbose=True)
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model',model),
                      ])
clf.fit(X_train, train_y)
print(model.best_score_)
print(model.best_estimator_)


# In[ ]:






# In[ ]:





# In[ ]:


#Trying Lasso algoritm
numrical_transform = Pipeline(steps=[
    ('num_imputer', SimpleImputer(strategy='constant')),
    ('num_scaler', RobustScaler())
    ])

categorical_transform = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])


preprocessor = ColumnTransformer(
    transformers=[
        ('num', numrical_transform, numrical_cols),       
        ('cat',categorical_transform,categorical_cols),
        ])

lasso_model = Lasso(alpha=0.0001, random_state=5)


lasso_clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model',lasso_model),
                      
                     ])


lasso_clf.fit(X_train, train_y)
lasso_val_predictions = lasso_clf.predict(X_valid)
lasso_val_mae = mean_absolute_error(val_y, lasso_val_predictions)
print(lasso_val_mae)


# In[ ]:


preds_test = clf.predict(X_test)


# In[ ]:


output = pd.DataFrame({'Id': X_test.index,
                       'SalePrice': preds_test})
output.to_csv('submission.csv', index=False)

