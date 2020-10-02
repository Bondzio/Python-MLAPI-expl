#!/usr/bin/env python
# coding: utf-8

# Importing Data

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

print('Data imported')


# Reading Data

# In[ ]:


train_data = pd.read_csv("../input/forest-cover-type-kernels-only/train.csv.zip")
test_data = pd.read_csv("../input/forest-cover-type-kernels-only/test.csv.zip")
sample_submission = pd.read_csv('../input/forest-cover-type-kernels-only/sample_submission.csv.zip')
sampleSubmission = pd.read_csv('../input/forest-cover-type-kernels-only/sampleSubmission.csv.zip')


# In[ ]:


train_data.head()


# In[ ]:


train_data.describe()


# In[ ]:


sample_submission


# In[ ]:


train_data.Cover_Type.describe()


# In[ ]:


# Plot the effect of Slope
plt.plot(train_data.Slope,train_data.Cover_Type, 'o')
plt.legend()
plt.show()


# In[ ]:


# Plot the effect of Elevation 
plt.plot(train_data.Slope,train_data.Elevation, 'o')
plt.legend()
plt.show()


# In[ ]:


# Plot the effect of Aspect
plt.plot(train_data.Slope,train_data.Aspect, 'o')
plt.legend()
plt.show()


# In[ ]:


# Add a column for direct Distance to Hydrolgy
plus = np.power(train_data['Horizontal_Distance_To_Hydrology'],2) + np.power(train_data['Vertical_Distance_To_Hydrology'],2)
root = np.sqrt(plus)
train_data['Distance_To_Hydrology'] = root


# In[ ]:


train_data['Distance_To_Hydrology']


# In[ ]:


# See relation beween distance to hydrology and CoverType
plt.plot(train_data.Slope,train_data.Distance_To_Hydrology, 'o')
plt.legend()
plt.show()

