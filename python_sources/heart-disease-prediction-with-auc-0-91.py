#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
df=pd.read_csv('/kaggle/input/heart-disease-uci/heart.csv')


# 

# In[ ]:


df.info()


# In[ ]:


df.head()


# In[ ]:


df.target.value_counts()


# ##**FEATURE SELECTION**

# In[ ]:


corrmat=df.corr()
top_corr_features=corrmat.index
plt.figure(figsize=(20,20))
sns.heatmap(df[top_corr_features].corr(),annot=True)


# In[ ]:



plt.figure(figsize=(20,20))
df.hist()


# In[ ]:


dataset=pd.get_dummies(df,columns=['sex','cp','fbs','restecg','exang','slope','ca','thal'])


# In[ ]:


dataset


# In[ ]:


y=dataset['target']
x=dataset.drop(['target'],axis=1)


# In[ ]:


from sklearn.model_selection import cross_val_score
knn_score=[]
from sklearn.neighbors import KNeighborsClassifier
for k in range(1,21):
    knn_classifier=KNeighborsClassifier(n_neighbors=k)
    score=cross_val_score(knn_classifier,x,y,cv=10)
    knn_score.append(score.mean())


# In[ ]:


plt.plot([k for k in range(1,21)],knn_score,color='red')
for i in range(1,21):
    plt.text(i,knn_score[i-1],(i,knn_scores[i-1]))
plt.xticks([i for i in range(1,21)])


# In[ ]:


knn_score[11]


#  * ACCURACY LOW WONDERING WHY...NOTICE THE DAATSET WE DESN'T HAVE APPLIED STANDARD SCALER AS VARIOUS VALUES  ARE AT VERY DIFFERENT MAGNITUDE*

# In[ ]:


knn_classifier=KNeighborsClassifier(n_neighbors=12)
score=cross_val_score(knn_classifier,x,y,cv=10)
score.mean()


# using random forest as it most suits are condition we didn't have to use standard scaler in it.

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #for plotting
from sklearn.ensemble import RandomForestClassifier #for the model
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz #plot tree
from sklearn.metrics import roc_curve, auc #for model evaluation
from sklearn.metrics import classification_report #for model evaluation
from sklearn.metrics import confusion_matrix #for model evaluation
from sklearn.model_selection import train_test_split #for data splitting
import eli5 #for purmutation importance
from eli5.sklearn import PermutationImportance
import shap #for SHAP values
from pdpbox import pdp, info_plots #for partial plots
np.random.seed(123) #ensure reproducibility


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(dataset.drop('target', 1), dataset['target'], test_size = .2, random_state=10)


# In[ ]:


model = RandomForestClassifier(max_depth=5)
model.fit(X_train, y_train)


# for more accuracy use can use grid_search_cv or randominzed_search_cv

# In[ ]:


y_predict = model.predict(X_test)
y_pred_quant = model.predict_proba(X_test)[:, 1]
y_pred_bin = model.predict(X_test)


# In[ ]:


confusion_matrix = confusion_matrix(y_test, y_pred_bin)
confusion_matrix


# let's see AUC

# In[ ]:


fpr, tpr, thresholds = roc_curve(y_test, y_pred_quant)


# In[ ]:


auc(fpr,tpr)


# **PARTIAL DEPENDENCE PLOTS CAN BE FUTHER USED TO DRAW SOME INSIGHTS FROM DATA **

# In[ ]:




