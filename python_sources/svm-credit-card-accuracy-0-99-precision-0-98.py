#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Author Felipe Cruz --- GitHub @F-Cruz
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


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv('/kaggle/input/creditcardfraud/creditcard.csv')


# In[ ]:


df.head()


# In[ ]:


df_target = pd.DataFrame(df['Class'])


# In[ ]:


df_target.info()


# In[ ]:


df_fit = pd.DataFrame(df.iloc[:, 1:29])


# In[ ]:


df_fit.info()


# In[ ]:


from sklearn.svm import SVC


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(df_fit, np.ravel(df_target), test_size = 0.3, random_state=101)


# In[ ]:


model = SVC()


# In[ ]:


model.fit(X_train, y_train)


# In[ ]:


from sklearn.metrics import accuracy_score,confusion_matrix,classification_report


# In[ ]:


predictions = model.predict(X_test)


# In[ ]:


print(confusion_matrix(y_test,predictions))
print('\n')
print(accuracy_score(y_test,predictions))
print('\n')
print(classification_report(y_test,predictions))


# In[ ]:




