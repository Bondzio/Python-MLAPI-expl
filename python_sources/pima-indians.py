#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense
import numpy

seed = 7
numpy.random.seed(seed)


# **Import the data and take the first 8 columns as the X Columns and the 9th column as the prediction**

# In[ ]:


dataset = numpy.loadtxt("../input/diabetes.csv", delimiter=",", skiprows=1)
X = dataset[:,0:8]
Y = dataset[:,8]


# Create the model in keras
# Layer 1 : 12 neurons and expecting 8 inputs (relu)
# Layer 2 : 8 neurons and expecting 12 inputs (relu)
# Layer 3 : 1 neron and expects 8 inputs (sigmoid)

# In[ ]:


model = Sequential()
model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))


# In[ ]:


model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[ ]:


# Automatic validation
model.fit(X, Y, validation_split=0.33, nb_epoch=1000,batch_size=100)


# In[ ]:


scores = model.evaluate(X,Y)
print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))


# In[ ]:


# Manual Validation
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33,random_state=seed)
model.fit(X_train,Y_train, validation_data=(X_test,Y_test), nb_epoch=150, batch_size=10)


# In[ ]:


# K fold Cross validation
from sklearn.model_selection import StratifiedKFold

kfold = StratifiedKFold(n_splits=10,shuffle=True, random_state=seed)
cvscores = []


for train, test in kfold.split(X,Y):
    model = Sequential()
    model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
    model.add(Dense(8, init='uniform',activation='relu'))
    model.add(Dense(1, init='uniform',activation='sigmoid'))
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    model.fit(X[train], Y[train], nb_epoch=150, batch_size=10, verbose=0)
    
    scores = model.evaluate(X[test], Y[test], verbose=0)
    print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))
    cvscores.append(scores[1]*100)
    

print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))
    


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
import numpy


# In[ ]:


def create_model():
    model = Sequential()
    model.add(Dense(12, input_dim=8, init= 'uniform' , activation= 'relu' ))
    model.add(Dense(8, init= 'uniform' , activation= 'relu' ))
    model.add(Dense(1, init= 'uniform' , activation= 'sigmoid' ))
    
    model.compile(loss= 'binary_crossentropy' , optimizer= 'adam' , metrics=['accuracy'])
    return model


# In[ ]:


seed = 7 
numpy.random.seed()
# load pima indians dataset
dataset = numpy.loadtxt("../input/diabetes.csv", delimiter=",", skiprows=1)
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
# create model
model = KerasClassifier(build_fn=create_model, nb_epoch=150, batch_size=10, verbose=0)
# evaluate using 10-fold cross validation
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(model, X, Y, cv=kfold)
print(results.mean())


# In[ ]:




