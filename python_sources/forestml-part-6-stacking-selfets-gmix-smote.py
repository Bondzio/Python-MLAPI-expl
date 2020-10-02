#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# Import required librarues

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import QuantileTransformer

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.multiclass import OneVsRestClassifier

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
import catboost as cb
import lightgbm as lgb

from mlxtend.classifier import StackingCVClassifier
from sklearn.model_selection import cross_val_score

from sklearn.metrics import accuracy_score

from mlxtend.feature_selection import ColumnSelector
from sklearn.pipeline import make_pipeline

from imblearn.over_sampling import SMOTE


# In[ ]:





# In[ ]:





# ### Import the Raw Data

# In[ ]:


train = pd.read_csv("/kaggle/input/learn-together/train.csv")
test = pd.read_csv("/kaggle/input/learn-together/test.csv")


# In[ ]:


# Remove the Labels and make them y
y = train['Cover_Type']

# Remove label from Train set
X = train.drop(['Cover_Type'],axis=1)

# Rename test to text_X
test_X = test



# split data into training and validation data
train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.2, random_state=42)

X = X.drop(['Id'], axis = 1)
train_X = train_X.drop(['Id'], axis = 1)
val_X = val_X.drop(['Id'], axis = 1)
test_X = test_X.drop(['Id'], axis = 1)


# In[ ]:


train_X.describe()


# In[ ]:


val_X.describe()


# In[ ]:


## Harnessing Gaussian Mixture from https://www.kaggle.com/stevegreenau/stacking-multiple-classifiers-clustering


# In[ ]:




print('> Adding cluster based feature')
from sklearn.mixture import GaussianMixture

gmix = GaussianMixture(n_components=10)
gmix.fit(test_X)

train_X['Test_Cluster'] = gmix.predict(train_X)
val_X['Test_Cluster'] = gmix.predict(val_X)
test_X['Test_Cluster'] = gmix.predict(test_X)


# In[ ]:





# In[ ]:


sns.distplot(train_X['Elevation'], label = 'train_X')
sns.distplot(val_X['Elevation'], label = 'val_X')
sns.distplot(test_X['Elevation'], label = 'test_X')
plt.legend()
plt.title('Elevation')
plt.show()


# In[ ]:


sns.distplot(train_X['Aspect'], label = 'train_X')
sns.distplot(val_X['Aspect'], label = 'val_X')
sns.distplot(test_X['Aspect'], label = 'test_X')
plt.title('Aspect')
plt.legend()
plt.show()


# In[ ]:


sns.distplot(train_X['Horizontal_Distance_To_Hydrology'], label = 'train_X')
sns.distplot(val_X['Horizontal_Distance_To_Hydrology'], label = 'val_X')
sns.distplot(test_X['Horizontal_Distance_To_Hydrology'], label = 'test_X')
plt.title('Horizontal_Distance_To_Hydrology')
plt.legend()
plt.show()


# In[ ]:


sns.distplot(train_X['Vertical_Distance_To_Hydrology'], label = 'train_X')
sns.distplot(val_X['Vertical_Distance_To_Hydrology'], label = 'val_X')
sns.distplot(test_X['Vertical_Distance_To_Hydrology'], label = 'test_X')
plt.title('Vertical_Distance_To_Hydrology')
plt.legend()
plt.show()


# In[ ]:


sns.distplot(train_X['Horizontal_Distance_To_Roadways'], label = 'train_X')
sns.distplot(val_X['Horizontal_Distance_To_Roadways'], label = 'val_X')
sns.distplot(test_X['Horizontal_Distance_To_Roadways'], label = 'test_X')
plt.title('Horizontal_Distance_To_Roadways')
plt.legend()
plt.show()


# In[ ]:


sns.distplot(train_X['Hillshade_9am'], label = 'train_X')
sns.distplot(val_X['Hillshade_9am'], label = 'val_X')
sns.distplot(test_X['Hillshade_9am'], label = 'test_X')
plt.title('Hillshade_9am')
plt.legend()
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


### define the classifiers
### Parameters from :https://www.kaggle.com/joshofg/pure-random-forest-hyperparameter-tuning

classifier_rf = RandomForestClassifier(n_estimators = 719,
                                       max_features = 0.3,
                                       max_depth = 464,
                                       min_samples_split = 2,
                                       min_samples_leaf = 1,
                                       bootstrap = False,
                                       random_state=42)
classifier_xgb = OneVsRestClassifier(XGBClassifier(n_estimators = 719,
                                                   max_depth = 464,
                                                   random_state=42))
classifier_et = ExtraTreesClassifier(random_state=42)
classifier_lg = lgb.LGBMClassifier(silent=True, random_state=42)
classifier_adb = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth  = 464,
                                                                          min_samples_split = 2,
                                                                          min_samples_leaf = 1,
                                                                          random_state=42), random_state=42)


# In[ ]:


pipe_rf = make_pipeline(ColumnSelector(cols=(0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53)),
                        classifier_rf)
pipe_xgb = make_pipeline(ColumnSelector(cols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 51, 52)),
                         classifier_xgb)
pipe_et = make_pipeline(ColumnSelector(cols=(0, 1, 3, 5, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53)),
                        classifier_et)

pipe_lg = make_pipeline(ColumnSelector(cols=(0, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 23, 24, 25, 26, 29, 30, 31, 33, 35, 36, 37, 42, 43, 44, 45, 46, 48, 51, 53)),
                        classifier_lg)


pipe_adb = make_pipeline(ColumnSelector(cols=(0, 1, 3, 5, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 22, 23, 24, 26, 27, 28, 29, 30, 31, 33, 34, 36, 37, 38, 39, 41, 42, 44, 45, 46, 47, 48, 50, 51, 52, 53)),
                        classifier_adb)


# In[ ]:





# In[ ]:


sm = SMOTE(random_state=2, sampling_strategy = 'all', ratio = {1:8000, 2:8000, 3:3000, 4:3000, 5:3000, 6:3000, 7:3000})
train_X_sm, train_y_sm = sm.fit_sample(train_X, train_y.ravel())

print('After OverSampling, the shape of train_X: {}'.format(train_X_sm.shape))
print('After OverSampling, the shape of train_y: {}'.format(train_y_sm.shape))

print("After OverSampling, counts of label '1': {}".format(sum(train_y_sm==1)))
print("After OverSampling, counts of label '2': {}".format(sum(train_y_sm==2)))
print("After OverSampling, counts of label '3': {}".format(sum(train_y_sm==3)))
print("After OverSampling, counts of label '4': {}".format(sum(train_y_sm==4)))
print("After OverSampling, counts of label '5': {}".format(sum(train_y_sm==5)))
print("After OverSampling, counts of label '6': {}".format(sum(train_y_sm==6)))
print("After OverSampling, counts of label '7': {}".format(sum(train_y_sm==7)))


# In[ ]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
sclf = StackingCVClassifier(classifiers=[pipe_rf,
                                         pipe_xgb,
                                         pipe_et,
                                         pipe_lg,
                                         pipe_adb],
                            use_probas=True,
                            meta_classifier=classifier_rf)



labels = ['Random Forest', 'XGBoost', 'ExtraTrees', 'LightGBM', 'AdaBoost', 'MetaClassifier']




for clf, label in zip([classifier_rf, classifier_xgb, classifier_et, classifier_lg, classifier_adb, sclf], labels):
    scores = cross_val_score(clf, train_X_sm, train_y_sm.ravel(),
                             cv=5,
                             scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))


# In[ ]:


sclf.fit(train_X.values, train_y.values.ravel())


# In[ ]:



val_pred = sclf.predict(val_X.values)


# In[ ]:


acc = accuracy_score(val_y, val_pred)
print(acc)


# In[ ]:


sclffin = StackingCVClassifier(classifiers=[pipe_rf,
                                            pipe_xgb,
                                            pipe_et,
                                            pipe_lg,
                                            pipe_adb],
                            use_probas=True,
                            meta_classifier=classifier_rf)


# In[ ]:


print("Before OverSampling, counts of label '1': {}".format(sum(y==1)))
print("Before OverSampling, counts of label '2': {}".format(sum(y==2)))
print("Before OverSampling, counts of label '3': {}".format(sum(y==3)))
print("Before OverSampling, counts of label '4': {}".format(sum(y==4)))
print("Before OverSampling, counts of label '5': {}".format(sum(y==5)))
print("Before OverSampling, counts of label '6': {}".format(sum(y==6)))
print("Before OverSampling, counts of label '7': {}".format(sum(y==7)))


# In[ ]:


sm = SMOTE(random_state=2, sampling_strategy = 'all', ratio = {1:8000, 2:8000, 3:3000, 4:3000, 5:3000, 6:3000, 7:3000})
X_sm, y_sm = sm.fit_sample(X, y.ravel())

print('After OverSampling, the shape of train_X: {}'.format(X_sm.shape))
print('After OverSampling, the shape of train_y: {}'.format(y_sm.shape))

print("After OverSampling, counts of label '1': {}".format(sum(y_sm==1)))
print("After OverSampling, counts of label '2': {}".format(sum(y_sm==2)))
print("After OverSampling, counts of label '3': {}".format(sum(y_sm==3)))
print("After OverSampling, counts of label '4': {}".format(sum(y_sm==4)))
print("After OverSampling, counts of label '5': {}".format(sum(y_sm==5)))
print("After OverSampling, counts of label '6': {}".format(sum(y_sm==6)))
print("After OverSampling, counts of label '7': {}".format(sum(y_sm==7)))


# In[ ]:





# In[ ]:


sclffin.fit(X_sm, y_sm.ravel())


# In[ ]:


test_ids = test["Id"]
test_pred = sclffin.predict(test_X.values)


# In[ ]:


# Save test predictions to file
output = pd.DataFrame({'Id': test_ids,
                       'Cover_Type': test_pred})
output.to_csv('submission.csv', index=False)

