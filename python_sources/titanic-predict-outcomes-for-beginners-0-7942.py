#!/usr/bin/env python
# coding: utf-8

# ## Kaggle Competition

# # Titanic : Machine Learning from Disaster

# **By Aziz Presswala**

# Steps:-
# 1. Machine Learning Problem
# 2. Exploratory Data Analysis
# 3. Preprocessing & Feature Engineering
# 4. Applying Machine Learning Models
# 5. Conclusion

# ## 1. Machine Learning Problem

# ### Data

# - Data is given in 2 files - train.csv (for training the model) & test.csv (for testing the accuracy of the model)
# - Given data contains 12 columns - PassengerID, PClass, SibSp, Parch, Age, Fare, Sex, Name, Ticket, Cabin, Embarked, Survived
# - Size of train.csv: 59.7KB, test.csv: 27.9KB
# - Number of Rows in train.csv: 891, test.csv: 418

# ### Type of ML Problem

# - It is a binary classification problem.
# - Given data about the passengers, task is to predict whether a passenger will survive the disaster or not.
# - 1 if the passenger survived, 0 if did not survive.

# ### Performance Metric

# - Accuracy (No. of correctly classified pts / Total no. of pts)
# - Confusion Matrix

# ## 2. Exploratory Data Analysis

# In[ ]:


# importing libraries
import warnings
warnings.filterwarnings("ignore")
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from mlxtend.classifier import StackingClassifier
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier
from sklearn.preprocessing import normalize

from keras.models import Sequential 
from keras.layers import Dense, Activation, Dropout
from keras.layers.normalization import BatchNormalization


# ### Loading the Data

# In[ ]:


# loading the train dataset
train_df = pd.read_csv("../input/train.csv")
print("Number of data points:",train_df.shape[0])


# In[ ]:


# loading the test dataset
test_df = pd.read_csv("../input/test.csv")
print("Number of data points:",test_df.shape[0])


# In[ ]:


# combining both the datasets for EDA
titanic = pd.concat([train_df, test_df], sort=False)


# In[ ]:


titanic.head()


# In[ ]:


titanic.info()


# - 3 columns of float datatype
# - 4 columns of int datatype
# - 5 columns of string

# In[ ]:


titanic.describe()


# ### Checking for NULL/Missing values

# In[ ]:


titanic.isnull().sum()


# - Columns: Age, Fare, Cabin & Embarked have missing values

# In[ ]:


# replacing the missing values of the Cabin column with 'unknown'
titanic.Cabin = titanic.Cabin.fillna("unknown")


# In[ ]:


# replacing the missing value of Embarked with the mode of the column
titanic.Embarked = titanic.Embarked.fillna(titanic['Embarked'].mode()[0])


# In[ ]:


# replacing the missing value of Fare with the mean of the column
titanic.Fare = titanic.Fare.fillna(titanic['Fare'].mean())


# In[ ]:


#using the title column to fill the age column
titanic['title']=titanic.Name.apply(lambda x: x.split('.')[0].split(',')[1].strip())


# In[ ]:


newtitles={
    "Capt":       "Officer",
    "Col":        "Officer",
    "Major":      "Officer",
    "Jonkheer":   "Royalty",
    "Don":        "Royalty",
    "Sir" :       "Royalty",
    "Dr":         "Officer",
    "Rev":        "Officer",
    "the Countess":"Royalty",
    "Dona":       "Royalty",
    "Mme":        "Mrs",
    "Mlle":       "Miss",
    "Ms":         "Mrs",
    "Mr" :        "Mr",
    "Mrs" :       "Mrs",
    "Miss" :      "Miss",
    "Master" :    "Master",
    "Lady" :      "Royalty"}


# In[ ]:


titanic['title']=titanic.title.map(newtitles)


# In[ ]:


titanic.groupby(['title','Sex']).Age.mean()


# In[ ]:


def newage (cols):
    title=cols[0]
    Sex=cols[1]
    Age=cols[2]
    if pd.isnull(Age):
        if title=='Master' and Sex=="male":
            return 4.57
        elif title=='Miss' and Sex=='female':
            return 21.8
        elif title=='Mr' and Sex=='male': 
            return 32.37
        elif title=='Mrs' and Sex=='female':
            return 35.72
        elif title=='Officer' and Sex=='female':
            return 49
        elif title=='Officer' and Sex=='male':
            return 46.56
        elif title=='Royalty' and Sex=='female':
            return 40.50
        else:
            return 42.33
    else:
        return Age


# In[ ]:


titanic.Age=titanic[['title','Sex','Age']].apply(newage, axis=1)


# ### Distribution of datapoints among output classes

# In[ ]:


titanic.groupby('Survived')['PassengerId'].count().plot.bar()


# In[ ]:


# from the above plot
print('Passengers that survived {} %'.format(round(titanic['Survived'].mean()*100,2)))
print('Passengers that did not survive {} %'.format(100 - round(titanic['Survived'].mean()*100,2)))


# ### Correlation Matrix

# In[ ]:


corr = train_df.corr()
sns.heatmap(corr, cbar=True, annot=True, square=True, 
            fmt='.2f', annot_kws={'size': 10}, 
            yticklabels=corr.columns.values, xticklabels=corr.columns.values)


# From the above matrix, it is evident that no feature has a high correlation with the class label - Survived.

# ### Pair plots of features - [Pclass, Fare, Age, Sibsp, Parch]

# In[ ]:


n = titanic.shape[0]
sns.pairplot(titanic[['Pclass', 'Fare', 'Age', 'SibSp', 'Parch', 'Survived']][0:n], hue='Survived', 
             vars=['Pclass', 'Fare', 'Age', 'SibSp', 'Parch'])
plt.show()


# Observations:-
# - Passengers of Class 1 & 2 were given more preference than passengers of class 3.
# - Passengers whose Ticket Fare was more were a higher preference.
# - Passengers who did'nt have any parents/children onboard were given a higher preference.
# - The Pclass vs Age plot can classify the datapoints to a certain extent, therefore, Age & Pclass are very important features.

# ### Bar Plots

# In[ ]:


plt.figure(figsize=[12,10])
plt.subplot(2,2,1)
sns.barplot('Sex','Survived',data=train_df)
plt.subplot(2,2,2)
sns.barplot('Embarked','Survived',data=train_df)


# Observations:-
# - Probability of survival of females is significantly more than males.
# - Probability of survival of people who embarked from Cherbourg(C) is high.

# ## 3. Preprocessing & Feature Engineering

# - Feature - Name, a good strategy can be to take the count of number of characters
# - Feature - Cabin, a good strategy will be to make a new column HasCabin.
# - Feature - Ticket has no significance, therfore it can be dropped.
# - Feature - Sex & Embarked, we can perform one hot encoding.
# - Creating 2 new features - FamilySize (Parch + SibSp) & IsAlone.

# In[ ]:


# taking the count of characcters in Name
titanic['Name1'] = titanic.Name.apply(lambda x:len(x))


# In[ ]:


titanic['HasCabin'] = titanic['Cabin'].apply(lambda x:0 if x=='unknown' else 1)


# In[ ]:


titanic['FamilySize'] = titanic['SibSp'] + titanic['Parch']


# In[ ]:


titanic['IsAlone'] = titanic['FamilySize'].apply(lambda x:1 if x==0 else 0)


# In[ ]:


titanic = titanic.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'],axis=1)


# In[ ]:


# performing one hot encoding of the categorical features
titanic = pd.get_dummies(titanic)


# In[ ]:


# now the dataset is ready, ML model can be trained on it
titanic.head()


# ### Correlation Matrix for new features

# In[ ]:


corr = titanic.corr()
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(corr, cbar=True, annot=True, square=True, 
            fmt='.2f', annot_kws={'size': 8},
            yticklabels=corr.columns.values, xticklabels=corr.columns.values)


# - Here we can see that the engineered features - title, Name1, HasCabin, IsAlone have a high correlation with the class label Survived.

# ## 4. Applying Machine Learning Models

# ### Splitting into Train & Test

# In[ ]:


train_len = train_df.shape[0]
train=titanic[:train_len]
test=titanic[train_len:]


# In[ ]:


# changing the type of the class label from float to int
train.Survived=train.Survived.astype('int')
train.Survived.dtype


# In[ ]:


X_train = train.drop("Survived",axis=1)
y_train = train['Survived']
X_test = test.drop("Survived", axis=1)


# In[ ]:


# normalizing the train & test dataset
X_train = normalize(X_train)
X_test = normalize(X_test)


# In[ ]:


print(X_train.shape)
print(X_test.shape)


# ## Logistic Regression

# In[ ]:


# initializing Logistic Regression model with L2 regularisation
lr = LogisticRegression(penalty='l2')

# C values we need to try on classifier
C = [1000,500,100,50,10,5,1,0.5,0.1,0.05,0.01,0.005,0.001,0.0005,0.0001]
param_grid = {'C':C}

# using GridSearchCV to find the optimal value of C
# using roc_auc as the scoring parameter & applying 10 fold CV
gscv = GridSearchCV(lr,param_grid,scoring='accuracy',cv=10,return_train_score=True)

gscv.fit(X_train,y_train)

print("Best C Value: ",gscv.best_params_)
print("Best Accuracy: %.5f"%(gscv.best_score_))


# In[ ]:


# determining optimal C
optimal_C = gscv.best_params_['C']

#training the model using the optimal C
lrf = LogisticRegression(penalty='l2', C=optimal_C)
lrf.fit(X_train,y_train)

#predicting the class label using test data 
y_pred = lrf.predict(X_test)


# In[ ]:


# confusion matrix on train data
y_predict = lrf.predict(X_train)
cm = confusion_matrix(y_train, y_predict)
sns.heatmap(cm, annot=True, annot_kws={"size": 16}, fmt='g')


# In[ ]:


output=pd.DataFrame({'PassengerId':test_df['PassengerId'],'Survived':y_pred})
output.to_csv('submission.csv', index=False)


# **Result** - This model has an accuracy score of **77.51%** on test data

# ## Support Vector Machines

# In[ ]:


# initializing Linear SVM model with L1 regularisation
svm = SGDClassifier(loss='hinge', penalty='l1')

# C values we need to try on classifier
alpha_values = [1000,500,100,50,10,5,1,0.5,0.1,0.05,0.01,0.005,0.001,0.0005,0.0001,0.00001]
param_grid = {'alpha':alpha_values}

# using GridSearchCV to find the optimal value of alpha
# using roc_auc as the scoring parameter & applying 10 fold CV
gscv = GridSearchCV(svm,param_grid,scoring='accuracy',cv=10,return_train_score=True)

gscv.fit(X_train,y_train)

print("Best alpha Value: ",gscv.best_params_)
print("Best Accuracy: %.5f"%(gscv.best_score_))


# In[ ]:


# determining optimal alpha
optimal_alpha = gscv.best_params_['alpha']

#training the model using the optimal alpha
svm = SGDClassifier(loss='hinge', penalty='l1', alpha=optimal_alpha)
svm.fit(X_train,y_train)

#predicting the class label using test data 
y_pred = svm.predict(X_test)


# In[ ]:


# confusion matrix on train data
y_predict = svm.predict(X_train)
cm = confusion_matrix(y_train, y_predict)
sns.heatmap(cm, annot=True, annot_kws={"size": 16}, fmt='g')


# In[ ]:


output=pd.DataFrame({'PassengerId':test_df['PassengerId'],'Survived':y_pred})
output.to_csv('submission.csv', index=False)


# **Result** - This model has an accuracy score of **72.24%** on test data

# ## K Nearest Neighbors

# In[ ]:


# initializing KNN model 
knn = KNeighborsClassifier(weights='uniform')

# C values we need to try on classifier
neighbors = [5, 7, 9, 11, 15, 21, 25, 31, 35, 41, 47, 52]
param_grid = {'n_neighbors':neighbors}

# using GridSearchCV to find the optimal value of k
# using roc_auc as the scoring parameter & applying 10 fold CV
gscv = GridSearchCV(knn,param_grid,scoring='accuracy',cv=10,return_train_score=True)

gscv.fit(X_train,y_train)

print("Best k Value: ",gscv.best_params_)
print("Best Accuracy: %.5f"%(gscv.best_score_))


# In[ ]:


# determining optimal neighbors
optimal_k = gscv.best_params_['n_neighbors']

#training the model using the optimal k
knn = KNeighborsClassifier(n_neighbors=optimal_k, weights='uniform')
knn.fit(X_train,y_train)

#predicting the class label using test data 
y_pred = knn.predict(X_test)


# In[ ]:


# confusion matrix on train data
y_predict = knn.predict(X_train)
cm = confusion_matrix(y_train, y_predict)
sns.heatmap(cm, annot=True, annot_kws={"size": 16}, fmt='g')


# In[ ]:


output=pd.DataFrame({'PassengerId':test_df['PassengerId'],'Survived':y_pred})
output.to_csv('submission.csv', index=False)


# **Result** - This model has an accuracy score of **70.34%** on test data

# ## Decision Tree

# In[ ]:


# initializing DT model 
dt = DecisionTreeClassifier(class_weight='balanced')

# max_depth values we need to try on classifier
depth = [5, 7, 9, 11, 15, 21, 25, 31, 35, 41, 47, 52]
param_grid = {'max_depth':depth}

# using GridSearchCV to find the optimal value of k
# using roc_auc as the scoring parameter & applying 10 fold CV
gscv = GridSearchCV(dt,param_grid,scoring='accuracy',cv=10,return_train_score=True)

gscv.fit(X_train,y_train)

print("Best depth Value: ",gscv.best_params_)
print("Best Accuracy: %.5f"%(gscv.best_score_))


# In[ ]:


# determining optimal max_depth
optimal_depth = gscv.best_params_['max_depth']

#training the model using the optimal k
dt = DecisionTreeClassifier(max_depth=optimal_depth, class_weight='balanced')
dt.fit(X_train,y_train)

#predicting the class label using test data 
y_pred = dt.predict(X_test)


# In[ ]:


# confusion matrix on train data
y_predict = dt.predict(X_train)
cm = confusion_matrix(y_train, y_predict)
sns.heatmap(cm, annot=True, annot_kws={"size": 16}, fmt='g')


# In[ ]:


output=pd.DataFrame({'PassengerId':test_df['PassengerId'],'Survived':y_pred})
output.to_csv('submission.csv', index=False)


# **Result** - This model has an accuracy score of **76.55%** on test data

# ## Random Forest

# In[ ]:


rf=RandomForestClassifier(random_state=1)

params={'n_estimators': list(range(10,100,10)),
      'max_depth':[3,4,5,6,7,8,9,10],
      'criterion':['gini','entropy']}

gscv=GridSearchCV(estimator=rf, param_grid=params, scoring='accuracy', cv=10, return_train_score=True)
gscv.fit(X_train,y_train)
print("Best C Value: ",gscv.best_params_)
print("Best Accuracy: %.5f"%(gscv.best_score_))


# In[ ]:


#training the model using the optimal params
rf = RandomForestClassifier(random_state=1, criterion='gini', max_depth= 4, n_estimators=20)
rf.fit(X_train,y_train)

#predicting the class label using test data 
y_pred = rf.predict(X_test)


# In[ ]:


# confusion matrix on train data
y_predict = rf.predict(X_train)
cm = confusion_matrix(y_train, y_predict)
sns.heatmap(cm, annot=True, annot_kws={"size": 16}, fmt='g')


# In[ ]:


output=pd.DataFrame({'PassengerId':test_df['PassengerId'],'Survived':y_pred})
output.to_csv('submission.csv', index=False)


# **Result** - This model has an accuracy score of **79.42%** on test data

# ## XGBoost

# In[ ]:


param_grid={
    'max_depth':list(range(2,10)),
    'n_estimators':list(range(50,500,50)),
}

xgb = XGBClassifier(objective='binary:logistic')
rscv = GridSearchCV(xgb, param_grid, scoring='accuracy', n_jobs=-1, return_train_score=True)
rscv.fit(X_train, y_train)
print("Best Max_Depth:",rscv.best_params_['max_depth'])
print("Best N estimators:",rscv.best_params_['n_estimators'])
print("Best Accuracy: %.5f"%(rscv.best_score_))


# In[ ]:


#training the model using the optimal params
xgb = XGBClassifier(learning_rate=0.2, max_depth=4, n_estimators=150)
xgb.fit(X_train,y_train)

#predicting the class label using test data 
y_pred = xgb.predict(X_test)


# In[ ]:


# confusion matrix on train data
y_predict = xgb.predict(X_train)
cm = confusion_matrix(y_train, y_predict)
sns.heatmap(cm, annot=True, annot_kws={"size": 16}, fmt='g')


# In[ ]:


features = X_train.columns
importances = xgb.feature_importances_
indices = (np.argsort(importances))
plt.figure(figsize=(8,8))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], color='r', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()


# In[ ]:


output=pd.DataFrame({'PassengerId':test_df['PassengerId'],'Survived':y_pred})
output.to_csv('submission.csv', index=False)


# **Result** - This model has an accuracy score of **75.11%** on test data

# ## Stacking Classifier

# In[ ]:


clf1 = DecisionTreeClassifier(max_depth=5, class_weight='balanced')
clf2 = LogisticRegression(penalty='l2',C=10)
clf3 = XGBClassifier(learning_rate=0.2, max_depth=4, n_estimators=150)
rf = RandomForestClassifier(criterion='entropy', max_depth= 9, n_estimators=90)

sclf = StackingClassifier(classifiers=[clf1, clf2, clf3], 
                          meta_classifier=rf)

sclf.fit(X_train, y_train)


# In[ ]:


#predicting the class label using test data 
y_pred = sclf.predict(X_test)


# In[ ]:


# confusion matrix on train data
y_predict = sclf.predict(X_train)
cm = confusion_matrix(y_train, y_predict)
sns.heatmap(cm, annot=True, annot_kws={"size": 16}, fmt='g')


# In[ ]:


output=pd.DataFrame({'PassengerId':test_df['PassengerId'],'Survived':y_pred})
output.to_csv('submission.csv', index=False)


# **Result** - This model has an accuracy score of **73.68%** on test data

# ## Neural Networks

# In[ ]:


from keras.utils import to_categorical
y_train_new = to_categorical(y_train)


# In[ ]:


# using He Normalization for weights initialization
model = Sequential()

# Layer 1 - 64 neurons
model.add(Dense(64, activation='relu', input_dim=X_train.shape[1]))
model.add(BatchNormalization())

# Layer 2 - 32 neurons
model.add(Dense(32, activation='relu', kernel_initializer='he_normal'))
model.add(BatchNormalization())

model.add(Dense(2, activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train_new, batch_size=128, epochs=10, verbose=1)


# In[ ]:


y_pred = model.predict(X_test)
y_classes = y_pred.argmax(axis=-1)


# In[ ]:


output=pd.DataFrame({'PassengerId':test_df['PassengerId'],'Survived':y_classes})
output.to_csv('submission.csv', index=False)


# ## 5. Conclusion

# In[ ]:


from prettytable import PrettyTable 
x = PrettyTable()
x.field_names = ["Model", "Train Accuracy(%)", "Test Accuracy(%)"]
x.add_row(['Logistic Regression', '82.49', '77.51'])
x.add_row(['Support Vector Machines', '77.44', '72.24'])
x.add_row(['K Nearest Neighbor', '72.84', '70.34'])
x.add_row(['Decision Tree', '80.80', '76.55'])
x.add_row(['Random Forest', '83.95', '79.42'])
x.add_row(['XGBoost', '83.61', '75.11'])
x.add_row(['Stacking Classifier', '-', '73.68'])
x.add_row(['Neural Networks', '81.59', ''])
print(x)


# - From the above table we conclude that Random Forest model performs the best with 79.42% test accuracy followed by Logistic Regression & Decision Tree.
