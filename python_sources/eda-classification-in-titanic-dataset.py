#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
train = pd.read_csv('../input/titanic/train.csv')
test = pd.read_csv('../input/titanic/test.csv')
gender = pd.read_csv('../input/titanic/gender_submission.csv')


# In[ ]:


train.head()


# In[ ]:


gender.head()


# In[ ]:


test.head()


# In[ ]:


test = pd.merge(test,gender,on=['PassengerId'])
test.head()


# In[ ]:


train.info()
test.info()


# In[ ]:


for i in train['Age'] : 
    train['Age'].fillna(train['Age'].median(), inplace = True)
for j in test['Age'] : 
    test['Age'].fillna(test['Age'].median(), inplace = True)

for k in train['Embarked'] :
    train['Embarked'].fillna(train['Embarked'].mode()[0], inplace = True)
for l in test['Embarked'] :
    test['Embarked'].fillna(test['Embarked'].mode()[0], inplace = True)


# In[ ]:


train.info()
test.info()


# In[ ]:


#Changing the sex column with 0 and 1
def gen(Gen):
    if Gen == 'male':
        return 0
    elif Gen == 'female':
        return 1
train['Sex'] = train['Sex'].apply(gen)
test['Sex'] = test['Sex'].apply(gen)


# In[ ]:


train['Title'] = [i.split('.')[0] for i in train.Name.astype('str')]
train['Title'] = [i.split(',')[1] for i in train.Title.astype('str')]
train.head()


# In[ ]:


test['Title'] = [i.split('.')[0] for i in test.Name.astype('str')]
test['Title'] = [i.split(',')[1] for i in test.Title.astype('str')]
test.head()


# In[ ]:


test['Embarked'].unique()


# In[ ]:


import seaborn as sns 
import matplotlib.pyplot as plt
plt.subplots(figsize=(10,8))
sns.countplot(x="Embarked",data=train,hue = "Survived").set_title("Embarked in Titanic ")


# In[ ]:


train['Embarked'].value_counts()


# In[ ]:


train['Pclass'].unique()


# In[ ]:


train['Pclass'].value_counts()


# In[ ]:


plt.subplots(figsize=(10,8))
sns.countplot(x="Pclass",data=train,hue = "Survived").set_title("Pclass in Titanic ")


# In[ ]:


train['Title'].unique()


# In[ ]:


def Title(t):
    if t == ' the Countess' or t == ' Mlle' or t == ' Sir' or t == ' Ms' or t ==' Lady' or t ==' Mme':
        return "special"
    elif t == ' Mrs':
        return ' Mrs'
    elif t == ' Miss':
        return ' Miss'
    elif t == ' Master':
        return ' Master'
    elif t == ' Col':
        return ' Col'
    elif t == ' Major':
        return ' Major'
    elif t == ' Dr':
        return ' Dr'
    elif t == ' Mr':
        return ' Mr'
    else:
        return 'another'

train['Title'] = train['Title'].apply(Title)
test['Title'] = test['Title'].apply(Title)


# In[ ]:


train['Title'].value_counts()


# In[ ]:


plt.subplots(figsize=(10,8))
sns.countplot(x="Title",data=train).set_title("People in Titanic based on the title")


# In[ ]:


#graph distribution of quantitative data
plt.figure(figsize=[16,12])


plt.subplot(234)
plt.hist(x = [train[train['Survived']==1]['Fare'], train[train['Survived']==0]['Fare']], 
         stacked=True, color = ['g','r'],label = ['Survived','Dead'])
plt.title('Fare Histogram by Survival')
plt.xlabel('Fare ($)')
plt.ylabel('# of Passengers')
plt.legend()

plt.subplot(235)
plt.hist(x = [train[train['Survived']==1]['Age'], train[train['Survived']==0]['Age']], 
         stacked=True, color = ['g','r'],label = ['Survived','Dead'])
plt.title('Age Histogram by Survival')
plt.xlabel('Age')
plt.ylabel('# of Passengers')
plt.legend()


# In[ ]:


drop_column = ['PassengerId']
train.drop(drop_column, axis=1, inplace = True)
test.drop(drop_column, axis=1, inplace = True)


# In[ ]:


train.groupby('Survived').mean()


# In[ ]:


train = pd.get_dummies(train, columns = ['Embarked'])
test = pd.get_dummies(test, columns = ['Embarked'])


# In[ ]:


drop_column = ['Cabin', 'Ticket']
train.drop(drop_column, axis=1, inplace = True)
test.drop(drop_column, axis=1, inplace = True)


# In[ ]:


train = pd.get_dummies(train, columns = ['Title'])
test = pd.get_dummies(test, columns = ['Title'])


# In[ ]:


train.head()


# **Feature selection to do classification by using ML method**

# In[ ]:


x = train.iloc[:,3:]  #delete target column from train dataset
y = train['Survived'] # test dataset  


# In[ ]:


from sklearn.model_selection import train_test_split
# divide dataset into 65% train, and other 35% test.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35, random_state=0)


# knowing the class that will be classified based on the data

# In[ ]:


train['Survived'].unique()


# **Make the classification, to predict anyone who survived or not by using various classifier**

# 1. K - Nearest neighbour

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix 
classifier1 = KNeighborsClassifier(n_neighbors=2)
classifier1.fit(x_train, y_train)
#Predicting the Test set results 
y_pred = classifier1.predict(x_test)
#Making the confusion matrix 
cm = confusion_matrix(y_test,y_pred)


sns.heatmap(cm, annot=True, linewidth=5, cbar=None)
plt.title('KNN Classifier confusion matrix')
plt.ylabel('True label')
plt.xlabel('predicted label')


# In[ ]:


print('accuracy of train dataset is',classifier1.score(x_train, y_train))
print('accuracy of test dataset is',classifier1.score(x_test, y_test))


# In[ ]:


#classification report for the test set
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


# 2. SVM with rbf (radial basis function) kernel

# In[ ]:


from sklearn.svm import SVC 
classifier2 = SVC(kernel = 'rbf', random_state = 0)
classifier2.fit(x_train, y_train)
#Predicting the Test set results 
y_pred = classifier2.predict(x_test)
#Making the confusion matrix 
#from sklearn.metrics import confusion_matrix 
cm = confusion_matrix(y_test,y_pred)



sns.heatmap(cm, annot=True, linewidth=5, cbar=None)
plt.title('SVM with rbf kernel Classifier confusion matrix')
plt.ylabel('True label')
plt.xlabel('predicted label')


# In[ ]:


print('accuracy of train dataset is',classifier3.score(x_train, y_train))
print('accuracy of test dataset is',classifier3.score(x_test, y_test))


# In[ ]:


#classification report for the test set
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
classifier3 = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier3.fit(x_train, y_train)
#Predicting the Test set results 
y_pred = classifier3.predict(x_test)
#Making the confusion matrix 
#from sklearn.metrics import confusion_matrix 
cm = confusion_matrix(y_test,y_pred)

sns.heatmap(cm, annot=True, linewidth=5, cbar=None)
plt.title('Decision Tree Classifier confusion matrix')
plt.ylabel('True label')
plt.xlabel('predicted label')


# In[ ]:


print('accuracy of train dataset is',classifier3.score(x_train, y_train))
print('accuracy of test dataset is',classifier3.score(x_test, y_test))


# In[ ]:


#classification report for the test set
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


# In[ ]:


from sklearn.ensemble import RandomForestClassifier 

classifier4 = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier4.fit(x_train,y_train)
#Predicting the Test set results 
y_pred = classifier4.predict(x_test)
#Making the confusion matrix 
#from sklearn.metrics import confusion_matrix 
cm = confusion_matrix(y_test,y_pred)

sns.heatmap(cm, annot=True, linewidth=5, cbar=None)
plt.title('RF with with entropy impurity Classifier confusion matrix')
plt.ylabel('True label')
plt.xlabel('predicted label')


# In[ ]:


print('accuracy of train dataset is',classifier4.score(x_train, y_train))
print('accuracy of test dataset is',classifier4.score(x_test, y_test))

