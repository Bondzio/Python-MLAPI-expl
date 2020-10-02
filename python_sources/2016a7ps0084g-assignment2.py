#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
get_ipython().system('{sys.executable} -m pip install sklearn')


# In[ ]:


import numpy as np
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns

#import sklearn.preprocessing as sk
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm


# In[ ]:


df_train_original = pd.read_csv("../input/train.csv" , sep = ",")
df_train = df_train_original


# In[ ]:


df_train.info()


# In[ ]:


df_train.head()


# # Data Preprocessing 

# In[ ]:


df_train.duplicated(keep ='first').any()
#no duplicates


# In[ ]:


#Replacing '?' with np.nan to make it readable by code.
df_temp = df_train.replace('?',np.nan)
df_dropped = df_temp.copy()

# Dropping columns that contain lot of null values.
df_dropped = df_dropped.drop('Fill',axis =1)
df_dropped = df_dropped.drop('Enrolled',axis = 1)
df_dropped = df_dropped.drop('MLU',axis =1)
df_dropped = df_dropped.drop('Reason',axis =1)
df_dropped = df_dropped.drop('Area',axis =1)
df_dropped = df_dropped.drop('State',axis =1)
df_dropped = df_dropped.drop('PREV',axis =1)
df_dropped = df_dropped.drop('ID',axis = 1)
df_dropped = df_dropped.drop('Teen',axis = 1)

# Dropping columns with multiple categorical entries.
df_dropped = df_dropped.drop('COB SELF',axis = 1)
df_dropped = df_dropped.drop('COB MOTHER',axis = 1)
df_dropped = df_dropped.drop('COB FATHER',axis = 1)
df_dropped = df_dropped.drop('MOC',axis = 1)
df_dropped = df_dropped.drop('MIC',axis = 1)
df_dropped = df_dropped.drop('MSA',axis = 1)
df_dropped = df_dropped.drop('REG',axis = 1)
df_dropped = df_dropped.drop('MOVE',axis = 1)
df_dropped = df_dropped.drop('Live',axis = 1)

df_dropped = df_dropped.drop('Schooling',axis =1)
df_dropped = df_dropped.drop('Detailed',axis =1)
df_dropped = df_dropped.drop('Married_Life',axis =1)
df_dropped = df_dropped.drop('Hispanic',axis =1)
df_dropped = df_dropped.drop('Worker Class',axis =1)


df_dropped = df_dropped.drop('Cast',axis =1)


df_dropped.head()


# In[ ]:


df_dropped = df_dropped.fillna(df_dropped.mode().iloc[0])


# In[ ]:


df_dropped.head()


# # Visualization

# In[ ]:


f, ax = plt.subplots(figsize=(10, 8))
corr=df_dropped.corr()
sns.heatmap(corr, annot=True, fmt=".1f")


# In[ ]:


# Dropping Weaks
df_dropped = df_dropped.drop('Weaks',axis = 1)

df_labeled = df_dropped.copy()


# In[ ]:


df_dropped.info()


# # Encoding

# In[ ]:


df_encoded_train = pd.get_dummies(df_dropped, columns = ['Sex','Full/Part','Tax Status'
                                                  ,'Summary','Citizen'])#,'Cast 
#df_encoded = pd.get_dummies(df_dropped, columns = ['Worker Class','Sex','Full/Part','Tax Status',
#                                                  'Summary','Live','Citizen'])
df_encoded_train.head()


# In[ ]:


df_encoded_train.info()


# # Feature Scaling

# In[ ]:


sampling_encoded_1 = df_encoded_train[df_encoded_train['Class']==1]
sampling_encoded_0 = df_encoded_train[df_encoded_train['Class']==0]


# In[ ]:


sampled_data = sampling_encoded_0.sample(frac=0.07)


# In[ ]:


df_sampled = pd.concat([sampling_encoded_1,sampled_data], ignore_index=True)


# In[ ]:


df_sampled.info()


# In[ ]:


# Dropping class
y = df_sampled['Class']
X = df_sampled.drop('Class',axis =1)
X.head()


# In[ ]:


# Test train split
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.20, random_state=42)


# In[ ]:


from sklearn import preprocessing
#Performing Min_Max Normalization
min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(X_train)
X_train = pd.DataFrame(np_scaled)
np_scaled_val = min_max_scaler.transform(X_val)
X_val = pd.DataFrame(np_scaled_val)
X_train.head()


# # Naive Bayes

# In[ ]:


np.random.seed(42)


# In[ ]:


from sklearn.naive_bayes import GaussianNB as NB
nb = NB()
nb.fit(X_train,y_train)
nb.score(X_val,y_val)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report,accuracy_score

y_pred_NB = nb.predict(X_val)
print(confusion_matrix(y_val, y_pred_NB))


# In[ ]:


# calculate accuracy
from sklearn import metrics
print(metrics.accuracy_score(y_val, y_pred_NB))


# In[ ]:


print(classification_report(y_val, y_pred_NB))


# In[ ]:


from sklearn.metrics import roc_auc_score

roc_auc_score(y_val, y_pred_NB)


# # Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression


# In[ ]:


lg = LogisticRegression(solver = 'liblinear', C = 1, multi_class = 'ovr', random_state = 42)
lg.fit(X_train,y_train)
#lg.score(X_val,y_val)


# In[ ]:


lg = LogisticRegression(solver = 'lbfgs', C = 8, multi_class = 'multinomial', random_state = 42)
lg.fit(X_train,y_train)
lg.score(X_val,y_val)


# In[ ]:


y_pred_LR = lg.predict(X_val)
print(confusion_matrix(y_val, y_pred_LR))


# In[ ]:


# calculate accuracy
from sklearn import metrics
print(metrics.accuracy_score(y_val, y_pred_LR))


# In[ ]:


print(classification_report(y_val, y_pred_LR))


# In[ ]:


from sklearn.metrics import roc_auc_score

roc_auc_score(y_val, y_pred_LR)


# # Decision Tree

# In[ ]:


from sklearn.tree import DecisionTreeClassifier


# In[ ]:


from sklearn.tree import DecisionTreeClassifier

train_acc = []
test_acc = []
for i in range(1,15):
    dTree = DecisionTreeClassifier(max_depth=i)
    dTree.fit(X_train,y_train)
    acc_train = dTree.score(X_train,y_train)
    train_acc.append(acc_train)
    acc_test = dTree.score(X_val,y_val)
    test_acc.append(acc_test)


# In[ ]:


plt.figure(figsize=(10,6))
train_score,=plt.plot(range(1,15),train_acc,color='blue', linestyle='dashed', marker='o',
         markerfacecolor='green', markersize=5)
test_score,=plt.plot(range(1,15),test_acc,color='red',linestyle='dashed',  marker='o',
         markerfacecolor='blue', markersize=5)
plt.legend( [train_score, test_score],["Train Accuracy", "Validation Accuracy"])
plt.title('Accuracy vs Max Depth')
plt.xlabel('Max Depth')
plt.ylabel('Accuracy')


# In[ ]:


from sklearn.tree import DecisionTreeClassifier

train_acc = []
test_acc = []
for i in range(2,30):
    dTree = DecisionTreeClassifier(max_depth = 9, min_samples_split=i, random_state = 42)
    dTree.fit(X_train,y_train)
    acc_train = dTree.score(X_train,y_train)
    train_acc.append(acc_train)
    acc_test = dTree.score(X_val,y_val)
    test_acc.append(acc_test)


# In[ ]:


plt.figure(figsize=(10,6))
train_score,=plt.plot(range(2,30),train_acc,color='blue', linestyle='dashed', marker='o',
         markerfacecolor='green', markersize=5)
test_score,=plt.plot(range(2,30),test_acc,color='red',linestyle='dashed',  marker='o',
         markerfacecolor='blue', markersize=5)
plt.legend( [train_score, test_score],["Train Accuracy", "Validation Accuracy"])
plt.title('Accuracy vs min_samples_split')
plt.xlabel('Max Depth')
plt.ylabel('Accuracy')


# In[ ]:


dTree = DecisionTreeClassifier(max_depth=9, min_samples_split = 27 , random_state = 42)
dTree.fit(X_train,y_train)
dTree.score(X_val,y_val)


# In[ ]:


y_pred_DT = dTree.predict(X_val)
print(confusion_matrix(y_val, y_pred_DT))


# In[ ]:


from sklearn.metrics import roc_auc_score

roc_auc_score(y_val,y_pred_DT)


# # Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


score_train_RF = []
score_test_RF = []

for i in range(1,18,1):
    rf = RandomForestClassifier(n_estimators=i, random_state = 42)
    rf.fit(X_train, y_train)
    sc_train = rf.score(X_train,y_train)
    score_train_RF.append(sc_train)
    sc_test = rf.score(X_val,y_val)
    score_test_RF.append(sc_test)


# In[ ]:


plt.figure(figsize=(10,6))
train_score,=plt.plot(range(1,18,1),score_train_RF,color='blue', linestyle='dashed', marker='o',
         markerfacecolor='green', markersize=5)
test_score,=plt.plot(range(1,18,1),score_test_RF,color='red',linestyle='dashed',  marker='o',
         markerfacecolor='blue', markersize=5)
plt.legend( [train_score,test_score],["Train Score","Test Score"])
plt.title('Fig4. Score vs. No. of Trees')
plt.xlabel('No. of Trees')
plt.ylabel('Score')


# In[ ]:


rf = RandomForestClassifier(n_estimators=17, random_state = 42)
rf.fit(X_train, y_train)
rf.score(X_val,y_val)


# In[ ]:


y_pred_RF = rf.predict(X_val)
confusion_matrix(y_val,y_pred_RF)


# In[ ]:


print(classification_report(y_val, y_pred_RF))


# In[ ]:


from sklearn.metrics import roc_auc_score

roc_auc_score(y_val, y_pred_RF)


# # Ada Boosting

# In[ ]:


from sklearn.ensemble import AdaBoostClassifier
# Create adaboost classifer object
abc = AdaBoostClassifier(n_estimators=50,
                         learning_rate=1)
# Train Adaboost Classifer
model = abc.fit(X_train, y_train)

#Predict the response for test dataset
y_pred_boost = model.predict(X_val)


# In[ ]:


from sklearn.metrics import accuracy_score
# Accuracy
accuracy_score( y_val,y_pred_boost)


# In[ ]:


X_val.head()


# In[ ]:


from sklearn.metrics import roc_auc_score

roc_auc_score(y_val, y_pred_boost)


# In[ ]:


from sklearn.ensemble import BaggingClassifier
from sklearn import tree
model = BaggingClassifier(tree.DecisionTreeClassifier(random_state=1))
model.fit(X_train, y_train)
model.score(X_val,y_val)


# In[ ]:


y_pred_bagging = model.predict(X_val)


# In[ ]:


accuracy_score(y_val,y_pred_bagging)


# # Testing on test.csv

# In[ ]:


df_test_original = pd.read_csv("../input/test.csv" , sep = ",")
df_test = df_test_original


# In[ ]:


df_test.head()


# In[ ]:


df_test.info()


# In[ ]:


df_test.duplicated(keep ='first').any()


# In[ ]:


#Replacing '?' with np.nan to make it readable by code.
df_temp_test = df_test.replace('?',np.nan)
df_dropped_test = df_temp_test.copy()
# Dropping columns will lot of null values.
df_dropped_test = df_dropped_test.drop('Fill',axis =1)
df_dropped_test = df_dropped_test.drop('Enrolled',axis = 1)
df_dropped_test = df_dropped_test.drop('MLU',axis =1)
df_dropped_test = df_dropped_test.drop('Reason',axis =1)
df_dropped_test = df_dropped_test.drop('Area',axis =1)
df_dropped_test = df_dropped_test.drop('State',axis =1)
df_dropped_test = df_dropped_test.drop('PREV',axis =1)
df_dropped_test = df_dropped_test.drop('ID',axis = 1)
df_dropped_test = df_dropped_test.drop('Teen',axis = 1)

# Dropping columns with multiple categorical entries.

df_dropped_test = df_dropped_test.drop('COB SELF',axis = 1)
df_dropped_test = df_dropped_test.drop('COB MOTHER',axis = 1)
df_dropped_test = df_dropped_test.drop('COB FATHER',axis = 1)
df_dropped_test = df_dropped_test.drop('MOC',axis = 1)
df_dropped_test = df_dropped_test.drop('MIC',axis = 1)
df_dropped_test = df_dropped_test.drop('MSA',axis = 1)
df_dropped_test = df_dropped_test.drop('REG',axis = 1)
df_dropped_test = df_dropped_test.drop('MOVE',axis = 1)
df_dropped_test = df_dropped_test.drop('Live',axis = 1)

df_dropped_test = df_dropped_test.drop('Schooling',axis =1)
df_dropped_test = df_dropped_test.drop('Detailed',axis =1)
df_dropped_test = df_dropped_test.drop('Married_Life',axis =1)
df_dropped_test = df_dropped_test.drop('Hispanic',axis =1)
df_dropped_test = df_dropped_test.drop('Worker Class',axis =1)

df_dropped_test = df_dropped_test.drop('Cast',axis =1)


df_dropped_test.head()


# In[ ]:


df_dropped_test = df_dropped_test.fillna(df_dropped_test.mode().iloc[0])


# In[ ]:


df_dropped_test.info()


# In[ ]:


f, ax = plt.subplots(figsize=(10, 8))
corr=df_dropped_test.corr()
sns.heatmap(corr, annot=True, fmt=".1f")


# In[ ]:


df_dropped_test = df_dropped_test.drop('Weaks',axis =1)


# In[ ]:


df_labeled_test = df_dropped_test.copy()


# In[ ]:


df_encoded = pd.get_dummies(df_dropped_test, columns = ['Sex','Full/Part','Tax Status'
                                                  ,'Summary','Citizen'])#,'Married_Life',,'Cast 
#df_encoded = pd.get_dummies(df_dropped, columns = ['Worker Class','Sex','Full/Part','Tax Status',
#                                                  'Summary','Live','Citizen'])
df_encoded.head()


# In[ ]:


df_encoded.info()


# In[ ]:


df_encoded.head()


# In[ ]:


min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(X)
X1 = pd.DataFrame(np_scaled)
X1.head()


# In[ ]:


min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(X)
X1 = pd.DataFrame(np_scaled)
X1.head()


# In[ ]:


#dTree1 = DecisionTreeClassifier(max_depth=7, random_state = 42)
#dTree1.fit(X1,y)
#rf = RandomForestClassifier(n_estimators=12, random_state = 42)
#rf.fit(X1, y)

abc = AdaBoostClassifier(n_estimators=50,
                         learning_rate=1)
adaboost = abc.fit(X1, y)


# In[ ]:


df_encoded.info()


# In[ ]:


min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(df_encoded)
df_encoded1 = pd.DataFrame(np_scaled)
df_encoded1.head()


# In[ ]:


predictions = adaboost.predict(df_encoded1)


# In[ ]:


submit = pd.read_csv("../input/test.csv" , sep = ",")
colID = submit[['ID']]


# In[ ]:


res = colID.assign(Class = predictions)


# In[ ]:


res['ID'] = res['ID'].astype(int)


# In[ ]:


res.to_csv("Submission.csv",index = False)


# In[ ]:


res.head()


# In[ ]:


from IPython.display import HTML
import pandas as pd
import numpy as np
import base64

def create_download_link(df, title = "Download CSV file", filename = "data.csv"):  
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload,title=title,filename=filename)
    return HTML(html)

create_download_link(res)


# In[ ]:




