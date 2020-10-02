#!/usr/bin/env python
# coding: utf-8

# # Python for Data 7: Dictionaries and Sets
# [back to index](https://www.kaggle.com/hamelg/python-for-data-analysis-index)

# Sequence data types like lists, tuples and strings are ordered. Ordering can be useful in some cases, such as if your data is sorted or has some other natural sense of ordering, but it comes at a price. When you search through sequences like lists, your computer has to go through each element one at a time to find an object you're looking for.
# 
# Consider the following code:

# In[1]:


my_list = [1,2,3,4,5,6,7,8,9,10]

0 in my_list


# When running the code above, Python has to search through the entire list, one item at a time before it returns that 0 is not in the list. This sequential searching isn't much of a concern with small lists like this one, but if you're working with data that contains thousands or millions of values, it can add up quickly.
# 
# Dictionaries and sets are unordered Python data structures that solve this issue using a technique called [hashing](https://en.wikipedia.org/wiki/Hash_function). We won't go into the details of their implementation, but dictionaries and sets let you check whether they contain objects without having to search through each element one at a time, at the cost of having no order and using a bit more system memory.

# ## Dictionaries

# A [dictionary](https://docs.python.org/3.7/tutorial/datastructures.html#dictionaries) or dict is an object that maps a set of named indexes called keys to a set of corresponding values. Dictionaries are mutable, so you can add and remove keys and their associated values. A dictionary's keys must be immutable objects, such as ints, strings or tuples, but the values can be anything.
# 
# Create a dictionary with a comma-separated list of key: value pairs within curly braces:

# In[2]:


my_dict = {"name": "Joe",
           "age": 10, 
           "city": "Paris"}

print(my_dict)


# Notice that in the printed dictionary, the items don't appear in the same order as when we defined it, since dictionaries are unordered. Index into a dictionary using keys rather than numeric indexes:

# In[3]:


my_dict["name"]


# Add new items to an existing dictionary with the following syntax:

# In[4]:


my_dict["new_key"] = "new_value"

print(my_dict)


# Delete existing key: value pairs with del:

# In[5]:


del my_dict["new_key"]

print(my_dict)


# Check the number of items in a dict with len():

# In[6]:



len(my_dict)


# Check whether a certain key exists with "in":

# In[7]:


"name" in my_dict


# You can access all the keys, all the values or all the key: value pairs of a dictionary with the keys(), value() and items() functions respectively:

# In[8]:


my_dict.keys()


# In[10]:


my_dict.values()


# In[11]:


my_dict.items()


# Real world data often comes in the form tables of rows and columns, where each column specifies a different data feature like name or age and each row represents an individual record. We can encode this sort of tabular data in a dictionary by assigning each column label a key and then storing the column values as a list.
# 
# Consider the following table:
# 
# name  &nbsp; &nbsp;&nbsp;age      &nbsp;&nbsp;&nbsp;city  <br>
# Joe  &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;10     &nbsp;&nbsp;&nbsp;&nbsp; Paris <br>
# Bob   &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;15     &nbsp; &nbsp;&nbsp;&nbsp;New York <br>
# Harry  &nbsp;&nbsp; &nbsp;20      &nbsp;&nbsp;&nbsp; Tokyo
# 
# We can store this data in a dictionary like so:

# In[12]:


my_table_dict = {"name": ["Joe", "Bob", "Harry"],
                 "age": [10,15,20] , 
                 "city": ["Paris", "New York", "Tokyo"]}


# Certain data formats like XML and Json have a non-tabular, nested structure. Python dictionaries can contain other dictionaries, so they can mirror this sort of nested structure, providing a convenient interface for working with these sorts of data formats in Python. (We'll cover loading data into Python in a future lesson.).

# ## Sets

# Sets are unordered, mutable collections of immutable objects that cannot contain duplicates. Sets are useful for storing and performing operations on data where each value is unique.
# Create a set with a comma separated sequence of values within curly braces:

# In[13]:


my_set = {1,2,3,4,5,6,7}

type(my_set)


# Add and remove items from a set with add() and remove() respectively:

# In[ ]:


my_set.add(8)

my_set


# In[ ]:


my_set.remove(7)

my_set


# Sets do not support indexing, but they do support basic sequence functions like len(), min(), max() and sum(). You can also check membership and non-membership as usual with in:

# In[14]:


6 in my_set


# One of the main purposes of sets is to perform set operations that compare or combine different sets. Python sets support many common mathematical set operations like union, intersection, difference and checking whether one set is a subset of another:

# In[15]:


set1 = {1,3,5,6}
set2 = {1,2,3,4}

set1.union(set2)          # Get the union of two sets


# In[ ]:


set1.intersection(set2)   # Get the intersection of two sets


# In[ ]:


set1.difference(set2)     # Get the difference between two sets


# In[ ]:


set1.issubset(set2)       # Check whether set1 is a subset of set2


# You can convert a list into a set using the set() function. Converting a list to a set drops any duplicate elements in the list. This can be a useful way to strip unwanted duplicate items or count the number of unique elements in a list. I can also be useful to convert a list to a set if you plan to lookup items repeatedly, since membership lookups are faster with sets than lists.

# In[16]:


my_list = [1,2,2,2,3,3,4,5,5,5,6]

set(my_list)


# ## Wrap Up

# Dictionaries are general-purpose data structures capable of encoding both tabular and non-tabular data. As basic built in Python data structures, however, they lack many of the conveniences we'd like when working with tabular data, like the ability to look at summary statistics for each column and transform the data quickly and easily. In the next two lessons, we'll look at data structures available in Python packages designed for data analysis: numpy arrays and pandas DataFrames.

# ## Next Lesson: [Python for Data 8: Numpy Arrays](https://www.kaggle.com/hamelg/python-for-data-8-numpy-arrays)
# [back to index](https://www.kaggle.com/hamelg/python-for-data-analysis-index)
