#!/usr/bin/env python
# coding: utf-8

# In[ ]:


############## DIABETIES DATASET #################


# In[2]:


#####importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

import statsmodels.formula.api as smf
from scipy.stats import shapiro,levene


# ## DIABETIES DATASET

# In[3]:


########## importing the data ########################
data=pd.read_csv('../input/diabetes.csv')
#checking the head of the data
data.head()


# In[ ]:


#describing the data
data.describe()


# In[ ]:


#getting the information regarding the data
data.info()


# In[ ]:


#checking the shape of the data
data.shape


# ## EDA

# In[ ]:


#checking for null values in the data and performing EDA
data.isnull().sum()


# In[ ]:


#getting the individua count of the outcome yes or no in the dataset
data['Outcome'].value_counts()


# In[ ]:


#dropping the outcome in the x and considering it in y as y is the target variable
x=data.drop('Outcome',axis=1)
x.head()
y=data['Outcome']
y.head()


# ## PLOTS

# In[ ]:


#pairplot to check the distribution of the data
sns.pairplot(data=data,hue='Outcome',diag_kind='kde')
plt.show()


# In[ ]:


#### plotting a HISTOGRAM on the data
data.hist(figsize=(10,8))
plt.show()


# In[ ]:


#### BOXPLOT for checking the outliers
data.plot(kind= 'box' , subplots=True,layout=(3,3), sharex=False, sharey=False, figsize=(10,8))


# In[ ]:


#plotting the outcome yes or no for the data
sns.countplot(data['Outcome'])


# In[ ]:


#### checking the correlation in matrix for variables using HEATMAP
import seaborn as sns
sns.heatmap(data.corr(), annot = True)


# ## SPLITTING THE DATA

# In[ ]:


X=data.iloc[:,:-1]
X.head()
Y=data.iloc[:,-1]
Y.head()


# In[ ]:


#### splitting X and y into training and testing sets 
from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.28, random_state=100)


# ## DATA SCALING

# In[ ]:


# Scaling the data
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# ## BUILDING A LOGISTIC REGRESSION  MODEL

# In[ ]:


#logistic regression model
model=LogisticRegression()
model.fit(X_train,y_train)
ypred=model.predict(X_test)
ypred


# ## CHECKING FOR THE ACCURACY WITH THE METRICS

# In[ ]:


# accuracy score
from sklearn import metrics
accuracy=metrics.accuracy_score(y_test,ypred)
print(accuracy)


# In[ ]:


#confusion matrix
cm=metrics.confusion_matrix(y_test,ypred)
print(cm)
plt.imshow(cm, cmap='binary')


# In[ ]:


#sensitivity and specificity check
tpr=cm[1,1]/cm[1,:].sum()
print(tpr*100)
tnr=cm[0,0]/cm[0,:].sum()
print(tnr*100)


# In[ ]:


#checking roc and auc curves
from sklearn.metrics import roc_curve,auc
fpr,tpr,_=roc_curve(y_test,ypred)
roc_auc=auc(fpr,tpr)
print(roc_auc)
plt.figure()
plt.plot(fpr,tpr)
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.show()


# ## BUILDING A DECISION TREE CLASSIFIER

# In[ ]:


#### importing the classifier and building the model
from sklearn import tree

model = tree.DecisionTreeClassifier()


# In[ ]:


model.fit(X_train, y_train)


# ## ACCURACY SCORE USING GINI INDEX

# In[ ]:


from sklearn.metrics import accuracy_score,f1_score,recall_score,precision_score,confusion_matrix
print("Accuracy:",accuracy_score(y_test, ypred))
print("Recall:",recall_score(y_test, ypred, average="weighted"))
print("Precision",precision_score(y_test, ypred, average="weighted"))
print("F1 Score:",f1_score(y_test, ypred, average="weighted"))
print(metrics.classification_report(y_test,ypred))


# In[ ]:



dot_data = tree.export_graphviz(model,
                                feature_names=X.columns,
                                out_file='tree1.dot',
                                filled=True,
                                rounded=True)

get_ipython().system('dot -Tpng tree1.dot > tree1.png')

from IPython.display import Image
Image(filename='tree1.png')


# ## ACCURACY SCORE USING ENTROPY

# In[ ]:


model1 = tree.DecisionTreeClassifier(criterion='entropy')
model1.fit(X_train, y_train)
preds= model1.predict(X_test)
print(accuracy_score(y_test, ypred))
print(recall_score(y_test, ypred, average="weighted"))
print(precision_score(y_test, ypred, average="weighted"))
print(f1_score(y_test, ypred, average="weighted"))
print(metrics.classification_report(y_test,ypred))

dot_data = tree.export_graphviz(model1,
                                feature_names=X.columns,
                                out_file='tree1.dot',
                                filled=True,
                                rounded=True)

get_ipython().system('dot -Tpng tree1.dot > tree1.png')

from IPython.display import Image
Image(filename='tree1.png')


# ## BUILDING A RANDOM FOREST CLASSIFIER

# In[ ]:


#importing the random forest classifier
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(criterion = 'gini',
                               n_estimators = 25,
                               random_state = 1)


# In[ ]:


# fitting the model and checking the accuracy score
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
from sklearn.metrics import accuracy_score
print (accuracy_score(y_test, y_predict))


# In[ ]:


#checking for top 3 variables in the given dataset
Importance = pd.DataFrame({'Importance':model.feature_importances_*100}, index=X_train.columns)
Importance.sort_values('Importance', axis=0, ascending=True).plot(kind='barh', color='r', )
plt.xlabel('Variable Importance')
plt.gca().legend_ = None


# ## BUILDING A RANDOM FOREST CLASSIFIER WITH TOP 3 VARIABLES

# In[ ]:


X = data[['Glucose', 'BMI', 'Age']]
y = data['Outcome']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(criterion = 'gini',
                               n_estimators = 25,
                               random_state = 1)

model.fit(X_train, y_train)
y_predict = model.predict(X_test)

from sklearn.metrics import accuracy_score

print (accuracy_score(y_test, y_predict))


# ## BUILDING A K-NEAREST NEIGHBOURS CLASSIFIER

# In[ ]:


# KNN
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 5)

x,y = data.drop('Outcome', axis = 1), data['Outcome']
# x,y = data.loc[:,data.columns != 'class'], data.loc[:,'class']

knn.fit(x,y)
prediction = knn.predict(x)
print('Prediction: {}'.format(prediction))


# In[ ]:


# train test split
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.3,random_state = 1)


# In[ ]:


display (x_train[:5])
print ()
display (x_test[:5])


# In[ ]:


knn = KNeighborsClassifier(n_neighbors = 3)

# x,y = data.loc[:,data.columns != 'class'], data.loc[:,'class']

knn.fit(x_train,y_train)
prediction = knn.predict(x_test)
#print('Prediction: {}'.format(prediction))
print('With KNN (K=3) accuracy is: ',knn.score(x_test,y_test)) # accuracy


# In[ ]:


knn = KNeighborsClassifier(n_neighbors = 10, p = 12)
from sklearn.model_selection import cross_val_score
CVscore = cross_val_score(knn.fit(x, y),
                        x_train,y_train, cv = 10)
print(CVscore)
print(CVscore.mean())


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=12, p=6, metric='minkowski')
knn.fit(x_train, y_train)

print('The accuracy of the knn classifier is {:.2f} out of 1 on training data'.format(knn.score(x_train, y_train)))
print('The accuracy of the knn classifier is {:.2f} out of 1 on test data'.format(knn.score(x_test, y_test)))


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
neig = np.arange(1, 20)
train_score_knn=[]
test_score_knn=[]
for i in range(1,20):
    knn = KNeighborsClassifier(n_neighbors=12, p=i, metric='minkowski')
    knn.fit(x_train, y_train)
    train_score_knn.append(knn.score(x_train, y_train))
    test_score_knn.append(knn.score(x_test, y_test))
#     print('For k value=',i)
#     print('The accuracy of the knn classifier is {:.2f} out of 1 on training data'.format(knn.score(x_train, y_train)))
#     print('The accuracy of the knn classifier is {:.2f} out of 1 on test data'.format(knn.score(x_test, y_test)))
#     print()


# In[ ]:


# Plot
plt.figure(figsize=[13,4])
plt.plot(neig, train_score_knn, label = 'Training Score')
plt.plot(neig, test_score_knn, label = 'Testing Score')
plt.legend()
plt.title('Value V/s Score',fontsize=20)
plt.xlabel('Pregnancies',fontsize=20)
plt.ylabel('outcome',fontsize=20)
plt.xticks(neig)
plt.grid()
plt.show()
print("Best score is {} with K = {}".format(np.max(test_score_knn),1+test_score_knn.index(np.max(test_score_knn))))


# ## BUILDING A NAIVE BAYES CLASSIFIER

# In[ ]:


X=data.iloc[:,:-1].values
X
Y=data.iloc[:,-1].values
Y[:5]
# splitting X and y into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.28, random_state=100) 


# In[ ]:


#importing naive bayes classifier and building the model
from sklearn.naive_bayes import GaussianNB 
classifier = GaussianNB()
classifier.fit(X_train, y_train)


# In[ ]:


y_pred = classifier.predict(X_test)
y_pred


# ## EVALUATING THE MODEL USING METRICS

# In[ ]:


cm = confusion_matrix(y_test, y_pred)
cm

print(f1_score(y_test, y_pred))
print(accuracy_score(y_test, y_pred))
label = ["0","1"]
sns.heatmap(cm, annot=True, xticklabels=label, yticklabels=label)


# In[ ]:


print(metrics.classification_report(y_test,y_pred))


# ## K-FOLD VAIDATION

# In[ ]:


#importing k-fold
from sklearn.model_selection import KFold


# In[ ]:


#performing k-fold cross validation
kf=KFold(n_splits=5,shuffle=True,random_state=2)
acc=[]
au=[]
for train,test in kf.split(X,Y):
    M=LogisticRegression()
    M.fit(X_train,y_train)
    y_pred=M.predict(X_test)
    acc.append(metrics.accuracy_score(y_test,y_pred))
    fpr,tpr,_=roc_curve(y_test,y_pred)
    au.append(auc(fpr,tpr))
    
print("Cross-validated AUC Mean Score:%.2f%%" % np.mean(au))
print("Cross-validated AUC Var Score:%.5f%%" % np.var(au,ddof=1))


# In[ ]:




