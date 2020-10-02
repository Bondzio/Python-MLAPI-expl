#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')
dataset = pd.read_csv('turkiye-student-evaluation_generic.csv')
dataset.head()


# In[ ]:


dataset = pd.read_csv('turkiye-student-evaluation_generic.csv')


# In[ ]:


dataset.head()


# In[ ]:


dataset.describe()


# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # visualize
import matplotlib.pyplot as plt


# In[ ]:


plt.figure(figsize=(18,18))
sns.heatmap(dataset.corr(),annot = True,fmt = ".2f",cbar = True)
plt.xticks(rotation=90)
plt.yticks(rotation = 0)


# ## To understand which course got most responde

# In[ ]:


plt.figure(figsize=(10, 6))
sns.countplot(x='class', data=dataset)


# ### Below Graph to see how the rating has been given by student for each questions

# In[ ]:


plt.figure(figsize=(10,10))
sns.boxplot(data=dataset.iloc[:,5:33 ])


# ### By above graph, we can see that very less students have given completely disagree (Rating 1) for Question Q14, Q15, Q17, Q19 - Q22, Q25,Q28

# ## Lets understand the students have responded for the questions against classes

# In[ ]:


# Calculate mean for each question response for all the classes.
questionmeans = []
classlist = []
questions = []
totalplotdata = pd.DataFrame(list(zip(classlist,questions,questionmeans))
                      ,columns=['class','questions', 'mean'])
for class_num in range(1,14):
    class_data = dataset[(dataset["class"]==class_num)]
    
    questionmeans = []
    classlist = []
    questions = []
    
    for num in range(1,14):
        questions.append(num)
    #Class related questions are from Q1 to Q12
    for col in range(5,17):
        questionmeans.append(class_data.iloc[:,col].mean())
    classlist += 12 * [class_num] 
    print(classlist)
    plotdata = pd.DataFrame(list(zip(classlist,questions,questionmeans))
                      ,columns=['class','questions', 'mean'])
    totalplotdata = totalplotdata.append(plotdata, ignore_index=True)
    


# In[ ]:


plt.figure(figsize=(20, 10))
sns.pointplot(x="questions", y="mean", data=totalplotdata, hue="class")


# ### Lets see how rating has been given against instructor wise.

# In[ ]:


# Calculate mean for each question response for all the classes.
questionmeans = []
inslist = []
questions = []
totalplotdata = pd.DataFrame(list(zip(inslist,questions,questionmeans))
                      ,columns=['ins','questions', 'mean'])
for ins_num in range(1,4):
    ins_data = dataset[(dataset["instr"]==ins_num)]
    questionmeans = []
    inslist = []
    questions = []
    
    for num in range(13,29):
        questions.append(num)
    
    for col in range(17,33):
        questionmeans.append(ins_data.iloc[:,col].mean())
    inslist += 16 * [ins_num] 
    plotdata = pd.DataFrame(list(zip(inslist,questions,questionmeans))
                      ,columns=['ins','questions', 'mean'])
    totalplotdata = totalplotdata.append(plotdata, ignore_index=True)
    plt.figure(figsize=(15, 5))
sns.pointplot(x="questions", y="mean", data=totalplotdata, hue="ins")


# ### Lets begin to cluster the students based on the questionaire data

# #### Lets try to cluster all the students based on the Question responses data.

# In[ ]:


dataset_questions = dataset.iloc[:,5:]


# In[ ]:


dataset_questions.head()


# # PCA Analysis 

# In[ ]:


import numpy as np
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
X=dataset_questions
pca = PCA().fit(scale(X))
plt.plot(np.cumsum(pca.explained_variance_ratio_)*100)
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance');


# In[ ]:


X=dataset_questions
pca = PCA().fit(scale(X))
plt.plot(np.cumsum(pca.explained_variance_ratio_)*100)
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance');


# In[ ]:


pca = PCA(n_components = 2)
dataset_questions_pca = pca.fit_transform(dataset_questions)


# ### Variance (% cumulative) explained by the principal components

# In[ ]:


print(np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100))
print(len(np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)))


# In[ ]:


np.cumsum(pca.explained_variance_ratio_)*100


# ###  Eiegenvalues

# In[ ]:


pca.explained_variance_


# # Clustring 

# In[ ]:


from sklearn.cluster import KMeans
wcss = []
for i in range(1, 7):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(dataset_questions_pca)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 7), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


# ## based on the Elbow graph , we can go for 3 clusters.

# In[ ]:


kmeans = KMeans(n_clusters = 3, init = 'k-means++')
y_kmeans = kmeans.fit_predict(dataset_questions_pca)
# Visualising the clusters
plt.scatter(dataset_questions_pca[y_kmeans == 0, 0], dataset_questions_pca[y_kmeans == 0, 1], s = 100, c = 'yellow', label = 'Cluster 1')
plt.scatter(dataset_questions_pca[y_kmeans == 1, 0], dataset_questions_pca[y_kmeans == 1, 1], s = 100, c = 'green', label = 'Cluster 2')
plt.scatter(dataset_questions_pca[y_kmeans == 2, 0], dataset_questions_pca[y_kmeans == 2, 1], s = 100, c = 'red', label = 'Cluster 3')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 100, c = 'blue', label = 'Centroids')
plt.title('Clusters of students')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.legend()
plt.show()


# ### Looking at the above graph , i see we have 3 clusters of students who have given like Negative, Neutral and Positive feedback

# In[ ]:


import collections
collections.Counter(y_kmeans)


# ### So we have 2358 students who have given negative ratings overall , 2222 students with positive ratings and 1240 students with nuetral response

# ##  Using the dendrogram to find the optimal number of clusters

# In[ ]:


import scipy.cluster.hierarchy as sch
dendrogram = sch.dendrogram(sch.linkage(dataset_questions_pca, method = 'ward'))
#plt.figure(figsize=(20, 10))
plt.title('Dendrogram')
plt.xlabel('questions')
plt.ylabel('Euclidean distances')
plt.show()


# In[ ]:


import scipy.cluster.hierarchy as sch

dendrogram = sch.dendrogram(sch.linkage(dataset_questions_pca, method = 'centroid'))
#plt.figure(figsize=(20, 10))
plt.title('Dendrogram')
plt.xlabel('questions')
plt.ylabel('Euclidean distances')
plt.show()


# In[ ]:


# Fitting Hierarchical Clustering to the dataset
from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters = 2, affinity = 'euclidean', linkage = 'ward')
y_hc = hc.fit_predict(dataset_questions_pca)
X = dataset_questions_pca
# Visualising the clusters
plt.scatter(X[y_hc == 0, 0], X[y_hc == 0, 1], s = 100, c = 'yellow', label = 'Cluster 1')
plt.scatter(X[y_hc == 1, 0], X[y_hc == 1, 1], s = 100, c = 'red', label = 'Cluster 2')
plt.title('Clusters of STUDENTS')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.legend()
plt.show()


# In[ ]:


# Let me check the count of students in each cluster
import collections
collections.Counter(y_hc)


# # Factor analysis 

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
import pandas as pd
import numpy as np
#from sklearn.datasets import load_iris
from sklearn.decomposition import FactorAnalysis
factor = FactorAnalysis(n_components=2, random_state=101).fit(X)
pd.DataFrame(factor.components_)


# # Try

# In[ ]:


dataset.head(2)


# In[ ]:


from sklearn.preprocessing import scale


# In[ ]:


data=scale(dataset.iloc[:,3:])
data


# In[ ]:


from pylab import * 
import pandas as pd
import numpy as np   
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB  
import sklearn.metrics as sm  
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from collections import Counter
from sklearn.naive_bayes import GaussianNB  
from sklearn import tree, svm
from sklearn.linear_model import LogisticRegression  
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import ClusterCentroids
from imblearn.combine import SMOTEENN
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import RandomOverSampler


# In[ ]:


seed = 7
test_size = 0.15
Data=data
Target=dataset.iloc[:,2]
Classes=Target


# In[ ]:


Naive_Bayes_classifier = GaussianNB() 
DTC = tree.DecisionTreeClassifier()
LR = LogisticRegression() 
SVM_Classifier = svm.SVC() 
KNN = KNeighborsClassifier(n_neighbors=5)  
RF=RandomForestClassifier(n_estimators=25)
X_train, X_test, y_train, y_test = train_test_split(Data, Target, test_size=test_size, random_state=seed)
Trained_Classifier  =RF.fit(X_train, y_train)  

Tested_Classifier = Trained_Classifier.predict(X_test)  
  
