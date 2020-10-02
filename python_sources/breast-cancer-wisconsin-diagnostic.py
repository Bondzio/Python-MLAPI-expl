#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing the required packages
import warnings
warnings.filterwarnings('ignore')
import sys
import os
import time

import numpy as np
import pandas as pd

import seaborn as sns
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Importing the CSV file
b_cancer = pd.read_csv('../input/data.csv')


# In[ ]:


# Checking the number of rows and columns
b_cancer.shape


# In[ ]:


# Checking the table information
b_cancer.info()


# In[ ]:


# Checking the values for different quantiles
b_cancer.describe()


# In[ ]:


# Checking the column present
b_cancer.columns


# In[ ]:


# Checking the random data
b_cancer.head()
b_cancer.tail()


# In[ ]:


# Dropping the upwanted columns
#loans_df.dropna(axis=1,how='all')
b_cancer = b_cancer.drop(['id','Unnamed: 32'],axis = 1)
#b_cancer.head()


# In[ ]:


# def remove_outliers(df):
#     df_new = []
#     for i in df.columns:
#         Q1 = pd.DataFrame(df[i]).quantile(0.25)
#         Q3 = pd.DataFrame(df[i]).quantile(0.75)
#         IQR = Q3 - Q1
#         df_new = pd.DataFrame(df[(pd.DataFrame(df[i]) >= Q1 - 1.5*IQR) & (pd.DataFrame(df[i]) <= Q3 + 1.5*IQR)])
#     return pd.DataFrame(df_new)


# In[ ]:


# Checking for the outliers for the metric columns
b_cancer[['radius_mean','texture_mean', 'perimeter_mean', 'area_mean','smoothness_mean','compactness_mean','concavity_mean','concave points_mean','symmetry_mean']].describe([0.25,0.50,0.75,0.99])


# In[ ]:


# Removing outliers
plt.figure(figsize=(20,5))
plt.subplot(1,5,1)
sns.boxplot(y = b_cancer.area_mean)

plt.subplot(1,5,2)
sns.boxplot(y = b_cancer.compactness_mean)

plt.subplot(1,5,3)
sns.boxplot(y = b_cancer.concavity_mean)

plt.subplot(1,5,4)
sns.boxplot(y = b_cancer.symmetry_mean)

plt.subplot(1,5,5)
sns.boxplot(y = b_cancer['concave points_mean'])


# In[ ]:


# Removing Outliers
Q1 = b_cancer.area_mean.quantile(0.25)
Q3 = b_cancer.area_mean.quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer.area_mean >= Q1 - 1.5*IQR) & (b_cancer.area_mean <= Q3 + 1.5*IQR)]


Q1 = b_cancer.compactness_mean.quantile(0.25)
Q3 = b_cancer.compactness_mean.quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer.compactness_mean >= Q1 - 1.5*IQR) & (b_cancer.compactness_mean <= Q3 + 1.5*IQR)]


Q1 = b_cancer.concavity_mean.quantile(0.25)
Q3 = b_cancer.concavity_mean.quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer.concavity_mean >= Q1 - 1.5*IQR) & (b_cancer.concavity_mean <= Q3 + 1.5*IQR)]

Q1 = b_cancer.symmetry_mean.quantile(0.25)
Q3 = b_cancer.symmetry_mean.quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer.symmetry_mean >= Q1 - 1.5*IQR) & (b_cancer.symmetry_mean <= Q3 + 1.5*IQR)]


Q1 = b_cancer['concave points_mean'].quantile(0.25)
Q3 = b_cancer['concave points_mean'].quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer['concave points_mean'] >= Q1 - 1.5*IQR) & (b_cancer['concave points_mean'] <= Q3 + 1.5*IQR)]


# In[ ]:


b_cancer.shape


# In[ ]:


b_cancer[['fractal_dimension_mean','radius_se','texture_se','perimeter_se','area_se','smoothness_se','compactness_se','concavity_se','concave points_se','symmetry_se']].describe([0.25,0.50,0.75,0.99])


# In[ ]:


# Removing  outliers
plt.figure(figsize=(20,5))
plt.subplot(1,4,1)
sns.boxplot(y = b_cancer.texture_se)

plt.subplot(1,4,2)
sns.boxplot(y = b_cancer.area_se)

plt.subplot(1,4,3)
sns.boxplot(y = b_cancer.compactness_se)

plt.subplot(1,4,4)
sns.boxplot(y = b_cancer.concavity_se)


# In[ ]:


# Removing Outliers
Q1 = b_cancer.texture_se.quantile(0.25)
Q3 = b_cancer.texture_se.quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer.texture_se >= Q1 - 1.5*IQR) & (b_cancer.texture_se <= Q3 + 1.5*IQR)]


Q1 = b_cancer.area_se.quantile(0.25)
Q3 = b_cancer.area_se.quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer.area_se >= Q1 - 1.5*IQR) & (b_cancer.area_se <= Q3 + 1.5*IQR)]


Q1 = b_cancer.compactness_se.quantile(0.25)
Q3 = b_cancer.compactness_se.quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer.compactness_se >= Q1 - 1.5*IQR) & (b_cancer.compactness_se <= Q3 + 1.5*IQR)]

Q1 = b_cancer.concavity_se.quantile(0.25)
Q3 = b_cancer.concavity_se.quantile(0.75)
IQR = Q3 - Q1
b_cancer = b_cancer[(b_cancer.concavity_se >= Q1 - 1.5*IQR) & (b_cancer.concavity_se <= Q3 + 1.5*IQR)]


# In[ ]:


# Checking the numbers of rows after removing outliers
b_cancer.shape


# In[ ]:


# Describing again to check the effect after outliers removal
b_cancer[['fractal_dimension_se','radius_worst','texture_worst','perimeter_worst','area_worst','smoothness_worst','compactness_worst','concavity_worst','concave points_worst']].describe([0.25,0.50,0.75,0.99])


# In[ ]:


sns.boxplot(y = b_cancer.compactness_worst)


# In[ ]:


Q1 = b_cancer.compactness_worst.quantile(0.25)
Q3 = b_cancer.compactness_worst.quantile(0.75)
IQR = Q3 - Q1

b_cancer = b_cancer[(b_cancer.compactness_worst >= Q1 - 1.5*IQR) & (b_cancer.compactness_worst<=Q3 + 1.5*IQR)]


# In[ ]:


b_cancer.shape


# In[ ]:


b_cancer[['symmetry_worst', 'fractal_dimension_worst']].describe([0.99])


# In[ ]:


df_cancer = b_cancer


# In[ ]:


# Replacing the dependent variable with binary value for prediction
df_cancer.diagnosis = df_cancer.diagnosis.map({'M':1,'B':0})


# In[ ]:


# Checking for the outliers using pair plot
plt.figure(figsize = (10,10))
sns.pairplot(df_cancer.corr())


# In[ ]:


# Checking the correlation using heatmap
plt.figure(figsize=(20,20))
sns.heatmap(df_cancer.corr(),annot = True,cmap='winter')


# In[ ]:


plt.scatter(x = 'radius_worst',y = 'diagnosis',data = df_cancer)


# In[ ]:


# Spliting the dependent and independent variable
y = df_cancer.pop('diagnosis')
X = df_cancer


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


# Spliting the dataset for training and testing purpose
X_train,X_test,y_train,y_test = train_test_split(X,y,train_size= 0.7,test_size=0.3,random_state=100)


# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()


# In[ ]:


X_train.columns


# In[ ]:


# Scaling the dataset for bringing all the columns to a single scale
X_train = pd.DataFrame(scaler.fit_transform(pd.DataFrame(X_train)))


# In[ ]:


X_train.columns = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
       'smoothness_mean', 'compactness_mean', 'concavity_mean',
       'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
       'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
       'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
       'fractal_dimension_se', 'radius_worst', 'texture_worst',
       'perimeter_worst', 'area_worst', 'smoothness_worst',
       'compactness_worst', 'concavity_worst', 'concave points_worst',
       'symmetry_worst', 'fractal_dimension_worst']


# In[ ]:


# Describe the dataset after standerdScaling the mean should near to 0 and the SD should be 1
X_train.describe()


# In[ ]:


from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()


# In[ ]:


# Using the automated technique for feature selection
rfe = RFE(logreg,15)
rfe = rfe.fit(X_train,y_train)


# In[ ]:


list(zip(X_train.columns,rfe.support_,rfe.ranking_))


# In[ ]:


cols = X_train.columns[rfe.support_]


# In[ ]:


import statsmodels.api as sm


# In[ ]:


#Model 1
X_train_new1 = sm.add_constant(X_train[cols])
lm1 = sm.GLM(list(y_train),X_train_new1,family = sm.families.Binomial()).fit()
print(lm1.summary())


# In[ ]:


# Model 2
X_train_new2 = X_train_new1.drop('concave points_mean',axis='columns')
X_train_new2 = sm.add_constant(X_train_new2)
lm2 = sm.GLM(list(y_train),X_train_new2,family = sm.families.Binomial()).fit()
lm2.summary()


# In[ ]:


# Model 3
X_train_new3 = X_train_new2.drop('area_worst',axis='columns')
X_train_new3 = sm.add_constant(X_train_new3)
lm3 = sm.GLM(list(y_train),X_train_new3,family=sm.families.Binomial()).fit()
lm3.summary()


# In[ ]:


# Model 4
X_train_new4 = X_train_new3.drop('smoothness_worst',axis='columns')
X_train_new4 = sm.add_constant(X_train_new4)
lm4 = sm.GLM(list(y_train),X_train_new4,family=sm.families.Binomial()).fit()
lm4.summary()


# In[ ]:


# Model 5
X_train_new5 = X_train_new4.drop('area_se',axis='columns')
X_train_new5 = sm.add_constant(X_train_new5)
lm5 = sm.GLM(list(y_train),X_train_new5,family=sm.families.Binomial()).fit()
lm5.summary()


# In[ ]:


# Model 6
X_train_new6 = X_train_new5.drop('concavity_worst',axis='columns')
X_train_new6 = sm.add_constant(X_train_new6)
lm6 = sm.GLM(list(y_train),X_train_new6,family=sm.families.Binomial()).fit()
lm6.summary()


# In[ ]:


# Model 7
X_train_new7 = X_train_new6.drop('compactness_mean',axis='columns')
X_train_new7 = sm.add_constant(X_train_new7)
lm7 = sm.GLM(list(y_train),X_train_new7,family=sm.families.Binomial()).fit()
lm7.summary()


# In[ ]:


# Model 8
X_train_new8 = X_train_new7.drop('perimeter_worst',axis='columns')
X_train_new8 = sm.add_constant(X_train_new8)
lm8 = sm.GLM(list(y_train),X_train_new8,family=sm.families.Binomial()).fit()
lm8.summary()


# In[ ]:


# Creating fucntion to check the multicolenearity between the independent variables
from statsmodels.stats.outliers_influence import variance_inflation_factor
def calculate_vif(df):
    vif = pd.DataFrame()
    vif['Feature'] = df.columns
    vif['VIF'] = [variance_inflation_factor(df.values,i) for i in range(df.shape[1])]
    vif['VIF'] = round(vif['VIF'],2)
    vif = vif.sort_values(by = 'VIF',ascending=False)
    return vif


# In[ ]:


calculate_vif(X_train_new8.drop('const',axis='columns'))


# In[ ]:


#Model 9
X_train_new9 = X_train_new8.drop('concavity_mean',axis='columns')
X_train_new9 = sm.add_constant(X_train_new9)
lm9 = sm.GLM(list(y_train),X_train_new9,family=sm.families.Binomial()).fit()
print(lm9.summary())


# In[ ]:


# Model 10
X_train_new10 = X_train_new9.drop('compactness_se',axis = 'columns')
X_train_new10 = sm.add_constant(X_train_new10)
lm10 = sm.GLM(list(y_train),X_train_new10,family=sm.families.Binomial()).fit()
print(lm10.summary())


# In[ ]:


calculate_vif(X_train_new10.drop('const',axis=1))


# In[ ]:


# Model 10 is our final model based on that we will check the different metric now
y_train_pred = lm10.predict(X_train_new10)
print(y_train_pred[:10])


# In[ ]:


y_train_pred = y_train_pred.values.reshape(-1)


# In[ ]:


# Creating data frame with actual value and predicted probability

y_train_pred_final = pd.DataFrame({'cancer':y_train, 'cancer_prob':y_train_pred})
y_train_pred_final['ID'] = y_train.index


# In[ ]:


y_train_pred_final.head()


# In[ ]:


y_train_pred_final['predicted'] = y_train_pred_final.cancer_prob.map(lambda x : 1 if x>0.5 else 0)


# In[ ]:


y_train_pred_final.head()


# In[ ]:


from sklearn.metrics import confusion_matrix
confusion = confusion_matrix(y_train_pred_final.cancer,y_train_pred_final.predicted)
print(confusion)


# In[ ]:


# Predicted     not_cancer  cancer
# Actual
# not_cancer        208       7
# cancer            6       56  


# In[ ]:


from sklearn.metrics import accuracy_score
print(accuracy_score(y_train_pred_final.cancer,y_train_pred_final.predicted))


# In[ ]:


TP = confusion[1,1]
TN = confusion[0,0]
FN = confusion[1,0]
FP = confusion[0,1]


# In[ ]:


# sensitivity
print(TP/float(TP+FN))


# In[ ]:


#specificity
print(TN/float(TN+FP))


# In[ ]:


# False positive rate
print(FP/float(FP+TN))


# In[ ]:


from sklearn.metrics import roc_curve,roc_auc_score


# In[ ]:


