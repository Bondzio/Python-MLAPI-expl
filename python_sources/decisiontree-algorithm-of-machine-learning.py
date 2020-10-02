#!/usr/bin/env python
# coding: utf-8

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


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv('/kaggle/input/titanicdataset-traincsv/train.csv')
pd.set_option('Display.max_columns', 12)


# In[ ]:


df.head()


# In[ ]:


df.drop(['PassengerId' , 'Name' , 'SibSp' , 'Parch' , 'Ticket' , 'Cabin' , 'Embarked'] , axis = 1 , inplace = True)


# In[ ]:


df.dropna(axis = 'index' , how = 'any' , inplace = True)


# In[ ]:


from sklearn.preprocessing import LabelEncoder


# In[ ]:


labelencoder = LabelEncoder()


# In[ ]:


df['Sex'] = labelencoder.fit_transform(df['Sex']) 


# In[ ]:


inputs = df[['Pclass' , 'Sex' , 'Age' , 'Fare']]
target = df['Survived']


# In[ ]:


from sklearn import tree


# In[ ]:


Dec_tree = tree.DecisionTreeClassifier()


# In[ ]:


Dec_tree.fit(inputs , target)


# In[ ]:


Dec_tree.predict([[1,0,19,30]])


# In[ ]:


Dec_tree.score(inputs , target)


# In[ ]:


# This is the DecisionTree model for this titanic data set to predict the survival from the incident..hit the like..ThankYou 


# In[ ]:




