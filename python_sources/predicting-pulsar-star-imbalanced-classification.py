#!/usr/bin/env python
# coding: utf-8

# ## Introduction

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


# In[ ]:


# Import related libraries

import matplotlib.pyplot as plt
import seaborn as sns
import os
import gc
import psutil

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, KernelPCA

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score,make_scorer

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,VotingClassifier

from imblearn.pipeline import make_pipeline
from imblearn.under_sampling import OneSidedSelection
from imblearn.under_sampling import NearMiss
from imblearn.under_sampling import EditedNearestNeighbours
from imblearn.under_sampling import TomekLinks
from imblearn.under_sampling import RandomUnderSampler

pd.set_option('display.max_columns', None)

import warnings
warnings.filterwarnings("ignore")

RANDOM_SEED = 101

import collections
from mpl_toolkits import mplot3d


# #### Data ingestion

# In[ ]:


# Input file
main_df = pd.read_csv("/kaggle/input/predicting-a-pulsar-star/pulsar_stars.csv")


# #### Basic Exploration on the Data

# In[ ]:


main_df.shape


# In[ ]:


main_df.head()


# #### Projecting the Class Imbalance

# In[ ]:


main_df["target_class"].value_counts().plot.bar()


# In[ ]:


main_df.describe()


# In[ ]:


main_df[main_df["target_class"] == 0].describe()


# In[ ]:


main_df[main_df["target_class"] == 1].describe()


# In[ ]:


# Check whether there is any missing values
main_df.isnull().sum()


# ## Exloratory Data Analysis

# #### Visualizing high correlations

# In[ ]:


main_df_corr = main_df.iloc[:,:-1].corr()
main_df_corr[np.abs(main_df_corr)<.5] = 0

# Correlation plot
plt.figure(figsize=(15,10))
sns.heatmap(main_df_corr,
            vmin=-1,
            cmap='bone',
            annot=True);


# In[ ]:


# Release memory and garbage collection
del main_df_corr
gc.collect()


# #### Explore the skewness

# In[ ]:


for col in main_df.columns[:-1]:
    fig = plt.figure(figsize = (8,6))
    ax = fig.add_subplot(111)
    ax = sns.kdeplot(main_df[col][(main_df["target_class"] == 0)], color="Red", shade = True)
    ax = sns.kdeplot(main_df[col][(main_df["target_class"] == 1)], color="Blue", shade= True)
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.legend(["Not Pulsar Star","Pulsar Star"],loc="best")
    ax.set_title('Frequency Distribution of {}'.format(col), fontsize = 15)
    print('\n')
    print('\n')


# #### Explore the inter-dependance of each 

# In[ ]:


sns.pairplot(data=main_df,
             palette="husl",
             hue="target_class",
             vars=main_df.columns[:-1])

plt.suptitle("Paiplot for variables",fontsize=18)


# ** There are some clear as well as some overlapping differences between variables in order to identify the target. Lets try to visualize after PCA transformations and see we can have better distinguishable parameters to separate and identify the targets. **

# ## Data Tranformations

# #### Linear PCA

# In[ ]:


# Create a Pipeline
estimators_pca = []
estimators_pca.append(('Scaler',StandardScaler()))
estimators_pca.append(('PCA',PCA(n_components=2)))

pca = Pipeline(estimators_pca)


# In[ ]:


# Transform data with PCA
data_pca = pca.fit_transform(main_df.iloc[:,:-1].values)

pca_df = pd.DataFrame(data = data_pca, columns = ['comp 1', 'comp 2'])
pca_df = pd.concat([pca_df, main_df[['target_class']]], axis = 1)


# In[ ]:


# Release memory and Garbage Collection
del data_pca
gc.collect()


# In[ ]:


# Plot Linear PCA with 2 components
fig = plt.figure(figsize = (20,15))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = [0,1]
colors = ['r', 'g']
for target, color in zip(targets,colors):
    indicesToKeep = pca_df['target_class'] == target
    ax.scatter(pca_df.loc[indicesToKeep, 'comp 1'],pca_df.loc[indicesToKeep, 'comp 2'],c = color,s = 50)
ax.legend(targets)
ax.grid()


# ** We still see there is overlapping space. Lets see if this could be resolved with Kernel-PCA with 2 components **

# In[ ]:


