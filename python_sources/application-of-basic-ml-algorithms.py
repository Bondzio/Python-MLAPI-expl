#!/usr/bin/env python
# coding: utf-8

# <Center><H1>Credit Card Fraud Detection </Center></H1> 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # for data visualization
import seaborn as sns # for heatmap plot
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
# Suppressing Warnings
import warnings
warnings.filterwarnings('ignore')
#import os
#print(os.listdir("../input"))
CCData = pd.read_csv("../input/creditcard.csv")
CCData.shape
# Any results you write to the current directory are saved as output.


# In[ ]:


CCData.describe()


# ### Data Preparation
# As the data is generated by PCA not performing any other data Preparation Steps.
# 
# The idea behind StandardScaler is that it will transform your data such that its distribution will have a mean value 0 and standard deviation of 1. Given the distribution of the data, each value in the dataset will have the sample mean value subtracted, and then divided by the standard deviation of the whole dataset.

# In[ ]:


#Time column is not necessary so removing it form the data
from sklearn.preprocessing import StandardScaler
#CCData['Amount'].head()
CCData['NormAmount'] = StandardScaler().fit_transform(CCData['Amount'].values.reshape(-1, 1))
CCData = CCData.drop(['Time','Amount'],axis=1)
CCData.head()


# In[ ]:


plt.figure(figsize = (50,50))        # Size of the figure
sns.heatmap(CCData.corr(),annot = True)


# As the data has been derived from PCA, Very less Co-relation exists between features

# In[ ]:


# plotting a histogram to identify the frequency of each type in class
count_classes = pd.value_counts(CCData['Class'], sort = True).sort_index()
count_classes.plot(kind = 'bar')
plt.title("Credit Card - Fraud Class histogram (1 represent Fraud)")
plt.xlabel("Class")
plt.ylabel("Frequency")


# In[ ]:


# Showing ratio
print("Percentage of normal transactions: ", (len(CCData[CCData.Class == 0])/len(CCData))*100)
print("Percentage of fraud transactions: ", (len(CCData[CCData.Class == 1])/len(CCData))*100)
print("Total number of transactions in sampled data: ", len(CCData))


# ### From the above graph and percentage it is clear that Non Fraud data points are consierably huge when compared to Fraud datapoints. So we need to redistribute the sample in such 50-50 Fraud & non Fraud dataset.

# ## **SMOTE (Synthetic Minority Over-sampling Technique)**
# SMOTE is an over-sampling method. What it does is, it creates synthetic (not duplicate) samples of the minority class. Hence making the minority class equal to the majority class. SMOTE does this by selecting similar records and altering that record one column at a time by a random amount within the difference to the neighbouring records.
# #### if you fail to import imblearn please run following command here - !pip install imblearn

# #### Before Applying SMOTE, breaking the whole dataframe into Test and Train and the apply SMOTE on Train Data

# In[ ]:


from sklearn.model_selection import train_test_split

# Putting feature variable to X
X = CCData.drop(['Class'],axis=1)
# Putting response variable to y
y = CCData['Class']
X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=0.7,test_size=0.3,random_state=100)
print("Number transactions X_train dataset: ", X_train.shape)
print("Number transactions y_train dataset: ", y_train.shape)
print("Number transactions X_test dataset: ", X_test.shape)
print("Number transactions y_test dataset: ", y_test.shape)


# In[ ]:


X_train.head()


# In[ ]:


# if you fail to import imblearn please run following command here -!pip install imblearn

from imblearn.over_sampling import SMOTE

print("Before OverSampling, counts of label '1': {}".format(sum(y_train==1)))
print("Before OverSampling, counts of label '0': {} \n".format(sum(y_train==0)))

sm = SMOTE(random_state=2)
X_train_res, y_train_res = sm.fit_sample(X_train, y_train.ravel())

print('After OverSampling, the shape of train_X: {}'.format(X_train_res.shape))
print('After OverSampling, the shape of train_y: {} \n'.format(y_train_res.shape))

print("After OverSampling, counts of label '1': {}".format(sum(y_train_res==1)))
print("After OverSampling, counts of label '0': {}".format(sum(y_train_res==0)))


# In[ ]:


X_train_res


# ### Converting resulted numpy arrays into dataframes with header info

# In[ ]:


X_train_df=pd.DataFrame(X_train_res,columns=X_train.columns)
X_train_df.head()


# In[ ]:


# plotting a histogram to identify the frequency of each type in class
count_classes = pd.value_counts(y_train_res, sort = True).sort_index()
count_classes.plot(kind = 'bar')
plt.title("Credit Card - Fraud Class histogram (1 represent Fraud)")
plt.xlabel("Class")
plt.ylabel("Frequency")


# <h2> Model Building </h2>

# ### Feature Selection

# In[ ]:


##X_train_res, y_train_res
X_train_df.shape


# ### As the training set contains 29 Features in it , we will perform Feature Selection using RFE to pick top 10 Features that will assist in bulding the model

# In[ ]:


from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
from sklearn.feature_selection import RFE
rfe = RFE(logreg, 10)             # running RFE with 10 variables as output
rfe = rfe.fit(X_train_df,y_train_res)
print(rfe.support_)           # Printing the boolean results
print(rfe.ranking_)           # Printing the ranking


# In[ ]:


col = X_train_df.columns[rfe.support_]
print(col)


# In[ ]:


UpdatedTrain_X=X_train_df[col]
print(UpdatedTrain_X.shape)
UpdatedTest_X=X_test[col]
print(UpdatedTest_X.shape)


# In[ ]:


import statsmodels.api as sm
df_train_rfe = sm.add_constant(UpdatedTrain_X)
log_mod_rfe = sm.GLM(y_train_res,df_train_rfe,family = sm.families.Binomial())
mod_res_rfe = log_mod_rfe.fit()
log_mod_rfe.fit().summary()


# In[ ]:


#Predicting the Test Data
UpdatedTestCoef_X = sm.add_constant(UpdatedTest_X[col])
predictions = mod_res_rfe.predict(UpdatedTestCoef_X)


# Obtaining Metrics from the above model

# In[ ]:


Y_pred= predictions.map(lambda x: 1 if x > 0.5 else 0)
Y_pred.head()


# In[ ]:


from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test,Y_pred))


# In[ ]:


# Let us calculate 
from sklearn import metrics
print(metrics.confusion_matrix(y_test, Y_pred), "\n")
print("accuracy", metrics.accuracy_score(y_test, Y_pred))
print("precision", metrics.precision_score(y_test,Y_pred))
print("recall", metrics.recall_score(y_test,Y_pred))
confusion=confusion_matrix(y_test,Y_pred)    
TP = confusion[1,1] # true positive 
TN = confusion[0,0] # true negatives
FP = confusion[0,1] # false positives
FN = confusion[1,0] # false negatives
# Let's see the sensitivity of our logistic regression model
print("Sensitivity",TP / float(TP+FN))
# positive predictive value 
print ("Positive Predection Rate",TP / float(TP+FP))
# Negative predictive value
print ("Negative Predection rate",TN / float(TN+ FN))
# Calculate false postive rate - predicting churn when customer does not have churned
print("False positive Predection Rate",FP/ float(TN+FP))


# In[ ]:


def draw_roc( actual, probs ):
    fpr, tpr, thresholds = metrics.roc_curve( actual, probs,
                                              drop_intermediate = False )
    auc_score = metrics.roc_auc_score( actual, probs )
    plt.figure(figsize=(5, 5))
    plt.plot( fpr, tpr, label='ROC curve (area = %0.2f)' % auc_score )
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate or [1 - True Negative Rate]')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

    return None

draw_roc(y_test, Y_pred)


# ## Model -2 : Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
# Create a based model
rf = RandomForestClassifier()


# In[ ]:


rf.fit(UpdatedTrain_X, y_train_res)


# In[ ]:


y_pred=rf.predict(UpdatedTest_X)
Y_pred=pd.DataFrame(y_pred)
#Y_pred= Y_pred.map(lambda x: 1 if x > 0.5 else 0)
Y_pred.shape


# In[ ]:


# Let's check the report of our default model
print(classification_report(y_test,Y_pred))


# In[ ]:


# Let us calculate 
from sklearn import metrics
print(metrics.confusion_matrix(y_test, Y_pred), "\n")
print("accuracy", metrics.accuracy_score(y_test, Y_pred))
print("precision", metrics.precision_score(y_test,Y_pred))
print("recall", metrics.recall_score(y_test,Y_pred))
confusion=confusion_matrix(y_test,Y_pred)    
TP = confusion[1,1] # true positive 
TN = confusion[0,0] # true negatives
FP = confusion[0,1] # false positives
FN = confusion[1,0] # false negatives
# Let's see the sensitivity of our logistic regression model
print("Sensitivity",TP / float(TP+FN))
# positive predictive value 
print ("Positive Predection Rate",TP / float(TP+FP))
# Negative predictive value
print ("Negative Predection rate",TN / float(TN+ FN))
# Calculate false postive rate - predicting churn when customer does not have churned
print("False positive Predection Rate",FP/ float(TN+FP))


# In[ ]:


feature_importances = pd.DataFrame(rf.feature_importances_,
                                   index = UpdatedTrain_X.columns,
                                    columns=['importance']).sort_values('importance',ascending=False)


# In[ ]:


feature_importances


# In[ ]:




