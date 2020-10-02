#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('../input/StudentsPerformance.csv')

df.head()

df.describe()

print(df.shape)

p = sns.countplot(x='gender', data=df)

p = sns.countplot(x='race/ethnicity', data=df)

p = sns.countplot(x='parental level of education', data=df)
_ = plt.setp(p.get_xticklabels(), rotation=90)

p = sns.countplot(x='lunch', data=df)

p = sns.countplot(x='test preparation course', data=df)

min_pass_marks = 50
df['passed_maths'] = np.where(df['math score']<min_pass_marks, 'F', 'P')
p = sns.countplot(x='gender', data=df, hue='passed_maths')


df['passed_writing'] = np.where(df['writing score']<min_pass_marks, 'F', 'P')
p = sns.countplot(x='gender', data=df, hue='passed_writing')

df['passed_reading'] = np.where(df['writing score']<min_pass_marks, 'F', 'P')
p = sns.countplot(x='gender', data=df, hue='passed_reading')

df['overall'] = (df['math score'] + df['reading score'] + df['writing score'])/3

print(df['overall'])

print(max(df['overall']))

