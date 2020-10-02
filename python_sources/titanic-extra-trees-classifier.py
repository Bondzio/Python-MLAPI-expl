import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier

#Print you can execute arbitrary python code
train = pd.read_csv("../input/train.csv", dtype={"Age": np.float64}, )
test = pd.read_csv("../input/test.csv", dtype={"Age": np.float64}, )
combine = [train, test]

#Method for finding substrings
def substrings_in_string(big_string, substrings):
    for substring in substrings:
        if substring in big_string:
            return substring
    return np.nan
    
#Mappings
title_list=['Mrs', 'Mr', 'Master', 'Miss', 'Major', 'Rev',
                    'Dr', 'Ms', 'Mlle','Col', 'Capt', 'Mme', 'Countess',
                    'Don', 'Jonkheer']

cabin_list = ['A', 'B', 'C', 'D', 'E', 'F', 'T', 'G', 'Unknown']

title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}

for df in combine:
    # Convert the male and female groups to integer form
    df["Sex"][df["Sex"] == "male"] = 0
    df["Sex"][df["Sex"] == "female"] = 1
    
    #Map and Create Title Feature
    df['Title'] = df['Name'].astype(str).map(lambda x: substrings_in_string(x, title_list))
    df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col',\
 	'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    df['Title'] = df['Title'].replace('Mlle', 'Miss')
    df['Title'] = df['Title'].replace('Ms', 'Miss')
    df['Title'] = df['Title'].replace('Mme', 'Mrs')
    df['Title'] = df['Title'].map(title_mapping)
    df['Title'] = df['Title'].fillna(0)
    
    #Map and Create Deck feature
    df['Deck'] = df['Cabin'].astype(str).map(lambda x: substrings_in_string(x, cabin_list))
    df["Deck"][df["Deck"] == "A"] = 1
    df["Deck"][df["Deck"] == "B"] = 2
    df["Deck"][df["Deck"] == "C"] = 3
    df["Deck"][df["Deck"] == "D"] = 4
    df["Deck"][df["Deck"] == "E"] = 5
    df["Deck"][df["Deck"] == "F"] = 6
    df["Deck"][df["Deck"] == "G"] = 7
    df["Deck"][df["Deck"] == "T"] = 8
    df["Deck"] = df["Deck"].fillna(0)
    
    #Create Family size, Fare per person, and isAlone features
    df['Family_size'] = df['SibSp']+df['Parch']+1
    
    df['Fare_Per_Person']=df['Fare']/(df['Family_size'])
    
    df['isAlone']=0
    df.loc[df['Family_size']==1, 'isAlone'] = 1
    
    # Impute the Embarked variable to the mode
    df["Embarked"] = df["Embarked"].fillna("S")

    # Convert the Embarked classes to integer form
    df["Embarked"][df["Embarked"] == "S"] = 0
    df["Embarked"][df["Embarked"] == "C"] = 1
    df["Embarked"][df["Embarked"] == "Q"] = 2

#Impute ages based off sex and class
guess_ages = np.zeros((2,3))
for df in combine:
    for i in range(0, 2):
        for j in range(0, 3):
            guess_df = df[(df['Sex'] == i) & \
                                  (df['Pclass'] == j+1)]['Age'].dropna()
            age_guess = guess_df.median()

            # Convert random age float to nearest .5 age
            guess_ages[i,j] = int( age_guess/0.5 + 0.5 ) * 0.5
            
    for i in range(0, 2):
        for j in range(0, 3):
            df.loc[ (df.Age.isnull()) & (df.Sex == i) & (df.Pclass == j+1),\
                    'Age'] = guess_ages[i,j]

    df['Age'] = df['Age'].astype(int)

for df in combine:
    #set child feature
    df["child"] = float('NaN')
    df["child"][df["Age"] < 18] = 1
    df["child"][df["Age"] >=18] = 0

#Set single null fare in test data
test['Fare'] = test['Fare'].fillna(0)
test['Fare_Per_Person'] = test['Fare_Per_Person'].fillna(0)

#Create target feature set
excl = ['PassengerId', 'Survived', 'Ticket', 'Cabin', 'Name']
cols = [c for c in train.columns if c not in excl]


target = train["Survived"].values
features = train[cols].values

#Extra Trees Classifier
etc = ExtraTreesClassifier(n_estimators=1000, max_depth=9, min_samples_split=6, min_samples_leaf=4, n_jobs=-1, random_state=10, verbose=0)
etcmod = etc.fit(features, target)

#Show feature importances
fi = etcmod.feature_importances_
importances = pd.DataFrame(fi, columns = ['importance'])
importances['feature'] = cols
print(importances.sort_values(by='importance', ascending=False))

#Predict test
test_features = test[cols].values
pred = etcmod.predict(test_features)

PassengerId = np.array(test["PassengerId"]).astype(int)
my_solution = pd.DataFrame(pred, PassengerId, columns = ["Survived"])

my_solution.to_csv("extraTrees.csv", index_label = ["PassengerId"])
