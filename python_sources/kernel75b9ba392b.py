#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# #Basic Operations 

# Types of Operators in Python:
# #1	Arithmetic Operators
# #2	Assignment Operators
# #3	Comparison Operators
# #4	Logical Operators
# 

# Arithmetic Operators:
# 	Its use to perform arithmetic operations between variables.
# Such as  + ,  - , * ,  / ,  % ,  ** ,  // , etc.
# 

# Airthmatic Opertors

# In[ ]:


x=10
y=7
x+y #addition
print(x+y)
print(x-y) #substraction
print(x*y) #multiplication
print(x/y) #division
print(x//y) #Floor  division
print(x%y) #mod opeartore
print(x**y) #givse y power of x num


# In[ ]:


#Renaming Variable
a=5
b=a
print(a)
print(b)


# In[ ]:


#assigment Operatores
a=5
b=10
a+=1
b*=3
print(a)
print(b)


# In[ ]:


#Comparison Operators
a=5
b=7
print(a>b)
print(a<b)
print(a==b)
print(a!=b)
print(a>=b)
print(a<=b)


# In[ ]:


#logical Operators
#1. and
#2.or
#3.not


# In[ ]:


x=15
y=20

print((x > 5 and y<30))  # and is used if both statements are true.

print((x > 5 or y < 15)) 

print(not(x > 5 and  y > 15))