def draw_roc(actual,prob):
    fpr,tpr,thresholds = roc_curve(actual,prob,drop_intermediate=True)
    accuracy_score = roc_auc_score(actual,prob)
    plt.figure(figsize=(5,5))
    plt.plot( fpr, tpr, label='ROC curve (area = %0.2f)'  %accuracy_score )
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate or [1 - True Negative Rate]')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.show()
    return None


# In[ ]:


draw_roc(y_train_pred_final.cancer,y_train_pred_final.predicted)


# In[ ]:


# Checking for the more accurate cutoff value
numbers = [float(x/10) for x in range(10)]

for i in numbers:
    y_train_pred_final[i] = y_train_pred_final.cancer_prob.map(lambda x : 1 if x>i else 0)
y_train_pred_final.head()


# In[ ]:


# Now let's calculate accuracy sensitivity and specificity for various probability cutoffs.
cutoff_df = pd.DataFrame( columns = ['prob','accuracy','sensi','speci'])
from sklearn.metrics import confusion_matrix

# TP = confusion[1,1] # true positive 
# TN = confusion[0,0] # true negatives
# FP = confusion[0,1] # false positives
# FN = confusion[1,0] # false negatives

num = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
for i in num:
    cm1 = confusion_matrix(y_train_pred_final.cancer, y_train_pred_final[i] )
    total1=sum(sum(cm1))
    accuracy = (cm1[0,0]+cm1[1,1])/total1
    
    speci = cm1[0,0]/(cm1[0,0]+cm1[0,1])
    sensi = cm1[1,1]/(cm1[1,0]+cm1[1,1])
    cutoff_df.loc[i] =[ i ,accuracy,sensi,speci]
print(cutoff_df)


# In[ ]:


# Let's plot accuracy sensitivity and specificity for various probabilities.
cutoff_df.plot.line(x='prob', y=['accuracy','sensi','speci'])
plt.show()


# In[ ]:


y_train_pred_final['final_predicted'] = y_train_pred_final.cancer_prob.map( lambda x: 1 if x > 0.2 else 0)
y_train_pred_final.head()


# In[ ]:


accuracy_score(y_train_pred_final.cancer,y_train_pred_final.final_predicted)


# In[ ]:


confusion = confusion_matrix(y_train_pred_final.cancer,y_train_pred_final.final_predicted)
confusion


# In[ ]:


TP = confusion[1,1]
TN = confusion[0,0]
FN = confusion[1,0]
FP = confusion[0,1]


# In[ ]:


#Sensitivity
print(TP/float(TP + FN))


# In[ ]:


#Specificity
print(TN/float(TN+FP))


# In[ ]:


X_train_new10.columns


# In[ ]:


# Now we will make prediction on the test data
X_test = pd.DataFrame(scaler.transform(pd.DataFrame(X_test)))
X_test.columns = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
       'smoothness_mean', 'compactness_mean', 'concavity_mean',
       'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
       'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
       'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
       'fractal_dimension_se', 'radius_worst', 'texture_worst',
       'perimeter_worst', 'area_worst', 'smoothness_worst',
       'compactness_worst', 'concavity_worst', 'concave points_worst',
       'symmetry_worst', 'fractal_dimension_worst']


# In[ ]:


cols = X_train_new10.columns[X_train_new10.columns !='const']


# In[ ]:


X_test = X_test[cols]


# In[ ]:


X_test_sm = sm.add_constant(X_test)
y_test_pred = lm10.predict(X_test_sm)


# In[ ]:


y_pred_1 = pd.DataFrame(y_test_pred)


# In[ ]:


y_pred_1.head(5)


# In[ ]:


y_test_df = pd.DataFrame(y_test)


# In[ ]:


# Removing index for both dataframes to append them side by side 
y_pred_1.reset_index(drop=True, inplace=True)
y_test_df.reset_index(drop=True, inplace=True)


# In[ ]:


y_pred_final = pd.concat([y_test_df,y_pred_1],axis='columns')


# In[ ]:


y_pred_final.columns = ['cancer','pred_prob']


# In[ ]:


y_pred_final['Prediction'] = y_pred_final.pred_prob.map(lambda x : 1 if x>0.2 else 0)


# In[ ]:


y_pred_final.head()


# In[ ]:


accuracy_score(y_pred_final.cancer,y_pred_final.Prediction)


# In[ ]:


confusion = confusion_matrix(y_pred_final.cancer,y_pred_final.Prediction)
confusion


# In[ ]:


TP = confusion[1,1]
TN = confusion[0,0]
FN = confusion[1,0]
FP = confusion[0,1]
print(TP,TN,FP,FN)


# In[ ]:


# Sensitivity
print(TP/float(TP+FN))


# In[ ]:


# Specificity
print(TN/float(TN+FP))


# In[ ]:




