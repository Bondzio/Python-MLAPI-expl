#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


report_df = pd.read_csv('../input/HR_comma_sep.csv')
report_df.head()


# In[ ]:


report_df.info()


# In[ ]:


sns.factorplot("left",data=report_df,kind='count',legend=True)


# In[ ]:


sns.regplot(x="satisfaction_level", y="left", data=report_df, order=1, truncate=True)


# In[ ]:


sns.regplot(x="last_evaluation", y="left", data=report_df, truncate=True)


# In[ ]:


sns.factorplot('number_project','left',data=report_df,aspect=2)


# In[ ]:


sns.factorplot("average_montly_hours", data=report_df[report_df.left == 1],kind='count',aspect=4,orient='h')


# In[ ]:


sns.factorplot('time_spend_company','left',data=report_df,aspect=2)


# In[ ]:


sns.factorplot('Work_accident','left',data=report_df,aspect=2)


# In[ ]:


sns.factorplot('promotion_last_5years','left',data=report_df,aspect=2)


# In[ ]:


sns.factorplot('sales','left',data=report_df,aspect=4)


# In[ ]:


sns.factorplot('salary','left',data=report_df,aspect=2)


# In[ ]:


report_df.head()


# In[ ]:


domain_df = pd.get_dummies(report_df.sales, prefix='domain')
domain_df.head()


# In[ ]:


salary_df = pd.get_dummies(report_df.salary, prefix='salary')
salary_df.head()


# In[ ]:


processed_df = pd.concat([report_df, domain_df, salary_df], axis=1)
processed_df.drop(['sales','salary'],axis=1,inplace=True)
processed_df.drop(['last_evaluation','time_spend_company','average_montly_hours'],axis=1,inplace=True)
processed_df.head()


# In[ ]:


result_df = processed_df['left']
processed_df.drop(['left'],axis=1,inplace=True)
from sklearn.model_selection import train_test_split
train_valid_X,test_X,train_valid_y,test_y = train_test_split(processed_df,result_df, test_size=0.3)
train_X , valid_X , train_y , valid_y = train_test_split( train_valid_X , train_valid_y , train_size = .7 )


# In[ ]:


from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import ExtraTreesClassifier

lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(train_X, train_y)
model = SelectFromModel(lsvc, prefit=True)
train_X_new = model.transform(train_X)
valid_X_new = model.transform(valid_X)
forest = ExtraTreesClassifier(random_state=0)
forest.fit(train_X_new, train_y)
# print('Train accuracy: ' + str(forest.score(train_X_new,train_y)))
print('Train accuracy: ' + str(forest.score(train_X_new,train_y))+'\nValidation accuracy: '+ str(forest.score(valid_X_new,valid_y)))


# In[ ]:


from sklearn.metrics import accuracy_score
test_X_new = model.transform(test_X)
test_Y = forest.predict(test_X_new)
print('Fianl Model accuracy: ' + str(accuracy_score(test_y, test_Y)))


# In[ ]:





# In[ ]:




