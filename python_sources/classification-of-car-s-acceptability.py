#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Importing the basic libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.offline as py
from plotly import tools
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


#Reading the dataset 
cars = pd.read_csv('/kaggle/input/car-evaluation-data-set/car_evaluation.csv')
cars.shape


# In[ ]:


#Since our dataset doesn't contain the name of columns, the column names were assigned 
cars.columns = ['Buying', 'Maint', 'Doors','Persons','LugBoot','Safety','Evaluation']


# In[ ]:


#Taking an overview of data
cars.sample(10)


# In[ ]:


a_df=[]
for i in cars.values:
    if i[6] == 'acc':
        a_df.append(i)


# In[ ]:


df=pd.DataFrame(a_df)


# In[ ]:


df.sample(10)


# In[ ]:


#Let's check if there are any missing values in our dataset 
cars.isnull().sum()


# In[ ]:


#We see that there are no missing values in our dataset 
#Let's take a more analytical look at our dataset 
cars.describe()


# In[ ]:


#We realize that our data has categorical values 
cars.columns


# In[ ]:


#Lets find out the number of cars in each evaluation category
cars['Evaluation'].value_counts().sort_index()


# In[ ]:


fig = {
  "data": [
    {
      "values": [1210,384,69,65],
      "labels": [
        "Unacceptable",
        "Acceptable",
        "Good",
        "Very Good"
      ],
      "domain": {"column": 0},
      "name": "Car Evaluation",
      "hoverinfo":"label+percent+name",
      "hole": .6,
      "type": "pie"
    }],
  "layout": {
        "title":"Distribution of Evaluated Cars",
        "grid": {"rows": 1, "columns": 1},
        "annotations": [
            {
                "font": {
                    "size": 36
                },
                "showarrow": False,
                "text": "",
                "x": 0.5,
                "y": 0.5
            }
        ]
    }
}
py.iplot(fig, filename='cars_donut')


# In[ ]:


#cars.Evaluation.replace(('unacc', 'acc', 'good', 'vgood'), (0, 1, 2, 3), inplace = True)
#cars.Buying.replace(('vhigh', 'high', 'med', 'low'), (3, 2, 1, 0), inplace = True)
#cars.Maint.replace(('vhigh', 'high', 'med', 'low'), (3, 2, 1, 0), inplace = True)
#cars.Doors.replace(('5more'),(5),inplace=True)
#cars.Persons.replace(('more'),(5),inplace=True)
#cars.LugBoot.replace(('small','med','big'),(0,1,2),inplace=True)
#cars.Safety.replace(('low','med','high'),(0,1,2),inplace=True)


# In[ ]:


cars.Doors.replace(('5more'),('5'),inplace=True)
cars.Persons.replace(('more'),('5'),inplace=True)


# In[ ]:


features = cars.iloc[:,:-1]
features[:5]
a=[]
for i in features:
    a.append(features[i].value_counts())


# In[ ]:


buy = pd.crosstab(cars['Buying'], cars['Evaluation'])
mc = pd.crosstab(cars['Maint'], cars['Evaluation'])
drs = pd.crosstab(cars['Doors'], cars['Evaluation'])
prsn = pd.crosstab(cars['Persons'], cars['Evaluation'])
lb = pd.crosstab(cars['LugBoot'], cars['Evaluation'])
sfty = pd.crosstab(cars['Safety'], cars['Evaluation'])


# In[ ]:


buy


# In[ ]:


data = [
    go.Bar(
        x=a[0].index, # assign x as the dataframe column 'x'
        y=buy['unacc'],
        name='Unacceptable'
    ),
    go.Bar(
        x=a[0].index,
        y=buy['acc'],
        name='Acceptable'
    ),
    go.Bar(
        x=a[0].index,
        y=buy['good'],
        name='Good'
    ),
    go.Bar(
        x=a[0].index,
        y=buy['vgood'],
        name='Very Good'
    )

]

layout = go.Layout(
    barmode='stack',
    title='Selling Price vs Evaluation'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='distri')


# In[ ]:


data = [
    go.Bar(
        x=a[0].index, # assign x as the dataframe column 'x'
        y=mc['unacc'],
        name='Unacceptable'
    ),
    go.Bar(
        x=a[0].index,
        y=mc['acc'],
        name='Acceptable'
    ),
    go.Bar(
        x=a[0].index,
        y=mc['good'],
        name='Good'
    ),
    go.Bar(
        x=a[0].index,
        y=mc['vgood'],
        name='Very Good'
    )

]

layout = go.Layout(
    barmode='stack',
    title='Maintainance cost vs Evaluation'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='cars_donut')


# In[ ]:


data = [
    go.Bar(
        x=a[2].index, # assign x as the dataframe column 'x'
        y=drs['unacc'],
        name='Unacceptable'
    ),
    go.Bar(
        x=a[2].index,
        y=drs['acc'],
        name='Acceptable'
    ),
    go.Bar(
        x=a[2].index,
        y=drs['good'],
        name='Good'
    ),
    go.Bar(
        x=a[2].index,
        y=drs['vgood'],
        name='Very Good'
    )

]

layout = go.Layout(
    barmode='stack',
    title='Doors vs Evaluation'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='cars_donut')


# In[ ]:


data = [
    go.Bar(
        x=a[3].index, # assign x as the dataframe column 'x'
        y=prsn['unacc'],
        name='Unacceptable'
    ),
    go.Bar(
        x=a[3].index,
        y=prsn['acc'],
        name='Acceptable'
    ),
    go.Bar(
        x=a[3].index,
        y=prsn['good'],
        name='Good'
    ),
    go.Bar(
        x=a[3].index,
        y=prsn['vgood'],
        name='Very Good'
    )

]

layout = go.Layout(
    barmode='stack',
    title='Number of Passengers vs Evaluation'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='cars_donut')


# In[ ]:


data = [
    go.Bar(
        x=a[4].index, # assign x as the dataframe column 'x'
        y=lb['unacc'],
        name='Unacceptable'
    ),
    go.Bar(
        x=a[4].index,
        y=lb['acc'],
        name='Acceptable'
    ),
    go.Bar(
        x=a[4].index,
        y=lb['good'],
        name='Good'
    ),
    go.Bar(
        x=a[4].index,
        y=lb['vgood'],
        name='Very Good'
    )

]

layout = go.Layout(
    barmode='stack',
    title='Luggage Boot vs Evaluation'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='cars_donut')


# In[ ]:


data = [
    go.Bar(
        x=a[5].index, # assign x as the dataframe column 'x'
        y=sfty['unacc'],
        name='Unacceptable'
    ),
    go.Bar(
        x=a[5].index,
        y=sfty['acc'],
        name='Acceptable'
    ),
    go.Bar(
        x=a[5].index,
        y=sfty['good'],
        name='Good'
    ),
    go.Bar(
        x=a[5].index,
        y=sfty['vgood'],
        name='Very Good'
    )

]

layout = go.Layout(
    barmode='stack',
    title='Safety vs Evaluation'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='cars_donut')


# In[ ]:


#We need to encode the categorical data 
#We have two options, either we use label encoder or one hot encoder 
#We use label encoder when our target variable changes with increase or decrease in that feature variable 
#We use One hot encoder when a target variable depends upon the feature variable 


# In[ ]:


#Dividing the dataframe into x features and y target variable
x = cars.iloc[:, :-1]
y = cars.iloc[:, 6]


# In[ ]:


x.columns = ['Buying', 'Maint', 'Doors','Persons','LugBoot','Safety']
y.columns=['Evaluation']


# In[ ]:


x.head()


# In[ ]:


#Using pandas dummies function to encode the data into categorical data
x = pd.get_dummies(x, prefix_sep='_', drop_first=True)


# In[ ]:


x.sample(5)


# In[ ]:


y.describe()


# In[ ]:


x=x.values
y=y.values


# In[ ]:


#And the rest of them to be categorically encoded: ['Buying', 'Maint', 'Doors', 'Persons','Safety','Evaluation']


# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)


# In[ ]:


"""from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)"""


# In[ ]:


x_train[:5]


# In[ ]:


y_train[:5]


# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix


# In[ ]:


#Using ogistic regression
clf = LogisticRegression(random_state = 0)
clf.fit(x_train, y_train)


# In[ ]:


y_pred = clf.predict(x_test)
f1_LR=f1_score(y_test,y_pred, average='macro')
print("Training Accuracy: ",clf.score(x_train, y_train))
print("Testing Accuracy: ", clf.score(x_test, y_test))
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test,y_pred)) 


# In[ ]:


#Using KNN classifier
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
clf.fit(x_train, y_train)


# In[ ]:


y_pred = clf.predict(x_test)
f1_KNN=f1_score(y_test,y_pred, average='macro')
print("Training Accuracy: ",clf.score(x_train, y_train))
print("Testing Accuracy: ", clf.score(x_test, y_test))
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test,y_pred))


# In[ ]:


#Using Linear SVC
from sklearn.svm import SVC
clf = SVC(kernel = 'linear', random_state = 0)
clf.fit(x_train, y_train)


# In[ ]:


y_pred = clf.predict(x_test)
f1_SVC_Linear=f1_score(y_test,y_pred, average='macro')
print("Training Accuracy: ",clf.score(x_train, y_train))
print("Testing Accuracy: ", clf.score(x_test, y_test))
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test,y_pred))


# In[ ]:


#Using rbf SVC
from sklearn.svm import SVC
clf = SVC(kernel = 'rbf', random_state = 0)
clf.fit(x_train, y_train)


# In[ ]:


y_pred = clf.predict(x_test)
f1_SVC_rbf=f1_score(y_test,y_pred, average='macro')
print("Training Accuracy: ",clf.score(x_train, y_train))
print("Testing Accuracy: ", clf.score(x_test, y_test))
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test,y_pred))


# In[ ]:


#Using NB classifier
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(x_train, y_train)


# In[ ]:


#GaussianNB?


# In[ ]:


y_pred = clf.predict(x_test)
print("Training Accuracy: ",clf.score(x_train, y_train))
print("Testing Accuracy: ", clf.score(x_test, y_test))
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test,y_pred))


# Note that this is WRONG implementation of Naive Bayes classifier. Since the Independence assumption of NB classifier states that the features shoud not be correlated to each other; so when creating the dummy variables, we make family of dependent features and hence we get such a terrible accuracy. So after trying out a couple more algorithms, I've done this one properly :)

# In[ ]:


#Trying decision tree classifier
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
clf.fit(x_train, y_train)


# In[ ]:


y_pred = clf.predict(x_test)
f1_DT=f1_score(y_test,y_pred, average='macro')
print("Training Accuracy: ",clf.score(x_train, y_train))
print("Testing Accuracy: ", clf.score(x_test, y_test))
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test,y_pred))


# In[ ]:


#Trying Random forest classifier
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators = 25, criterion = 'entropy', random_state = 0)
clf.fit(x_train, y_train)


# In[ ]:


y_pred = clf.predict(x_test)
f1_RF=f1_score(y_test,y_pred, average='macro')
print("Training Accuracy: ",clf.score(x_train, y_train))
print("Testing Accuracy: ", clf.score(x_test, y_test))
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test,y_pred))


# In[ ]:


#Now trying the NB classifier again, this time without dummy variables 
x_new = cars.iloc[:,:-1]


# In[ ]:


from sklearn.preprocessing import LabelEncoder


# In[ ]:


lae = LabelEncoder()
x_new=x_new.apply(lambda col: lae.fit_transform(col))
x_new.head()


# In[ ]:


x_new=x_new.values


# In[ ]:


x_train_new, x_test_new= train_test_split(x_new, test_size = 0.25, random_state = 0)


# In[ ]:


clf_new = GaussianNB(priors=None)
clf_new.fit(x_train_new, y_train)


# In[ ]:


y_train[:10]


# In[ ]:


y_pred = clf_new.predict(x_test_new)
f1_NB=f1_score(y_test,y_pred, average='macro')
print("Training Accuracy: ",clf_new.score(x_train_new, y_train))
print("Testing Accuracy: ", clf_new.score(x_test_new, y_test))
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test,y_pred))


# In[ ]:


models=['Linear SVC', 'Kernel SVC','Logistic Regression','Decision Tree Classifier','Random Forest Classifier','Naive Bayes Classifier' ]
fig = go.Figure(data=[
    go.Bar(name='f1_score', x=models, y=[f1_SVC_Linear,f1_SVC_rbf,f1_LR,f1_DT,f1_RF,f1_NB])])
fig.show()


# The in depth analysis and dscription for the project can be found in the blogs :
# 
# [The Classifier Part 1](http://medium.com/@harjotspahwa/the-classifier-part-1-2-18f3c70d01fe)
# 
# [The Classifier Part 2](http://medium.com/@harjotspahwa/the-classifier-part-2-2-38df3de1f9b3)
