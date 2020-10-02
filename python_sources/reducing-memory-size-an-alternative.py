#!/usr/bin/env python
# coding: utf-8

# ### Why this kernel?
# Whenever the size of dataset goes above 1.5GB there are some memory issues when working with Kaggle Kernels, particlarly when you want to fit everything in one kernel. In the public kernls of this competition I saw a very commonly used function `reduce_mem_usage()` to reduce memory usage introduced in [here](https://www.kaggle.com/mjbahmani/reducing-memory-size-for-ieee) that is basically using the function first introduced in [here](https://www.kaggle.com/arjanso/reducing-dataframe-memory-size-by-65). The same (or very similar function) was being used in Predicting Molecular Properties competition as well. 
# 
# As cool as it seems to use this function, it is not the best idea to use a function blindly. First of all, this function automatically fills in your null values for you! that is not exactly what you asked for. Moreover, there are some hidden pitfalls in using that function as described in [here](https://www.kaggle.com/c/champs-scalar-coupling/discussion/96655#latest-566225) and I identified them in [here](https://www.kaggle.com/mhviraf/why-i-wouldn-t-use-reduce-mem-usage). I think that is the reason why Pandas (with all of its genious developers) doesn't have this basic function built-in. Hence, I believe there is a better solution to this problem here.
# 
# ### What is the problem in first place?
# The fundamental problem is the null values we have in dataset. Since `numpy` treats `NaN` cells as `float`, whenever you have null values in a column even if the natural data type of that column is integer Pandas forces that column to be `float64`. This results in a significantly higher memory usage because many of the features we have in this competition are integers but when loaded as a Pandas DataFrame, they will be stored in memory as `float64`.
# 
# ### Solution
# The solution is simple. Load integers as integers in the first place. The easiest way to do so is to identify data types and use `dtypes={'columns': 'dtype'}` when calling `pd.read_csv()`. However, when you want to use `intXX` as dtype in Pandas (versions earlier than 0.24.0) it doesn't let you use it for columns that contain `NaN` values because as I said before, Pandas uses Numpy `NaN` which is by definition a float (this is why using `reduce_mem_usage()` would fill your `NaN` values for you). However, *starting version 0.24.0* Pandas has introduced a new nullable integer datatype that actually lets you have `NaN` values in integer columns (signed and unsigned). We are going to use this new datatype.
# 
# ### References:
# * https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html
# * https://pandas.pydata.org/pandas-docs/stable/user_guide/integer_na.html

# First we need to install pandas versions later than 0.24.0. In this kernel I will install pandas==0.24.0.
# 
# Don't forget to turn on the Internet under the Settings of your kernel.

# In[ ]:


get_ipython().system("pip install 'pandas==0.24.0' --force-reinstall")


# In[ ]:


import pandas as pd
import numpy as np
pd.__version__


# In[ ]:


train = pd.read_csv('../input/train_transaction.csv')
print('Memory usage:', round(train.memory_usage(deep=True).sum()/1024/1024, 2), 'MB')


# As can be seen, if we import data as is, by default it uses Numpy and its memory usage is 2123.15 MB. Now let's look at the data types

# In[ ]:


train.dtypes.value_counts()


# 376 `float64`s. But do we really have that many columns of type `float64`? Given that we have 590540 rows, using correct data types will make a significant difference. I identified the unsigned nullable integer columns and listed them below as a Python dictionary. To use it, copy this dictionary and simply pass `dtype=proper_dtypes` as an argument in `read_csv()`.

# In[ ]:


proper_dtypes = {'TransactionID': 'UInt32', 'isFraud': 'UInt8', 'TransactionDT': 'UInt32', 'card1': 'UInt16', 'card2': 'UInt16', 'card3': 'UInt8', 'card5': 'UInt8', 'addr1': 'UInt16', 'addr2': 'UInt8', 'dist1': 'UInt16', 'dist2': 'UInt16', 'C1': 'UInt16', 'C2': 'UInt16', 'C3': 'UInt8', 'C4': 'UInt16', 'C5': 'UInt16', 'C6': 'UInt16', 'C7': 'UInt16', 'C8': 'UInt16', 'C9': 'UInt16', 'C10': 'UInt16', 'C11': 'UInt16', 'C12': 'UInt16', 'C13': 'UInt16', 'C14': 'UInt16', 'D1': 'UInt16', 'D2': 'UInt16', 'D3': 'UInt16', 'D5': 'UInt16', 'D7': 'UInt16', 'D10': 'UInt16', 'D13': 'UInt16', 'V1': 'UInt8', 'V2': 'UInt8', 'V3': 'UInt8', 'V4': 'UInt8', 'V5': 'UInt8', 'V6': 'UInt8', 'V7': 'UInt8', 'V8': 'UInt8', 'V9': 'UInt8', 'V10': 'UInt8', 'V11': 'UInt8', 'V12': 'UInt8', 'V13': 'UInt8', 'V14': 'UInt8', 'V15': 'UInt8', 'V16': 'UInt8', 'V17': 'UInt8', 'V18': 'UInt8', 'V19': 'UInt8', 'V20': 'UInt8', 'V21': 'UInt8', 'V22': 'UInt8', 'V23': 'UInt8', 'V24': 'UInt8', 'V25': 'UInt8', 'V26': 'UInt8', 'V27': 'UInt8', 'V28': 'UInt8', 'V29': 'UInt8', 'V30': 'UInt8', 'V31': 'UInt8', 'V32': 'UInt8', 'V33': 'UInt8', 'V34': 'UInt8', 'V35': 'UInt8', 'V36': 'UInt8', 'V37': 'UInt8', 'V38': 'UInt8', 'V39': 'UInt8', 'V40': 'UInt8', 'V41': 'UInt8', 'V42': 'UInt8', 'V43': 'UInt8', 'V44': 'UInt8', 'V45': 'UInt8', 'V46': 'UInt8', 'V47': 'UInt8', 'V48': 'UInt8', 'V49': 'UInt8', 'V50': 'UInt8', 'V51': 'UInt8', 'V52': 'UInt8', 'V53': 'UInt8', 'V54': 'UInt8', 'V55': 'UInt8', 'V56': 'UInt8', 'V57': 'UInt8', 'V58': 'UInt8', 'V59': 'UInt8', 'V60': 'UInt8', 'V61': 'UInt8', 'V62': 'UInt8', 'V63': 'UInt8', 'V64': 'UInt8', 'V65': 'UInt8', 'V66': 'UInt8', 'V67': 'UInt8', 'V68': 'UInt8', 'V69': 'UInt8', 'V70': 'UInt8', 'V71': 'UInt8', 'V72': 'UInt8', 'V73': 'UInt8', 'V74': 'UInt8', 'V75': 'UInt8', 'V76': 'UInt8', 'V77': 'UInt8', 'V78': 'UInt8', 'V79': 'UInt8', 'V80': 'UInt8', 'V81': 'UInt8', 'V82': 'UInt8', 'V83': 'UInt8', 'V84': 'UInt8', 'V85': 'UInt8', 'V86': 'UInt8', 'V87': 'UInt8', 'V88': 'UInt8', 'V89': 'UInt8', 'V90': 'UInt8', 'V91': 'UInt8', 'V92': 'UInt8', 'V93': 'UInt8', 'V94': 'UInt8', 'V95': 'UInt16', 'V96': 'UInt16', 'V97': 'UInt16', 'V98': 'UInt8', 'V99': 'UInt8', 'V100': 'UInt8', 'V101': 'UInt16', 'V102': 'UInt16', 'V103': 'UInt16', 'V104': 'UInt8', 'V105': 'UInt8', 'V106': 'UInt8', 'V107': 'UInt8', 'V108': 'UInt8', 'V109': 'UInt8', 'V110': 'UInt8', 'V111': 'UInt8', 'V112': 'UInt8', 'V113': 'UInt8', 'V114': 'UInt8', 'V115': 'UInt8', 'V116': 'UInt8', 'V117': 'UInt8', 'V118': 'UInt8', 'V119': 'UInt8', 'V120': 'UInt8', 'V121': 'UInt8', 'V122': 'UInt8', 'V123': 'UInt8', 'V124': 'UInt8', 'V125': 'UInt8', 'V138': 'UInt8', 'V139': 'UInt8', 'V140': 'UInt8', 'V141': 'UInt8', 'V142': 'UInt8', 'V143': 'UInt16', 'V144': 'UInt8', 'V145': 'UInt16', 'V146': 'UInt8', 'V147': 'UInt8', 'V148': 'UInt8', 'V149': 'UInt8', 'V150': 'UInt16', 'V151': 'UInt8', 'V152': 'UInt8', 'V153': 'UInt8', 'V154': 'UInt8', 'V155': 'UInt8', 'V156': 'UInt8', 'V157': 'UInt8', 'V158': 'UInt8', 'V167': 'UInt16', 'V168': 'UInt16', 'V169': 'UInt8', 'V170': 'UInt8', 'V171': 'UInt8', 'V172': 'UInt8', 'V173': 'UInt8', 'V174': 'UInt8', 'V175': 'UInt8', 'V176': 'UInt8', 'V177': 'UInt16', 'V178': 'UInt16', 'V179': 'UInt16', 'V180': 'UInt8', 'V181': 'UInt8', 'V182': 'UInt8', 'V183': 'UInt8', 'V184': 'UInt8', 'V185': 'UInt8', 'V186': 'UInt8', 'V187': 'UInt8', 'V188': 'UInt8', 'V189': 'UInt8', 'V190': 'UInt8', 'V191': 'UInt8', 'V192': 'UInt8', 'V193': 'UInt8', 'V194': 'UInt8', 'V195': 'UInt8', 'V196': 'UInt8', 'V197': 'UInt8', 'V198': 'UInt8', 'V199': 'UInt8', 'V200': 'UInt8', 'V201': 'UInt8', 'V217': 'UInt16', 'V218': 'UInt16', 'V219': 'UInt16', 'V220': 'UInt8', 'V221': 'UInt16', 'V222': 'UInt16', 'V223': 'UInt8', 'V224': 'UInt8', 'V225': 'UInt8', 'V226': 'UInt16', 'V227': 'UInt16', 'V228': 'UInt8', 'V229': 'UInt16', 'V230': 'UInt16', 'V231': 'UInt16', 'V232': 'UInt16', 'V233': 'UInt16', 'V234': 'UInt16', 'V235': 'UInt8', 'V236': 'UInt8', 'V237': 'UInt8', 'V238': 'UInt8', 'V239': 'UInt8', 'V240': 'UInt8', 'V241': 'UInt8', 'V242': 'UInt8', 'V243': 'UInt8', 'V244': 'UInt8', 'V245': 'UInt16', 'V246': 'UInt8', 'V247': 'UInt8', 'V248': 'UInt8', 'V249': 'UInt8', 'V250': 'UInt8', 'V251': 'UInt8', 'V252': 'UInt8', 'V253': 'UInt8', 'V254': 'UInt8', 'V255': 'UInt8', 'V256': 'UInt8', 'V257': 'UInt8', 'V258': 'UInt16', 'V259': 'UInt16', 'V260': 'UInt8', 'V261': 'UInt8', 'V262': 'UInt8', 'V279': 'UInt16', 'V280': 'UInt16', 'V281': 'UInt8', 'V282': 'UInt8', 'V283': 'UInt8', 'V284': 'UInt8', 'V285': 'UInt8', 'V286': 'UInt8', 'V287': 'UInt8', 'V288': 'UInt8', 'V289': 'UInt8', 'V290': 'UInt8', 'V291': 'UInt16', 'V292': 'UInt16', 'V293': 'UInt16', 'V294': 'UInt16', 'V295': 'UInt16', 'V296': 'UInt8', 'V297': 'UInt8', 'V298': 'UInt8', 'V299': 'UInt8', 'V300': 'UInt8', 'V301': 'UInt8', 'V302': 'UInt8', 'V303': 'UInt8', 'V304': 'UInt8', 'V305': 'UInt8', 'V322': 'UInt16', 'V323': 'UInt16', 'V324': 'UInt16', 'V325': 'UInt8', 'V326': 'UInt8', 'V327': 'UInt8', 'V328': 'UInt8', 'V329': 'UInt8', 'V330': 'UInt8'}


# In[ ]:


train = pd.read_csv('../input/train_transaction.csv', dtype=proper_dtypes)
print('Memory usage:', round(train.memory_usage(deep=True).sum()/1024/1024, 2), 'MB')


# #### Test set

# In[ ]:


test = pd.read_csv('../input/test_transaction.csv')
print('Memory usage:', round(test.memory_usage(deep=True).sum()/1024/1024, 2), 'MB')


# In[ ]:


test = pd.read_csv('../input/test_transaction.csv',  dtype=proper_dtypes)
print('Memory usage:', round(test.memory_usage(deep=True).sum()/1024/1024, 2), 'MB')


# ## Advantages over reduce_mem_usage():
# * You get to choose how to handle your null values.
# * You don't loose percision.
# 
# (Don't forget that you will need to install Pandas version > 0.24.0)
