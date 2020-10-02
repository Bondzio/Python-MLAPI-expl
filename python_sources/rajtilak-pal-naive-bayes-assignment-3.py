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


iris=pd.read_csv('/kaggle/input/iris/Iris.csv')


# In[ ]:


iris


# ## This data is numerical but Naive Bayes requires categorical columns. 
# We are going to encode the columns using pd.get_dummies() but to maintain the same encoding for the prediction point, we are going to concatenate prediction point with the training data. Once the encoding is done, we will train our model with the training data only and not pass the input point to the training process.

# ### Input Point

# In[ ]:


input_point=pd.DataFrame({'SepalLengthCm': [4.7], 'SepalWidthCm': [3.7], 'PetalLengthCm': [2], 'PetalWidthCm': [0.3]})


# ### Concatenating input point with training data

# In[ ]:


new=iris.append(input_point,ignore_index=True)


# In[ ]:


new


# In[ ]:


new.drop(columns='Id',inplace=True)


# ### Encoding the data

# In[ ]:


train=pd.get_dummies(new.iloc[:,:-1].astype(str))


# In[ ]:


train


# ### Did not encode the target column as it is already categorical

# In[ ]:


train['Species']=iris['Species']


# In[ ]:


train


# ## The General Class of Naive Bayes model

# In[ ]:


class NaiveBayes():

    def __init__(self):
        self.prob=dict()   # It stores, for every column, the probabilities of the unique values of every column given a class 
        self.target=''     # Stores the target column name   
        self.cl_prob=[]    # Stores the probabilities of every class
  
    def fit(self,data,target):

        # This function trains the NaiveBayes model. 
        # Params: 
        # data: The data to train(should contain the target column)
        # target: Mention the name of the target column

        print('Starting Training...')

        self.target=target

        # Extracting the columns except the target column
        columns=data.columns.to_list()
        columns.remove(self.target) 

        # Generating probabilities for every unique value in every column for every class  
        for column in columns:
            self.prob[column]=pd.crosstab(data[column],data[self.target])
        for key in self.prob.keys():
            for cl in self.prob[key].columns:
                self.prob[key][cl]=self.prob[key][cl]/self.prob[key][cl].sum()

        # Calculating the probabilities of every individual class
        cl_count=data[self.target].value_counts()
        self.cl_prob=cl_count/cl_count.sum()

        print('Training Complete!')


    def predict(self,test):

        # This function predicts the class for a given data
        # Params:
        # test: The data to predict the class. Should be a DataFrame.

        output=np.array([])  # Stores the predicted classes for every row

        # For every row predicting the class label
        for row in range(test.shape[0]):


            y=dict()       # Stores the probabilities corresponding to every class
            for cl in self.cl_prob.index.to_list():
                y[cl]=self.cl_prob[cl]
                for column in test.columns:
                    try:
                        y[cl]=y[cl]*self.prob[column][cl][test.loc[row][column]]
                    except:
                        pass

            output=np.append(output,max(y, key=y.get))   # Get the class with maximum probability and store it in output 
        return output


# In[ ]:


nb=NaiveBayes()


# ### The training data

# In[ ]:


train.iloc[:-1,:]


# In[ ]:


nb.fit(train.iloc[:-1,:],'Species')


# ### The input point to predict

# In[ ]:


test=train.iloc[-1:,:-1].reset_index(drop=True)


# In[ ]:


test


# ### Predicting now

# In[ ]:


results=nb.predict(test)


# ### Prediction results

# In[ ]:


results


# ### The input flower belongs to iris setosa 

# In[ ]:




