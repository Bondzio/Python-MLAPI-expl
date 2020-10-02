#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import all necessary libraries
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split

from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


# #### Data Import

# In[ ]:


#import file and reading few lines
numbers = pd.read_csv('../input/train.csv')
numbers.head(10)


# In[ ]:


numbers.shape


# #### Data understanding and exploration

# In[ ]:


#checking the datatype
numbers.info()


# All the data type are of type -int64.

# In[ ]:


numbers.describe(percentiles = [0.05,0.10,0.25,0.50,0.75,0.90,0.99])


# In[ ]:


round(100*(numbers.isnull().sum()/(len(numbers.index))),2).sort_values(ascending = False)


# There are no null values.

# Column - `Label`

# In[ ]:


# let us check unique entries of label column
np.unique(numbers['label'])


# In[ ]:


numbers['label'].value_counts()


# In[ ]:


#visualising the column - label
sns.countplot(numbers['label'],palette = 'icefire')


# Let us examine few `pixels`

# In[ ]:


y = pd.value_counts(numbers.values.ravel()).sort_index()
N = len(y)
x = range(N)
width =0.9
plt.figure(figsize=[8,8])
plt.bar(x, y, width, color="blue")
plt.title('Pixel Value Frequency (Log Scale)')
plt.yscale('log')
plt.xlabel('Pixel Value (0-255)')
plt.ylabel('Frequency')


# In[ ]:


plt.figure(figsize=(5,5))
sns.distplot(numbers['pixel656'])
plt.show()


# In[ ]:


plt.figure(figsize=(5,5))
sns.distplot(numbers['pixel684'])


# `Label` vs `pixel`

# In[ ]:


sns.barplot(x='label', y='pixel683', data=numbers)


# In[ ]:


sns.barplot(x='label', y='pixel572', data=numbers)


# #### Let us visualise few numbers:

# In[ ]:


one = numbers.iloc[2, 1:]
one = one.values.reshape(28,28)
plt.imshow(one)
plt.title("Digit 1")


# In[ ]:


nine = numbers.iloc[11, 1:]
nine = nine.values.reshape(28,28)
plt.imshow(nine)
plt.title("Digit 9")


# In[ ]:


zero = numbers.iloc[1, 1:]
zero = zero.values.reshape(28,28)
plt.imshow(zero)
plt.title("Digit 0")


# #### Let us check heatmap

# In[ ]:


plt.figure(figsize=(15,15))
sns.heatmap(data=numbers.corr(),annot=False)


# Almost all nearby pixel values are correlated, which is expected as well.

# #### Data Preparation:

# In[ ]:


# average feature values
pd.set_option('display.max_rows', 999)
round(numbers.drop('label', axis=1).mean(), 2).sort_values(ascending = False)


# We see that average varies between 140 to 0. It is better to scale them.

# In[ ]:


# splitting into X and y
X = numbers.drop("label", axis = 1)
y = numbers['label']


# In[ ]:


# scaling the features
X_scaled = scale(X)

# train test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, train_size=0.2,test_size = 0.8, random_state = 101)


# In[ ]:


print('X_train shape:',X_train.shape)
print('y_train shape:',y_train.shape)
print('X_test shape:',X_test.shape)
print('y_test shape:',y_test.shape)


# #### Model Building:

# 1. Let us first try - `Linear` model:

# In[ ]:


# linear model
model_linear = SVC(kernel='linear')
model_linear.fit(X_train, y_train)

# predict
y_pred = model_linear.predict(X_test)


# In[ ]:


# confusion matrix and accuracy, precision, recall

# accuracy
print("accuracy:", metrics.accuracy_score(y_true=y_test, y_pred=y_pred), "\n")

# cm
print(metrics.confusion_matrix(y_true=y_test, y_pred=y_pred))


# In[ ]:


#precision, recall and f1-score
scores=metrics.classification_report(y_test, y_pred, labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(scores)


# The linear model gives approx. 91.31% accuracy. Let's look at a non-linear model with randomly chosen hyperparameters.

# Let us try `Non- linear` models:

# 2. `Poly` kernel

# In[ ]:


# non-linear model
# using poly kernel, C=1, default value of gamma

# model
non_linear_model_poly = SVC(kernel='poly')

# fit
non_linear_model_poly.fit(X_train, y_train)

# predict
y_pred = non_linear_model_poly.predict(X_test)


# In[ ]:


# confusion matrix and accuracy, precision, recall

# accuracy
print("accuracy:", metrics.accuracy_score(y_true=y_test, y_pred=y_pred), "\n")

# cm
print(metrics.confusion_matrix(y_true=y_test, y_pred=y_pred))


# The accuracy dropped to 87.12%, so obviously no point in going with polynomial. Let us try 'rbf'.

# 3. `rbf` kernel

# In[ ]:


# non-linear model
# using rbf kernel, C=1, default value of gamma

# model
non_linear_model = SVC(kernel='rbf')

# fit
non_linear_model.fit(X_train, y_train)

# predict
y_pred = non_linear_model.predict(X_test)


# In[ ]:


# confusion matrix and accuracy, precision, recall

# accuracy
print("accuracy:", metrics.accuracy_score(y_true=y_test, y_pred=y_pred), "\n")

# cm
print(metrics.confusion_matrix(y_true=y_test, y_pred=y_pred))


# In[ ]:


#precision, recall and f1-score
scores=metrics.classification_report(y_test, y_pred, labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(scores)


# As we clearly see that the non-linear rbf model gives approx. 94% accuracy. And most of the precision is above 90%.Thus, going forward, let's choose hyperparameters corresponding to non-linear rbf models.
# 

# #### Grid Search: Hyperparameter Tuning:

# In[ ]:


# creating a KFold object with 5 splits 
folds = KFold(n_splits = 5, shuffle = True, random_state = 101)

# specify range of hyperparameters
# Set the parameters by cross-validation
hyper_params = [ {'gamma': [0.01, 0.001,0.0001],
                     'C': [1, 10, 100]}]


# specify model
model = SVC(kernel="rbf")

# set up GridSearchCV()
model_cv = GridSearchCV(estimator = model, 
                        param_grid = hyper_params, 
                        scoring= 'accuracy', 
                        cv = folds, 
                        verbose = 1,
                        return_train_score=True,n_jobs = -1)      

# fit the model
model_cv.fit(X_train, y_train)  


# In[ ]:


# cv results
cv_results = pd.DataFrame(model_cv.cv_results_)
cv_results


# In[ ]:


# converting C to numeric type for plotting on x-axis
cv_results['param_C'] = cv_results['param_C'].astype('int')

# # plotting
plt.figure(figsize=(20,7))

# subplot 1/3
plt.subplot(131)
gamma_01 = cv_results[cv_results['param_gamma']==0.01]

plt.plot(gamma_01["param_C"], gamma_01["mean_test_score"])
plt.plot(gamma_01["param_C"], gamma_01["mean_train_score"])
plt.xlabel('C')
plt.ylabel('Accuracy')
plt.title("Gamma=0.01")
plt.ylim([0.50, 1.1])
plt.legend(['test accuracy', 'train accuracy'], loc='upper left')
plt.xscale('log')

# subplot 2/3
plt.subplot(132)
gamma_001 = cv_results[cv_results['param_gamma']==0.001]

plt.plot(gamma_001["param_C"], gamma_001["mean_test_score"])
plt.plot(gamma_001["param_C"], gamma_001["mean_train_score"])
plt.xlabel('C')
plt.ylabel('Accuracy')
plt.title("Gamma=0.001")
plt.ylim([0.50, 1.1])
plt.legend(['test accuracy', 'train accuracy'], loc='upper left')
plt.xscale('log')


# subplot 3/3
plt.subplot(133)
gamma_0001 = cv_results[cv_results['param_gamma']==0.0001]

plt.plot(gamma_0001["param_C"], gamma_0001["mean_test_score"])
plt.plot(gamma_0001["param_C"], gamma_0001["mean_train_score"])
plt.xlabel('C')
plt.ylabel('Accuracy')
plt.title("Gamma=0.0001")
plt.ylim([0.50, 1.1])
plt.legend(['test accuracy', 'train accuracy'], loc='upper left')
plt.xscale('log')


# In[ ]:


# printing the optimal accuracy score and hyperparameters
best_score = model_cv.best_score_
best_hyperparams = model_cv.best_params_

print("The best test score is {0} corresponding to hyperparameters {1}".format(best_score, best_hyperparams))


# Let us go with the best value ({'C': 10, 'gamma': 0.001}) as suggested by the sklearn.

# #### Building and Evaluating the Final Model

# In[ ]:


# model with optimal hyperparameters

# model
model = SVC(C=10, gamma=0.001, kernel="rbf")

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# metrics
print("accuracy", metrics.accuracy_score(y_test, y_pred), "\n")
print(metrics.confusion_matrix(y_test, y_pred), "\n")


# In[ ]:


# different class-wise accuracy - #precision, recall and f1-score
scores=metrics.classification_report(y_test, y_pred, labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(scores)


# We see that with hyperparameter - C = 10 and gamma = 0.001, we see overall accuracy of the model is 95% and also precision for each label is above 94%.

# In[ ]:


# Let us visualize our final model on unseen training dataset

df = np.random.randint(1,y_pred.shape[0]+1,5)

plt.figure(figsize=(16,4))
for i,j in enumerate(df):
    plt.subplot(150+i+1)
    d = X_test[j].reshape(28,28)
    plt.title(f'Predicted Label: {y_pred[j]}')
    plt.imshow(d)
plt.show()


# #### Let us use our final model on test data (test.csv)

# In[ ]:


#import file and reading few lines
test_df = pd.read_csv('../input/test.csv')
test_df.head(10)


# In[ ]:


test_df.shape


# In[ ]:


test_df.info()


# In[ ]:


# scaling the features
test_scaled = scale(test_df)


# In[ ]:


#model.predict
test_predict = model.predict(test_scaled)


# In[ ]:


# Plotting the distribution of prediction
a = {'ImageId': np.arange(1,test_predict.shape[0]+1), 'Label': test_predict}
data_to_export = pd.DataFrame(a)
sns.countplot(data_to_export['Label'], palette = 'icefire')


# In[ ]:


# Let us visualize few of predicted test numbers

df = np.random.randint(1,test_predict.shape[0]+1,5)

plt.figure(figsize=(16,4))
for i,j in enumerate(df):
    plt.subplot(150+i+1)
    d = test_scaled[j].reshape(28,28)
    plt.title(f'Predicted Label: {test_predict[j]}')
    plt.imshow(d)
plt.show()


# In[ ]:


# Exporting the predicted values 
data_to_export.to_csv(path_or_buf='submission.csv', index=False)

