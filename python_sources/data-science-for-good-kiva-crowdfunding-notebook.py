#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


kiva_loans_df = pd.read_csv("../input/kiva_loans.csv")
print(kiva_loans_df.shape)
kiva_loans_df.head()


# In[ ]:


kiva_mpi_df = pd.read_csv("../input/kiva_mpi_region_locations.csv")
print(kiva_mpi_df.shape)
kiva_mpi_df.head()


# In[ ]:


loan_theme_df = pd.read_csv("../input/loan_theme_ids.csv")
print(loan_theme_df.shape)
loan_theme_df.head()


# In[ ]:


loan_themes_df = pd.read_csv("../input/loan_themes_by_region.csv")
print(loan_themes_df.shape)
loan_themes_df.head()


# Start Exploring the Data 

# In[ ]:


kiva_loans_df.info()


# In[ ]:


fd_amt = plt.boxplot(kiva_loans_df['funded_amount'])


# In[ ]:


ln_amt = plt.boxplot(kiva_loans_df['loan_amount'])


# In[ ]:


plt.figure(figsize=(13,4))
sns.countplot(kiva_loans_df['activity'].iloc[:50],order=kiva_loans_df['activity'].iloc[:50].value_counts().index,palette='Set1')
plt.xticks(rotation=90)


# In[ ]:


plt.figure(figsize=(13,4))
sns.countplot(kiva_loans_df['sector'],order=kiva_loans_df['sector'].value_counts().index,palette='Set1')
plt.xticks(rotation=90)


# In[ ]:


plt.figure(figsize=(13,4))
sns.countplot(kiva_loans_df['country'],order=kiva_loans_df['country'].value_counts().index,palette='Set1')
plt.xticks(rotation=90)


# In[ ]:


kiva_loans_df['region'].value_counts().head(50)


# In[ ]:


plt.figure(figsize=(13,4))
sns.countplot(kiva_loans_df['region'].iloc[0:100],order=kiva_loans_df['region'].iloc[0:100].value_counts().index,palette='Set1')
plt.xticks(rotation=90)


# In[ ]:


kiva_loans_df['term_in_months'].value_counts().head(50)


# In[ ]:


plt.figure(figsize=(13,4))
sns.countplot(kiva_loans_df['term_in_months'].iloc[0:50],order=kiva_loans_df['term_in_months'].value_counts().iloc[0:50].index,palette='Set1')
plt.xticks(rotation=90)


# In[ ]:


plt.figure(figsize=(13,4))
sns.countplot(kiva_loans_df['lender_count'], order = kiva_loans_df['lender_count'].value_counts().iloc[0:50].index, palette='Set1')
plt.xticks(rotation=90)


# In[ ]:


kiva_gender = []

for gender in kiva_loans_df["borrower_genders"].values:
    if str(gender) != "nan":
        gender_strip = gender.split(',')
        for i in gender_strip:
            kiva_gender.extend(i.split())
kiva_gender = pd.DataFrame(kiva_gender)


# In[ ]:


pd.value_counts(kiva_gender.values.flatten())


# In[ ]:


plt.figure(figsize=(13,4))
sns.countplot(kiva_loans_df['repayment_interval'], order = kiva_loans_df['repayment_interval'].value_counts().iloc[0:50].index, palette='Set1')
plt.xticks(rotation=90)


# In[ ]:


ctry_fd = pd.DataFrame(kiva_loans_df.groupby('country').sum()['funded_amount'].sort_values(ascending=False)).reset_index()


# In[ ]:


ctry_fd.head(5)


# In[ ]:


kiva_loans_df.groupby(['country'])['loan_amount'].mean().sort_values(ascending=False)


# In[ ]:


kiva_loans_df[kiva_loans_df['country'] == "Cote D'Ivoire"]


# This is my **First Competition Kernal**, hope so you guys like it. Please **share** and Vote. 
# Let me know anthing i need to work on. :)

# 
