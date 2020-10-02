#!/usr/bin/env python
# coding: utf-8

# Studying an Expert's code.
# https://www.kaggle.com/omarelgabry/titanic/a-journey-through-titanic

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

# pandas
import pandas as pd
from pandas import Series,DataFrame

# numpy, matplotlib, seaborn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
#%matplotlib inline

# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB


# In[ ]:


# get titanic & test csv files as a DataFrame
titanic_df = pd.read_csv("../input/train.csv")
test_df    = pd.read_csv("../input/test.csv")

# preview the data
#titanic_df.head()

#titanic_df.info()
#print("----------------------------")
#test_df.info()


# In[ ]:


titanic_df = titanic_df.drop(["PassengerId", "Name", "Ticket"], axis = 1)
test_df = test_df.drop(["Name", "Ticket"], axis = 1)

# Fill the two missing values with the most occurred value 
titanic_df["Embarked"] = titanic_df["Embarked"].fillna("S")

sns.factorplot("Embarked", "Survived", data = titanic_df, size=2, aspect =3)
fig, (axis1, axis2, axis3) = plt.subplots(1, 3, figsize = (8,5))

sns.countplot(x = "Embarked", data = titanic_df, ax = axis1)
sns.countplot(x = "Survived", hue = "Embarked", data = titanic_df, order = [1, 0], ax = axis2)

#Group by embarked, and get the mean for survived passengers for each value in Embarked
embark_perc = titanic_df[["Embarked", "Survived"]].groupby(["Embarked"], as_index = False).mean()
#print(embark_perc)
sns.barplot(x="Embarked", y = "Survived", data = embark_perc, order=["S", "C", "Q"], ax = axis3)

#Remove S dummy variable and leave C and Q which have good rate for Suvival.
###I don't understand why S is not good vaiable
#or don't create dummy variables for embarked column, because Embarked doesn't seem to be useful in prediction.

embark_dummies_titanic = pd.get_dummies(titanic_df["Embarked"])
embark_dummies_titanic.drop(["S"], axis = 1, inplace = True)

embark_dummies_test = pd.get_dummies(test_df["Embarked"])
embark_dummies_test.drop(["S"], axis=1, inplace = True)

titanic_df = titanic_df.join(embark_dummies_titanic)
test_df = test_df.join(embark_dummies_test)

titanic_df.drop(["Embarked"], axis = 1, inplace = True)
test_df.drop(["Embarked"], axis = 1, inplace = True)


# In[ ]:


#Fare
#Only for test_df. since there is a missing Fare value
test_df["Fare"].fillna(test_df["Fare"].median(), inplace=True)

#Convert from float to int
titanic_df["Fare"] = titanic_df["Fare"].astype(int)
test_df["Fare"] = test_df["Fare"].astype(int)

#Get fare for survived and didn't survive pasengers
fare_not_survived = titanic_df["Fare"][titanic_df["Survived"] == 0]
fare_survived = titanic_df["Fare"][titanic_df["Survived"] == 1]

#Get average and std for fare of survived/not survived passengers
average_fare = DataFrame([fare_not_survived.mean(), fare_survived.mean()])
std_fare = DataFrame([fare_not_survived.std(), fare_survived.std()])

#plot
titanic_df["Fare"].plot(kind = "hist", figsize = (7, 3), bins = 100, xlim = (0, 100))

average_fare.index.names = std_fare.index.name = ["Survived"]
average_fare.plot(yerr= std_fare, kind = "bar", legend = False)


# In[ ]:


#Age

flg, (axis1, axis2) = plt.subplots(1, 2, figsize = (7, 3))
axis1.set_title("Original Age values - Titanic")
axis2.set_title("New Age values - Titanic")

#Get average, std, and number of NaN vaues in titanic_df
average_age_titanic = titanic_df["Age"].mean()
std_age_titanic = titanic_df["Age"].std()
count_nan_age_titanic = titanic_df["Age"].isnull().sum()

#Get average, std and number of NaN values in test_df
average_age_test = test_df["Age"].mean()
std_age_test = test_df["Age"].std()
count_nan_age_test = test_df["Age"].isnull().sum()

#Generate random numbers between (mean -std) & (mean + std)
### Why need this?
rand_1 = np.random.randint(average_age_titanic - std_age_titanic, average_age_titanic + std_age_titanic, size = count_nan_age_titanic)
rand_2 = np.random.randint(average_age_test - std_age_test, average_age_test + std_age_test, size = count_nan_age_test)
#print(average_age_titanic - std_age_titanic,  average_age_titanic + std_age_titanic, count_nan_age_titanic)
#print(average_age_test - std_age_titanic,  average_age_test + std_age_test, count_nan_age_test)

#Plot original Age values 
#Note: drop all null values, and covert to int
titanic_df["Age"].dropna().astype(int).hist(bins=70, ax = axis1)

#Fill NaN values in Age column with random values generated
#print(np.isnan(titanic_df["Age"]))
###In the ealier step, it drops all NaN cells.
###Then why does it need to fill nan with random values?
titanic_df["Age"][np.isnan(titanic_df["Age"])] = rand_1
test_df["Age"][np.isnan(test_df["Age"])] = rand_2

#convert from float to int
titanic_df["Age"] = titanic_df["Age"].astype(int)
test_df["Age"] = test_df["Age"].astype(int)

#Plot new Age values
titanic_df["Age"].hist(bins=70, ax = axis2)

#As of the end of this step, there is a difference in the result of mine and expart's


# In[ ]:


# .... continue with plot Age column

# peaks for survived/not survived passengers by their age
facet = sns.FacetGrid(titanic_df, hue="Survived",aspect=4)
facet.map(sns.kdeplot,'Age',shade= True)
facet.set(xlim=(0, titanic_df['Age'].max()))
facet.add_legend()

# average survived passengers by age
fig, axis1 = plt.subplots(1,1,figsize=(18,4))
average_age = titanic_df[["Age", "Survived"]].groupby(['Age'],as_index=False).mean()
sns.barplot(x='Age', y='Survived', data=average_age)


# In[ ]:


# Cabin
# It has a lot of NaN values, so it wont cause a remarkable impact on prediction
#print(titanic_df["Cabin"])
titanic_df.drop("Cabin", axis = 1,  inplace = True)
test_df.drop("Cabin", axis = 1, inplace = True)


# In[ ]:


# Family

# Instead of having two columns Parch & SibSp, 
# we can have only one column represent if the passenger had any family member aboard or not,
# Meaning, if having any family member(whether parent, brother, ...etc) will increase chances of Survival or not.
titanic_df['Family'] =  titanic_df["Parch"] + titanic_df["SibSp"]
titanic_df['Family'].loc[titanic_df['Family'] > 0] = 1
titanic_df['Family'].loc[titanic_df['Family'] == 0] = 0

test_df['Family'] =  test_df["Parch"] + test_df["SibSp"]
test_df['Family'].loc[test_df['Family'] > 0] = 1
test_df['Family'].loc[test_df['Family'] == 0] = 0

# drop Parch & SibSp
titanic_df = titanic_df.drop(['SibSp','Parch'], axis=1)
test_df    = test_df.drop(['SibSp','Parch'], axis=1)

# plot
fig, (axis1,axis2) = plt.subplots(1,2,sharex=True,figsize=(10,5))

# sns.factorplot('Family',data=titanic_df,kind='count',ax=axis1)
sns.countplot(x='Family', data=titanic_df, order=[1,0], ax=axis1)

# average of survived for those who had/didn't have any family member
family_perc = titanic_df[["Family", "Survived"]].groupby(['Family'],as_index=False).mean()
sns.barplot(x='Family', y='Survived', data=family_perc, order=[1,0], ax=axis2)

axis1.set_xticklabels(["With Family","Alone"], rotation=0)


# In[ ]:


# Sex

# As we see, children(age < ~16) on aboard seem to have a high chances for Survival.
# So, we can classify passengers as males, females, and child
def get_person(passenger):
    age,sex = passenger
    return 'child' if age < 16 else sex
    
titanic_df['Person'] = titanic_df[['Age','Sex']].apply(get_person,axis=1)
test_df['Person']    = test_df[['Age','Sex']].apply(get_person,axis=1)

# No need to use Sex column since we created Person column
titanic_df.drop(['Sex'],axis=1,inplace=True)
test_df.drop(['Sex'],axis=1,inplace=True)

# create dummy variables for Person column, & drop Male as it has the lowest average of survived passengers
person_dummies_titanic  = pd.get_dummies(titanic_df['Person'])
person_dummies_titanic.columns = ['Child','Female','Male']
person_dummies_titanic.drop(['Male'], axis=1, inplace=True)

person_dummies_test  = pd.get_dummies(test_df['Person'])
person_dummies_test.columns = ['Child','Female','Male']
person_dummies_test.drop(['Male'], axis=1, inplace=True)

titanic_df = titanic_df.join(person_dummies_titanic)
test_df    = test_df.join(person_dummies_test)

fig, (axis1,axis2) = plt.subplots(1,2,figsize=(10,5))

# sns.factorplot('Person',data=titanic_df,kind='count',ax=axis1)
sns.countplot(x='Person', data=titanic_df, ax=axis1)

# average of survived for each Person(male, female, or child)
person_perc = titanic_df[["Person", "Survived"]].groupby(['Person'],as_index=False).mean()
sns.barplot(x='Person', y='Survived', data=person_perc, ax=axis2, order=['male','female','child'])

titanic_df.drop(['Person'],axis=1,inplace=True)
test_df.drop(['Person'],axis=1,inplace=True)


# In[ ]:


# Pclass

# sns.factorplot('Pclass',data=titanic_df,kind='count',order=[1,2,3])
sns.factorplot('Pclass','Survived',order=[1,2,3], data=titanic_df,size=5)

# create dummy variables for Pclass column, & drop 3rd class as it has the lowest average of survived passengers
pclass_dummies_titanic  = pd.get_dummies(titanic_df['Pclass'])
pclass_dummies_titanic.columns = ['Class_1','Class_2','Class_3']
pclass_dummies_titanic.drop(['Class_3'], axis=1, inplace=True)

pclass_dummies_test  = pd.get_dummies(test_df['Pclass'])
pclass_dummies_test.columns = ['Class_1','Class_2','Class_3']
pclass_dummies_test.drop(['Class_3'], axis=1, inplace=True)

titanic_df.drop(['Pclass'],axis=1,inplace=True)
test_df.drop(['Pclass'],axis=1,inplace=True)

titanic_df = titanic_df.join(pclass_dummies_titanic)
test_df    = test_df.join(pclass_dummies_test)


# In[ ]:


# define training and testing sets

X_train = titanic_df.drop("Survived",axis=1)
Y_train = titanic_df["Survived"]
X_test  = test_df.drop("PassengerId",axis=1).copy()

# Logistic Regression

logreg = LogisticRegression()

logreg.fit(X_train, Y_train)

Y_pred = logreg.predict(X_test)

logreg.score(X_train, Y_train)


# In[ ]:


#Support Vector Machines
svc = SVC()
svc.fit(X_train, Y_train)
Y_pred = svc.predict(X_test)
svc.score(X_train, Y_train)


# In[ ]:


# Random Forests

random_forest = RandomForestClassifier(n_estimators = 100)
random_forest.fit(X_train, Y_train)
Y_pred = random_forest.predict(X_test)
random_forest.score(X_train, Y_train)



# In[ ]:


#knn = KNeighborsClassifier(n_neighbors = 3)
knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(X_train, Y_train)
Y_pred = knn.predict(X_test)
knn.score(X_train, Y_train)


# In[ ]:


#Gaussian Naive Bayes
gaussian = GaussianNB()
gaussian.fit(X_train, Y_train)
Y_pred = gaussian.predict(X_test)
gaussian.score(X_train, Y_train)



# In[ ]:


#Get Correlation Coefficient for each feature using Logistic Regression
coeff_df = DataFrame(titanic_df.columns.delete(0))
coeff_



