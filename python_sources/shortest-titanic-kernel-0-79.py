#!/usr/bin/env python
# coding: utf-8

# Original kernel: https://www.kaggle.com/pavlofesenko/shortest-titanic-kernel-0-78468

# In[ ]:


import pandas as p,sklearn.ensemble as s;a=p.concat([p.read_csv(f"../input/{f}.csv").fillna(-1) for f in['train','test']]);n=891;b=p.concat((p.get_dummies(a.select_dtypes('object')),a[['Age','Fare']]),axis=1);b={0:b.iloc[:n,:],1:b.iloc[n::,:]};p.concat((p.Series(range(n+1,1310),name='PassengerId'),p.Series(s.RandomForestClassifier().fit(b[0],a['Survived'].iloc[:891]).predict(b[1]).astype(int),name='Survived')),axis=1).to_csv('s.csv',index=False)

