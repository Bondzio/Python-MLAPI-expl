#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


# import library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# import dataset
df=pd.read_csv("../input/students-performance-in-exams/StudentsPerformance.csv")


# In[ ]:


#first 5 rows
df.head()


# In[ ]:


df.columns


# In[ ]:


df.info()


# In[ ]:


df.isnull().sum()


# In[ ]:


df['Total']=df['math score']+df['reading score']+df['writing score']


# In[ ]:


df.head()


# # Data Visulation

# # 1. count total no. of Male vs Female

# In[ ]:


plt.figure(figsize=(12,7))
ax=sns.countplot(df.gender)

plt.title("Gender ",fontsize=20)

plt.xlabel("Gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 2. count total of every group

# In[ ]:


plt.figure(figsize=(12,7))
label=["group A","group B","group C","group D","group E"]
ax=sns.countplot(x=df["race/ethnicity"],data=df,order=label)

plt.title("Group",fontsize=20)

plt.xlabel("Group",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 3. count Education

# In[ ]:



label=['high school','some high school','some college',"bachelor's degree","associate's degree","master's degree"]    
plt.figure(figsize=(17,7))
ax=sns.countplot(df['parental level of education'],order=label)

plt.title("Education",fontsize=20)

plt.xlabel("Education",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


#  #  4. count Education Gender Wise

# In[ ]:


label=['high school','some high school','some college',"bachelor's degree","associate's degree","master's degree"]    
plt.figure(figsize=(17,7))
ax=sns.countplot(df['parental level of education'],order=label,hue=df.gender)

plt.title("Education",fontsize=20)

plt.xlabel("Education",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 5. Count test preparation coure status

# In[ ]:



plt.figure(figsize=(12,7))
ax=sns.countplot(df['test preparation course'])

plt.title("test preparation course status",fontsize=20)

plt.xlabel("test preparation course status",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
       fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 6. Count test preparation coure status Gender Wise

# In[ ]:


plt.figure(figsize=(12,7))
ax=sns.countplot(df['test preparation course'],hue=df.gender)

plt.title("test preparation course status",fontsize=20)

plt.xlabel("test preparation course status",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 7. Count Lunch

# In[ ]:


plt.figure(figsize=(12,7))
ax=sns.countplot(df['lunch'])

plt.title("Lunch",fontsize=20)

plt.xlabel("Lunch",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 8. Count lunch gender Wise

# In[ ]:


plt.figure(figsize=(12,7))
ax=sns.countplot(df['lunch'],hue=df.gender)

plt.title("Lunch",fontsize=20)

plt.xlabel("Lunch",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 9. Compare 90+ Math score

# In[ ]:


data=df[df['math score']>90]
plt.figure(figsize=(12,7))
ax=sns.countplot(data['gender'])

plt.title("compare 90+ Math Score Male vs female",fontsize=20)

plt.xlabel("gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 10. Compare 90+ Math score Group Wise

# In[ ]:


data=df[df['math score']>90]
plt.figure(figsize=(17,7))
label=["group A","group B","group C","group D","group E"]
ax=sns.countplot(data['gender'],hue=data['race/ethnicity'],hue_order=label)

plt.title("Compare 90+ Math score in every group",fontsize=20)

plt.xlabel("gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 10. Compare 90+ reading score

# In[ ]:


data=df[df['reading score']>90]
plt.figure(figsize=(12,7))
ax=sns.countplot(data['gender'])

plt.title("90+ reading score Male vs female",fontsize=20)

plt.xlabel("gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 11. Compare 90+ reading score Group wise

# In[ ]:


data=df[df['reading score']>90]
plt.figure(figsize=(17,7))
label=["group A","group B","group C","group D","group E"]

ax=sns.countplot(data['gender'],hue=data['race/ethnicity'],hue_order=label)

plt.title("90+ reading score Group Wise",fontsize=20)

plt.xlabel("Gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 12. Compare 90+ writing score

# In[ ]:


data=df[df['writing score']>90]
plt.figure(figsize=(12,7))
ax=sns.countplot(data['gender'])

plt.title("90+ Writing score Male vs female",fontsize=20)

plt.xlabel("Gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 13. Compare 90+ writing score Group wise

# In[ ]:


data=df[df['writing score']>90]
plt.figure(figsize=(17,7))
label=["group A","group B","group C","group D","group E"]

ax=sns.countplot(data['gender'],hue=data['race/ethnicity'],hue_order=label)

plt.title("90+ reading score Group Wise",fontsize=20)

plt.xlabel("Gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 14 compare 70 % up students

# In[ ]:


data=df[df['Total']>210]
plt.figure(figsize=(12,7))
ax=sns.countplot(data['gender'])

plt.title("compare 70% up students",fontsize=20)

plt.xlabel("Gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# # 15 Less than 40 % students

# In[ ]:


data=df[df['Total']<120]
plt.figure(figsize=(12,7))
ax=sns.countplot(data['gender'])

plt.title("compare less than 40%  students",fontsize=20)

plt.xlabel("Gender",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()

