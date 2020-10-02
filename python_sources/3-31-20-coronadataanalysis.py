#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


corona_df = pd.read_csv('/kaggle/input/coronadata-33120/time_series_covid19_confirmed_global.csv')


# In[ ]:


corona_df.head()


# In[ ]:


corona_df.drop(columns=['Province/State','Lat','Long'], axis=1, inplace=True)


# In[ ]:


corona_df = corona_df.set_index('Country/Region')


# In[ ]:


country_list = ['Afghanistan','India','Pakistan','Bangladesh','Sri Lanka','Nepal','Bhutan','Maldives']


# In[ ]:


from matplotlib.ticker import MaxNLocator


def plot(x1,Y,label1,label2,plottype):
    ax = plt.figure().gca()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(20,10)
    plt.margins(x=0)
    
    if(plottype == 'multi'):
        for y in Y:
            plt.plot(x1, y)
    else:
        plt.plot(x1,Y)

    plt.xlabel(label1)
    plt.ylabel(label2)
    
    plt.gca().legend(country_list)
    plt.show()


# In[ ]:


def strtodatenum(time_str):
    a = datetime.strptime(time_str, '%m/%d/%y')
    return a


# In[ ]:


def data_list(country_name):
    a = []
    for x in country_name:
        a.append(corona_df.loc[x].tolist())
    return a


# In[ ]:


#timest = corona_df.drop(columns='Country/Region', axis=1)
time_list = list(corona_df.columns.values)


# In[ ]:


time_correct = []
for i in range(0,len(time_list)):
    time_correct.append(strtodatenum(time_list[i]))


# For South Asian Country

# In[ ]:


X1 = time_correct
Y = data_list(country_list)


# In[ ]:


plot(X1,Y,'Date','Confirmed Case','multi')


# Data Analysis India: Before and After Lockdwon

# In[ ]:


india_corona = corona_df.loc['India'].tolist()


# In[ ]:


each_day = [india_corona[0]]
def each_day_case(india):
    for i in range(0,len(india_corona)-1):
        a = india_corona[i+1]-india_corona[i]
        each_day.append(a)
    return each_day


# In[ ]:


each_day_india = each_day_case(india_corona)


# In[ ]:


plot(X1,each_day_india,'Date','Confirmed Case','single')


# In[ ]:


count = 0
for x in X1:
    if(x == strtodatenum('3/24/20')):
        break;
    else:
        count+=1


# India Before Lockdown: Before(24 march)

# In[ ]:


date_unlock = X1[:count]
confirm_unlock = each_day_india[:count]


# In[ ]:


plot(date_unlock,confirm_unlock,'Date','Confirmed Case','single')


# India After Lockdown: After(24 march)

# In[ ]:


date_lock = X1[count:]
confirm_lock = each_day_india[count:]


# In[ ]:


plot(date_lock,confirm_lock,'Date','Confirmed Case','single')


# In[ ]:




