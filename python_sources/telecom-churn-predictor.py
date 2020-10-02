#!/usr/bin/env python
# coding: utf-8

# ## Customer Churn Prediction

# In[ ]:


# This Notebook Contains Logistic Regression model which is my Highest solution for Competition
# You can see my other versions for more 4 model based prediction


# In[ ]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from sklearn import metrics


# In[ ]:


trainds = pd.read_csv("/kaggle/input/predict-the-churn-for-customer-dataset/Train File.csv")
testds = pd.read_csv("/kaggle/input/predict-the-churn-for-customer-dataset/Test File.csv")

trainds.head(3)


# In[ ]:


testds.head(3)


# In[ ]:


print('Train Dataset Infomarion')
print ("Rows     : " ,trainds.shape[0])
print ("Columns  : " ,trainds.shape[1])
print ("\nFeatures : \n" ,trainds.columns.tolist())
print ("\nMissing values :  ", trainds.isnull().sum().values.sum())
print ("\nUnique values :  \n",trainds.nunique())


# In[ ]:


plt.subplots(figsize=(10, 6))
plt.title('Cooralation Matrix', size=30)
sns.heatmap(trainds.corr(),annot=True,linewidths=0.5)


# #### Data Manipulation

# In[ ]:


trainds.loc[trainds['TotalCharges'].isnull()] #NUll values Present


# In[ ]:


trainds['TotalCharges'] = trainds['TotalCharges'].fillna(trainds['TotalCharges'].median()) #
#trainds = trainds[trainds["TotalCharges"].notnull()]


# In[ ]:


CustomerIDS = testds['customerID']
trainds.drop('customerID', axis=1,inplace =True)
testds.drop('customerID', axis=1,inplace =True)


# In[ ]:


trainds.columns


# In[ ]:


testds.describe()


# In[ ]:


testds['TotalCharges'] = testds['TotalCharges'].fillna(testds['TotalCharges'].median())


# In[ ]:


trainds["InternetService"]=trainds["InternetService"].astype('str')
testds["InternetService"]=testds["InternetService"].astype('str')


# In[ ]:


trainds["TotalCharges"] = trainds["TotalCharges"].astype(float)
trainds["MonthlyCharges"] = trainds["MonthlyCharges"].astype(float)

testds["TotalCharges"] = testds["TotalCharges"].astype(float)
testds["MonthlyCharges"] = testds["MonthlyCharges"].astype(float)


# In[ ]:


replace_cols = [ 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection','TechSupport','StreamingTV', 'StreamingMovies']
for i in replace_cols : 
    trainds[i]  = trainds[i].replace({'No internet service' : 'No'})
    testds[i]  = testds[i].replace({'No internet service' : 'No'})


# In[ ]:


replace_cols = ['MultipleLines']
for i in replace_cols : 
    trainds[i]  = trainds[i].replace({'No phone service' : 'No'})
    testds[i]  = testds[i].replace({'No phone service' : 'No'})


# #### Data Exploration code:

# In[ ]:


def customercountplot(x):
    z = "Customer Count wrt "+ x
    plt.title(z,size=20)
    sns.countplot(trainds[x])


# In[ ]:


def churnratio():
    import plotly.offline as py
    import plotly.graph_objs as go
    val = trainds["Churn"].value_counts().values.tolist()

    trace = go.Pie(labels = ["Not Churned","Churned"] ,
                   values = val ,
                   marker = dict(colors =  [ 'royalblue' ,'lime']), hole = .5)
    layout = go.Layout(dict(title = "Train Dataset Customers"))
    data = [trace]
    fig = go.Figure(data = data,layout = layout)
    py.iplot(fig)


# In[ ]:


def churnrate():
    features = ['PhoneService','MultipleLines','InternetService',
                'TechSupport','StreamingTV','StreamingMovies','Contract']
    for i, item in enumerate(features):
        if i < 3:
            fig1 = pd.crosstab(trainds[item],trainds.Churn,margins=True)
            fig1.drop('All',inplace=True)
            fig1.drop('All',axis=1, inplace=True)
            fig1.plot.bar()
            z= 'Customer Churned wrt ' + item
            plt.title(z,size=20)
        elif i >=3 and i < 6:
            fig1 = pd.crosstab(trainds[item],trainds.Churn,margins=True)
            fig1.drop('All',inplace=True)
            fig1.drop('All',axis=1, inplace=True)
            fig1.plot.bar()
            z= 'Customer Churned wrt ' + item
            plt.title(z,size=20)
        elif i < 9:
            fig1 = pd.crosstab(trainds[item],trainds.Churn,margins=True)
            fig1.drop('All',inplace=True)
            fig1.drop('All',axis=1, inplace=True)
            fig1.plot.bar()
            z= 'Customer Churned wrt ' + item
            plt.title(z,size=20)


# ## Data Exploration

# In[ ]:


churnratio()


# In[ ]:


customercountplot('Churn')


# In[ ]:


customercountplot('gender')


# In[ ]:


customercountplot('Contract')


# In[ ]:


customercountplot('Partner')


# In[ ]:


customercountplot('PhoneService')


# In[ ]:


customercountplot('MultipleLines')


# In[ ]:


customercountplot('StreamingTV')


# In[ ]:


tempdf = trainds.copy()
bins=[0,12,24,48,60,100]
tempdf['tenure_group']=pd.cut(tempdf['tenure'],bins,labels=['0-12','12-24','24-48','48-60','>60'])
plt.title('Customer Count wrt to tenure',size=20)
sns.countplot(tempdf['tenure_group'])


# In[ ]:


plt.title("Distribution Plot For Montly Charges",size=20)
sns.distplot(trainds['MonthlyCharges'],hist_kws={'edgecolor':'black','alpha':.5})


# In[ ]:


plt.title("Distribution Plot For TotalCharges",size=20)
sns.distplot(trainds['TotalCharges'],hist_kws={'edgecolor':'black','alpha':.5})


# In[ ]:


churnrate()


# ## Data PreProcessing

# In[ ]:


train = trainds.copy()
test = testds.copy()
train


# In[ ]:


train.columns


# In[ ]:


train = pd.get_dummies(train, columns=['gender', 'SeniorCitizen', 'Partner', 'Dependents',
                                       'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
                                       'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
                                       'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod'])


# In[ ]:


test = pd.get_dummies(test, columns=['gender', 'SeniorCitizen', 'Partner', 'Dependents',
                                       'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
                                       'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
                                       'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod'])


# In[ ]:


train.head(3)


# In[ ]:


train["Churn"] = train["Churn"].replace({'Yes':1,'No':0})


# In[ ]:


# For writing solution to file
def writetofile(solution,filename):
    with open(filename,'w') as file:
        file.write('customerID,Churn\n')
        for (a, b) in zip(CustomerIDS, solution):
            c=""
            if b==0:
                c="No"
            else:
                c='Yes'
            file.write(str(a)+','+str(c)+'\n')


# In[ ]:


X = train.drop('Churn', axis=1)
y = train['Churn']


# # Building model

# ## Logistic Regression Model

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
from sklearn.metrics import f1_score


# In[ ]:


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=42)


# In[ ]:


logreg = LogisticRegression()
logreg.fit(X_train,y_train)


# In[ ]:


y_pred=logreg.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))


# In[ ]:


sol2=logreg.predict(test)
sol2


# In[ ]:


print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))


# In[ ]:


import collections, numpy
collections.Counter(sol2)


# In[ ]:


pds = pd.DataFrame(columns=['CustomerID','Churn'])
pds['CustomerID'] = CustomerIDS
pds['Churn']=sol2
pds


# ## Writing Predicted Data to Solution.csv

# In[ ]:


#writetofile(Prediction ,'filename you want to save')
writetofile(sol2,'Prediction-Solution')


# ##### The Best accuracy Model was Logistic Regression Model .
# ##### You can see other Models I Tried in other Versions.
