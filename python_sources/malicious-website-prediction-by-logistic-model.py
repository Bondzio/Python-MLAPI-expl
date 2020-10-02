#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
print(os.listdir("../input"))


# In[ ]:


df = pd.read_csv('../input/malicious-and-benign-websites/dataset.csv')
df.head(10)


# **Discover the dataset**

# In[ ]:


df.shape


# In[ ]:


df.dtypes


# In[ ]:


print(df.isnull().sum())
df[pd.isnull(df).any(axis=1)]


# CONTENT_LENGTH has 812 NaN.

# In[ ]:


df = df.interpolate()
print(df.isnull().sum())


# In[ ]:


#Charset
df['CHARSET'].unique()
df['CHARSET']=np.where(df['CHARSET'] =='iso-8859-1', 'ISO-8859-1', df['CHARSET'])
df['CHARSET']=np.where(df['CHARSET'] =='utf-8', 'UTF-8', df['CHARSET'])


# In[ ]:


#WHOIS_COUNTRY 
df['WHOIS_COUNTRY'].unique()
df['WHOIS_COUNTRY']=np.where(df['WHOIS_COUNTRY'] =='United Kingdom', 'UK', df['WHOIS_COUNTRY'])
df['WHOIS_COUNTRY']=np.where(df['WHOIS_COUNTRY'] =="[u'GB'; u'UK']", 'UK', df['WHOIS_COUNTRY'])
df['WHOIS_COUNTRY']=np.where(df['WHOIS_COUNTRY'] =='United Kingdom', 'UK', df['WHOIS_COUNTRY'])
df['WHOIS_COUNTRY']=np.where(df['WHOIS_COUNTRY'] =='us', 'US', df['WHOIS_COUNTRY'])
df['WHOIS_COUNTRY']=np.where(df['WHOIS_COUNTRY'] =='se', 'SE', df['WHOIS_COUNTRY'])
df['WHOIS_COUNTRY']=np.where(df['WHOIS_COUNTRY'] =='ru', 'RU', df['WHOIS_COUNTRY'])


# In[ ]:


df.describe(include='all')


# In[ ]:


#How many URLs are malicious?
df['Type'].value_counts()


# In[ ]:


df.groupby('Type').mean()


# In[ ]:


df.groupby('Type').median()


# In[ ]:


df.groupby(['CHARSET','Type']).count()


# In[ ]:


df.groupby(['WHOIS_COUNTRY','Type']).count()


# **Find important factors**

# In[ ]:


correlation = df.corr()
plt.figure(figsize = (20, 20))
sns.set(font_scale = 2)
sns.heatmap(correlation, annot = True, annot_kws = {'size': 15}, cmap = 'Blues')


# In[ ]:


#Type x URL Length
plt.figure(figsize=(5, 5))
sns.boxenplot(data = df, x="Type", y="URL_LENGTH",
              color="b", scale="linear")


# In[ ]:


#Type x Number of Special Characters
plt.figure(figsize=(5, 5))
sns.boxenplot(data = df, x="Type", y="NUMBER_SPECIAL_CHARACTERS",
              color="g", scale="linear")


# In[ ]:


#Type x Content Length
plt.figure(figsize=(5, 5))
sns.boxenplot(data = df, x="Type", y="CONTENT_LENGTH",
              color="y", scale="linear")


# In[ ]:


#Type x DNS Query Times
plt.figure(figsize=(5, 5))
sns.boxenplot(data = df, x="Type", y="DNS_QUERY_TIMES",
              color="y", scale="linear")


# **Logistic Regression**

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

X = df[['URL_LENGTH', 'NUMBER_SPECIAL_CHARACTERS','DNS_QUERY_TIMES']]
y = df['Type']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)


# In[ ]:


logistic_regression= LogisticRegression()
logistic_regression.fit(X_train,y_train)
y_pred=logistic_regression.predict(X_test)

print (X_test) 
print (y_pred)


# In[ ]:


print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logistic_regression.score(X_test, y_test)))


# In[ ]:


from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

logit_roc_auc = roc_auc_score(y_test, logistic_regression.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logistic_regression.predict_proba(X_test)[:,1])

plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()


# Since AUC = 0.61, this model is predictable.
