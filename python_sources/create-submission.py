#!/usr/bin/env python
# coding: utf-8

# We have to submit our answers in a `.csv` file. This notebook shows how to create the `.csv` in the correct format.

# In[1]:


import numpy as np
import pandas as pd
import os
import glob
import datetime


# In[2]:


data_dir=os.path.join('..','input')


# In[3]:


# setup path variables
paths_test_a=glob.glob(os.path.join(data_dir,'testing-a','*.png'))
paths_test_b=glob.glob(os.path.join(data_dir,'testing-b','*.png'))
paths_test_c=glob.glob(os.path.join(data_dir,'testing-c','*.png'))
paths_test_d=glob.glob(os.path.join(data_dir,'testing-d','*.png'))
paths_test_e=glob.glob(os.path.join(data_dir,'testing-e','*.png'))
paths_test_f=glob.glob(os.path.join(data_dir,'testing-f','*.png'))+glob.glob(os.path.join(data_dir,'testing-f','*.JPG'))
paths_test_auga=glob.glob(os.path.join(data_dir,'testing-auga','*.png'))
paths_test_augc=glob.glob(os.path.join(data_dir,'testing-augc','*.png'))
paths_test_all=paths_test_a+paths_test_b+paths_test_c+paths_test_d+paths_test_e+paths_test_f+paths_test_auga+paths_test_augc


# In[4]:


paths_test_all[0:3]


# In[5]:


def get_key(path):
    # separate the key from the filepath of an image
    return path.split(sep=os.sep)[-1]


# In[6]:


# get the keys of all test images
keys=[get_key(path) for path in paths_test_all]
predictions=np.random.randint(low=0,high=10,size=len(keys)) # make some dummy predections (random integers between 0 t0 9)
# predictions=np.random.randint(low=0,high=1,size=len(keys)) 


# In[13]:


# get the current time and add it to the submission filename, helps to keep track of submissions
current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
flname_sub = 'submission_' + current_time + '_'+'.csv' # submission file name
flname_sub


# In[14]:


def create_submission(predictions,keys,path):
    result = pd.DataFrame(
        predictions,
        columns=['label'],
        index=keys
        )
    result.index.name='key'
    result.to_csv(path, index=True) 


# In[15]:


create_submission(predictions,keys,flname_sub)


# In[16]:


# Let's load the submission and display it
pd.read_csv(flname_sub)

