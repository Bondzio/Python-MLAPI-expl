#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold


# In[ ]:


X = np.array( [12,5,90,3,45,1] )
y = np.array( [1,1,1,1,0,0] )

y


# In[ ]:


cv = KFold( n_splits=2, shuffle=True, random_state=11)
for idxtrain, idxtest in cv.split(X=y):
    print (idxtrain, idxtest)
    print ( y[idxtrain] , y[idxtest] )
    print(' ')


# In[ ]:





# In[ ]:


cv = StratifiedKFold( n_splits=2, shuffle=True, random_state=1)
for idxtrain, idxtest in cv.split(X=y, y=y):
    print (idxtrain, idxtest)
    print ( y[idxtrain] , y[idxtest] )
    print(' ')


# In[ ]:





# In[ ]:





# In[ ]:


df = pd.read_csv( '../input/titanic/train.csv' )

df['Age'].fillna( df['Age'].mean( ) , inplace=True )

df.loc[ df['Sex']=='male' , 'Sex'] = 0
df.loc[ df['Sex']=='female' , 'Sex'] = 1

df.head(2)


# In[ ]:


df.shape


# In[ ]:


train = df[:700].reset_index(drop=True)
test  = df[700:].reset_index(drop=True)
print(train.shape, test.shape)


# In[ ]:


cols = ['Pclass',  'Fare', 'Age' ,'Sex']
testX  = test[ cols ].values
testY  = test[ 'Survived' ].values

trainX = train[ cols ].values
trainY = train[ 'Survived' ].values


# In[ ]:


df.isnull().sum()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


from keras.layers import Input, Dense, Activation
from keras import Model
from keras.optimizers import SGD


# In[ ]:


inpt = Input( shape=(4,) )

output1 = Dense(10, activation='relu') (inpt)

output1 = Dense(1) (output1)
output2 = Activation( 'sigmoid' ) (output1)

model = Model( inpt, output2 )


# In[ ]:


model.summary()


# In[ ]:


sgd = SGD()
model.compile( optimizer=sgd, metrics=['accuracy'], loss='mse' )


# In[ ]:


model.fit(trainX, trainY, epochs=10, validation_data=[testX, testY])


# In[ ]:





# In[ ]:


df = pd.DataFrame( [1,2,3,4,np.NaN,6,9,np.NaN] , columns=['a'])
df


# In[ ]:





# In[ ]:





# In[ ]:




