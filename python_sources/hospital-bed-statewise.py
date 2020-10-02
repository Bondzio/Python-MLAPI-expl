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


# # importing the dataset

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# # Loading the Dataset

# In[ ]:


statewise = pd.read_csv('../input/hospitals-and-beds-in-india/Hospitals_and_Beds_statewise.csv')
MHD =pd.read_csv('../input/hospitals-and-beds-in-india/Hospitals and Beds maintained by Ministry of Defence.csv')
gov_details = pd.read_csv('../input/hospitals-and-beds-in-india/Number of Government Hospitals and Beds in Rural and Urban Areas .csv')
Insurance =pd.read_csv('../input/hospitals-and-beds-in-india/Employees State Insurance Corporation .csv')
Ayush = pd.read_csv('../input/hospitals-and-beds-in-india/AYUSHHospitals.csv')
Railway = pd.read_csv('../input/hospitals-and-beds-in-india/Hospitals and beds maintained by Railways.csv')
state_wise.shape ,MHD.shape , gov_details.shape ,Insurance.shape ,Ayush.shape, Railway.shape 


# In[ ]:



state_wise.head(5) 


# # Display Maximum beds in which state:-

# In[ ]:


# drop the total rows from the statewise Dataframe
state_wise[state_wise['Name of State']=='Total']
state_wise =state_wise.drop(state_wise.index[[29]])


# In[ ]:


state_wise['No. of beds'].max()


# In[ ]:


state_wise[state_wise['No. of beds']== 4570].iloc[:,1:]


# In[ ]:



plt.figure(figsize=(20,15))
sns.barplot(state_wise['No. of beds'] ,state_wise['Name of State'])


# ## According to graph UP has more no of. Beds in INDIA
# ## According to graph Tripura has less  no of. Beds in INDIA

# # State vs Hospitals

# In[ ]:


plt.figure(figsize=(20,15))
sns.barplot(state_wise['No. of Hospitals'] ,state_wise['Name of State'])


# In[ ]:


combine_details= pd.concat([state_wise ,MHD])
combine_details.shape


# In[ ]:


combine_details[combine_details['Name of State']=='Bihar']


# In[ ]:




