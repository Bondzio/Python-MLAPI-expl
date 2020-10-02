#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# This is the workbook component of the "Indexing, selecting, assigning" section. For the reference component, [**click here**](https://www.kaggle.com/residentmario/indexing-selecting-assigning-reference).
# 
# Selecting specific values of a `pandas` `DataFrame` or `Series` to work on is an implicit step in almost any data operation you'll run, so one of the first things you need to learn in working with data in Python is how to go about selecting the data points relevant to you quickly and effectively.
# 
# In this set of exercises we will work on exploring the [Wine Reviews dataset](https://www.kaggle.com/zynicide/wine-reviews). 
# 
# # Relevant Resources
# * **[Quickstart to indexing and selecting data](https://www.kaggle.com/residentmario/indexing-and-selecting-data/)** 
# * [Indexing and Selecting Data](https://pandas.pydata.org/pandas-docs/stable/indexing.html) section of pandas documentation
# * [Pandas Cheat Sheet](https://assets.datacamp.com/blog_assets/PandasPythonForDataScience.pdf)
# 
# 
# 

# # Set Up
# **Fork this notebook using the button towards the top of the screen.**
# 
# Run the following cell to load your data and some utility functions

# In[2]:


import pandas as pd
import seaborn as sns
from learntools.advanced_pandas.indexing_selecting_assigning import *

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)
pd.set_option("display.max_rows", 5)


# Look at an overview of your data by running the following line

# In[3]:


reviews.head()


# # Checking Answers
# 
# You can check your answers in each of the exercises that follow using the  `check_qN` function provided in the code cell above (replacing `N` with the number of the exercise). For example here's how you would check an incorrect answer to exercise 1:

# In[4]:


check_q1(pd.DataFrame())


# For the first set of questions, if you use `check_qN` on your answer, and your answer is right, a simple `True` value will be returned.
# 
# For the second set of questions, using this function to check a correct answer will present you will an informative graph!
# 
# If you get stuck, use `answer_qN` function to print the answer outright.

# # Exercises

# **Exercise 1**: Select the `description` column from `reviews`.

# In[5]:


reviews.info()


# In[6]:


reviews['description'].head(5)


# **Exercise 2**: Select the first value from the description column of `reviews`.

# In[7]:


reviews['description'].head(1)


# **Exercise 3**: Select the first row of data (the first record) from `reviews`. Hint: from this exercise onwards I strongly recommend using `loc` or `iloc`.

# In[8]:


reviews.loc[0]


# **Exercise 4**: Select the first 10 values from the `description` column in `reviews`. Hint: format your output as a `pandas` `Series`.

# In[19]:


reviews.loc[0:9, 'description']


# **Exercise 5**: Select the records with the `1`, `2`, `3`, `5`, and `8` row index positions. In other words, generate the following`DataFrame`:
# 
# ![](https://i.imgur.com/sHZvI1O.png)

# In[20]:


pd.DataFrame(reviews.loc[[1, 2, 3, 5, 8]])


# **Exercise 6**: Select the `country`, `province`, `region_1`, and `region_2` columns of the records with the `0`, `1`, `10`, and `100` index positions. In other words, generate the following `DataFrame`:
# 
# ![](https://i.imgur.com/FUCGiKP.png)

# In[11]:


reviews.loc[[0, 1, 10, 100], ['country', 'province', 'region_1', 'region_2']]


# **Exercise 7**: Select the `country` and `variety` columns of the first 100 records. 
# 
# Hint: you may use `loc` or `iloc`. When working on the answer this question and the several of the ones that follow, keep the following "gotcha" described in the [reference](https://www.kaggle.com/residentmario/indexing-selecting-assigning-reference) for this tutorial section:
# 
# > `iloc` uses the Python stdlib indexing scheme, where the first element of the range is included and the last one excluded. So `0:10` will select entries `0,...,9`. `loc`, meanwhile, indexes inclusively. So `0:10` will select entries `0,...,10`.
# 
# > [...]
# 
# > ...[consider] when the DataFrame index is a simple numerical list, e.g. `0,...,1000`. In this case `df.iloc[0:1000]` will return 999 entries, while `df.loc[0:1000]` return 1000 of them! To get 1000 elements using `iloc`, you will need to go one higher and ask for `df.iloc[0:1001]`.

# In[14]:


reviews.loc[0:100, ['country', 'variety']]


# **Exercise 8**: Select wines made in `Italy`. Hint: `reviews.country` equals what?

# In[74]:


reviews[reviews['country'] == 'Italy']


# **Exercise 9**: Select wines whose `region_2` is not `NaN`.

# In[81]:


reviews['region_2'] == 'NaN'


# The remaining exercises are visual.

# **Exercise 10**: <!--What is the distribution of wine ratings assigned by Wine Magazine?--> Select the `points` column.

# In[21]:


reviews['points']


# **Exercise 11**: <!--What is the distribution of reviews scores for the first 1000 wines in the dataset?--> Select the `points` column for the first 1000 wines.

# In[22]:


reviews.loc[0:1000, 'points']


# **Exercise 12**: <!--What is the distribution of reviews scores for the last 1000 wines in the dataset?--> Select the `points` column for the last 1000 wines.

# In[25]:


reviews['points'].tail(1000)


# 
# **Exercise 13**: <!--What is the distribution of reviews scores for wines made in Italy?--> Select the `points` column, but only for wines made in Italy.

# In[ ]:


# Your code here


# **Exercise 14**: Who produces more above-averagely good wines, France or Italy? Select the `country` column, but only  when said `country` is one of those two options, _and_ the `points` column is greater than or equal to 90.
# 
# Your output should look roughly like this:
# ```
# 119       France
# 120        Italy
#            ...  
# 129969    France
# 129970    France
# Name: country, Length: 15840, dtype: object
# ```

# In[ ]:


# Your code here


# ## Keep going
# 
# Move on to the [**Summary functions and maps workbook**](https://www.kaggle.com/residentmario/summary-functions-and-maps-workbook).
