#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries:

get_ipython().run_line_magic('reset', '-f')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# For measuring time elapsed
from time import time

# Working with imbalanced data
from imblearn.over_sampling import SMOTE, ADASYN

# Processing data
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler as ss

from sklearn.ensemble import ExtraTreesClassifier


# Model building
import h2o
from h2o.estimators.deeplearning import H2ODeepLearningEstimator

# for ROC graphs & metrics, import scikitplot as skplt
#import scikitplot as skplt
#import sklearn metrics to determine model characteristcs
from sklearn.metrics import confusion_matrix
from sklearn.metrics import average_precision_score
import sklearn.metrics as metrics
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.metrics import auc, roc_curve


# In[ ]:


# Change ipython options to display all data columns
pd.options.display.max_columns = 300


# In[ ]:


# Read data
# os.chdir("/Users/dileeprayagiri/Documents/ML Course")
# ccf = pd.read_csv("creditcard.csv.zip")

ccf = pd.read_csv("../input/creditcard.csv")


# In[ ]:


# Explore data
ccf.head(3)
ccf.info()


# In[ ]:


# Examine distribution of continuous variables
ccf.describe()


# In[ ]:


# boxplot for Time and Amount vs Class:
ccf.boxplot(column = ['Time'], by = ['Class'])
ccf.boxplot(column = ['Amount'], by = ['Class'])


# In[ ]:


ccf.shape


# In[ ]:


ccf.columns.values


# In[ ]:


ccf.dtypes.value_counts()


# In[ ]:


# Check for Null values:
(ccf.isnull()).apply(sum, axis=0)


# In[ ]:


# Summary of target feature
ccf['Class'].value_counts()


# In[ ]:


# % of data with valid/fraud transaction
ccf['Class'].value_counts()[1]/ccf.shape[0]


# In[ ]:


# Separation into target/predictors
y = ccf.iloc[:,30]
X = ccf.iloc[:,0:30]
X.head(3)


# In[ ]:


# shape of X
X.shape


# In[ ]:


# Shape of y
y.shape


# In[ ]:


# Scale all numerical features in X  using sklearn's StandardScaler class
scale = ss()
X_trans = scale.fit_transform(X)
X_trans.shape


# In[ ]:


# Split data into train/test
# train-test split. startify on 'y' variable, Default is None.
X_train, X_test, y_train, y_test =   train_test_split(X_trans,
                                                      y,
                                                      test_size = 0.3,
                                                      stratify = y
                                                      )


# In[ ]:


X_train.shape 


# In[ ]:


y_train.shape


# In[ ]:


####Data Modelling########

# Oversample X_train data with SMOTE


sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_sample(X_train, y_train)
type(X_res)


# In[ ]:


# Check if the data is now balanced
X_res.shape                   
np.sum(y_res)/len(y_res)      
np.unique(y_res, return_counts = True)


# In[ ]:


# Data modelling on balanced dataset using Extra Tree classifier

et = ExtraTreesClassifier(n_estimators=100)
et1 = et.fit(X_res,y_res)
y_pred_et = et1.predict(X_test)
y_pred_et


# In[ ]:


# Prediction Probablity for the ET Model
y_pred_et_prob = et1.predict_proba(X_test)
y_pred_et_prob


# In[ ]:


#Accuracy Score
accuracy_score(y_test,y_pred_et)


# In[ ]:


#Compute & Print the confusion Matrix
confusion_matrix(y_test,y_pred_et)


# In[ ]:


#Precision, Recall and F_Score calculation
p_et,r_et,f_et,_ = precision_recall_fscore_support(y_test,y_pred_et)


# In[ ]:


#Print p,r & f-score
f"Precision: {p_et},Recall: {r_et}, F-Score: {f_et}"


# In[ ]:


# fpr and tpr computation
fpr_et, tpr_et, thresholds = roc_curve(y_test,
                                 y_pred_et_prob[: , 1],
                                 pos_label= 1
                                 )


# In[ ]:


#Area Under the curve
auc(fpr_et,tpr_et)


# In[ ]:


# Plotting Graph
fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111)
# connecting diagonals
ax.plot([0, 1], [0, 1], ls="--")
# Creating Labels for Graph
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title('ROC curve for ET')
# Setting graph limits
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.0])

ax.plot(fpr_et, tpr_et, label = 'Extra Trees Classifier')
ax.legend(loc="lower right")
plt.show()


# In[ ]:


#Balancing the Data using ADASYN and use H2O Deeplearning estimator

# Oversample X_train data with ADASYN
ad = ADASYN()
X_res1, y_res1 = ad.fit_sample(X_train, y_train)

type(X_res1)


# In[ ]:


# Checking if the data is balanced after ADASYN
X_res1.shape                   
np.sum(y_res1)/len(y_res1)      
np.unique(y_res1, return_counts = True)


# In[ ]:


X_res1.shape


# In[ ]:


y_res1.shape


# In[ ]:


# Transform y_res into 2D array to allow stacking
y_res1 = y_res1.reshape(y_res1.size, 1)
y_res1.shape


# In[ ]:


# Horizontal stacking
X = np.hstack((X_res1,y_res1))
X.shape


# In[ ]:


# Start h2o
h2o.init()


# In[ ]:


# Transform X to h2o dataframe
df = h2o.H2OFrame(X)
len(df.columns) 
df.shape


# In[ ]:


df.columns


# In[ ]:


# Get list of predictor column names and target column names

X_columns = df.columns[0:30]   
X_columns 


# In[ ]:


y_columns = df.columns[30]
y_columns


# In[ ]:


# Make Target column as factor, as required by h20
df['C31'] = df['C31'].asfactor()


# In[ ]:


# Build a deeplearning model on balanced data using H2o Estimator

dl_model = H2ODeepLearningEstimator(epochs=1000,
                                    distribution = 'bernoulli', 
                                    missing_values_handling = "MeanImputation",
                                    variable_importances=True,
                                    nfolds = 2,
                                    fold_assignment = "Stratified",
                                    keep_cross_validation_predictions = True,
                                    balance_classes=False,
                                    standardize = True, 
                                    activation = 'RectifierWithDropout',
                                    hidden = [100,100], 
                                    stopping_metric = 'logloss',
                                    loss = 'CrossEntropy')


# In[ ]:


# Train our model
start = time()
dl_model.train(X_columns,
               y_columns,
               training_frame = df)

end = time()
(end - start)/60


# In[ ]:


# Get model summary
type(dl_model)
print(dl_model)
dl_model.cross_validation_holdout_predictions()
dl_model.varimp()


# In[ ]:


##### Making predictions on X_test ######
# Checking the class distibution in unbalanced test data
np.unique(
         y_test,
         return_counts = True) 

# Check the shapes of X_test and y_test

# Check the shape of X_test
X_test.shape


# In[ ]:


# Check the shape of y_test

y_test.shape


# In[ ]:


# y_test is 1-D array, so need to reshape into 2-D array
# to be able to stack alongside X_test
y_test = y_test.ravel()
y_test = y_test.reshape(len(y_test), 1)
y_test.shape


# In[ ]:


# Horizontally stack X-test and y_test
X_test = np.hstack((X_test,y_test)) 
X_test.shape


# In[ ]:


# Transform X_test to h2o dataframe
X_test = h2o.H2OFrame(X_test)


# In[ ]:


# convert into a factor, as required by H2O
X_test['C31'] = X_test['C31'].asfactor()


# In[ ]:


# Make prediction on X_test
result = dl_model.predict(X_test[: , 0:30])
result.shape


# In[ ]:


result.as_data_frame().head()


# In[ ]:


# Convert H2O frame back to pandas dataframe
xe = X_test['C31'].as_data_frame()
xe['result'] = result[0].as_data_frame()
xe.head()


# In[ ]:


xe.columns


# In[ ]:


# So actual target vs predicted
out = (xe['result'] == xe['C31'])
np.sum(out)/out.size


# In[ ]:


# Create confusion matrix

f  = confusion_matrix( xe['C31'], xe['result'] )
f


# In[ ]:


# Flatten confusion matrix
tn,fp,fn,tp = f.ravel()
tn,fp,fn,tp


# In[ ]:


# Evaluate precision/recall

precision = tp/(tp+fp)
precision 
recall = tp/(tp + fn)
recall  
f"Precision: {precision}, Recall: {recall}"


# In[ ]:


# Calculate the fpr and tpr for
# all thresholds of the classification

pred_probability = result["p1"].as_data_frame()


# In[ ]:


# Get fpr, tpr for various thresholds
fpr, tpr, threshold = metrics.roc_curve(xe['C31'],
                                        pred_probability,
                                        pos_label = 1
                                        )


# In[ ]:


# Plotting Graph
fig = plt.figure(figsize=(12,10))
ax1 = fig.add_subplot(111)
# connecting diagonals
ax1.plot([0, 1], [0, 1], ls="--")
# Creating Labels for Graph
ax1.set_xlabel('False Positive Rate')
ax1.set_ylabel('True Positive Rate')
ax1.set_title('ROC curve for H2O DL Estimator')
# Setting graph limits
ax1.set_xlim([0.0, 1.0])
ax1.set_ylim([0.0, 1.0])

ax1.plot(fpr, tpr, label = 'H2O Deeplearning Estimator')
ax1.legend(loc="lower right")
plt.show()


# In[ ]:


# This is the AUC
auc = np.trapz(tpr,fpr)
auc


# In[ ]:


# Based on the AUC results, we can see that Model ExtraTreeClassifier with SMOTE balancing
# resulted in a better performance compared to H2O Deep learning Model with ASYDN balancing
#for the given Dataset


# In[ ]:


#  feature importance
var_df = pd.DataFrame(dl_model.varimp(),
             columns=["Variable", "Relative Importance", "Scaled Importance", "Percentage"])
var_df.head(10)


# In[ ]:




