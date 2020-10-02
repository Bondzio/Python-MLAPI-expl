#!/usr/bin/env python
# coding: utf-8

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


# In[ ]:


km= 178.5
A = 0.6
delta = 0.009
trueMil = km*1.6

maxLoss = 0.01
error = maxLoss +1

trueMil


# In[ ]:


def predictA(A, km, delta, trueMil):
    estimatedMil = km*A
    print ("for given km ", km, "estimated mile: ", estimatedMil ," estimated")
    error = trueMil-estimatedMil
    #error= error/km
    
    update = error * delta
    print ("error= ",error, " update= ", update)
    
    A += update
    return A,estimatedMil,  error


# In[ ]:


while abs(error) > maxLoss:
    A,estimatedMil,error = predictA(A, km, delta, trueMil)
print("for given km: ", km, " the true mile: ",trueMil," but we estimated: ", estimatedMil, "last error:", error )


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


A

