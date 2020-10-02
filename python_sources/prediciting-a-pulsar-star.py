#!/usr/bin/env python
# coding: utf-8

# # ** Introduction **
# 
# ### Hello, in this notebook I will do some experiments to figure out the best Machine Learning algorithm on this data and try to tune them to get highest success.  After tuning I will compare them to find best one of the following 6 models.
# 
# ### <a href="#eda">EDA</a>
# ### <a href="#visual">Visual EDA</a>
# ### <a href="#prep">Data Preprocess</a>
# 
# ### <a href="#mls">Machine Learning Models</a>
# *  <a href="#lr"> Logistic Regression</a>
# *  <a href="#knn"> KNN</a>
# *  <a href="#svm">SVM</a>
# *  <a href="#rf">Random Forest</a>
# *  <a href="#dc">Decision Tree</a>
# *  <a href="#nb">Naive Bayes</a>
# 
# ### <a href="#res">Results and Comparisons</a>

# <a id="eda"></a>
# ## ** Exploratory Data Analysis **

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing
import warnings
warnings.filterwarnings("ignore")


# ### Loading the dataset

# In[ ]:


DataFrame = pd.read_csv("../input/pulsar_stars.csv")  


# ### Investigating the Dataset

# In[ ]:


DataFrame.head()    # first 5 rows of whole columns


# ### Looking to Dtypes and amounts of values

# In[ ]:


DataFrame.info()   # information about data types and amount of non-null rows of our Dataset


# (Bonus) data types are all numeric and non-null, I don't need to do any transformations or cleaning.

# ### Statistical Investigation

# In[ ]:


DataFrame.describe()   # statistical information about our data


# In[ ]:


DataFrame.corr()    # correlation between fields


# <a id="visual"></a>
# ## ** Visual EDA **

# In[ ]:


import matplotlib.pyplot as plt    # basic plotting library
import seaborn as sns              # more advanced visual plotting library


# ### ** PairPlot **  (each column is compared the others and itself)

# In[ ]:


sns.pairplot(data=DataFrame,
             palette="husl",
             hue="target_class",
             vars=[" Mean of the integrated profile",
                   " Excess kurtosis of the integrated profile",
                   " Skewness of the integrated profile",
                   " Mean of the DM-SNR curve",
                   " Excess kurtosis of the DM-SNR curve",
                   " Skewness of the DM-SNR curve"])

plt.suptitle("PairPlot of Data Without Std. Dev. Fields",fontsize=18)

plt.tight_layout()
plt.show()   # pairplot without standard deviaton fields of data


# we can see that our data is quite separable on most of the columns

# ### ** Correlation HeatMap **

# In[ ]:


plt.figure(figsize=(16,12))
sns.heatmap(data=DataFrame.corr(),annot=True,cmap="bone",linewidths=1,fmt=".2f",linecolor="gray")
plt.title("Correlation Map",fontsize=20)
plt.tight_layout()
plt.show()      # lightest and darkest cells are most correlated ones


# Most of our Columns are already related or derived from one or another. And we can see it clearly on some Cells above

# ### ** ViolinPlot **  (act as a boxplot but we can see amounts too)

# In[ ]:


plt.figure(figsize=(16,10))

plt.subplot(2,2,1)
sns.violinplot(data=DataFrame,y=" Mean of the integrated profile",x="target_class")

plt.subplot(2,2,2)
sns.violinplot(data=DataFrame,y=" Mean of the DM-SNR curve",x="target_class")

plt.subplot(2,2,3)
sns.violinplot(data=DataFrame,y=" Standard deviation of the integrated profile",x="target_class")

plt.subplot(2,2,4)
sns.violinplot(data=DataFrame,y=" Standard deviation of the DM-SNR curve",x="target_class")


plt.suptitle("ViolinPlot",fontsize=20)

plt.show()


# We can see that our data has different kind of distributions which is helpful for training our models.

# <a id="prep"></a>
# ## ** Data PreProcessing **

# ### Splitting the Feature and Label fields

# In[ ]:


labels = DataFrame.target_class.values

DataFrame.drop(["target_class"],axis=1,inplace=True)

features = DataFrame.values


# ### Scaling the Features  

# In[ ]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

features_scaled = scaler.fit_transform(features)


# ###  Splitting the Train and the Test rows

# In[ ]:


from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(features_scaled,labels,test_size=0.2)


# ## ** Machine Learning Models **
# <a id="mls"></a>

# <a id="lr"></a>
# ### ** Logistic Regression **

# In[ ]:


from sklearn.linear_model import LogisticRegression
lr_model = LogisticRegression(random_state=42,solver="liblinear",C=1.6,penalty="l1")

lr_model.fit(x_train,y_train)

y_head_lr = lr_model.predict(x_test)

lr_score = lr_model.score(x_test,y_test)


# <a id="dc"></a>
# ### ** Decision Tree Classifier **

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
dc_model = DecisionTreeClassifier(random_state=42)

dc_model.fit(x_train,y_train)

y_head_dc = dc_model.predict(x_test)

dc_score = dc_model.score(x_test,y_test)


# <a id="rf"></a>
# ### ** Random Forest Classifier **

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rfc_model = RandomForestClassifier(n_estimators=37,random_state=42,max_leaf_nodes=200,criterion="entropy")

rfc_model.fit(x_train,y_train)

y_head_rfc = rfc_model.predict(x_test)

rfc_score = rfc_model.score(x_test,y_test)


#    <a id="nb"></a>
#   ### ** Naive Bayes Classifier **

# In[ ]:


from sklearn.naive_bayes import GaussianNB
nb_model = GaussianNB()

nb_model.fit(x_train,y_train)

y_head_nb = nb_model.predict(x_test)

nb_score = nb_model.score(x_test,y_test)


# <a id="knn"></a>
# ### ** K Nearest Neighbors **

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
knn_model = KNeighborsClassifier(n_neighbors=7,weights="distance")

knn_model.fit(x_train,y_train)

y_head_knn = knn_model.predict(x_test)

knn_score = knn_model.score(x_test,y_test)


# <a id="svm"></a>
# ### ** Support Vector Machine **
# 

# In[ ]:


from sklearn.svm import SVC
svm_model = SVC(random_state=42,C=250,gamma=1.6,kernel="poly",probability=True)

svm_model.fit(x_train,y_train)

y_head_svm = svm_model.predict(x_test)

svm_score = svm_model.score(x_test,y_test)


# <a id="res"></a>
# ## ** Model Evaluating **

# ### ** Confusion Matrix **

# In[ ]:


from sklearn.metrics import confusion_matrix

cm_lr = confusion_matrix(y_test,y_head_lr)
cm_dc = confusion_matrix(y_test,y_head_dc)
cm_knn = confusion_matrix(y_test,y_head_knn)
cm_nb = confusion_matrix(y_test,y_head_nb)
cm_rfc = confusion_matrix(y_test,y_head_rfc)
cm_svm = confusion_matrix(y_test,y_head_svm)


# In[ ]:


plt.figure(figsize=(24,12))

plt.suptitle("Confusion Matrixes",fontsize=24)

plt.subplot(2,3,1)
plt.title("Logistic Regression Confusion Matrix")
sns.heatmap(cm_lr,cbar=False,annot=True,cmap="CMRmap_r",fmt="d")

plt.subplot(2,3,2)
plt.title("Decision Tree Classifier Confusion Matrix")
sns.heatmap(cm_dc,cbar=False,annot=True,cmap="CMRmap_r",fmt="d")

plt.subplot(2,3,3)
plt.title("K Nearest Neighbors Confusion Matrix")
sns.heatmap(cm_knn,cbar=False,annot=True,cmap="CMRmap_r",fmt="d")

plt.subplot(2,3,4)
plt.title("Naive Bayes Confusion Matrix")
sns.heatmap(cm_nb,cbar=False,annot=True,cmap="CMRmap_r",fmt="d")

plt.subplot(2,3,5)
plt.title("Random Forest Confusion Matrix")
sns.heatmap(cm_rfc,cbar=False,annot=True,cmap="CMRmap_r",fmt="d")

plt.subplot(2,3,6)
plt.title("Support Vector Machine Confusion Matrix")
sns.heatmap(cm_svm,cbar=False,annot=True,cmap="CMRmap_r",fmt="d")

plt.show()


# if we compare total mistakes:  RandomForest, SVM, KNN seem to be best for this dataset

# ### ** Bar Chart Comparison  ** 

# In[ ]:


algorithms = ("Logistic Regression","Decision Tree","Random Forest","K Nearest Neighbors","Naive Bayes","Support Vector Machine")
scores = (lr_score,dc_score,rfc_score,knn_score,nb_score,svm_score)
y_pos = np.arange(1,7)
colors = ("red","gray","purple","green","orange","blue")

plt.figure(figsize=(24,12))
plt.xticks(y_pos,algorithms,fontsize=18)
plt.yticks(np.arange(0.00, 1.01, step=0.01))
plt.ylim(0.90,1.00)
plt.bar(y_pos,scores,color=colors)
plt.grid()
plt.suptitle("Bar Chart Comparison of Models",fontsize=24)
plt.show()


# if we look at the graph and check the scores, LogisticRegression, RandomForest and SVM are better than the others.

# # ** Conclusion **

# ### After my tests I see that:
# ### RandomForest and SVM are Overall winnners in my case above.
# But all of these 6 models did a great job on predicting 

# In[ ]:


# thanks for reading. Votes, Comments and Advices are all welcome :) 


# In[ ]:





# In[ ]:




