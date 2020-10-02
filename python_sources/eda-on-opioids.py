#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:





# In[ ]:


df1 = pd.read_csv("../input/Connecticut_Medicare_Part_D_Opioid_Prescriber_Summary_File_2014.csv")


# In[ ]:


df1.head()


# In[ ]:


df2 = pd.read_csv("../input/VSRR_Provisional_Drug_Overdose_Death_Counts copy.csv")


# In[ ]:


df2.head()


# In[ ]:


df3 = pd.read_csv("../input/Opioid_Related_Treatment_Admissions_by_Town_in_Department_of_Mental_Health_and_Addiction_Services_Programs.csv")


# In[ ]:


df3.head()


# In[ ]:


df4 = pd.read_csv("../input/Pharmacies_offering_Narcan__Evzio_and_other_brands_of_Naloxone.csv")


# In[ ]:


df4.head()


# In[ ]:




