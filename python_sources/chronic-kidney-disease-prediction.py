#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing the libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report,accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


#Reading the dataset
kidney = pd.read_csv("../input/kidney_disease.csv")
kidney.head()


# In[ ]:


# Information about the dataset
kidney.info()


# In[ ]:


# Description of the dataset
kidney.describe()


# In[ ]:


# To see what are the column names in our dataset
print(kidney.columns)


# In[ ]:


# Mapping the text to 1/0 and cleaning the dataset 
kidney[['htn','dm','cad','pe','ane']] = kidney[['htn','dm','cad','pe','ane']].replace(to_replace={'yes':1,'no':0})
kidney[['rbc','pc']] = kidney[['rbc','pc']].replace(to_replace={'abnormal':1,'normal':0})
kidney[['pcc','ba']] = kidney[['pcc','ba']].replace(to_replace={'present':1,'notpresent':0})
kidney[['appet']] = kidney[['appet']].replace(to_replace={'good':1,'poor':0,'no':np.nan})
kidney['classification'] = kidney['classification'].replace(to_replace={'ckd':1.0,'ckd\t':1.0,'notckd':0.0,'no':0.0})
kidney.rename(columns={'classification':'class'},inplace=True)

kidney['pe'] = kidney['pe'].replace(to_replace='good',value=0) # Not having pedal edema is good
kidney['appet'] = kidney['appet'].replace(to_replace='no',value=0)
kidney['cad'] = kidney['cad'].replace(to_replace='\tno',value=0)
kidney['dm'] = kidney['dm'].replace(to_replace={'\tno':0,'\tyes':1,' yes':1, '':np.nan})
kidney.drop('id',axis=1,inplace=True)


# In[ ]:


kidney.head()


# In[ ]:


# This helps us to count how many NaN are there in each column
len(kidney)-kidney.count()


# In[ ]:


# This shows number of rows with missing data
kidney.isnull().sum(axis = 1)


# In[ ]:


#This is a visualization of missing data in the dataset
sns.heatmap(kidney.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


# This shows number of complete cases and also removes all the rows with NaN
kidney2 = kidney.dropna()
print(kidney2.shape)


# In[ ]:


# Now our dataset is clean
sns.heatmap(kidney2.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


sns.heatmap(kidney2.corr())


# In[ ]:


# Counting number of normal vs. abnormal red blood cells of people having chronic kidney disease
print(kidney2.groupby('rbc').rbc.count().plot(kind="bar"))


# In[ ]:


#This plot shows the patient's sugar level compared to their ages
kidney2.plot(kind='scatter', x='age',y='su');
plt.show()


# In[ ]:


# Shows the maximum blood pressure having chronic kidney disease
print(kidney2.groupby('class').bp.max())


# In[ ]:


print(kidney2['dm'].value_counts(dropna=False))


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(kidney2.iloc[:,:-1], kidney2['class'], test_size=0.33, random_state=44, stratify= kidney2['class'])


# In[ ]:


print(X_train.shape)


# In[ ]:


y_train.value_counts()


# In[ ]:


rfc = RandomForestClassifier(random_state = 22)
rfc_fit = rfc.fit(X_train,y_train)


# In[ ]:


rfc_pred = rfc_fit.predict(X_test)


# In[ ]:


print(confusion_matrix(y_test,rfc_pred))


# In[ ]:


print(classification_report(y_test,rfc_pred))


# In[ ]:


accuracy_score( y_test, rfc_pred)


# In[ ]:


knn = KNeighborsClassifier(n_neighbors=1)


# In[ ]:


knn.fit(X_train,y_train)


# In[ ]:


pred = knn.predict(X_test)


# In[ ]:


print(confusion_matrix(y_test,pred))


# In[ ]:


print(classification_report(y_test,pred))


# In[ ]:


accuracy_score( y_test,pred)


# In[ ]:


logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)


# In[ ]:


predictions = logmodel.predict(X_test)


# In[ ]:


print(classification_report(y_test,predictions))


# In[ ]:


print(confusion_matrix(y_test,predictions))


# In[ ]:


accuracy_score( y_test, predictions)


# In[ ]:


feature_importances = pd.DataFrame(rfc.fit(X_train,y_train).feature_importances_, index = X_train.columns,
                                   columns=['importance']).sort_values('importance', ascending=False)
print(feature_importances)


# In[ ]:


kidney3 = kidney.drop(columns=['rbc', 'pc', 'sod', 'pot', 'pcv', 'wc', 'rc'])
kidney3. shape


# In[ ]:


kidney3.head()


# In[ ]:


kidney3.isnull().sum()


# In[ ]:


kidney3.mode()


# In[ ]:


# Fill in the NaNs with the mode for each column.   
kidney3_imp = kidney3.apply(lambda x:x.fillna(x.value_counts().index[0]))


# In[ ]:


kidney3_imp.isnull().sum()


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(kidney3_imp.iloc[:,:-1], kidney3_imp['class'],
                                                    test_size = 0.33, random_state=44,
                                                   stratify = kidney3_imp['class'])


# In[ ]:


y_train.value_counts()


# In[ ]:


rfc = RandomForestClassifier(random_state = 22)
rfc_fit = rfc.fit(X_train,y_train)


# In[ ]:


rfc_pred = rfc_fit.predict(X_test)


# In[ ]:


print(confusion_matrix(y_test,rfc_pred))


# In[ ]:


print(classification_report(y_test,rfc_pred))


# In[ ]:


accuracy_score( y_test, rfc_pred)


# In[ ]:


logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)


# In[ ]:


predictions = logmodel.predict(X_test)


# In[ ]:


print(classification_report(y_test,predictions))


# In[ ]:


print(confusion_matrix(y_test,predictions))


# In[ ]:


accuracy_score( y_test, rfc_pred)


# In[ ]:


dtree=DecisionTreeClassifier()


# In[ ]:


dtree.fit(X_train,y_train)


# In[ ]:


predictions=dtree.predict(X_test)


# In[ ]:


print(classification_report(y_test,predictions))


# In[ ]:


from IPython.display import Image
from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
import pydot
import os
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)/Graphviz2.38/bin/'

features = list(kidney3.columns[1:])
features


# In[ ]:


dot_data = StringIO()
export_graphviz(dtree, out_file = dot_data,feature_names = features,filled = True,rounded=True)

graph = pydot.graph_from_dot_data(dot_data.getvalue())
Image(graph[0].create_png())


# In[ ]:


rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(X_train,y_train)


# In[ ]:


rfc_pred = rfc.predict(X_test)


# In[ ]:


print(confusion_matrix(y_test,rfc_pred))


# In[ ]:


print(classification_report(y_test,rfc_pred))


# In[ ]:


accuracy_score( y_test, rfc_pred)


# In[ ]:


# Choosing a K Value.
# Let's go ahead and use the elbow method to pick a good k value.
error_rate = []

# Will take some time
for i in range(1,40):
    
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))


# In[ ]:


plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate,color='blue', linestyle='dashed', marker='o', markerfacecolor='red',markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')


# In[ ]:


knn = KNeighborsClassifier(n_neighbors=1)


# In[ ]:


knn.fit(X_train,y_train)


# In[ ]:


pred = knn.predict(X_test)


# In[ ]:


print(confusion_matrix(y_test,pred))


# In[ ]:


print(classification_report(y_test,pred))


# In[ ]:


accuracy_score( y_test,pred)

