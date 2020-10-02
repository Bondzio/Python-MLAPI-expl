#!/usr/bin/env python
# coding: utf-8

# # 1. Importing Libraries

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # 2. Loading Dataset

# In[ ]:


df = pd.read_csv('../input/graduate-admissions/Admission_Predict.csv')


# In[ ]:


df.head()


#  ### 2.a Checking Columns And Removing Spaces

# In[ ]:


df.columns


# In[ ]:


df = df.rename(columns={'LOR ':'LOR','Chance of Admit ':'Chance of Admit'})


# In[ ]:


df.columns


# ### 2.b Checking For Null Values In Columns
# * No null values were found in columns

# In[ ]:


for col in df.columns:
    print(col+' has '+ str(df[col].isnull().sum()) + ' null values')


# ### 2.c understanding datatypes in dataframe

# In[ ]:


df.info()


# In[ ]:


df.describe()


# ## 3. Exploratory Data Analysis

# ### 3.a Checking for columns with categorical data and contineous data
# * Columns SOP,LOR,Research And University Rating have categorical data
# * Refrence Links
#     https://www.datacamp.com/community/tutorials/categorical-data
#     

# In[ ]:


for col in df.columns:
    print(col + ' ' + str(len(df[col].value_counts())))


# In[ ]:


df.info()


# checking distinct values in categorical features

# In[ ]:


catList = ['Research','SOP','LOR','University Rating']
for col in catList:
    print(df[col].unique())


# ### 3.b Checking Distribution Of Each Column

# In[ ]:


for col in df.columns:
    plt.figure()
    sns.distplot(df[col])


# ### 3.c Checking relation between target feature and each feature
# > no conclusion can be drawn from serial number <br>
# > chance of admit increases with increase in gre score <br>
# > chance of admit increases with increase in toefl score <br>
# > chance of admit increases with increase in university rating <br>
# > chance of admit increases with increase in SOP <br>
# > chance of admit increases with increase in LOR <br>
# > chance of admit increases with increase in CGPA <br>
# > chance of admit increases with increase in Research <br>

# In[ ]:


for col in df.columns:
    if col != 'Chance of Admit':
        plt.figure()
        sns.relplot(x=col,y='Chance of Admit',data=df)
        plt.ylabel('Chance of Admit')
        plt.xlabel(col)


# ### 3.d Plotting Categorical Distributions
# > Chance Of Admit is more with research <br>
# > Chance of Admit increases with SOP <br>
# > Chance Of Admit increases with LOR <br>
# > CHance of admit increases with University Rating <br>

# In[ ]:


for col in catList:
    plt.figure()
    sns.catplot(x=col,y='Chance of Admit',kind='bar',data=df)


# ### 3.e Checking Correlation Between Features
# > Serial No. has no relation to Chance Of Admit <br>
# > CGPA, GRE Score, TOEFL Score and University Rating are top 5 parameters <br>
# > Serial No. is not showing much correlation with any feature <br>
# > GRE Score score has strong coorelation with TOEFL Score and CGPA <br>
# > Research correlations are not very strong with any feature <br>

# In[ ]:


dfCorr = df.corr()
dfCorr['Chance of Admit'].sort_values(ascending=False)


# #### 3.e.1 correlational maps

# In[ ]:


plt.figure(figsize=(10,10))
sns.heatmap(dfCorr,annot=True,linewidths=.5,cmap="magma",fmt='.2f')


# ## 4.Feature Engineering

# ### 4.a Outlier detection

# In[ ]:


def detect_outliers(df,features):
    outlier_indices = []
    
    for col in features:
        #1st quartile
        Q1 = np.percentile(df[col],25)
        #3rd quartile
        Q3 = np.percentile(df[col],75)
        #Interquartile range
        IQR = Q3-Q1
        
        # outlier step
        outlier_step = 1.5 * IQR
        
        #list of indices of outliers
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | 
                             (df[col] > Q3 + outlier_step)].index
        
        outlier_indices.extend(outlier_list_col)
        
    return outlier_indices


# In[ ]:


outliers_to_drop = detect_outliers(df,df.columns)
outlierDf = df.loc[outliers_to_drop]


# In[ ]:


df = df.drop(outliers_to_drop,axis=0).reset_index(drop=True)


# In[ ]:


df.head()


# ### 4.c Feature Selection
# > from correlation analysis we can remove serial number column

# In[ ]:


df = df.drop(['Serial No.'], axis=1)


# In[ ]:


# Feature Importance
X = df.iloc[:,:7]
Y = df.iloc[:,-1]

from sklearn.ensemble import ExtraTreesRegressor
model = ExtraTreesRegressor()
model.fit(X,Y)
print(model.feature_importances_)
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.show()


# ### 4.b Encoding
# > since for research both 0 and 1 are at same level this needs one hot encoding

# In[ ]:


from sklearn.preprocessing import OneHotEncoder
# saving a copy
dfEnc = df.copy()


# In[ ]:


enc = OneHotEncoder(categorical_features=[6])
dfEnc = enc.fit_transform(dfEnc).toarray()


# In[ ]:


dfEnc.shape


# In[ ]:


dfEnc = pd.DataFrame(dfEnc)


# In[ ]:


dfEnc.head()


# In[ ]:


df.head()
df.rename(columns={})


# ## 5. Feature Scaling and Data Split

# In[ ]:


y = pd.DataFrame(dfEnc.iloc[:,-1])
x = dfEnc.iloc[:,0:8]


# ### 5.a) Splitting data

# In[ ]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)


# ### 5.b) Scaling Data

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


# ## 6 Regression Algorithms

# In[ ]:


from sklearn.linear_model import LinearRegression, Ridge,Lasso, ElasticNet 
from sklearn.linear_model import BayesianRidge
from sklearn.svm import SVR
from sklearn.linear_model import SGDRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
modelList = [LinearRegression, Ridge,Lasso, ElasticNet,BayesianRidge,
SVR,SGDRegressor,KNeighborsRegressor,GaussianProcessRegressor,RandomForestRegressor,
DecisionTreeRegressor]


# In[ ]:


RegModelScores = []
def predictFunc(model):
    model=model()
    model_name = model.__class__.__name__
    model.fit(x_train,y_train)
    model_score_test = model.score(x_test,y_test)
    model_score_train = model.score(x_train,y_train)
    model_pred = model.predict(x_test)
    
    plt.figure()
    sns.distplot(y_test,hist=False,color='blue')
    sns.distplot(model_pred,hist=False,color='red')
    plt.xlabel(model_name)
    RegModelScores.append([model_name,model_score_test,model_score_train])


# In[ ]:


for model in modelList:
    predictFunc(model)


# ### 6.a) Regression Algorithms Chart Representation
# > Linear Regression has highest Score

# In[ ]:


dfReg = pd.DataFrame(RegModelScores,columns=['model','train_score','test_score'])


# In[ ]:


dfReg


# ### 6.b) Regression Algorithms Visual Representation

# In[ ]:


fig,ax = plt.subplots(figsize=(20,20))
p2 = sns.catplot(ax=ax,y='model',x='train_score',data=dfReg,kind='bar')
#p2.set_xticklabels(p2.get_xticklabels(),rotation=45)
plt.setp(ax.get_yticklabels(),fontsize=24)
plt.close(p2.fig)


# ## 7. Classification Algorithms
# > Random Forest CLassifier is the most suitable model to use

# ### 7.a) preparing target value (making it discrete from contineous)
# > We are assuming that if chance of admit is more that 0.8 student will get selected

# In[ ]:


y_train[8] = y_train[8].apply(lambda x:1 if x>0.8 else 0)
y_test[8] = y_test[8].apply(lambda x:1 if x>0.8 else 0)


# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import r2_score
from sklearn.metrics import precision_score,recall_score
from sklearn.metrics import f1_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score,StratifiedKFold, learning_curve


# In[ ]:


conMatList = []
prcList = []
clRep= []
rocDet = []
preScore = []
recScore = []
f1Score = []
yPred = []

def getClassModel(model):
    model = model()
    model_name = model.__class__.__name__
    model.fit(x_train,y_train)
    
    #getting prediction
    y_pred = model.predict(x_test)
    yPred.append([model_name,y_pred])
    
    # getting scores
    
    pre_score = precision_score(y_test,y_pred)
    rec_score= recall_score(y_test,y_pred)
    f1score = f1_score(y_test,y_pred)
    
    preScore.append([model_name,pre_score])
    recScore.append([model_name,rec_score])
    f1Score.append([model_name,f1score])
    
    ## getting confusion matrix
    cm = confusion_matrix(y_test,y_pred)
    matrix = pd.DataFrame(cm,columns=['predicted 0','predicted 1'],
                         index=['Actual 0','Actual 1'])
    conMatList.append([model_name,matrix])
    
     ## getting precision recall curve values
    
    precision, recall, thresholds = precision_recall_curve(y_test,y_pred)
    prcList.append([model_name,precision,recall,thresholds])
    
    ## roc details
    
    fpr,tpr,thresholds = roc_curve(y_test,y_pred)
    rocDet.append([model_name,fpr,tpr,thresholds])
    
    ## classification report
    
    classRep = classification_report(y_test,y_pred)
    clRep.append([model_name,classRep])


# In[ ]:


kfold = StratifiedKFold(n_splits=10)
classModelList = [LogisticRegression,SVC,GaussianNB,DecisionTreeClassifier
                 ,RandomForestClassifier,KNeighborsClassifier]

for model in classModelList:
    getClassModel(model)
    


# ## 7.b) Generating cross validation chart

# In[ ]:


#getting cross validation scores for each model
cv_results = []
for model in classModelList:
    cv_results.append(cross_val_score(model(),x_train,y_train,scoring='accuracy',
                                     cv=kfold,n_jobs=4))
cv_means = []
cv_std = []

for cv_result in cv_results:
    cv_means.append(cv_result.mean())
    cv_std.append(cv_result.std())
    
model_name = []
for model in classModelList:
    modelIns = model()
    model_name.append(modelIns.__class__.__name__)
    
cv_res = pd.DataFrame({
    "CrossValMeans":cv_means,
    "CrossValErrors":cv_std,
    "Model":model_name
})
  
cv_res


# ## 7.c) Generating prediction distribution chart

# In[ ]:


fig,ax = plt.subplots(figsize=(20,10))
p2 = sns.distplot(y_test,hist=False,label='test_set',ax=ax)
for pred in yPred:
    sns.distplot(pred[1],hist=False,label=pred[0],ax=ax)
plt.setp(ax.get_legend().get_texts(), fontsize='22') 
1==1
#plt.close()


# ## 7.d) Generating Confusion Matrix Chart

# In[ ]:


#conMatList,prcList ,clRep ,rocDet ,preScore ,recScore 
for mat in conMatList:
    print(mat[0])
    print(' ')
    print(mat[1])
    print('-----------------------------------------------')


# ## 7.e) Generating precision,f1 and recall score Chart

# In[ ]:


precisionDf = pd.DataFrame(preScore,columns=['model','precisionScore'])
recallDf = pd.DataFrame(recScore,columns=['model','recallScore'])
f1Df = pd.DataFrame(f1Score,columns=['model','f1Score'])
precisionDf['f1Score'] = f1Df['f1Score']
precisionDf['recallScore'] = recallDf['recallScore']
precisionDf


# ## 7.f) Generating ROC Curve

# In[ ]:


for roc in rocDet:
    print(roc[0])
    fpr = roc[1]
    tpr = roc[2]
    plt.plot(fpr,tpr,label=roc[0])
    plt.legend()


# In[ ]:


for prc in prcList:
    precision = prc[1]
    recall = prc[2]
    plt.plot(precision,recall,label=prc[0])
    plt.legend()


# ## 8 Finalising algorithms and saving models
# 

# ### 8.a) Regression Althorithm
# > Linear Regression is selected as final prediction algorithm

# In[ ]:


lreg = LinearRegression()
lreg.fit(x_train,y_train)


# In[ ]:


#saving model
import pickle
pkl_Filename = "regModel"

with open(pkl_Filename, 'wb') as file:
    pickle.dump(lreg,file)


# In[ ]:


#cheking if model saved works
with open(pkl_Filename, 'rb') as file: 
    print(file)
    Pickled_LR_Model = pickle.load(file)

y_pred = Pickled_LR_Model.predict(x_test[0].reshape(1,-1))


# In[ ]:


# creating link to download the model
from IPython.display import FileLink
FileLink(pkl_Filename)


# ### 8.b) Saving Classification Model
# > Random Forest Classifier was selected

# In[ ]:


#preparing data for classification
y_train[8] = y_train[8].apply(lambda x:1 if x>0.8 else 0)
y_test[8] = y_test[8].apply(lambda x:1 if x>0.8 else 0)


# In[ ]:


rfc = RandomForestClassifier()
rfc.fit(x_train,y_train)


# In[ ]:


#saving model
import pickle
pkl_Filename = "classModel"

with open(pkl_Filename, 'wb') as file:
    pickle.dump(rfc,file)


# In[ ]:


#cheking if model saved works
with open(pkl_Filename, 'rb') as file: 
    print(file)
    Pickled_LR_Model = pickle.load(file)

y_pred = Pickled_LR_Model.predict(x_test)


# In[ ]:


# creating link to download the model
from IPython.display import FileLink
FileLink(pkl_Filename)


# In[ ]:




