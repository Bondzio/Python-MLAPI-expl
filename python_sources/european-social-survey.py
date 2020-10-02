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


from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import os # accessing directory structure
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


df = pd.read_csv('../input/european-social-survey-ess-8-ed21-201617/ESS8e02.1_F1.csv',index_col='name')
df


# In[ ]:


df.info()


# In[ ]:


df['cntry'].unique()


# In[ ]:


df.columns


# In[ ]:


df.head(5)


# In[ ]:


df.tail(5)


# In[ ]:


plt.figure(figsize=(12, 8))
sns.barplot(x=df['cntry'], y=df.ipcrtiv)
plt.xlabel("")
#Human values


# In[ ]:


plt.figure(figsize=(12, 8))
sns.barplot(x=df['cntry'], y=df.inwmms)
plt.xlabel("")
#Administrative variables


# In[ ]:


plt.figure(figsize=(12, 8))
sns.barplot(x=df['cntry'], y=df.pweight)
plt.xlabel("")
#Weights


# In[ ]:


plt.figure(figsize=(12, 8))
sns.barplot(x=df['cntry'], y=df.eneffap)
plt.xlabel("")
 #Climate change


# In[ ]:


plt.figure(figsize=(12, 8))
sns.barplot(x=df['cntry'], y=df.icpart1)
plt.xlabel("")
#Socio-demographics


# In[ ]:


plt.figure(figsize=(12, 8))
sns.barplot(x=df['cntry'], y=df.dfincac)
plt.xlabel("")
#Welfare attitudes


# In[ ]:


plt.figure(figsize=(12, 8))
sns.barplot(x=df['cntry'], y=df.nwspol)
plt.xlabel("")
# social trust


# In[ ]:


sns.scatterplot(x=df['cntry'], y=df['pweight'])
#Weights


# In[ ]:


sns.scatterplot(x=df['cntry'], y=df['inwsmm'])
#Administrative variables

