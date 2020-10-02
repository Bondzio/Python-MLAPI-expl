#!/usr/bin/env python
# coding: utf-8

# # World Happiness 

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
plt.rcParams['figure.figsize'] = (7.0,7.0)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ## Reading The Data

# In[ ]:


data_happy = pd.read_csv('/kaggle/input/world-happiness-report-2019/world-happiness-report-2019.csv')
data_happy.head()


# In[ ]:


data_happy.columns


# ## Renaming the columns

# In[ ]:


data_happy.columns = ['country', 'L', 'SD', 'Positive_affect', 'Negative_affect','Social_support',
                      'Freedom','Corruption','Generosity','GDP', 'Healthy_life_expectancy']


# In[ ]:


data_happy.head()


# In[ ]:


#describing the data
data_happy.describe()


# ## Handling the missing values and null values
# 

# In[ ]:


data_happy.isnull().sum()


# In[ ]:


#droping the rows with null values
data_happy = data_happy.dropna(0)


# In[ ]:


data_happy.isnull().sum()


# In[ ]:


# scatter plot to visualize the relation between positive_affect and negative_affect
plt.scatter(data_happy['Positive_affect'],data_happy['Negative_affect'])
plt.xlabel('positive affect', fontsize=15)
plt.ylabel('negative affect', fontsize=15)
plt.title('positive vs negative', fontsize=20)
plt.show()


# ## Plotting bar graphs of Positive_affect and Negative_affect Countrywise

# In[ ]:


df1 = data_happy.groupby('country').agg({'Positive_affect':'sum'}).sort_values(by='Positive_affect', ascending = False)
df1 =df1.head(10)


# In[ ]:


sb.set_style('whitegrid')
sb.barplot(y = df1.index,x = df1['Positive_affect'], palette = 'Blues_r')
plt.title('countries with positive emotions', fontsize = 20)
plt.show()


# In[ ]:


df2 = data_happy.groupby('country').agg({'Negative_affect':'sum'}).sort_values(by='Negative_affect', ascending = False)
df2 = df2.head(10)


# In[ ]:


sb.set_style('whitegrid')
sb.barplot(y = df2.index,x = df2['Negative_affect'], palette = 'Reds_r')
plt.title('countries with negative emotions', fontsize = 20)
plt.show()


# ## Plotting scatter with respect to healthy life expenctancy

# In[ ]:


plt.scatter(data_happy['L'],data_happy['Healthy_life_expectancy'])
plt.xlabel('L',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('L vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['L'],data_happy['Healthy_life_expectancy'])[0,1]
print("correlation coefficeint:",corr)


# In[ ]:


plt.scatter(data_happy['Social_support'],data_happy['Healthy_life_expectancy'])
plt.xlabel('Social_support',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('Social_support vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['Social_support'],data_happy['Healthy_life_expectancy'])[0,1]
print("correlation coefficeint:",corr)


# In[ ]:


sb.regplot(data_happy['Freedom'],data_happy['Healthy_life_expectancy'])
plt.xlabel('Freedom',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('Freedom vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['Freedom'],data_happy['Healthy_life_expectancy'])[0,1]
print("correlation coefficeint:",corr)


# In[ ]:


sb.regplot(data_happy['Corruption'],data_happy['Healthy_life_expectancy'])
plt.xlabel('Corruption',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('Corruption vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['Corruption'],data_happy['Healthy_life_expectancy'])[0,1]
print("correlation coefficeint:",corr)


# In[ ]:


sb.regplot(data_happy['Generosity'],data_happy['Healthy_life_expectancy'])
plt.xlabel('Generosity',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('Generosity vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['Generosity'],data_happy['Healthy_life_expectancy'])[0,1]
print("correlation coefficeint:",corr)


# In[ ]:


plt.scatter(data_happy['GDP'],data_happy['Healthy_life_expectancy'])
plt.xlabel('GDP',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('GDP vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['GDP'],data_happy['Healthy_life_expectancy'])[0,1]


# In[ ]:


sb.regplot(data_happy['Positive_affect'],data_happy['Healthy_life_expectancy'])
plt.xlabel('Positive_affect',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('L vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['Positive_affect'],data_happy['Healthy_life_expectancy'])[0,1]
print("correlation coefficeint:",corr)


# In[ ]:


sb.regplot(data_happy['Negative_affect'],data_happy['Healthy_life_expectancy'])
plt.xlabel('Negative_affect',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('Negative_affect vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['Negative_affect'],data_happy['Healthy_life_expectancy'])[0,1]
print("correlation coefficeint:",corr)


# In[ ]:


plt.scatter(data_happy['SD'],data_happy['Healthy_life_expectancy'])
plt.xlabel('SD',fontsize = 12)
plt.ylabel('Healthy_life_expectancy',fontsize = 12)
plt.title('SD vs Healthy_life_expectancy', fontsize = 18)

corr = np.corrcoef(data_happy['SD'],data_happy['Healthy_life_expectancy'])[0,1]
print("correlation coefficeint:",corr)


# ## Test Train data spliting
# 1. **dropping unnecessary column data**

# In[ ]:


from sklearn.model_selection import train_test_split
x = data_happy.drop(['country', 'Healthy_life_expectancy', 'SD'], axis=1)
y = data_happy['Healthy_life_expectancy']


# In[ ]:


x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3, random_state = None)


# ## fitting the data in RandomForest Regression model

# In[ ]:


#importing random forest regression package
from sklearn.ensemble import RandomForestRegressor
random = RandomForestRegressor()
random.fit(x_train, y_train)
y_pred = random.predict(x_test)


# **R2 value**

# In[ ]:


print('accuraccy of linear regression on taining set:{:.2f}'.format(random.score(x_train,y_train)))
print('accuraccy of  linear regression on testing set:{:.2f}'.format(random.score(x_test,y_test)))


# In[ ]:


plt.scatter(y_test,y_pred,color='c')
plt.xlabel('y test data')
plt.ylabel(' predicted data')
plt.title('predicted test data regression graph')
plt.show()

