#!/usr/bin/env python
# coding: utf-8

# # Kernel Summary
# 
# Basically there is no feature engineering to be done as the features are given as PCA of the original feature. The only important thing to note here is that we need to sample the data to have equal number of both the classes.
# 
# * Working with skewed datasets with disproportionate classes
# * Different types of sampling undersampling, oversampling, SMOTE
# * Confusion Matrix and applications - plotting the matrix using imshow
# * Metrics to use : Recall, TPR, FPR, AOC Curve
# * Precision Vs. Recall Trade-off
# * Training on disproportionate datasets and doing KFold for recall
# 

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


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


data = pd.read_csv("../input/creditcard.csv")
data.head()


# In[ ]:


sns.countplot(x='Class', data=data)


# Since the data is highly disproportionate, even just simply predicting the score would give us a high accuracy score. This can be solved by changing the metric of performance
# * Confusion Matrix
# * F1 Score 
# * ROC Curve
# * Kappa
# 
# Resampling data
# * Processes data to have 50-50 ratio
# * Undersampling 
# * Oversampling
# 

# # Setting input and target variable with resampling

# In[ ]:


# Standardizing the amount column
from sklearn.preprocessing import StandardScaler

data['normAmount'] = StandardScaler().fit_transform(data['Amount'].values.reshape(-1, 1))

data = data.drop(['Time', 'Amount'], axis=1)
data.head()


# # Undersampling the data

# In[ ]:


import random

X = data.iloc[:, data.columns != 'Class']
y = data.iloc[:, data.columns == 'Class']

fraud_instances = data[data['Class']==1]['Class'].count()
sampled_non_fraud_data = data[data.Class == 0].iloc[random.sample(list(data[data.Class == 0].index), fraud_instances)]


# In[ ]:


fraud_data = data[data.Class == 1]
sampled_data = pd.concat([sampled_non_fraud_data, fraud_data])

sampled_data = sampled_data.sample(frac=1)
X_sampled = sampled_data.iloc[:, sampled_data.columns != 'Class']
y_sampled = sampled_data.iloc[:, sampled_data.columns == 'Class']

# Showing ratio
print("Percentage of normal transactions: ", len(sampled_data[sampled_data.Class == 0])/len(sampled_data))
print("Percentage of fraud transactions: ", len(sampled_data[sampled_data.Class == 1])/len(sampled_data))
print("Total number of transactions in resampled data: ", len(sampled_data))


# # Splitting data into train and test set.

# In[ ]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3, random_state = 0)

print("Number transactions train dataset: ", len(X_train))
print("Number transactions test dataset: ", len(X_test))
print("Total number of transactions: ", len(X_train)+len(X_test))

# Undersampled dataset
X_train_undersample, X_test_undersample, y_train_undersample, y_test_undersample = train_test_split(X_sampled
                                                                                                   ,y_sampled
                                                                                                   ,test_size = 0.3
                                                                                                   ,random_state = 0)
print("")
print("Number transactions train dataset: ", len(X_train_undersample))
print("Number transactions test dataset: ", len(X_test_undersample))
print("Total number of transactions: ", len(X_train_undersample)+len(X_test_undersample))


# # Logistic Regression with KFold Cross Validation
# 

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import confusion_matrix,precision_recall_curve,auc,roc_auc_score,roc_curve,recall_score,classification_report, precision_score 


# In[ ]:


def printing_Kfold_scores(x_train_data,y_train_data):
    fold = KFold(n_splits=5,shuffle=False) 

    # Different C parameters
    c_param_range = [0.01,0.1,1,10,100]

    results_table = pd.DataFrame(index = range(len(c_param_range),2), columns = ['C_parameter','Mean recall score'])
    results_table['C_parameter'] = c_param_range
    j = 0
    for c_param in c_param_range:
        print('-------------------------------------------')
        print('C parameter: ', c_param)
        print('-------------------------------------------')
        print('')

        recall_accs = []
        for iteration, (train_indices, val_indices) in enumerate(fold.split(y_train_data)):
            
            # Train the logistic regression with multiple c parameter
            lr = LogisticRegression(C=c_param, penalty='l1')
            lr.fit(x_train_data.iloc[train_indices, :], y_train_data.iloc[train_indices, :])
            
            y_predict_undersample = lr.predict(x_train_data.iloc[val_indices])
            
            recall_acc = recall_score(y_train_data.iloc[val_indices], y_predict_undersample)
            recall_accs.append(recall_acc)
            print('Iteration ', iteration,': recall score = ', recall_acc)
        results_table.loc[j, 'Mean recall score'] = np.mean(recall_accs)
        j += 1
        print('')
        print('Mean recall score ', np.mean(recall_accs))
        print('')
    return results_table
        


# In[ ]:


param_df = printing_Kfold_scores(X_train_undersample,y_train_undersample)


# In[ ]:


param_df


# In[ ]:


optimum_c = param_df[param_df['Mean recall score'] == param_df['Mean recall score'].max()].C_parameter


# In[ ]:


optimum_c


# In[ ]:


import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        #print("Normalized confusion matrix")
    else:
        1#print('Confusion matrix, without normalization')

    #print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# Use the best param to predict the values on the test set

# In[ ]:


lr = LogisticRegression(C=float(optimum_c), penalty='l1')
lr.fit(X_train_undersample, y_train_undersample)

y_pred_undersample = lr.predict(X_test_undersample)

cnf = confusion_matrix(y_test_undersample, y_pred_undersample)
np.printoptions(precision=2)
print("Recall metric in the testing dataset: ", cnf[1,1]/(cnf[1,0]+cnf[1,1]))


# In[ ]:


# Plot non-normalized confusion matrix
class_names = [0,1]
plt.figure()
plot_confusion_matrix(cnf
                      , classes=class_names
                      , title='Confusion matrix')
plt.show()


# We get a 93% recall
# on the undersampled dataset.

# # Making Predictions on the whole of Test Dataset.

# In[ ]:


lr = LogisticRegression(C=float(optimum_c))
lr.fit(X_train_undersample, y_train_undersample)
preds_on_whole = lr.predict(X_test)

cnf = confusion_matrix(y_test, preds_on_whole)
print("Recall: {}".format(cnf[1][1]/(cnf[1][1]+cnf[1][0])))


# In[ ]:


class_names = [0, 1]
plt.figure()
plot_confusion_matrix(cnf, class_names, title='Confusion Matrix')


# # Whole dataset

# In[ ]:


preds_on_whole = lr.predict(X)

cnf = confusion_matrix(y, preds_on_whole)
print("Recall: {}".format(cnf[1][1]/(cnf[1][1]+cnf[1][0])))


# In[ ]:


class_names = [0, 1]
plt.figure()
plot_confusion_matrix(cnf, class_names, title='Confusion Matrix')


# # ROC Curve

# In[ ]:


lr = LogisticRegression(C=float(optimum_c), penalty='l1')
y_pred_undersample_score = lr.fit(X_train_undersample, y_train_undersample).decision_function(X_test_undersample)
fpr, tpr, thresholds = roc_curve(y_test_undersample.values, y_pred_undersample_score)
roc_auc = auc(fpr, tpr)


# * TPR = True positive rate: That is the recall value. The number of positive classification divided by the true number of postive classification. In this scenario it would be the number of correctly classified fraud cases by the sum of correctly classified fraud cases and the incorrectly labeled fraud cases
# * FPR = False Postive rate: The number of not fraud by the sum of the number of not fraud and the incorrectly classified not fraud.
# * AUC = is the area under the curve of TPR vs FPR

# In[ ]:


plt.title("TPR vs FPR of the data")
plt.plot(fpr, tpr, 'b',label='AUC = %0.2f'% roc_auc)
plt.legend(loc='lower right')
plt.plot([0,1],[0,1],'r--')
plt.xlim([-0.1,1.0])
plt.ylim([-0.1,1.01])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


# The metric is plotted by changin the thresholds of the probability predictions. We then plot the values TPR vs FPR. We can see that as FPR increases we keep on classifying non-frauds as frauds but our true-positive rates keep on increasing. We need to do make a trade-off of how much misclassifying of non-fraud as fraud we can sacrifice to increase the recall.

# # Logistic Regression Classifier on the Skewed Data
# 
# We'll do the KFold validation on the entire dataset and see what all inconsistencies creep up.

# In[ ]:


best_c = printing_Kfold_scores(X_train,y_train)


# In[ ]:


lr = LogisticRegression(C = best_c.iloc[0, 0], penalty = 'l1')
lr.fit(X_train,y_train)
y_pred_undersample = lr.predict(X_test)

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test,y_pred_undersample)
np.set_printoptions(precision=2)

print("Recall metric in the testing dataset: ", cnf_matrix[1,1]/(cnf_matrix[1,0]+cnf_matrix[1,1]))

# Plot non-normalized confusion matrix
class_names = [0,1]
plt.figure()
plot_confusion_matrix(cnf_matrix
                      , classes=class_names
                      , title='Confusion matrix')
plt.show()


# # Changing Classification Threshold
# If we use predict_prob() instead of the predict() method, we'll get the probability of the particular classification. If we use a threshold to control the probability, we can control the precision and the recall.

# In[ ]:


lr = LogisticRegression(C=0.01, penalty='l1')
lr.fit(X_train_undersample, y_train_undersample)

pred_prob = lr.predict_proba(X_test_undersample)

thresholds = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

plt.figure(figsize=(10, 10))

j=1
for i in thresholds:
    y_test_prediction_recall = pred_prob[:, 1] > i
    plt.subplot(3, 3, j)
    
    j += 1
    
    cnf = confusion_matrix(y_test_undersample, y_test_prediction_recall)
    np.set_printoptions(precision=2)

    print("Recall metric in the testing dataset: ", cnf[1,1]/(cnf[1,0]+cnf[1,1]))

    # Plot non-normalized confusion matrix
    class_names = [0,1]
    plot_confusion_matrix(cnf
                          , classes=class_names
                          , title='Threshold >= %s'%i)


# In[ ]:


from itertools import cycle

lr = LogisticRegression(C = 0.01, penalty = 'l1')
lr.fit(X_train_undersample,y_train_undersample.values.ravel())
y_pred_undersample_proba = lr.predict_proba(X_test_undersample.values)

thresholds = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
colors = cycle(['navy', 'turquoise', 'darkorange', 'cornflowerblue', 'teal', 'red', 'yellow', 'green', 'blue','black'])

plt.figure(figsize=(5,5))

for i,color in zip(thresholds,colors):
    y_test_predictions_prob = y_pred_undersample_proba[:,1] > i
    
    precision, recall, thresholds = precision_recall_curve(y_test_undersample,y_test_predictions_prob)
    print(precision, recall, thresholds)
    
    # Plot Precision-Recall curve
    plt.plot(recall, precision, color=color,
                 label='Threshold: %s'%i)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall example')
    plt.legend(loc="lower left")


# # SMOTE on the Imbalanced Data

# In[ ]:


print("X Train Shape : {}".format(X_train.shape))
print("y Train Shape : {}".format(y_train.shape))

print("X Test Shape : {}".format(X_test.shape))
print("Y Test Shape : {}".format(y_test.shape))


# In[ ]:


from collections import Counter

from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=42)
X_resample, y_resample = sm.fit_resample(X_train, y_train)

print("Y Size: {}".format(Counter(y_resample)))
print("X Size: {}".format(X_resample.shape))


# In[ ]:


lr = LogisticRegression(C=0.01, penalty='l1')

lr.fit(X_resample, y_resample)
predictions = lr.predict(X_test)

cnf = confusion_matrix(y_test, predictions)

plot_confusion_matrix(cnf, [0, 1])


# In[ ]:


print("Recall: {}".format(recall_score(y_test, predictions)))
print("Precision: {}".format(precision_score(y_test, predictions)))


# # Grid Searching for Best Params (Logistic Regression)

# In[ ]:


from sklearn.model_selection import GridSearchCV


# In[ ]:


params = {
          'C': np.linspace(.01, 10),
          'penalty': ['l1', 'l2']
         }

lr = LogisticRegression()
clf = GridSearchCV(lr, params, cv=5, verbose=5, n_jobs=3)
clf.fit(X_sampled, y_sampled)


# In[ ]:


clf.best_params_


# In[ ]:


lr = LogisticRegression(C=2, penalty='l1')

lr.fit(X_resample, y_resample)
predictions = lr.predict(X_test)

cnf = confusion_matrix(y_test, predictions)

plot_confusion_matrix(cnf, [0, 1])

print("Recall: {}".format(recall_score(y_test, predictions)))
print("Precision: {}".format(precision_score(y_test, predictions)))


# # Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


rf = RandomForestClassifier()

param_grid = { 
    'n_estimators': [200, 500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,5,6,7,8],
    'criterion' :['gini', 'entropy']
}

clf = GridSearchCV(rf, param_grid, cv=5, verbose=5, n_jobs=10)
clf.fit(X_sampled, y_sampled)


# In[ ]:


optimum_params = dict(clf.best_params_)


# In[ ]:


lr = RandomForestClassifier(criterion= 'entropy',max_depth= 7,max_features='auto',n_estimators= 200)

lr.fit(X_sampled, y_sampled)
predictions = lr.predict(X_test)

cnf = confusion_matrix(y_test, predictions)

plot_confusion_matrix(cnf, [0, 1])

print("Recall: {}".format(recall_score(y_test, predictions)))
print("Precision: {}".format(precision_score(y_test, predictions)))

