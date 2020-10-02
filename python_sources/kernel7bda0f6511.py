#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


# Calling libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# for data visulization
import matplotlib.pyplot as plt
import seaborn as sns

# for modeling estimators
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier as gbm
from xgboost.sklearn import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import  OneHotEncoder as ohe
from sklearn.preprocessing import StandardScaler as ss
from sklearn.compose import ColumnTransformer as ct
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.tree import  DecisionTreeClassifier as dt
import lightgbm as lgb



#for data processing
from sklearn.model_selection import train_test_split

#for tuning parameters
from bayes_opt import BayesianOptimization
from skopt import BayesSearchCV
from eli5.sklearn import PermutationImportance
from sklearn.metrics import accuracy_score
from sklearn.metrics import auc, roc_curve
from sklearn.metrics import f1_score
from sklearn.metrics import average_precision_score
import sklearn.metrics as metrics
from xgboost import plot_importance
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix

# Misc.
import os
import time
import gc


#Other Libraries

import random
from scipy.stats import uniform
import warnings


# In[ ]:


# data processing
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# In[ ]:


# Read Data
import os
print(os.listdir("../input"))

train=pd.read_csv("../input/train.csv")


# In[ ]:


# Explore data

train.shape


# In[ ]:


train.head(5)


# In[ ]:


train.plot(figsize = (14,12))


# Feature-Target Relationships

# In[ ]:


sns.countplot("Target", data=train)


# In[ ]:


sns.countplot(x="hhsize",hue="Target",data=train)


# Feature-Feature Relationships

# In[ ]:


from pandas.plotting import scatter_matrix
scatter_matrix(train.select_dtypes('float'), alpha=0.2, figsize=(26, 20), diagonal='kde')


# Distribution plots using seaborn

# In[ ]:


from collections import OrderedDict

plt.figure(figsize = (20, 16))
plt.style.use('fivethirtyeight')

# Color mapping
colors = OrderedDict({1: 'red', 2: 'orange', 3: 'blue', 4: 'green'})
poverty_mapping = OrderedDict({1: 'extreme', 2: 'moderate', 3: 'vulnerable', 4: 'non vulnerable'})

# Iterate through the float columns
for i, col in enumerate(train.select_dtypes('float')):
    ax = plt.subplot(4, 2, i + 1)
    # Iterate through the poverty levels
    for poverty_level, color in colors.items():
        # Plot each poverty level as a separate line
        sns.kdeplot(train.loc[train['Target'] == poverty_level, col].dropna(), 
                    ax = ax, color = color, label = poverty_mapping[poverty_level])
        
    plt.title(f'{col.capitalize()} Distribution'); plt.xlabel(f'{col}'); plt.ylabel('Density')

plt.subplots_adjust(top = 2)


# In[ ]:


#train['rooms'].value_counts().plot(kind='bar', hue='Target')
sns.countplot(x="rooms", hue= "Target", data=train, palette="cool")
plt.xlabel("No. of Rooms", fontsize=12)
plt.ylabel("No. of Household", fontsize=12)
plt.title("No. of Rooms in Households - Different poverty Class", fontsize=15)
plt.show()


# In[ ]:


train['Target'].value_counts().plot(kind='pie',  autopct='%1.1f%%')
plt.show()


# In[ ]:


sns.countplot(x="r4h3", hue= "Target", data=train, palette="cool")
plt.xlabel("No. of Males", fontsize=12)
plt.ylabel("No. of Household", fontsize=12)
plt.title("No. of Males in Households in different poverty Class", fontsize=15)
plt.show()


# In[ ]:


train.boxplot(column='r4h3', by='Target',patch_artist=True, )
plt.grid(True)
plt.xlabel("Class")
plt.ylabel("Males ")
plt.title("Boxplot of Males by Poverty Class ")
plt.suptitle("")
plt.show() 


# In[ ]:


sns.distplot( train["r4t3"], color= 'green',  hist= True, rug= True, bins=15).grid(True)
plt.xlabel("Total persons in the household")
#plt.ylabel("Males ")
plt.title("Household Size ")
plt.suptitle("")
plt.show() 


# In[ ]:


sns.violinplot( x=train["Target"], y=train["meaneduc"], linewidth=1)
plt.show()


# In[ ]:



#Rent paid
sns.violinplot( x=train["Target"], y=train["v2a1"], linewidth=1)
plt.show()


# In[ ]:


sns.countplot(x="refrig", hue= "Target", data=train, palette="cool")
plt.xlabel("Refrig", fontsize=12)
plt.ylabel("No. of Household", fontsize=12)
plt.title("No. of Refrigerators in Households in different poverty Class", fontsize=15)
plt.show()


# Engineering - Feature

# In[ ]:


# Create correlation matrix
#Subset only to the columns where parentesco1 == 1 because 
#this is the head of household, the correct label for each household.
heads = train.loc[train['parentesco1'] == 1].copy()
corr_matrix = heads.corr()

# Select upper triangle of correlation matrix
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

# Find index of feature columns with correlation greater than 0.95
to_drop = [column for column in upper.columns if any(abs(upper[column]) > 0.95)]

to_drop


# In[ ]:


corr_matrix.loc[corr_matrix['tamhog'].abs() > 0.9, corr_matrix['tamhog'].abs() > 0.9]


# Interpretation
# There are several variables here having to do with the size of the house:
# 
# r4t3: Total persons in the household
# 
# tamhog: size of the household
# 
# tamviv: number of persons living in the household
# 
# hhsize: household size
# 
# hogar_total: total individuals in the household
# 
# High correlation among variables. 
# hhsize- perfect correlation with tamhog and hogar_total
# 
# SQBhogar: Total individuals in the household and its square highly correlated
# SQBage and Age variables highly correlated

# Dropping Variables due to correlation

# In[ ]:


train.drop(['Id','idhogar','r4t3','tamhog','tamviv','hogar_total', 'SQBmeaned', 'SQBhogar_total',
            'SQBage','SQBescolari','SQBedjefe','SQBhogar_nin','SQBovercrowding','SQBdependency',
            'SQBmeaned','agesq'], inplace = True, axis=1)
train.shape


# Fill Missing Values

# In[ ]:


#pd.DataFrame(train.isnull().sum())

train.columns[train.isnull().sum()!=0]


# Variables Type having Missing values
# v2a1 - monthly rent
# 
# v18q1 - number of tablets
# 
# rez_esc - years behind school
# 
# meaneduc - mean education for adults
# 
# No categorical variable

# In[ ]:


#Replace the na values with the mean value of each variable
train['v2a1'] = train['v2a1'].fillna((train['v2a1'].mean()))
train['v18q1'] = train['v18q1'].fillna((train['v18q1'].mean()))
train['rez_esc'] = train['rez_esc'].fillna((train['rez_esc'].mean()))
train['meaneduc'] = train['meaneduc'].fillna((train['meaneduc'].mean()))
#Check if any na
train.columns[train.isnull().sum()!=0]


# Find Object (String) in the Data frame and converting them to Float

# In[ ]:


train.select_dtypes('object').head()


# In[ ]:


# Converting the string to float
yes_no_map = {'no':0,'yes':1}
train['dependency'] = train['dependency'].replace(yes_no_map).astype(np.float32)
train['edjefe'] = train['edjefe'].replace(yes_no_map).astype(np.float32)
train['edjefa'] = train['edjefa'].replace(yes_no_map).astype(np.float32)


# In[ ]:


# Testing for String 
train.select_dtypes('object').head()


# Preparing Data

# In[ ]:


# Splitting data into dependent and independent variable
# X is the independent variables matrix
X = train.drop('Target', axis = 1)

# y is the dependent variable vector
y = train.Target

# Scaling Features
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()

X_ss = ss.fit_transform(X)


# PCA

# In[ ]:


from sklearn.decomposition import PCA

pca = PCA(n_components=0.95)
X_PCA = pca.fit_transform(X_ss)

#Split in Train and Test and reseample data

Xdt_train, Xdt_test, ydt_train, ydt_test = train_test_split(X_PCA, y, random_state=1)


# In[ ]:


Xdt_test.shape


# Modelling

# 1. Random Forest Classifier

# In[ ]:


from sklearn.ensemble import RandomForestClassifier

anotherModel1 = RandomForestClassifier(n_estimators=100, max_features=2, oob_score=True, random_state=42)
anotherModel1 = anotherModel1.fit(Xdt_train, ydt_train)

ydt_pred1 = anotherModel1.predict(Xdt_test)
ydt_pred1


# In[ ]:


con_mat_dt = metrics.confusion_matrix(ydt_test, ydt_pred1)
#print(con_mat_dt)
sns.heatmap(con_mat_dt,annot=True,cmap='Blues', fmt='g')
plt.title('RFM Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
#plt.grid(True)
plt.show()


# In[ ]:


print('    Accuracy Report: Random Forest Model\n', classification_report(ydt_test, ydt_pred1))


# 2. Decision Tree Classifier

# In[ ]:


from sklearn.tree import DecisionTreeClassifier

anotherModel2 = DecisionTreeClassifier(max_depth=3, random_state=42)
anotherModel2 = anotherModel2.fit(Xdt_train, ydt_train)

ydt_pred2 = anotherModel2.predict(Xdt_test)
ydt_pred2


# In[ ]:


con_mat_dt = metrics.confusion_matrix(ydt_test, ydt_pred2)
sns.heatmap(con_mat_dt,annot=True,cmap='Reds', fmt='g')
plt.title('Decision Tree Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


# In[ ]:


print('    Accuracy Report: Decision Tree Model\n', classification_report(ydt_test, ydt_pred2))


# 3. Gradient Boost Classifier

# In[ ]:


from sklearn.ensemble import GradientBoostingClassifier as gbm

anotherModel3 = gbm()
anotherModel3 = anotherModel3.fit(Xdt_train, ydt_train)

ydt_pred3 = anotherModel3.predict(Xdt_test)
ydt_pred3


# In[ ]:


con_mat_dt = metrics.confusion_matrix(ydt_test, ydt_pred3)
sns.heatmap(con_mat_dt,annot=True,cmap='Greens', fmt='g')
plt.title('Decision Tree Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


# In[ ]:


print('    Accuracy Report: Gradient Boost Model\n', classification_report(ydt_test, ydt_pred3))


# 4. K Neighbors Classifier

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier

anotherModel4 = KNeighborsClassifier(n_neighbors=4)
anotherModel4 = anotherModel4.fit(Xdt_train, ydt_train)

ydt_pred4 = anotherModel4.predict(Xdt_test)
ydt_pred4


# In[ ]:


con_mat_dt = metrics.confusion_matrix(ydt_test, ydt_pred4)
sns.heatmap(con_mat_dt,annot=True,cmap='YlGnBu', fmt='g')
plt.title('K Neighbors Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


# In[ ]:


print('    Accuracy Report: K Neighbors Model\n', classification_report(ydt_test, ydt_pred4))


# 5. Light GBM

# In[ ]:


import lightgbm as lgb

anotherModel5 = lgb.LGBMClassifier()
anotherModel5 = anotherModel5.fit(Xdt_train, ydt_train)

ydt_pred5 = anotherModel5.predict(Xdt_test)
ydt_pred5

con_mat_dt = metrics.confusion_matrix(ydt_test, ydt_pred5)
sns.heatmap(con_mat_dt,annot=True,cmap='BuGn_r', fmt='g')
plt.title('Light GBM Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


# In[ ]:


print('    Accuracy Report: Light GBM Model\n', classification_report(ydt_test, ydt_pred5))


# 6. Logistic Regressioin with L1 Penalty

# In[ ]:


from sklearn.linear_model import LogisticRegression

anotherModel6 = LogisticRegression(C=0.1, penalty='l1')
anotherModel6 = anotherModel6.fit(Xdt_train, ydt_train)

ydt_pred6 = anotherModel6.predict(Xdt_test)
ydt_pred6

con_mat_dt = metrics.confusion_matrix(ydt_test, ydt_pred6)
sns.heatmap(con_mat_dt,annot=True,cmap='Oranges', fmt='g')
plt.title('Logistic Regressioin with L1 Penalty Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


# In[ ]:


print('    Accuracy Report: Logistic Regressioin with L1 Penalty Model\n', classification_report(ydt_test, ydt_pred6))


# 7. Extra Trees Classifier

# In[ ]:


from sklearn.ensemble import ExtraTreesClassifier

anotherModel7 = ExtraTreesClassifier()
anotherModel7 = anotherModel7.fit(Xdt_train, ydt_train)

ydt_pred7 = anotherModel7.predict(Xdt_test)
ydt_pred7

con_mat_dt = metrics.confusion_matrix(ydt_test, ydt_pred7)
sns.heatmap(con_mat_dt,annot=True,cmap='Blues', fmt='g')
plt.title('Logistic Extra Trees Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


# In[ ]:


print('    Accuracy Report: Extra Trees Model\n', classification_report(ydt_test, ydt_pred7))


# 8. XGB Classifier
# 

# In[ ]:


from xgboost.sklearn import XGBClassifier as XGB

anotherModel8 = XGB()
anotherModel8 = anotherModel8.fit(Xdt_train, ydt_train)

ydt_pred8 = anotherModel8.predict(Xdt_test)
ydt_pred8

con_mat_dt = metrics.confusion_matrix(ydt_test, ydt_pred8)
sns.heatmap(con_mat_dt,annot=True,cmap='BuGn', fmt='g')
plt.title('XGB Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


# In[ ]:


print('    Accuracy Report: XGB Model\n', classification_report(ydt_test, ydt_pred8))


# Maximum F1 value obtained by Model K Neighbors Classifier
# Applying it to the test data

# In[ ]:


from bayes_opt import BayesianOptimization
from skopt import BayesSearchCV as BayesSCV

bayes_tuner = BayesSCV(RandomForestClassifier(n_jobs = 2),

    #  Estimator parameters to be change/tune
    {
        'n_estimators': (100, 500),           
        'criterion': ['gini', 'entropy'],    
        'max_depth': (4, 100),               
        'max_features' : (10,64),             
        'min_weight_fraction_leaf' : (0,0.5, 'uniform')   
    },

    # 2.13
    n_iter=32,            
    cv = 3               
)


# In[ ]:


#bayes_cv_tuner.fit(Xdt_train, ydt_train)


# In[ ]:


test=pd.read_csv("../input/test.csv")
#test=pd.read_table("F:\\Big Data Analytics\\Homework\\Costa Rican problem\\test.csv", engine='python', sep=',')


# In[ ]:


test.drop(['Id','idhogar','r4t3','tamhog','tamviv','hogar_total', 'SQBmeaned', 'SQBhogar_total',
            'SQBage','SQBescolari','SQBedjefe','SQBhogar_nin','SQBovercrowding','SQBdependency',
            'SQBmeaned','agesq'], inplace = True, axis=1)
test.shape


# In[ ]:


test.columns[test.isnull().sum()!=0]


# In[ ]:


#Replace the na values with the mean value of each variable
test['v2a1'] = test['v2a1'].fillna((test['v2a1'].mean()))
test['v18q1'] = test['v18q1'].fillna((test['v18q1'].mean()))
test['rez_esc'] = test['rez_esc'].fillna((test['rez_esc'].mean()))
test['meaneduc'] = test['meaneduc'].fillna((test['meaneduc'].mean()))
#Check if any na
test.columns[test.isnull().sum()!=0]


# In[ ]:


test.select_dtypes('object').head()


# In[ ]:


# Converting the string to float
yes_no_map = {'no':0,'yes':1}
test['dependency'] = test['dependency'].replace(yes_no_map).astype(np.float32)
test['edjefe'] = test['edjefe'].replace(yes_no_map).astype(np.float32)
test['edjefa'] = test['edjefa'].replace(yes_no_map).astype(np.float32)


# In[ ]:


test_ss = ss.fit_transform(test)


# In[ ]:


test_ss.shape


# In[ ]:


pca = PCA(n_components=83)
test_PCA = pca.fit_transform(test_ss)

ydt_pred41 = anotherModel4.predict(test_PCA)
ydt_pred41


# In[ ]:


unique_elements, counts_elements = np.unique(ydt_pred41, return_counts=True)
print(np.asarray((unique_elements, counts_elements)))


# In[ ]:


#Saving as tab - seperated values
ydt_pred41.tofile('submit.csv', sep='\t')


# In[ ]:




