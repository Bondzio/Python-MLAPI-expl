#!/usr/bin/env python
# coding: utf-8

# In this kernel we will be demonstrating the Grid Search technique used for model optimization.Most cases after the basic model is build the challenge for the data scientist is to optimize hyperparameters.Grid search can help us in doing it.If you like my work please do vote.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# **Importing Python Modules**

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# **Importing dataset**

# In[ ]:


df = pd.read_csv('../input/socialnetwork/Social_Network.csv')
df.head()


# **Creating the matrix of features**

# In[ ]:


X=df.iloc[:,[2,3]].values
y=df.iloc[:,4].values


# **Splitting the dataset into Training and Test Set **

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)


# **Feature Scaling **

# In[ ]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# **Training Kernel SVM Model on the dataset**

# In[ ]:


from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf',random_state=0)
classifier.fit(X_train,y_train)


# **Making confusion Matrix**

# In[ ]:


from sklearn.metrics import confusion_matrix,accuracy_score
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test,y_pred)
print(cm)
accuracy_score(y_test,y_pred)


# So our model has good accuray of 93 %. But to have a better evaluation of model performance we need to cross check the accuracy using K Fold Cross Validation.

# **Applying K-Fold Cross Validation**

# In[ ]:


from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier,X = X_train,y = y_train,cv = 10)
print('Accuracy: {:.2f} %'.format(accuracies.mean()*100))
print('Standard Deviation: {:.2f} %'.format(accuracies.std()*100))


# In case of Cross validation we have used 10 set of validation data to evaluate our model accuracy.From the K fold cross validation we get an accuray score of 90.33% with a standard deviation of 6.57%. This means our models can gave an accuracy between 84 to 96%.

# **Applying Grid Search to find out the best model and best parameters**

# In[ ]:


from sklearn.model_selection import GridSearchCV
parameters = [{'C':[0.25,0.5,0.75,1],'kernel':['linear']},
             {'C':[0.25,0.5,0.75,1],'kernel':['rbf'],'gamma':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]}]
grid_search = GridSearchCV(estimator = classifier,
                          param_grid = parameters,
                          scoring = 'accuracy',
                          cv =10,
                          n_jobs = -1)
grid_search.fit(X_train,y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_
print('Best Accuracy: {:.2f} %'.format(best_accuracy*100))
print('Best Parameters:',best_parameters)


# So using Grid Search we are able to get the best hyperameters that we should us to have best accuracy for our model.
