#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing libraries and Reading the Dataset
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys
import os


# In[ ]:


df=pd.read_csv("../input/Admission_Predict.csv")


# In[ ]:


df.head()


# In[ ]:


print("There are",len(df.columns),"columns:")
for x in df.columns:
    sys.stdout.write(str(x)+",")


# In[ ]:


df=df.rename(columns = {'Chance of Admit ':'Chance of Admit'})


# In[ ]:


df.info()


# In[ ]:


df.head(5)


# In[ ]:


fig,ax=plt.subplots(figsize=(10,10))
sns.heatmap(df.corr(),ax=ax,annot=True,linewidths=0.05,fmt='.2f',cmap="magma")
plt.show()


# In[ ]:


print("Not having Research:",len(df[df.Research==0]))
print("Having Research:",len(df[df.Research==1]))
y=np.array([len(df[df.Research==0]),len(df[df.Research==1])])
x=["Not Having Research","Having Research"]
plt.bar(x,y)
plt.title("Research Experience")
plt.xlabel("Candidates")
plt.ylabel("Frequency")
plt.show()


# TOEFL Score:
# * The lowest TOEFL Score is 92 and the highest Toefl score is 120. The average is 107.41    

# In[ ]:


y=np.array([df["TOEFL Score"].min(),df["TOEFL Score"].mean(),df["TOEFL Score"].max()])
x=["Worest","Average","Best"]
plt.bar(x,y)
plt.title("TOEFL Scores")
plt.xlabel("Level")
plt.ylabel("TOEFL Score")
plt.show()


# GRE Score:
# * This histogram shows the frequency for GRE scores.
# * There is a density between 310 and 330.Being above this range would be a good feature for a candidate to stand out. 

# In[ ]:


df["GRE Score"].plot(kind='hist',bins=200,figsize=(6,6))
plt.title("GRE Scores")
plt.xlabel("GRE Score")
plt.ylabel("Frequency")
plt.show()


# CGPA Score for University Ratings:
# * As the quality of the university increases the CGPA score increases    

# In[ ]:


plt.scatter(df["University Rating"],df.CGPA)
plt.title("CGPA Scores for University Ratings")
plt.xlabel("University Rating")
plt.ylabel("CGPA")
plt.show()


# In[ ]:


plt.scatter(df["GRE Score"],df.CGPA)
plt.title("CGPA for GRE Scores")
plt.xlabel("GRE Score")
plt.ylabel("CGPA")
plt.show()


# * Candidates with high GRE scores usually have a high CGPA score

# In[ ]:


df[df.CGPA >=8.5].plot(kind='scatter',x='GRE Score',y='TOEFL Score',color='red')
plt.xlabel("GRE Score")
plt.ylabel("TOEFL  SCORE")
plt.title("CGPA >=8.5")
plt.grid(True)
plt.show()


# * Candidates who graduate from good universitiew are more fortunate to be accepted.

# In[ ]:


s = df[df["Chance of Admit"] >= 0.75]["University Rating"].value_counts().head(5)
plt.title("University Ratings of Candidates with an 75% acceptance chance")
s.plot(kind='bar',figsize=(20, 10))
plt.xlabel("University Rating")
plt.ylabel("Candidates")
plt.show()


# *Candidates with high CGPA scores usually have a high SOP score

# In[ ]:


plt.scatter(df["CGPA"],df.SOP)
plt.xlabel("CGPA")
plt.ylabel("SOP")
plt.title("SOP for CGPA")
plt.show()


# * Candidates with high GRE scores usually have a high SOP score

# In[ ]:


plt.scatter(df["GRE Score"],df["SOP"])
plt.xlabel("GRE Score")
plt.ylabel("SOP")
plt.title("SOP for GRE Score")
plt.show()


# ## <a id='regression'> REGRESSION ALGORITHMS (SUPERVISED MACHINE LEARNING ALGORITHMS)</a>

# ### <a id='prepareForRegression'>Preparing Data for Regression</a>

# In[ ]:


#reading the dataset
df=pd.read_csv("../input/Admission_Predict.csv")

#it may be needed in the future
serialNo=df['Serial No.'].values

df.drop(['Serial No.'],axis=1,inplace=True)

df=df.rename(columns = {'Chance of Admit ':'Chance of Admit'})


# train_test_split:
# * it split the data into random train (80%) and test (20%) subsets.    

# In[ ]:


y = df["Chance of Admit"].values
x = df.drop(["Chance of Admit"],axis=1)

#separating train (80%) and test (20%) sets
from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=42)


# In[ ]:


#normalization
from sklearn.preprocessing import MinMaxScaler
scalerX=MinMaxScaler(feature_range=(0,1))
x_train[x_train.columns]=scalerX.fit_transform(x_train[x_train.columns])
x_test[x_test.columns]=scalerX.transform(x_test[x_test.columns])


# ### <a id=' linearRegression'>Linear Regression</a>

# In[ ]:


from sklearn.linear_model import LinearRegression
lr=LinearRegression()
lr.fit(x_train,y_train)
y_head_lr=lr.predict(x_test)

print("real value of y_test[1]:"+str(y_test[1]) + "-> the predict:" +str(lr.predict(x_test.iloc[[1],:])))
print("real value of y_test[2]: " + str(y_test[2]) + " -> the predict: " + str(lr.predict(x_test.iloc[[2],:])))

from sklearn.metrics import r2_score
print("r_square score:",r2_score(y_test,y_head_lr))

y_head_lr_train=lr.predict(x_train)
print("r_square score (train dataset):",r2_score(y_train,y_head_lr_train))


# ### <a id ="randomForestRegression">Random Forest Regresssion</a>

# In[ ]:


from sklearn.ensemble import RandomForestRegressor
rfr=RandomForestRegressor(n_estimators=100,random_state=42)
rfr.fit(x_train,y_train)
y_head_rfr=rfr.predict(x_test)

from sklearn.metrics import r2_score
print("r_square score:",r2_score(y_test,y_head_rfr))
print("real value of y_test[1]:" +str(y_test[1])+"-> the predict:"+str(rfr.predict(x_test.iloc[[1],:])))
print("real value of y_test[2]:" +str(y_test[2])+"-> the predict:"+str(rfr.predict(x_test.iloc[[2],:])))

y_head_rf_train=rfr.predict(x_train)
print("r_square score (train dataset):",r2_score(y_train,y_head_rf_train))


# ### <a id="DecisionTreeRegression">Decision Tree Regression </a>

# In[ ]:


from sklearn.tree import DecisionTreeRegressor
dtr=DecisionTreeRegressor(random_state=42)
dtr.fit(x_train,y_train)
y_head_dtr=dtr.predict(x_test)

from sklearn.metrics import r2_score
print("r_square score:",r2_score(y_test,y_head_dtr))
print("real value of y_test[1]:" +str(y_test[1])+ "-> the predict" +str(dtr.predict(x_test.iloc[[1],:])))
print("real value of y_test[2]:" +str(y_test[2])+ "-> the predict"+ str(dtr.predict(x_test.iloc[[2],:])))

y_head_dtr_train=dtr.predict(x_train)
print("r_square score (train dataset):",r2_score(y_train,y_head_dtr_train))


# ### <a id='comparisonOfRegression'>Comparison of Regression Algorithms</a>
# 
# * Linear regression and random forest regression algorithms were better than decision tree regression algorithm.

# In[ ]:


y = np.array([r2_score(y_test,y_head_lr),r2_score(y_test,y_head_rfr),r2_score(y_test,y_head_dtr)])
x=["LinearRegression","RandomForestReg","DecisionTreeReg."]
plt.bar(x,y)
plt.title("Comparision of Regression Algorithms")
plt.xlabel("Regressor")
plt.ylabel("r2_score")
plt.show()


# * These are the regression estimates for samples with 5 and 50 indexes:

# In[ ]:


print("real value of y_test[5]:" +str(y_test[5]) +"-> the predict:" +str(lr.predict(x_test.iloc[[5],:])))
print("real value of y_test[5]:" +str(y_test[5]) +"-> the predict:" +str(rfr.predict(x_test.iloc[[5],:])))
print("real value of y_test[5]:" +str(y_test[5]) +"-> the predict:" +str(dtr.predict(x_test.iloc[[5],:])))
print()
print("real value of y_test[50]:" +str(y_test[50]) +"-> the predict:" +str(lr.predict(x_test.iloc[[50],:])))
print("real value of y_test[50]:" +str(y_test[50]) +"-> the predict:" +str(rfr.predict(x_test.iloc[[50],:])))
print("real value of y_test[50]:" +str(y_test[50]) +"-> the predict:" +str(lr.predict(x_test.iloc[[50],:])))


# This is the estimate and the actual acceptance possibilities made with 3 regression algorithms for test samples with 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75 indexes:

# In[ ]:


red=plt.scatter(np.arange(0,80,5),y_head_lr[0:80:5],color='red')
green=plt.scatter(np.arange(0,80,5),y_head_rfr[0:80:5],color='green')
blue=plt.scatter(np.arange(0,80,5),y_head_dtr[0:80:5],color="blue")
black=plt.scatter(np.arange(0,80,5),y_test[0:80:5],color="black")
plt.title("Comparision of Regression Algorithms")
plt.xlabel("Index of Candidate")
plt.ylabel("Chance of Admit")
plt.legend((red,green,blue,black),('LR','RFR','DTR','REAL'))
plt.show()


# Comment:
# * Because most candidates in the data have over 70% chance, many unsuccessful candidates are not well predicted.

# In[ ]:


df['Chance of Admit'].plot(kind='hist',bins=200,figsize=(6,6))
plt.title("Chance of Admit")
plt.xlabel("Chance of Admit")
plt.ylabel("Frequency")
plt.show()


# ## <a id='classification'>CLASSIFICATION ALGORITHMS (SUPERVISED MACHINE LEARNING ALGORITHMS)</a>

# ### <a id='prepareForClassification'>Preparing Data for Classification</a>

# * If a candidate's Chance of Admit is greater than 80%, the candidate will receive the 1 label.
# * If a candidate's Chance of Admit is less than or equal to 80%, the candidate will receive the 0 label.

# In[ ]:


# reading the dataset
df = pd.read_csv("../input/Admission_Predict.csv")

# it may be needed in the future.
serialNo = df["Serial No."].values
df.drop(["Serial No."],axis=1,inplace = True)

df=df.rename(columns = {'Chance of Admit ':'Chance of Admit'})
y = df["Chance of Admit"].values
x = df.drop(["Chance of Admit"],axis=1)

# separating train (80%) and test (%20) sets
from sklearn.model_selection import train_test_split
x_train, x_test,y_train, y_test = train_test_split(x,y,test_size = 0.20,random_state = 42)


# In[ ]:


#normalization
from sklearn.preprocessing import MinMaxScaler
scalerX=MinMaxScaler(feature_range=(0,1))
x_train[x_train.columns]=scalerX.fit_transform(x_train[x_train.columns])
x_test[x_test.columns]=scalerX.transform(x_test[x_test.columns])

y_train_01=[1 if each >0.8 else 0 for each in y_train]
y_test_01=[1 if each > 0.8 else 0 for each in y_test]


#List to array
y_train_01=np.array(y_train_01)
y_test_01=np.array(y_test_01)


# ### <a id='lr'>Logistic Regression</a>

# In[ ]:


from sklearn.linear_model import LogisticRegression
lrc=LogisticRegression()
lrc.fit(x_train,y_train_01)
print("score:",lrc.score(x_test,y_test_01))
print("real value of y_test_01[1]:" +str(y_test_01[1]) + "-> the predict:" +str(lrc.predict(x_test.iloc[[1],:])))
print("real value of y_test_01[2]:"+str(y_test_01[2]) +"->the predict:" +str(lrc.predict(x_test.iloc[[2],:])))


# In[ ]:


#confusion matrix
from sklearn.metrics import confusion_matrix
cm_lrc=confusion_matrix(y_test_01,lrc.predict(x_test))


# In[ ]:


#cm visualization
import seaborn as sns
import matplotlib.pyplot as plt
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm_lrc,annot=True,linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.title("Test for Test Dataset")
plt.xlabel("Predicted y values")
plt.ylabel("Predicted y values")
plt.show()


from sklearn.metrics import precision_score,recall_score
print("precision_score:",precision_score(y_test_01,lrc.predict(x_test)))
print("recall_score:",recall_score(y_test_01,lrc.predict(x_test)))


from sklearn.metrics import f1_score
print("f1_score:",f1_score(y_test_01,lrc.predict(x_test)))


# Test for Train Dataset:

# In[ ]:


cm_lrc_train=confusion_matrix(y_train_01,lrc.predict(x_train))
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm_lrc_train,annot=True,linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("predicted y values")
plt.ylabel("real y values")
plt.title("Test for Train Dataset")
plt.show()


# ### <a id='svm'>Support Vector Machine</a>

# In[ ]:


from sklearn.svm import SVC
svm=SVC(random_state=1)
svm.fit(x_train,y_train_01)
print("score:",svm.score(x_test,y_test_01))
print("real value of y_test_01[1]:"+str(y_test_01[1]))
print("real value of y_test_01[2]:"+str(y_test_01[2]))


# In[ ]:


#confusion matrix
from sklearn.metrics import confusion_matrix
cm_svm=confusion_matrix(y_test_01,svm.predict(x_test))


# In[ ]:


#cm visualization
import seaborn as sns
import matplotlib.pyplot as plt
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm_svm,annot=True,linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.title("Test for Test Dataset")
plt.xlabel("predicted y values")
plt.ylabel("real y values")
plt.show()


# In[ ]:


from sklearn.metrics import precision_score,recall_score
print("precision_score:",precision_score(y_test_01,svm.predict(x_test)))
print("recall_score:",recall_score(y_test_01,svm.predict(x_test)))


from sklearn.metrics import f1_score
print("f1_score",f1_score(y_test_01,svm.predict(x_test)))


# Test for Train Dataset:

# In[ ]:


cm_svm_train=confusion_matrix(y_train_01,svm.predict(x_train))
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm_svm_train,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("predicted y values")
plt.ylabel("real y values")
plt.title("Test for train dataset")
plt.show()


# ### <a id='gnb'>Gaussian Naive Bayes</a>

# In[ ]:


from sklearn.naive_bayes import GaussianNB
nb=GaussianNB()
nb.fit(x_train,y_train_01)
print("score:",nb.score(x_test,y_test_01))
print("real value of y_test_01[1]:"+str(y_test_01[1]))
print("real value of y_test_01[2]:" +str(y_test_01[2]))


# In[ ]:


#confusian matrix
from sklearn.metrics import confusion_matrix
cm_nb=confusion_matrix(y_test_01,nb.predict(x_test))


# In[ ]:


# cm visualization
import seaborn as sns
import matplotlib.pyplot as plt
f, ax = plt.subplots(figsize =(5,5))
sns.heatmap(cm_nb,annot = True,linewidths=0.5,linecolor="red",fmt = ".0f",ax=ax)
plt.title("Test for Test Dataset")
plt.xlabel("predicted y  values")
plt.ylabel("real y values")
plt.show()


# In[ ]:


from sklearn.metrics import precision_score,recall_score
print("precision_score",precision_score(y_test_01,nb.predict(x_test)))
print("recall_score:",recall_score(y_test_01,nb.predict(x_test)))

from sklearn.metrics import f1_score
print("f1_score:",f1_score(y_test_01,nb.predict(x_test)))


# Test for Train Dataset:

# In[ ]:


cm_nb_train=confusion_matrix(y_train_01,nb.predict(x_train))
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm_nb_train,annot=True,linewidths=0.5,linecolor="red",fmt="0.0f",ax=ax)
plt.xlabel("predicted y values")
plt.ylabel("predicted y values")
plt.title("Test for Train Dataset")
plt.show()


# ### <a id='dtc'>Decision Tree Classification</a>

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
dtc=DecisionTreeClassifier()
dtc.fit(x_train,y_train_01)
print("score:",dtc.score(x_test,y_test_01))
print("real value of y_test_01[1]:"+str(y_test_01[1]))
print("real value of y_test_01[2]:" +str(y_test_01[2]))


# In[ ]:


#confusian matrix
from sklearn.metrics import confusion_matrix
cm_dtc=confusion_matrix(y_test_01,nb.predict(x_test))


# In[ ]:


# cm visualization
import seaborn as sns
import matplotlib.pyplot as plt
f, ax = plt.subplots(figsize =(5,5))
sns.heatmap(cm_dtc,annot = True,linewidths=0.5,linecolor="red",fmt = ".0f",ax=ax)
plt.title("Test for Test Dataset")
plt.xlabel("predicted y  values")
plt.ylabel("real y values")
plt.show()


# In[ ]:


from sklearn.metrics import precision_score,recall_score
print("precision_score",precision_score(y_test_01,dtc.predict(x_test)))
print("recall_score:",recall_score(y_test_01,dtc.predict(x_test)))

from sklearn.metrics import f1_score
print("f1_score:",f1_score(y_test_01,dtc.predict(x_test)))


# Test for Train Dataset:

# In[ ]:


cm_dtc_train=confusion_matrix(y_train_01,dtc.predict(x_train))
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm_dtc_train,annot=True,linewidths=0.5,linecolor="red",fmt="0.0f",ax=ax)
plt.xlabel("predicted y values")
plt.ylabel("predicted y values")
plt.title("Test for Train Dataset")
plt.show()


# ### <a id='rfc'>Random Forest Classification</a>

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators = 100,random_state = 1)
rfc.fit(x_train,y_train_01)
print("score: ", rfc.score(x_test,y_test_01))
print("real value of y_test_01[1]: " + str(y_test_01[1]) + " -> the predict: " + str(rfc.predict(x_test.iloc[[1],:])))
print("real value of y_test_01[2]: " + str(y_test_01[2]) + " -> the predict: " + str(rfc.predict(x_test.iloc[[2],:])))

# confusion matrix
from sklearn.metrics import confusion_matrix
cm_rfc = confusion_matrix(y_test_01,rfc.predict(x_test))
# print("y_test_01 == 1 :" + str(len(y_test_01[y_test_01==1]))) # 29
# cm visualization
import seaborn as sns
import matplotlib.pyplot as plt
f, ax = plt.subplots(figsize =(5,5))
sns.heatmap(cm_rfc,annot = True,linewidths=0.5,linecolor="red",fmt = ".0f",ax=ax)
plt.title("Test for Test Dataset")
plt.xlabel("predicted y values")
plt.ylabel("real y values")
plt.show()

from sklearn.metrics import precision_score, recall_score
print("precision_score: ", precision_score(y_test_01,rfc.predict(x_test)))
print("recall_score: ", recall_score(y_test_01,rfc.predict(x_test)))

from sklearn.metrics import f1_score
print("f1_score: ",f1_score(y_test_01,rfc.predict(x_test)))


# In[ ]:


cm_rfc_train = confusion_matrix(y_train_01,rfc.predict(x_train))
f, ax = plt.subplots(figsize =(5,5))
sns.heatmap(cm_rfc_train,annot = True,linewidths=0.5,linecolor="red",fmt = ".0f",ax=ax)
plt.xlabel("predicted y values")
plt.ylabel("real y values")
plt.title("Test for Train Dataset")
plt.show()


# ### <a id='knnc'>K Nearest Neighbors Classification</a>
# 

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier

#finding k value
scores=[]
for each in range(1,50):
    knn_n=KNeighborsClassifier(n_neighbors=each)
    knn_n.fit(x_train,y_train_01)
    scores.append(knn_n.score(x_test,y_test_01))
plt.plot(range(1,50),scores) 
plt.xlabel("k")
plt.ylabel("accuracy")
plt.show()



knn = KNeighborsClassifier(n_neighbors = 3) # n_neighbors = k
knn.fit(x_train,y_train_01)
print("score of 3 :",knn.score(x_test,y_test_01))
print("real value of y_test_01[1]: " + str(y_test_01[1]) + " -> the predict: " + str(knn.predict(x_test.iloc[[1],:])))
print("real value of y_test_01[2]: " + str(y_test_01[2]) + " -> the predict: " + str(knn.predict(x_test.iloc[[2],:])))


# In[ ]:


#confusion matrix
from sklearn.metrics import confusion_matrix
cm_knn=confusion_matrix(y_test_01,knn.predict(x_test))

# cm visualization
import seaborn as sns
import matplotlib.pyplot as plt
f, ax = plt.subplots(figsize =(5,5))
sns.heatmap(cm_knn,annot = True,linewidths=0.5,linecolor="red",fmt = ".0f",ax=ax)
plt.title("Test for Test Dataset")
plt.xlabel("predicted y values")
plt.ylabel("real y values")
plt.show()

from sklearn.metrics import precision_score, recall_score
print("precision_score: ", precision_score(y_test_01,knn.predict(x_test)))
print("recall_score: ", recall_score(y_test_01,knn.predict(x_test)))

from sklearn.metrics import f1_score
print("f1_score: ",f1_score(y_test_01,knn.predict(x_test)))


# ### <a id="comparisonofclassificationalgorithms">Comparison of Classification Algorithms</a>

# * All classification algorithms achieved around 90% success. The most successful one is Gaussian Naive Bayes with 96% score.

# In[ ]:


y = np.array([lrc.score(x_test,y_test_01),svm.score(x_test,y_test_01),nb.score(x_test,y_test_01),dtc.score(x_test,y_test_01),rfc.score(x_test,y_test_01),knn.score(x_test,y_test_01)])
x=["LogisticReg.","SVM","GNB","DEC. Tree","Ran.Forest","KNN"]

plt.bar(x,y)
plt.title("Comparison of Classification Algorithms")
plt.xlabel("Classificatin")
plt.ylabel("Score")
plt.show()


# ## <a id='introduction'>CLUSTERING ALGORITHMS (UNSUPERVISED MACHINE LEARNING ALGORITHMS)</a>

# ### <a id='prepareForClustering'>Preparing Data for Clustering</a>

# In[ ]:


df = pd.read_csv("../input/Admission_Predict.csv",sep = ",")
df=df.rename(columns = {'Chance of Admit ':'ChanceOfAdmit'})
serial = df["Serial No."]
df.drop(["Serial No."],axis=1,inplace = True)
df = (df- np.min(df))/(np.max(df)-np.min(df))
y = df.ChanceOfAdmit 
x = df.drop(["ChanceOfAdmit"],axis=1)


# ### <a id='pca'>Principal Component Analysis</a>

# In[ ]:


#for data visualization
from sklearn.decomposition import PCA
pca=PCA(n_components=1,whiten=True) #whitten =normalize
pca.fit(x)
x_pca=pca.transform(x)
x_pca=x_pca.reshape(400,)
dictionary={"x":x_pca,"y":y}
data=pd.DataFrame(dictionary)
print("data")
print(data.head())
print("\ndf:")
print(df.head())


# ### <a id='kmeans'>K-means Clustering</a>

# In[ ]:


df["Serial No."] = serial
from sklearn.cluster import KMeans
wcss = []
for k in range(1,15):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,15),wcss)
plt.xlabel("k values")
plt.ylabel("WCSS")
plt.show()

kmeans = KMeans(n_clusters=3)
clusters_knn = kmeans.fit_predict(x)

df["label_kmeans"] = clusters_knn


plt.scatter(df[df.label_kmeans == 0 ]["Serial No."],df[df.label_kmeans == 0].ChanceOfAdmit,color = "red")
plt.scatter(df[df.label_kmeans == 1 ]["Serial No."],df[df.label_kmeans == 1].ChanceOfAdmit,color = "blue")
plt.scatter(df[df.label_kmeans == 2 ]["Serial No."],df[df.label_kmeans == 2].ChanceOfAdmit,color = "green")
plt.title("K-means Clustering")
plt.xlabel("Candidates")
plt.ylabel("Chance of Admit")
plt.show()

df["label_kmeans"] = clusters_knn
plt.scatter(data.x[df.label_kmeans == 0 ],data[df.label_kmeans == 0].y,color = "red")
plt.scatter(data.x[df.label_kmeans == 1 ],data[df.label_kmeans == 1].y,color = "blue")
plt.scatter(data.x[df.label_kmeans == 2 ],data[df.label_kmeans == 2].y,color = "green")
plt.title("K-means Clustering")
plt.xlabel("X")
plt.ylabel("Chance of Admit")
plt.show()


# ### <a id='hierarchical '>Hierarchical Clustering</a>

# In[ ]:


df["Serial No."] = serial

from scipy.cluster.hierarchy import linkage, dendrogram
merg = linkage(x,method="ward")
dendrogram(merg,leaf_rotation = 90)
plt.xlabel("data points")
plt.ylabel("euclidean distance")
plt.show()

from sklearn.cluster import AgglomerativeClustering
hiyerartical_cluster = AgglomerativeClustering(n_clusters = 3,affinity= "euclidean",linkage = "ward")
clusters_hiyerartical = hiyerartical_cluster.fit_predict(x)

df["label_hiyerartical"] = clusters_hiyerartical

plt.scatter(df[df.label_hiyerartical == 0 ]["Serial No."],df[df.label_hiyerartical == 0].ChanceOfAdmit,color = "red")
plt.scatter(df[df.label_hiyerartical == 1 ]["Serial No."],df[df.label_hiyerartical == 1].ChanceOfAdmit,color = "blue")
plt.scatter(df[df.label_hiyerartical == 2 ]["Serial No."],df[df.label_hiyerartical == 2].ChanceOfAdmit,color = "green")
plt.title("Hierarchical Clustering")
plt.xlabel("Candidates")
plt.ylabel("Chance of Admit")
plt.show()

plt.scatter(data[df.label_hiyerartical == 0 ].x,data.y[df.label_hiyerartical == 0],color = "red")
plt.scatter(data[df.label_hiyerartical == 1 ].x,data.y[df.label_hiyerartical == 1],color = "blue")
plt.scatter(data[df.label_hiyerartical == 2 ].x,data.y[df.label_hiyerartical == 2],color = "green")
plt.title("Hierarchical Clustering")
plt.xlabel("X")
plt.ylabel("Chance of Admit")
plt.show()


# In[ ]:


print(df.head())


# ### <a id='comparisonOfClustering'>Comparison of Clustering Algorithms</a>

# * K-means Clustering and Hierarchical Clustering are similarly.

# ## <a id='feature'>THE THREE IMPORTANT FEATURES</a>

# ### <a id='correlationForFeature'>Correlation between All Columns</a>

# * The 3 most important features for admission to the Master: CGPA, GRE SCORE, and TOEFL SCORE
# * The 3 least important features for admission to the Master: Research, LOR, and SOP

# In[ ]:


fig,ax=plt.subplots(figsize=(10,10))
sns.heatmap(df.corr(),ax=ax,annot=True,linewidths=0.05,fmt='.2f',cmap="magma")
plt.show()


# ### <a id='ThreeLinearRegression'>The Three Features for Linear Regression</a>

# * The first results for Linear Regression (7 features):
# <br> r_square score:  0.821208259148699
# 
# * The results for Linear Regression now (3 features):                               
# r_square score:  0.8212241793299223
# 
# * The two results are very close. If these 3 features (CGPA, GRE SCORE, and TOEFL SCORE) are used instead of all 7 features together, the result is not bad and performance is increased because less calculation is required.                                 
# 

# In[ ]:


df = pd.read_csv("../input/Admission_Predict.csv",sep = ",")
df=df.rename(columns = {'Chance of Admit ':'Chance of Admit'})
newDF = pd.DataFrame()
newDF["GRE Score"] = df["GRE Score"]
newDF["TOEFL Score"] = df["TOEFL Score"]
newDF["CGPA"] = df["CGPA"]
newDF["Chance of Admit"] = df["Chance of Admit"]

y_new = df["Chance of Admit"].values
x_new = df.drop(["Chance of Admit"],axis=1)

# separating train (80%) and test (%20) sets
from sklearn.model_selection import train_test_split
x_train_new, x_test_new,y_train_new, y_test_new = train_test_split(x_new,y_new,test_size = 0.20,random_state = 42)

# normalization
from sklearn.preprocessing import MinMaxScaler
scalerX = MinMaxScaler(feature_range=(0, 1))
x_train[x_train.columns] = scalerX.fit_transform(x_train[x_train.columns])
x_test[x_test.columns] = scalerX.transform(x_test[x_test.columns])

from sklearn.linear_model import LinearRegression
lr_new = LinearRegression()
lr_new.fit(x_train_new,y_train_new)
y_head_lr_new = lr_new.predict(x_test_new)

from sklearn.metrics import r2_score
print("r_square score: ", r2_score(y_test_new,y_head_lr_new))


# In[ ]:





# In[ ]:




