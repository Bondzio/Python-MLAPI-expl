#!/usr/bin/env python
# coding: utf-8

# # Diabetes Classification Using KNN
# This is my first ever project that I have shared. I am new in this field. I am looking forward to your advice. Thank you.

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


df = pd.read_csv('/kaggle/input/pima-indians-diabetes-database/diabetes.csv')
df.head()


# In[ ]:


df.dtypes


# In[ ]:


df.describe()


# # Data Wrangling
# From statistics descriptive, we know that the minimum value of several features is 0. For several features such as Glucose, BloodPressure, SkinThickness, Insulin, and BMI which is impossible. I almost trapped by this thinking there's no NaN value. TO make the data cleaning easier, I changed 0 value to NaN.

# In[ ]:


#df_train is a clean version of df
df_train = df


# In[ ]:


NaN_var = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
df_train[NaN_var] = df_train[NaN_var].replace(0, np.nan) #replace the 0 value of NaN_var with NaN
df_train.head()


# This is the histogram plot that show the distribution of the data.

# In[ ]:


p = df_train.hist(figsize=(20,10))


# In[ ]:


df_train.isnull().sum()


# I replace the the NaN values with its mean

# In[ ]:


df_train['Glucose'] = df_train['Glucose'].replace(np.nan, df_train['Glucose'].mean())
df_train['BloodPressure'] = df_train['BloodPressure'].replace(np.nan, df_train['BloodPressure'].mean())
df_train['SkinThickness'] = df_train['SkinThickness'].replace(np.nan, df_train['SkinThickness'].mean())
df_train['Insulin'] = df_train['Insulin'].replace(np.nan, df_train['Insulin'].mean())
df_train['BMI'] = df_train['BMI'].replace(np.nan, df_train['BMI'].mean())
df_train.head()


# The distribution plot with the replaced value

# In[ ]:


p = df_train.hist(figsize=(20,10))


# # EDA (Exploratory Data Analysis)

# In[ ]:


from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

cat_variables = df_train.drop(['Outcome'],axis=1).columns
f = pd.melt(df_train, value_vars=cat_variables)
g = sns.FacetGrid(f, col="variable",  col_wrap=4, sharex=False, sharey=False, size = 5)
g = g.map(sns.distplot, "value", fit=stats.norm)


# In[ ]:


x_var = "Outcome"
fig, axes = plt.subplots(2,4, figsize=(20,10))
axes = axes.flatten()

i = 0
for t in cat_variables:
    ax = sns.boxplot(x=x_var, y=t, data=df, orient='v', ax=axes[i])
    i +=1


# In[ ]:


sns.pairplot(df_train, hue = 'Outcome')


# In[ ]:


corr = df.corr()
fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corr, vmax=1, annot=True,square=True);
plt.show()


# In[ ]:


print(corr.iloc[-1].sort_values(ascending=False).drop("Outcome").head(10))
#I am using the features with more than 0.1 correlation, but it seems like it means all features.
var = (corr.iloc[-1].sort_values(ascending=False).drop("Outcome")>0.1).index


# In[ ]:


out = df_train.Outcome.value_counts()
print(out)
print(out/df_train.shape[0])
out.plot(kind='bar')
plt.show()


# ### Standardize
# I am using normal standardization. Standardization is used to faster the training iteration.

# In[ ]:


from sklearn.preprocessing import StandardScaler 


# In[ ]:


scaler = StandardScaler()
X = pd.DataFrame(scaler.fit_transform(df_train[var]), columns=var)
X.head()


# # Training

# In[ ]:


from sklearn.model_selection import train_test_split
y = df['Outcome'].values
x_train, x_test, y_train, y_test = train_test_split(X,y, random_state=123, test_size=0.3, stratify=y)


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier

train_score=[]
test_score=[]
for i in range(1,26):
    knn = KNeighborsClassifier(n_neighbors = i)
    knn.fit(x_train,y_train)
    
    train_score.append(knn.score(x_train,y_train))
    test_score.append(knn.score(x_test,y_test))
    
loc = np.where(train_score==max(train_score))
print('Max train score: {} and K = {}' .format(max(train_score), loc[0][0]+1))

loc = np.where(test_score==max(test_score))
print('Max test score: {} and K = {}' .format(max(test_score), loc[0][0]+1))


# In[ ]:


plt.figure(figsize=(15,5))
plt.plot(range(1,i+1), train_score, label='train set')
plt.plot(range(1,i+1), test_score, label='test set')
plt.legend()
plt.show()


# In[ ]:


knn = KNeighborsClassifier(15)

knn.fit(x_train,y_train)
knn.score(x_test,y_test)


# # Model Performance Analysis
# I am using confusion matrix evaluate the model performance. More infos about confusion matrix can be read <a href= "https://towardsdatascience.com/demystifying-the-confusion-matrix-d8ee2497da4d">here</a>

# In[ ]:


from sklearn.metrics import confusion_matrix

y_pred = knn.predict(x_test)
confusion_matrix(y_test,y_pred)
pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True)


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

