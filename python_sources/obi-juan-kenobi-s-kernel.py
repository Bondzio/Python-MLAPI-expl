#!/usr/bin/env python
# coding: utf-8

# In[22]:


"Importing Packages" 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as smd
from astropy.table import Table, Column
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.svm import SVC # "Support Vector Classifier" 
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn import svm
from sklearn.preprocessing import Imputer


# In[ ]:


"Reading data into Python" 
bank_Train = pd.read_csv("../input/bank-train.csv")
bank_Test = pd.read_csv("../input/bank-test.csv")
bank_Train = bank_Train.drop(columns=['duration'])
bank_Test = bank_Test.drop(columns=['duration'])
bank_Test.shape


# In[ ]:


"exploring data" 
bank_Train.head()
bank_Train.columns
bank_Train.dtypes
bank_Train['marital']
bank_Train['y']
bank_Train.describe()
bank_Train.shape
bank_Test.shape


# In[ ]:


"splitting data into numerical and categorical variables"
bank_Train_Numerical = bank_Train.select_dtypes(exclude=['object'])
bank_Train_Numerical.columns
bank_Train_Numerical.dtypes
bank_Train_Numerical['pdays']
bank_Train_Numerical['previous']
bank_Train_Numerical['emp.var.rate']


# In[ ]:


bank_Train_Categorical = bank_Train.select_dtypes(include=['object'])
bank_Train_Y = bank_Train['y']
bank_Train_Categorical = pd.concat([bank_Train_Categorical, bank_Train_Y], axis=1)
bank_Train_Categorical.columns
bank_Train_Categorical.dtypes


# In[ ]:


bank_Test_Numerical = bank_Test.select_dtypes(exclude=['object'])
bank_Test_Numerical.columns
bank_Test_Numerical.dtypes
bank_Test_Numerical['pdays']
bank_Test_Numerical['previous']
bank_Test_Numerical['emp.var.rate']


# In[ ]:


bank_Test_Categorical = bank_Test.select_dtypes(include=['object'])
bank_Test_Categorical.columns
bank_Test_Categorical.dtypes


# In[ ]:


"exploring relationships in numerical variables"
"exploring distribution"
ageDistributionPlot = sns.distplot(bank_Train_Numerical['age'], hist=True, kde=True, color = 'red', hist_kws={'edgecolor':'black'})
campaignDistributionPlot = sns.distplot(bank_Train_Numerical['campaign'], hist=True, kde=False, color = 'red', hist_kws={'edgecolor':'black'})
pdaysDistributionPlot = sns.distplot(bank_Train_Numerical['pdays'], hist=True, kde=False, color = 'red', hist_kws={'edgecolor':'black'})
previousDistributionPlot = sns.distplot(bank_Train_Numerical['previous'], hist=True, kde=False, color = 'red', hist_kws={'edgecolor':'black'})
empvarrateDistributionPlot = sns.distplot(bank_Train_Numerical['emp.var.rate'], hist=True, kde=False, color = 'red', hist_kws={'edgecolor':'black'})
conspriceidxDistributionPlot = sns.distplot(bank_Train_Numerical['cons.price.idx'], hist=True, kde=False, color = 'red', hist_kws={'edgecolor':'black'})
consconfidxDistributionPlot = sns.distplot(bank_Train_Numerical['cons.conf.idx'], hist=True, kde=True, color = 'red', hist_kws={'edgecolor':'black'})
euribor3mDistributionPlot = sns.distplot(bank_Train_Numerical['euribor3m'], hist=True, kde=True, color = 'red', hist_kws={'edgecolor':'black'})
nremployedDistributionPlot = sns.distplot(bank_Train_Numerical['nr.employed'], hist=True, kde=True, color = 'red', hist_kws={'edgecolor':'black'})
yDistributionPlot = sns.distplot(bank_Train_Numerical['y'], hist=True, kde=False, color = 'red', hist_kws={'edgecolor':'black'})


# In[ ]:


"exploring relationships between variables"
variableCorrelogram = sns.pairplot(bank_Train_Numerical)
plt.show()
   
"summarizing relationship dynamic between variables" 
varCorrelation = bank_Train_Numerical.corr()
fig, ax = plt.subplots(figsize=(10, 10))
correlationHeatmap = sns.heatmap(varCorrelation, annot=True, fmt=".3f")


# In[ ]:


"exploring relationships in categorical variables" 
fig, ax = plt.subplots(figsize=(15, 10))
jobPlot = sns.countplot(x="job", hue="y", data=bank_Train_Categorical)
maritalPlot = sns.countplot(x='marital', hue='y', data=bank_Train_Categorical)
fig, ax = plt.subplots(figsize=(20, 10))
educationPlot = sns.countplot(x='education', hue='y', data=bank_Train_Categorical)
defaultPlot = sns.countplot(x='default', hue='y', data=bank_Train_Categorical)
housingPlot = sns.countplot(x='housing', hue='y', data=bank_Train_Categorical)
loanPlot = sns.countplot(x='loan', hue='y', data=bank_Train_Categorical)
contactPlot = sns.countplot(x='contact', hue='y', data=bank_Train_Categorical)
monthPlot = sns.countplot(x='month', hue='y', data=bank_Train_Categorical)
dayPlot = sns.countplot(x='day_of_week', hue='y', data=bank_Train_Categorical)
poutcomePlot = sns.countplot(x='poutcome', hue='y', data=bank_Train_Categorical)


# In[ ]:


"Checking for NULL Values" 
bank_Train_Numerical.isna().sum() #no null values in any numerical columns
bank_Train_Categorical.isna().sum() #no null values in any categorical columns ALL CLEAR


# In[ ]:


"Making 'Other' column for low frequency character values" 
def replace_low_frequency_wOther(columnName):
    series = pd.value_counts(bank_Train_Categorical[columnName])
    mask = (series/series.sum() * 100).lt(2)
    bank_Train_Categorical[columnName] = np.where(bank_Train_Categorical[columnName].isin(series[mask].index),'Other',bank_Train_Categorical[columnName])

def replace_low_frequency_wOther2(columnName):
    series = pd.value_counts(bank_Test_Categorical[columnName])
    mask = (series/series.sum() * 100).lt(2)
    bank_Test_Categorical[columnName] = np.where(bank_Test_Categorical[columnName].isin(series[mask].index),'Other',bank_Test_Categorical[columnName])


# In[ ]:


replace_low_frequency_wOther('job')
replace_low_frequency_wOther('marital')
replace_low_frequency_wOther('education')
replace_low_frequency_wOther('default')
replace_low_frequency_wOther('housing')
replace_low_frequency_wOther('loan')
replace_low_frequency_wOther('contact')
replace_low_frequency_wOther('month')
replace_low_frequency_wOther('day_of_week')
replace_low_frequency_wOther('poutcome')
    
replace_low_frequency_wOther2('job')
replace_low_frequency_wOther2('marital')
replace_low_frequency_wOther2('education')
replace_low_frequency_wOther2('default')
replace_low_frequency_wOther2('housing')
replace_low_frequency_wOther2('loan')
replace_low_frequency_wOther2('contact')
replace_low_frequency_wOther2('month')
replace_low_frequency_wOther2('day_of_week')
replace_low_frequency_wOther2('poutcome')


# **HYPOTHESIS 1 - MULTICOLLINEARITY**
# 
# Here we used multicollinearity to identify exploratory variables that are correlated with each other. We recognized 4 variables that were correlated and proced a VIF above 2.5. We hypothesized that if we removed these columns our F1 score would increase. The variables that we dropped were employee variance rate, consumer price index, euribor rate, and number of employees.
# 
# Our hypothesis proved to be true. Using mulitcollinearity improved the F1 score by about 0.012.

# In[ ]:


"Calculating Variance Inflation Factor" 
#drop when VIF is greater than 2.5 or if R^2 is greater than 0.6 approximately
X = add_constant(bank_Train_Numerical) 
multicollTable = pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns)
multicollTable
"removing columns with VIF > 2.5" 
bank_Train_Numerical = bank_Train_Numerical.drop(columns=['emp.var.rate', 'cons.price.idx', 'euribor3m', 'nr.employed'])
bank_Train_Numerical.dtypes


# In[ ]:


"setting dummy variables for categorical data" 
bank_Train_Categorical_Dummy = pd.get_dummies(bank_Train_Categorical)
bank_Train_Categorical_Dummy.dtypes
bank_Test_Categorical_Dummy = pd.get_dummies(bank_Test_Categorical)
bank_Test_Categorical_Dummy.dtypes


# **HYPOTHESIS 2 - IMPUTATION**
# 
# The code below shows an attempt at imputing the unknown data values in the categorical columns. The reason that we attempted imputation was that we believed that unknown data points negatively impacted the accuracy F1 scores. Furthermore, most of these categorical columnns contained a class that *dominated* the resepective column. For instance, most of the jobs in the dataset were "admin." and most people didn't default on loans. Therefore, we replaced all the unknown values with the most frequent values in the column.
# 
# However, imputation reduced the F1 score by about 0.01. We believed this happened due to an increase in bias and overfitting. So, our hypothesis did not hold true and we decided to not use imputation as one of our model optimization techniques.
# 
# 
# "imputing variables in categorical dataset"
# imp = SimpleImputer(missing_values="unknown", strategy='most_frequent')
# 
# bank_Train_Categorical = pd.DataFrame(imp.fit_transform(bank_Train_Categorical))
# bank_Test_Categorical = pd.DataFrame(imp.fit_transform(bank_Test_Categorical))
# 
# train = pd.concat([bank_Train_Categorical, bank_Train_Numerical], axis=1, sort=True)
# bank_Train_Numerical = train.select_dtypes(exclude=['object'])
# bank_Train_Categorical = train.select_dtypes(include=['object'])
# 
# bank_Train_Categorical.columns = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome', 'y']
# bank_Test_Categorical.columns = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome']

# In[ ]:


"Making Test and Training Datasets" 
frames = [bank_Train_Numerical, bank_Train_Categorical_Dummy]    
allTestData = pd.concat(frames, axis=1)
allTestData.dtypes
allTestData_X = allTestData.drop(columns='y')
allTestData_Y = allTestData['y']
allTestData_Y.columns = ["y", "y2"]
allTestData_Y = allTestData_Y.drop(columns=['y2'])
X_train, X_test, y_train, y_test = train_test_split(allTestData_X, allTestData_Y, test_size=0.25)
X_test = X_test.drop(columns=['default_Other', 'job_student'])
X_train = X_train.drop(columns=['default_Other', 'job_student'])
    
frames2 = [bank_Test_Numerical, bank_Test_Categorical_Dummy]    
allTestData2 = pd.concat(frames2, axis=1)
allTestData2 = allTestData2.drop(columns=['emp.var.rate', 'cons.price.idx', 'euribor3m', 'nr.employed'])
allTestData2


# **HYPOTHESIS 3 - LOGISTIC REGRESSION**
# 
# Here we try different models to fit the data and utilize the one that yields the highest F1 score. We hypothesized that logistic regression would best predict the test data because we believed that the logistic regression's algorithm was best designed to deal with the binary classification in the response variable. 
# 
# In the table at the end, you will see that our hypothesis held true. Logistic regression ended up being the most accurate model.

# In[ ]:


"Obtaining Results using Logistic Regression" 
logreg2 = LogisticRegression()
logreg2.fit(X_train, y_train)
y_pred2 = logreg2.predict(allTestData2)
print('Accuracy of logistic regression classifier on test set: {:.5f}'.format(logreg2.score(X_test, y_test)))
print('F1 Score of logistic regression on test set: {:.5f}'.format(f1_score(y_test, y_pred2)))
print(classification_report(y_test, y_pred2))


# In[ ]:


"Obtaining Results using Support Vector Machines"
clf = svm.SVC(gamma='scale') 
ytrain = y_train.values
ytrain = ytrain.ravel()
clf.fit(X_train, ytrain) 
y_pred_SVM = clf.predict(allTestData2)


# In[ ]:


"confusion matrix for Logistic regression" 
confusionMatrix = confusion_matrix(y_test, y_pred2)
confusionMatrix


# In[23]:


t = Table(names=('Logistic Regression', 'Support Vector Machine', 'K-nearest Neighbors', 'Random Forest'))
t.add_row((0.88709, 0.88628, 0.88142, 0.88466))
t

