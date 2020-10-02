#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[2]:


train_df=pd.read_csv('../input/train.csv')
train_df.head()


# In[3]:


test_df=pd.read_csv('../input/test.csv')
test_df.head()


# In[4]:


#define a function to draw the image
#x-> dataframe with data
#y-> dataframe with labels
def draw_digit(x,y, label='Actual'):
    plt.figure(figsize=(20,5))
    #check the length of input dataset and divide by 8 to print 10 digits on each line
    nrows=(len(x)//10)+1
    #ncols=(len(x)%10)
    ncols=10
    print('Lenght of input: {}, nrows: {}, ncols: {}, label: {}'.format(len(x), nrows, ncols, y.shape))
    #print(x.shape)
    #iterate over all the digits passed in the array
   
    for idx,i in enumerate(x.index):
        #loop to iterate over blocks of 10 digits            
            plt.subplot(nrows,10,idx+1)  #subplots start with 1
            plt.subplots_adjust(top=1.3)
            plt.imshow(x.loc[i].values.reshape(28,28), cmap=plt.cm.gray, interpolation='nearest',clim=(0, 255))
            plt.title(label+' %i\n' % y.iloc[idx,:].values, fontsize = 11)
            #plt.title('Actual {}\n'.format(y.iloc[idx,:].values), fontsize = 11)
           
    plt.show()


# In[5]:


#Display image of digits
draw_digit(train_df.iloc[:15,1:], train_df.iloc[:15,:1],'Actual')


# **Using Random Forest to classify**

# In[6]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
rf=RandomForestClassifier(n_jobs=-1, oob_score=True, verbose=1)


# In[7]:


#Prepare a pipeline
steps=[('Scaler',StandardScaler()), ('rf',rf)]


# # Create a Pipeline for scaling and training 

# In[8]:


from sklearn.pipeline import Pipeline
pipeline=Pipeline(steps)


# In[9]:


#Define the hyperparameters for Random Forest 
params={'rf__n_estimators':[1000, 1500, 2000, 2500], 'rf__max_depth':[10,15, 20, 25], 'rf__oob_score':['True']}


# In[10]:


from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score


# **Split the dataset into training and test**

# In[11]:


y=train_df['label']
X=train_df.drop('label', axis=1)


# In[12]:


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, test_size=0.3, random_state=2)


# In[13]:


print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


# In[14]:


grid_cv=GridSearchCV(n_jobs=-1,
                     estimator=pipeline,
                     param_grid=params,
                     return_train_score=True,
                     cv=3,
                     verbose=1)


# In[15]:


from timeit import default_timer as timer


# In[16]:


grid_cv.estimator.get_params().keys()


# In[17]:


start=timer()
grid_cv.fit(X_train, y_train)
end=timer()


# In[18]:


print('Time taken to fit on train data (in min): {} '.format((end-start)/60))


# In[19]:


#Check the score
grid_cv.score(X_train, y_train), grid_cv.score(X_test, y_test)


# **99.85% accuracy :)**

# In[20]:


grid_cv.best_params_


# In[21]:


cv_result=pd.DataFrame(grid_cv.cv_results_)
cv_result.head()


# **Plot the Accuracy curve for train and test data**

# In[22]:


plt.figure(figsize=(15,8))
plt.subplots(1,2, sharex='none', figsize=(20,8))
plt.subplot(1,2,1)
plt.plot(cv_result['param_rf__max_depth'], cv_result['mean_test_score'],'-xr', label='Test')
plt.plot(cv_result['param_rf__max_depth'], cv_result['mean_train_score'],'-xg', label='Train')
plt.xlabel('Max Depth')
plt.ylabel('Accuracy')
#

plt.subplot(1,2,2)
plt.plot(cv_result['param_rf__n_estimators'], cv_result['mean_test_score'],'-*r', label='Test')
plt.plot(cv_result['param_rf__n_estimators'], cv_result['mean_train_score'],'-*g', label='Train')
plt.xlabel('Estimators')
plt.ylabel('Accuracy')


# In[23]:


cv_result[['rank_test_score','param_rf__n_estimators','param_rf__max_depth', 'mean_train_score', 'mean_test_score']]


# **Create a new model with the best params and make predictions**

# In[25]:


rf1=RandomForestClassifier(max_depth=grid_cv.best_params_['rf__max_depth'], n_estimators=grid_cv.best_params_['rf__n_estimators'], n_jobs=-1, verbose=1, oob_score=True)
pipeline1= Pipeline([('Scaler',StandardScaler()), ('rf',rf1)])


# In[26]:


start=timer()
pipeline1.fit(X_train, y_train)
end=timer()


# In[27]:


print('Time taken to fit on train data using best hyperparameter (in min): {} '.format((end-start)/60))


# In[28]:


#Make a prediction
start=timer()
y_pred=pipeline1.predict(X_test)
end=timer()
print('Time taken to Preidct on test data (in min): {} '.format((end-start)/60))


# **Analyze the prediction. Calculate Metrics**

# In[29]:


from sklearn.metrics import classification_report, confusion_matrix


# In[30]:


cmat=confusion_matrix(y_test, y_pred)


# In[31]:


cmat


# In[33]:


import seaborn as sns


# In[34]:


sns.heatmap(cmat, annot=True, fmt='g')


# In[ ]:





# In[ ]:





# In[ ]:





# In[43]:


submit_df =pd.concat([pd.Series(test_df.index, name='ImageId'), pd.Series(y_pred, name='Label')], axis=1)
submit_df.to_csv('./rf_submission.csv', index=False)


# In[ ]:





# In[ ]:





# In[ ]:




