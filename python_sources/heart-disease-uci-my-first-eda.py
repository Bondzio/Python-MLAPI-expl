#!/usr/bin/env python
# coding: utf-8

# Hi, This is my very first EDA. If you like it please do comment and vote. **Thank you**.

# **Attribute Information:** 
# > 1. age 
# > 2. sex 
# > 3. chest pain type (4 values) 
# > 4. resting blood pressure 
# > 5. serum cholestoral in mg/dl 
# > 6. fasting blood sugar > 120 mg/dl
# > 7. resting electrocardiographic results (values 0,1,2)
# > 8. maximum heart rate achieved 
# > 9. exercise induced angina 
# > 10. oldpeak = ST depression induced by exercise relative to rest 
# > 11. the slope of the peak exercise ST segment 
# > 12. number of major vessels (0-3) colored by flourosopy 
# > 13. thal
# > 14. target

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Loading the data and Checking first 5 rows.
data=pd.read_csv('../input/heart.csv')
data.head()


# In[ ]:


#Getting info about our Variables
data.info()


# In[ ]:


#Cheching any Null values.
data.isnull().any()


# In[ ]:


#Descriptive statistics of data
data.describe()


# In[ ]:


#Checking our Columns
data.columns


# In[ ]:


#Getting the shape of the data set
data.shape


# In[ ]:


#How well the variables are related to each other.
plt.figure(figsize = (15, 15))
sns.heatmap(data.corr(), annot = True)
plt.title('Correlation Table', fontsize = 20)


# Age Analysis

# In[ ]:


data.age.head()


# In[ ]:


print('The Oldest Person in the room is of age', data.age.max())
print('The Youngest Person in the room is of age', data.age.min())
print('The Mean age in the room is', data.age.mean())


# In[ ]:


#lets find the frequency of age
data.age.value_counts()


# In[ ]:


#Plotting the Frequency of Age.
plt.figure(figsize = (15,8))
sns.countplot(data['age'])
plt.xlabel('Age', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Frequency', fontsize = 20)


# Majority of People are of age 58 and 57.
# So people of late 50's be careful :p

# In[ ]:


#Plotting the Distribution of Age. 
#Histogram
plt.figure(figsize = (10,8))
sns.distplot(data['age'], bins = 35, kde = True)
plt.xlabel('Age', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Histogram', fontsize = 20)


# Gender Analysis

# In[ ]:


#0 = female, 1 = male
plt.figure(figsize = (5,5))
sns.set(style = 'white', palette = 'bright', color_codes = True)
sns.countplot(data['sex'])
plt.xlabel('Gender - 0 = female, 1 = male', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)


# In[ ]:


#Plotting the Frequency of Male Age.
plt.figure(figsize = (15, 8))
sns.countplot(data[data['sex']==1]['age'])
plt.xlabel('Age', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Frequency', fontsize = 20)


# In[ ]:


#Plotting the Frequency of Female Age.
plt.figure(figsize = (15, 8))
sns.countplot(data[data['sex']==0]['age'])
plt.xlabel('Age', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Frequency', fontsize = 20)


# In[ ]:


#lets crosstabs for age and gender.
pd.crosstab(data.age,data.sex).plot(kind='bar',figsize=(20,6))
plt.xlabel('Age', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Frequency', fontsize = 20)


# cp Analysis

# In[ ]:


#Value 1: typical angina 
#Value 2: atypical angina
#Value 3: non-anginal pain 
#Value 4: asymptomatic
plt.figure(figsize = (5,5))
sns.countplot(data['cp'])
plt.xlabel('Chest Pain Type', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Frequency', fontsize = 20)


# We see majority of people are suffering from Typical Angina

# In[ ]:


#Percentage of People Suffering from different Chest Pain Types
plt.figure(figsize = (8,8))
lables = ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic']
sizes = data['cp'].value_counts().values
explode = [0.1, 0, 0, 0]
plt.pie(sizes, labels = lables, explode = explode, shadow = True, startangle=90, autopct='%1.1f%%')
plt.legend()
plt.show()


# In[ ]:


#People falling Under Different Chest Pain Types accourding to ages
plt.figure(figsize = (10,7))
sns.set(style = 'white', palette = 'colorblind', color_codes = True)
sns.swarmplot(x = 'cp', y = 'age', hue = 'sex', data = data)
plt.xlabel('Chest Pain Type', fontsize = 15)
plt.ylabel('Age', fontsize = 15)
plt.title('People falling Under Different Chest Pain Types', fontsize = 15)


# From Pie Chart we know that majority of people suffer from CP0.
# Here we can see that 55-60 age group people are most prone to CP0. 

# In[ ]:


#Different Chest Pain Types Vs Resting BPs
plt.figure(figsize = (10,7))
sns.set(style = 'white', palette = 'colorblind', color_codes = True)
sns.swarmplot(x = 'cp', y = 'trestbps', hue = 'sex', data = data)
plt.xlabel('Chest Pain Type', fontsize = 15)
plt.ylabel('Resting BPs', fontsize = 15)
plt.title('Different Chest Pain Types Vs Resting BPs', fontsize = 15)


# trestbps Analysis - resting blood pressure (in mm Hg on admission to the hospital)

# In[ ]:


#Resting Blood Pressure Freqeuncy
plt.figure(figsize = (20,8))
sns.countplot(data['trestbps'])
plt.xlabel('Resting Blood Pressure (in mm Hg on admission to the hospital)', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Resting Blood Pressure Freqeuncy', fontsize = 20)


# In[ ]:


plt.figure(figsize = (15,8))
sns.regplot(x = 'age', y = 'trestbps', data = data, fit_reg = True)
plt.xlabel('Age', fontsize = 15)
plt.ylabel('Resting BPs', fontsize = 15)
plt.title('Regression plot b/w Age and Resting BPs', fontsize = 20)


# We can see that there is a Positive relaion between Age and BP

# In[ ]:


print('Maximum Blood Pressure Observed with Chest Pain Type 0 Patients is:',data[data['cp']==0]['trestbps'].max())
print('Maximum Blood Pressure Observed with Chest Pain Type 1 Patients is:',data[data['cp']==1]['trestbps'].max())
print('Maximum Blood Pressure Observed with Chest Pain Type 2 Patients is:',data[data['cp']==2]['trestbps'].max())
print('Maximum Blood Pressure Observed with Chest Pain Type 3 Patients is:',data[data['cp']==3]['trestbps'].max())
print('Average Blood Pressure is', data['trestbps'].mean())
print('Minimum Blood Pressure Observed with Chest Pain Type 0 Patients is:',data[data['cp']==0]['trestbps'].min())
print('Minimum Blood Pressure Observed with Chest Pain Type 1 Patients is:',data[data['cp']==1]['trestbps'].min())
print('Minimum Blood Pressure Observed with Chest Pain Type 2 Patients is:',data[data['cp']==2]['trestbps'].min())
print('Minimum Blood Pressure Observed with Chest Pain Type 3 Patients is:',data[data['cp']==3]['trestbps'].min())


# chol Analysis (serum cholestoral in mg/dl)

# In[ ]:


plt.figure(figsize = (20,10))
sns.set(style = 'whitegrid', palette = 'bright', color_codes = True)
sns.distplot(data['chol'], bins = 45, kde = True)
plt.xlabel('serum cholestoral in mg/dl', fontsize = 15)
plt.title('Histogram for Chol', fontsize = 20)


# In[ ]:


print('Maximum Serum Cholestrol(mg/dl) Observed with Chest Pain Type 0 Patients is:',
      data[data['cp']==0]['chol'].max())
print('Maximum Serum Cholestrol(mg/dl) Observed with Chest Pain Type 1 Patients is:',
      data[data['cp']==1]['chol'].max())
print('Maximum Serum Cholestrol(mg/dl) Observed with Chest Pain Type 2 Patients is:',
      data[data['cp']==2]['chol'].max())
print('Maximum Serum Cholestrol(mg/dl) Observed with Chest Pain Type 3 Patients is:',
      data[data['cp']==3]['chol'].max())
print('Average Serum Cholestrol(mg/dl) is', data['chol'].mean())
print('Minimum Serum Cholestrol(mg/dl) Observed with Chest Pain Type 0 Patients is:',
      data[data['cp']==0]['chol'].min())
print('Minimum Serum Cholestrol(mg/dl) Observed with Chest Pain Type 1 Patients is:',
      data[data['cp']==1]['chol'].min())
print('Minimum Serum Cholestrol(mg/dl) Observed with Chest Pain Type 2 Patients is:',
      data[data['cp']==2]['chol'].min())
print('Minimum Serum Cholestrol(mg/dl) Observed with Chest Pain Type 3 Patients is:',
      data[data['cp']==3]['chol'].min())


# In[ ]:


plt.figure(figsize = (10,8))
sns.set(style = 'white', palette = 'bright', color_codes = True)
ax = sns.regplot(x = 'trestbps', y = 'chol', data = data, fit_reg = True)
ax.set_xlabel(xlabel = 'Resting BPs')
ax.set_ylabel(ylabel = 'serum cholestoral in mg/dl')
ax.set_title(label = 'Trestbps Vs Chol')
plt.show()


# In[ ]:


plt.figure(figsize = (10,8))
sns.set(style = 'white', palette = 'bright', color_codes = True)
ax = sns.regplot(x = 'age', y = 'chol', data = data, fit_reg = True)
ax.set_xlabel(xlabel = 'age')
ax.set_ylabel(ylabel = 'serum cholestoral in mg/dl')
ax.set_title(label = 'age Vs Chol')
plt.show()


# Fasting Blood Sugar Analysis

# In[ ]:


plt.figure(figsize = (5,5))
sns.countplot(data['fbs'])
plt.xlabel('fasting blood sugar > 120 mg/dl', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Count of FBs', fontsize = 20)


# In[ ]:


plt.figure(figsize=(10, 5))

#Number of Males with fasting blood sugar > 120 mg/dl
#1 = true; 0 = false
plt.subplot(1,2,1)
sns.countplot(data[data['sex']==1]['fbs'])
plt.xlabel('fasting blood sugar > 120 mg/dl', fontsize = 15)
plt.ylabel('Number of Males', fontsize = 15)
plt.title('Count of FBs', fontsize = 20)

#Number of Females with fasting blood sugar > 120 mg/dl
#1 = true; 0 = false
plt.subplot(1,2,2)
sns.countplot(data[data['sex']==0]['fbs'])
plt.xlabel('fasting blood sugar > 120 mg/dl', fontsize = 15)
plt.ylabel('Number of Females', fontsize = 15)
plt.title('Count of FBs', fontsize = 20)


# Resting Electrocardiographic Analysis

# In[ ]:


plt.figure(figsize = (5,5))
sns.countplot(data['restecg'])
plt.xlabel('resting electrocardiographic results', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)
plt.title('Count of restecg', fontsize = 20)


# In[ ]:


plt.figure(figsize=(10, 5))

#Male resting electrocardiographic results
plt.subplot(1,2,1)
sns.countplot(data[data['sex']==1]['restecg'])
plt.xlabel('resting electrocardiographic results', fontsize = 15)
plt.ylabel('Number of Males', fontsize = 15)

#Female resting electrocardiographic results
plt.subplot(1,2,2)
sns.countplot(data[data['sex']==0]['restecg'])
plt.xlabel('resting electrocardiographic results', fontsize = 15)
plt.ylabel('Number of Females', fontsize = 15)


# In[ ]:


plt.figure(figsize = (10,10))
sns.set(style = 'white', palette = 'bright', color_codes = True)
sns.catplot(x = 'restecg', y = 'chol', hue = 'sex', col = 'fbs', data = data)


# Analysis on Maximum Heart Rate Achieved

# In[ ]:


#Distribution of maximum heart rate achieved.
plt.figure(figsize = (10,5))
sns.distplot(data['thalach'], kde = True)
plt.title('Distribution of maximum heart rate', fontsize = 20)


# In[ ]:


#we will see the Average of the Maximum Heart Achieved Accourding to the Chest Pain Type
plt.figure(figsize = (8,5))
sns.set(style = 'white', palette = 'colorblind', color_codes = True)
sns.barplot(x = data.groupby(data['cp'])['thalach'].mean().index, 
            y = data.groupby(data['cp'])['thalach'].mean().values)
plt.xlabel('Type of Chest Pain', fontsize = 15)
plt.ylabel('Average of the Max Heart Rate Achieved', fontsize = 15)


# In[ ]:


sns.set(style = 'white', palette = 'colorblind', color_codes = True)
sns.lmplot(x = 'thalach', y = 'trestbps', hue = 'sex', fit_reg = True, height = 7, aspect = 1, data = data)
plt.xlabel('maximum heart rate achieved', fontsize = 15)
plt.ylabel('resting blood pressure', fontsize = 15)
plt.title('Thalach Vs Trestbps', fontsize = 15)


# In[ ]:


sns.set(style = 'white', palette = 'colorblind', color_codes = True)
sns.lmplot(x = 'thalach', y = 'chol', hue = 'sex', fit_reg = True, height = 7, aspect = 1, data = data)
plt.xlabel('maximum heart rate achieved', fontsize = 15)
plt.ylabel('serum cholestoral in mg/dl', fontsize = 15)
plt.title('Thalach Vs Chol', fontsize = 15)


# In[ ]:


plt.figure(figsize = (10,8))
sns.set(style = 'white', palette = 'bright', color_codes = True)
sns.swarmplot(x = 'restecg', y = 'thalach', hue = 'sex', data = data)
plt.xlabel('resting electrocardiographic results', fontsize = 15)
plt.ylabel('maximum heart rate achieved', fontsize = 15)
plt.title('Restecg Vs Thalach', fontsize = 15)


# Analysis on Exercise Induced Angina

# In[ ]:


plt.figure(figsize = (5,5))
sns.countplot(data['exang'])
plt.xlabel('exercise induced angina : 1 = yes, 0 = no', fontsize = 15)
plt.ylabel('Number of People', fontsize = 15)


# In[ ]:


plt.figure(figsize=(10, 5))

#exercise induced angina - Males
#1 = yes, 0 = no
plt.subplot(1,2,1)
sns.countplot(data[data['sex']==1]['exang'])
plt.xlabel('exercise induced angina - Males', fontsize = 15)
plt.ylabel('Number of Males', fontsize = 15)

#exercise induced angina - Females
#1 = yes, 0 = no
plt.subplot(1,2,2)
sns.countplot(data[data['sex']==0]['exang'])
plt.xlabel('exercise induced angina - Females', fontsize = 15)
plt.ylabel('Number of Females', fontsize = 15)


# We Concentrate on People with exercise induced angina (1 = Yes).
# For more Detais about exercise induced angina [Click here](https://rehabilitateyourheart.wordpress.com/2013/01/16/exercise-induced-angina/)

# In[ ]:


exang1 = data[data['exang']==1][['sex', 'exang', 'restecg', 'age', 'thalach']]
exang1.head()


# In[ ]:


plt.figure(figsize = (15,8))
sns.barplot(x = 'age', y = 'thalach', data = exang1)
plt.xlabel('Age', fontsize = 15)
plt.ylabel('maximum heart rate achieved', fontsize = 15)
plt.title('Age Vs Thalach when Exang = 1', fontsize = 15)


# Analysis on **oldpeak** - ST depression induced by exercise relative to rest

# In[ ]:


data['oldpeak'].value_counts().head()


# We Concentrate on the People whose oldpeak(ST depression induced by exercise relative to rest) 
# is no equal to 0.

# In[ ]:


plt.figure(figsize = (15,8))
sns.countplot(data[data['oldpeak']!=0]['oldpeak'])
plt.xlabel('ST depression induced by exercise relative to rest', fontsize = 15)
plt.ylabel('Count', fontsize = 15)
plt.title('oldpeak frequency', fontsize = 20)


# Some Violinplots ahead

# In[ ]:


plt.figure(figsize = (8,5))
sns.violinplot(x = data['exang'], y = data[data['oldpeak']!=0]['oldpeak'])
plt.xlabel('exercise induced angina - 1 = yes; 0 = no', fontsize = 10)
plt.ylabel('oldpeak', fontsize = 10)
plt.title('violin plot of oldpeak', fontsize = 15)


# In[ ]:


plt.figure(figsize = (8,5))
sns.violinplot(x = data['restecg'], y = data[data['oldpeak']!=0]['oldpeak'])
plt.xlabel('resting electrocardiographic results', fontsize = 10)
plt.ylabel('oldpeak', fontsize = 10)
plt.title('violin plot of oldpeak', fontsize = 15)


# In[ ]:


plt.figure(figsize = (8,5))
sns.violinplot(x = data['cp'], y = data[data['oldpeak']!=0]['oldpeak'])
plt.xlabel('chest pain type', fontsize = 10)
plt.ylabel('oldpeak', fontsize = 10)
plt.title('violin plot of oldpeak', fontsize = 15)


# In[ ]:


plt.figure(figsize = (8,5))
sns.violinplot(x = data['slope'], y = data[data['oldpeak']!=0]['oldpeak'])
plt.xlabel('the slope of the peak exercise ST segment', fontsize = 10)
plt.ylabel('oldpeak', fontsize = 10)
plt.title('violin plot of oldpeak', fontsize = 15)


# Analysis on **slope** - the slope of the peak exercise ST segment

# In[ ]:


plt.figure(figsize = (8,5))
sns.barplot(x = 'slope', y = 'thalach', data = data)
plt.xlabel('the slope of the peak exercise ST segment', fontsize = 15)
plt.ylabel('maximum heart rate achieved', fontsize = 15)


# In[ ]:


plt.figure(figsize = (10,8))
sns.set(style = 'white', palette = 'colorblind', color_codes = True)
sns.swarmplot(x = 'slope', y = 'oldpeak', hue = 'sex', data = data)
plt.xlabel('the slope of the peak exercise ST segment', fontsize = 15)
plt.ylabel('ST depression induced by exercise relative to rest', fontsize = 15)
plt.title('Slope Vs Oldpeak', fontsize = 15)


# Analysis on **ca** - number of major vessels (0-3) colored by flourosopy

# In[ ]:


plt.figure(figsize = (5,5))
sns.countplot(data['ca'])
plt.xlabel('number of major vessels (0-3) colored by flourosopy', fontsize = 15)
plt.ylabel('Frequency', fontsize = 15)


# Analysis on Thal

# In[ ]:


plt.figure(figsize = (5,5))
sns.countplot(data['thal'])
plt.xlabel('Blood Defective Type', fontsize = 15)
plt.ylabel('Frequency', fontsize = 15)


# In[ ]:


plt.figure(figsize = (10,8))
sns.set(style = 'white', palette = 'muted', color_codes = True)
sns.swarmplot(x = 'thal', y = 'chol', hue = 'sex', data = data)
plt.xlabel('Blood Defective Type', fontsize = 15)
plt.ylabel('serum cholestoral in mg/dl', fontsize = 15)
plt.title('Thal Vs Chol', fontsize = 15)


# In[ ]:


plt.figure(figsize = (10,7))
sns.violinplot(x = data['thal'], y = data['thalach'])
plt.xlabel('Blood Defective Type', fontsize = 12)
plt.ylabel('maximum heart rate achieved', fontsize = 12)


# **Target** Analysis 

# In[ ]:


plt.figure(figsize = (5,5))
sns.countplot(data['target'])
plt.xlabel('Target', fontsize = 15)
plt.ylabel('Frequency', fontsize = 15)


# In[ ]:


plt.figure(figsize=(10, 5))

#exercise induced angina - Males
#1 = yes, 0 = no
plt.subplot(1,2,1)
sns.countplot(data[data['sex']==1]['target'])
plt.xlabel('Target - Males', fontsize = 15)
plt.ylabel('Number of Males', fontsize = 15)

#exercise induced angina - Females
#1 = yes, 0 = no
plt.subplot(1,2,2)
sns.countplot(data[data['sex']==0]['target'])
plt.xlabel('Target - Females', fontsize = 15)
plt.ylabel('Number of Females', fontsize = 15)


# In[ ]:


sns.set(style = 'white', palette = 'bright', color_codes = True)
sns.catplot(x = 'target', y = 'chol', hue = 'sex', height = 7, aspect = 1.5, data = data)
plt.xlabel('Target', fontsize = 12)
plt.ylabel('serum cholestoral in mg/dl', fontsize = 12)
plt.title('Target Classification wrt resting BP', fontsize = 15)


# In[ ]:


pd.crosstab(data.age,data.target).plot(kind='bar',figsize=(20,6))


# In[ ]:


pd.crosstab(data.thalach,data.target).plot(kind='bar',figsize=(20,8))


# In[ ]:


plt.figure(figsize = (20,8))

plt.subplot(1,3,1)
sns.violinplot(x = 'target', y = 'trestbps', split = True, hue = 'sex', data = data, palette="Set2")
plt.xlabel('Target', fontsize = 12)
plt.ylabel('resting blood pressure', fontsize = 12)
plt.title('Target Classification wrt resting BP', fontsize = 15)

plt.subplot(1,3,2)
sns.violinplot(x = 'target', y = 'thalach', split = True, hue = 'sex', data = data, palette="Set2")
plt.xlabel('Target', fontsize = 12)
plt.ylabel('maximum heart rate achieved', fontsize = 12)
plt.title('Target Classification wrt maximum heart rate', fontsize = 15)

plt.subplot(1,3,3)
sns.violinplot(x = 'target', y = 'oldpeak', split = True, hue = 'sex', data = data, palette="Set2" )
plt.xlabel('Target', fontsize = 12)
plt.ylabel('Oldpeak', fontsize = 12)
plt.title('Target Classification wrt Oldpeak', fontsize = 15)


# In[ ]:




