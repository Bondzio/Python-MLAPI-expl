#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # for plotting

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# this gives all the filenames directory locations and names in lists
filename_list = []
filename_name = []
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        if not filename.endswith('csv'):
            continue
        else:    
            filename_list.append(os.path.join(dirname, filename))
            filename_name.append(filename[:-4])


# In[ ]:


#filename_list


# In[ ]:


#all_csvs = pd.concat(map(pd.read_csv, filename_list[0:25])) # takes too much memory to run
#all_csvs.apply(lambda row: row.astype(str).str.contains('cancer').any(), axis=1)


# In[ ]:


# this creates a dataframe for each file, named file_num 1-200 
#then adds an attribute 'file_name' that corressponds to the file it came from or resets the index with the the file name
for i in range(len(filename_list)):
    globals()['file_num'+str(i)] = pd.read_csv(filename_list[i])
    #globals()['file_num'+str(i)].file_name = filename_name[i] #this might be easier to use than renaming the index like in the next line
    globals()['file_num'+str(i)] = globals()['file_num'+str(i)].reindex(globals()['file_num'+str(i)].index.rename(filename_name[i]))
    


# In[ ]:


#file_num0.file_name


# In[ ]:


file_num0.head()


# In[ ]:


file_num0.apply(lambda row: row.astype(str).str.contains('cancer').any(), axis=1).sum()


# In[ ]:


# this checks to see if cancer is mentioned in any of the dataframes, and makes a list of counts
#this takes awhile to run
cancer_list = []
for i in range(len(filename_list)):
    cancer_list.append(globals()['file_num'+str(i)].apply(lambda row: row.astype(str).str.contains('cancer', case=False).any(), axis=1).sum())


# In[ ]:


# turn list into numpy array
cancer_arr = np.array(cancer_list)
cancer_arr


# In[ ]:


#gives array of indices of dataframe filenames that have cancer mentioned 
np.nonzero(cancer_arr)


# In[ ]:


file_num10.head()


# In[ ]:


file_num14.head()


# In[ ]:


file_num22.head()


# In[ ]:


file_num26.head()


# In[ ]:


file_num33.head()


# In[ ]:


file_num47.head()


# In[ ]:


file_num55.head()


# In[ ]:


file_num69.head()


# In[ ]:





# In[ ]:


file_num13.columns.str.contains('state',case = False).sum()


# In[ ]:


# this checks to see if cancer is mentioned in any of the dataframes columns, and makes a list of counts
cancer_col = []
for i in range(len(filename_list)):
    cancer_col.append(globals()['file_num'+str(i)].columns.str.contains('cancer', case=False).sum())


# In[ ]:


#cancer_col


# In[ ]:


# turn list into numpy array
cancer_col_arr = np.array(cancer_col)
#cancer_col_arr


# In[ ]:


#gives array of indices of dataframe filenames that have cancer mentioned 
np.nonzero(cancer_col_arr)


# In[ ]:


#this is the only dataframe that has a column with cancer in its name
file_num13.columns


# In[ ]:


file_num13.cancer_crude95ci


# In[ ]:




