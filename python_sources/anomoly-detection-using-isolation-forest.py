#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp


# In[ ]:


data=pd.read_csv('/home/harish/ML deco/Eduonix/creditcard.csv')


# In[ ]:


print(data.columns)


# In[ ]:


print(data.shape)


# In[ ]:


print(data.head())


# In[ ]:


print(data.describe())


# In[ ]:


data=data.sample(frac=0.1,random_state=1)


# In[ ]:


data.hist(figsize=(20,20))
plt.show()


# In[ ]:


Valid=data[data['Class']==0]
Fraud=data[data['Class']==1]

fraction=(len(Fraud))/(float)(len(Valid))

print (fraction)
print(len(Fraud))
print(len(Valid))


# In[ ]:


corremat=data.corr()

fig=plt.figure(figsize=(12,9))

sns.heatmap(corremat,vmax=0.8,square=True)
plt.show()


# In[ ]:


columns=data.columns.tolist()

columns=[c for c in columns if c not in ['Class']]

target="Class"

X=data[columns]

Y=data[target]

print(X.shape)
print(Y.shape)


# In[ ]:


from sklearn.metrics import classification_report,accuracy_score
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


# In[ ]:


state =1

classifiers={
    "Isolation Forest": IsolationForest(max_samples=len(X),contamination=fraction,random_state=state),
    "Local Outlier Factor": LocalOutlierFactor(n_neighbors=25,contamination=fraction)
}


# In[ ]:


#FIt the model

n_outliers=len(Fraud)

for i,(clf_name,clf) in enumerate(classifiers.items()):
    
    if clf_name == "Local Outlier Factor":
        y_pred=clf.fit_predict(X)
        scores_pred= clf.negative_outlier_factor_
    else:
        clf.fit(X)
        scores_pred=clf.decision_function(X)
        y_pred=clf.predict(X)
        
    y_pred[y_pred==1]=0
    y_pred[y_pred==-1]=1
    
    n_errors=(y_pred!=Y).sum()
    
    print('{}: {}'.format(clf_name,n_errors))
    print(accuracy_score(Y,y_pred))
    print(classification_report(Y,y_pred))


# In[ ]:




