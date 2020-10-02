#!/usr/bin/env python
# coding: utf-8

# # Machine Learning of Titanic
# In this notebook, I will not only provide the basic steps to use machine learning knowledge to make predictions but also unite all important steps, define a interactive function, and make Titanic's machine learning more direct and clear

# ## Import the Packages We Need

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier


# ## Basic Operation about Dataframe - Prepare Data and Clean Data

# In[ ]:


train_df = pd.read_csv("../input/train.csv")
test_df = pd.read_csv("../input/test.csv")
print(train_df.head())
print(test_df.head())


# In[ ]:


# For now, We jest explore training data first. Because when I am done with the training data, We will do the same things to testing data
train_df.isnull().sum()


# In[ ]:


# First, we can find that the 'Cabin' variable has just 204 values, which is far less than other variables' values.
# So we need to remove it
train_df = train_df.drop(['Cabin'], axis = 1)
# What's more, the passengerID, Name and Ticket seem no use for further analysis. And we can remove them
train_df = train_df.drop(['PassengerId', 'Name', 'Ticket'], axis = 1)


# In[ ]:


train_df.head()


# ## Further Exploration of Training Data - Clean Data Deeperly
# In this part, we will first fill the blank values of "Age" and "Embarker". And then we will transfer some variables, such as "Sex" and "Embarked", into dummy variables. Last, we will use different kinds of plots to see whether specific variable is related with the passengers' survival

# ### Fill All Null Values

# In[ ]:


# For "Age"
min_age = train_df['Age'].min()
max_age = train_df['Age'].max()
null_values_count = train_df['Age'].isnull().sum()
age_fill_values = np.random.randint(min_age, max_age, size = null_values_count)
train_df['Age'][np.isnan(train_df['Age'])] = age_fill_values


# In[ ]:


# For "Embarked"
train_df['Embarked'].unique()


# In[ ]:


print(train_df['Embarked'][train_df['Embarked'] == 'S'].count()) # 644
print(train_df['Embarked'][train_df['Embarked'] == 'C'].count()) # 168
print(train_df['Embarked'][train_df['Embarked'] == 'Q'].count()) # 77 


# In[ ]:


# For "Embarked" variable, we can use 'S' to fill it because it has the largest frequency
train_df['Embarked'] = train_df['Embarked'].fillna('S')


# In[ ]:


train_df.count() # Make sure that all null values have been filled with some values


# ### The Relationship Among Different Variables and Survival
# When we find some variables are related to survival rate, we may keep those variables and sometime may transform them to a more suitable mode.

# #### Correlation of Every Variables

# In[ ]:


corr = train_df.corr()
sns.heatmap(corr, cmap = 'coolwarm', linewidth = 1, linecolor = 'white')
# From heatmap, we can see that there are some relations between survival and pclass, sex, age, sibsp, parch, fare and embark


# #### Pclass and Survival

# In[ ]:


pclass_df = train_df[['Survived', 'Pclass']]
fig = plt.figure(figsize = (10,5))
axes0 = plt.subplot(1,2,1)
axes0 = sns.countplot(x = 'Pclass', hue = 'Survived', data = pclass_df)
axes0.set_title('The Number of Survival Based on Class')
axes0.set_ylabel('Count')
axes0.legend(['No', 'Yes'])

survival_pclass = pclass_df.groupby(['Pclass'], as_index = False).mean()
axes1 = plt.subplot(1,2,2)
axes1 = sns.barplot(x = 'Pclass', y = 'Survived', data = survival_pclass)  # sns barplot
axes1.set_title('The Survival Rate Based on Class')
axes1.set_ylabel('Survival Rate')

plt.tight_layout()
# It seems that the higher class passengers are, the more possible they can survive. 
# Therefore we need to produce two dummy variables to describe 'Pclass' according to Pclass values


# In[ ]:


train_df['High Class'] = np.where(train_df['Pclass'] == 1, 1, 0)
train_df['Median Class'] = np.where(train_df['Pclass'] == 2, 1, 0)
train_df.head()


# #### Sex and Survival

# In[ ]:


sex_df = train_df[['Survived', 'Sex']]
fig = plt.figure(figsize = (10,5))
axes0 = plt.subplot(1,2,1)
axes0 = sns.countplot(x = 'Sex', hue = 'Survived', data = sex_df)
axes0.set_title('The Number of Survival Based on Sex')
axes0.set_ylabel('Count')
axes0.legend(['No', 'Yes'])

survival_sex = sex_df.groupby(['Sex'], as_index = False).mean()
axes1 = plt.subplot(1,2,2)
axes1 = sns.barplot(x = 'Sex', y = 'Survived', data = survival_sex, palette = 'Set1') # sns factorplot
axes1.set_title('The Survival Rate Based on Sex')
axes1.set_ylabel('Survival Rate')
# It shows that female has more chances to survival
# We also need to transfer Sex to a dummy variable


# In[ ]:


train_df = train_df.replace({'Sex': {'male':0, 'female':1}})
train_df.head()


# #### Age and Survival

# In[ ]:


age_df = train_df[['Survived', 'Age']]
age_df['Age'] = pd.cut(age_df['Age'], bins = 5, labels = [1, 2, 3, 4, 5])
fig = plt.figure(figsize = (10,5))
axes0 = plt.subplot(1,2,1)
axes0 = sns.countplot(x = 'Age', hue = 'Survived', data = age_df)
axes0.set_title('The Number of Survival Based on Age')
axes0.set_ylabel('Count')
axes0.legend(['No', 'Yes'])

survival_age = age_df.groupby(['Age'], as_index = False).mean()
axes1 = plt.subplot(1,2,2)
axes1 = sns.barplot(x = 'Age', y = 'Survived', data = survival_age, palette = 'Set1') 
axes1.set_title('The Survival Rate Based on Age')
axes1.set_ylabel('Survival Rate')

# It indicates that age has influence on survival
# But we need to normalize Age values to make sure it belongs to [0,1]


# In[ ]:


age = train_df[['Age']].values.astype(float)
min_max_scaler = preprocessing.MinMaxScaler()
age_scaled = min_max_scaler.fit_transform(age)
train_df['Age'] = pd.DataFrame(age_scaled)
train_df.head()


# #### SibSp and Survival

# In[ ]:


sibsp_df = train_df[['Survived', 'SibSp']]
survival_sibsp = sibsp_df.groupby(['SibSp'], as_index = False).mean()
sns.barplot(x = 'SibSp', y = 'Survived', data = survival_sibsp)
# Different "SibSps" have different survival rate


# In[ ]:


sibsp_df['SibSp'] = np.where(sibsp_df['SibSp'] > 0, 1, 0)
fig = plt.figure(figsize = (10,5))
axes0 = plt.subplot(1,2,1)
axes0 = sns.countplot(x = 'SibSp', hue = 'Survived', data = sibsp_df)
axes0.set_title('The Number of Survival Based on SibSp')
axes0.set_ylabel('Count')
axes0.legend(['No', 'Yes'])

survival_sibsp = sibsp_df.groupby(['SibSp'], as_index = False).mean()
axes1 = plt.subplot(1,2,2)
axes1 = sns.barplot(x = 'SibSp', y = 'Survived', data = survival_sibsp, palette = 'Set1') 
axes1.set_title('The Survival Rate Based on SibSp')
axes1.set_ylabel('Survival Rate')


# In[ ]:


# Transfer 'SibSp' to dummy variables in training dataframe
train_df['SibSp'] = np.where(train_df['SibSp'] > 0, 1, 0)
train_df.head()


# #### Parch and Survival

# In[ ]:


parch_df= train_df[['Survived', 'Parch']]
survival_parch = parch_df.groupby(['Parch'], as_index = False).mean()
sns.barplot(x = 'Parch', y = 'Survived', data = survival_parch)
# Different Parches have different survival rate


# In[ ]:


parch_df['Parch'] = np.where(parch_df['Parch'] > 0, 1, 0)
fig = plt.figure(figsize = (10,5))
axes0 = plt.subplot(1,2,1)
axes0 = sns.countplot(x = 'Parch', hue = 'Survived', data = parch_df)
axes0.set_title('The Number of Survival Based on Parch')
axes0.set_ylabel('Count')
axes0.legend(['No', 'Yes'])

survival_parch = parch_df.groupby(['Parch'], as_index = False).mean()
axes1 = plt.subplot(1,2,2)
axes1 = sns.barplot(x = 'Parch', y = 'Survived', data = survival_parch, palette = 'Set1') 
axes1.set_title('The Survival Rate Based on Parch')
axes1.set_ylabel('Survival Rate')


# In[ ]:


# Transfer 'Parch' to dummy variables in training dataframe
train_df['Parch'] = np.where(train_df['Parch'] > 0, 1, 0)
train_df.head()


# #### Fare and Survival

# In[ ]:


fare_df = train_df[['Survived', 'Fare']]
fare_df['Fare'] = pd.cut(fare_df['Fare'], bins = 5, labels = [1, 2, 3, 4, 5])
fig = plt.figure(figsize = (10,5))
axes0 = plt.subplot(1,2,1)
axes0 = sns.countplot(x = 'Fare', hue = 'Survived', data = fare_df)
axes0.set_title('The Number of Survival Based on Fare')
axes0.set_ylabel('Count')
axes0.legend(['No', 'Yes'])

survival_fare = fare_df.groupby(['Fare'], as_index = False).mean()
axes1 = plt.subplot(1,2,2)
axes1 = sns.barplot(x = 'Fare', y = 'Survived', data = survival_fare, palette = 'Set1') 
axes1.set_title('The Survival Rate Based on Fare')
axes1.set_ylabel('Survival Rate')
# By dividing fare into several parts, I just want to maker sure whether there is relationship between fare and survival
# Now we can see that this relationship does exist. And we need to normalize it


# In[ ]:


fare = train_df[['Fare']].values.astype(float)
min_max_scaler = preprocessing.MinMaxScaler()
fare_scaled = min_max_scaler.fit_transform(fare)
train_df['Fare'] = pd.DataFrame(fare_scaled)
train_df.head()


# #### Embarked and Survival

# In[ ]:


embarked_df = train_df[['Survived', 'Embarked']]
fig = plt.figure(figsize = (10,5))
axes0 = plt.subplot(1,2,1)
axes0 = sns.countplot(x = 'Embarked', hue = 'Survived', data = embarked_df)
axes0.set_title('The Number of Survival Based on Embark')
axes0.set_ylabel('Count')
axes0.legend(['No', 'Yes'])

survival_embarked = embarked_df.groupby(['Embarked'], as_index = False).mean()
axes1 = plt.subplot(1,2,2)
axes1 = sns.barplot(x = 'Embarked', y = 'Survived', data = survival_embarked, palette = 'Set1') 
axes1.set_title('The Survival Rate Based on Embark')
axes1.set_ylabel('Survival Rate')
# The "Embarked" variable can also affect survival


# In[ ]:


train_df['Embarked C'] = np.where(train_df['Embarked'] == 'C', 1, 0)
train_df['Embarked Q'] = np.where(train_df['Embarked'] == 'Q', 1, 0)
train_df.head()


# ### Final Training Dataframe
# We have seen all variables in the training dataframe will influence passengers' survival rate. Therefore, we need include any of them to build up our models. However, before that, we have to delete some extral ones

# In[ ]:


final_train_df = train_df[['Survived', 'High Class', 'Median Class', 'Sex', 'Age', 'SibSp', 
                           'Parch', 'Fare', 'Embarked C', 'Embarked Q']]
final_train_df.head()


# ## Build Prediction Model

# In[ ]:


independent_v_train = final_train_df[['High Class', 'Median Class', 'Sex', 'Age', 'SibSp', 
                                      'Parch', 'Fare', 'Embarked C', 'Embarked Q']]
dependent_v_train = final_train_df['Survived']


# ### Gaussian Model

# In[ ]:


gau = GaussianNB()
gau.fit(independent_v_train, dependent_v_train)
gau.score(independent_v_train, dependent_v_train)


# ### SVC Model

# In[ ]:


svc = SVC()
svc.fit(independent_v_train, dependent_v_train)
svc.score(independent_v_train, dependent_v_train)


# ### Perceptron Model

# In[ ]:


per = Perceptron()
per.fit(independent_v_train, dependent_v_train)
per.score(independent_v_train, dependent_v_train)


# ### Logistic Model

# In[ ]:


log = LogisticRegression()
log.fit(independent_v_train, dependent_v_train)
log.score(independent_v_train, dependent_v_train)


# ### RandomForest Model

# In[ ]:


rf = RandomForestClassifier()
rf.fit(independent_v_train, dependent_v_train)
rf.score(independent_v_train, dependent_v_train)


# ### DecisionTree Model

# In[ ]:


dt = DecisionTreeClassifier()
dt.fit(independent_v_train, dependent_v_train)
dt.score(independent_v_train, dependent_v_train)


# ### K-Neighbors Model

# In[ ]:


kn = KNeighborsClassifier()
kn.fit(independent_v_train, dependent_v_train)
kn.score(independent_v_train, dependent_v_train)


# ### SGD Model

# In[ ]:


sdg = SGDClassifier()
sdg.fit(independent_v_train, dependent_v_train)
sdg.score(independent_v_train, dependent_v_train)


# ### GradientBoosting Model

# In[ ]:


gb = GradientBoostingClassifier()
gb.fit(independent_v_train, dependent_v_train)
gb.score(independent_v_train, dependent_v_train)


# In[ ]:


result_dict = {'Model' :['Gaussian', 'SVC', 'Perceptron', 'Logistic', 'RandomForest', 
                         'DecisionTree', 'K-Neibours', 'SGD', 'GradientBoosting'], 
              'Score': [gau.score(independent_v_train, dependent_v_train), svc.score(independent_v_train, dependent_v_train),
                       per.score(independent_v_train, dependent_v_train), log.score(independent_v_train, dependent_v_train),
                       rf.score(independent_v_train, dependent_v_train), dt.score(independent_v_train, dependent_v_train),
                       kn.score(independent_v_train, dependent_v_train), sdg.score(independent_v_train, dependent_v_train), 
                       gb.score(independent_v_train, dependent_v_train)]}
pd.DataFrame(result_dict)


# ## Make Predictions

# ### Clean the Testing Data

# In[ ]:


test_df.count()


# In[ ]:


# Remove unrelated variables
test_df = test_df.drop(['Cabin', 'PassengerId', 'Name', 'Ticket'], axis = 1)
# Transform Pclass and Sex variable
test_df['High Class'] = np.where(test_df['Pclass'] == 1, 1, 0)
test_df['Median Class'] = np.where(test_df['Pclass'] == 2, 1, 0)
test_df = test_df.replace({'Sex': {'male':0, 'female':1}})
# Fill NAs in Age and normalizing values
min_age = test_df['Age'].min()
max_age = test_df['Age'].max()
null_values_count = test_df['Age'].isnull().sum()
age_fill_values = np.random.randint(min_age, max_age, size = null_values_count)
test_df['Age'][np.isnan(test_df['Age'])] = age_fill_values
age = test_df[['Age']].values.astype(float)
min_max_scaler = preprocessing.MinMaxScaler()
age_scaled = min_max_scaler.fit_transform(age)
test_df['Age'] = pd.DataFrame(age_scaled)


# In[ ]:


# Transform SibSp and Parch variables
test_df['SibSp'] = np.where(test_df['SibSp'] > 0, 1, 0)
test_df['Parch'] = np.where(test_df['Parch'] > 0, 1, 0) 
# Fill NA in Fare and Normalizing values
test_df['Fare'] = test_df['Fare'].fillna(test_df['Fare'].mean())
fare = train_df[['Fare']].values.astype(float)
min_max_scaler = preprocessing.MinMaxScaler()
fare_scaled = min_max_scaler.fit_transform(fare)
test_df['Fare'] = pd.DataFrame(fare_scaled)
# Fill NA in Embarked and transform values
print(test_df['Embarked'][test_df['Embarked'] == 'S'].count()) # 270
print(test_df['Embarked'][test_df['Embarked'] == 'C'].count()) # 102
print(test_df['Embarked'][test_df['Embarked'] == 'Q'].count()) # 46
test_df['Embarked'] = test_df['Embarked'].fillna('S')
test_df['Embarked C'] = np.where(test_df['Embarked'] == 'C', 1, 0)
test_df['Embarked Q'] = np.where(test_df['Embarked'] == 'Q', 1, 0)
test_df.count()


# In[ ]:


final_test_df = test_df[['High Class', 'Median Class', 'Sex', 'Age', 'SibSp', 
                           'Parch', 'Fare', 'Embarked C', 'Embarked Q']]
final_test_df.head()


# ### Predict

# In[ ]:


independent_v_test = final_test_df
dependent_v_test_predict = gb.predict(independent_v_test)
survival_df = pd.DataFrame(dependent_v_test_predict)
test_get_id = pd.read_csv('../input/test.csv')
prediction_df = pd.DataFrame(test_get_id['PassengerId'])
prediction_df['Survived'] = survival_df


# In[ ]:


prediction_df.to_csv('Prediction of Titanic.csv', index=False)


# In[ ]:




