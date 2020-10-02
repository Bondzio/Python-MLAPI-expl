#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import regex as re
pd.options.display.max_columns = 999
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
import matplotlib.pyplot as plt
import matplotlib
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
from sklearn import svm
from sklearn.model_selection import train_test_split


# In[ ]:


df = pd.read_csv('../input/2016 School Explorer.csv')
df.shape


# In[ ]:


df.head()


# In[ ]:


df['School Income Estimate'] = df['School Income Estimate'].astype(str)
df['School Income Estimate'] = [re.sub("\D", "", s) for s in df['School Income Estimate']]
df = df.replace('', np.nan, regex=True)
df['School Income Estimate'] = [float(x) for x in df['School Income Estimate']]
df.sort_values(by='School Income Estimate')


# In[ ]:


list(df.columns)


# In[ ]:


df['Grade 3 passing rate'] = df['Grade 3 ELA 4s - All Students'].astype(float) /df['Grade 3 ELA - All Students Tested'].astype(float)
df['Grade 4 passing rate'] = df['Grade 4 ELA 4s - All Students'].astype(float) /df['Grade 4 ELA - All Students Tested'].astype(float)
df['Grade 5 passing rate'] = df['Grade 5 ELA 4s - All Students'].astype(float) /df['Grade 5 ELA - All Students Tested'].astype(float)
df['Grade 6 passing rate'] = df['Grade 6 ELA 4s - All Students'].astype(float) /df['Grade 6 ELA - All Students Tested'].astype(float)
df['Grade 7 passing rate'] = df['Grade 7 ELA 4s - All Students'].astype(float) /df['Grade 7 ELA - All Students Tested'].astype(float)
df['Grade 8 passing rate'] = df['Grade 8 ELA 4s - All Students'].astype(float) /df['Grade 8 ELA - All Students Tested'].astype(float)
df['Grade 4 math passing rate'] = df['Grade 4 Math 4s - All Students'].astype(float) /df['Grade 4 Math - All Students Tested'].astype(float)
df['Grade 5 math passing rate'] = df['Grade 5 Math 4s - All Students'].astype(float) /df['Grade 5 Math - All Students Tested'].astype(float)
df['Grade 6 math passing rate'] = df['Grade 6 Math 4s - All Students'].astype(float) /df['Grade 6 Math - All Students Tested'].astype(float)
df['Grade 7 math passing rate'] = df['Grade 7 Math 4s - All Students'].astype(float) /df['Grade 7 Math - All Students Tested'].astype(float)
df['Grade 8 math passing rate'] = df['Grade 8 Math 4s - All Students'].astype(float) /df['Grade 8 Math - All Students Tested'].astype(float)


# In[ ]:


df.tail()


# In[ ]:


df['Average English passing rate'] = df.loc[:,['Grade 3 passing rate','Grade 8 passing rate']].mean(axis=1)
df['Average math passing rate'] = df.loc[:,['Grade 4 math passing rate','Grade 8 math passing rate']].mean(axis=1)


# In[ ]:


df.tail()


# Being an economist, my first suspicion is whether income is the main driver to school performance.

# In[ ]:


plt.scatter(df['School Income Estimate'], df['Average English passing rate'])
plt.show()


# In[ ]:


plt.scatter(df['School Income Estimate'], df['Average math passing rate'])
plt.show()


# Apparently not. Let's see if English and math are strongly correlated.

# In[ ]:


plt.scatter(df['Average English passing rate'], df['Average math passing rate'])
plt.show()


# That doesn't appear to be the case, with numerous outliers. We need a more thorough approach to why some schools are failing and others are succeeding.

# In[ ]:


df.sort_values(by='School Income Estimate', ascending = False).head(10)


# In[ ]:


df['Improvement'] = df['Grade 8 passing rate'] - df['Grade 3 passing rate']


# In[ ]:


df.sort_values(by='Improvement').head()


# In[ ]:


df['English passing percentile'] = df['Average English passing rate'].rank(pct=True)
df['Math passing percentile'] = df['Average math passing rate'].rank(pct=True)
df['Income percentile'] = df['School Income Estimate'].rank(pct=True)


# In[ ]:


df.head()


# In[ ]:


plt.scatter(df['English passing percentile'], df['Math passing percentile'])
plt.show()
print("There doesn't appear to be any correlation between English and math performance. More is going on here.")


# In[ ]:


list(df.columns)


# In[ ]:


def percentconverter(x):
    lambda x: float(x.strip(b"%"))/100


# In[ ]:


a = 'English passing percentile'
cols = ['Percent ELL', 'Percent Asian', 'Percent Black', 'Percent Hispanic', 'Percent Black / Hispanic', 'Percent White', 'Student Attendance Rate','Percent of Students Chronically Absent','Rigorous Instruction %','Collaborative Teachers %','Supportive Environment %','Effective School Leadership %','Strong Family-Community Ties %','Trust %']
for a in cols:
    df[a] = df[a] = df[a].str.rstrip('%').astype('float') / 100.0
df2 = df.drop(['Adjusted Grade','New?','Other Location Code in LCGMS','School Name','Location Code','Address (Full)','City','Grades','Grade Low','Grade High','Community School?','Rigorous Instruction Rating','Collaborative Teachers Rating','Supportive Environment Rating','Effective School Leadership Rating','Strong Family-Community Ties Rating','Trust Rating','Student Achievement Rating'], 1)
df2 = df2.dropna(axis = 0)
y = df2[a]
X = df2.drop([a], 1)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)
rf = RandomForestRegressor(n_jobs=-1)
rf.fit(X, y)
names = X.dtypes.index
print("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), 
             reverse=True))
print('School leadership and collaborative teaching models pull over 78% of the weight.')


# In[ ]:


a = 'Math passing percentile'
y = df2[a]
X = df2.drop([a], 1)
rf = RandomForestRegressor(n_jobs=-1)
rf.fit(X, y)
names = X.dtypes.index
print("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), 
             reverse=True))


# In[ ]:


plt.scatter(df['Collaborative Teachers %'], df['Math passing percentile'])
plt.show()
print('Not enough variation to tell at a glance.')


# In[ ]:


# Note the difference in argument order
# optionally, you can chain "fit()" to the model object
df2 = df2.drop(['Average ELA Proficiency',
 'Average Math Proficiency',
 'Grade 3 ELA - All Students Tested',
 'Grade 3 ELA 4s - All Students',
 'Grade 3 ELA 4s - American Indian or Alaska Native',
 'Grade 3 ELA 4s - Black or African American',
 'Grade 3 ELA 4s - Hispanic or Latino',
 'Grade 3 ELA 4s - Asian or Pacific Islander',
 'Grade 3 ELA 4s - White',
 'Grade 3 ELA 4s - Multiracial',
 'Grade 3 ELA 4s - Limited English Proficient',
 'Grade 3 ELA 4s - Economically Disadvantaged',
 'Grade 3 Math - All Students tested',
 'Grade 3 Math 4s - All Students',
 'Grade 3 Math 4s - American Indian or Alaska Native',
 'Grade 3 Math 4s - Black or African American',
 'Grade 3 Math 4s - Hispanic or Latino',
 'Grade 3 Math 4s - Asian or Pacific Islander',
 'Grade 3 Math 4s - White',
 'Grade 3 Math 4s - Multiracial',
 'Grade 3 Math 4s - Limited English Proficient',
 'Grade 3 Math 4s - Economically Disadvantaged',
 'Grade 4 ELA - All Students Tested',
 'Grade 4 ELA 4s - All Students',
 'Grade 4 ELA 4s - American Indian or Alaska Native',
 'Grade 4 ELA 4s - Black or African American',
 'Grade 4 ELA 4s - Hispanic or Latino',
 'Grade 4 ELA 4s - Asian or Pacific Islander',
 'Grade 4 ELA 4s - White',
 'Grade 4 ELA 4s - Multiracial',
 'Grade 4 ELA 4s - Limited English Proficient',
 'Grade 4 ELA 4s - Economically Disadvantaged',
 'Grade 4 Math - All Students Tested',
 'Grade 4 Math 4s - All Students',
 'Grade 4 Math 4s - American Indian or Alaska Native',
 'Grade 4 Math 4s - Black or African American',
 'Grade 4 Math 4s - Hispanic or Latino',
 'Grade 4 Math 4s - Asian or Pacific Islander',
 'Grade 4 Math 4s - White',
 'Grade 4 Math 4s - Multiracial',
 'Grade 4 Math 4s - Limited English Proficient',
 'Grade 4 Math 4s - Economically Disadvantaged',
 'Grade 5 ELA - All Students Tested',
 'Grade 5 ELA 4s - All Students',
 'Grade 5 ELA 4s - American Indian or Alaska Native',
 'Grade 5 ELA 4s - Black or African American',
 'Grade 5 ELA 4s - Hispanic or Latino',
 'Grade 5 ELA 4s - Asian or Pacific Islander',
 'Grade 5 ELA 4s - White',
 'Grade 5 ELA 4s - Multiracial',
 'Grade 5 ELA 4s - Limited English Proficient',
 'Grade 5 ELA 4s - Economically Disadvantaged',
 'Grade 5 Math - All Students Tested',
 'Grade 5 Math 4s - All Students',
 'Grade 5 Math 4s - American Indian or Alaska Native',
 'Grade 5 Math 4s - Black or African American',
 'Grade 5 Math 4s - Hispanic or Latino',
 'Grade 5 Math 4s - Asian or Pacific Islander',
 'Grade 5 Math 4s - White',
 'Grade 5 Math 4s - Multiracial',
 'Grade 5 Math 4s - Limited English Proficient',
 'Grade 5 Math 4s - Economically Disadvantaged',
 'Grade 6 ELA - All Students Tested',
 'Grade 6 ELA 4s - All Students',
 'Grade 6 ELA 4s - American Indian or Alaska Native',
 'Grade 6 ELA 4s - Black or African American',
 'Grade 6 ELA 4s - Hispanic or Latino',
 'Grade 6 ELA 4s - Asian or Pacific Islander',
 'Grade 6 ELA 4s - White',
 'Grade 6 ELA 4s - Multiracial',
 'Grade 6 ELA 4s - Limited English Proficient',
 'Grade 6 ELA 4s - Economically Disadvantaged',
 'Grade 6 Math - All Students Tested',
 'Grade 6 Math 4s - All Students',
 'Grade 6 Math 4s - American Indian or Alaska Native',
 'Grade 6 Math 4s - Black or African American',
 'Grade 6 Math 4s - Hispanic or Latino',
 'Grade 6 Math 4s - Asian or Pacific Islander',
 'Grade 6 Math 4s - White',
 'Grade 6 Math 4s - Multiracial',
 'Grade 6 Math 4s - Limited English Proficient',
 'Grade 6 Math 4s - Economically Disadvantaged',
 'Grade 7 ELA - All Students Tested',
 'Grade 7 ELA 4s - All Students',
 'Grade 7 ELA 4s - American Indian or Alaska Native',
 'Grade 7 ELA 4s - Black or African American',
 'Grade 7 ELA 4s - Hispanic or Latino',
 'Grade 7 ELA 4s - Asian or Pacific Islander',
 'Grade 7 ELA 4s - White',
 'Grade 7 ELA 4s - Multiracial',
 'Grade 7 ELA 4s - Limited English Proficient',
 'Grade 7 ELA 4s - Economically Disadvantaged',
 'Grade 7 Math - All Students Tested',
 'Grade 7 Math 4s - All Students',
 'Grade 7 Math 4s - American Indian or Alaska Native',
 'Grade 7 Math 4s - Black or African American',
 'Grade 7 Math 4s - Hispanic or Latino',
 'Grade 7 Math 4s - Asian or Pacific Islander',
 'Grade 7 Math 4s - White',
 'Grade 7 Math 4s - Multiracial',
 'Grade 7 Math 4s - Limited English Proficient',
 'Grade 7 Math 4s - Economically Disadvantaged',
 'Grade 8 ELA - All Students Tested',
 'Grade 8 ELA 4s - All Students',
 'Grade 8 ELA 4s - American Indian or Alaska Native',
 'Grade 8 ELA 4s - Black or African American',
 'Grade 8 ELA 4s - Hispanic or Latino',
 'Grade 8 ELA 4s - Asian or Pacific Islander',
 'Grade 8 ELA 4s - White',
 'Grade 8 ELA 4s - Multiracial',
 'Grade 8 ELA 4s - Limited English Proficient',
 'Grade 8 ELA 4s - Economically Disadvantaged',
 'Grade 8 Math - All Students Tested',
 'Grade 8 Math 4s - All Students',
 'Grade 8 Math 4s - American Indian or Alaska Native',
 'Grade 8 Math 4s - Black or African American',
 'Grade 8 Math 4s - Hispanic or Latino',
 'Grade 8 Math 4s - Asian or Pacific Islander',
 'Grade 8 Math 4s - White',
 'Grade 8 Math 4s - Multiracial',
 'Grade 8 Math 4s - Limited English Proficient',
 'Grade 8 Math 4s - Economically Disadvantaged',
 'Grade 3 passing rate',
 'Grade 4 passing rate',
 'Grade 5 passing rate',
 'Grade 6 passing rate',
 'Grade 7 passing rate',
 'Grade 8 passing rate',
 'Grade 4 math passing rate',
 'Grade 5 math passing rate',
 'Grade 6 math passing rate',
 'Grade 7 math passing rate',
 'Grade 8 math passing rate',], axis = 1)
y = df2[a]
X = df2.drop([a,'Average math passing rate'], 1)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)
model = sm.OLS(y_train, X_train, n_jobs=-1)
model = model.fit()
predictions = model.predict(X_test)

# Plot the model
plt.figure(figsize=(8,6))
plt.scatter(predictions, y_test, s=30, c='r', marker='+', zorder=10)
plt.xlabel("Predicted Values - $\hat{y}$")
plt.ylabel("Actual Values - $y$")
plt.show()

print("MSE:", mean_squared_error(y_test, predictions))


# In[ ]:


model.summary()


# In[ ]:


print("This regression is too busy to be useful.")


# In[ ]:


a = 'Effective School Leadership %'
y = df2[a]
X = df2.drop([a], 1)
rf = RandomForestRegressor(n_jobs=-1)
rf.fit(X, y)
names = X.dtypes.index
print("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), 
             reverse=True))


# In[ ]:


print("Collaborative teachers are very highly correlated with having an effective school leadership. Nothing else comes close.")


# In[ ]:


df2.corr()


# In[ ]:


a = 'Math passing percentile'
y = df2[a]
X = df2.drop([a,'Average math passing rate','Average English passing rate'], 1)
rf = RandomForestRegressor(n_jobs=-1)
rf.fit(X, y)
names = X.dtypes.index
print("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), 
             reverse=True))


# In[ ]:


a = 'English passing percentile'
y = df2[a]
X = df2.drop([a,'Average math passing rate','Average English passing rate'], 1)
rf = RandomForestRegressor(n_jobs=-1)
rf.fit(X, y)
names = X.dtypes.index
print("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), 
             reverse=True))


# In[ ]:


print("Once we clear out a lot of the variables which we determined our percentile with, we can tell that math and English are the most important variables to determine each other. We need to test only one at a time, excluding them from the next regressions.")


# In[ ]:


a = 'Math passing percentile'
y = df2[a]
X = df2.drop([a,'Average math passing rate','Average English passing rate','English passing percentile'], 1)
rf = RandomForestRegressor(n_jobs=-1)
rf.fit(X, y)
names = X.dtypes.index
print("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), 
             reverse=True))


# In[ ]:


print("Absent students and poverty are important for math.")


# In[ ]:


a = 'English passing percentile'
y = df2[a]
X = df2.drop([a,'Average math passing rate','Average English passing rate','Math passing percentile'], 1)
rf = RandomForestRegressor(n_jobs=-1)
rf.fit(X, y)
names = X.dtypes.index
print("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), 
             reverse=True))


# In[ ]:


print("Absent students and poverty are the most important variables for students being successful in Math and English.")


# In[ ]:


model = sm.OLS(y_train, X_train, n_jobs=-1)
model = model.fit()
predictions = model.predict(X_test)

# Plot the model
plt.figure(figsize=(8,6))
plt.scatter(predictions, y_test, s=30, c='r', marker='+', zorder=10)
plt.xlabel("Predicted Values - $\hat{y}$")
plt.ylabel("Actual Values - $y$")
plt.show()

print("MSE:", mean_squared_error(y_test, predictions))


# In[ ]:


model.summary()


# Now we come to the key takeaways. Once we get to the most important variables in determining how well students do in Math and English, assuming that the test scores are a good metric, we learn that alleviating poverty has the biggest impact on whether a student is going to do well on their math and English exams. Race had no significant impact when considering economics.<br />
# These studies very clearly imply that the bestt programs to increase student success are going  to be general economic development programs to raise people out of poverty. This could come from small tweaks like increase accessbility to food stamps, or raising the bar for eligibility for Medicaid, or it could come from bigger programs like a Universal Basic Income which has very wide support from economists from across the political spectrum.<br />
# No decent person wants to see children failing to learn the skills they need to be successful adults and engaged citizens, and in order to provide children the best environment possible we need to look at what programs will raise people out of poverty. There is a wide economic literature on this topic which can be used by governments across the world to improve the well being of everybody.<br />
# Let's make a better New York.<br />
# Let's make a better America.<br />
# Let's build a more just and peaceful world, driven by science and morality. This is my mission. This is what we must do.

# In[ ]:




