#!/usr/bin/env python
# coding: utf-8

# # Minimizing the Churn Rate Through Analysis of Financial Habits 
# 
# # Table of Contents: 
# * [1-Exploratory Data Analysis](#eda)
# * [2-Preprocessing the data](#preprocessing)
# * [3-Training the model](#training)
# * [4-Evaluating the model](#evaluation)
# * [5-Feature selection](#features)
#     * [5.1-Evaluating the new model](#evaluation2)
# * [6-Conclusions](#conclusions)
# 

# In[ ]:


#importing libraries
import pandas as pd
import numpy as np
import os
import random
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


#loading the dataset
df=pd.read_csv("../input/new_churn_data.csv")


# # Exploratory Data Analysis <a class='anchor' id='eda'></a>

# In[ ]:


#list of columns
list(df)


# In[ ]:


df.head()


# In[ ]:


#detecting missing values
df.isna().any()


# In[ ]:


plt.figure(figsize=(12,10))
sns.heatmap(df.corr())


# In[ ]:


df2=df[['age','cards_clicked','cards_viewed','cash_back_engagement']]
#histogram to get the distributions of different variables
df2.hist(bins=70, figsize=(20,20))
plt.show()


# # Preprocessing the data <a class='anchor' id='preprocessing'></a>

# In[ ]:


user_id = df['userid']
df=df.drop(columns=['userid'])


# In[ ]:


#transforming into dummy variables
df.rent_or_own.value_counts()
df.groupby('rent_or_own')['churn'].nunique().reset_index()
df = pd.get_dummies(df)
df.columns
df = df.drop(columns = ['rent_or_own_na', 'zodiac_sign_na', 'payfreq_na'])


# In[ ]:


#splitting our data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns = 'churn'), df['churn'],
                                                    test_size = 0.2,
                                                    random_state = 1992)


# In[ ]:


# Balancing the Training Set
y_train.value_counts()

pos_index = y_train[y_train.values == 1].index
neg_index = y_train[y_train.values == 0].index

if len(pos_index) > len(neg_index):
    higher = pos_index
    lower = neg_index
else:
    higher = neg_index
    lower = pos_index

random.seed(1992)
higher = np.random.choice(higher, size=len(lower))
lower = np.asarray(lower)
new_indexes = np.concatenate((lower, higher))

X_train = X_train.loc[new_indexes,]
y_train = y_train[new_indexes]


# In[ ]:


#scaling the variables
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train2 = pd.DataFrame(sc_X.fit_transform(X_train))
X_test2 = pd.DataFrame(sc_X.transform(X_test))
X_train2.columns = X_train.columns.values
X_test2.columns = X_test.columns.values
X_train2.index = X_train.index.values
X_test2.index = X_test.index.values
X_train = X_train2
X_test = X_test2


# # Training the model <a class='anchor' id='training'></a>

# In[ ]:


from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 1492)
classifier.fit(X_train, y_train)


# In[ ]:


y_pred=classifier.predict(X_test)


# # Evaluating the model <a class='anchor' id='evaluation'></a>

# In[ ]:


from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
cm = confusion_matrix(y_test, y_pred)
accuracy_score(y_test, y_pred)
precision_score(y_test, y_pred) # tp / (tp + fp)
recall_score(y_test, y_pred) # tp / (tp + fn)
f1_score(y_test, y_pred)

df_cm = pd.DataFrame(cm, index = (0, 1), columns = (0, 1))
plt.figure(figsize = (10,7))
sns.set(font_scale=1.4)
sns.heatmap(df_cm, annot=True, fmt='g')
print("Test Data Accuracy: %0.4f" % accuracy_score(y_test, y_pred))
print("Precission score: %0.4f" % precision_score(y_test, y_pred))
print("Recall score: %0.4f" % recall_score(y_test, y_pred))
print("F1 score: %0.4f" %f1_score(y_test, y_pred))


# In[ ]:


# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
print("SVM Accuracy: %0.3f (+/- %0.3f)" % (accuracies.mean(), accuracies.std() * 2))


# In[ ]:


# Analyzing Coefficients
pd.concat([pd.DataFrame(X_train.columns, columns = ["features"]),
           pd.DataFrame(np.transpose(classifier.coef_), columns = ["coef"])
           ],axis = 1)


# # Feature selection <a class='anchor' id='features'></a>

# In[ ]:


# Recursive Feature Elimination (RFE)
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

# Model to Test
classifier = LogisticRegression()


# In[ ]:


# Select Best X Features
rfe = RFE(classifier, 20)
rfe = rfe.fit(X_train, y_train)
# summarize the selection of the attributes
print(rfe.support_)
print(rfe.ranking_)
X_train.columns[rfe.support_]


# In[ ]:


#new heatmap
# New Correlation Matrix
sns.set(style="white")

# Compute the correlation matrix
corr = X_train[X_train.columns[rfe.support_]].corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(18, 15))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})  


# # Evaluating the model <a class='anchor' id='evaluation2'></a>

# In[ ]:


classifier = LogisticRegression()
classifier.fit(X_train[X_train.columns[rfe.support_]], y_train)

# Predicting Test Set
y_pred = classifier.predict(X_test[X_train.columns[rfe.support_]])


# In[ ]:


from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
cm = confusion_matrix(y_test, y_pred)
accuracy_score(y_test, y_pred)
precision_score(y_test, y_pred) # tp / (tp + fp)
recall_score(y_test, y_pred) # tp / (tp + fn)
f1_score(y_test, y_pred)

df_cm = pd.DataFrame(cm, index = (0, 1), columns = (0, 1))
plt.figure(figsize = (10,7))
sns.set(font_scale=1.4)
sns.heatmap(df_cm, annot=True, fmt='g')
print("Test Data Accuracy: %0.4f" % accuracy_score(y_test, y_pred))
print("Precission score: %0.4f" % precision_score(y_test, y_pred))
print("Recall score: %0.4f" % recall_score(y_test, y_pred))
print("F1 score: %0.4f" %f1_score(y_test, y_pred))


# In[ ]:


from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier,
                             X = X_train[X_train.columns[rfe.support_]],
                             y = y_train, cv = 10)
print("SVM Accuracy: %0.3f (+/- %0.3f)" % (accuracies.mean(), accuracies.std() * 2))


# In[ ]:


# Analyzing Coefficients
pd.concat([pd.DataFrame(X_train[X_train.columns[rfe.support_]].columns, columns = ["features"]),
           pd.DataFrame(np.transpose(classifier.coef_), columns = ["coef"])
           ],axis = 1)


# In[ ]:


# Formatting Final Results
final_results = pd.concat([y_test, user_id], axis = 1).dropna()
final_results['predicted_churn'] = y_pred
final_results = final_results[['userid', 'churn', 'predicted_churn']].reset_index(drop=True)
print(final_results)


# # Conclusions <a class='anchor' id='conclusions'></a>
# 
# ### The model has around the 65% of accuracy. The next steps to improve the score could be: 
# ### 1- Try with another method such as XGBoost.
# ### 2- Select or discard other features.
# ### 3- Do oversampling or undersampling to the dataset.

# In[ ]:




