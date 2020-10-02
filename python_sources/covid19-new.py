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





# In[ ]:


import pandas as pd
patient = pd.read_csv("../input/coronavirusdataset/patient.csv")
route = pd.read_csv("../input/coronavirusdataset/route.csv")
time = pd.read_csv("../input/coronavirusdataset/time.csv")


# In[ ]:


patient.head()


# In[ ]:


import seaborn as sns


# In[ ]:


sns.scatterplot(x= patient['birth_year'], y = patient['infection_order'] )


# In[ ]:


sns.pairplot(patient)


# In[ ]:




sns.distplot(patient['infection_order'])


# In[ ]:


patient = patient.drop('infected_by', axis = True)


# In[ ]:


patient.head()


# In[ ]:


patient = patient.drop('patient_id', axis =1)


# In[ ]:


patient.head(10)


# In[ ]:


patient.info()


# In[ ]:


sns.scatterplot(x= 'infection_order' ,y ='birth_year', data = patient)


# In[ ]:


sns.countplot(patient['sex'])


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(30,25))
sns.countplot(patient['region'])


# In[ ]:




