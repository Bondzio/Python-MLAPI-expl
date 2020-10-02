#!/usr/bin/env python
# coding: utf-8

# # Titanic Survival Predicton

# The objective is to predict if passanger has survived or not.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


train=pd.read_csv("../input/train.csv")
test=pd.read_csv("../input/test.csv")

print("Train dataset has {} samples and {} attributes".format(*train.shape))
print("Test dataset has {} samples and {} attributes".format(*test.shape))


# In[ ]:


train.head()


# We have 11 feature columns and target variable **Survived** which is binary.

# Pclass, Sex and Embarked are **Categorical** Features while Age, SibSp, Parch and Fare are **continuous** variables.

# We will use Name, Ticket and Cabin variable in Feature Engineering

# ## EDA

# In[ ]:


n=len(train)
surv_0=len(train[train['Survived']==0])
surv_1=len(train[train['Survived']==1])

print("% of passanger survived in train dataset: ",surv_1*100/n)
print("% of passanger not survived in train dataset: ",surv_0*100/n)


# Passanger not survived has edge over survived passanger.  

# And even if we do nothing we would get approximately 61% accuracy by simple marking all passangers as not survived(**Accuracy Paradox**). So our aim should be to get accuracy higher than this.

# ### Let's find correlation between Numeric Variable

# In[ ]:


cat=['Pclass','Sex','Embarked']
num=['Age','SibSp','Parch','Fare']


# In[ ]:


corr_df=train[num]  #New dataframe to calculate correlation between numeric features
cor= corr_df.corr(method='pearson')
print(cor)


# In[ ]:


fig, ax =plt.subplots(figsize=(8, 6))
plt.title("Correlation Plot")
sns.heatmap(cor, mask=np.zeros_like(cor, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax)
plt.show()


# There's no strong correlation between any two variables. The strongest correlation is between **SibSp** and **Parch** features (0.414).

#  I would like to keep all the features as there is no strong evidence of data redundancy.

# ### Let's use chi-square test to understand relationship between categorical variables and target variable

# In[ ]:


csq=chi2_contingency(pd.crosstab(train['Survived'], train['Sex']))
print("P-value: ",csq[1])


# In[ ]:


csq2=chi2_contingency(pd.crosstab(train['Survived'], train['Embarked']))
print("P-value: ",csq2[1])


# In[ ]:


csq3=chi2_contingency(pd.crosstab(train['Survived'], train['Pclass']))
print("P-value: ",csq3[1])


# P values for features Sex, Embarked and Pclass are very low. So we can reject our Null Hypothesis which is these features are independent and have no relationship with target variable

# So these features contribute by providing some information.

# ## Visualization 

# * Let's check which features contain missing values

# In[ ]:


print(train.isnull().sum())


# In[ ]:


print(test.isnull().sum())


# Only 4 features have missing values

# #### Age

# In[ ]:


train['Age'].describe()


# ****Let's replace missing values by median of Age.

# In[ ]:


med=np.nanmedian(train['Age'])
train['Age']=train['Age'].fillna(med)
test['Age']=test['Age'].fillna(med)


# #### Cabin

# In[ ]:


train['Cabin'].value_counts()


# Let's replace NaN by 0

# In[ ]:


train['Cabin']=train['Cabin'].fillna(0)
test['Cabin']=test['Cabin'].fillna(0)


# #### Embarked****

# In[ ]:


train['Embarked'].value_counts()


#  Let's replace the NaN by mode

# In[ ]:


train['Cabin']=train['Cabin'].fillna("S")


# #### Fare

# In[ ]:


train['Fare'].describe()


# In[ ]:


med=np.nanmedian(train['Fare'])
test['Fare']=test['Fare'].fillna(med)


# ## Feature Engineering

# from **cabin** let's create a new feature **hasCabin** 

# In[ ]:


train['hasCabin']=train['Cabin'].apply(lambda x: 0 if x==0 else 1)
test['hasCabin']=test['Cabin'].apply(lambda x: 0 if x==0 else 1)


# * Let's combine SibSp and Parch features to create new one **FamilyMem**

# In[ ]:


train['FamilyMem']=train.apply(lambda x: x['SibSp']+x['Parch'], axis=1)
test['FamilyMem']=test.apply(lambda x: x['SibSp']+x['Parch'], axis=1)


# Let's use prefixes in the name to Create a new column **Title** 

# In[ ]:


def get_title(name):
    title_search = re.search(' ([A-Za-z]+)\.', name)
    if title_search:
        return title_search.group(1)
    return ""


# In[ ]:


train['title']=train['Name'].apply(get_title)
test['title']=test['Name'].apply(get_title)


# In[ ]:


title_lev1=list(train['title'].value_counts().reset_index()['index'])
title_lev2=list(test['title'].value_counts().reset_index()['index'])


# In[ ]:


title_lev=list(set().union(title_lev1, title_lev2))
print(title_lev)


# ### Assigning datatypes

# In[ ]:


train['title']=pd.Categorical(train['title'], categories=title_lev)
test['title']=pd.Categorical(test['title'], categories=title_lev)


# In[ ]:


cols=['Pclass','Sex','Embarked','hasCabin','title']
fcol=['Pclass','Sex','Embarked','hasCabin','title','Age','FamilyMem','Fare']


# In[ ]:


for c in cols:
    train[c]=train[c].astype('category')
    test[c]=test[c].astype('category')


# ###  Let's create dummy variables

# In[ ]:


train_df=train[fcol]
test_df=test[fcol]


# In[ ]:


train_df=pd.get_dummies(train_df, columns=cols, drop_first=True)
test_df=pd.get_dummies(test_df, columns=cols, drop_first=True)


# In[ ]:


y=train['Survived']


# ## Data seperation test and train

# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(train_df, y, test_size=0.3, random_state=42)


# # Start Creating Model

# ## 0. Decision Tree

# In[ ]:


prams_DTree = {
    'min_samples_split' : range(10,500,20),
    'max_depth': range(1,20,2)
}

from sklearn.tree import DecisionTreeClassifier
clf_DTree = DecisionTreeClassifier()
clf_DTree = GridSearchCV(clf_DTree, prams_DTree)
clf_DTree.fit(x_train, y_train)
print("Best: %f using %s" % (clf_DTree.best_score_, clf_DTree.best_params_))
clf_Dtree_preds = clf_DTree.predict(x_test)
print("0. Accuracy for Random Forest on CV data: ",accuracy_score(y_test,clf_Dtree_preds))


# ## 1. Random Forest

# In[ ]:


params_rf = { 
    'n_estimators': [200, 500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,5,6,7,8],
    'criterion' :['gini', 'entropy']
}
rfc=RandomForestClassifier(random_state=42)
clf_rf = GridSearchCV(estimator=rfc, param_grid=params_rf, cv= 5)
clf_rf.fit(x_train, y_train)
print("Best: %f using %s" % (clf_rf.best_score_, clf_rf.best_params_))
clf_rf_preds = clf_rf.predict(x_test)
print("1. Accuracy for Random Forest on CV data: ",accuracy_score(y_test,clf_rf_preds))


# ### 2. Support vector machine - SVM

# In[ ]:


from sklearn import svm

params_svm = {
    'kernel':('linear', 'rbf'),
    'C':(1,0.25,0.5,0.75),
    'gamma': (1,2,3,'auto'),
    'decision_function_shape':('ovo','ovr'),
    'shrinking':(True,False)
}

svc = svm.SVC(gamma="scale")
clf_svm = GridSearchCV(svc, params_svm, cv=5)

get_ipython().run_line_magic('time', 'clf_svm.fit(x_train, y_train)')
print("Best: %f using %s" % (clf_svm.best_score_, clf_svm.best_params_))

get_ipython().run_line_magic('time', 'clf_svm_preds = clf_svm.predict(x_test)')
print("2. Accuracy for SVM on CV data: ",accuracy_score(y_test,clf_svm_preds))


# ## 3. LogisticRegression

# In[ ]:


from sklearn.linear_model import LogisticRegression
svm_parameters = {
    'dual': [True,False],
    'max_iter': [100,110,120,130,140],
    'C': [1.0,1.5,2.0,2.5]
}

lr = LogisticRegression(penalty='l2')
clf_lr = GridSearchCV(lr, svm_parameters, cv = 5)

get_ipython().run_line_magic('time', 'clf_lr.fit(x_train, y_train)')
# print("Best: %f using %s" % (clf_lr.best_score_, clf_lr.best_params_))

get_ipython().run_line_magic('time', 'clf_lr_preds = clf_lr.predict(x_test)')
# print("3. Accuracy for LogisticRegression on CV data: ",accuracy_score(y_test,clf_lr_preds))


# ## 4. Naive Bayes 
# No need to grid search due to there are no parameters to tune

# In[ ]:


from sklearn.naive_bayes import GaussianNB
clf_nb = GaussianNB()
get_ipython().run_line_magic('time', 'clf_nb.fit(x_train, y_train)')
get_ipython().run_line_magic('time', 'clf_nb_preds = clf_nb.predict(x_test)')
print("4. Accuracy for Naive bayas on CV data: ",accuracy_score(y_test, clf_nb_preds))


# ## 5. AdaBoostClassifier

# In[ ]:


DTC = DecisionTreeClassifier(random_state = 11,
#                              max_features = "auto",
#                              class_weight = "balanced",
#                              max_depth = None
                            )

from sklearn.ensemble import AdaBoostClassifier
params_abc = {"base_estimator__criterion" : ["gini", "entropy"],
              "base_estimator__splitter" :   ["best", "random"],
              "n_estimators": [1, 2]
             }

ABC = AdaBoostClassifier(base_estimator = DTC)

clf_abc = GridSearchCV(ABC, param_grid=params_abc)
clf_abc.fit(x_train, y_train)

get_ipython().run_line_magic('time', 'clf_abc_preds = clf_abc.predict(x_test)')
print("5. Accuracy for Ada boost on CV data: ",accuracy_score(y_test, clf_abc_preds))

