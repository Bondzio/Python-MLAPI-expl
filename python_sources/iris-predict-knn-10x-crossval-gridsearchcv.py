#!/usr/bin/env python
# coding: utf-8

# ## Super beginner

# Iris dataset is one of the basic simple and small dataset for those who want to start learning data science which including myself. This is one of my early code and it's very easy to follow.
# 
# In beginning I learned about supervised and unsupervised learning. For supervised learning, kNN is one of the famous algorithm to use and hence for this I decided to use kNN.
# 
# I added hyperparameter GridSearchCV after I've learn more about Machine Learning and having much better understanding of kNN

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# ### **1. Exploratory Data Analysis**
# ####  **1.1 Import Libraries**

# In[ ]:


# pandas - data analysis library
import pandas as pd

#scientific computing library
import numpy as np

# data visualization library
import matplotlib.pyplot as plt

# line required for inline charts/plots
get_ipython().run_line_magic('matplotlib', 'inline')

# for high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns


# #### **1.2 Assign dataframe**

# In[ ]:


#read dataframe
df_iris = pd.read_csv("/kaggle/input/iris/Iris.csv")

# check first five row of dataframe
df_iris.head()


# I use head() function to get initial overview of the dataframe.

# In[ ]:


# get summary
df_iris.info()


# I use info() function to get more information of the number of rows and columns, data type and missing value

# In[ ]:


# drop id column - data cleaning
df_iris = df_iris.drop(['Id'], axis = 1)


# In[ ]:


#findout no of rows for each Species. to check whether dataset is balanced or not
print(df_iris.groupby('Species').size())


# class is balance

# In[ ]:


#Plot a pairwise relationships
sns.pairplot(df_iris,x_vars=['SepalLengthCm','SepalWidthCm'], 
             y_vars=['PetalLengthCm','PetalWidthCm'],hue='Species')


# the visualisation helps me to understand the correlation of each attributes to the class

# ### **Split DataFrame into Train & Test**

# In[ ]:


#Defining data and label
X = df_iris.iloc[:, :-1]
y = df_iris.iloc[:, -1]

#Split data into training and test datasets (training will be based on 70% of data)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify =y)

# transform data so its distribution will have a mean value 0 and standard deviation of 1
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#test_size: if integer, number of examples into test dataset; if between 0.0 and 1.0, means proportion
print('There are {} samples in the training set and {} samples in the test set'.format(X_train.shape[0], X_test.shape[0]))


# # **KNN**

# In[ ]:


from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

#create report function
def generateClassificationReport(y_test,y_pred):
    print(classification_report(y_test,y_pred))
    print(confusion_matrix(y_test,y_pred))    
    print('accuracy is ',accuracy_score(y_test,y_pred))
    df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    df['result'] = np.where(df['Actual'] == df['Predicted'], 'correct', 'wrong')
    print(df)


# In[ ]:


#K-NEAREST NEIGHBOUR
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train,y_train)
y_pred = knn.predict(X_test)


# In[ ]:


from sklearn import metrics

# empty variable for storing the KNN metrics
scores=[]

# We try different values of k for the KNN (from k=1 up to k=26)
lrange=list(range(1,26,2))

# loop the KNN process
for k in lrange:
    # input the k value and 'distance' measure
    knn=KNeighborsClassifier(n_neighbors=k)
    # input the train data to train KNN
    knn.fit(X_train,y_train)
    # see KNN prediction by inputting the test data
    y_pred=knn.predict(X_test)
    # append the performance metric (accuracy)
    scores.append(metrics.accuracy_score(y_test,y_pred))

optimal_k = lrange[scores.index(max(scores))]
print("The optimal number of neighbors is %d" % optimal_k)
print("The optimal score is %.2f" % max(scores))

plt.figure(2,figsize=(15,5))
    
# plot the results
plt.plot(lrange, scores,ls='dashed')
plt.xlabel('Value of k for KNN')
plt.ylabel('Accuracy Score')
plt.title('Accuracy Scores for Values of k of k-Nearest-Neighbors')
plt.xticks(lrange)
plt.yticks(scores)

plt.grid()
plt.show()


# In[ ]:


#using 10 fold cross validation
# empty variable for storing the KNN metrics
scores=[]

# We try different values of k for the KNN (from k=1 up to k=26)
lrange=list(range(1,26, 2))

# loop the KNN process
for k in lrange:
    # input the k value and 'distance' measure
    knn=KNeighborsClassifier(n_neighbors=k, weights='distance', algorithm='auto')
    # get score for the 10 fold cross validation
    score = cross_val_score(knn, X_train, y_train, cv=10, scoring='accuracy')
    scores.append(score.mean())

optimal_k = lrange[scores.index(max(scores))]
print("The optimal number of neighbors is %d" % optimal_k)
print("The optimal score is %.2f" % max(scores))

plt.figure(2,figsize=(15,5))
    
# plot the results
plt.plot(lrange, scores,ls='dashed')
plt.xlabel('Value of k for KNN')
plt.ylabel('Accuracy Score')
plt.title('Accuracy Scores for Values of k of k-Nearest-Neighbors')
plt.xticks(lrange)

plt.grid()
plt.show()


# In[ ]:


#using hyperparameter
from sklearn.model_selection import GridSearchCV

params = {
    'n_neighbors' : [5, 25],
    'weights': ['uniform', 'distance'],
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
}
grid_kn = GridSearchCV(estimator = knn,
                        param_grid = params,
                        scoring = 'accuracy', 
                        cv = 5, 
                        verbose = 1,
                        n_jobs = -1)
grid_kn.fit(X_train, y_train)


# In[ ]:


# extract best estimator
print(grid_kn.best_estimator_)


# In[ ]:


# to test the bestfit
print(grid_kn.score(X_test, y_test))

