#!/usr/bin/env python
# coding: utf-8

# This script is the second in my series of following Andrew Ng's ML course on [Coursera][1]. In my [previous kernel][2], I explored the SVM classification algorithm for detection of breast cancer. In this script I will use a logistic regression classifier to try and predict whether an athlete is a male or a female based on their height, weight and age.
# 
#  1. How accurately can we guess the sex based on these features with a simple logistic regression?
#  2. Linear vs polynomial model
#  3. Accuracy vs ROC as success metrics
# 
#   [1]: https://www.coursera.org/learn/machine-learning/home/welcome
#   [2]: https://www.kaggle.com/drgilermo/d/uciml/breast-cancer-wisconsin-data/exploration-of-svm

# Load Libraries:

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
from sklearn.decomposition import PCA


plt.style.use('fivethirtyeight')

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))


# Read the data, remove NaNs and add the Age feature based on the date of birth:

# In[ ]:


#Read The data
df = pd.read_csv('../input/athletes.csv')

#Add the Age feature
for i,row in enumerate(df.iterrows()):
    try:
        df.loc[i,'Age'] = 116 - float(row[1].dob[len(row[1].dob)-2:len(row[1].dob)])
    except TypeError:
        df.loc[i,'Age'] = 0
        
        
df['BMI'] = np.true_divide(df.weight,df.height*df.height)

#Get rid of NaNs
df = df[np.isnan(df.height) == 0]
df = df[np.isnan(df.weight) == 0]
df = df[np.isnan(df.Age) == 0]
df = df[df.Age<100]
df = df[np.isnan(df.BMI) == 0]


# Let's explore the correlations and see which features separate the females\males populations:

# In[ ]:


g = sns.PairGrid(df[['height','weight','Age','BMI','sex']],hue='sex')
g = g.map_diag(plt.hist)
g = g.map_offdiag(plt.scatter, s = 3, alpha = 0.2)


# Age and BMI aren't very good predictors, whereas weight and height, somewhat unsurprisingly, are.
# 
# Let's split the data into train and validation and start classifying:

# In[ ]:


X = df[['height','weight']]
y = np.zeros(len(df))
y[df.sex.values == 'female'] = 1
X['target'] = y


traindf, testdf = train_test_split(X, test_size = 0.2)


# First let's check the effect of the regularization:

# In[ ]:


trainning = []
validation = []
reg = np.linspace(0.1,10,100)
for C in reg:
    clf = LogisticRegression(penalty='l2',C= C )
    clf.fit(traindf.drop(['target'], axis = 1), traindf.target)
    trainning.append(clf.score(traindf.drop(['target'],axis = 1),traindf.target))
    validation.append(clf.score(testdf.drop(['target'],axis = 1),testdf.target))
    
plt.plot(reg,trainning)
plt.plot(reg,validation)
plt.legend(['Trainning','Validation'])
plt.xlabel('Regularization Strength (Inverse)')
plt.ylabel('Accuracy')


# We don't see a large effect in this scale. let's pick C = 2 and visualize the decision boundary produced by the classifier on the data:

# In[ ]:


clf = LogisticRegression(penalty='l2',C= 2 )
clf.fit(traindf.drop(['target'], axis = 1), traindf.target)

print('Training Accuracy.....',clf.score(traindf.drop(['target'],axis = 1),traindf.target))
prediction = clf.predict(testdf.drop(['target'], axis = 1))
print('Validation Accuracy....',clf.score(testdf.drop(['target'],axis = 1),testdf.target))
loss = prediction - testdf['target']
accuracy = 1 - np.true_divide(sum(np.abs(loss)),len(loss))

radius = np.linspace(min(X.height), max(X.height), 100)
line = (-clf.coef_[0][0]/clf.coef_[0][1])*radius + np.ones(len(radius))*(-clf.intercept_/clf.coef_[0][1])
plt.plot(radius,line)
      
plt.plot(X['height'][X.target == 0] + np.random.normal(0,0.01,len(X[X.target == 0])),X['weight'][X.target == 0],'o',color = 'b', alpha = 0.2, markersize = 5)
plt.plot(X['height'][X.target == 1] + np.random.normal(0,0.01,len(X[X.target == 1])),X['weight'][X.target == 1],'o',color = 'r', alpha = 0.2, markersize = 5)
plt.legend(['Decision Line','Male','Female'])
plt.title('Logistic Regression. Accuracy:' + str(accuracy)[0:4])
plt.xlabel('Height')
plt.ylabel('Weight')
plt.xlim([min(X.height),max(X.height)])
plt.ylim([min(X.weight),max(X.weight)])


# With these results as a benchmark, let's see if we can improve with by adding a polynomial component: height^2:

# In[ ]:


clf = LogisticRegression(penalty='l2',C= 0.1 )

traindf['height^2'] = traindf['height']*traindf['height']
testdf['height^2'] = testdf['height']*testdf['height']

clf.fit(traindf.drop(['target'], axis = 1), traindf.target)

print('Training Accuracy.....',clf.score(traindf.drop(['target'],axis = 1),traindf.target))
prediction = clf.predict(testdf.drop(['target'], axis = 1))
print('Validation Accuracy....',clf.score(testdf.drop(['target'],axis = 1),testdf.target))
loss = prediction - testdf['target']
accuracy = 1 - np.true_divide(sum(np.abs(loss)),len(loss))

radius = np.linspace(min(X.height), max(X.height), 100)
curve= (-clf.coef_[0][0]/clf.coef_[0][1])*radius +(-clf.coef_[0][2]/clf.coef_[0][1])*radius**2 + np.ones(len(radius))*(-clf.intercept_/clf.coef_[0][1])
plt.plot(radius,curve)
      
plt.plot(X['height'][X.target == 0] + np.random.normal(0,0.01,len(X[X.target == 0])),X['weight'][X.target == 0],'o',color = 'b', alpha = 0.2, markersize = 5)
plt.plot(X['height'][X.target == 1] + np.random.normal(0,0.01,len(X[X.target == 1])),X['weight'][X.target == 1],'o',color = 'r', alpha = 0.2, markersize = 5)
plt.legend(['Decision Line','Male','Female'])
plt.title('Logistic Regression. Accuracy:' + str(accuracy)[0:4])
plt.xlabel('Height')
plt.ylabel('Weight')
plt.xlim([min(X.height),max(X.height)])
plt.ylim([min(X.weight),max(X.weight)])



# The accuracy does not improve. Maybe if we add in the other continuous features - Age, and the engineered BMI (which is simply a kind of a polynomial feature):

# In[ ]:


X = df[['height','weight','Age','BMI']]
y = np.zeros(len(df))
y[df.sex.values == 'female'] = 1
X['target'] = y


traindf, testdf = train_test_split(X, test_size = 0.2)

clf = LogisticRegression(penalty='l2',C= 2 )
clf.fit(traindf.drop(['target'], axis = 1), traindf.target)

print('Training Accuracy.....',clf.score(traindf.drop(['target'],axis = 1),traindf.target))
prediction = clf.predict(testdf.drop(['target'], axis = 1))
print('Validation Accuracy....',clf.score(testdf.drop(['target'],axis = 1),testdf.target))


# Let's try a different approach to assessing the classifier performance. the ROC (and the area under the curve) instead of accuracy:

# In[ ]:


X = df[['height','weight','Age','BMI']]
y = np.zeros(len(df))
y[df.sex.values == 'female'] = 1
X['target'] = y

traindf, testdf = train_test_split(X, test_size = 0.2)

probas_1 = clf.fit(traindf.drop(['target'], axis = 1), traindf.target).predict_proba(testdf.drop(['target'],axis = 1))
probas_2 = clf.fit(traindf.drop(['target','Age','BMI'], axis = 1), traindf.target).predict_proba(testdf.drop(['target','Age','BMI'],axis = 1))

traindf['height^2'] = traindf['height']*traindf['height']
testdf['height^2'] = testdf['height']*testdf['height']
probas_3 = clf.fit(traindf.drop(['target','Age','BMI'], axis = 1), traindf.target).predict_proba(testdf.drop(['target','Age','BMI'],axis = 1))


fpr, tpr, thresholds = roc_curve(testdf['target'], probas_1[:, 1])
plt.plot(fpr, tpr, linewidth = 1)
fpr, tpr, thresholds = roc_curve(testdf['target'], probas_2[:, 1])
plt.plot(fpr, tpr, linewidth = 2)
fpr, tpr, thresholds = roc_curve(testdf['target'], probas_3[:, 1])
plt.plot(fpr, tpr, linewidth = 1)
plt.plot([0,1],[0,1], linewidth = 1)

plt.legend(['Linear - 4 features','Linear - 2 features','Deg 2 Polynomial - 2 features','Random Guess'])
plt.title('ROC Curve for different classifiers')


# MMM. not really. Adding polynomial or additional features doesn't outperform the linear approach with only the height and weight, both when using the accuracy or the AUC (which was not calculated but can be qualitatively deduced from the graph) as metrics.
# 
# 
