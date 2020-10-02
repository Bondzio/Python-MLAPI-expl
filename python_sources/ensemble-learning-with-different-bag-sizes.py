#!/usr/bin/env python
# coding: utf-8

# * Author: Syed Sheheryar
# * Idea  : To demonstrate the ensemble learning methods with to choose optimal bagging size. 

# In[1]:


#Import libraries
import pandas                                            as pd
import numpy                                             as np

from sklearn.preprocessing import MinMaxScaler
from sklearn               import model_selection
from sklearn.ensemble      import BaggingClassifier      as bagclf
from sklearn.tree          import DecisionTreeClassifier as dt


# In[2]:


df = pd.read_csv('../input/add.csv' ,usecols=list(range(0,1560)), index_col=False )


# In[3]:


df.shape


# In[4]:


df.drop(axis=1, columns=['Unnamed: 0'], inplace=True )


# In[5]:


df.dropna(inplace=True)
df = df.applymap(lambda val: np.nan if str(val).strip() == '?' else val)
df.fillna(0, inplace=True)


# In[6]:


df.shape


# In[7]:


df.tail()


# In[8]:


df.info()


# In[9]:


#Checking for classes; two classes we have.
df.iloc[:,1558].unique()


# In[10]:


#Converting the values  'ad' to 1 and 'nonad' to 0 
df.iloc[:,1558]= np.where(df.iloc[:,1558]=='ad.', 1, 0)


# In[11]:


# Spliting into data and labels
X  = df.iloc[:,0:1558]
y  = df.iloc[:,1558]


# In[12]:


scaler = MinMaxScaler()
scaler.fit(X)
X = scaler.transform(X)


# In[13]:


y.unique()


# In[14]:


#Declare variables
seed      = 0
num_trees = 100
#instantiate the kfold splitter
kfold = model_selection.KFold(n_splits=10, random_state=seed)


# In[15]:


def getAccurcy(x, num_trees):
        model     = bagclf(dt(), max_samples=x, n_estimators=num_trees)
        results   = model_selection.cross_val_score(model, X, y, cv=kfold)
        return results.mean()


# In[16]:


from matplotlib import pyplot as plt

#Populating lists
    
yList = []
for bagsize in np.arange(0.1, 1.1, 0.1):
    yList.append(getAccurcy(bagsize,100))

df_plot = pd.DataFrame({'x': np.arange(0.1, 1.1, 0.1), 'y': yList})


# In[17]:



# initialize a figure
fig=plt.figure()

# Do a 2x2 chart
#plt.subplot(221)
plt.plot( 'x', 'y', data=df_plot, marker='o', alpha=0.4)
plt.title('Bag (%) size with Accuracy ' ,fontsize=12, color='grey', loc='left', style='italic')

# Add a title:"
plt.suptitle('Ensemble learning accuracies with different bag sizes', y=1.02)
plt.show()


# ** Conclusion: As the bag size increases; model's accuracy tends to decrease. **

# In[ ]:




