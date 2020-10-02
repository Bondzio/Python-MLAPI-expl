#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import os
print(os.listdir("../input"))


# In[ ]:


data= pd.read_csv("/kaggle/input/titanic/train.csv")
data.head()


# In[ ]:


data.info()


# # **check for missing values**

# In[ ]:


data.isna().sum()
#we have missing values 


# # **Handling the missing values**

# In[ ]:


#replacing missing datas with mean
from sklearn.impute import SimpleImputer 
imputer = SimpleImputer(missing_values=np.nan, 
                  strategy="mean") 
imputer = imputer.fit(data.iloc[:,5:7]) 
data.iloc[:,5:7] = imputer.transform(data.iloc[:,5:7])
data.head()


# In[ ]:


#let's check
data.isna().sum()
# so there are no missing values now
#there are still some missing values in cabin column but cabin might not have have that effect on survival


# #  **Look for some insights**

# In[ ]:


sns.scatterplot(data["Fare"],data["Age"],color='Green')


# In[ ]:


sns.factorplot(x="Sex",col="Survived", data=data , kind="count",size=7, aspect=.7,palette=['red','green'])


# **here we can conclude the girls survived more **

# In[ ]:


sns.catplot(x="Survived", hue="SibSp", col = 'Sex',kind="count", data=data,height=7);
sns.catplot(x="Survived", hue="Parch", col = 'Sex', kind="count", data=data,height=7);


# **Now, this gives a very good insight about family and gender relations. Female passengers were helped by there family males so they have higher survival rate in case if there family is onboard. But it was just the opposite for males as they were not prefered and thus most of them died saving there families**

# In[ ]:


surv =data.groupby('Survived').size() #this gives us total passengers survived and died
fig = plt.figure()
ax1 = fig.add_axes([0, 0, 1, 1], aspect=1)
ax1.pie(surv.values,labels=['Died','Survived'],startangle=90,autopct='%1.1f%%')
plt.title('Survivors to Casualties Ratio',bbox={'facecolor':'0.8', 'pad':5})
plt.show() 
    


# # Testing on different models

# **There are some categorical values we need to convert them into numerical values**

# In[ ]:


data["Sex"].replace(["male","female"],[0,1],inplace=True)
data["Embarked"].replace(["S","C","Q"],[0,1,2],inplace=True)
data.head()


# In[ ]:


data.isna().sum() #this says that there are still null values ... we had previously handled missing values but there are still null values left...


# In[ ]:


#Checking null values and fill 0 at the place of NaN.
data.isnull().sum()

data.fillna(0,inplace=True)
data.isna().sum()


# In[ ]:


data.drop(['PassengerId','Name','Ticket','Cabin'], axis=1, inplace=True)
#these are unnecessary columns
data.head()


# **since there are so many ages and fares we convert them into several groups**

# In[ ]:


data['Age Band']=0

data.loc[data['Age']<=16,'Age Band']=0
data.loc[(data['Age']>16)&(data['Age']<=32), 'Age Band']=1
data.loc[(data['Age']>32)&(data['Age']<=48),'Age Band']=2
data.loc[(data['Age']>48)&(data['Age']<=64),'Age Band']=3
data.loc[data['Age']>64,'Age Band']=4

data.head(10)


# In[ ]:


data['Age Band'].value_counts()


# In[ ]:


data["Fare Range"]= pd.qcut(data["Fare"],4)

data["Fare Range"].value_counts()


# In[ ]:


data["Fare_grp"]=0
data.loc[data["Fare"]<=7.91,"Fare_grp"]=0
data.loc[(data["Fare"]>7.91)&(data["Fare"]<=14.454),"Fare_grp"]=1
data.loc[(data['Fare']>14.454)&(data['Fare']<=31),'Fare_grp']=2
data.loc[(data['Fare']>31)&(data['Fare']<=513),'Fare_grp']=3
data.head()


# In[ ]:


data['Fare_grp'].value_counts()


# In[ ]:


data.drop(['Fare Range','Age'], axis=1, inplace=True)


# In[ ]:


#Splitting the dataset
X=data[data.columns[1:]]
Y=data['Survived']
print("y data=",Y.head())
print("---------------------------------------------------------------")
print("x data",X.head())


# In[ ]:


X.isna().sum()


# In[ ]:


#Importing ML libraries.
from sklearn.model_selection import train_test_split
from sklearn import metrics
X_train,X_test,Y_train,Y_test= train_test_split(X,Y,test_size=0.3, random_state=0)


# **LOGISTIC REGRESSION**

# In[ ]:



from sklearn.linear_model import LogisticRegression
logr= LogisticRegression()
logr.fit(X_train,Y_train)
Y_pred=logr.predict(X_test)
#MAKING CONFUSION MATRIX
from sklearn.metrics import confusion_matrix
cm = confusion_matrix( Y_pred ,Y_test )
score = metrics.accuracy_score(Y_pred,Y_test)
print("accuracy=",score)
print("Confusion matrix = ",cm)#(contain both correct and incorrect predictions)
#here correct predictions are 154+10 and incorrect ones are 14+90


#  **KNN**

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
model_knn= KNeighborsClassifier()
model_knn.fit(X_train,Y_train)
Y_knn=model_knn.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix( Y_knn,Y_test)
score = metrics.accuracy_score(Y_knn,Y_test)
print("accuracy=",score)
print("Confusion matrix = ",cm)


# **DECISION TREE CLASSIFIER**

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion='entropy' , random_state = 0)
classifier.fit(X_train,Y_train)
Y_dt = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test , Y_dt)
score = metrics.accuracy_score(Y_dt,Y_test)
print("accuracy=",score)
print("Confusion matrix = ",cm)


# **RANDOM FOREST CLASSIFIER**

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10 , criterion = 'entropy' , random_state=0) 
classifier.fit(X_train,Y_train)
Y_rf = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test , Y_rf)
score = metrics.accuracy_score(Y_rf,Y_test)
print("accuracy=",score)
print("Confusion matrix = ",cm)


# **WE CAN CONCLUDE THAT RANDOM FOREST HAS HIGHEST ACCURACY**

# ## SUBMISSION FOR KAGGLE COMPETETION

# **repeating same steps for test**

# In[ ]:


data_train= pd.read_csv("/kaggle/input/titanic/train.csv")
test_sur = pd.read_csv("/kaggle/input/titanic/gender_submission.csv")
data_test = pd.read_csv("/kaggle/input/titanic/test.csv")


# In[ ]:


data_train.drop(['Name','Ticket','Cabin'], axis=1, inplace=True)
data_test.drop(['Name','Ticket','Cabin'], axis=1, inplace=True)


# In[ ]:


#categorical to numerical values
data_train["Sex"].replace(["male","female"],[0,1],inplace=True)
data_train["Embarked"].replace(["S","C","Q"],[0,1,2],inplace=True)
data_test["Sex"].replace(["male","female"],[0,1],inplace=True)
data_test["Embarked"].replace(["S","C","Q"],[0,1,2],inplace=True)


# In[ ]:


#replacing missing datas with mean
from sklearn.impute import SimpleImputer 
imputer = SimpleImputer(missing_values=np.nan, 
                  strategy="mean") 
imputer = imputer.fit(data_train.iloc[:,5:7]) 
data_train.iloc[:,5:7] = imputer.transform(data_train.iloc[:,5:7])
print(data_train.head())
print("-------------------------------------------------------------------------------------")
from sklearn.impute import SimpleImputer 
imputer = SimpleImputer(missing_values=np.nan, 
                  strategy="mean") 
imputer = imputer.fit(data_test.iloc[:,5:7]) 
data_test.iloc[:,5:7] = imputer.transform(data_test.iloc[:,5:7])
print(data_test.head())


# **Comparision of both datas after preprocessing**

# In[ ]:


#Checking null values and fill 0 at the place of NaN.
data_train.isnull().sum()

data_train.fillna(0,inplace=True)
print("TRAINING DATA")
print(data_train.isna().sum())
print("----------------------------------------------------------")
data_test.isnull().sum()

data_test.fillna(0,inplace=True)
print("TEST DATA")
print(data_test.isna().sum())


# **we found that RANDOM FOREST has best accuracy.. now predicting score w.r.f test dataset**

# In[ ]:


#Splitting the dataset
X= data_train.drop(['Survived'], axis=1)
#X=data_train[data_train.columns[2:]]
Y=data_train['Survived']
X.head()


# In[ ]:


#Importing ML libraries.
from sklearn.model_selection import train_test_split
from sklearn import metrics
X_train,X_test,Y_train,Y_test= train_test_split(X,Y,test_size=0.3, random_state=0)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10 , criterion = 'entropy' , random_state=0) 
classifier.fit(X_train,Y_train)
Y_rf = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test , Y_rf)
score = metrics.accuracy_score(Y_rf,Y_test)
print("accuracy=",score)
print("Confusion matrix = ",cm)


# ### TESTING ON TEST DATASET

# In[ ]:


final_prediction = classifier.predict(data_test)


# In[ ]:


output = pd.DataFrame({"PassengerId":data_test.PassengerId , "Survived" : final_prediction})
output.to_csv("../submission_"  + ".csv",index = False)


# In[ ]:




