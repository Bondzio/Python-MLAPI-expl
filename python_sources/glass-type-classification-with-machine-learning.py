#!/usr/bin/env python
# coding: utf-8

# # Glass type classification with machine learning

# I'm a data science newbie and this is my first Kaggle notebook. Here's my plan of attack for the glass classification problem.
# 
# # Contents
# 
# ## 1) Prepare Problem
# 
#  * Load libraries
# 
#  * Load and explore the shape of the dataset
# 
# ## 2) Summarize Data
# 
# * Descriptive statistics
# 
# * Data visualization
# 
# ## 3) Prepare Data
# 
# * Data Cleaning
# 
# * Split-out validation dataset
# 
# *  Data transformation  
# 
# ## 4) Evaluate Algorithms
# 
# * Dimensionality reduction
# 
# * Compare Algorithms
# 
# ## 5) Improve Accuracy
# 
# * Algorithm Tuning
# 
# ## 6) Diagnose the performance of the best algorithms
# 
# * Diagnose overfitting by plotting the learning and validation curves
# * Further tuning
# 
# ## 7) Finalize Model
# 
# * Create standalone model on entire training dataset
# 
# * Predictions on test dataset

# ## 1. Prepare Problem

# ### Loading the libraries 

# Let us first begin by loading the libraries that we'll use in the notebook

# In[ ]:


import numpy as np  # linear algebra
import pandas as pd  # read dataframes
import matplotlib.pyplot as plt # visualization
import seaborn as sns # statistical visualizations and aesthetics
from sklearn.base import TransformerMixin # To create new classes for transformations
from sklearn.preprocessing import (FunctionTransformer, StandardScaler) # preprocessing 
from sklearn.decomposition import PCA # dimensionality reduction
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from scipy.stats import boxcox # data transform
from sklearn.model_selection import (train_test_split, KFold , StratifiedKFold,
                                     cross_val_score, GridSearchCV ) # model selection modules
from sklearn.pipeline import Pipeline # streaming pipelines
from sklearn.base import BaseEstimator, TransformerMixin # To create a box-cox transformation class
from collections import Counter
import warnings
# load models
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import (XGBClassifier, plot_importance)
from sklearn.svm import SVC
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier, GradientBoostingClassifier)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from time import time
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Loading and exploring the shape of the dataset

# In[ ]:


warnings.filterwarnings('ignore')
df = pd.read_csv('../input/glass.csv')
features = df.columns[:-1].tolist()
print(df.shape)


# The dataset consists of 214 observations

# In[ ]:


df.head(15)


# In[ ]:


df.dtypes


# ## 2. Summarize data

# ### Descriptive statistics

# Let's first summarize the distribution of the numerical variables.

# In[ ]:


df.describe()


# The features are not on the same scale. For example Si has a mean of 72.65 while Fe has a mean value of 0.057. Features should be on the same scale for an algorithm such as logistic regression (gradient descent) to converge fast. Let's go ahead and check the distribution of the glass types.

# In[ ]:


df['Type'].value_counts()


# The dataset is pretty unbalanced. The instances of types 1 and 2 constitute more than 67 % of the glass types.

# ###  Data Visualization

# * **Univariate plots**

# Let's go ahead an look at the distribution of the different features of this dataset.

# In[ ]:


for feat in features:
    skew = df[feat].skew()
    sns.distplot(df[feat], label='Skew = %.3f' %(skew))
    plt.legend(loc='best')
    plt.show()


# None of the features is normally distributed. The features Fe, Ba, Ca and K exhibit the highest skew coefficients. Moreover, the distribution of potassium (K) and Barium (Ba) seem to contain many outliers.
# Let's identify the indices of the observations containing outliers using [Turkey's method](http://datapigtechnologies.com/blog/index.php/highlighting-outliers-in-your-data-with-the-tukey-method/).
# 

# In[ ]:


# Detect observations with more than one outlier

def outlier_hunt(df):
    """
    Takes a dataframe df of features and returns a list of the indices
    corresponding to the observations containing more than 1 outlier. 
    """
    outlier_indices = []
    
    # iterate over features(columns)
    for col in df.columns.tolist():
        # 1st quartile (25%)
        Q1 = np.percentile(df[col], 25)
        
        # 3rd quartile (75%)
        Q3 = np.percentile(df[col],75)
        
        # Interquartile rrange (IQR)
        IQR = Q3 - Q1
        
        # outlier step
        outlier_step = 1.5 * IQR
        
        # Determine a list of indices of outliers for feature col
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step )].index
        
        # append the found outlier indices for col to the list of outlier indices 
        outlier_indices.extend(outlier_list_col)
        
    # select observations containing more than 2 outliers
    outlier_indices = Counter(outlier_indices)        
    multiple_outliers = list( k for k, v in outlier_indices.items() if v > 1 )
    
    return multiple_outliers   

print('The dataset contains %d observations with multiple outliers' %(len(outlier_hunt(df[features]))))   


# Aha! there exists some 35 observations with multiple outliers.  These  could harm the efficiency of our learning algorithms. We'll make sure to get rid of these in the next sections.
# 
# Let's examine the boxplots for the several distributions.

# In[ ]:


sns.boxplot(df[features])
plt.show()


# Unsurprisingly, Silicon has a mean that is much superior to the other constituents as we already saw in the previous section. Well, that is normal since glass is mainly based on silica.

# * **Multivariate plots**

# Let's now proceed by drawing a pairplot to visually examine the correlation between the features.

# In[ ]:


plt.figure(figsize=(8,8))
sns.pairplot(df[features],palette='coolwarm')
plt.show()


# Let's go ahead and examine a heatmap of the correlations.

# In[ ]:


corr = df[features].corr()
plt.figure(figsize=(14,14))
sns.heatmap(corr, cbar = True,  square = True, annot=True, fmt= '.2f',annot_kws={'size': 15},
           xticklabels= features, yticklabels= features,
           cmap= 'coolwarm')
plt.show()
print(corr)


# There seems to be a strong positive correlation between RI and Ca. This could be a hint to perform Principal component analysis in order to decorrelate some of the input features.

# ## 3. Prepare data

# ### - Data cleaning 

# In[ ]:


df.info()


# This dataset is clean; there aren't any missing values in it.

# ### - Hunting and removing multiple outliers
# 
# Let's remove the observations containing multiple outliers with the function we created in the previous section.

# In[ ]:


outlier_indices = outlier_hunt(df[features])
df = df.drop(outlier_indices).reset_index(drop=True)
print(df.shape)
print(df.tail())


# Removing observations with multiple outliers leaves us with 179 observations to learn from. Not that much! Let's now see how our distributions look like.

# In[ ]:


for feat in features:
    skew = df[feat].skew()
    sns.distplot(df[feat], label='Skew = %.3f' %(skew))
    plt.legend(loc='best')
    plt.show()


# In[ ]:


df['Type'].value_counts()


# ### - Split-out validation dataset

# In[ ]:


# Define X as features and y as lablels
X = df[features] 
y = df['Type'] 
# set a seed and a test size for splitting the dataset 
seed = 7
test_size = 0.2

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size , random_state = seed)


# ### - Data transformation  

# Let's examine if a Box-Cox transform can contribute to the normalization of some features. It should be emphasized that all transformations should only be done on the training set to avoid data snooping. Otherwise the test error estimation will be biased.

# In[ ]:


features_boxcox = []

for feature in features:
    bc_transformed, _ = boxcox(df[feature]+1)  # shift by 1 to avoid computing log of negative values
    features_boxcox.append(bc_transformed)

features_boxcox = np.column_stack(features_boxcox)
df_bc = pd.DataFrame(data=features_boxcox, columns=features)
df_bc['Type'] = df['Type']


# In[ ]:


df_bc.head()


# In[ ]:


for feature in features:
    fig, ax = plt.subplots(1,2,figsize=(7,3.5))    
    ax[0].hist(df[feature], color='blue', bins=30, alpha=0.3, label='Skew = %s' %(str(round(df[feature].skew(),3))) )
    ax[0].set_title(str(feature))   
    ax[0].legend(loc=0)
    ax[1].hist(df_bc[feature], color='red', bins=30, alpha=0.3, label='Skew = %s' %(str(round(df_bc[feature].skew(),3))) )
    ax[1].set_title(str(feature)+' after a Box-Cox transformation')
    ax[1].legend(loc=0)
    plt.show()


# In[ ]:


# check if skew is closer to zero after a box-cox transform
for feature in features:
    delta = np.abs( df_bc[feature].skew() / df[feature].skew() )
    if delta < 1.0 :
        print('Feature %s is less skewed after a Box-Cox transform' %(feature))
    else:
        print('Feature %s is more skewed after a Box-Cox transform'  %(feature))


# The Box-Cox transform seems to do a good job in reducing the skews of the different distributions of features.  However, it does not lead to the normalization of the feature distributions.  Next, let's explore dimensionality reduction techniques.

# ## 4. Evaluate Algorithms

# ### - Dimensionality reduction

# * **XGBoost**

# In[ ]:


model_importances = XGBClassifier()
start = time()
model_importances.fit(X_train, y_train)
print('Elapsed time to train Random Forests %.3f seconds' %(time()-start))
plot_importance(model_importances)
plt.show()


# It appears that no main features dominate the importance in the XGBoost modeling of the problem. Also, XGBoost seems to take a lot of time to train in the Kaggle kernel; it might be badly configured. For the rest of this notebook, we will only make use of scikit-learn models.

# * **PCA**

# Let's go ahead and perform a PCA on the features to decorrelate the ones that are linearly dependent and then let's plot the cumulative explained variance.

# In[ ]:


pca = PCA(random_state = seed)
pca.fit(X_train)
var_exp = pca.explained_variance_ratio_
cum_var_exp = np.cumsum(var_exp)
plt.figure(figsize=(8,6))
plt.bar(range(1,len(cum_var_exp)+1), var_exp, align= 'center', label= 'individual variance explained',        alpha = 0.7)
plt.step(range(1,len(cum_var_exp)+1), cum_var_exp, where = 'mid' , label= 'cumulative variance explained',         color= 'red')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.xticks(np.arange(1,len(var_exp)+1,1))
plt.legend(loc='center right')
plt.show()

# Cumulative variance explained
for i, sum in enumerate(cum_var_exp):
    print("PC" + str(i+1), "Cumulative variance: %.3f% %" %(cum_var_exp[i]*100))


# It appears that about 99 % of the variance can be explained with the first 5 principal components. However feeding the PCA features to the learning algorithms did not contribute to a better performance. This might be because PCA is a linear method.

# ### - Compare Algorithms

# Now it's time to compare the performance of different machine learning algorithms. We'll use 10-folds cross-validation to assess the performance of each model with the metric being the classification accuracy. Pipelines encompassing a Box-Cox transformation, Standarization  are used in order to avoid data leakage.

# In[ ]:


class Box_Cox(BaseEstimator,TransformerMixin):
    """
    Box-Cox transformation estimator:
    Takes a feature vector X of numerical distributions
    and performs a box-cox transformation to each feature.
    """
    def __init__(self):
        self.lbds = {}
    
    def fit(self,X, *args):        
        features = X.columns.tolist()
        for feature in features:
            # Skip Silicon
            #if feature == 'Si':   continue
            feat_transf, lmbda = boxcox(X[feature]+1)
            self.lbds[feature] = lmbda
        return self
    
    def transform(self,X, *args):
        features = X.columns.tolist()       
        for feature in features:
            # Skip Silicon
            #if feature == 'Si':   continue
            if feature != 'Si':
                X[feature] = X[feature].apply(                lambda x: ((x+1)**(self.lbds[feature]) -1.0)/self.lbds[feature] if self.lbds[feature] != 0                                               else np.log(x+1) )
        return X


# In[ ]:


n_components = 5
pipelines = []

#print(df.shape)
pipelines.append( ('SVC',
                   Pipeline([ 
                               ('BC', Box_Cox()),
                              ('sc', StandardScaler()),
                             #('pca', PCA(n_components = n_components, random_state=seed ) ),
                             ('SVC', SVC(random_state=seed))]) ) )


pipelines.append(('KNN',
                  Pipeline([ ('BC', Box_Cox()),
                              ('sc', StandardScaler()),
                          #  ('pca', PCA(n_components = n_components, random_state=seed ) ),
                            ('KNN', KNeighborsClassifier()) ])))
pipelines.append( ('RF',
                   Pipeline([('BC', Box_Cox()),
                            #   ('sc', StandardScaler()),
                            # ('pca', PCA(n_components = n_components, random_state=seed ) ), 
                             ('RF', RandomForestClassifier(random_state=seed)) ]) ))

pipelines.append( ('GNB',
                   Pipeline([ ('BC', Box_Cox()),
                              ('sc', StandardScaler()),
                            # ('pca', PCA(n_components = n_components, random_state=seed ) ), 
                             ('GNB', GaussianNB()) ]) ))

tree = DecisionTreeClassifier(max_depth=3)
pipelines.append( ('Ada',
                   Pipeline([ ('BC', Box_Cox()),
                             # ('sc', StandardScaler()),
                            # ('pca', PCA(n_components = n_components, random_state=seed ) ), 
                    ('Ada', AdaBoostClassifier(base_estimator=tree,random_state=seed)) ]) ))

pipelines.append( ('ET',
                   Pipeline([('BC', Box_Cox()),
                              #('sc', StandardScaler()),
                            # ('pca', PCA(n_components = n_components, random_state=seed ) ), 
                             ('ET', ExtraTreesClassifier(random_state=seed)) ]) ))
pipelines.append( ('GB',
                   Pipeline([ ('BC', Box_Cox()),
                           #   ('sc', StandardScaler()),
                           #  ('pca', PCA(n_components = n_components, random_state=seed ) ), 
                             ('GB', GradientBoostingClassifier(random_state=seed)) ]) ))

pipelines.append( ('LR',
                   Pipeline([ ('BC', Box_Cox()),
                              ('sc', StandardScaler()),
                         #    ('pca', PCA(n_components = n_components, random_state=seed ) ), 
                             ('LR', LogisticRegression(random_state=seed)) ]) ))

