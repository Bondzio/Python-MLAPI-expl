#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input/twitter-user-gender-classification/'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


## Amir Shokri
## St code : 9811920009
## E-mail : amirsh.nll@gmail.com


# In[ ]:


## mlp


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neural_network import MLPClassifier

import os
for dirname, _, filenames in os.walk('/Users/Amirsh.nll/Downloads/'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


data = pd.read_csv('/kaggle/input/twitter-user-gender-classification/gender-classifier-DFE-791531.csv', encoding ='latin1')
data.info()


# In[ ]:


data = data.drop(['_unit_id', '_golden', '_unit_state', '_trusted_judgments', '_last_judgment_at', 'profile_yn', 'profile_yn:confidence', 'created', 'description', 'gender_gold', 'link_color', 'profile_yn_gold', 'profileimage', 'sidebar_color', 'text', 'tweet_coord', 'tweet_created', 'tweet_id', 'tweet_location', 'user_timezone', 'gender:confidence', 'gender', 'name'],axis=1)


# In[ ]:


data.head(20000)


# In[ ]:


y = data['tweet_count'].values
y = y.reshape(-1,1)
x_data = data.drop(['tweet_count'],axis = 1)
print(x_data)


# In[ ]:


x = (x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data)).values
x.head(20000)


# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.5,random_state=100)

y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)

print("x_train: ",x_train.shape)
print("x_test: ",x_test.shape)
print("y_train: ",y_train.shape)
print("y_test: ",y_test.shape)

my_x = x_train
my_y = y_train

my_xx = x_test
my_yy = y_test


# In[ ]:


from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(3, 2), random_state=1)


# In[ ]:


clf.fit(my_x, my_y)
y_pred = clf.predict(my_xx)
print("Accuracy:",metrics.accuracy_score(my_yy, y_pred))

