#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# ### Have you ever wondered what if summary statistics is more just a simple summary? 
# 
# ##Introducing, **pandas_profiling** for simple and fast exploratory data analysis of a Pandas Datafram

# Exploratory Data Analysis (EDA) plays a very important role in understanding the dataset. Whether you are going to build a Machine Learning Model or if it's just an exercise to bring out insights from the given data, EDA is the primary task to perform. While it's undeniable that EDA is very important, The task of performing Exploratory Data Analysis grows in parallel with the number of columns your dataset has got. 
# 
# For ex: Assume you've got a dataset with 10 rows x 2 columns. It's very simply to specify those two column names separately and plot all the required plots to perform EDA. Alternatively, If the dataset has got 20 columns, you've to repeat the same above exercise for another 10 times. Now, there's another layer of complexity because the visualization that you choose for a `continuous variable` and `categorical variable` is different, hence the type of the plot changes when the data type changes. 
# 
# Given all these conditions, EDA sometimes becomes a tedious task - but remember it's all driven by a set of rules - like plot `boxplot` and `histogram` for a continous variable, Measure `missing values`, Calculate `frequency` if it's categorical variable - thus giving us opportunity to automate things. That's the base of this python module `pandas_profiling` that helps one in automating the first-level of EDA. 

# From their github page:
# 
# For each column the following statistics - if relevant for the column type - are presented in an interactive HTML report:
# 
# * **Essentials**:  type, unique values, missing values
# * **Quantile statistics** like minimum value, Q1, median, Q3, maximum, range, interquartile range
# * **Descriptive statistics** like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
# * **Most frequent values**
# * **Histogram**
# * **Correlations** highlighting of highly correlated variables, Spearman and Pearson matrixes

# In[ ]:


get_ipython().run_cell_magic('capture', '', 'import numpy as np # linear algebra\nimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\nimport pandas_profiling as pp\n\n# Input data files are available in the "../input/" directory.\n# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory\n\nimport os\nprint(os.listdir("../input"))\n\n# Any results you write to the current directory are saved as output.')


# **Loading Training Dataset**

# In[ ]:


train = pd.read_csv("../input/train.csv", encoding='UTF-8', parse_dates = ['project_submitted_datetime'])


# The primariy objective of this Kernel is to introduce this amazing Python Module `pandas_profiling` that does an excellent job in aiding you perform a simple quick **EDA**. You can refer more about this module here on github: [https://github.com/pandas-profiling/pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)

# In[ ]:


pp.ProfileReport(train)


# In[ ]:


resources = pd.read_csv("../input/resources.csv", encoding='UTF-8')


# **Exploring `resources` Data**

# In[ ]:


pp.ProfileReport(resources)

