#!/usr/bin/env python
# coding: utf-8

# # Artificial Neural Network in python without any deep learning library
# Deep Learning libraries are fast and makes our code short, but we must know maths behind those one line functions used in libraries like tensorflow, theano, keras etc.
# 
# **** Please upvote if found useful****

# In[ ]:


# Importing basic libraries 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


# Import dataset
dataset = pd.read_csv('../input/train.csv')


# In[ ]:


dataset.head()


# ## Cleaning Data
# Our data is not cleaned, there are many columns which we can't feed into neural network.

# In[ ]:


dataset.describe()


# we can see that there are some values missing in columns.

# In[ ]:


# Check missing data
dataset.isnull().sum()


# ### Dealing with missing Data

# In[ ]:


# We will fill median of all values instead of mean because it will be more correct
dataset['Age'] = dataset['Age'].fillna(dataset['Age'].median())


# Cabin does not have much impact on our dependent variable, so we will ignore that

# In[ ]:


dataset['Embarked'].value_counts()


# In[ ]:


# Embarked column have 'S' value in large amount than rest of the values.
# So we will fill 'S' in two empty rows.
dataset['Embarked'].fillna('S', inplace = True)


# In[ ]:


dataset['Sex'].value_counts()


# In[ ]:


# We will fill 1 for male and 0 for female in our data
dataset['Sex'] = dataset['Sex'].apply(lambda x: 1 if x=='male' else 0)


# In[ ]:


# we can't feed Embarked column with its original values.
# we'll have one-hot-encode this column

cat_columns = ['Embarked'] # categorical column which we'll one-hot-encode.
dataset = pd.get_dummies(dataset,prefix_sep = '__',  columns = cat_columns)


# In[ ]:


# We'll drop unnecessary columns which doesn't have much impact on our dependent variable
dataset.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, inplace=True)


# In[ ]:


dataset.head()


# Now data is ready to feed into neural network

# In[ ]:


x = dataset.iloc[:, 1:].values
y = dataset.iloc[:,:1].values


# Now we'll split data into training part and testing part, generally we split into 7:3 but I have used 80% data for training and remaining for testing part.

# In[ ]:


# Split data
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2 )


# In[ ]:


N,D = x.shape        #Dimentions of data
M = 10               #Hidden Units in our neural network


# In[ ]:


# First we'll initialize random weights and bias for our neural network
w1= np.random.randn(D,M)/np.sqrt(D+M)
b1 = np.zeros(M)
w2 = np.random.randn(M,1)/np.sqrt(M+1)
b2 = 0


# In[ ]:


# We'll use sigmoid because we are classifying our data and result is binary
def sigmoid(z):
    return 1/(1+np.exp(-z))


# In[ ]:


# We'll use rectifier linear unit as non-linearity.
# So Differentiation of relu will be required.

d_relu = lambda x: (x>0).astype(x.dtype) 


# In[ ]:


# Feed Forward function for our neural network

def forward(x,w1,b1,w2,b2):
    z = np.maximum((x.dot(w1)+b1), 0)     # relu nonlinearity
    return sigmoid(z.dot(w2)+b2), z       # we'll return both, since output of relu will be required.


# In[ ]:


# Defining Cross Entropy for sigmoid
def cross_en(T,Y):
    return -np.mean(T*np.log(Y) + (1-T)*np.log(1-Y))


# In[ ]:


# Empty list, cost will be appended in backpropagation 
cost_train = []
cost_test = []

#Defining learning rate
lr = 0.001


# ## Backpropagation

# In[ ]:


for i in range(100000):
    yprep, ztrain = forward(x_train,w1,b1,w2,b2)  
    train_cost = cross_en(y_train, yprep)
    
    yprep_test, ztest = forward(x_test, w1,b1,w2,b2)
    test_cost = cross_en(y_test, yprep_test)
    
    if i%5000==0:  #Every 5000th step cost will be printed 
        print('train_cost = {}'.format(train_cost))
        print('test_cost = {}'.format(test_cost))
    
    E = (yprep-y_train)     # It'll be used many times in loop so we'll define for reducing computation
    
    #We'll update weights from right to left
    w2-= lr*(ztrain.T.dot(E)/len(x_train))  
    b2-= lr*(E.sum()/len(x_train))
    
    dz = E.dot(w2.T)*d_relu(ztrain)  # It'll be used multiple times so we'll define once.
    
    w1-= lr*(x_train.T.dot(dz)/len(x_train))
    b1-= lr*(dz.sum()/len(x_train))
    
    # append cost in list
    cost_train.append(train_cost)
    cost_test.append(test_cost)
    


# In[ ]:


#Plotting train and test cost
plt.plot(cost_train, 'k') #black
plt.plot(cost_test, 'b') #blue


# ## Submitting to Kaggle

# In[ ]:


#Import test dataset
test_dataset = pd.read_csv('../input/test.csv')


# In[ ]:


test_dataset.head()


# Test dataset must be in same form as the dataset we had feeded to our neural network

# In[ ]:


test_dataset.isnull().sum()


# In[ ]:


#Fill missing data
test_dataset['Age']= test_dataset['Age'].fillna(test_dataset['Age'].median())

test_dataset['Fare']= test_dataset['Fare'].fillna(test_dataset['Fare'].median())


# In[ ]:


test_dataset['Sex'] = test_dataset['Sex'].apply(lambda x: 1 if x=='male' else 0)


# In[ ]:


# One hot encodint
test_dataset = pd.get_dummies(test_dataset,prefix_sep = '__',  columns = cat_columns)


# In[ ]:


passengerID = test_dataset['PassengerId'] # Passenger Id will be required in our submission

test_dataset.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, inplace=True)


# In[ ]:


test_dataset.head()


# Now data is ready to feed forward

# In[ ]:


test_data_pred,z_test_data = forward(test_dataset,w1,b1,w2,b2)

#We'll round values because we have probabilities (Sigmoid is used)
test_data_pred = (np.round(test_data_pred))

submission = pd.DataFrame({'PassengerId': passengerID, 'Survived':test_data_pred[0]}).astype(int)


# In[ ]:


#Our submission
submission.to_csv('submission.csv', index=False)
#Output file

