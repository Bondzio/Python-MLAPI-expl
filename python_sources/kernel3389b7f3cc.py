#!/usr/bin/env python
# coding: utf-8

# In[148]:


# This Python 3 environment comes with many helpful analytics libraries installed

# data analysis and wrangling
import pandas as pd
import numpy as np
import random as rnd

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
sns.set() # setting seaborn default for plots
from sklearn import metrics
get_ipython().run_line_magic('matplotlib', 'inline')


# In[149]:


train_df = pd.read_csv('../input/train.csv')
test_df = pd.read_csv('../input/test.csv')


# In[150]:


train_df.columns


# In[151]:


train_df.head()


# * Categorical: Survived, Sex, and Embarked. Ordinal: Pclass. <br>
# * Continous: Age, Fare. <br>
# * Discrete: SibSp, Parch. <br>

# In[152]:


train_df.describe()


# In[153]:


train_df.info()


# In[154]:


test_df.info()


# In[155]:


train_df.isnull().sum()


# In[156]:


test_df.isnull().sum()


# # Data Visualization

# In[157]:


train_df['Survived'].value_counts()


# In[158]:


def bar_chart(feature):
    survived = train_df[train_df['Survived']==1][feature].value_counts()
    dead = train_df[train_df['Survived']==0][feature].value_counts()
    df = pd.DataFrame([survived,dead])
    df.index = ['Survived','Dead']
    df.plot(kind='bar',stacked=True, figsize=(10,5))


# In[159]:


bar_chart('Sex')


# In[160]:


train_df[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[161]:


bar_chart('Pclass')


# In[162]:


train_df[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[163]:


train_df[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[164]:


train_df[["Parch", "Survived"]].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[165]:


g = sns.FacetGrid(train_df, col='Survived')
g.map(plt.hist, 'Age', bins=20)


# # Feature engineering

# # Data Preprocessing

# In[166]:


train_df = pd.read_csv('../input/train.csv')
test_df = pd.read_csv('../input/test.csv')
train_df.columns


# In[167]:


train_test_data = [train_df, test_df] # combining train and test dataset

for dataset in train_test_data:
    dataset['Title'] = dataset['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

title_mapping = {"Mr": 0, "Miss": 1, "Mrs": 2, 
                 "Master": 3, "Dr": 3, "Rev": 3, "Col": 3, "Major": 3, "Mlle": 3,"Countess": 3,
                 "Ms": 3, "Lady": 3, "Jonkheer": 3, "Don": 3, "Dona" : 3, "Mme": 3,"Capt": 3,"Sir": 3 }
for dataset in train_test_data:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    


# In[168]:


train_df.columns


# In[169]:


# train_df['Has_family'] = train_df['SibSp'] + train_df['Parch']
# test_df['Has_family'] = test_df['SibSp'] + test_df['Parch']
# train_df[train_df['Has_family']>0] = 1
# test_df[test_df['Has_family']>0] = 1


# In[170]:


X_train_df = train_df.drop(columns=['Survived', 'PassengerId', 'Name', 'Ticket', 'Cabin'])
X_test_df = test_df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])


# In[171]:


y_train_df = train_df['Survived']


# In[172]:


X_train_df.isnull().sum()


# In[173]:


X_test_df.isnull().sum()


# In[174]:


age_med = train_df.Age.median()
X_train_df.Age.fillna(age_med, inplace=True)
X_test_df.Age.fillna(age_med, inplace=True)


# In[175]:


mod = X_train_df.Embarked.value_counts().argmax()
X_train_df.Embarked.fillna(mod, inplace=True)


# In[176]:


fare_med = train_df.Fare.median()
X_test_df.Fare.fillna(fare_med, inplace=True)


# In[177]:


X_train_df.isnull().sum()


# In[178]:


X_test_df.isnull().sum()


# # Lable Encoding

# In[179]:


X_train_df.columns


# In[180]:


X_train_df.replace({"male": 0, "female": 1}, inplace=True)
X_test_df.replace({"male": 0, "female": 1}, inplace=True)
X_train_df.replace({"S": 0, "C": 1, "Q": 2}, inplace=True)
X_test_df.replace({"S": 0, "C": 1, "Q": 2}, inplace=True)


# In[181]:


X_train_df.head()


# # OneHot Encoding

# In[182]:


X_train_df = pd.get_dummies(X_train_df, columns=['Pclass', 'Embarked', 'Title'], drop_first=True)
X_test_df = pd.get_dummies(X_test_df, columns=['Pclass', 'Embarked', 'Title'], drop_first=True)
X_train_df.head()


# In[183]:


X_train_df.shape, X_test_df.shape


# ## Data Scaling

# In[184]:


from sklearn.preprocessing import MinMaxScaler
sc_X = MinMaxScaler()
X_train_sc = sc_X.fit_transform(X_train_df)
X_test_sc = sc_X.transform(X_test_df)


# # Algorithms Training

# In[185]:


from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble  import GradientBoostingClassifier,AdaBoostClassifier
from sklearn.ensemble  import BaggingClassifier
from sklearn.metrics import r2_score


# In[193]:


g_l=GradientBoostingClassifier(max_depth=7,subsample=.90,n_estimators=200)
g_l.fit(X_train_sc, y_train_df)
y_pre=g_l.predict(X_train_sc)
r2_score(y_train_df,y_pre)


# In[194]:


b_r=BaggingClassifier(base_estimator=g_l,bootstrap_features=True,n_estimators=150)
b_r.fit(X_train_sc, y_train_df)
y_pre=b_r.predict(X_train_sc)
r2_score(y_train_df,y_pre)


# In[198]:


logi_clf = LogisticRegression(random_state=0)
logi_parm = {"penalty": ['l1', 'l2'], "C": [0.1, 0.5, 1, 5, 10, 50]}

svm_clf = SVC(random_state=0)
svm_parm = {'kernel': ['rbf', 'poly'], 'C': [1, 5, 50, 100, 500, 1000], 'degree': [3, 5, 7], 
            'gamma': ['auto', 'scale']}

dt_clf = DecisionTreeClassifier(random_state=0)
dt_parm = {'criterion':['gini', 'entropy']}

knn_clf = KNeighborsClassifier()
knn_parm = {'n_neighbors':[5, 10, 15, 20], 'weights':['uniform', 'distance'], 'p': [1,2]}
dt=DecisionTreeClassifier()
gnb_clf = GaussianNB()
gnb_parm = {'priors':['None']}


ada=AdaBoostClassifier(base_estimator=dt)
ada_parm={'learning_rate':[.01, .1, .001], 'n_estimators':[50, 100,150,200],}


clfs = [logi_clf, svm_clf, dt_clf, knn_clf,ada]
params = [logi_parm, svm_parm, dt_parm, knn_parm,ada_parm] 


# In[199]:


clfs_opt = []
clfs_best_scores = []
clfs_best_param = []
for clf_, param in zip(clfs, params):
    clf = RandomizedSearchCV(clf_, param, cv=5)
    clf.fit(X_train_sc, y_train_df)
    clfs_opt.append(clf)
    clfs_best_scores.append(clf.best_score_)
    clfs_best_param.append(clf.best_params_)


# In[200]:


max(clfs_best_scores)


# In[203]:


clfs_best_param


# In[201]:


arg = np.argmax(clfs_best_scores)
clfs_best_param[arg]


# In[202]:


clf = clfs_opt[arg]


# In[ ]:


pred = b_r.predict(X_test_sc)
test_df = pd.read_csv('../input/test.csv')
y_test_df = test_df['PassengerId']


# In[ ]:


# dataset.loc[ dataset['Age'] <= 16, 'Age']= 0
# dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
# dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
# dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
# dataset.loc[ dataset['Age'] > 64, 'Age']    


# In[204]:


clfs_best_param


# In[ ]:


from sklearn.ensemble import RandomForestClassifier, VotingClassifier
logi_clf = LogisticRegression(random_state=0,penalty= 'l1' , C = 50)
svm_clf = SVC(probability=True,random_state=0,kernel= 'rbf', gamma= 'scale', degree= 5, C= 50)
dt_clf = DecisionTreeClassifier(random_state=0,criterion= 'gini')
knn_clf = KNeighborsClassifier(weights= 'uniform', p= 2, n_neighbors= 15)
gnb_clf = GaussianNB()
ada=AdaBoostClassifier(n_estimators=50,learning_rate=.001)


# In[ ]:


eclf2 = VotingClassifier(estimators=[('LogisticRegression', logi_clf), ('svc', svm_clf), ('DecisionTreeClassifier', dt_clf),('knn_clf',knn_clf),('GaussianNB',gnb_clf),('gradientboost',b_r),('ada_boost',ada)],voting='soft')
eclf2.fit(X_train_sc, y_train_df)


# In[ ]:


y_pre=eclf2.predict(X_test_sc)


# In[ ]:


y_pre_train=eclf2.predict(X_train_sc)
metrics.accuracy_score(y_train_df,y_pre_train)


# In[ ]:


y_predict_test=eclf2.predict(X_test_sc)
cols = ['PassengerId', 'Survived']
submit_df = pd.DataFrame(np.hstack((y_test_df.values.reshape(-1,1),y_predict_test.reshape(-1,1))), 
                         columns=cols)


# In[ ]:


submit_df.to_csv('submission.csv', index=False)

