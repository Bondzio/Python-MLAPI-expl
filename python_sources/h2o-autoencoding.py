#!/usr/bin/env python
# coding: utf-8

# > * **Import Dependencies**

# In[ ]:


import gc
gc.collect()
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os, time, sys
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
# Call h2o
import h2o
## If h2o is already started
#h2o.shutdown(prompt=False)  
#h2o.cluster().shutdown()
h2o.init()
h2o.connect()


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output


# Any results you write to the current directory are saved as output.


# * **Import RF, GBM and Stacked Ensemble Estimators**

# In[ ]:


from h2o.estimators.deeplearning import H2OAutoEncoderEstimator


# * **Also Grid search while stacking**

# In[ ]:


from h2o.grid.grid_search import H2OGridSearch


# * **What h2o objects are in memory**

# In[ ]:


h2o.ls()


# * **Remove specific object from memory**

# In[ ]:


#       h2o.remove("model_grid")
#      Remove all h2o objects from memory
h2o.remove_all()
h2o.ls()


# * **Read in an H2OFrameand explore data**

# In[ ]:


train = pd.read_csv("../input/Kaggle_Training_Dataset_v2.csv", header=0)
test = pd.read_csv("../input/Kaggle_Test_Dataset_v2.csv", header=0)


# * **Find Missing Values - Train Data**

# In[ ]:


def findMissingValues(data):
    total = data.isnull().sum().sort_values(ascending=False)
    missing_data = pd.concat([total], axis=1, keys=['Total', 'Percent'])
    return missing_data 
def missingDataTreatment(data,missing_data):
    data = data.drop((missing_data[missing_data['Total'] > 1]).index,1)
    return data
def removeNa(data):
    data.dropna(axis=0, how='any',inplace = True)
    return data


# In[ ]:


missing_data=findMissingValues(train)
#train=missingDataTreatment(train,missing_data)
train=removeNa(train)
missing_data=findMissingValues(train)
missing_data


# In[ ]:


missing_data=findMissingValues(test)
#test=missingDataTreatment(test,missing_data)
test=removeNa(test)
missing_data=findMissingValues(test)
missing_data


# In[ ]:


train=train.replace('Yes',1)
train=train.replace('No',0)
test=test.replace('Yes',1)
test=test.replace('No',0)


# In[ ]:


train_h = h2o.H2OFrame(train)
test_h = h2o.H2OFrame(test)

#  Identify predictors and response

X = train_h.columns          
y = "went_on_backorder"    # Target column name
X.remove(y)


# In[ ]:


anomaly_model = H2OAutoEncoderEstimator(   activation="Tanh",
                                           hidden=[22, 10,2,10,  22],
                                           ignore_const_cols = False,
                                           epochs=500)

anomaly_model.train(x = X,  training_frame = train_h)
recon_error = anomaly_model.anomaly(train_h)

layerLevel= 3
bidimensional_data = anomaly_model.deepfeatures(train_h,layerLevel)
bidimensional_data = bidimensional_data.cbind(train_h[y])
bidimensional_data = bidimensional_data.as_data_frame()

print("MSE := ",anomaly_model.mse())


# In[ ]:


layerLevel= 2
bidimensional_data = anomaly_model.deepfeatures(train_h,layerLevel)
bidimensional_data = bidimensional_data.cbind(train_h[y])
bidimensional_data = bidimensional_data.as_data_frame()


# In[ ]:


error_train = train_h.cbind(recon_error)

error_train = error_train.as_data_frame()
error_train['id'] = error_train.index.values ;

sns.FacetGrid(error_train, hue=y, size=8).map(plt.scatter, "id", "Reconstruction.MSE").add_legend()
plt.show()

error_train[error_train[y] == 1].plot(kind='scatter', x='id', y='Reconstruction.MSE',c='green',marker='x', label='True')
error_train[error_train[y] == 0].plot(kind='scatter', x='id', y='Reconstruction.MSE',c='yellow',marker='o', label='False')
plt.legend(loc='upper left')
plt.show()


# In[ ]:


h2o.remove_all()
h2o.ls()
h2o.shutdown()    
h2o.cluster().shutdown()

