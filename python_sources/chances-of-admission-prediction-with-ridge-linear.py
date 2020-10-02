#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


df=pd.read_csv('../input/graduate-admissions/Admission_Predict.csv')


# In[ ]:


df.describe


# In[ ]:


df.columns


# In[ ]:


df.describe(include = 'all')


# Serial number isnt a crieteria for classfication.

# In[ ]:


df=df.drop(['Serial No.'], axis = 1)


# In[ ]:


df.columns


# A relative mapping of the basis of classifications vs the result

# In[ ]:


f, (ax1,ax2,ax3) = plt.subplots(1,3, sharey=True, figsize=(15,10))
ax1.scatter(df['GRE Score'], df['Chance of Admit '],color='red')
ax1.set_title('Chance of Admit vs GRE Score')
ax2.scatter(df['TOEFL Score'], df['Chance of Admit '],color='yellow')
ax2.set_title('Chance of Admit vs TOEFL Score')
ax3.scatter(df['CGPA'],df['Chance of Admit '],color='green')
ax3.set_title('Chance of Admit vs CGPA')

plt.show()


# Splitting dataset and predicting results

# In[ ]:


df.columns


# In[ ]:


y=df['Chance of Admit ']
X=df.drop(['Chance of Admit '], axis = 1)
x_train,x_test,y_train,y_test = train_test_split(X,y, test_size = 0.2, random_state = 365)



from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Ridge

reg=Ridge()


# In[ ]:


reg.fit(x_train,y_train)


# In[ ]:


res=reg.predict(x_test)


# In[ ]:


reg.score(x_train,y_train)


# In[ ]:


reg.intercept_


# Mapping of results

# In[ ]:


reg_summary = pd.DataFrame(X.columns.values, columns = ['Features'])
reg_summary['Weights'] = reg.coef_
reg_summary


# In[ ]:


print(res)
print(y_test)


# In[ ]:


plt.scatter(y_test, res,color='green')
plt.xlabel('Exact values', size = 10)
plt.ylabel('Predicted values', size = 10)
plt.show()


# #  The score of 80% using Ridge Regression is quite acceptable as a solution.
