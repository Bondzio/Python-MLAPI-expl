#!/usr/bin/env python
# coding: utf-8

# This is an analysis of gun deaths in USA and also application of the Knearest neighbors algorithm to predict the intents.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn import cross_validation, preprocessing, neighbors

# Any results you write to the current directory are saved as output.


# Here i'm trying to predict the intent of a gun death by taking into consideration the features as inputs.
# I'm going to convert all texts into unique numbers.

# In[ ]:


import pandas as pd
import numpy as np
from sklearn import cross_validation, preprocessing, neighbors

df = pd.read_csv('../input/guns.csv')

df_predict = df.fillna(-99999)



def convert_text(df):
    columns = list(df)
    for column in columns:
        text_digit_vals = {}
        def convert_to_int(val):
            return text_digit_vals[val]
        if df[column].dtype != np.int64 and df[column].dtype != np.float64:
            column_contents = df[column].values.tolist()
            unique_elements = set(column_contents)
            count = 0
            for unique in unique_elements:
                if unique not in text_digit_vals:
                    text_digit_vals[unique] = count
                    count += 1
            print(text_digit_vals)
            df[column] = list(map(convert_to_int, df[column]))
    return df

df_predict = convert_text(df_predict)

df_predict['intent'].replace(-9999999,4, inplace=True)
print(df_predict.head())

y = np.array(df_predict['intent'])
df_predict.drop('intent', 1, inplace=True)
X= np.array((df_predict).astype(float))
X= preprocessing.scale(X)

X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y, test_size=0.05)

clf = neighbors.KNeighborsClassifier(n_neighbors=5)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
print('The % accuracy of the algorithm is: ', accuracy)


# In[ ]:


ANALYSIS WITH CHARTS


# In[ ]:


import seaborn as sns

df = df = pd.read_csv('../input/guns.csv')
sns.countplot(x = 'month', data=df, palette="husl")
sns.plt.show()


# In[ ]:


import seaborn as sns
from collections import Counter

c = Counter(df['month'])
value= []
months = []
for i in c:
    value.append(c[i])
    months.append(i)
sns.pointplot(months, value)
sns.plt.xlabel('The Months')
sns.plt.ylabel('The Number of times deaths occured by guns in each month')
 


# In both graphs above it shows that more death occurred in the month of August with around 9000 deaths
# while the least death occurred during the month of February. 
# There should be some explanation for such plunge in gun deaths in the month of February. 
# 

# In[ ]:


y = Counter(df['year'])
value_y = []
year = []
for i in y:
    value_y.append(y[i])
    year.append(i)
sns.pointplot(year, value_y)
sns.plt.xlabel("Year")
sns.plt.ylabel("The Number of times death occured in each year")
  


# In the plot above most deaths occurred during the year 2013 leading to an increase in deaths (0.22%  relative to 2012), maybe due to some actions taken by the government the deaths reduced by 0.11%.
# More Analysis could be done if data sets for subsequent years were available.

# In[ ]:


sns.countplot( y = 'month', hue='intent', data=df, palette='Greens_d')
sns.plt.show()


# This graph shows that more deaths were as a result of Suicide while the least was a tagged "undetermined".

# In[ ]:


#Really not sure of the name given to the age group here. Just came up with something.
#Sorted the DataFrame in ascending order with respect to the age.

#filled the NaN with 44.0 which is the average age of the age column
df['age'].fillna(44.0, inplace=True)

df_sort= df.sort_values(by='age')

def map_age(df):
    map_dict = {}
    classification = ['childhood', 'adolescent', 'youth', ' adulthood', 'old age']
    col_cont = df['age'].values.tolist()
    items = set(col_cont)
    def age_converter(col):
        return map_dict[col]
    for ages in items:
        if ages <= 14:
            map_dict[ages] = classification[0]
        if ages >14 and ages<=24:
            map_dict[ages]=classification[1]
        if ages >24 and ages<=54:
            map_dict[ages]=classification[2]
        if ages > 54 and ages<=64:
            map_dict[ages]=classification[3]
        if ages > 64 :
            map_dict[ages]=classification[4]
    df['age']= list(map(age_converter, df['age']))
    return df['age']

age_df = map_age(df_sort)
df_sort.replace(['age'], ['age_df'],inplace=True) 
print(df_sort.head())

sns.countplot(x='age', data=df_sort, hue='intent', palette="Blues")
sns.plt.show()


# The plot 

# In[ ]:


sns.countplot(x= 'sex', data=df_sort, hue='age', palette="GnBu_d")


# The plot above shows:
# More gun deaths for Male with the age group(25-54)years same goes for the Female but more death occurred in Male.

# In[ ]:


sns.countplot(x='sex', hue= 'intent', data = df_sort, palette="Paired")
sns.plt.show()


# In[ ]:


sns.countplot( x = 'month', hue='intent', data=df_sort, palette='Greens_d')
sns.plt.show()


# In[ ]:


g = sns.FacetGrid(df, col='year', size=5, aspect=0.7)
g.map(sns.barplot,'age','race')


# In[ ]:


g = sns.FacetGrid(df, col='year', size=5, aspect=0.7)
g.map(sns.barplot,'age','intent')


# ***
# 
# Main Point:
# -----------
# 
# ***
# There were more deaths in the month of August.
# More Males were involved than Females.
# Sex, age, education are very important in making predictions.They affect it a lot.
# Those within the age bracket of 25-54 were more involved in gundeaths.
# More gun deaths were as a result of Suicide.
# 
# Thanks.
# 

# In[ ]:




