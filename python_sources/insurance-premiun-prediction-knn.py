#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


insurance_data = pd.read_csv('../input/insurance.csv')


# In[ ]:


insurance_data.info()


# In[ ]:


insurance_data.head()


# In[ ]:


insurance_data.duplicated().sum()


# In[ ]:


insurance_data.drop_duplicates(inplace = True)


# In[ ]:


insurance_data.duplicated().sum()


# In[ ]:


insurance_data["sex"].value_counts()


# In[ ]:


insurance_data["smoker"].value_counts()


# In[ ]:


insurance_data["region"].value_counts()


# In[ ]:


num_cols = insurance_data.select_dtypes(include = np.number).columns
cat_cols = insurance_data.select_dtypes(exclude = np.number).columns


# In[ ]:


one_hot_data = pd.get_dummies(insurance_data[cat_cols])


# In[ ]:


one_hot_data.head(3)


# In[ ]:


insurance_final = pd.concat([insurance_data[num_cols],one_hot_data],axis = 1)


# In[ ]:


insurance_final.head()


# In[ ]:


insurance_final.info()


# In[ ]:


Y = insurance_final["expenses"]
Y[0:3]


# In[ ]:


X = insurance_final.drop(columns = ["expenses"] )
X[0:3]


# In[ ]:


from sklearn import preprocessing


# In[ ]:


X = preprocessing.StandardScaler().fit(X).transform(X.astype(float))
X[0:5]


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split (X,Y,test_size=0.3, random_state=42)


# In[ ]:


X_train.shape


# In[ ]:


X_test.shape


# In[ ]:


from sklearn.neighbors import KNeighborsRegressor
from math import sqrt
from sklearn.metrics import mean_squared_error


# In[ ]:


length = round(sqrt(insurance_data.shape[0]))


# In[ ]:


length


# In[ ]:


rmse_dict = {}
rmse_list = []
for k in range(1,length+1):
    model = KNeighborsRegressor(n_neighbors = k).fit(X_train,Y_train)
    Y_predict = model.predict(X_test)
    rmse = sqrt(mean_squared_error(Y_test,Y_predict))
    rmse_dict.update({k:rmse})
    rmse_list.append(rmse)
    print("Rmse for k = {} is {}" .format(k,rmse))

    


# In[ ]:


key_min = min(rmse_dict.keys(), key=(lambda k: rmse_dict[k]))

print( "The miminum RMSE value is ",rmse_dict[key_min], "with k= ", key_min) 


# In[ ]:


elbow_curve = pd.DataFrame(rmse_list,columns = ['RMSE'])


# In[ ]:


elbow_curve.head()


# In[ ]:


elbow_curve.plot()


# In[ ]:




