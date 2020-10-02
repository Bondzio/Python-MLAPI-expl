#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("../input/Salaries.csv" , low_memory=False)
print ( "Dataset has %d rows and %d columns" % (df.shape[0] , df.shape[1] )  )


# Now let's do some pre-processing on the features that are text: "JobTitle" and "EmployeeName"

# In[ ]:


df["EmployeeName"] = df["EmployeeName"].apply(lambda x:x.lower())
df["JobTitle"] = df["JobTitle"].apply(lambda x:x.lower())
df["namelength"] = df["EmployeeName"].apply(lambda x:len(x.split()))
df["compoundName"] = df["EmployeeName"].apply(lambda x: 1 if "-" in x else 0 )


# In[ ]:


#last name analysis
def lastName(x):
    sp = x.split()
    if sp[-1].lower() == "jr":
        return sp[-2]
    else:
        return sp[-1]  

df["lastName"] = df["EmployeeName"].apply(lastName)
sns.countplot(y = "lastName" , data = df , order=df["lastName"].value_counts()[:10].index)


# In[ ]:


#first name
df["firstName"] = df["EmployeeName"].apply(lambda x:x.split()[0])
sns.countplot(y = "firstName" , data = df , order=df["firstName"].value_counts()[:10].index)


# In[ ]:


# first + last name
sns.countplot(y = "EmployeeName" , data = df , order=df["EmployeeName"].value_counts()[:10].index)


# In[ ]:


# pay
sns.distplot(a=df["BasePay"][:10])


# In[ ]:


df


# In[ ]:




