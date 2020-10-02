#!/usr/bin/env python
# coding: utf-8

# Aljo Jose - 05 June 2017

# **Motivation - Classify Iris plants into three species based on attributes given.**

# In[ ]:


# Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# # 1.1. Load dataset and summarize.

# In[ ]:


# Load dataset and draw shape.
dataset = pd.read_csv('../input/Iris.csv')
dataset.shape


# 150 samples, 05 attributes and 01 outcome.

# In[ ]:


# Looking at a few samples.
dataset.sample(5)


# Column "Id" can be ignored as it has no relation with outcome.

# In[ ]:


dataset.drop('Id', axis = 1, inplace = True)
dataset.describe()


# All attributes are having values.  attribute values can be scaled during pre-processing.

# In[ ]:


dataset.info()


# Output "Species" needs to be encoded. 

# # 1.2. Visualize dataset.

# In[ ]:


# Encode outcome variable.
key = {'Iris-setosa':0,'Iris-versicolor':1,'Iris-virginica':2}
dataset['Species'] = dataset['Species'].map(key)
dataset.sample(5) # Encoding looks fine.


# In[ ]:


# histogram
dataset.hist(figsize=(10, 8))


# SepalWidth nearly follows Gaussian distribution.
# <br> Each output type has exactly 50 samples.

# In[ ]:


dataset.plot( kind = 'box', subplots = True, layout = (3,3), sharex = False, sharey = False, figsize = (10, 8)   )


# In[ ]:


import seaborn as sns
Corr = dataset[dataset.columns].corr()
sns.heatmap(Corr, annot = True )


# # 1.3. Data pre-processing.

# In[ ]:





# In[ ]:


# Split dataset into X and y. (Removed SepalWidth as it doesn't much help in predicting the outcome)
X = np.array(dataset[["SepalLengthCm","PetalLengthCm","PetalWidthCm"]]) 
y = dataset['Species'].values


# In[ ]:


# Split into training and test set.
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state =0 )


# In[ ]:


# Standardize train and test sets.
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
sc_X.fit (X_train)
X_train = sc_X.transform(X_train)
X_test = sc_X.transform(X_test)

print("Training set sample \n\n" +str(X_train[:2]))
print("\nTest set sample \n\n" +str(X_test[:2]))


# In[ ]:


# Applying Kernel PCA to select best features.
from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
explained_variance = pca.explained_variance_ratio_
print(explained_variance)


# SepalWidth doesn't help in predicting Species.

# In[ ]:


sns.violinplot(dataset.SepalWidthCm)


# In[ ]:


#sns.violinplot(dataset.SepalWidthCm, dataset.SepalLengthCm, vert=False)


# #1.4. Evaluate models.

# In[ ]:


# Import suite of classifers.
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier, GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV


# In[ ]:


# Create objects of required models.
models = []
models.append(("LR",LogisticRegression()))
models.append(("GNB",GaussianNB()))
models.append(("KNN",KNeighborsClassifier()))
models.append(("DecisionTree",DecisionTreeClassifier()))
models.append(("LDA",  LinearDiscriminantAnalysis()))
models.append(("QDA",  QuadraticDiscriminantAnalysis()))
models.append(("AdaBoost", AdaBoostClassifier()))
models.append(("SVM Linear",SVC(kernel="linear")))
models.append(("SVM RBF",SVC(kernel="rbf")))
models.append(("Random Forest",  RandomForestClassifier()))
models.append(("Bagging",BaggingClassifier()))
models.append(("Calibrated",CalibratedClassifierCV()))
models.append(("GradientBoosting",GradientBoostingClassifier()))
models.append(("LinearSVC",LinearSVC()))
models.append(("Ridge",RidgeClassifier()))


# In[ ]:


# Find accuracy of models.
results = []
for name,model in models:
    kfold = KFold(n_splits=10, random_state=0)
    cv_result = cross_val_score(model,X_train,y_train, cv = kfold,scoring = "accuracy")
    results.append(tuple([name,cv_result.mean(), cv_result.std()]))
  
results.sort(key=lambda x: x[1], reverse = True)    
for i in range(len(results)):
    print('{:20s} {:2.2f} (+/-) {:2.2f} '.format(results[i][0] , results[i][1] * 100, results[i][2] * 100))


# #1.5.  Optimize performance.

# In[ ]:


from sklearn.model_selection import GridSearchCV
model = DecisionTreeClassifier()         
paramaters = [
             {'max_depth' : [2,4,6,8,10], 'criterion' : ['gini']} ,         
             {'max_depth' : [2,4,6,8,10], 'criterion' : ['entropy']}   
   
             ]
grid_search = GridSearchCV(estimator = model, 
                           param_grid = paramaters,
                           scoring = 'accuracy',
                           cv = 10,
                           n_jobs = -1)
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_ 
best_parameters = grid_search.best_params_  

print('Best accuracy : ', grid_search.best_score_)
print('Best parameters :', grid_search.best_params_  )


# #1.6. Finalise model and predict performance on test set.

# In[ ]:


final_model = DecisionTreeClassifier(criterion='gini',max_depth=4, random_state =0)
final_model.fit(X_train, y_train)
y_pred = final_model.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cf = confusion_matrix(y_test, y_pred)
print(cf)
print(accuracy_score(y_test, y_pred) * 100)


# **Conclusion : Observed 96.7% accuracy on IRIS model using DecisionTree Classifier**.