estimators_kpca = []
estimators_kpca.append(('Scaler',StandardScaler()))
estimators_kpca.append(('KPCA',KernelPCA(kernel="rbf", n_components=2)))

kpca = Pipeline(estimators_kpca)

data_kpca = kpca.fit_transform(main_df.iloc[:,:-1].values)

kpca_df = pd.DataFrame(data = data_kpca, columns = ['comp 1', 'comp 2'])
kpca_df = pd.concat([kpca_df, main_df[['target_class']]], axis = 1)

del data_kpca
gc.collect()


# In[ ]:


fig = plt.figure(figsize = (20,15))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = [0,1]
colors = ['r', 'g']
for target, color in zip(targets,colors):
    indicesToKeep = kpca_df['target_class'] == target
    ax.scatter(kpca_df.loc[indicesToKeep, 'comp 1'],kpca_df.loc[indicesToKeep, 'comp 2'],c = color,s = 50)
ax.legend(targets)
ax.grid()


# ** KernelPCA with "rbf" kernel doesn't yield better separable class boundaries. Lets try with "sigmoid" kernel ** 

# In[ ]:


estimators_kpca = []
estimators_kpca.append(('Scaler',StandardScaler()))
estimators_kpca.append(('KPCA',KernelPCA(kernel="sigmoid", n_components=2)))

kpca = Pipeline(estimators_kpca)

data_kpca = kpca.fit_transform(main_df.iloc[:,:-1].values)

kpca_df = pd.DataFrame(data = data_kpca, columns = ['comp 1', 'comp 2'])
kpca_df = pd.concat([kpca_df, main_df[['target_class']]], axis = 1)

del data_kpca
gc.collect()


# In[ ]:


fig = plt.figure(figsize = (20,15))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = [0,1]
colors = ['r', 'g']
for target, color in zip(targets,colors):
    indicesToKeep = kpca_df['target_class'] == target
    ax.scatter(kpca_df.loc[indicesToKeep, 'comp 1'],kpca_df.loc[indicesToKeep, 'comp 2'],c = color,s = 50)
ax.legend(targets)
ax.grid()


# ** KernelPCA with "sigmoid" kernel using 2 components reveal that there is a separable boundary, as wee see the data points representing "target_class = 1" overlayed on the data points representing "target_class = 0" in the overlapping space. Lets try KernelPCA with "sigmoid" kernel using 3 components and visualize on a 3-dimensional space. **

# In[ ]:


estimators_kpca = []
estimators_kpca.append(('Scaler',StandardScaler()))
estimators_kpca.append(('KPCA',KernelPCA(kernel="sigmoid", n_components=3)))
kpca3 = Pipeline(estimators_kpca)

data_kpca3 = kpca3.fit_transform(main_df.iloc[:,:-1].values)

kpca3_df = pd.DataFrame(data = data_kpca3, columns = ['comp 1', 'comp 2', 'comp 3'])
kpca3_df = pd.concat([kpca3_df, main_df[['target_class']]], axis = 1)


# In[ ]:


del data_kpca3
gc.collect()


# In[ ]:


fig = plt.figure(figsize = (40,25))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Principal Component 1', fontsize = 30)
ax.set_ylabel('Principal Component 2', fontsize = 30)
ax.set_zlabel('Principal Component 3', fontsize = 30)
ax.set_title('3 component Kernel - PCA', fontsize = 35)
ax.tick_params(labelsize=10)
targets = [0,1]
colors = ['r', 'g']
for target, color in zip(targets,colors):
    indicesToKeep = kpca3_df['target_class'] == target
    ax.scatter(kpca3_df.loc[indicesToKeep, 'comp 1'],
               kpca3_df.loc[indicesToKeep, 'comp 2'],
               kpca3_df.loc[indicesToKeep, 'comp 3'],
               c = color,
               s = 50)
ax.legend(targets)
ax.grid()


# ** Now this is a much better representation of our data, therefore we will move ahead with 3 component PCA transformations on the data **

# In[ ]:


# Delete all prior data created for transformations
del pca_df
del kpca_df
gc.collect()


# ## Baselining

# #### Create a Baseline Models

# In[ ]:


# Split the data in train and test for baseline models
X_train,X_test,y_train,y_test = train_test_split(kpca3_df.iloc[:,:-1].values,
                                                 kpca3_df.iloc[:,-1].values,
                                                 test_size=0.25,
                                                 random_state=RANDOM_SEED)


# In[ ]:


# List of models to be used
classification_models = ['LogisticRegression',
                         'SVC',
                         'DecisionTreeClassifier',
                         'RandomForestClassifier',
                         'AdaBoostClassifier']


# In[ ]:


# Metrics to be captured for each model
cm = []
acc = []
prec = []
rec = []
f1 = []
models = []
estimators = []
estimators_us = []


# In[ ]:


# Instantiate every model, fit on training data, make predictions on testing data and capture prediction metrices
for classfication_model in classification_models:
    
    model = eval(classfication_model)()
    
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    
    models.append(classfication_model)
    estimators.append((classfication_model,model))
    cm.append(confusion_matrix(y_test,y_pred))
    acc.append(accuracy_score(y_test,y_pred))
    prec.append(precision_score(y_test,y_pred))
    rec.append(recall_score(y_test,y_pred))
    f1.append(f1_score(y_test,y_pred))


# In[ ]:


model_dict = {"Models":models,
             "CM":cm,
             "Accuracy":acc,
             "Precision":prec,
             "Recall":rec,
             "f1_score":f1}
model_df = pd.DataFrame(model_dict)
model_df.sort_values(by=['f1_score','Recall','Precision','Accuracy'],ascending=False,inplace=True)
model_df


# ** Here we have just used Baseline models on the PCA transformed data and we have the following observations ** 
# - The Accuracy score is high for all of the five models 
# - The Recall and F1-score is suffering for all of the five models

# ## Identifying the problem

# ** From the above observations from baseline models we can conclude: **
# - The learning of the models are getting skewed towards identifying negatives. As a result, we see high accuracy score but low recall and f1-scores.
# - Therefore, this is an Imbalanced Classification. We need to balance the data with respect to the target classes.
# - We will under-sample the majority target class using different methods.

# In[ ]:


# Different Under Sampling methods
undersamplers = ['TomekLinks','RandomUnderSampler','EditedNearestNeighbours',
                 'NearMiss','OneSidedSelection']


# In[ ]:


print("Shape before under-sampling: ",main_df.shape[0])
print("Target spread before under-sampling: ",main_df['target_class'].value_counts())
print('\n')
for undersampler in undersamplers:
    
    us_obj = eval(undersampler)()
    X_res, y_res = us_obj.fit_resample(main_df.iloc[:,:-1].values,
                                       main_df.iloc[:,-1].values)
    print(undersampler," : ")
    print("Shape after under-sampling: ",y_res.shape)
    print("Target spread after under-sampling: ",collections.Counter(y_res))
    print('\n')


# In[ ]:


# Visualizing the undersampled transformed data
for undersampler in undersamplers:
    us_obj = eval(undersampler)()
    if undersampler in ['RandomUnderSampler','NearMiss']:
        X_res, y_res = us_obj.fit_resample(main_df.iloc[:,:-1].values,
                                           main_df.iloc[:,-1].values)
    else:
        X_res, y_res = us_obj.fit_sample(main_df.iloc[:,:-1].values,
                                         main_df.iloc[:,-1].values)
    est_US_kpca = []
    est_US_kpca.append(('Scaler',StandardScaler()))
    est_US_kpca.append(('KPCA',KernelPCA(kernel="sigmoid", n_components=3)))
    kpca3_us = Pipeline(est_US_kpca)

    data_US_kpca3 = kpca3_us.fit_transform(X_res)

    kpca3_US_df = pd.DataFrame(data = data_US_kpca3, columns = ['comp 1', 'comp 2', 'comp 3'])
    kpca3_US_df = pd.concat([kpca3_US_df, 
                             pd.DataFrame(y_res, columns=['target_class'])], 
                            axis = 1)
    
    # Plot the Graphs
    fig = plt.figure(figsize = (40,25))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Principal Component 1', fontsize = 30)
    ax.set_ylabel('Principal Component 2', fontsize = 30)
    ax.set_zlabel('Principal Component 3', fontsize = 30)
    ax.set_title('3 component Kernel-PCA with Undersampler : {}'.format(undersampler), 
                 fontsize = 35)
    targets = [0,1]
    colors = ['r', 'g']
    for target, color in zip(targets,colors):
        indicesToKeep = kpca3_US_df['target_class'] == target
        ax.scatter(kpca3_US_df.loc[indicesToKeep, 'comp 1'],
                   kpca3_US_df.loc[indicesToKeep, 'comp 2'],
                   kpca3_US_df.loc[indicesToKeep, 'comp 3'],
                   c = color,
                   s = 50)
    ax.legend(targets)
    ax.grid()
    
    del X_res
    del y_res
    del kpca3_US_df
    del data_US_kpca3
    gc.collect()
    
    print('\n')
    print('\n')


# #### Create Baseline models with Under-Sampled data

# In[ ]:


model_sampler = [(model,sampler) for model in classification_models for sampler in undersamplers]


# In[ ]:


for classification_model,undersampler in model_sampler:
    
    us_obj = eval(undersampler)()
    X_res, y_res = us_obj.fit_resample(main_df.iloc[:,:-1].values,
                                       main_df.iloc[:,-1].values)
    
    kpca3_us = Pipeline([('Scaler',StandardScaler()),
                         ('KPCA',KernelPCA(kernel="sigmoid", n_components=3))])

    data_US_kpca3 = kpca3_us.fit_transform(X_res)
    X_train,X_test,y_train,y_test = train_test_split(data_US_kpca3,
                                                     y_res,
                                                     test_size=0.25,
                                                     random_state=RANDOM_SEED)
    model = eval(classification_model)()
    
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    
    model_name = classification_model + "_" + undersampler
    models.append(model_name)
    estimators_us.append((model_name,model))
    cm.append(confusion_matrix(y_test,y_pred))
    acc.append(accuracy_score(y_test,y_pred))
    prec.append(precision_score(y_test,y_pred))
    rec.append(recall_score(y_test,y_pred))
    f1.append(f1_score(y_test,y_pred))
    
    del X_res
    del y_res
    del data_US_kpca3
    gc.collect()


# In[ ]:


model_dict = {"Models":models,
             "CM":cm,
             "Accuracy":acc,
             "Precision":prec,
             "Recall":rec,
             "f1_score":f1}
model_df = pd.DataFrame(model_dict)
model_df.sort_values(by=['f1_score','Recall','Precision','Accuracy'],ascending=False,inplace=True)
model_df.head(10)


# ** Lets pick the top five performing models and create a stacked ensemble **

# In[ ]:


best_models = model_df.head(5)["Models"].tolist()

best_estimators = []
for model,est in estimators_us:
    if model in best_models:
        best_estimators.append((model,est))


# ** Create a Stacked Ensemble **
# ##### Note - We will train the stacked ensemble without undersampling the data

# In[ ]:


vc = VotingClassifier(best_estimators)
vc.fit(X_train,y_train)
y_pred = vc.predict(X_test)
    
models.append(type(vc).__name__ + "Best_Under_Sampled_Baseline")

cm.append(confusion_matrix(y_test,y_pred))
acc.append(accuracy_score(y_test,y_pred))
prec.append(precision_score(y_test,y_pred))
rec.append(recall_score(y_test,y_pred))
f1.append(f1_score(y_test,y_pred))


# In[ ]:


model_dict = {"Models":models,
             "CM":cm,
             "Accuracy":acc,
             "Precision":prec,
             "Recall":rec,
             "f1_score":f1}
model_df = pd.DataFrame(model_dict)
model_df.sort_values(by=['f1_score','Recall','Precision','Accuracy'],ascending=False,inplace=True)
model_df.head(10)


# ## Cross-Validate the stacked ensemble baseline

# In[ ]:


# Define f1-metric function
def f1_metric(y_test,y_pred):
    return f1_score(y_test,y_pred)


# In[ ]:


# Define f1 scorer
f1_scorer = make_scorer(f1_metric,greater_is_better=True)


# In[ ]:


# Get cross-validated f1-scores
cv_scores = cross_val_score(vc,
                            X_train,
                            y_train,
                            scoring=f1_scorer,
                            cv=20,
                            n_jobs=-1)


# In[ ]:


print("F1-score statistics: ")
print("Mean: ",cv_scores.mean())
print("Standard Deviation: ",cv_scores.std())
print("Max value: ",cv_scores.max())
print("Min value: ",cv_scores.min())


# ## Conclusion

# - We get much better results with re-sampling in case of Imbalanced Classification
# - We can try over-sampling techniques as well
