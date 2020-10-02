#!/usr/bin/env python
# coding: utf-8

# **The method being used to detect anomalies in the production line is Logistic Regression. The output is a binary one and hence the above decision was made. Since the assumption of no multicollinearity of the Logistic Regression model was being violated, Principal Component Analysis was used to eliminate it. But before this, some routine checks like class imbalance and missing values were made in order to prepare the data for analysis.**

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
from sklearn import preprocessing
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA
from sklearn import metrics
import statsmodels.api as sm
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


#Loading the dataset
df= pd.read_csv("/kaggle/input/bda-2019-ml-test/Train_Mask.csv")
X = df.drop("flag",1)   #Feature Matrix
y = df["flag"]          #Target Variable
df.shape


# In[ ]:


#Checking for class imbalance
print(df['flag'].value_counts())
sns.countplot(x='flag',data=df)
plt.show()
count_anomaly = len(df[df['flag']==0])
count_normal = len(df[df['flag']==1])
pct_anomaly = count_anomaly/(count_anomaly+count_normal)
print("percentage of anomaly:", pct_anomaly*100)
pct_normal = count_normal/(count_anomaly+count_normal)
print("percentage of normal:", pct_normal*100)
print("There is no class imbalance")


# In[ ]:


#Checking for missing values
if df.shape==df.notnull().shape:
    print (" No missing values")
else:
    print(" There are missing values")


# In[ ]:


#Backward Elimination to remove unimportant features
cols = list(X.columns)
pmax = 1
while (len(cols)>0):
    p= []
    X_1 = X[cols]
    X_1 = sm.add_constant(X_1)
    model = sm.OLS(y,X_1).fit()
    p = pd.Series(model.pvalues.values[1:],index = cols)      
    pmax = max(p)
    feature_with_p_max = p.idxmax()
    if(pmax>0.05):
        cols.remove(feature_with_p_max)
    else:
        break
selected_features_BE = cols
print(selected_features_BE)


# In[ ]:


#The new feature matrix
new_x = pd.DataFrame(df[selected_features_BE],columns=selected_features_BE)
new_x.head()


# In[ ]:


#Check for multicollinearity
cor= new_x.corr()
sns.heatmap(cor)
print("Multicollinearity exists")


# In[ ]:


#Fitting a logistic model
X_train, X_test, y_train, y_test = train_test_split(new_x, y, test_size=0.3)
#Principal Component Analysis to combat multicollinearity
model_pca = PCA(n_components=5)
new_train = model_pca.fit_transform(X_train)
new_test  = model_pca.fit_transform(X_test)
logreg=LogisticRegression()
logreg.fit(new_train,y_train)


# In[ ]:


#f1 score of logistic model
y_pred=logreg.predict(new_test)
print(classification_report(y_test,y_pred))


# In[ ]:


#Implementing model on test data
test=pd.read_csv("../input/bda-2019-ml-test/Test_Mask_Dataset.csv")
model_pca = PCA(n_components=5)
test= model_pca.fit_transform(test)
pred=logreg.predict(test)


# In[ ]:


#Sample imputation
sub=pd.read_csv("../input/bda-2019-ml-test/Sample Submission.csv")
sub['flag']=pred
sub


# In[ ]:


#Creation of submission file
sub.to_csv("Sample Submission5.csv",index=False)

