#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# First of all , we need to read our csv file.

# In[ ]:


data = pd.read_csv('../input/biomechanical-features-of-orthopedic-patients/column_2C_weka.csv')


# In[ ]:


data.describe()


# In[ ]:


data.columns


# In[ ]:


data.info()


# In[ ]:


data.shape


# In[ ]:


data.head(10)


# Plotting scatter 
# 
# green : normal
# 
# red : abnormal 
# 
# c : color
# 
# figsize = figure size
# 
# diagonal = histogram of each features
# 
# alpha = opacity
# 
# s = size of marker
# 
# marker = marker type
# 
# 

# In[ ]:


color_list = ['red' if i == 'Abnormal' else 'green' for i in data.loc[:,'class']]

pd.plotting.scatter_matrix(data.loc[:,data.columns != 'class'],
                          c = color_list,
                          figsize=[15,15],
                          diagonal='hist',
                          alpha =0.5,
                          s=200,
                          marker='*',
                          edgecolor='black')

plt.show()


# Let's checking how many normal and abnormal in this class.

# In[ ]:


data.loc[:,'class'].value_counts()


# Also we can learn this information by using seaborn library.

# In[ ]:


sns.countplot(x='class',data=data)


# In[ ]:


data_with_class_equals_normal = data[data['class']=='Abnormal']
data_with_class_equals_normal


# In[ ]:


x = data_with_class_equals_normal['pelvic_incidence'].values.reshape(-1,1)
y = data_with_class_equals_normal['sacral_slope'].values.reshape(-1,1)

#Scatter
plt.figure(figsize=[15,15])
plt.scatter(x,y,color='blue')
plt.xlabel('Pelvic Incidence')
plt.ylabel('Sacral Slope')

plt.show()


#     Now we have a data to make linear regression . In regression problems target value is continuosly varying variable such as price of house or sacral_slope .
#     Lets fit line into this points.

# In[ ]:


from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()

# predict space

predict_space = np.linspace(min(x),max(x)).reshape(-1,1)

# Fitting

lin_reg.fit(x,y)

#Predicting

predicted = lin_reg.predict(predict_space)

# R^2

r2 = lin_reg.score(x,y)

print('R^2 Score: ',r2)


# In[ ]:


# Plotting regression line


plt.plot(predict_space,predicted,color="black",linewidth=4)
plt.scatter(x,y)
plt.xlabel('Pelvic Incidence')
plt.ylabel('Sacral Slope')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




