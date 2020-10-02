#!/usr/bin/env python
# coding: utf-8

# ### Please help by upvoting this kernel if you feel useful. 

# This note book will guide you quickly for the neccesary funtions to use in data science.
# 
# # Contents
# 
# 1. [Numpy(Numerical Python)](#Numpy)
#     1. [Basic operations](#BasicOperation)
#     2. [Array creation](#creation)
#     3. [Indexing & Slicing](#slicing)
# 2. [Pandas](#Pandas)
#     1. [Data Structures](#DataStructures)
#        1. [Series](#Series)
#        2. [Data Frame](#DataFrames)
#     2. [Handle Missing Data](#MissingDataHandle)
#         1. [Drop missing data](#dropna)
#         2. [Fill missing data](#fillna)
#     3. [Data Operations](#DataOperations)
#         1. [Custom functions(applymap)](#CustomFunction)
#         2. [Statistical functions(max,mean,std)](#StatFunction)
#         3. [Grouping(groupby)](#groupby)
#         4. [Sorting(sort_values)](#Sorting)        
# 3. [matplotlib](#matplotlib)
#     1. [Basic Plot](#basicplot)
#     2. [Multiple plots](#MultiplePlots)
#     3. [Subplots](#Subplots)
#     4. [Properties](#Properties)
#         1. [Alpha](#Alpha)
#         2. [Annotation](#Annotation)
#     5. [Types of plots](#Types)
#         1. [histogram](#histogram)
#         2. [scatter](#scatter)
#         3. [heatmap](#heatmap)
#         3. [pie](#pie)
#         4. [errorbar](#errorbar)

# ## 1) Numpy(Numerical Python)[^](#Numpy)<a id="Numpy" ></a><br>

# is a library consisting of multidimensional array objects and a collection of routines for processing those arrays. Using NumPy, mathematical and logical operations on arrays can be performed.

# In[ ]:


#First we need to import the numpy library
import numpy as np # linear algebra


# ### 1) Basic operations[^](#BasicOperation)<a id="BasicOperation" ></a><br>

# In[ ]:


#1) Create arrays
data = np.array([[1, 2], [3, 4]])  # create 2D array
print(data)
data_complex = np.array([1, 2, 3], dtype = complex) 
print(data_complex)
#2) see datatype
print(np.dtype(np.int64)) 
print(np.dtype('i1')) #int8=i1, int16=i2, int64=i4
#3) shape
print(data.shape)
#4) arange
data_arange = np.arange(15) #one dimentional array
print(data_arange)
#5) reshape, change shape
reshaped = data_arange.reshape((3,5))
print(reshaped.shape)
#6) itemsize : length of each element of array in bytes
print(reshaped.itemsize)


# ### 2) Array creations[^](#creation)<a id="creation" ></a><br>

# In[ ]:


#1) empty : array of random values (not initialized)
empty = np.empty([2,3]) #Default dtype is float
print(empty) 
#2) zeros : 
zeros = np.zeros([2,3], dtype = int)
print(zeros)
#3) ones : 
ones = np.ones([2,3], dtype = int)
print(ones)
#4) create based on exising list
list_data = [1,2,3] 
np_data = np.asarray(list_data)
print(np_data)
#5) create based on exising tuple
tuple_data = (1,2,3,5) 
np_data_tuple = np.asarray(tuple_data)
print(np_data_tuple)
#6) from buffer
str_data = 'String date'.encode()
np_str = np.frombuffer(str_data, dtype = 'S1') 
print(np_str)
#7) range func
range_data = np.asarray(range(5))
print(range_data)
#8) linspace : eg -> linspace(start, stop, num, endpoint, retstep, dtype)
linspace_data = np.linspace(10,20,5) 
print(linspace_data)
linspace_data_1 = np.linspace(1,2,5, retstep = True)
print(linspace_data_1)
#9) logspace : numbers that are evenly spaced on a log scale (numpy.logspace(start, stop, num, endpoint, base, dtype)) 
log_data = np.logspace(1.0, 2.0, num = 10) 
print(log_data)


# ### 3) Indexing & Slicing[^](#slicing)<a id="slicing" ></a><br>

# In[ ]:


#1) slice :  slice(start:stop:step) 
data = np.arange(10) 
sliced = slice(2,7,2) 
print(data)
print(data[sliced])
#2) same above with array with colon
data = np.arange(10) 
sliced_index = data[2:7:2]
print(sliced_index)
#3) few indexed operations
data = np.array([[1,2,3],[3,4,5],[4,5,6]]) 
print('Original array is:') 
print(data)   
# this returns array of items in the second column 
print('The items in the second column are:')  
print(data[...,1]) 
# Now we will slice all items from the second row 
print('The items in the second row are:') 
print(data[1,...]) 
# Now we will slice all items from column 1 onwards 
print('The items column 1 onwards are:') 
print(data[...,1:])


# ## 2) Pandas[^](#Pandas)<a id="Pandas" ></a><br>

# ### 1) Data Structures[^](#DataStructures)<a id="DataStructures" ></a><br>
# 
# 1. Series - labled 1D array
# 2. Data Frames - 
# 3. Panel - 3 dimensional
# 4. Panel 4D - 4 dimensional

# In[ ]:


#First we need to import the pandas library
import pandas as pd
import numpy as np


# #### 1) Series(One dimentinal array)[^](#Series)<a id="Series" ></a><br>

# In[ ]:


#### 1) Series(One dimentinal array)[^](#Series)<a id="Series" ></a><br>###Create Series
#1) list
list_series = pd.Series(list('abcdef'))
print(list_series)
#2) ndarray
arr_series = pd.Series(np.array(["one","two"]))
print(arr_series)
#3) dict
dict_series = pd.Series([120,230],index=["one","two"])
print(dict_series)
#4) scalar
scalar_series = pd.Series(3.,index=["a","b","c"])
print(scalar_series)


# In[ ]:


#### Access data of a series
print(dict_series[1])  # index
print(scalar_series[0:1]) # index range
print(dict_series.loc['one']) # index name
print(list_series.iloc[2]) # index position


# #### 2) Data Frame(Two dimentinal array)[^](#DataFrame)<a id="DataFrame" ></a><br>
# like a spread sheet

# In[ ]:


###Create Data Frames
#1) list
data_list = {'city':["London","Sydney"],'year':[2001,2005]}
list_df = pd.DataFrame(data_list)
print(list_df)
#2) dict
dict_data = {'London':{2001:100},'Sydney':{2005:200}}
dict_df = pd.DataFrame(dict_data)
print(dict_df)
#3) Series
series_data = pd.Series([120,230],index=["one","two"])
series_df = pd.DataFrame({'value':series_data})
print(series_df)
#4) narray
array_data = np.array([2001,2005,2006])
arr_df = pd.DataFrame({'year':array_data})
print(arr_df)
#4) dataframe
df_data = pd.DataFrame({'year':array_data})
df_df = pd.DataFrame(array_data)
print(df_df)


# In[ ]:


#Using above data frames 
#View Data
print(list_df.city) # specific column
list_df.describe # whole dataset 
print(arr_df.head(1)) #top records 
print(arr_df.index) #list indexs
print(dict_df.columns)  #list columns
print(list_df['year'])  #specific column by name give column
print(dict_df.loc[2001])  #view by key gives row
print(dict_df.iloc[0:1])  #view by index gives rows
print(dict_df.iat[1,1])  #view by index gives value
print(list_df[list_df['year']>2003])  #view by condition, column greater than a value


# * ### 2) Handle Missing Data[^](#MissingDataHandle)<a id="MissingDataHandle" ></a><br>

# #### 1) Drop missing data[^](#dropna)<a id="dropna" ></a><br>

# In[ ]:


import pandas as pd
df = pd.DataFrame({'col1':{2001:100,2002:300},'col2':{2002:200}})
print("df : \n",df)
df_droped  = df.dropna()
print("droped df : \n",df_droped)


# #### 2) Fill missing data[^](#fillna)<a id="fillna" ></a><br>

# In[ ]:


import pandas as pd
df = pd.DataFrame({'col1':{2001:100,2002:300},'col2':{2002:200}})
print("df : \n",df)
df_filled  = df.fillna(0)
print("filled df : \n",df_filled)


# ### 2) Data Operations[^](#DataOperations)<a id="DataOperations" ></a><br>

# #### 1) Custom Function(applymap)[^](#CustomFunction)<a id="CustomFunction" ></a><br>

# In[ ]:


import pandas as pd
df_movie_rating = pd.DataFrame({'movie 1':[5,4,3,3,2,1],'movie 2':[4,2,1,2,3,5]},
                              index=['Tom','Jeff','Pterm','Ann','Ted','Paul'])
df_movie_rating


# In[ ]:


def movie_grade(rating):
    if rating==5:
        return 'A'
    if rating==4:
        return 'B'
    if rating==3:
        return 'C'
    else:
        return 'F'

print(movie_grade(4))

df_movie_rating.applymap(movie_grade)


# #### 2) Statistical functions(max,mean,std)[^](#StatFunction)<a id="StatFunction" ></a><br>

# In[ ]:


import pandas as pd
df_test_scores = pd.DataFrame({'test 1':[98,89,34,23,45],'test 2':[23,34,50,76,80]}
                            ,index=['Sam','Ann','Tom','Fed','Jef'])
df_test_scores


# In[ ]:


print("max : ",df_test_scores.max())
print("min : ",df_test_scores.min())
print("mean : ",df_test_scores.mean())
print("std : ",df_test_scores.std())


# #### 3) Grouping (groupby)[^](#groupby)<a id="groupby" ></a><br>

# In[ ]:


df_names = pd.DataFrame({'first':['George','Bill','Ronald','Jimmy','George'],
                        'last':['Bush','Clienton','Regon','Carter','Washington']})
df_names


# In[ ]:


df_names_grouped = df_names.groupby('first')
df_names_grouped.get_group('George')


# #### 4) Sorting (sort_values)[^](#Sorting)<a id="Sorting" ></a><br>

# In[ ]:


df_names.sort_values('first') # indexes will remain same unless you are re indexing


# ## 3) matplotlib[^](#matplotlib)<a id="matplotlib" ></a><br>

# ### 1) Basic plot[^](#basicplot)<a id="basicplot" ></a><br>

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
get_ipython().run_line_magic('matplotlib', 'inline')
randomNumbers = np.random.rand(10)
print(randomNumbers)
style.use('ggplot')
plt.plot(randomNumbers,'g',label='line one',linewidth=2)
plt.xlabel('Range')
plt.ylabel('Numbers')
plt.title('Random number plot')
plt.legend()
plt.show()


# ### 2) Multiple plots[^](#MultiplePlots)<a id="MultiplePlots" ></a><br>

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
get_ipython().run_line_magic('matplotlib', 'inline')
web_customers_monday = [12,34,5,232,232,232,53,5,64,34]
web_customers_tuesday = [3,23,12,21,500,54,34,65,87,92]
web_customers_wednesday = [32,82,23,22,332,242,153,73,12,23]
time_hrs = [2,4,6,7,8,10,12,15,18,20]
style.use('ggplot')
plt.plot(time_hrs,web_customers_monday,'r',label='monday',linewidth=1)
plt.plot(time_hrs,web_customers_tuesday,'g',label='tuesday',linewidth=1.2)
plt.plot(time_hrs,web_customers_wednesday,'b',label='wednesday',linewidth=1.5)
plt.title('Web site traffic')
plt.xlabel('Hrs')
plt.ylabel('Number of users')
plt.legend()
plt.show()


# ### 3) Sub plots[^](#Subplots)<a id="Subplots" ></a><br>

# In[ ]:


#subplot(row,cloum,position)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
get_ipython().run_line_magic('matplotlib', 'inline')
web_customers_monday = [12,34,5,232,232,232,53,5,64,34]
web_customers_tuesday = [3,23,12,21,500,54,34,65,87,92]
web_customers_wednesday = [32,82,23,22,332,242,153,73,12,23]
time_hrs = [2,4,6,7,8,10,12,15,18,20]
style.use('ggplot')
plt.figure(figsize=(8,4))
plt.subplots_adjust(hspace=1,wspace=1)
plt.subplot(2,2,1)
plt.title('Monday')
plt.plot(time_hrs,web_customers_monday,'r',label='monday',linewidth=1,linestyle='-')
plt.subplot(2,2,2)
plt.title('Tuesday')
plt.plot(time_hrs,web_customers_tuesday,'g',label='tuesday',linewidth=1.2)
plt.subplot(2,2,3)
plt.title('Wednesday')
plt.plot(time_hrs,web_customers_wednesday,'b',label='wednesday',linewidth=1.5)
plt.xlabel('Hrs')
plt.ylabel('Number of users')
plt.show()


# ### 4) Properties [^](#Properties)<a id="Properties" ></a><br>
# 
# Line properties
# 1. alpha
# 2. animated
# 
# Plot graphics
# 1. line style
# 2. line width
# 3. marker style

# #### 1) Alpha [^](#Alpha)<a id="Alpha" ></a><br>

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
get_ipython().run_line_magic('matplotlib', 'inline')
web_customers = [12,34,5,232,232,232,53,5,64,34]
time_hrs = [2,4,6,7,8,10,12,15,18,20]
style.use('ggplot')
plt.plot(time_hrs,web_customers,alpha=0.4)
plt.title('Web site traffic')
plt.xlabel('Hrs')
plt.ylabel('Number of users')
plt.show()


# #### 2) Annotation [^](#Annotation)<a id="Annotation" ></a><br>

# In[ ]:


import matplotlib.pyplot as plt
from matplotlib import style
get_ipython().run_line_magic('matplotlib', 'inline')
#Alpha for line transparency
web_customers = [12,34,10,232,200,180,53,5,64,34]
time_hrs = [2,4,6,7,8,10,12,15,18,20]
style.use('ggplot')
plt.plot(time_hrs,web_customers,alpha=0.7)
plt.title('Web site traffic')
plt.xlabel('Hrs')
plt.ylabel('Number of users')
#plt.annotate('annotation text','ha=horizontal align',va='vertical align',xytext=text position,
#xy=arrow position,arrowprops=properties of arrow)
plt.annotate('Max',ha='center',va='bottom',xytext=(5,232),xy=(7,232),arrowprops={'facecolor':'green'})
plt.annotate('Min',ha='center',va='bottom',xytext=(13,5),xy=(15,5),arrowprops={'facecolor':'green'})

plt.show()


# ### 1) Types of plots (types)[^](#Types)<a id="Types" ></a><br>
# 
# 1. Histogram
# 2. Heat Map
# 3. Scatter Plot
# 4. Pie Chart
# 5. Error Bar

# #### 1) Histogram (histogram)[^](#histogram)<a id="histogram" ></a><br>

# In[ ]:


#Histogram
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
from matplotlib import style
get_ipython().run_line_magic('matplotlib', 'inline')

bostan_real_state_data = load_boston()
#print(bostan_real_state_data.DESCR)
x_axis = bostan_real_state_data.data
y_axis = bostan_real_state_data.target
style.use('ggplot')
plt.figure(figsize=(8,8))
plt.hist(y_axis,bins=50)
plt.xlabel('price')
plt.ylabel('number of houses')
plt.show()


# #### 2) Scatter (scatter)[^](#scatter)<a id="scatter" ></a><br>

# In[ ]:


#Scatter plot
style.use('ggplot')
plt.figure(figsize=(6,6))
plt.scatter(x_axis[:,5],y_axis)
plt.show()


# #### 3) Heat Map (heatmap)[^](#heatmap)<a id="heatmap" ></a><br>

# In[ ]:


#Heat Map
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

flight_data = sns.load_dataset('flights')
#flight_data.head()
flight_data = flight_data.pivot('month','year','passengers')
sns.heatmap(flight_data)


# #### 4) Pie chart (pie)[^](#pie)<a id="pie" ></a><br>
# 

# In[ ]:


#Pie Charts
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

job_data = ['40','20','12','23','15']
labels = ['IT','Finace','marketing','Admin','HR']
explode = (0.05,0.04,0,0,0)  #spilit the chart
#autopct= percent value embedded
plt.pie(job_data,labels=labels,explode=explode,autopct='%1.1f%%',startangle=70)
plt.axis('equal') # equal size chart
plt.show()


# #### 5) Error bar (errorbar)[^](#errorbar)<a id="errorbar" ></a><br>
# 
# Error bars use mainly to identify errors
# 

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt

# example data
x = np.arange(0.1, 4, 0.5)
y = np.exp(-x)

# example variable error bar values
yerr = 0.1 + 0.2*np.sqrt(x)
xerr = 0.1 + yerr

# First illustrate basic pyplot interface, using defaults where possible.
plt.figure()
plt.errorbar(x, y, xerr=0.2, yerr=0.4)
plt.title("Simplest errorbars, 0.2 in x, 0.4 in y")
plt.show()

