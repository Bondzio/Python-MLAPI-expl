#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv('../input/eval-lab-1-f464-v2/train.csv')
test = pd.read_csv('../input/eval-lab-1-f464-v2/test.csv')


# In[ ]:


df.head(10)


# ### Fill missing values; Drop duplicate rows

# In[ ]:


df.isnull().sum()


# In[ ]:


df['rating'].value_counts()


# In[ ]:


df = df.fillna(value = df.mean())
test = test.fillna(value=df.mean())


# In[ ]:


df.drop(['id'],axis=1,inplace=True)
df.drop_duplicates(inplace=True)


# In[ ]:


sns.boxplot(x="type", y="rating", data=df)


# In[ ]:


sns.regplot(x="feature11", y="rating", data=df)


# In[ ]:


df.corr()


# In[ ]:


# Compute the correlation matrix
corr = df.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(12, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.show()


# In[ ]:


X = df.drop('rating',axis=1).copy()
Y = df["rating"].copy()


# In[ ]:


X.head()


# In[ ]:


sns.distplot(df['feature11'],kde = False)


# In[ ]:


numerical_features = list(X.columns)
numerical_features.remove('type')
categorical_features = ["type"]


# ### Standard Scaling

# In[ ]:


from sklearn.preprocessing import StandardScaler
s = StandardScaler()
X[numerical_features]=s.fit_transform(X[numerical_features])
test[numerical_features]=s.transform(test[numerical_features])


# In[ ]:


#one hot encoding
X = pd.get_dummies(data = X, columns = ["type"])
test = pd.get_dummies(data=test,columns=['type'])


# ### Training and Test Data split

# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3,stratify=Y)


# In[ ]:


X_train.columns


# In[ ]:


Y_train.value_counts()


# In[ ]:


Y_test.value_counts()


# ### Fitting to various models

# In[ ]:


from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor,RandomForestClassifier,RandomForestRegressor,GradientBoostingRegressor,AdaBoostRegressor, AdaBoostClassifier,GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import ExtraTreeClassifier, ExtraTreeRegressor
from sklearn.ensemble import VotingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier,MLPRegressor
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.metrics import mean_squared_error


# In[ ]:


mlp = MLPRegressor(hidden_layer_sizes=(15,20,40,20,15),alpha=0.0001,batch_size=X_train.shape[0],random_state=100,max_iter=5000)
mlp.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,mlp.predict(X_test).round()))


# In[ ]:


rf = RandomForestClassifier(n_estimators = 2000, random_state=100)
rf.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,rf.predict(X_test)))


# In[ ]:


svc = SVC(C=1.0,kernel='rbf',degree=3,random_state=100)
svc.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,svc.predict(X_test)))


# In[ ]:


gdb = GradientBoostingRegressor(n_estimators=2000,random_state=100)
gdb.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,gdb.predict(X_test).round()))


# In[ ]:


gdbc = GradientBoostingClassifier(n_estimators=2000,random_state=100)
gdbc.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,gdbc.predict(X_test).round()))


# In[ ]:


adb = AdaBoostRegressor(n_estimators=2000,random_state=100)
adb.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,adb.predict(X_test).round()))


# In[ ]:


adbc = AdaBoostClassifier(n_estimators=2000,random_state=100)
adbc.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,adbc.predict(X_test).round()))


# In[ ]:


rfr =  RandomForestRegressor(n_estimators=2000, random_state=100)
rfr.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,rfr.predict(X_test).round()))


# In[ ]:


etc = ExtraTreesClassifier(n_estimators = 2000,random_state=504)
etc.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,etc.predict(X_test).round()))


# #### Extra Trees Regressor

# In[ ]:


# Best result so far on n_estimators = 2600,random_state = 120
# Second best on changing the above two values to n_estimators = 2400, random state = 504


# In[ ]:


etr = ExtraTreesRegressor(n_estimators = 2600,random_state=120)
etr.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,etr.predict(X_test).round()))


# In[ ]:


knnc = KNeighborsClassifier(15)
knnc.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,knnc.predict(X_test).round()))


# In[ ]:


knn = KNeighborsRegressor(15)
knn.fit(X_train,Y_train)
np.sqrt(mean_squared_error(Y_test,knn.predict(X_test).round()))


# ### Voting Classifier

# In[ ]:


# Trien mean and mode based classification


# In[ ]:


from scipy.stats import mode


# In[ ]:


rgrs = [('mlp',mlp),('rf',rfr),('adb',adb),('gdb',gdb),('knn',knn),('rfc',rf),]
weights =[4,10,2,0,3,5]
#weights = [1,1,1,1,1,1]
def voting_predict(X_train,Y_train,X_test,rgrs,weights):
    predictions = []
    for i in range(len(rgrs)):
        if(weights[i]!=0):
            predictions.append(weights[i]*rgrs[i][1].fit(X_train,Y_train).predict(X_test).round())
    predictions = np.array(predictions)
    mean_pred = np.sum(predictions,axis=0)/np.sum(weights)
    #mean_pred = mode(predictions,axis=0)
    #mean_pred = np.array(mean_pred)[0][0]
    return mean_pred.round()


# In[ ]:


mean_pred = voting_predict(X_train,Y_train,X_test,rgrs,weights)


# In[ ]:


np.sqrt(mean_squared_error(Y_test,mean_pred))


# ### Selecting best result out of Voting Classifier/ ExtraTreeRegressor

# In[ ]:


#pred = voting_predict(X,Y,(test.drop('id',axis=1)),rgrs,weights)
pred = etr.fit(X,Y).predict(test.drop('id',axis=1))


# In[ ]:


pred = pred.round()
pred = np.array(list(map(int,pred)))


# In[ ]:


sub_csv = pd.DataFrame({'id':test['id'],'rating':pred},columns = ['id','rating'])


# In[ ]:


sub_csv['rating'].value_counts()


# In[ ]:


sub_csv.to_csv('submission16.csv',index=False)


# ### Compare to last best result

# In[ ]:


#pd.read_csv('submission-15.csv')['rating'].value_counts()


# In[ ]:




