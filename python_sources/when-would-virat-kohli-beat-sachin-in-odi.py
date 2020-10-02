#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import scipy.linalg as la


# **My basic question was:**
# 
# When would Virat Kohli reach the top scorer in ODI Criket?
# 
# As we have Sachin's total run as constant, we could definitely make a comparision between Sachin and Virat Kohli. Let's see what we can do!

# In[ ]:


# Sachin score
sachin_years = np.array([1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012
])
sachin_runs = np.array([239,417,704,319,1089,444,1611,1011,1894,843,1328,904,741,1141,812,412,628,1425,460,972,204,513,315])

# source: http://www.cricmetric.com/playerstats.py?player=SR+Tendulkar&role=all&format=all&groupby=year


# In[ ]:


def show_plot(years, runs, title):

    plt.rcParams["figure.figsize"] = (20,3)    
    plt.plot(years, runs)
    plt.grid(True)
    plt.xticks(years)
    plt.title(title)
    plt.show()


# In[ ]:


show_plot(sachin_years, sachin_runs, 'Sachin Runs')


# In[ ]:


# Virat score

virat_years = np.array([2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019])
virat_runs = np.array([159,328,995,1382,1028,1268,1054,623,739,1473,1172,1429])

# source: http://www.cricmetric.com/playerstats.py?player=V%20Kohli&format=all&role=all


# In[ ]:


show_plot(virat_years, virat_runs, 'Virat Runs')


# In[ ]:


np.amax(virat_runs)   


# In[ ]:


# Compute the linear model
def compute_linear_model(years, runs, title):
    
    X = np.column_stack([np.ones(len(years)), years])
    
    a = la.solve(X.T @ X, X.T @ runs)

    model = a[0] + a[1] * years

    plt.plot(years, model, years, runs, 'b.', ms = 15)
    plt.title(title)
    plt.ylim([0, np.amax(runs) + 500])
    plt.grid(True)
    plt.show()


# In[ ]:


compute_linear_model(virat_years, virat_runs, 'Virat Runs')


# In[ ]:


sachin_total_runs = np.sum(sachin_runs)
virat_total_runs = np.sum(virat_runs)


# In[ ]:


sachin_total_runs


# In[ ]:


virat_total_runs


# In[ ]:


def show_future_runs(years, runs):
    
    # extrapolate to future years
    
    X = np.column_stack([np.ones(len(years)), years])
    #print(X)

    a = la.solve(X.T @ X, X.T @ runs)

    future_years = np.array([2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
    future_runs = (a[0] + a[1] * future_years)
    
    total_runs = np.sum(runs) + np.cumsum(future_runs)
    sachin = sachin_total_runs * np.ones(len(future_years))
    
    plt.plot(future_years, total_runs, future_years, sachin)
    plt.grid(True)
    plt.xticks(future_years)
    plt.title('Virat Total Points Prediction')
    plt.show()


# In[ ]:


show_future_runs(virat_years, virat_runs)


# It seems, Virat Kohli will reach the top in ODI runs in 2023! Let's wait and see whether prediction will work. 

# Sources:
# 
# http://www.cricketweb.net/statsspider/player/graph/905006-ODI-13.php
# http://www.cricmetric.com/playerstats.py?player=SR+Tendulkar&role=all&format=all&groupby=year
# 
# http://www.cricmetric.com/playerstats.py?player=V%20Kohli&format=all&role=all
# 
# https://www.jagranjosh.com/general-knowledge/cricketers-who-have-scored-10000-runs-in-odi-1499859286-1
# 
# Analysis inspired from:
# 
# https://www.math.ubc.ca/~pwalls/math-python/linear-algebra/applications/
# 

# **KPS (Kaggle Post Script):**
# 
# Still, I need to clean the code up. However, feel free to fork and play around. Also, if you find any issues/improvements, please let me know. I would be happy to learn from others.

# In[ ]:




