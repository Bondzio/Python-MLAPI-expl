#!/usr/bin/env python
# coding: utf-8

# # CONTENTS
# * [Imports](#imports)
# * [Functions Definition](#functions_definition)
# * [Exploratory Data Analysis](#eda)
# * [K-Fold Cross Validation using Balanced DataSet](#kfold_cv_baldata)

# ## Imports <a id='imports'></a>

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math

import matplotlib.pyplot as plt
import seaborn as sns

import xgboost as xgb
import shap

from numpy import interp
from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, roc_auc_score, auc, classification_report, precision_recall_curve
from sklearn.impute import SimpleImputer
from termcolor import colored

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from statsmodels.stats.contingency_tables import mcnemar

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ## Functions definition <a id='functions_definition'></a>

# In[ ]:


# Function to plot a histogram that shows the number of NaN values for each column.
def plot_hist_nan(df):
    
    nan_df = pd.DataFrame(df.isna().sum().tolist(), df.columns.tolist()).reset_index()
    nan_df.columns = ['column_name', 'total_nan']
    nan_df['nan_perc'] = 100*round(nan_df['total_nan']/len(df),3)
    nan_df = nan_df.sort_values('total_nan', ascending=False)
    
    plt.figure(figsize=(20,15))
    step = 25
    j = 0
    t_plots = math.ceil(len(nan_df) / step)

    fig, axes = plt.subplots(t_plots, 1, figsize=(20,20))

    for i in range(0,len(nan_df), step):
        sns.barplot(x="nan_perc", y="column_name", data=nan_df[i:i+step], ax=axes[j])    
        axes[j].set_ylabel('Columns', fontsize = 15)
        axes[j].set_xlabel('NaN %', fontsize = 15)
        axes[j].set_xticks([0,10,20,30,40,50,60,70,80,90,100], minor=False)
        j = j + 1    
        if j == t_plots:
            break


# In[ ]:


# Function to plot a chart that shows the class distribution.
def plot_class_distribution(df: pd.DataFrame):
    
    values = df.groupby('SARS-Cov-2 exam result')['SARS-Cov-2 exam result'].count()
    n_samples = df.shape[0]
    
    plt.figure(figsize=(10,6))
    labels = ['Negative', 'Positive']
    explode = (0, 0.2) 
    colors = ['#66b3ff','#ff9999']

    plt.pie(values, colors = colors, autopct='%1.1f%%',
        startangle=90, pctdistance=0.85, explode=explode)

    plt.legend(labels,loc=1)

    centre_circle = plt.Circle((0,0),0.20,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)  
    plt.tight_layout()

    fig.text(0.42, 0.5, "{} samples".format(n_samples), style='italic', fontsize=10)
    plt.show()


# In[ ]:


# Function to plot a chart that shows ROC Curve.
def plot_roc_curve(results):
        
    plt.figure(figsize=(10,8))
    mean_fpr = np.linspace(0, 1, 100)
    tprs = []
    i = 0
    
    colors = ['r','b','g']
    
    for idx,result in enumerate(results):
    
        plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', alpha=.8)
        mean_tpr = np.mean(result.tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(result.aucs)
        
        plt.plot(mean_fpr, mean_tpr, color=colors[idx], label=result.model_name + ' (AUC = %0.3f $\pm$ %0.3f)' % (mean_auc, std_auc), lw=2, alpha=.8)
        
        std_tpr = np.std(result.tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        
        if i == 0:
            plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color=colors[idx], alpha=.2)
        else:
            plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color=colors[idx], alpha=.2)
        i = i + 1
    
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='black', label='Chance', alpha=.8)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate', size=12)
    plt.ylabel('True Positive Rate', size=12)
    plt.title('ROC CURVE')
    plt.legend(loc="lower right")    
    plt.show()


# In[ ]:


# Function to plot the confusion matrix.
def plot_confusion_matrix(results):
        
    sns.set(font_scale = 1.6)
    plt.figure(figsize=(12,10))
    threshold = 0.5
    index = 0
        
    for result in results:
                            
        cm = confusion_matrix(result.y_pred, result.y_test)
        
        labels = ['Negative', 'Positive']
        ax = plt.subplot(2, 2, index+1)
        sns.set_palette("PuBuGn_d")
        
        if index == 0 or index == 2:
            show_scale = False
        else:
            show_scale = True
            
        sum_0 =  cm.sum(axis=1)[0]
        sum_1 = cm.sum(axis=1)[1]
        
        cm_aux = np.zeros((2,2))

        cm_aux[0][0] = (cm[1][1]) #/ sum_1
        cm_aux[0][1] = (cm[1][0])
        cm_aux[1][0] = (cm[0][1])
        cm_aux[1][1] = (cm[0][0])
        
        sns.heatmap(cm_aux, annot=True, ax = ax, fmt="", cmap="Blues", cbar=False)
        #sns.heatmap(cm_aux, annot=True, ax = ax, cmap="Blues", cbar=False)
        
        ax.set_title(result.model_name)
        ax.yaxis.set_ticklabels(['Positive', 'Negative'])
        ax.xaxis.set_ticklabels(['Positive', 'Negative'])
        
        if index == 0 or index == 1:
            ax.set_xlabel('');
        else:
            ax.set_xlabel('Predicted labels');
            
        if index == 1 or index == 3:
            ax.set_ylabel(''); 
        else:
            ax.set_ylabel('True labels')
            
        index = index + 1
    
    plt.show()


# In[ ]:


# Function to create a balanced dataset.
def create_balanced_dataset(df: pd.DataFrame, percent):
    # Class count
    count_class_0, count_class_1 = df['SARS-Cov-2 exam result'].value_counts() * percent
    count_class_0 = int(count_class_0)
    count_class_1 = int(count_class_1)

    # Divide by class
    df_class_0 = df[df['SARS-Cov-2 exam result'] == 0]
    df_class_1 = df[df['SARS-Cov-2 exam result'] == 1]
    
    df_class_1 = df_class_1.sample(count_class_1, random_state=1)
    
    df_class_0_under = df_class_0.sample(count_class_1, random_state=1)
    df_balanced = pd.concat([df_class_0_under, df_class_1], axis=0)
    
    return df_balanced


# In[ ]:


def evaluate_model(model, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.DataFrame, y_test: pd.DataFrame):
    """
    Used to evaluate a given model. Just an API wrapper.    
    Returns the fitted model along with the predictions generated for the test set
    """
    model.fit(X_train, y_train)
    y_preds = model.predict(X_test)
    y_preds_proba = model.predict_proba(X_test)
    return model, y_preds, y_preds_proba


# In[ ]:


def generate_performance_stats(y_test, y_pred):    
    target_names = ['Negative', 'Positive'] 
    cm = confusion_matrix(y_test, y_pred)        
    print("Accuracy: {}\n".format(metrics.accuracy_score(y_test,y_pred)))
    print("Confusion Matrix: \n{}\n".format(pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])))
    print("Classification Report: \n{}\n".format(classification_report(y_test, y_pred, target_names=target_names)))


# In[ ]:


# Function to perform K-fold Cross Validation.
def permoform_cv(df: pd.DataFrame, target: pd.DataFrame, models):
        
    results = []
    mean_fpr = np.linspace(0, 1, 100)
    models_predictions = {}

    for model_alias in models:
    
        print("Model: {}\n".format(model_alias))
        tprs = []
        aucs = []
        thresholds = []
        y_preds = []
        y_preds_prob = []
        y_tests = []
        model = models[model_alias]

        i = 0
        kf = KFold(n_splits=n_folds, random_state=13, shuffle=True)
        model_predicted = []
        model_gt = []
    
        for index in kf.split(df):

            print("Fold[{}]\n".format(i+1))

            X_train, X_test, y_train, y_test = df.iloc[index[0]], df.iloc[index[1]], target.iloc[index[0]], target.iloc[index[1]]            
            model_fit, y_pred, y_pred_proba = evaluate_model(model, X_train, X_test, y_train, y_test)
            
            y_pred = y_pred_proba[:,1] > thresh
            y_pred = y_pred.astype(int)  
            model_predicted = np.concatenate((np.array(model_predicted),y_pred))
            model_gt = np.concatenate((np.array(model_gt),y_test))
            
            generate_performance_stats(y_test, y_pred)                    

            # Compute ROC curve and area the curve
            fpr, tpr, threshold = roc_curve(y_test, y_pred_proba[:,1])
            prec, rec, tre = precision_recall_curve(y_test, y_pred_proba[:,1])
            
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            thresholds.append(threshold)
            
            y_preds = np.append(y_preds, y_pred)
            y_preds_prob = np.append(y_preds_prob, y_pred_proba[:,1])
            y_tests = np.append(y_tests, y_test)
            
            i = i + 1
    
        generate_performance_stats(model_gt, model_predicted)

        result = RESULT(model_alias, tprs, aucs, thresholds, y_preds, y_preds_prob, y_tests)
        results.append(result)
        models_predictions[model_alias] = (model_predicted,model_gt)
        print("########################################################\n")
    
    return results, models_predictions


# In[ ]:


class RESULT(object):
    
    def __init__(self, model_name, tprs, aucs, thresholds, y_pred, y_pred_prob, y_test):
        self.model_name = model_name
        self.tprs = tprs
        self.aucs = aucs
        self.thresholds = thresholds
        self.y_pred = y_pred
        self.y_pred_prob = y_pred_prob
        self.y_test = y_test


# In[ ]:


# Importing raw dataset
df_all = pd.read_excel('/kaggle/input/covid19/dataset.xlsx')


# In[ ]:


print("The dataset has {} many rows and {} columns".format(df_all.shape[0], df_all.shape[1]))


# ## Exploratory Data Analysis <a id='eda'></a>

# In[ ]:


# Look at the data
df_all.head(5)


# It seems there are several features with NaN values. It will be checked the amount of missing data in each column.

# In[ ]:


plot_hist_nan(df_all)


# The histogram above shows that only the target features e "Patient age quantile" feature do not have NaN values. Therefore, we can observe that 94% of the features have more than 70% of the missing values. It will be maintaned the features with less than 90% of the missing values.

# In[ ]:


df = df_all.loc[:, df_all.isnull().mean() <= .9]


# ### Class distribution for the SARS-Cov-2 exam result

# In[ ]:


# Class distribution for the SARS-Cov-2 exam result
plot_class_distribution(df)


# For task 1, the dataset is unbalanced, with 90.1% of negative cases and 9.9% of positive cases. 

# ## K-Fold Cross Validation using Balanced Dataset<a id='kfold_cv_baldata'></a>

# In[ ]:


# Drop the target columns related to task 2
cols_task2 = ['Patient addmited to regular ward (1=yes, 0=no)', 'Patient addmited to semi-intensive unit (1=yes, 0=no)',
              'Patient addmited to intensive care unit (1=yes, 0=no)']

df = df.drop(cols_task2, axis = 1)


# In[ ]:


# Let's check the data type of predictive features.
df.info(verbose=True)


# In[ ]:


# The new dataset will only have numerical features. The target feature is converted to 0 or 1.
df_numeric = df.copy()
df_numeric['SARS-Cov-2 exam result'][df_numeric['SARS-Cov-2 exam result'] == 'negative'] = 0
df_numeric['SARS-Cov-2 exam result'][df_numeric['SARS-Cov-2 exam result'] == 'positive'] = 1
df_numeric['SARS-Cov-2 exam result'] = df_numeric['SARS-Cov-2 exam result'].astype(str).astype(int)


# ### Get the Balanced Dataset
# The *percent* variable defines the percentual of the minority class samples (positive) will be used to create a balanced dataset. The remaining samples will be used afterwards like the unbalanced dataset. 

# In[ ]:


percent = 0.8
df_balanced = create_balanced_dataset(df_numeric, percent)
print("The balanced dataset has {} many rows and {} columns".format(df_balanced.shape[0], df_balanced.shape[1]))


# ### Get the Unbalanced Dataset - Test

# In[ ]:


df_test = df[(~df['Patient ID'].isin(df_balanced['Patient ID']))]
print("The unbalanced dataset (test) has {} many rows and {} columns".format(df_test.shape[0], df_test.shape[1]))


# In[ ]:


# Predictive models
models = {
    'XGBoost': XGBClassifier(),
    'RF': RandomForestClassifier(n_estimators=100,criterion='gini'),
    'Logistic': LogisticRegression(),
}


# Several variable are the "object" type and mostlikely have a categorical domain. As the first experiment, it will be used only numerical features.

# In[ ]:


df_balanced_num = df_balanced.select_dtypes(include=['float64', 'int64'])


# Most of the predictive models to be created do not handle missing values. Therefore, it will be used the simple inputation method.

# In[ ]:


cols = df_balanced_num.columns
df_balanced_num[cols] = df_balanced_num.filter(cols).fillna(df_balanced_num.mode().iloc[0])


# ### Perform k-fold cross validation

# In[ ]:


# Getting the target column and drop 'Patient ID' column
y_train = df_balanced_num['SARS-Cov-2 exam result']
df_balanced_num = df_balanced_num.drop(['SARS-Cov-2 exam result'], axis = 1)


# In[ ]:


#K-Fold parameters
thresh = 0.5
k_fold_seed = 13
n_folds = 10
results, models_predictions = permoform_cv(df_balanced_num, y_train, models)


# In[ ]:


# Performance stats for models
for result in results:
    print("Model: {}\n".format(result.model_name))
    generate_performance_stats(result.y_pred, result.y_test)
    print("###########################################################\n")


# ### ROC curve plot

# In[ ]:


plot_roc_curve(results)


# ### Confusion Matrix plot

# In[ ]:


plot_confusion_matrix(results)


# The charts and metric values shows that the Xgboost and Random Forest models presents a better predictive power. There are several detais to be consider to improove the results, like:
# * include non-numerical features
# * Use other inputation methods
# * Ensemble models
# * ...
