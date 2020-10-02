#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# data analysis and wrangling
import pandas as pd
import numpy as np
import random as rnd

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier


# In[ ]:


train_df = pd.read_csv('../input/train.csv')
test_df = pd.read_csv('../input/test.csv')
combine = [train_df, test_df]
print(train_df.columns.values)


# In[ ]:





# In[ ]:


# preview the first 5 data
train_df.head()


# In[ ]:


# preview the last 5 data
train_df.tail()


# In[ ]:


train_df.info()
print('_'*40)
test_df.info()


# In[ ]:


train_df.describe()


# - Total samples are 891 or 40% of the actual number of passengers on board the Titanic (2,224).
# - Survived is a categorical feature with 0 or 1 values.
# - Around 38% samples survived representative of the actual survival rate at 32%.
# - Most passengers (> 75%) did not travel with parents or children.
# - Nearly 30% of the passengers had siblings and/or spouse aboard.
# - Fares varied significantly with few passengers (<1%) paying as high as $512.
# - Few elderly passengers (<1%) within age range 65-80.

# In[ ]:


train_df.describe(include=['O'])


# - Names are unique across the dataset (count=unique=891)
# - Sex variable as two possible values with 65% male (top=male, freq=577/count=891).
# - Cabin values have several dupicates across samples. Alternatively several passengers shared a cabin.
# - Embarked takes three possible values. S port used by most passengers (top=S)
# - Ticket feature has high ratio (22%) of duplicate values (unique=681).

# In[ ]:


# check correlation among Pclass and Survived
train_df[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[ ]:


# check correlation among Sex and Survived
train_df[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[ ]:


# check correlation among numbers of siblings
train_df[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='SibSp')


# In[ ]:


# check correlation among numbers of parents and children
train_df[["Parch", "Survived"]].groupby(['Parch'], as_index=False).mean().sort_values(by='Parch')


# - **Pclass** We observe significant correlation (>0.5) among Pclass=1 and Survived (classifying #3). We decide to include this feature in our model.
# - **Sex** We confirm the observation during problem definition that Sex=female had very high survival rate at 74% (classifying #1).
# - **SibSp and Parch** These features have zero correlation for certain values. It may be best to derive a feature or a set of features from these individual features (creating #1).

# In[ ]:


# Note that x-axis in historgram visualizations represents the count of samples or passengers.
g = sns.FacetGrid(train_df, col='Survived')
g.map(plt.hist, 'Age', bins=20)


# **Observations.**
# 
# - Infants (Age <=4) had high survival rate.
# - Oldest passengers (Age = 80) survived.
# - Large number of 15-25 year olds did not survive.
# - Most passengers are in 15-35 age range.
# 
# **Decisions.**
# 
# This simple analysis confirms our assumptions as decisions for subsequent workflow stages.
# 
# - We should consider Age (our assumption classifying #2) in our model training.
# - Complete the Age feature for null values (completing #1).
# - We should band age groups (creating #3).

# ### Correlating numerical and ordinal features
# 
# We can combine multiple features for identifying correlations using a single plot. This can be done with numerical and categorical features which have numeric values.
# 
# **Observations.**
# 
# - Pclass=3 had most passengers, however most did not survive. Confirms our classifying assumption #2.
# - Infant passengers in Pclass=2 and Pclass=3 mostly survived. Further qualifies our classifying assumption #2.
# - Most passengers in Pclass=1 survived. Confirms our classifying assumption #3.
# - Pclass varies in terms of Age distribution of passengers.
# 
# **Decisions.**
# 
# - Consider Pclass for model training.

# In[ ]:


# grid = sns.FacetGrid(train_df, col='Pclass', hue='Survived')
grid = sns.FacetGrid(train_df, col='Survived', row='Pclass', height=2.2, aspect=1.6)
grid.map(plt.hist, 'Age', alpha=.5, bins=20)
grid.add_legend();


# 

# In[ ]:


# grid = sns.FacetGrid(train_df, col='Embarked')
grid = sns.FacetGrid(train_df, row='Embarked', height=2.2, aspect=1.6)
grid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette='deep')
grid.add_legend()


# ### Correlating categorical features
# 
# Now we can correlate categorical features with our solution goal.
# 
# **Observations.**
# 
# - Female passengers had much better survival rate than males. Confirms classifying (#1).
# - Exception in Embarked=C where males had higher survival rate. This could be a correlation between Pclass and Embarked and in turn Pclass and Survived, not necessarily direct correlation between Embarked and Survived.
# - Males had better survival rate in Pclass=3 when compared with Pclass=2 for C and Q ports. Completing (#2).
# - Ports of embarkation have varying survival rates for Pclass=3 and among male passengers. Correlating (#1).
# 
# **Decisions.**
# 
# - Add Sex feature to model training.
# - Complete and add Embarked feature to model training.

# In[ ]:


# grid = sns.FacetGrid(train_df, col='Embarked', hue='Survived', palette={0: 'k', 1: 'w'})
grid = sns.FacetGrid(train_df, row='Embarked', col='Survived', height=2.2, aspect=2)
grid.map(sns.barplot, 'Sex', 'Fare', alpha=1, ci=None)
grid.add_legend()


# ### Correlating categorical and numerical features
# 
# We may also want to correlate categorical features (with non-numeric values) and numeric features. We can consider correlating Embarked (Categorical non-numeric), Sex (Categorical non-numeric), Fare (Numeric continuous), with Survived (Categorical numeric).
# 
# **Observations.**
# 
# - Higher fare paying passengers had better survival. Confirms our assumption for creating (#4) fare ranges.
# - Port of embarkation correlates with survival rates. Confirms correlating (#1) and completing (#2).
# 
# **Decisions.**
# 
# - Consider banding Fare feature.

# In[ ]:


print("Before", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)

train_df = train_df.drop(['Ticket', 'Cabin'], axis=1)
test_df = test_df.drop(['Ticket', 'Cabin'], axis=1)
combine = [train_df, test_df]

"After", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape


# In[ ]:


for dataset in combine:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

pd.crosstab(train_df['Title'], train_df['Sex'])


# Get rid off rare titles from table

# In[ ]:


for dataset in combine:
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col', 	'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')
    
train_df[['Title', 'Survived']].groupby(['Title'], as_index=False).mean()


# **Observations.**
# 
# When we plot Title, Age, and Survived, we note the following observations.
# 
# - Most titles band Age groups accurately. For example: Master title has Age mean of 5 years.
# - Survival among Title Age bands varies slightly.
# - Certain titles mostly survived (Mme, Lady, Sir) or did not (Don, Rev, Jonkheer).
# 
# **Decision.**
# 
# - We decide to retain the new Title feature for model training.

# We can convert the categorical titles to ordinal.

# In[ ]:


title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
for dataset in combine:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)

train_df.head()


# Now we can safely drop the Name feature from training and testing datasets. We also do not need the PassengerId feature in the training dataset.
# 

# In[ ]:


train_df = train_df.drop(['Name', 'PassengerId'], axis=1)
test_df = test_df.drop(['Name'], axis=1)
combine = [train_df, test_df]
train_df.shape, test_df.shape


# ### Converting a categorical feature
# 
# Now we can convert features which contain strings to numerical values. This is required by most model algorithms. Doing so will also help us in achieving the feature completing goal.
# 
# Let us start by converting Sex feature to a new feature called Gender where female=1 and male=0.

# In[ ]:


for dataset in combine:
    dataset['Sex'] = dataset['Sex'].map( {'female': 1, 'male': 0} ).astype(int)

train_df.head()


# ### Completing a numerical continuous feature
# 
# Now we should start estimating and completing features with missing or null values. We will first do this for the Age feature.
# 
# We can consider three methods to complete a numerical continuous feature.
# 
# 1. A simple way is to generate random numbers between mean and [standard deviation](https://en.wikipedia.org/wiki/Standard_deviation).
# 
# 2. More accurate way of guessing missing values is to use other correlated features. In our case we note correlation among Age, Gender, and Pclass. Guess Age values using [median](https://en.wikipedia.org/wiki/Median) values for Age across sets of Pclass and Gender feature combinations. So, median Age for Pclass=1 and Gender=0, Pclass=1 and Gender=1, and so on...
# 
# 3. Combine methods 1 and 2. So instead of guessing age values based on median, use random numbers between mean and standard deviation, based on sets of Pclass and Gender combinations.
# 
# Method 1 and 3 will introduce random noise into our models. The results from multiple executions might vary. We will prefer method 2.

# In[ ]:


# grid = sns.FacetGrid(train_df, col='Pclass', hue='Gender')
grid = sns.FacetGrid(train_df, row='Pclass', col='Sex', size=3, aspect=1.6)
grid.map(plt.hist, 'Age', alpha=.5, bins=20)
grid.add_legend()


# Let us start by preparing an empty array to contain guessed Age values based on Pclass x Gender combinations.

# In[ ]:


guess_ages = np.zeros((2,3))
guess_ages


# Now we iterate over Sex (0 or 1) and Pclass (1, 2, 3) to calculate guessed values of Age for the six combinations.

# In[ ]:


for dataset in combine:
    for i in range(0, 2):
        for j in range(0, 3):
            guess_df = dataset[(dataset['Sex'] == i) & (dataset['Pclass'] == j+1)]['Age'].dropna()

#             age_mean = guess_df.mean()
#             age_std = guess_df.std()
#             age_guess = rnd.uniform(age_mean - age_std, age_mean + age_std)

            age_guess = guess_df.median()

            # Convert random age float to nearest .5 age
            guess_ages[i,j] = int( age_guess/0.5 + 0.5 ) * 0.5
            
    for i in range(0, 2):
        for j in range(0, 3):
            dataset.loc[ (dataset.Age.isnull()) & (dataset.Sex == i) & (dataset.Pclass == j+1),                    'Age'] = guess_ages[i,j]

    dataset['Age'] = dataset['Age'].astype(int)

train_df.head()


# Let us create Age bands and determine correlations with Survived.

# In[ ]:


train_df['AgeBand'] = pd.cut(train_df['Age'], 5)
# train_df['Age']
# train_df['AgeBand']
train_df[['AgeBand', 'Survived']].groupby(['AgeBand'], as_index=False).mean().sort_values(by='AgeBand', ascending=True)


# Let us replace Age with ordinals based on these bands.

# In[ ]:


for dataset in combine:    
    dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
    dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
    dataset.loc[ dataset['Age'] > 64, 'Age'] = 4
train_df.head()


# In[ ]:


# get rid of AgeBand column
train_df = train_df.drop(['AgeBand'], axis=1)
combine = [train_df, test_df]
train_df.head()


# ### Create new feature combining existing features
# 
# We can create a new feature for FamilySize which combines Parch and SibSp. This will enable us to drop Parch and SibSp from our datasets.

# In[ ]:


for dataset in combine:
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1

train_df[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean().sort_values(by='Survived', ascending=True)


# Compare the survival rate with alone and not alone

# In[ ]:


# We can create another feature called IsAlone.
for dataset in combine:
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1

train_df[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()


# In[ ]:


# Let us drop Parch, SibSp, and FamilySize features in favor of IsAlone.
train_df = train_df.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
test_df = test_df.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
combine = [train_df, test_df]

train_df.head()


# In[ ]:


# We can also create an artificial feature combining Pclass and Age.
for dataset in combine:
    dataset['Age*Class'] = dataset.Age * dataset.Pclass

train_df.loc[:, ['Age*Class', 'Age', 'Pclass']].head(10)


# ### Completing a categorical feature
# 
# Embarked feature takes S, Q, C values based on port of embarkation. Our training dataset has two missing values. We simply fill these with the most common occurance.

# In[ ]:


# find most frequent boarding port in Embarked(not in cluding n/a)
freq_port = train_df.Embarked.dropna().mode()[0]
freq_port


# In[ ]:


for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].fillna(freq_port)
    
train_df[['Embarked', 'Survived']].groupby(['Embarked'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[ ]:


# We can now convert the EmbarkedFill feature by creating a new numeric Port feature.
for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)

train_df.head()


# In[ ]:


# Fill n/a in Fare by median
test_df['Fare'].fillna(test_df['Fare'].dropna().median(), inplace=True)
test_df.head()


# In[ ]:


# We can now create FareBand.
train_df['FareBand'] = pd.qcut(train_df['Fare'], 4)
train_df[['FareBand', 'Survived']].groupby(['FareBand'], as_index=False).mean().sort_values(by='FareBand', ascending=True)


# In[ ]:


# Convert the Fare feature to ordinal values based on the FareBand.
for dataset in combine:
    dataset.loc[ dataset['Fare'] <= 7.91, 'Fare'] = 0
    dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
    dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare']   = 2
    dataset.loc[ dataset['Fare'] > 31, 'Fare'] = 3
    dataset['Fare'] = dataset['Fare'].astype(int)

train_df = train_df.drop(['FareBand'], axis=1)
combine = [train_df, test_df]
    
train_df.head(10)


# In[ ]:


# checking test data
test_df.head(10)


# In[ ]:


sns.heatmap(train_df.corr(),annot=True,cmap='RdYlGn',linewidths=0.2) #data.corr()-->correlation matrix
fig=plt.gcf()
fig.set_size_inches(12,10)
plt.show()


# In[ ]:


# Finding coefficiency
coeff_df = pd.DataFrame(train_df.columns.delete(0))
coeff_df.columns = ['Feature']
coeff_df["Correlation"] = pd.Series(logreg.coef_[0])

coeff_df.sort_values(by='Correlation', ascending=True)


# ## Model, predict and solve
# 
# Now we are ready to train a model and predict the required solution. There are 60+ predictive modelling algorithms to choose from. We must understand the type of problem and solution requirement to narrow down to a select few models which we can evaluate. Our problem is a classification and regression problem. We want to identify relationship between output (Survived or not) with other variables or features (Gender, Age, Port...). We are also perfoming a category of machine learning which is called supervised learning as we are training our model with a given dataset. With these two criteria - Supervised Learning plus Classification and Regression, we can narrow down our choice of models to a few. These include:
# 
# - Logistic Regression
# - KNN or k-Nearest Neighbors
# - Support Vector Machines
# - Naive Bayes classifier
# - Decision Tree
# - Random Forrest
# - Perceptron
# - Artificial neural network
# - RVM or Relevance Vector Machine

# In[ ]:


X_train = train_df.drop("Survived", axis=1)
Y_train = train_df["Survived"]
X_test  = test_df.drop("PassengerId", axis=1).copy()
X_train.shape, Y_train.shape, X_test.shape


# In[ ]:


# Logistic Regression

logreg = LogisticRegression()
logreg.fit(X_train, Y_train)
Y_pred = logreg.predict(X_test)
acc_log = round(logreg.score(X_train, Y_train) * 100, 2)
acc_log


# In[ ]:


models = pd.DataFrame({
    'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression', 
              'Random Forest', 'Naive Bayes', 'Perceptron', 
              'Stochastic Gradient Decent', 'Linear SVC', 
              'Decision Tree'],
    'Score': [acc_svc, acc_knn, acc_log, 
              acc_random_forest, acc_gaussian, acc_perceptron, 
              acc_sgd, acc_linear_svc, acc_decision_tree]})
models.sort_values(by='Score', ascending=False)


# In[ ]:


# submit result
submission = pd.DataFrame({
        "PassengerId": test_df["PassengerId"],
        "Survived": Y_pred
    })
submission
submission.to_csv('results_1.csv')

