#!/usr/bin/env python
# coding: utf-8

# <h3> The dataset used is of penguins with information like species, island, culmen_length etc. </h3>
# 
# Source of data [github](https://github.com/allisonhorst/palmerpenguins)

# This is an attempt to explore the dataset, handle the missing values and classify them into their species by identifying the useful features.

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


# <h4>Sidetable - is a new package that helps us in getting useful summary tables of the pandas DataFrame.</h4>
# 
# source :- https://github.com/chris1610/sidetable#caveats
# 
# A nice youtube tutorial briefing about this : https://www.youtube.com/watch?v=BoIDhAxdO5s&t=4s

# In[ ]:


get_ipython().system('pip install sidetable')


# In[ ]:


#Import libraries
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
import sidetable
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, accuracy_score  
from math import sqrt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


# <h3>Reading the CSV file to a dataframe</h3>

# In[ ]:


df = pd.read_csv('/kaggle/input/palmer-archipelago-antarctica-penguin-data/penguins_size.csv')
df.head(2)
#len(df) 


# <h3>Understanding the data.</h3>

# In[ ]:


# to view few metrics of  columns
df.describe(include="all")


# In[ ]:


#to identify the unique values in any column
df['sex'].value_counts()


# <h3>Handling Missing Values</h3>

# In[ ]:


#Replace the null/junk rows of the column Sex with its mode
mode_sex = df['sex'].mode()[0]  
df['sex'].fillna(mode_sex,inplace=True)
df['sex'] = df['sex'].str.replace(".",mode_sex)


# In[ ]:


# Filling null values of culmenlen, culmendepth, flipper_length_mm and body_mass_g by their mean 
# grouped by species.

df['culmen_length_mm'].fillna(df.groupby('species')['culmen_length_mm'].transform('mean'),inplace=True)
df['culmen_depth_mm'].fillna(df.groupby('species')['culmen_depth_mm'].transform('mean'),inplace=True)
df['flipper_length_mm'].fillna(df.groupby('species')['flipper_length_mm'].transform('mean'),inplace=True)
df['body_mass_g'].fillna(df.groupby('species')['body_mass_g'].transform('mean'),inplace=True)


# In[ ]:


#After handling the empty values
df.describe(include="all") 


# <h3>Data Visualization</h3>

# In[ ]:


#Sideplot is a combination of value_counts and crosstab.
print(df.stb.freq(['species']))
df.stb.freq(['species']).Count.plot(kind='bar',legend=True)
plt.xlabel('Species')
plt.show()

#Understanding the counts of each specie present in our dataset


# In[ ]:


print(df.stb.freq(['sex']))
df.stb.freq(['sex']).Count.plot(kind='bar',color='r', legend=True)
plt.xlabel('Sex')
plt.show()


# In[ ]:


sns.countplot(x="species", hue="sex", data=df)
plt.show()


# In[ ]:


#Box plots would help us identify if there any outliers and about percenatge of data above/below the median etc
f, axes = plt.subplots(1, 4)
plt.subplots_adjust(right=2)
sns.set(style="whitegrid")
sns.boxplot(  x = "culmen_length_mm", data=df,  ax=axes[0])
#plt.xlabel("culmen_length")
sns.boxplot(  x= "culmen_depth_mm", data=df, ax=axes[1])
sns.boxplot(  x= "flipper_length_mm", data=df,   ax=axes[2])
sns.boxplot(  x= "body_mass_g", data=df,   ax=axes[3])
plt.show()


# In[ ]:


# Pair Plot below helps us understand the relationship between all the features.
sns.pairplot(df,hue='species')
plt.show()


# In[ ]:


#converting species to Categories to help us for our classification.
df['species'] = df['species'].astype('category')
df['species'] = df['species'].cat.codes
df['species'].unique()


# <h3> Modelling - To predict the species based on the features.</h3>

# From the above pairplot, it looks like culmen_length and flipper_length would help us classify into respective classes (here, species) better. So, retaining only these two columns as of now and checking the accuracy.

# In[ ]:


X =  df.drop(['species','island','sex','culmen_depth_mm','body_mass_g'],axis=1)


# In[ ]:


#defining the class
y  = df['species']


# In[ ]:


#Splitting the data into train and test (70-30 respectively)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,stratify=y,random_state=42)


# Using GridSearch CV to determine the best hyper parameter i.e. "K"

# In[ ]:


knn2 = KNeighborsClassifier()
#Creating a dictionary of neighbours 
neighbours= {'n_neighbors': np.arange(1, 5)}
knn_cv = GridSearchCV(knn2, neighbours, cv=5)
#fit model to data
knn_cv.fit(X_train, y_train)


# In[ ]:


#gives the n for the best score
print(knn_cv.best_params_)
print(knn_cv.best_score_)


# To Visualize the decision boundary.
# 
# Ref - https://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html

# In[ ]:


from matplotlib.colors import ListedColormap


# In[ ]:


h = 0.1
x_min, x_max = X_train.iloc[:,0].min() - .5, X_train.iloc[:,0].max() + .5
y_min, y_max = X_train.iloc[:,1].min() - .5, X_train.iloc[:,1].max() + .5
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
Z = knn_cv.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the prediction into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1, figsize=(6, 5))
#plt.set_cmap(plt.cm.Paired)
plt.pcolormesh(xx, yy, Z,cmap=cmap_light)

# Plot training points
plt.scatter(X_train.iloc[:,0], X_train.iloc[:,1],c=y_train, cmap=cmap_bold )
plt.xlabel('culmen_length')
plt.ylabel('flipper_length')

plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xticks(())
plt.yticks(())

plt.show()


# <h3>Confusion Matrix and accuracy on the test data<h3>

# In[ ]:


y_predict = knn_cv.predict(X_test)
print(confusion_matrix(y_test,y_predict))
print(accuracy_score(y_test,y_predict))


# PS : Would love to hear your feedback :) 
