#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  # visualization tool

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


data = pd.read_csv("/kaggle/input/red-wine-quality-cortez-et-al-2009/winequality-red.csv")
data.head()


# In[ ]:


data.info()


# In[ ]:


data.columns


# In[ ]:


data.rename(columns={'fixed acidity': 'fixed_acidity', 'volatile acidity': 'volatile_acidity','citric acid':'citric_acid',
                    'residual sugar':'residual_sugar','free sulfur dioxide':'free_sulfur_dioxide',
                     'total sulfur dioxide':'total_sulfur_dioxide'} ,inplace = True)


# In[ ]:


data.columns


# In[ ]:


df = pd.DataFrame(data, columns = [ 'alcohol', 'pH'] ) #histogram of alcohol and quality

df.hist() 
plt.show()


# In[ ]:


data.corr()


# In[ ]:


f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(data.corr(), annot = True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


data.pH.plot(kind = 'line', color = 'b',label = 'pH',linewidth=1,alpha = 0.5,grid = True,linestyle = ':')
data.alcohol.plot(color = 'y',label = 'alcohol',linewidth=1, alpha = 0.5,grid = True,linestyle = '-.')
plt.legend(loc='upper right')     
plt.xlabel('X Axis')             
plt.ylabel('Y Axis')
plt.title('Line Plot')           
plt.show()


# In[ ]:


data.chlorides.plot(kind = 'line', color = 'g',label = 'chlorides',linewidth=1,alpha = 0.5,grid = True,linestyle = ':')
data.volatile_acidity.plot(color = 'r',label = 'volatile_acidity',linewidth=1, alpha = 0.5,grid = True,linestyle = '-.')
plt.legend(loc='upper right')     
plt.xlabel('X Axis')             
plt.ylabel('Y Axis')
plt.title('Line Plot')           
plt.show()


# In[ ]:


# scatter plot between citric asid and density 
plt.scatter(data['density'], data['citric_acid'])
plt.xlabel("Density")
plt.ylabel("Citric Asid")
plt.show() 


# In[ ]:


plt.scatter(data['fixed_acidity'], data['volatile_acidity'],alpha = 0.5,color ='r')
plt.xlabel("Fixed Acidity")
plt.ylabel("Volatile Acidity")
plt.show()


# In[ ]:


plt.scatter(data['sulphates'], data['free_sulfur_dioxide'],alpha = 0.5,color ='g')
plt.xlabel("Sulphates")
plt.ylabel("Free Sulfur Dioxide")
plt.show()


# In[ ]:


data.residual_sugar.plot(kind = 'hist',bins = 50,figsize = (12,12),color = 'gray')
plt.xlabel("Residual Sugar")
plt.show()


# In[ ]:


data.plot.box(figsize = (15,15)) 
  
# individual attribute box plot 
plt.boxplot(data['quality']) 
plt.show() 


# In[ ]:


x = data['fixed_acidity'] > 13.5
data[x]


# In[ ]:


x = data['citric_acid'] > 0.75
data[x]


# In[ ]:


data[np.logical_and(data['residual_sugar'] > 7, data['free_sulfur_dioxide'] > 60 )]

