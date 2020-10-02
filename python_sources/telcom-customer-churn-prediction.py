#!/usr/bin/env python
# coding: utf-8

# In[59]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# # Import packages

# In[60]:


import matplotlib.pyplot as plt
import seaborn as sns
from pylab import rcParams
import matplotlib.cm as cm

import sklearn
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import classification_report, precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.ensemble import VotingClassifier

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import warnings
warnings.filterwarnings('ignore')

get_ipython().run_line_magic('matplotlib', 'inline')


# In[61]:


telcom=pd.read_csv("../input/WA_Fn-UseC_-Telco-Customer-Churn.csv")


# # Exploratory Data Analysis

# ### **A Brief Overview of The Data**

# In[62]:


telcom.head()


# In[63]:


#A brief overview of our data value
telcom.shape


# There are 7043 rows of telecom customer dataset, 21 columns, including 20 variables and 1 target column "Churn"

# In[64]:


#Search missing value
pd.isnull(telcom).sum()


# Here is no null value data. 

# In[65]:


telcom["Churn"].value_counts()


# There are 5174 "No" and 1869 "Yes" in Churn, the dataset is imbalanced.

# In[66]:


telcom.dtypes


# Since TotalCharges supposed to be numerical data rather than object, we need to convert it to float.

# In[67]:


telcom['TotalCharges']=telcom['TotalCharges'].convert_objects(convert_numeric=True)
telcom["TotalCharges"].dtypes


# Check if TotalCharges has missing value.

# In[68]:


pd.isnull(telcom["TotalCharges"]).sum()


# There are 11 missing values in TotalCharges variable, which is not a big amount. We can drop these rows directly.

# In[69]:


telcom.dropna(inplace=True)
telcom.shape


# In[70]:


telcomdata=telcom


# We also need to replace the value of Churn column using "1" for "Yes" and "0" for "No"

# In[71]:


telcom['Churn'].replace(to_replace='Yes', value=1, inplace=True)
telcom['Churn'].replace(to_replace='No',  value=0, inplace=True)
telcom['Churn'].head()


# ### **Data Visualization**

# Firstly, we can check our the proportions of "Churn".

# In[72]:


churnvalue=telcom["Churn"].value_counts()
labels=telcom["Churn"].value_counts().index

rcParams["figure.figsize"]=6,6
plt.pie(churnvalue,labels=labels,colors=["whitesmoke","yellow"], explode=(0.1,0),autopct='%1.1f%%', shadow=True)
plt.title("Proportions of Customer Churn")
plt.show()


# ### **Feature Revelance**

# In[73]:


tel_dummies = pd.get_dummies(telcom.iloc[:,1:21])
tel_dummies.head()


# In[74]:


plt.figure(figsize=(15,8))
tel_dummies.corr()['Churn'].sort_values(ascending = False).plot(kind='bar')
plt.title("Correlations between Churn and variables")


# In the middle of the crrelation diagram, the dummie values of "gender" and "PhoneService" are approaching 0, which means these two variables have very low correlation that influencing "Churn" prediction.
# 
# We can drop them as they are not influential factors on determining churn or not churn.

# In[75]:


f, axes = plt.subplots(nrows=1, ncols=3, figsize=(15,5))

plt.subplot(1,3,1)
gender=sns.countplot(x="gender",hue="Churn",data=telcom,palette="Pastel1")
plt.xlabel("gender")
plt.title("Churn by Gender")

plt.subplot(1,3,2)
gender=sns.countplot(x="PhoneService",hue="Churn",data=telcom,palette="Pastel1")
plt.xlabel("PhoneService")
plt.title("Churn by PhoneService")

plt.subplot(1,3,3)
gender=sns.countplot(x="MultipleLines",hue="Churn",data=telcom,palette="Pastel1")
plt.xlabel("MultipleLines")
plt.title("Churn by MultipleLines")


# In[76]:


plt.figure(figsize=(20,16))
charges=telcom.iloc[:,1:20]
corr = charges.apply(lambda x: pd.factorize(x)[0]).corr()
ax = sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, 
                 linewidths=.2, cmap="YlGnBu",annot=True)
plt.title("Correlation between variables")


# OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies have strong correlations between each other, which means their data point are moving together towards the same direction.
# MultipleLines and PhoneService also have strong correlation.

# In[77]:


covariables=["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
fig,axes=plt.subplots(nrows=2,ncols=3,figsize=(16,10),sharex=False,sharey=True)
for i, item in enumerate(covariables):
    plt.subplot(2,3,(i+1),sharey=ax)
    ax=sns.countplot(x=item,hue="Churn",data=telcom,palette="Pastel2",order=["Yes","No","No internet service"])
    plt.xlabel(str(item))
    plt.title("Churn by "+str(item))
    i=i+1
plt.show()


# Look at these six barcharts, the values are similar, but not exactly the same. That means although they have strong correlation between each other, they can not replace each other. So we will keep all of them for better model training.
# 
# However, the churn values of no internet service are all the same within six variables above. It is probably because the six factors above could influence customers' decision making only if the customers are using internet service. 
# 
# Therefore we can simply merge "No internet service" value to "No" value.

# # Data Preprocess

# Firstly, we need to drop CustomerID since it is random characters for each customer. Also we will split variables and target Churn.
# 
# As we mentioned previously, "gender" and "PhoneService" have extremely low correlation with "Churn". We can ignore them since they have little influence on customer churn.

# In[78]:


telcomvar=telcom.iloc[:,1:20]


# In[79]:


def uni(columnlabel):
    print(columnlabel,"--" ,telcomvar[columnlabel].unique())
    
telcomobject=telcomvar.select_dtypes(['object'])
for i in range(0,len(telcomobject.columns)):
    uni(telcomobject.columns[i])


# As we mentioned previously, the "No internet service" value of six variables is not a determinant for customers who are not using internet service to make churn decision. These customers are not using any internet product. 
# 
# Therefore "No internet service" is the same as "No", so we can replace it by using "No".

# In[80]:


telcomvar.replace(to_replace='No internet service', value='No', inplace=True)
telcomvar.replace(to_replace='No phone service', value='No', inplace=True)
for i in range(0,len(telcomobject.columns)):
    uni(telcomobject.columns[i])


# ### **Feature Importance**

# The unique values of the variables above are all categorical. Some of them are binary, and all of them have four or less unique values. Therefore we can convert them into numerical values using Scikit-learn OneHotEncoder

# In[81]:


copy=telcomvar.copy()
copyobj=copy.select_dtypes(['object'])
def labelencode(columnlabel):
    copy[columnlabel] = LabelEncoder().fit_transform(copy[columnlabel])

for i in range(0,len(copyobj.columns)):
    labelencode(copyobj.columns[i])


# In[82]:


#Feature importance
x=copy
y=telcom['Churn']

from sklearn.ensemble import ExtraTreesClassifier
model=ExtraTreesClassifier()
model.fit(x,y)
print(model.feature_importances_) #use inbuilt class feature_importances of tree based classifiers
#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=x.columns)
feat_importances.nlargest(20).plot(kind='barh')
plt.show()


# In[83]:


dropvar=["PhoneService"]
telcomvar.drop(columns=dropvar,axis=1, inplace=True)
telcomvar.head()


# ### **ONE HOT ENCODING**

# In[84]:


telcomvar = pd.get_dummies(telcomvar)
telcomvar.head()


# In[85]:


def kdeplot(feature):
    plt.figure(figsize=(9, 4))
    plt.title("KDE for {}".format(feature))
    ax0 = sns.kdeplot(telcom[telcom['Churn'] == 0 ][feature].dropna(), color= 'navy', label= 'Churn: No')
    ax1 = sns.kdeplot(telcom[telcom['Churn'] == 1 ][feature].dropna(), color= 'orange', label= 'Churn: Yes')
kdeplot('tenure')
kdeplot('MonthlyCharges')
kdeplot('TotalCharges')


# In[86]:


fig,ax=plt.subplots(nrows=2,ncols=1,figsize=(10,10))

plt.subplot(2,1,1)
sns.barplot(x="Contract",y="Churn", data=telcom, palette="Pastel1", order= ['Month-to-month', 'One year', 'Two year'])
plt.title("Churn by Contract type")

plt.subplot(2,1,2)
sns.barplot(x="PaymentMethod",y="Churn",data=telcom,palette="Pastel1")
plt.title("Churn by PaymentMethod")


# The proportion of Churn customers with Month-to-month contract is larger than One-year-contract and Two-year contract. It may represent that set longe-term contract could be a effective approach to retain existing customers.

# In[87]:


scaler = StandardScaler(copy=False)
scaler.fit_transform(telcomvar[['tenure','MonthlyCharges','TotalCharges']])


# In[88]:


telcomvar[['tenure','MonthlyCharges','TotalCharges']]=scaler.transform(telcomvar[['tenure','MonthlyCharges','TotalCharges']])


# In[89]:


# check outliers
plt.figure(figsize = (8,4))
numbox = sns.boxplot(data=telcomvar[['tenure','MonthlyCharges','TotalCharges']], palette="Set2")
plt.title("Check outliers of standardized tenure, MonthlyCharges and TotalCharges")


# No obvious outliers existing within three variables.

# # Stratified Cross-Validation - Split training/testing datasets

# > Stratified ShuffleSplit cross-validator Provides train/test indices to split data in train/test sets. This cross-validation object is a merge of StratifiedKFold and ShuffleSplit, which returns stratified randomized folds. The folds are made by preserving the percentage of samples for each class. Note: like the ShuffleSplit strategy, stratified random splits do not guarantee that all folds will be different, although this is still very likely for sizeable datasets.
# 
# -- Scikit-learn organization (https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html#sklearn.model_selection.StratifiedShuffleSplit)

# In[90]:


X=telcomvar
y=telcom["Churn"].values

sss=StratifiedShuffleSplit(n_splits=5, test_size=0.2,random_state=0)
sss.get_n_splits(X,y)


# In[91]:


#So this is the cross-validator that we are using
print(sss)


# In[92]:


#Split train/test sets of X and y
for train_index, test_index in sss.split(X, y):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train,X_test=X.iloc[train_index], X.iloc[test_index]
    y_train,y_test=y[train_index], y[test_index]


# In[93]:


#Let's see the number of sets in each class of training and testing datasets
print(pd.Series(y_train).value_counts())
print(pd.Series(y_test).value_counts())


# # Oversampling training set

# In[94]:


from imblearn.over_sampling import ADASYN
ada= ADASYN()
X_resample,y_resample=ada.fit_sample(X_train,y_train)


# In[95]:


#concat oversampled "x" and "y" into one DataFrame
X_resample=pd.DataFrame(X_resample)
y_resample=pd.DataFrame(y_resample)
#replace column labels using the labels of original datasets
X_resample.columns=telcomvar.columns
y_resample.columns=["Churn"]


# In[96]:


y_resample["Churn"].value_counts()


# # Models training and comparison

# In[97]:


Classifiers=[["Support Vector Machine",SVC()],
             ["LogisticRegression",LogisticRegression()],
             ["Naive Bayes",GaussianNB()],
             ["Decision Tree",DecisionTreeClassifier()],
             ["Random Forest",RandomForestClassifier()],
             ["AdaBoostClassifier", AdaBoostClassifier()],
]

names=[]
prediction=[]
Classify_result=[]
for name,classifier in Classifiers:
    classifier=classifier
    classifier.fit(X_resample,y_resample)
    y_pred=classifier.predict(X_test)
    recall=recall_score(y_test,y_pred)
    precision=precision_score(y_test,y_pred)
    f_score=f1_score(y_test,y_pred)
    class_eva=pd.DataFrame([recall,precision,f_score])
    Classify_result.append(class_eva)
    name=pd.Series(name)
    names.append(name)
    y_pred=pd.Series(y_pred)
    prediction.append(y_pred)


# In[98]:


names=pd.DataFrame(names)
names=names[0].tolist()
result=pd.concat(Classify_result,axis=1)
result.columns=names
result.index=["recall","precision","f-socre"]
result


# In[99]:


prediction=pd.DataFrame(prediction)
y_pred_svc=np.array(prediction.iloc[0,:])
y_pred_lr=np.array(prediction.iloc[1,:])
y_pred_NB=np.array(prediction.iloc[2,:])
y_pred_dt=np.array(prediction.iloc[3,:])
y_pred_rf=np.array(prediction.iloc[4,:])
y_pred_AdaB=np.array(prediction.iloc[5,:])


# In[100]:


predictions=[y_pred_svc,y_pred_lr, y_pred_NB, y_pred_dt, y_pred_rf, y_pred_AdaB]

import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
        
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

fig,axes=plt.subplots(nrows=2,ncols=3,figsize=(25,10))
for i, item in enumerate(predictions):
    plt.subplot(2,3,(i+1))
    cnf_matrix = confusion_matrix(y_test,item)
    class_names = ["Remain","Churn"]
    title_label=["SVC","LogisticRegression","NaiveBayes","DecisionTree", "RandomForest","AdaBoostClassifier"]
    plot_confusion_matrix(cnf_matrix
                      , classes=class_names
                      , title='CM of '+str(title_label[i]))
    i=i+1
plt.show()


# In[101]:


from sklearn.ensemble import VotingClassifier
clf1 = GaussianNB()
clf2 = SVC(probability=True)
clf3 = LogisticRegression()
eclf1 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft')
eclf1.fit(X_resample, y_resample)
y_pred1= eclf1.predict(X_test)
labels=["Remain","Churn"]


# In[102]:


print(classification_report(y_test, y_pred1 ,target_names=labels,digits=5))


# In[103]:


cnf_matrix = confusion_matrix(y_test,y_pred1)
class_names = ["Remain","Churn"]
plot_confusion_matrix(cnf_matrix
                      , classes=class_names
                      , title='CM of Voting Classifier')

plt.show()


# In[104]:


# compute AUC and plot RPC curve
plt.figure(figsize=(8,6))
y_pred_proba1 = eclf1.predict_proba(X_test)[::,1]
fpr1, tpr1, _1 = roc_curve(y_test,  y_pred_proba1)
auc1 = roc_auc_score(y_test, y_pred_proba1)

svc = SVC(probability=True).fit(X_resample,y_resample)
y_pred_probasvc= svc.predict_proba(X_test)[::,1]
fpr, tpr, _ = roc_curve(y_test,  y_pred_probasvc)
aucsvc = roc_auc_score(y_test, y_pred_probasvc)

NB = GaussianNB().fit(X_resample,y_resample)
y_pred_probaNB= NB.predict_proba(X_test)[::,1]
fpr2, tpr2, _2 = roc_curve(y_test,  y_pred_probaNB)
aucNB = roc_auc_score(y_test, y_pred_probaNB)

lrg = LogisticRegression().fit(X_resample,y_resample)
y_pred_probalrg= lrg.predict_proba(X_test)[::,1]
fpr3, tpr3, _3 = roc_curve(y_test,  y_pred_probalrg)
auclrg = roc_auc_score(y_test, y_pred_probalrg)



lw=2
plt.plot([0, 1], [0, 1], color='lightgray', lw=lw, linestyle='--')

plt.plot(fpr1,tpr1,
         label="Voting ROC, auc="+str(auc1), 
         color='navy', linewidth=4)


plt.plot(fpr, tpr,
         label='SVM ROC, auc='+str(aucsvc),
         color='yellow', linestyle='-',  linewidth=2)

plt.plot(fpr2, tpr2,
         label='NB ROC, auc='+str(aucNB),
         color='red', linestyle=':',  linewidth=2)

plt.plot(fpr3, tpr3,
         label='LogReg ROC, auc='+str(auclrg),
         color='darkorange', linestyle='-.',  linewidth=2)

plt.legend(loc=4)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title("ROC curve of classifiers")
plt.legend(loc="lower right")

plt.show()


# # PCA implementation

# Now we are steping in the second part, Clustering for customer segmentation. In this part, we are not going to split training or testing data set. So we need to apply PCA to data in "telcomvar". 
# 
# Since using PCA on a dataset calculates the dimensions which best maximize variance, we will find which compound combinations of features best describe customers.

# In[105]:


y_pred= pd.DataFrame(np.array(prediction.iloc[1,:]))
churn_test=y_pred[y_pred[0]==1].index
churner_index= X_test.iloc[churn_test,:].index
churner=telcom.iloc[churner_index,1:20]
churner_var = pd.get_dummies(churner)
n=len(churner_var.columns)


# In[106]:


#Firstly, we need to check cumulative explained variance ratio to find out how many dimensions are necessary.
pca=PCA(n_components=n,random_state=0)
transpca=pca.fit_transform(churner_var)


# In[107]:


print("Explained Variance Ratio => {}\n".format(pca.explained_variance_ratio_))
print("Explained Variance Ratio(csum) => {}\n".format(pca.explained_variance_ratio_.cumsum()))


# From the *cumulative explained variance ratio* we can see that 99.998% variance is covered by first two dimension. Therefore we can reduce dimentionality to **two dimensions** to reduce the complexity of the problem.
# 
# Dimensionality reduction comes at a cost: Fewer dimensions used implies less of the total variance in the data is being explained.

# In[108]:


pca=PCA(n_components=2,random_state=0)
transpca=pca.fit_transform(churner_var)
reduced_data=pd.DataFrame(transpca,columns=['D_1','D_2'])
reduced_data.head()


# In[109]:


def biplot(churner_var, reduced_data, pca):
    '''
    Produce a biplot that shows a scatterplot of the reduced
    data and the projections of the original features.
    
    good_data: original data, before transformation.
               Needs to be a pandas dataframe with valid column names
    reduced_data: the reduced data (the first two dimensions are plotted)
    pca: pca object that contains the components_ attribute

    return: a matplotlib AxesSubplot object (for any additional customization)
    
    This procedure is inspired by the script:
    https://github.com/teddyroland/python-biplot
    '''

    fig, ax = plt.subplots(figsize = (14,8))
    # scatterplot of the reduced data    
    ax.scatter(x=reduced_data.loc[:, 'D_1'], y=reduced_data.loc[:, 'D_2'], 
        facecolors='b', edgecolors='b', s=70, alpha=0.5)
    
    feature_vectors = pca.components_.T

    ax.set_xlabel("Dimension 1", fontsize=14)
    ax.set_ylabel("Dimension 2", fontsize=14)
    ax.set_title("2-Dimension Visualization of Predicted Churn Customer Data", fontsize=16);
    return ax


# In[110]:


biplot(churner_var, reduced_data, pca)


# # Clustering with K-means

# In[111]:


def sil_coeff(no_clusters):
    # Apply your clustering algorithm of choice to the reduced data 
    clusterer_1 = KMeans(n_clusters=no_clusters, random_state=0 )
    clusterer_1.fit(reduced_data)
    
    # Predict the cluster for each data point
    preds_1 = clusterer_1.predict(reduced_data)
    
    # Find the cluster centers
    centers_1 = clusterer_1.cluster_centers_

    # Calculate the mean silhouette coefficient for the number of clusters chosen
    score = silhouette_score(reduced_data, preds_1)
    
    print("silhouette coefficient for `{}` clusters => {:.4f}".format(no_clusters, score))
    
clusters_range = range(2,16)
for i in clusters_range:
    sil_coeff(i)


# 2 clusters got highest silhouette score at 0.7031 which is the highest score. Therefore we can assign churn customers into 2 segments.
# 
# Before visualizing the clusters, let's select six samples as examples.

# In[112]:


samples = churner.sample(n=6)
indices= samples.index
print("Indices of Samples => {}".format(indices))

# Create a DataFrame of the chosen samples
samples_info = pd.DataFrame(telcom.loc[indices],columns = telcom.keys()).reset_index(drop = True).iloc[:,:20]
print("\nChosen samples of telecom customers dataset:")
display(samples_info)

# Apply PCA on samples
samples_var= pd.DataFrame(churner_var.loc[indices], columns = churner_var.keys()).reset_index(drop = True)
pca=PCA(n_components=2,random_state=0, svd_solver='full')
transam=pca.fit_transform(samples_var)
pca_samples=pd.DataFrame(transam,columns=['D_1','D_2'])


# In[113]:


def cluster_results(reduced_data, preds, centers, pca_samples):
    
#Visualizes the PCA-reduced cluster data in two dimensions
#Adds cues for cluster centers and selected sample data
    
    predictions = pd.DataFrame(preds, columns = ['Cluster']) 
    plot_data = pd.concat([predictions, reduced_data], axis = 1)
    
    # Generate the cluster plot
    fig, ax = plt.subplots(figsize = (14,8))

    # Color map
    cmap = cm.get_cmap('gist_rainbow')

    # Color the points based on assigned cluster
    for i, cluster in plot_data.groupby('Cluster'):   
        cluster.plot(ax = ax, kind = 'scatter', x = 'D_1', y = 'D_2',                      color = cmap((i)*1.0/(len(centers)-1)), label = 'Cluster %i'%(i), s=30);

    # Plot centers with indicators
    for i, c in enumerate(centers):
        ax.scatter(x = c[0], y = c[1], color = 'white', edgecolors = 'black',                    alpha = 1, linewidth = 2, marker = 'o', s=200);
        ax.scatter(x = c[0], y = c[1], marker='$%d$'%(i), alpha = 1, s=100);

    # Plot transformed sample points 
    ax.scatter(x = pca_samples.iloc[:,0], y = pca_samples.iloc[:,1],                s = 150, linewidth = 4, color = 'black', marker = 'x');

# Set plot title
    ax.set_title("2 Segments of Predicted Churn Customers - Samples Marked by Black Cross");


# In[114]:


# Display the results of the clustering from implementation for 3 clusters
clusterer = KMeans(n_clusters = 2)
clusterer.fit(reduced_data)
preds = clusterer.predict(reduced_data)
centers = clusterer.cluster_centers_
sample_preds = clusterer.predict(pca_samples)

cluster_results(reduced_data, preds, centers, pca_samples)


# # Data Recovery

# In[115]:


#Data Recovery
st_centers = pca.inverse_transform(centers)

# Display the centers
segments = ['Segment {}'.format(i) for i in range(0,len(centers))]
true_centers = pd.DataFrame(np.round(st_centers), columns = churner_var.keys())
true_centers.index = segments
display(true_centers)


# # Segments that samples belonging to 

# In[116]:


# Display the predictions
for i, pred in enumerate(sample_preds):
    print("Sample point", i, "predicted to be in Cluster", pred)