# Compute the confusion matrix and calculation the performance creteria   
P=sm.confusion_matrix(y_test,Tested_Classifier)  
Accuracy = ((P[0,0] + P[1,1]+P[2,2])/float(sum(P)))*100  
sensitivity = (P[0,0] / float(sum(P[:,0])))*100  
specificity = (P[1,1] / float(sum(P[:,1])))*100  
Precision =(P[0,0] / float(sum(P[0,:])))*100 # TP/(TP+FP)
F_measure=(2*sensitivity*Precision )/(sensitivity+Precision)

print(" Accuracy = %s" % Accuracy, " Sensitivity = %s" % sensitivity," Specificity = %s" % specificity)  
print(" Precision = %s" % Precision ,"F-measure= %s"%F_measure)  

             


# In[ ]:





# In[ ]:


Naive_Bayes_classifier = GaussianNB() 
DTC = tree.DecisionTreeClassifier()
LR = LogisticRegression() 
SVM_Classifier = svm.SVC() 
KNN = KNeighborsClassifier(n_neighbors=5)  
RF=RandomForestClassifier(n_estimators=25)
X_train, X_test, y_train, y_test = train_test_split(Data, Target, test_size=test_size, random_state=seed)
Trained_Classifier = LR.fit(X_train, y_train)  

Tested_Classifier = Trained_Classifier.predict(X_test)  
  
# Compute the confusion matrix and calculation the performance creteria   
P=sm.confusion_matrix(y_test,Tested_Classifier)  
Accuracy = ((P[0,0] + P[1,1]+P[2,2])/float(sum(P)))*100  
sensitivity = (P[0,0] / float(sum(P[:,0])))*100  
specificity = (P[1,1] / float(sum(P[:,1])))*100  
Precision =(P[0,0] / float(sum(P[0,:])))*100 # TP/(TP+FP)
F_measure=(2*sensitivity*Precision )/(sensitivity+Precision)

print(" Accuracy = %s" % Accuracy, " Sensitivity = %s" % sensitivity," Specificity = %s" % specificity)  
print(" Precision = %s" % Precision ,"F-measure= %s"%F_measure)  


# In[ ]:


print('original data check balance: ',sorted(Counter(Target).items()))


# In[ ]:


plt.figure(figsize=(10, 6))
sns.countplot(x=Target, data=dataset)
percentage=print('Class1=',4909*100/(5820),'Class2=' ,576*100/(5820),'Class3=',335*100/(5820))


# # we have biased data, so I am going to resolve it

# In[ ]:


cc = ClusterCentroids(random_state=0)
smote_tomek = SMOTETomek(random_state=0)
Data1, Classes1 = smote_tomek.fit_sample(Data, Classes)
print(sorted(Counter(Classes1).items()))
X_train, X_test, y_train, y_test = train_test_split(Data, Classes, test_size=test_size, random_state=seed)
print('modified data check balance using SMOTETomek: ',sorted(Counter(Classes1).items()))
Data2, Classes2 = cc.fit_sample(Data, Classes)
print('modified data check balance using undrsampling: ',sorted(Counter(Classes2).items()))
ros = RandomOverSampler(random_state=0)
Data3, Classes3 = ros.fit_sample(Data, Classes)
print('modified data check balance using oversampling: ',sorted(Counter(Classes3).items()))


# In[ ]:





# In[ ]:


seed = 7
test_size = 0.15


Naive_Bayes_classifier = GaussianNB() 
DTC = tree.DecisionTreeClassifier()
LR = LogisticRegression() 
SVM_Classifier = svm.SVC() 
KNN = KNeighborsClassifier(n_neighbors=5)  
RF=RandomForestClassifier(n_estimators=25)
X_train, X_test, y_train, y_test = train_test_split(Data1, Classes1, test_size=test_size, random_state=seed)
Trained_Classifier  =RF.fit(X_train, y_train)  
Tested_Classifier = Trained_Classifier.predict(X_test)  
  
# Compute the confusion matrix and calculation the performance creteria   
P=sm.confusion_matrix(y_test,Tested_Classifier)  
Accuracy = ((P[0,0] + P[1,1]+P[2,2])/float(sum(P)))*100  
sensitivity = (P[0,0] / float(sum(P[:,0])))*100  
specificity = (P[1,1] / float(sum(P[:,1])))*100  
Precision =(P[0,0] / float(sum(P[0,:])))*100 # TP/(TP+FP)
F_measure=(2*sensitivity*Precision )/(sensitivity+Precision)

print(" Accuracy = %s" % Accuracy, " Sensitivity = %s" % sensitivity," Specificity = %s" % specificity)  
print(" Precision = %s" % Precision ,"F-measure= %s"%F_measure)  

