#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np                # array processing 
import pandas as pd             # work with labeled data
import seaborn as sns           # Advanced visualization, correlation
import matplotlib.pyplot as plt  #Visualization, basic


# In[ ]:


passmark = 70


# In[ ]:


df = pd.read_csv("../input/StudentsPerformance.csv")


# In[ ]:


df.head()


# In[ ]:


print(df. shape)


# In[ ]:


df.describe()


# In[ ]:


p = sns.countplot(x="math score", data = df, palette = "muted")
_ = plt.setp(p.get_xticklabels(), rotation=180) 


# In[ ]:


df['Math_PassStatus'] = np.where(df['math score']<passmark, 'F', 'P')    # df[column name]
df.Math_PassStatus.value_counts()


# In[ ]:


p = sns.countplot(x='parental level of education', data = df, hue='Math_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='gender', data = df, hue='Math_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='race/ethnicity', data = df, hue='Math_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='test preparation course', data = df, hue='Math_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='lunch', data = df, hue='Math_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


sns.countplot(x= "reading score", data = df, palette="muted")
plt.show()


# In[ ]:


df['Reading_PassStatus'] = np.where(df['reading score']<passmark, 'F', 'P')
df.Reading_PassStatus.value_counts()


# In[ ]:


p = sns.countplot(x='parental level of education', data = df, hue='Reading_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation = 90)


# In[ ]:


p = sns.countplot(x='gender', data = df, hue='Reading_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='race/ethnicity', data = df, hue='Reading_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='test preparation course', data = df, hue='Reading_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='lunch', data = df, hue='Reading_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x="writing score", data = df, palette="muted")
_ = plt.setp(p.get_xticklabels(), rotation=90) 


# In[ ]:


df['Writing_PassStatus'] = np.where(df['writing score']<passmark, 'F', 'P')
df.Writing_PassStatus.value_counts()


# In[ ]:


p = sns.countplot(x='parental level of education', data = df, hue='Writing_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='gender', data = df, hue='Writing_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='race/ethnicity', data = df, hue='Writing_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='test preparation course', data = df, hue='Writing_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='lunch', data = df, hue='Writing_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


df['OverAll_PassStatus'] = df.apply(lambda x : 'F' if x['Math_PassStatus'] == 'F' or 
                                    x['Reading_PassStatus'] == 'F' or x['Writing_PassStatus'] == 'F' else 'P', axis =1)

df.OverAll_PassStatus.value_counts()


# In[ ]:


p = sns.countplot(x='parental level of education', data = df, hue='OverAll_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90) 


# In[ ]:


p = sns.countplot(x='gender', data = df, hue='OverAll_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90) 


# In[ ]:


p = sns.countplot(x='lunch', data = df, hue='OverAll_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90) 


# In[ ]:


p = sns.countplot(x='race/ethnicity', data = df, hue='OverAll_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90) 


# In[ ]:


p = sns.countplot(x='test preparation course', data = df, hue='OverAll_PassStatus', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90) 


# In[ ]:


df['Total_Marks'] = df['math score']+df['reading score']+df['writing score']
df['Percentage'] = df['Total_Marks']/3


# In[ ]:


p = sns.countplot(x= "Percentage", data = df, palette="muted")
_ = plt.setup(p.get_xticklabel(), rotation = 0)


# In[ ]:


def GetGrade(Percentage, OverAll_PassStatus):
    if ( OverAll_PassStatus == 'F'):
        return 'F'    
    if ( Percentage >= 90 ):
        return 'A'
    if ( Percentage >= 80):
        return 'B'
    if ( Percentage >= 70):
        return 'C'
    else: 
        return 'F'

df['Grade'] = df.apply(lambda x : GetGrade(x['Percentage'], x['OverAll_PassStatus']), axis=1)

df.Grade.value_counts()


# In[ ]:


sns.countplot(x="Grade", data = df, order=['A','B','C','F'],  palette="muted")
plt.show()


# In[ ]:


p = sns.countplot(x='parental level of education', data = df, hue='Grade', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='gender', data = df, hue='Grade', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='race/ethnicity', data = df, hue='Grade', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='lunch', data = df, hue='Grade', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:


p = sns.countplot(x='test preparation course', data = df, hue='Grade', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)


# In[ ]:




