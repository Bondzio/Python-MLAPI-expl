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


n_array = np.array([[1,2,3], [231,134,34], [1243,34,4321]])
n_array.ndim


# In[ ]:


print (n_array.shape)
print (n_array.size)
n_array.dtype.name


# In[ ]:


a = np.array([1,23,3,34,2])
b = np.array([0,23,1,22,3])
c = a - b
print (c)
c


# In[ ]:


print (b < 2)


# In[ ]:


a*b


# In[ ]:


np.dot(a,b)


# In[ ]:


a = np.array([[1,3,4], [2,4,4], [3,5,3]])
b = np.array([[2,3,5], [1,2,4], [1,2,3]])
a*b


# In[ ]:


np.dot(a,b)


# In[ ]:


a.shape


# In[ ]:


a.ndim


# In[ ]:


print (a)
a[2,1]


# In[ ]:


c = a.ravel()


# In[ ]:





# In[ ]:


c.shape


# In[ ]:


n = np.array([[1,2,3], [231,134,34], [1243,34,4321], [2,3,1]])


# In[ ]:


n.ravel()


# In[ ]:


n.shape = 6,2


# In[ ]:


c.shape = 3,3


# In[ ]:


c


# In[ ]:


c.transpose()


# In[ ]:


d = {'a':'er','b':2,'c':3}
pd.Series(d)


# In[ ]:


d = {'c1': pd.Series(['A','B','C']), 'c2': pd.Series([2,3,4])}
df = pd.DataFrame(d)
df


# In[ ]:


d = {'c1': ['A','B','C'], 'c2': [1,2,3.]}
df = pd.DataFrame(d)
print (df)


# In[ ]:


panel = {'Item1': pd.DataFrame(np.random.randn(2,3)), 'Item2': pd.DataFrame(np.random.randn(3,2))}
df = pd.Panel(panel)
df.to_frame()


# In[ ]:


np.random.randn(2,3)


# In[ ]:


np.random.randn(3,2)


# In[ ]:


d = pd.read_csv('../input/Student_Weight_Status_Category_Reporting_Results__Beginning_2010.csv')


# In[ ]:


d.head()


# In[ ]:


d[0:5]['Percent Overweight']


# In[ ]:


from scipy.stats import binom
import matplotlib.pyplot as plt


# In[ ]:


fig, ax = plt.subplots(1,1)
x = range(10)
n, p = 10, .5
rv = binom(n,p)
ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-',lw=2, label='Probability')
ax.legend(loc='best', frameon=False)
plt.show()


# In[ ]:


from scipy.stats import poisson
rv = poisson(20)
rv.pmf(23)


# In[ ]:


from scipy.stats import bernoulli


# In[ ]:


bernoulli.rvs(.7,size=100)


# In[ ]:



classscore = np.random.normal(50,10,60).round()
classscore


# In[ ]:


plt.hist(classscore,1000, normed=True)
plt.show()


# In[ ]:


from scipy import stats
stats.zscore(classscore)


# In[ ]:



df  = pd.read_csv("../input/titanic-training-dataset/titanic-training-data.csv")


# In[ ]:


import pylab as plt


# In[ ]:


df['Pclass'].isnull().value_counts()


# In[ ]:


print (df.columns)
df['Survived'].isnull().value_counts()


# In[ ]:


# Passangers survived in each class (out of 1,2,3)
survivors = df.groupby('Pclass')['Survived'].agg(sum)


# In[ ]:


survivors


# In[ ]:


# Total passangers in each class
total_passengers = df.groupby('Pclass')['PassengerId'].count()
total_passengers


# In[ ]:


survivor_percentage = survivors/total_passengers
survivor_percentage


# In[ ]:


# Plotting the total number of survivors
fig = plt.figure()
ax = fig.add_subplot(111)
rect = ax.bar(survivors.index.values.tolist(), survivors, color='blue', width=.5)
ax.set_ylabel('No. of survivors')
ax.set_title('Total number of survivors based on Pclass')
plt.show()


# In[ ]:


# Plotting the % of survivors in each class
fig = plt.figure()
ax = fig.add_subplot(111)
rect = ax.bar(survivor_percentage.index.values.tolist(), survivor_percentage, width=.5, color='Red')
ax.set_ylabel('% of survivors')
ax.set_title('% of Survivors based on Pclass')
plt.show()


# **What is the distribution of survivors based on gender among the various classes?**

# In[ ]:


# printing all the columns
df.columns


# In[ ]:


# Checking for the NUll values
df['Sex'].isnull().count()


# In[ ]:


# Male passangers survived in each class
male_sur = df[df['Sex'] == 'male'].groupby('Pclass')['Survived'].agg(sum)

# Total Male passengers in each class
male_total = df[df['Sex'] == 'male'].groupby('Pclass')['PassengerId'].count()
male_total


# In[ ]:


male_perc_sur = male_sur/male_total


# In[ ]:


male_perc_sur


# In[ ]:


# Female Passengers survived in each class
female_survivors = df[df['Sex'] == 'female'].groupby('Pclass')['Survived'].agg(sum)
#Total Female Passengers in each class
female_total_passengers = df[df['Sex'] == 'female'].groupby('Pclass')['PassengerId'].count()
female_survivor_percentage = female_survivors /female_total_passengers


# In[ ]:


female_survivor_percentage


# In[ ]:


# Plotting
fig = plt.figure()
ax = fig.add_subplot(111)
index = np.arange(male_sur.count())
bar_width = .35
rect1 = ax.bar(index +  bar_width, male_sur, bar_width, label='Men')
rect2 = ax.bar(index , female_survivors, bar_width, color='y', label='Women')
ax.set_ylabel('Surivor Numbers')
ax.set_title('Male and Female Survivors based on Pclass')
plt.show()


# In[ ]:


df.columns


# **What is the distribution of nonsurvivors among the various classes who have family aboard the ship?**

# In[ ]:


# Checking the null values
df['SibSp'].isnull().value_counts()


# In[ ]:


df['Parch'].value_counts()


# In[ ]:


df['Parch'].isnull().value_counts()


# In[ ]:


# Total number of survivors in each class
non_survivors = df[(df['SibSp'] > 0) | (df['Parch'] > 0) & (df['Survived'] == 0)].groupby('Pclass')['Survived'].agg('count')


# In[ ]:


non_survivors


# In[ ]:


non_survivors_percentage = non_survivors / total_passengers
non_survivors_percentage


# In[ ]:


# Total number of non survivors with family based on class
fig = plt.figure()
ax = fig.add_subplot(111)
rect = ax.bar(non_survivors_percentage.index.values.tolist(), non_survivors_percentage, width=.5, color='r')
ax.set_title('Non-survivors % with family based on class')
ax.set_ylabel('No. of non survivors')
plt.show()


# In[ ]:





# **What was the survival percentage among different age groups?**

# In[ ]:


# Getting the columns and checking the null values of Age
df.columns


# In[ ]:


df['Age'].isnull().value_counts()


# In[ ]:


# Define the age binning interval
age_bin = [0,16,25,40,60,100]
# creating the bins
df['Age_bin'] = pd.cut(df.Age, bins=age_bin)
df.columns


# In[ ]:


#Removing null rows
d_temp = df[np.isfinite(df['Age'])] # Removing NA instances
# Number of survivors based on Age bin
survivors = d_temp.groupby('Age_bin')['Survived'].agg(sum)

#Total passengers in each bin
total_passengers = d_temp.groupby('Age_bin')['Survived'].agg('count')
total_passengers


# In[ ]:


# Plotting the Pi chart of total passengers in each bin
plt.pie(total_passengers, labels=total_passengers.index.values.tolist(),autopct='%1.1f%%', shadow=True, startangle=90)
plt.title('Total passengers in each Age groups')
plt.show()


# In[ ]:


# Plotting the Pi chart of total passengers in each bin
plt.pie(total_passengers, labels=total_passengers.index.values.tolist(), shadow=True, startangle=90)
plt.title('Total passengers in each Age groups')
plt.show()


# In[ ]:


#Plotting the pie chart of percentage passengers in each bin
plt.pie(survivors, labels=survivors.index.values.tolist(),autopct='%1.1f%%', shadow=True, startangle=90)
plt.title('Survivors in different age groups')
plt.show()


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


plt.plot([1,2,3,4], [1,4,9,16])
plt.show()


# In[ ]:


import pylab as plt


# In[ ]:


plt.plot([1,2,3,4], [1,4,9,16])
plt.show()


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


line, = plt.plot([1,2,3,4], [1,4,9,16], linewidth=2.5)
line.set_linestyle('--')
plt.setp(line, color='r', linewidth=1)
plt.show()


# In[ ]:


# Creating multiple plots
p1 = np.arange(0.0, 30.0, 0.1)
plt.subplot(211)
plt.plot(p1, np.sin(p1)/p1, 'b--')
plt.subplot(212)
plt.plot(p1, np.cos(p1), 'r--')
plt.show()


# In[ ]:


# Playing with text
r = np.random.random_sample((5,))
print (np.arange(len(r)))
plt.bar(np.arange(len(r)), r)
plt.xlabel('Indices')
plt.ylabel('Values')
plt.text( 1, .7, r'$\mu=' + str(np.round(np.mean(r),2)) + '$')
plt.show()


# In[ ]:


ax = plt.subplot(111)
t = np.arange(0.0, 5.0, .01)
s = np.cos(2*np.pi*t)
line, = plt.plot(t,s,lw=2)
plt.annotate('local max', xy=(2,.5), xytext=(3,.5), arrowprops=dict(facecolor='yellow', shrink=.5), )

plt.show()


# In[ ]:


# Styling your plots
plt.style.use('ggplot')
plt.plot([1,2,3,4], [1,4,9,16])
plt.show()


# In[ ]:


plt.style.use('fivethirtyeight')
plt.plot([1,2,3,4], [1,4,9,16])
plt.show()


# In[ ]:


with plt.style.context(('dark_background')):
    plt.plot([1,2,3,4], [1,4,9,16])
plt.show()


# In[ ]:


# Creating Box plots
# Creating some data
np.random.seed(10)
box1 = np.random.normal(100,10,200)
box2 = np.random.normal(80,30,200)
box3 = np.random.normal(90,20,200)

box_list = [box1, box2, box3]
# Creating the box plot
b = plt.boxplot(box_list)


# In[ ]:


b = plt.boxplot(box_list, patch_artist='True')


# In[ ]:


## change outline color, fill color and linewidth of the boxes
for box in b['boxes']:
    # Change outline color
    box.set(color='#7570b3', linewidth=2)
    # Change filled color
    box.set(facecolor = '#1b9e77')


# In[ ]:


import nltk


# In[ ]:




