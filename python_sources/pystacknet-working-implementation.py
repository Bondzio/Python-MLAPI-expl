#!/usr/bin/env python
# coding: utf-8

# # pyStackNet on Kaggle

# This kernel aims at exposing a working implentation of pyStackNet inside kaggle. The original pyStackNet does not work straightforward and some modifications are necessary to make it run in Kaggle. 
# This includes small modifications in the code that I uploaded on https://gitlab.com/YannBerthelot/kaggle_pystacknet.git
# 
# All credit goes to the original authors of StackNet and pyStackNet.
# https://github.com/h2oai/pystacknet
# https://github.com/kaz-Anova/StackNet

# Please comment and/or like if this kernel helped you so that others can see it.

# ## Classic start

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import os
print(os.listdir("../input"))


# ## pyStackNet installation

# don't forget to turn internet "On" in the kernel settings.

# In[ ]:


get_ipython().system('git clone https://gitlab.com/YannBerthelot/kaggle_pystacknet.git')
print(os.listdir("kaggle_pystacknet/pystacknet"))
get_ipython().system('pip install "kaggle_pystacknet/pystacknet"')
import pystacknet


# ## Titanic basic example

# *because I can't do better*

# In[ ]:


train=pd.read_csv("../input/train.csv")
test=pd.read_csv("../input/test.csv")


# In[ ]:


def feature_engineering(df):
    df["Cabin"]=df["Cabin"].fillna("C")
    deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "U": 8}
    df['Deck'] = df['Cabin'].map(lambda x: re.compile("([a-zA-Z]+)").search(x).group())
    mean = df["Age"].mean()
    std = df["Age"].std()
    is_null = df["Age"].isnull().sum()
    rand_age = np.random.randint(mean - std, mean + std, size = is_null)

    age_slice = df["Age"].copy()
    age_slice[np.isnan(age_slice)] = rand_age
    df["Age"] = age_slice
    df["Age"] = df["Age"].astype(int)
    df["Embarked"]=df['Embarked'].fillna("S")
    
    df["Siblings"]=df["SibSp"]+df["Parch"]
    df=df.drop(["Name","Ticket","SibSp","Parch","PassengerId","Cabin","Fare"],axis=1)
    return(df)

train=feature_engineering(train)
test=feature_engineering(test)


# In[ ]:


X=train.drop("Survived",axis=1)
Y=train["Survived"]


# In[ ]:


from sklearn.model_selection import train_test_split

x, x_test, y, y_test = train_test_split(X, Y, test_size=0.20, random_state=42,shuffle=True)

X_oh=pd.get_dummies(X)

test_oh=pd.get_dummies(test)
test_oh["Deck_T"]=0


# ## pyStackNet

# Including LGBM implementation in pystacknet for your pleasure

# In[ ]:


from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesClassifier, ExtraTreesRegressor, GradientBoostingClassifier,GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.decomposition import PCA
from lightgbm import LGBMClassifier
models=[ 
            
            [RandomForestClassifier (n_estimators=100, criterion="entropy", max_depth=5, max_features=0.5, random_state=1),
             ExtraTreesClassifier (n_estimators=100, criterion="entropy", max_depth=5, max_features=0.5, random_state=1),
             GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, max_features=0.5, random_state=1),
             LogisticRegression(random_state=1),
             LGBMClassifier()],
            [RandomForestClassifier (n_estimators=100, criterion="entropy", max_depth=5, max_features=0.5, random_state=1),
             ExtraTreesClassifier (n_estimators=100, criterion="entropy", max_depth=5, max_features=0.5, random_state=1),
             GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, max_features=0.5, random_state=1),
             LogisticRegression(random_state=1),
             LGBMClassifier()],           
            
            ]


# In[ ]:


from pystacknet.pystacknet import StackNetClassifier

model=StackNetClassifier(models, metric="auc", folds=5,
	restacking=False,use_retraining=True, use_proba=True, 
	random_state=12345,n_jobs=1, verbose=1)

model.fit(X_oh,Y)
output=model.predict_proba(test_oh)


# ## Output preparation

# In[ ]:


output=pd.DataFrame(output).rename(index=str, columns={"index": "PassengerId", 0: "Survived"})

output=output.reset_index()

output=output.rename(columns={"index":"PassengerId"})

output["PassengerId"]=output["PassengerId"].astype("int")+892

output["Survived"]=(output[output.columns[output.shape[1]-1]]>0.5).apply(int)

output=output[["PassengerId","Survived"]]


# ### IMPORTANT : due to the number of folders we created, commit will fail if we don't erase them. So let's do some cleaning

# In[ ]:


import shutil
shutil.rmtree("kaggle_pystacknet")


# ## Output for submission

# In[ ]:


output.to_csv("results.csv",index=False,header=True)