results, names, times  = [], [] , []
num_folds = 10
scoring = 'accuracy'

for name, model in pipelines:
    start = time()
    kfold = StratifiedKFold(n_splits=num_folds, random_state=seed)
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring = scoring,
                                n_jobs=-1) 
    t_elapsed = time() - start
    results.append(cv_results)
    names.append(name)
    times.append(t_elapsed)
    msg = "%s: %f (+/- %f) performed in %f seconds" % (name, 100*cv_results.mean(), 
                                                       100*cv_results.std(), t_elapsed)
    print(msg)

   
fig = plt.figure(figsize=(12,8))    
fig.suptitle("Algorithms comparison")
ax = fig.add_subplot(1,1,1)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()


# 
# **Observation:** The best performances are achieved by SVC, RF, KNN, ET and GB .However, these algorithms also yield a wide distribution. It is worthy to continue our study by tuning these  algorithms. 
# 
#  Gaussian Naive Bayes and Logistic Regression perform badly. This might be due to the fact that the data is not normally distributed as these algorithms perform well when data that is normally distributed.

# ## 5. Algorithm tuning

# ### Tuning the Support vector classifier
# 
# Let's start by tuning the hyperparameters of the SVC Classifier. We will use three kernels for this purpose: 
# 
# * A Radial Basis Function Kernel
# 
# * A Polynomial kernel

# In[ ]:


# Create a pipeline with SVC
pipe_svc = Pipeline([ ('BC', Box_Cox()),
                       ('scl', StandardScaler()), 
                     #('pca', PCA(n_components=n_components, random_state=seed)),
                    ('svc', SVC(random_state=seed) )])

# Set the parameter ranges
gamma_param_range = [0.001, 0.01, 0.1, 1.0, 10.0]
param_range = [1.0,3.0,5.0,7.0,8.0]
degree_range = [4, 6, 8]

# Set the grid parameters
param_grid_svc =  [
    #{'svc__C': param_range,'svc__kernel': ['linear']},   # Linear kernel
    {'svc__C': param_range,'svc__gamma': gamma_param_range,'svc__kernel': ['rbf']}, # radial basis function
    {'svc__C': param_range, 'svc__degree': degree_range, 'svc__kernel':['poly']} #polynomial
    ]
# Use 10 fold CV
kfold = StratifiedKFold(n_splits=num_folds, random_state= seed)
grid_svc = GridSearchCV(pipe_svc, param_grid= param_grid_svc, cv=kfold, scoring=scoring, 
                        n_jobs=-1)

#Fit the pipeline
start = time()
grid_svc = grid_svc.fit(X_train, y_train)
end = time()

print("SVC grid search took %.3f seconds" %(end-start))

# Best score and best parameters
print('-------Best score----------')
print(grid_svc.best_score_ * 100.0)
print('-------Best params----------')
print(grid_svc.best_params_)


# The best support vector estimator achieves a score of 74 %.

# ### Tuning Random Forests
# 
# For random forest, we can tune the number of grown trees (n_estimators), the trees' depth (max_depth), the criterion of splitting (gini or entropy) and so on.... Let's start tuning these.

# In[ ]:


# Create a pipeline with a Random forest classifier
pipe_rfc = Pipeline([ ('BC', Box_Cox()),
                   #   ('scl', StandardScaler()), 
                  #   ('pca', PCA(n_components=n_components, random_state=seed)),
                    ('rfc', RandomForestClassifier(random_state=seed, n_jobs=-1) )])

# Set the grid parameters
param_grid_rfc =  [ {
    'rfc__n_estimators': [100,200,300], # number of estimators
    #'rfc__criterion': ['gini', 'entropy'],   # Splitting criterion
    'rfc__max_features':[0.05 , 0.1], # maximum features used at each split
    'rfc__max_depth': [None, 5], # Max depth of the trees
    'rfc__min_samples_split': [0.005, 0.01, 0.02 ], # mininal samples in leafs
    }]
# Use 10 fold CV
kfold = StratifiedKFold(n_splits=num_folds, random_state= seed)
grid_rfc = GridSearchCV(pipe_rfc, param_grid= param_grid_rfc, cv=kfold, scoring=scoring, 
                      n_jobs=-1)

#Fit the pipeline
start = time()
grid_rfc = grid_rfc.fit(X_train, y_train)
end = time()

print("RFC grid search took %.3f seconds" %(end-start))

# Best score and best parameters
print('-------Best score----------')
print(grid_rfc.best_score_ * 100.0)
print('-------Best params----------')
print(grid_rfc.best_params_)


# # TO BE CONTINUED ....

# In[ ]:


#coding=utf-8
###
###this is my first kaggle code here ,please tell me if I am wrong
###

