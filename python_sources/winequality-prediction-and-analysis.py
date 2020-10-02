#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


df = pd.read_csv("/kaggle/input/wine-quality/wineQualityWhites.csv")


# In[ ]:


df


# In[ ]:


df.describe()


# In[ ]:


df.info()


# In[ ]:


df.corr()


# In[ ]:


sns.heatmap(df.corr())


# In[ ]:


df['fixed.acidity'] = np.round(df['fixed.acidity'])
df['alcohol'] = np.round(df['alcohol'])
df['sulphates'] = np.round(df['sulphates']*100)
df['pH'] = np.round(df['pH'])
df['residual.sugar'] = np.round(df['residual.sugar'])
df['volatile.acidity'] = np.round(df['volatile.acidity']*100)
df['citric.acid'] = np.round(df['citric.acid']*100)
df['chlorides'] = np.round(df['chlorides']*100)
df['density'] = np.round(df['density']*10000)


# In[ ]:


plt.xlabel('quality')
plt.ylabel('citric acid')
plt.scatter(x=df['quality'],y=df['citric.acid'])


# In[ ]:


plt.xlabel('quality')
plt.ylabel('fixed acidity')
plt.scatter(x=df['quality'],y=df['fixed.acidity'])


# In[ ]:


sns.relplot(x="quality", y="pH", size="free.sulfur.dioxide", sizes=(50,300), data=df)


# In[ ]:


plt.xlabel('quality')
plt.ylabel('free.sulfur.dioxide')
plt.scatter(x=df['quality'],y=df['free.sulfur.dioxide'])


# In[ ]:


sns.relplot(x="quality", y="alcohol", size="pH", sizes=(50,100), data=df)


# In[ ]:


sns.violinplot(x="quality", y="fixed.acidity", hue="pH",data=df)


# In[ ]:


sns.violinplot(x="quality", y="free.sulfur.dioxide", hue="pH",data=df)


# In[ ]:


sns.violinplot(x="quality", y="total.sulfur.dioxide", hue="pH",data=df)


# In[ ]:


sns.violinplot(x="quality", y="citric.acid", hue="pH",data=df)


# In[ ]:


sns.violinplot(x="quality", y="density", hue="pH",data=df)


# In[ ]:


sns.violinplot(x="quality", y="residual.sugar", hue="pH",data=df)


# In[ ]:


sns.catplot(x="quality", kind="count",palette="ch:.30",data=df)


# In[ ]:


g = sns.PairGrid(df)
g.map_diag(sns.kdeplot)
g.map_offdiag(plt.scatter)


# In[ ]:


from sklearn.model_selection import train_test_split

train_set,test_set = train_test_split(df,train_size = 0.2,test_size=0.8,shuffle=True)
X_train = train_set[['alcohol','density','total.sulfur.dioxide','chlorides','residual.sugar','volatile.acidity','fixed.acidity']]
Y_train = train_set['quality']


# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import k_means
from sklearn.metrics import accuracy_score


# In[ ]:


X_test= test_set[['alcohol','density','total.sulfur.dioxide','chlorides','residual.sugar','volatile.acidity','fixed.acidity']]
Y_test = test_set['quality']


# In[ ]:


clf = LinearRegression()
clf.fit(X_train,Y_train)
predicted_Y = clf.predict(X_test)
predicted = np.round(predicted_Y)
accuracy_score(predicted,Y_test)


# In[ ]:


clf = LogisticRegression()
clf.fit(X_train,Y_train)
predicted_Y = clf.predict(X_test)
predicted = np.round(predicted_Y)
accuracy_score(predicted,Y_test)


# In[ ]:


clf = SVC(kernel='linear')
clf.fit(X_train,Y_train)
predicted_Y = clf.predict(X_test)
predicted = np.round(predicted_Y)
accuracy_score(predicted,Y_test)


# In[ ]:


clf = DecisionTreeRegressor()
clf.fit(X_train,Y_train)
predicted_Y = clf.predict(X_test)
predicted = np.round(predicted_Y)
accuracy_score(predicted,Y_test)


# In[ ]:


clf = RandomForestRegressor()
clf.fit(X_train,Y_train)
predicted_Y = clf.predict(X_test)
predicted = np.round(predicted_Y)
accuracy_score(predicted,Y_test)


# In[ ]:


clf = SVC(kernel='rbf',gamma='auto')
clf.fit(X_train,Y_train)
predicted_Y = clf.predict(X_test)
predicted = np.round(predicted_Y)
accuracy_score(predicted,Y_test)

