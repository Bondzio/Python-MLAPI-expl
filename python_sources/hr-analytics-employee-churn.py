#!/usr/bin/env python
# coding: utf-8

# In[9]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt
import seaborn as sb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import (confusion_matrix,
                            accuracy_score,
                            f1_score,
                            precision_score,
                            recall_score)

from glob import glob
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

print(glob('../input/*'))

# Any results you write to the current directory are saved as output.


# In[6]:


HR_df = pd.read_csv('../input/HR_comma_sep.csv')


# In[10]:


print("nrows = %d, ncols = %d" % HR_df.shape)
print(HR_df.info())


# ### Convert categorical features from numerical to categorical data type

# In[11]:


HR_df.Work_accident = HR_df.Work_accident.astype('category')
HR_df.promotion_last_5years = HR_df.promotion_last_5years.astype('category')
HR_df.sales = HR_df.sales.astype('category')
HR_df.salary = HR_df.salary.astype('category')
HR_df.left = HR_df.left.astype('category')


# In[12]:


sb.factorplot(data=HR_df, y='sales', x='satisfaction_level', kind='bar',
             size=10, aspect=1);


# In[13]:


sb.factorplot(data=HR_df, y='salary', x='satisfaction_level', kind='bar',
             size=5, aspect=2);


# In[14]:


sales_dept = HR_df[HR_df.sales=='sales']
sb.set_context('poster')
sb.lmplot(data=sales_dept, y='last_evaluation', x='satisfaction_level', hue='left',
          fit_reg=False, size=10, aspect=1);


# In[15]:


sb.violinplot(data=HR_df, x='left', y='satisfaction_level');


# ## Splitting data into training and testing sets

# In[16]:


print(HR_df.dtypes)


# In[17]:


cat_cols = HR_df.select_dtypes(exclude=[np.number]).columns.tolist()


# In[18]:


HR_dummy = HR_df.copy()

for c in cat_cols:
    HR_dummy = pd.concat([HR_dummy, 
                          pd.get_dummies(HR_dummy[c].replace(1, 'YES').replace(0, 'NO'),
                                         prefix=c)], 
                         axis=1).drop(c, axis=1)
    
HR_dummy.drop('left_NO', axis=1, inplace=True)


# In[19]:


HR_dummy.columns


# In[20]:


X = HR_dummy.drop('left_YES', axis=1)
y = HR_dummy['left_YES']

print(y.value_counts(normalize=True))


# In[21]:


result = cross_val_score(X=X, y=y,
                         cv=5,
                         estimator=RandomForestClassifier())


# In[22]:


print(np.mean(result))


# In[23]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=20)


# In[24]:


RF = RandomForestClassifier()
RF.fit(X_train, y_train)


# In[25]:


y_pred = RF.predict(X_test)


# In[26]:


#cm = pd.DataFrame({'True': y_test, 'Predicted': y_pred}).pivot()

cm = confusion_matrix(y_pred=y_pred, y_true=y_test)

sb.heatmap(cm, annot=True, fmt='d', linewidths=1)
print(f'Accuracy (% of correct hits): {accuracy_score(y_test, y_pred):.3f} %')
print(f'F1 score: {f1_score(y_test, y_pred):.3f}')
print(f'Precision score (tp/(tp+fp)): {precision_score(y_test, y_pred):.3f} %')
print(f'Recall score (tp/(tp+fn)): {recall_score(y_test, y_pred):.3f} %')

