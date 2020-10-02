#!/usr/bin/env python
# coding: utf-8

# I had taken part in the Kaggle survey.So I am personally interested to  find out the outcome of this survey.Datascience is considered as the sexiest job of 21st century.We will try to see what makes it so sexy.If you like my work please do vote

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


# **Importing python modules **

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import warnings 
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
warnings.filterwarnings('ignore')
plt.style.use('fivethirtyeight')


# In[ ]:


data=pd.read_csv('../input/multipleChoiceResponses.csv')
data.head()


# In[ ]:


data=data.drop(data.index[0])
#data.head()


# In[ ]:


data = data.rename(columns={'Time from Start to Finish (seconds)': 'Time','Q1':'Gender','Q1_OTHER_TEXT':'What is your gender? - Prefer to self-describe - Text','Q2':'Age','Q3':'Country','Q4':'Highest_Degree','Q5':'Specilization','Q6':'Job_Title','Q7':'Industry','Q8':'Experience','Q9':'Annual_Salary'})
data.head()


# **Time to complete Survey**

# In[ ]:


print("Maximum time taken to complete survey",(data['Time'].astype('int')/60).max(),"mins")
print("Minimum time taken to complete survey",(data['Time'].astype('int')/60).min(),'mins')
print("Minimum time taken to complete survey",(data['Time'].astype('int')/60).mean(),'mins')
print("Minimum time taken to complete survey",(data['Time'].astype('int')/60).median(),'mins')


# The maximun and minimun times are outliers.
# 
# Mean also doesnt give correct impression about time needed to complete the Survey.
# 
# Median of 17.01 mins is correct value of approximate time needed by people to ccomplete this Kaggle survey.

# In[ ]:


data['mins']=data['Time'].astype('int')/60  #Converting time for completing survey from seconds into minutes
plt.hist(data[data['mins']<100].mins,bins=30,edgecolor='black',linewidth=1.2)
plt.title('Time to completing survey in mins')
plt.gcf().set_size_inches(10,5)


# We can see from the above distribution that most people complete the survey in less than 20 min.As observed before the median time to complete the survey was 17 min.

# **Gender distribution in area of Data Science**

# In[ ]:


ax=data['Gender'].value_counts().plot.barh(width=0.9,color='#ffd700')
for i,v in enumerate(data['Gender'].value_counts().values):
    ax.text(200,i,v,fontsize=12,color='blue',weight='bold')
plt.title('Gender Distribution')
plt.gcf().set_size_inches(8,5)
plt.show()


# In[ ]:




