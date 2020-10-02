#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from collections import Counter

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, learning_curve

sns.set(style='white', context='notebook', palette='deep')


# In[ ]:


train = pd.read_csv("../input/train.csv")
test = pd.read_csv("../input/test.csv")
IDtest = test["PassengerId"]


# In[ ]:


# Outlier detection 

def detect_outliers(df,n,features):
    """
    Takes a dataframe df of features and returns a list of the indices
    corresponding to the observations containing more than n outliers according
    to the Tukey method.
    """
    outlier_indices = []
    
    # iterate over features(columns)
    for col in features:
        # 1st quartile (25%)
        Q1 = np.percentile(df[col], 25)
        # 3rd quartile (75%)
        Q3 = np.percentile(df[col],75)
        # Interquartile range (IQR)
        IQR = Q3 - Q1
        
        # outlier step
        outlier_step = 1.5 * IQR
        
        # Determine a list of indices of outliers for feature col
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step )].index
        
        # append the found outlier indices for col to the list of outlier indices 
        outlier_indices.extend(outlier_list_col)
        
    # select observations containing more than 2 outliers
    outlier_indices = Counter(outlier_indices)        
    multiple_outliers = list( k for k, v in outlier_indices.items() if v > n )
    
    return multiple_outliers   

# detect outliers from Age, SibSp , Parch and Fare
Outliers_to_drop = detect_outliers(train,2,["Age","SibSp","Parch","Fare"])


# In[ ]:


train = train.drop(Outliers_to_drop, axis = 0).reset_index(drop=True)


# In[ ]:


train_len = len(train)
dataset =  pd.concat(objs=[train, test], axis=0).reset_index(drop=True)


# In[ ]:


dataset = dataset.fillna(np.nan)

# Check for Null values
dataset.isnull().sum()


# In[ ]:


g = sns.heatmap(train[["Survived","SibSp","Parch","Age","Fare"]].corr(),annot=True, fmt = ".2f", cmap = "coolwarm")


# In[ ]:


g = sns.factorplot(x="SibSp",y="Survived",data=train,kind="bar", size = 6 , 
palette = "muted")
g.despine(left=True)
g = g.set_ylabels("survival probability")


# In[ ]:


g  = sns.factorplot(x="Parch",y="Survived",data=train,kind="bar", size = 6 , 
palette = "muted")
g.despine(left=True)
g = g.set_ylabels("survival probability")


# In[ ]:


g = sns.FacetGrid(train, col='Survived')
g = g.map(sns.distplot, "Age")


# In[ ]:


g = sns.kdeplot(train["Age"][(train["Survived"] == 0) & (train["Age"].notnull())], color="Red", shade = True)
g = sns.kdeplot(train["Age"][(train["Survived"] == 1) & (train["Age"].notnull())], ax =g, color="Blue", shade= True)
g.set_xlabel("Age")
g.set_ylabel("Frequency")
g = g.legend(["Not Survived","Survived"])


# In[ ]:


dataset["Fare"] = dataset["Fare"].fillna(dataset["Fare"].median())


# In[ ]:


g = sns.distplot(dataset["Fare"], color="m", label="Skewness : %.2f"%(dataset["Fare"].skew()))
g = g.legend(loc="best")


# In[ ]:


dataset["Fare"] = dataset["Fare"].map(lambda i: np.log(i) if i > 0 else 0)


# In[ ]:


g = sns.distplot(dataset["Fare"], color="b", label="Skewness : %.2f"%(dataset["Fare"].skew()))
g = g.legend(loc="best")


# In[ ]:


g = sns.barplot(x="Sex",y="Survived",data=train)
g = g.set_ylabel("Survival Probability")


# In[ ]:


g = sns.factorplot(x="Pclass",y="Survived",data=train,kind="bar", size = 6 , 
palette = "muted")
g.despine(left=True)
g = g.set_ylabels("survival probability")


# In[ ]:


g = sns.factorplot(x="Pclass", y="Survived", hue="Sex", data=train,
                   size=6, kind="bar", palette="muted")
g.despine(left=True)
g = g.set_ylabels("survival probability")


# In[ ]:


dataset["Embarked"] = dataset["Embarked"].fillna("S")


# In[ ]:


g = sns.factorplot(x="Embarked", y="Survived",  data=train,
                   size=6, kind="bar", palette="muted")
g.despine(left=True)
g = g.set_ylabels("survival probability")


# In[ ]:


g = sns.factorplot("Pclass", col="Embarked",  data=train,
                   size=6, kind="count", palette="muted")
g.despine(left=True)
g = g.set_ylabels("Count")


# In[ ]:


g = sns.factorplot(y="Age",x="Sex",data=dataset,kind="box")
g = sns.factorplot(y="Age",x="Sex",hue="Pclass", data=dataset,kind="box")
g = sns.factorplot(y="Age",x="Parch", data=dataset,kind="box")
g = sns.factorplot(y="Age",x="SibSp", data=dataset,kind="box")


# In[ ]:


dataset["Sex"] = dataset["Sex"].map({"male": 0, "female":1})


# In[ ]:


g = sns.heatmap(dataset[["Age","Sex","SibSp","Parch","Pclass"]].corr(),cmap="BrBG",annot=True)


# In[ ]:


index_NaN_age = list(dataset["Age"][dataset["Age"].isnull()].index)

for i in index_NaN_age :
    age_med = dataset["Age"].median()
    age_pred = dataset["Age"][((dataset['SibSp'] == dataset.iloc[i]["SibSp"]) & (dataset['Parch'] == dataset.iloc[i]["Parch"]) & (dataset['Pclass'] == dataset.iloc[i]["Pclass"]))].median()
    if not np.isnan(age_pred) :
        dataset['Age'].iloc[i] = age_pred
    else :
        dataset['Age'].iloc[i] = age_med


# In[ ]:


g = sns.factorplot(x="Survived", y = "Age",data = train, kind="box")
g = sns.factorplot(x="Survived", y = "Age",data = train, kind="violin")


# In[ ]:


dataset_title = [i.split(",")[1].split(".")[0].strip() for i in dataset["Name"]]
dataset["Title"] = pd.Series(dataset_title)
dataset["Title"].head()


# In[ ]:


g = sns.countplot(x="Title",data=dataset)
g = plt.setp(g.get_xticklabels(), rotation=45) 


# In[ ]:


dataset["Title"] = dataset["Title"].replace(['Lady', 'the Countess','Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
dataset["Title"] = dataset["Title"].map({"Master":0, "Miss":1, "Ms" : 1 , "Mme":1, "Mlle":1, "Mrs":1, "Mr":2, "Rare":3})
dataset["Title"] = dataset["Title"].astype(int)


# In[ ]:


g = sns.countplot(dataset["Title"])
g = g.set_xticklabels(["Master","Miss/Ms/Mme/Mlle/Mrs","Mr","Rare"])


# In[ ]:


g = sns.factorplot(x="Title",y="Survived",data=dataset,kind="bar")
g = g.set_xticklabels(["Master","Miss-Mrs","Mr","Rare"])
g = g.set_ylabels("survival probability")


# In[ ]:


dataset.drop(labels = ["Name"], axis = 1, inplace = True)


# In[ ]:


dataset["Fsize"] = dataset["SibSp"] + dataset["Parch"] + 1


# In[ ]:


g = sns.factorplot(x="Fsize",y="Survived",data = dataset)
g = g.set_ylabels("Survival Probability")


# In[ ]:


dataset['Single'] = dataset['Fsize'].map(lambda s: 1 if s == 1 else 0)
dataset['SmallF'] = dataset['Fsize'].map(lambda s: 1 if  s == 2  else 0)
dataset['MedF'] = dataset['Fsize'].map(lambda s: 1 if 3 <= s <= 4 else 0)
dataset['LargeF'] = dataset['Fsize'].map(lambda s: 1 if s >= 5 else 0)


# In[ ]:


g = sns.factorplot(x="Single",y="Survived",data=dataset,kind="bar")
g = g.set_ylabels("Survival Probability")
g = sns.factorplot(x="SmallF",y="Survived",data=dataset,kind="bar")
g = g.set_ylabels("Survival Probability")
g = sns.factorplot(x="MedF",y="Survived",data=dataset,kind="bar")
g = g.set_ylabels("Survival Probability")
g = sns.factorplot(x="LargeF",y="Survived",data=dataset,kind="bar")
g = g.set_ylabels("Survival Probability")


# In[ ]:


dataset = pd.get_dummies(dataset, columns = ["Title"])
dataset = pd.get_dummies(dataset, columns = ["Embarked"], prefix="Em")


# In[ ]:


dataset["Cabin"] = pd.Series([i[0] if not pd.isnull(i) else 'X' for i in dataset['Cabin'] ])


# In[ ]:


g = sns.countplot(dataset["Cabin"],order=['A','B','C','D','E','F','G','T','X'])


# In[ ]:


g = sns.factorplot(y="Survived",x="Cabin",data=dataset,kind="bar",order=['A','B','C','D','E','F','G','T','X'])
g = g.set_ylabels("Survival Probability")


# In[ ]:


dataset = pd.get_dummies(dataset, columns = ["Cabin"],prefix="Cabin")


# In[ ]:


Ticket = []
for i in list(dataset.Ticket):
    if not i.isdigit() :
        Ticket.append(i.replace(".","").replace("/","").strip().split(' ')[0]) #Take prefix
    else:
        Ticket.append("X")
        
dataset["Ticket"] = Ticket
dataset["Ticket"].head()


# In[ ]:


dataset = pd.get_dummies(dataset, columns = ["Ticket"], prefix="T")


# In[ ]:


dataset["Pclass"] = dataset["Pclass"].astype("category")
dataset = pd.get_dummies(dataset, columns = ["Pclass"],prefix="Pc")


# In[ ]:


dataset.drop(labels = ["PassengerId"], axis = 1, inplace = True)


# In[ ]:


train = dataset[:train_len]
test = dataset[train_len:]
test.drop(labels=["Survived"],axis = 1,inplace=True)


# In[ ]:


train["Survived"] = train["Survived"].astype(int)

Y_train = train["Survived"]

X_train = train.drop(labels = ["Survived"],axis = 1)


# In[ ]:


X_train.shape


# In[ ]:


lr = LogisticRegression()


# In[ ]:


s = SVC()


# In[ ]:


from sklearn.naive_bayes import GaussianNB


# In[ ]:


gnb = GaussianNB()


# In[ ]:


from keras.models import Sequential


# In[ ]:


from keras.layers import Dense,BatchNormalization,Dropout


# In[ ]:


from keras import callbacks


# In[ ]:


model  = Sequential()


# In[ ]:


model.add(Dense(32,activation = "relu",input_shape = (66,)))
model.add(Dense(64,activation = "relu"))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Dense(1,activation = 'sigmoid'))


# In[ ]:


model.compile(optimizer = "adam",loss ="binary_crossentropy",metrics = ['accuracy'])
reduce_lr = callbacks.ReduceLROnPlateau(monitor='acc', factor=0.2,patience=3, min_lr=0.0001)
model.fit(X_train,Y_train,epochs = 30,callbacks = [reduce_lr])


# In[ ]:


y = model.predict(test)


# In[ ]:


def sig(y):
    pred= []
    for i in y:
        if i > 0.5:
            a = 1
        else :
            a = 0
        pred.append(a)
    return pred


# In[ ]:


y = sig(y)
y


# In[ ]:


IDtest


# In[ ]:


ans2 = pd.DataFrame(IDtest)


# In[ ]:


ans2["Survived"] = y


# In[ ]:


ans2.to_csv("sub.csv",index = False)

