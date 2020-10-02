#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


meningitis_dataframe = pd.read_csv('../input/meningitis_dataset.csv', delimiter=',')
nRow, nCol = meningitis_dataframe.shape
print("Dataset consists of [", nRow, "] Rows and [", nCol, "] Columns")


# In[ ]:


meningitis_dataframe.head()


# In[ ]:


meningitis_dataframe.describe()


# In[ ]:


meningitis_dataframe.info()


# In[ ]:


p_alive, p_dead,P_alive = meningitis_dataframe.groupby('health_status').size()
p_alive=p_alive+P_alive
meningitis_dataframe.groupby('health_status').size()


# In[ ]:


print(p_alive, "Dead Patients and ", p_dead, "Patients Alive")


# In[ ]:


p_confirmed,p_unconfirmed, P_confirmed = meningitis_dataframe.groupby('report_outcome').size()
p_confirmed = P_confirmed + p_confirmed
meningitis_dataframe.groupby('report_outcome').size()


# In[ ]:


print(p_unconfirmed, "Clinically Unconfirmed Cases and", p_confirmed, "Clinically Confirmed Cases")


# In[ ]:


m_NmA,m_NmC, m_NmW, m_Null, m_null = meningitis_dataframe.groupby('serotype').size()
m_null = m_Null + m_null
meningitis_dataframe.groupby('serotype').size()


# In[ ]:


print(m_NmA, "Neisseria meningitidis group A (NmA) Records,", m_NmC, "Neisseria meningitidis group C (NmC) Records,", m_NmW, "Neisseria meningitidis group W (NmW) Records, and", m_null, "Non Meningitis Records")


# In[ ]:


m_female, m_male =meningitis_dataframe.groupby('gender').size()
meningitis_dataframe.groupby('gender').size()


# In[ ]:


print(m_female, "Female Patients and ", m_male, "Male Patients")


# In[ ]:


m_cholera, m_diarrohea, m_ebola, m_malaria, m_marburg, m_measles, m_meningitis, m_rubella, m_viral_fever, m_yellow_fever =meningitis_dataframe.groupby('disease').size()
meningitis_dataframe.groupby('disease').size()


# In[ ]:


print(m_cholera, "Choleara Patients,", m_diarrohea, "Diarrhoea Patients,", m_ebola, "Ebola Patients,", m_malaria, "Malaria Patients,", m_marburg, "Marburg Virus Patients,", m_measles, "Measles Patients,", m_meningitis,"Meningitis Patients,", m_rubella,"Rubella Mars Patients,", m_viral_fever,"Viral Haemmorhaphic Fever,", m_yellow_fever, "Yellow Fever Patients")


# In[ ]:


meningitis_dataframe.groupby('state').size()


# In[ ]:


meningitis_dataframe.groupby('settlement').size()


# In[ ]:


meningitis_dataframe.groupby('age').size()


# In[ ]:


meningitis_dataframe.groupby('report_year').size()


# plt.figure(figsize=(120,80)
# sns.pairplot(meningitis_dataframe, hue='gender', size=3, aspect=1)
# plt.show()

# In[ ]:


meningitis_dataframe.hist(figsize=(120,80))
plt.show()


# In[ ]:


meningitis_dataframe.hist(edgecolor='black', linewidth=1.2, figsize=(120,80))
plt.show()


# In[ ]:


plt.figure(figsize=(60,40))
plt.subplot(2,2,1)
sns.violinplot(x='age', y='gender', data=meningitis_dataframe)
plt.show()


# In[ ]:


meningitis_dataframe.boxplot(by='age', figsize=(120,80))
plt.show()


# In[ ]:


pd.plotting.scatter_matrix(meningitis_dataframe, figsize=(12,8))
plt.show()


# In[ ]:




