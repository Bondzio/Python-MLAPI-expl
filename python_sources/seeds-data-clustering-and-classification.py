#!/usr/bin/env python
# coding: utf-8

# # SEEDS DATA SET:

# Measurements of geometrical properties of kernels belonging to three different varieties of wheat-  Kama,Rosa and Canadian. 
# 
# A soft X-ray technique and GRAINS package were used to construct all seven, real-valued attributes.

# **Importing necessary Libraries:**

# In[ ]:




# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# **Reading the seeds dataset:**

# In[ ]:


df=pd.read_csv('/kaggle/input/seedsdata/seeds.csv')
df.head()


# **Checking the data type of each attribute and if any missing value in each feature:**

# In[ ]:


df.info()


# **Every attribute median and max values of all features:**

# In[ ]:


df.describe()


# In[ ]:


sns.pairplot(df)


# In[ ]:


sns.pairplot(df,hue='seedType')


# # Heat Map:

# In[ ]:


plt.figure(figsize=(8,8))
cor=df.corr()
sns.heatmap(cor,annot=True,cmap='coolwarm')
plt.ylim(8,0)


# **Splitting independent and dependent variables:**

# In[ ]:


X=df.drop('ID',axis=1,inplace=True)


# In[ ]:


a=df.groupby('seedType').count()
a


# In[ ]:


feature_cols=['area','perimeter','compactness','lengthOfKernel','widthOfKernel','asymmetryCoefficient','lengthOfKernelGroove']


# In[ ]:


X=feature_cols
y=df['seedType']


# In[ ]:


df.area.astype(float)


# In[ ]:


df.info()


# **Standardization the data:**

# In[ ]:


from sklearn.preprocessing import StandardScaler
ss=StandardScaler()
df_new=ss.fit_transform(df)


# In[ ]:


X=df.drop('seedType',axis=1)


# In[ ]:


y=df['seedType']


# **Train - Test Split:**

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=3,test_size=0.30)


# # LINEAR REGRESSION:

# In[ ]:


from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
lin_reg.fit(X, y)


# In[ ]:


print(f'Coefficients: {lin_reg.coef_}')
print(f'Intercept: {lin_reg.intercept_}')
print(f'R^2 score: {lin_reg.score(X, y)}')


# In[ ]:


lin_reg = LinearRegression()
model = lin_reg.fit(X_train,y_train)
print(f'R^2 score for train: {lin_reg.score(X_train, y_train)}')
print(f'R^2 score for test: {lin_reg.score(X_test, y_test)}')


# # LINEAR REGRESSION - OLS:

# In[ ]:


import statsmodels.api as sm
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE

X_constant = sm.add_constant(X)
model = sm.OLS(y, X_constant).fit()

predictions = model.predict(X_constant)
model.summary()


# Let's deal the problem with Classification first.

# # LOGISTIC REGRESSION:

# In[ ]:


from sklearn.linear_model import LogisticRegression

model = LogisticRegression(fit_intercept=True,solver='liblinear',multi_class='ovr')
model.fit(X_train,y_train)
y_test_pred=model.predict(X_test)
y_test_prob=model.predict_proba(X_test)


# In[ ]:


model


# In[ ]:


predict=model.predict(X_train)


# In[ ]:


from sklearn.metrics import confusion_matrix,accuracy_score,roc_auc_score,roc_curve, classification_report


# In[ ]:


print(classification_report(y_train,predict))


# In[ ]:


print('AUC Value of the model:',roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# # DECISION TREE CLASSIFIER:

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
dt=DecisionTreeClassifier()


# In[ ]:


dt.fit(X,y)


# In[ ]:


dt=DecisionTreeClassifier()

dt.fit(X_train,y_train)


# In[ ]:


y_test_pred=dt.predict(X_test)
y_test_prob=dt.predict_proba(X_test)

print ('Confusion Matrix -Test :','\n',confusion_matrix(y_test,y_test_pred))

print ('Overall accuracy -Test :',accuracy_score(y_test,y_test_pred))

print ('AUC -Test :', roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# # **Decision Tree - HYPER PARAMETER TUNING USING GRID SEARCH:**

# In[ ]:


from sklearn.model_selection import GridSearchCV

dtc=DecisionTreeClassifier()


#from sklearn import preprocessing
#y = preprocessing.label_binarize(y, classes=[0, 1, 2])

params={'max_depth':[2,3,4,5,6],
        'min_samples_leaf':[1,2,3,4,5,6,7],
        'min_samples_split':[2,3,4,5,6,7,8,9,10],
        'criterion':['gini','entrophy']}
gsearch=GridSearchCV(dtc,param_grid=params,cv=3,scoring='accuracy')


# In[ ]:


gsearch.fit(X,y)


# In[ ]:


gsearch.best_params_


# In[ ]:


gs=pd.DataFrame(gsearch.cv_results_)
gs.head()


# In[ ]:


dt=DecisionTreeClassifier(**gsearch.best_params_)

dt.fit(X_train,y_train)


# In[ ]:


y_test_pred=dt.predict(X_test)
y_test_prob=dt.predict_proba(X_test)

print ('Confusion Matrix -Test :','\n',confusion_matrix(y_test,y_test_pred))

print ('Overall accuracy -Test :',accuracy_score(y_test,y_test_pred))

print ('AUC -Test :', roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# # Decision Tree - HYPER PARAMETER TUNING USING RANDOMIZED SEARCH:

# In[ ]:


from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint

dtc=DecisionTreeClassifier()
params={'max_depth':sp_randint(2,20),
        'min_samples_leaf':sp_randint(1,20),
        'min_samples_split':sp_randint(2,40),
        'criterion':['gini','entrophy']}


rsearch=RandomizedSearchCV(dtc,param_distributions=params,
                           cv=3,n_iter=200,scoring='accuracy')


# In[ ]:


rsearch.fit(X,y)


# In[ ]:


rsearch.best_params_


# In[ ]:


rs=pd.DataFrame(rsearch.cv_results_)
rs.head()


# In[ ]:


dt=DecisionTreeClassifier(**rsearch.best_params_)

dt.fit(X_train,y_train)


# In[ ]:


y_test_pred=dt.predict(X_test)
y_test_prob=dt.predict_proba(X_test) 

print ('Confusion Matrix -Test :','\n',confusion_matrix(y_test,y_test_pred))

print ('Overall accuracy -Test :',accuracy_score(y_test,y_test_pred))

print ('AUC -Test :', roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# Desicion Tree classifier and hyperparameter tuning using grid search and randomised search all 3 give an accuracy of 0.95 and AUC is about 0.96  for the test data.

# # RANDOM FOREST CLASSIFIER:

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=3,test_size=0.30)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

rfc=RandomForestClassifier(n_estimators=100)
rfc.fit(X_train,y_train)


# In[ ]:


y_test_pred=rfc.predict(X_test)
y_test_prob=rfc.predict_proba(X_test)

print ('Confusion Matrix -Test :','\n',confusion_matrix(y_test,y_test_pred))

print ('Overall accuracy -Test :',accuracy_score(y_test,y_test_pred))

print ('AUC -Test :', roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# # Random Forest -  HYPER PARAMETER TUNING USING RANDOMIZED SEARCH:

# In[ ]:


from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint
rfc=RandomForestClassifier()

params={'n_estimators':sp_randint(100,200),
        'max_features':sp_randint(1,24),
        'max_depth':sp_randint(2,10),
        'min_samples_split':sp_randint(2,20),
        'min_samples_leaf':sp_randint(1,20),
        'criterion':['gini','entropy']}

rsearch=RandomizedSearchCV(rfc,param_distributions=params,n_iter=50,cv=3,scoring='accuracy',
                           random_state=3,return_train_score=True)
rsearch.fit(X,y)


# In[ ]:


rsearch.best_params_


# In[ ]:


pd.DataFrame(rsearch.cv_results_).head(5)


# In[ ]:


rfc=RandomForestClassifier(**rsearch.best_params_,random_state=3)
rfc.fit(X_train,y_train)


# In[ ]:


y_test_pred=rfc.predict(X_test)
y_test_prob=rfc.predict_proba(X_test)

print ('Confusion Matrix -Test :','\n',confusion_matrix(y_test,y_test_pred))

print ('Overall accuracy -Test :',accuracy_score(y_test,y_test_pred))

print ('AUC -Test :', roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# # Random Forest - HYPER PARAMETER TUNING USING GRID SEARCH:

# In[ ]:


from sklearn.model_selection import GridSearchCV
rfc=RandomForestClassifier()

params={'max_depth':[2,3,4,5,6],
        'min_samples_leaf':[1,2,3,4,5,6,7],
        'min_samples_split':[2,3,4,5,6,7,8,9,10],
        'criterion':['gini','entrophy']}
gsearch=GridSearchCV(dtc,param_grid=params,cv=3,scoring='accuracy')


# In[ ]:


gsearch.fit(X,y)


# In[ ]:


gsearch.best_params_


# In[ ]:


gs=pd.DataFrame(gsearch.cv_results_)
gs.head()


# In[ ]:


rfc=RandomForestClassifier(**gsearch.best_params_)

rfc.fit(X_train,y_train)


# In[ ]:


y_test_pred=dt.predict(X_test)
y_test_prob=dt.predict_proba(X_test)

print ('Confusion Matrix -Test :','\n',confusion_matrix(y_test,y_test_pred))

print ('Overall accuracy -Test :',accuracy_score(y_test,y_test_pred))

print ('AUC -Test :', roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# Random Forest classifier and the hyper parameters have been tuned using grid search and randomised search. Out of which rsearch has the highest accuracy in test data.

# # MULTINOMINAL NAIVE BAYES:

# In[ ]:


from sklearn.naive_bayes import MultinomialNB
mnb=MultinomialNB()


# In[ ]:


mnb.fit(X_train,y_train)

y_test_pred=mnb.predict(X_test)
y_test_prob=mnb.predict_proba(X_test)

print ('Confusion Matrix -Test :','\n',confusion_matrix(y_test,y_test_pred))

print ('Overall accuracy -Test :',accuracy_score(y_test,y_test_pred))

print ('AUC -Test :', roc_auc_score(y_test,y_test_prob, multi_class='ovr'))


# # ADA BOOST CLASSIFIER:

# In[ ]:


from sklearn.ensemble import AdaBoostClassifier
ada = AdaBoostClassifier(random_state=3)

ada.fit(X_train,y_train)


y_test_pred=ada.predict(X_test)
y_test_prob = ada.predict_proba(X_test)
print('Confusion Matrix - Test : ','\n' , confusion_matrix(y_test,y_test_pred))
print('Classification Report - Test : ','\n' , classification_report(y_test,y_test_pred))
print('Overall Accuracy - Test : ' , accuracy_score(y_test,y_test_pred))
print('AUC - Test : ' , roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# # LIGHTGBM CLASSIFIER:

# In[ ]:


import lightgbm as lgb
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform


# In[ ]:


lgbm = lgb.LGBMClassifier()


# In[ ]:


params = { 'n_estimators' : sp_randint(50,200),
        'max_depth' : sp_randint(2,15),
         'learning_rate' : sp_uniform(0.201,0.5),
         'num_leaves' : sp_randint(20,50)}


# In[ ]:


rsearch = RandomizedSearchCV(lgbm, param_distributions=params, cv=3, n_iter=200, n_jobs=-1, random_state=3)


# In[ ]:


rsearch.fit(X,y)


# In[ ]:


rsearch.best_params_


# In[ ]:


lgbm = lgb.LGBMClassifier(**rsearch.best_params_)
lgbm.fit(X_train,y_train)

y_test_pred=lgbm.predict(X_test)
y_test_prob = lgbm.predict_proba(X_test)
print('Confusion Matrix - Test : ','\n' , confusion_matrix(y_test,y_test_pred))
print('Classification Report - Test : ','\n' , classification_report(y_test,y_test_pred))
print('Overall Accuracy - Test : ' , accuracy_score(y_test,y_test_pred))
print('AUC - Test : ' , roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# out of the all the boosting techniques used, LightGBM works the best.

# # STACKING the results of 3 learners (Decision Tree, K-NN , Logistic Regression)

# In[ ]:


from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(solver='liblinear')

lr.fit(X_train,y_train)

y_test_pred=lr.predict(X_test)
y_test_prob = lr.predict_proba(X_test)
print('Confusion Matrix - Test : ','\n' , confusion_matrix(y_test,y_test_pred))
print('Classification Report - Test : ','\n' , classification_report(y_test,y_test_pred))
print('Overall Accuracy - Test : ' , accuracy_score(y_test,y_test_pred))
print('AUC - Test : ' , roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# # K-NN ALGORITHM:

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from scipy.stats import randint as sp_randint

knn = KNeighborsClassifier()

params={'n_neighbors' : sp_randint(1,15),'p' : sp_randint(1,5)}

rsearch_knn = RandomizedSearchCV(knn, param_distributions=params, cv =3,n_iter=50,n_jobs=-1,return_train_score=True, random_state=3)

rsearch_knn.fit(X,y)


# In[ ]:


rsearch_knn.best_params_


# In[ ]:


knn = KNeighborsClassifier(**rsearch_knn.best_params_)


# In[ ]:


knn.fit(X_train,y_train)
y_train_pred=knn.predict(X_train)

y_test_pred=knn.predict(X_test)
y_test_prob = knn.predict_proba(X_test)

print('Confusion Matrix - Test : ','\n' , confusion_matrix(y_test,y_test_pred))
print('Classification Report - Test : ','\n' , classification_report(y_test,y_test_pred))
print('Overall Accuracy - Test : ' , accuracy_score(y_test,y_test_pred))
print('AUC - Test : ' , roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# In[ ]:


from sklearn.ensemble import VotingClassifier

lr=LogisticRegression(solver='liblinear')
knn=KNeighborsClassifier(**rsearch_knn.best_params_)
dt=DecisionTreeClassifier(**gsearch.best_params_)


# In[ ]:


## Hard Voting

clf = VotingClassifier(estimators=[('lr',lr),('knn',knn),('dt',dt)], voting='hard')

clf.fit(X_train, y_train)

y_train_pred = clf.predict(X_train)
y_test_pred = clf.predict(X_test)

print("Accuracy score Train : ",accuracy_score(y_train,y_train_pred))
print("Accuracy score Test : ",accuracy_score(y_test,y_test_pred))
print("\n")
print('Confusion Matrix - Test : ','\n' , confusion_matrix(y_test,y_test_pred))
print('Classification Report - Test : ','\n' , classification_report(y_test,y_test_pred))
print('Overall Accuracy - Test : ' , accuracy_score(y_test,y_test_pred))
print('AUC - Test : ' , roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# In[ ]:


#Soft Voting -- equal weightages

clf =VotingClassifier(estimators=[('lr',lr),('knn',knn),('dt',dt)],voting='soft')

clf.fit(X_train,y_train)

y_test_pred=clf.predict(X_test)
y_test_prob = clf.predict_proba(X_test)
print('Confusion Matrix - Test : ','\n' , confusion_matrix(y_test,y_test_pred))
print('Classification Report - Test : ','\n' , classification_report(y_test,y_test_pred))
print('Overall Accuracy - Test : ' , accuracy_score(y_test,y_test_pred))
print('AUC - Test : ' , roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# In[ ]:


#Soft Voting -- Different weightages

clf =VotingClassifier(estimators=[('lr',lr),('knn',knn),('dt',dt)],weights=[1,2,3],voting='soft')
clf.fit(X_train,y_train)

y_test_pred=clf.predict(X_test)
y_test_prob = clf.predict_proba(X_test)

print('Confusion Matrix - Test : ','\n' , confusion_matrix(y_test,y_test_pred))
print('Classification Report - Test : ','\n' , classification_report(y_test,y_test_pred))
print('Overall Accuracy - Test : ' , accuracy_score(y_test,y_test_pred))
print('AUC - Test : ' , roc_auc_score(y_test,y_test_prob,multi_class='ovr'))


# Stacking 3 learners for better results, with the scaled data - we can find the overall accuracy and Auc results of the test data has been better in terms of Soft voting either using equal weightages or different weightages than Hard voting technique.

# ___________________________________________________________________________________________________________________________

# **Having dealt the problem wrt classification, lets check on how the data performs when the problem is processed with clustering algorithms and techniques.**

# # CLUSTERING:

# In[ ]:


df2=df.copy()


# In[ ]:


from scipy.stats import zscore
df_scaled = df2.apply(zscore)


# In[ ]:


df_scaled.head()


# # K - MEANS:

# In[ ]:


from sklearn.cluster import KMeans
model = KMeans(n_clusters = 3)


# In[ ]:


model


# In[ ]:


cluster_range = range( 1, 15 )
cluster_errors = []
for num_clusters in cluster_range:
  clusters = KMeans( num_clusters, n_init = 10 )
  clusters.fit(df_scaled)
 # labels = clusters.labels_
 # centroids = clusters.cluster_centers_
  cluster_errors.append( clusters.inertia_ )
clusters_df = pd.DataFrame( { "num_clusters":cluster_range, "cluster_errors": cluster_errors } )
clusters_df[0:15]


# In[ ]:


# Elbow plot

plt.figure(figsize=(12,6))
plt.plot( clusters_df.num_clusters, clusters_df.cluster_errors, marker = "o" )


# In[ ]:


kmeans = KMeans(n_clusters=3, n_init = 15, random_state=2345)


# In[ ]:


kmeans.fit(df_scaled)


# In[ ]:


centroids = kmeans.cluster_centers_


# In[ ]:


centroids


# In[ ]:


centroid_df = pd.DataFrame(centroids, columns = list(df_scaled) )


# In[ ]:


centroid_df


# In[ ]:


df_labels = pd.DataFrame(kmeans.labels_ , columns = list(['labels']))

df_labels['labels'] = df_labels['labels'].astype('category')


# In[ ]:


snail_df_labeled = df.join(df_labels)


# In[ ]:


df_analysis = (snail_df_labeled.groupby(['labels'] , axis=0)).head() 
df_analysis


# In[ ]:


snail_df_labeled['labels'].value_counts() 


# In[ ]:


from mpl_toolkits.mplot3d import Axes3D


# In[ ]:


fig = plt.figure(figsize=(8, 6))
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=20, azim=100)
kmeans.fit(df_scaled)
labels = kmeans.labels_
ax.scatter(df_scaled.iloc[:, 0], df_scaled.iloc[:, 1], df_scaled.iloc[:, 3],c=labels.astype(np.float), edgecolor='k')
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Length')
ax.set_ylabel('Height')
ax.set_zlabel('Weight')
ax.set_title('3D plot of KMeans Clustering')


# In[ ]:


# Now we know our best k value is 3, I am creating a new kmeans model:
kmeans2 = KMeans(n_clusters=3)

# Training the model:
clusters = kmeans2.fit_predict(df)

# Adding a label feature with the predicted class values:
df_k = df.copy(deep=True)
df_k['label'] = clusters


# **Comparing Original Classes and K-Means Algorithm Classes:**
# 
# For visualization I will use only two features (area and perimeter) for the original and predicted datasets. Different classes will have seperate color and styles.

# In[ ]:


plt.figure(figsize=(7,5))
ax1 = plt.subplot(1,2,1)
plt.title('Original Classes')
sns.scatterplot(x='area', y='perimeter', hue='seedType', style='seedType', palette='plasma',data=df, ax=ax1)

ax2 = plt.subplot(1,2,2)
plt.title('Predicted Classes')
sns.scatterplot(x='area', y='perimeter', hue='label', style='label', palette='plasma',data=df_k, ax=ax2)
plt.show()


# In[ ]:


print('Original Data Classes:')
print(df.seedType.value_counts())
print('-' * 30)
print('Predicted Data Classes:')
print(df_k.label.value_counts())


# **HIERARCHICAL CLUSTERING ALGORITHM:**
# 
# **Creating the Dendrogram:**
# 
# We use dendrogram to find how many classes we have in our data set.

# In[ ]:


from scipy.cluster.hierarchy import linkage, dendrogram
plt.figure(figsize=[10,10])
merg = linkage(df, method='ward')
dendrogram(merg, leaf_rotation=90)
plt.title('Dendrogram')
plt.xlabel('Data Points')
plt.ylabel('Euclidean Distances')
plt.show()


# **From the dendrogram we can read there are 3 classes in our data set.**

# **Hierarchical Clustering Algorithm:**

# In[ ]:


from sklearn.cluster import AgglomerativeClustering

hie_clus = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
cluster2 = hie_clus.fit_predict(df)

df_h = df.copy(deep=True)
df_h['label'] = cluster2


# **Comparing Original, K-Means and Hierarchical Clustered Classes:**

# In[ ]:


plt.title('Original Classes')
sns.scatterplot(x='area', y='perimeter', hue='seedType', style='seedType', data=df,palette='viridis')
plt.show()
plt.title('K-Means Classes')
sns.scatterplot(x='area', y='perimeter', hue='label', style='label', data=df_k,palette='viridis')
plt.show()
plt.title('Hierarchical Classes')
sns.scatterplot(x='area', y='perimeter', hue='label', style='label', data=df_h,palette='viridis')
plt.show()


# In[ ]:


print('Original Data Classes:')
print(df.seedType.value_counts())
print('-' * 30)
print('K-Means Predicted Data Classes:')
print(df_k.label.value_counts())
print('-' * 30)
print('Hierarchical Predicted Data Classes:')
print(df_h.label.value_counts())


# # Silhouette analysis for K-Means clustering:

# In[ ]:


from __future__ import print_function
get_ipython().run_line_magic('matplotlib', 'inline')


from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

print(__doc__)

# Generating the sample data from make_blobs
# This particular setting has one distinct cluster and 3 clusters placed close
# together.
X, y = make_blobs(n_samples=500,
                  n_features=2,
                  centers=4,
                  cluster_std=1,
                  center_box=(-10.0, 10.0),
                  shuffle=True,
                  random_state=1)  # For reproducibility

range_n_clusters = [2, 3, 4, 5, 6]

for n_clusters in range_n_clusters:
    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = KMeans(n_clusters=n_clusters, random_state=10)
    cluster_labels = clusterer.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X, cluster_labels)

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values =             sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.Spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
    colors = cm.Spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                c=colors)

    # Labeling the clusters
    centers = clusterer.cluster_centers_
    # Draw white circles at cluster centers
    ax2.scatter(centers[:, 0], centers[:, 1],
                marker='o', c="white", alpha=1, s=200)

    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50)

    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")

    plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

    plt.show()


# With the analysis, we can see the highest accuracy is for the clusters with  n=4 and the silhouette score is about 0.65.

# # Build An Classification model with Hierarchical clustering:

# # K-Means: 

# In[ ]:


df_k.sample(5)


# In[ ]:


x= df_k.drop('label',axis=1)
y= df_k['label']


# In[ ]:


test_size = 0.30 # taking 70:30 training and test set
seed = 7  # Random numbmer seeding for reapeatability of the code
x_train, x_validate, y_train, y_validate = train_test_split(x, y, test_size=test_size, random_state=seed)


# In[ ]:


from sklearn.preprocessing import StandardScaler
independent_scalar = StandardScaler()
x_train = independent_scalar.fit_transform (x_train) #fit and transform
x_validate = independent_scalar.transform (x_validate) # only transform


# # Decision Tree Classifier

# In[ ]:


from sklearn.tree import DecisionTreeClassifier 
#DecisionTreeClassifier is the corresponding Classifier
Dtree = DecisionTreeClassifier(max_depth=3)
Dtree.fit (x_train, y_train)


# In[ ]:


predictValues_train = Dtree.predict(x_train)
accuracy_train=accuracy_score(y_train, predictValues_train)

predictValues_validate = Dtree.predict(x_validate)
accuracy_validate=accuracy_score(y_validate, predictValues_validate)

print("Train Accuracy  :: ",accuracy_train)
print("Validation Accuracy  :: ",accuracy_validate)


# In[ ]:


print('Classification Report')
print(classification_report(y_validate, predictValues_validate))


# # RANDOM FOREST:

# In[ ]:



RFclassifier = RandomForestClassifier(n_estimators = 100, random_state = 0,min_samples_split=5,criterion='gini',max_depth=5)
RFclassifier.fit(x_train, y_train)


# In[ ]:


predictValues_validate = RFclassifier.predict(x_validate)
accuracy_validate=accuracy_score(y_validate, predictValues_validate)

predictValues_train = RFclassifier.predict(x_train)
accuracy_train=accuracy_score(y_train, predictValues_train)


print("Train Accuracy  :: ",accuracy_train)
print("Validation Accuracy  :: ",accuracy_validate)


# In[ ]:


RFclassifier = RandomForestClassifier(n_estimators = 11, random_state = 0,min_samples_split=5,criterion='gini',max_depth=5)
RFclassifier.fit(x_train, y_train)


# In[ ]:


predictValues_validate = RFclassifier.predict(x_validate)
accuracy_validate=accuracy_score(y_validate, predictValues_validate)

predictValues_train = RFclassifier.predict(x_train)
accuracy_train=accuracy_score(y_train, predictValues_train)


print("Train Accuracy  :: ",accuracy_train)
print("Validation Accuracy  :: ",accuracy_validate)


# In[ ]:


print('Classification Report')
print(classification_report(y_validate, predictValues_validate))


# # K-NN :

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
from scipy.stats import zscore


# In[ ]:


x= df_k.drop('label',axis=1)
y= df_k['label']


# In[ ]:


x_standardize = x.apply(zscore)


# In[ ]:


#KNN only takes array as input hence it is importanct to convert dataframe to array
x1 = np.array(x_standardize)
y1 = np.array(y)


# In[ ]:


test_size = 0.30 # taking 70:30 training and test set
seed = 7  # Random numbmer seeding for reapeatability of the code
x_train, x_validate, y_train, y_validate = train_test_split(x1, y1, test_size=test_size, random_state=seed)


# In[ ]:


KNN = KNeighborsClassifier(n_neighbors= 8 , weights = 'uniform', metric='euclidean')
KNN.fit(x_train, y_train)


# In[ ]:


predictValues_train = KNN.predict(x_train)
print(predictValues_train)
accuracy_train=accuracy_score(y_train, predictValues_train)
print("Train Accuracy  :: ",accuracy_train)


# In[ ]:


predictValues_validate = KNN.predict(x_validate)
print(predictValues_validate)
accuracy_validate=accuracy_score(y_validate, predictValues_validate)
print("Validation Accuracy  :: ",accuracy_validate)


# Building a model using K-means algorithms of clustering, Random forest classifier has the highest accuracy in f1 score without underfitting or overfitting values.

# # Build An Classification model with Non - Hierarchical clustering:

# # Agglomerative Clustering:

# In[ ]:


df_h.sample(5)


# In[ ]:


x= df_k.drop('label',axis=1)
y= df_k['label']


# In[ ]:


test_size = 0.30 # taking 70:30 training and test set
seed = 7  # Random numbmer seeding for reapeatability of the code
x_train, x_validate, y_train, y_validate = train_test_split(x, y, test_size=test_size, random_state=seed)


# In[ ]:


from sklearn.preprocessing import StandardScaler
independent_scalar = StandardScaler()
x_train = independent_scalar.fit_transform (x_train) #fit and transform
x_validate = independent_scalar.transform (x_validate) # only transform


# # DECISION TREE CLASSIFIER:

# In[ ]:


from sklearn.tree import DecisionTreeClassifier 
#DecisionTreeClassifier is the corresponding Classifier
Dtree = DecisionTreeClassifier(max_depth=3)
Dtree.fit (x_train, y_train)


# In[ ]:


predictValues_train = Dtree.predict(x_train)
accuracy_train=accuracy_score(y_train, predictValues_train)

predictValues_validate = Dtree.predict(x_validate)
accuracy_validate=accuracy_score(y_validate, predictValues_validate)

print("Train Accuracy  :: ",accuracy_train)
print("Validation Accuracy  :: ",accuracy_validate)


# In[ ]:


print('Classification Report')
print(classification_report(y_validate, predictValues_validate))


# # RANDOM FOREST:

# In[ ]:


RFclassifier = RandomForestClassifier(n_estimators = 100, random_state = 0,min_samples_split=5,criterion='gini',max_depth=5)
RFclassifier.fit(x_train, y_train)


# In[ ]:


predictValues_validate = RFclassifier.predict(x_validate)
accuracy_validate=accuracy_score(y_validate, predictValues_validate)

predictValues_train = RFclassifier.predict(x_train)
accuracy_train=accuracy_score(y_train, predictValues_train)


print("Train Accuracy  :: ",accuracy_train)
print("Validation Accuracy  :: ",accuracy_validate)


# In[ ]:


RFclassifier = RandomForestClassifier(n_estimators = 11, random_state = 0,min_samples_split=5,criterion='gini',max_depth=5)
RFclassifier.fit(x_train, y_train)


# In[ ]:


predictValues_validate = RFclassifier.predict(x_validate)
accuracy_validate=accuracy_score(y_validate, predictValues_validate)

predictValues_train = RFclassifier.predict(x_train)
accuracy_train=accuracy_score(y_train, predictValues_train)


print("Train Accuracy  :: ",accuracy_train)
print("Validation Accuracy  :: ",accuracy_validate)


# In[ ]:


print('Classification Report')
print(classification_report(y_validate, predictValues_validate))


# # K-NN

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
from scipy.stats import zscore


# In[ ]:


x= df_k.drop('label',axis=1)
y= df_k['label']


# In[ ]:


x_standardize = x.apply(zscore)


# In[ ]:


#KNN only takes array as input hence it is importanct to convert dataframe to array
x1 = np.array(x_standardize)
y1 = np.array(y)


# In[ ]:


test_size = 0.30 # taking 70:30 training and test set
seed = 7  # Random numbmer seeding for reapeatability of the code
x_train, x_validate, y_train, y_validate = train_test_split(x1, y1, test_size=test_size, random_state=seed)


# In[ ]:


KNN = KNeighborsClassifier(n_neighbors= 8 , weights = 'uniform', metric='euclidean')
KNN.fit(x_train, y_train)


# In[ ]:


predictValues_train = KNN.predict(x_train)
print(predictValues_train)
accuracy_train=accuracy_score(y_train, predictValues_train)
print("Train Accuracy  :: ",accuracy_train)


# In[ ]:


predictValues_validate = KNN.predict(x_validate)
print(predictValues_validate)
accuracy_validate=accuracy_score(y_validate, predictValues_validate)
print("Validation Accuracy  :: ",accuracy_validate)


# In agglomerative clustering, Random forest is the best generalized model with accuracy of 0.98%.

# ___________________________________________________________________________________________________________________________

# **NOTE:**

# The analysis for the given dataset is done in both the perspectives of classification and clustering algorithms.
# 
# The maximum accuracy and the best models are evaluated using different techniques and test scores. 
# 
# As per the necessity and requirement the obtained results can be modified further to proceed.

# # END
