#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import os

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory


for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# # Importing Dataset and Data Cleaning.

# In[ ]:



df = pd.read_csv('/kaggle/input/pakistan-corona-virus-citywise-data/PK COVID-19.csv', delimiter=',')
df.dataframeName = 'PK COVID-19.csv'
nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


df.head()


# In[ ]:


#showing basic information rows and columns. showing number of filled rows and datatypes of given columns
df.info()


# In[ ]:


#showing the statistical measures in dataset like count, mean, min, max for numerical features
df.describe()


# In[ ]:


# Checking for wrong values
for col in df.columns:
    print("Unique Values of Column "+col+":\n "+str(df[col].unique())+" \n")


# In[ ]:


#removing null values
df.dropna(axis="rows", how="any", inplace = True)
df.reset_index(drop=True, inplace=True)


# In[ ]:


df.isnull().sum()


# In[ ]:


#Correcting values according to the domain
df['Deaths']=df['Deaths'].astype(int)
df['Cases']=df['Cases'].astype(int)
df['Recovered']=df['Recovered'].astype(int)


# In[ ]:


df.loc[df.Province == "khyber Pakhtunkhwa", "Province"] = "Khyber Pakhtunkhwa"


# # Multivariate Analysis

# In[ ]:


corr = df.corr()
sns.set(rc={'figure.figsize':(10,5)})
sns.heatmap(corr, annot=True)


# The above chart shows the correlation of features with each other. According to the above graph there is weak positive correlation of number of cases with deaths or vice versa.

# In[ ]:


sns.pairplot(df[['Cases','Deaths','Recovered']])


# # Univariate Analysis

# In[ ]:


Categorical = ['Date','Travel_history','Province','City']
Numerical = ['Deaths','Cases','Recovered']


# In[ ]:


fig = plt.figure(figsize = (30,35))
axes = 410
for cat in Categorical:
    axes += 1
    fig.add_subplot(axes)
    sns.countplot(data = df, x = cat)
    plt.xticks(rotation=30)
plt.show()


# The above count plots shows the number of data present according to the different features.

# In[ ]:


plt.subplots(figsize=(15, 15))
size = dict(df['Travel_history'].value_counts()).values()
colors = sns.color_palette()
labels = dict(df['Travel_history'].value_counts()).keys()
explode = [0.1, 0.2, 0.2, 0.1, 0, 0.1, 0.1, 0.1, 0.3, 0.3 ,0.3 ,0.3 , 0.3, 0.3, 0.3]

circle = plt.Circle((0, 0), 0.6, color = 'white')

plt.pie(size, colors = colors, labels = labels, explode = explode, shadow = False, autopct = '%.2f%%')
plt.title('Travel History', fontsize = 20)
p = plt.gcf()
p.gca().add_artist(circle)
plt.axis('off')
plt.legend()

plt.show()


# In[ ]:


plt.subplots(figsize=(7, 7))
size = dict(df['Province'].value_counts()).values()
colors = sns.color_palette()
labels = dict(df['Province'].value_counts()).keys()
explode = [0.1, 0.2, 0.2, 0.1, 0, 0.1, 0.1, 0.3]

circle = plt.Circle((0, 0), 0.6, color = 'white')

plt.pie(size, colors = colors, labels = labels, explode = explode, shadow = False, autopct = '%.2f%%')
plt.title('Province', fontsize = 20)
p = plt.gcf()
p.gca().add_artist(circle)
plt.axis('off')
plt.legend()

plt.show()


# According to the data and above pie chart, most of the events like identified cases, deaths and recovery are occurred in Punjab, KPK, Sindh and other provices have less amount of events occurred 

# In[ ]:


fig = plt.figure(figsize = (20,15))

for i,num in enumerate(Numerical):
    
    fig.add_subplot(3,3,i+1)
    sns.boxplot(data = df, x = num)
plt.show()


# The above plots shows that there are many outliers in the as the number of deaths, cases and recovered people are increasing day by day

# In[ ]:


df.hist()
print(f'Total number of cases registered: '+str(df['Cases'].sum()))
print(f'Total Number of deaths registered: '+str(df['Deaths'].sum()))
print(f'Total Number of recovered cases registered: '+str(df['Recovered'].sum()))


# # Bivariate Analysis

# In[ ]:



#Plotting how many cases registered on a particular date all over Pakistan.
ax = df.groupby('Date')['Cases'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Date',fontsize=15)
ax.set_ylabel('Cases',fontsize=15)
ax.set_title('Number of Corona virus cases registered on particular date.',fontsize=15)
plt.show()


# In[ ]:


#Plotting how many cases registered in provinces all over Pakistan.
ax = df.groupby('Province')['Cases'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Province',fontsize=15)
ax.set_ylabel('Cases',fontsize=15)
ax.set_title('Number of Corona virus cases registered in all provinces.',fontsize=15)
plt.show()


# In[ ]:


#Plotting how many cases registered in a particular city all over Pakistan.
ax = df.groupby('City')['Cases'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Cities',fontsize=15)
ax.set_ylabel('Cases',fontsize=15)
ax.set_title('Number of Corona virus cases registered in all cities.',fontsize=15)
plt.show()


# In[ ]:


#Plotting how many deaths registered in a particular city all over Pakistan.
ax = df.groupby('City')['Deaths'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Cities',fontsize=15)
ax.set_ylabel('Deaths',fontsize=15)
ax.set_title('Number of death cases registered due to Corona virus in all cities.',fontsize=15)
plt.show()


# In[ ]:


#Plotting how many deaths registered in a provinces all over Pakistan.
ax = df.groupby('Province')['Deaths'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Provinces',fontsize=15)
ax.set_ylabel('Deaths',fontsize=15)
ax.set_title('Number of death cases registered due to Corona virus in all provinces.',fontsize=15)
plt.show()


# In[ ]:


#Plotting how many deaths registered on a particular date all over Pakistan.
ax = df.groupby('Date')['Deaths'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Date',fontsize=15)
ax.set_ylabel('Deaths',fontsize=15)
ax.set_title('Number of death cases registered due to Corona virus on a particular date.',fontsize=15)
plt.show()


# In[ ]:


#Plotting how many recoveries registered in a particular city all over Pakistan.
ax = df.groupby('City')['Recovered'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Cities',fontsize=15)
ax.set_ylabel('Recovered',fontsize=15)
ax.set_title('Number of recoveries registered from Corona virus in all cities.',fontsize=15)
plt.show()


# In[ ]:


#Plotting how many recoveries registered in a particular province all over Pakistan.
ax = df.groupby('Province')['Recovered'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Provinces',fontsize=15)
ax.set_ylabel('Recovered',fontsize=15)
ax.set_title('Number of recoveries registered from Corona virus in all provinces.',fontsize=15)
plt.show()


# In[ ]:


#Plotting how many recoveries registered in a particular according to the dates all over Pakistan.
ax = df.groupby('Date')['Recovered'].sum().sort_index().plot('bar',figsize=(18,5))
ax.set_xlabel('Date',fontsize=15)
ax.set_ylabel('Recovered',fontsize=15)
ax.set_title('Number of recoveries registered from Corona virus on a particular date.',fontsize=15)
plt.show()


# In[ ]:


plt.subplots(figsize=(20, 5))
sns.stripplot(df['Province'], df['Cases'])
plt.title('Cases vs Province', fontsize = 30)
plt.xlabel('Province', fontsize = 18)
plt.ylabel('Cases', fontsize = 18)


# In[ ]:


plt.subplots(figsize=(20, 5))
sns.stripplot(df['Province'], df['Deaths'])
plt.title('Deaths vs Province', fontsize = 30)
plt.xlabel('Province', fontsize = 18)
plt.ylabel('Deaths', fontsize = 18)


# In[ ]:


plt.subplots(figsize=(20, 5))
sns.stripplot(df['Province'], df['Recovered'])
plt.title('Recovered vs Province', fontsize = 30)
plt.xlabel('Province', fontsize = 18)
plt.ylabel('Recovered', fontsize = 18)


# In[ ]:




