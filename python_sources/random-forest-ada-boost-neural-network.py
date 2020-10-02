#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np 
import pandas as pd
import numpy as np
from sklearn.svm import SVC, SVR
from sklearn import preprocessing
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.model_selection import train_test_split
from sklearn.ensemble import (RandomForestClassifier, ExtraTreesClassifier,
                              AdaBoostClassifier)
from sklearn.tree import DecisionTreeClassifier
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

import os
print(os.listdir("../input"))


# In[2]:


dataset=pd.read_csv("../input/faults.csv")
dataset[0:6]


# In[3]:


headers = list(dataset.columns.values)
headers_input = headers[:-7]
headers_output = headers[-7:]
print('features for input X:', headers_input)
print('classes for output Y:', headers_output)


# In[4]:


input_x = dataset[headers_input]
output_y = dataset[headers_output]


# Which features are not important

# In[5]:


min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
np_scaled = min_max_scaler.fit_transform(input_x)
headers_27 = list(input_x.columns.values)
input_x_27 = pd.DataFrame(np_scaled)
input_x_27.columns = headers_27
input_x_27[0:3]


# Value of Y is number between [0;6], which represent each class:

# In[8]:


from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
targets=(output_y.iloc[:,:]==1).idxmax(1)
print(targets.value_counts())
Y=le.fit_transform(targets)
print(len(Y))


# In[9]:


X_train_27, X_test_27, y_train_27, y_test_27 = train_test_split(input_x_27, Y, test_size=0.3)


# In[13]:


import matplotlib.pyplot as plt
import seaborn as sns

#Create a Gaussian Classifier
clf=RandomForestClassifier(n_estimators=100)
#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X_train_27,y_train_27)
headers_norm = list(X_train_27.columns.values)
feature_imp = pd.Series(clf.feature_importances_,index=headers_norm).sort_values(ascending=False)
# Creating a bar plot
sns.barplot(x=feature_imp, y=feature_imp.index)
# Add labels to your graph
plt.xlabel('Feature Importance Score')
plt.ylabel('Features')
plt.title("Visualizing Important Features")
plt.legend()
plt.show()


# The most important features accoding to Random Forest are: Length_of_Conveyer, LogOfAreas, Pixels_Areas, Steel_Plate_Thickness, Sum_of_Luminosity, Log_X_Index, X_Maximum. 

# We will drop values which are not important based on dimensionality reduction: high Correlation filter

# In[14]:


# Create correlation matrix
corr_matrix = input_x.corr().abs()

# Select upper triangle of correlation matrix
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

# Find index of feature columns with correlation greater than 0.95
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]

print(to_drop)


# In[15]:


plt.matshow(input_x.corr())
plt.xticks(range(len(input_x.columns)), input_x.columns)
plt.yticks(range(len(input_x.columns)), input_x.columns)
plt.colorbar()
plt.show()


# Drop features that have correlation with other features as they are not important according to Random Forest feature selection.

# In[16]:


input_x = input_x.drop(input_x[to_drop], axis=1)
input_x[0:6]


# We will drop values further based on dimensionality reduction: low variance filter.
# We will check variations of each columns, and drop some features wich have less variation.

# In[17]:


input_x.var()


# We find all the columns, which values varies less then 10%:

# In[18]:


numeric = input_x
var = numeric.var()
numeric = numeric.columns
variable = [ ]
for i in range(0,len(var)):
    if var[i]>=10:   #setting the threshold as 10%
        variable.append(numeric[i+1])


# In[19]:


variable


# Low variance filter shows features which are important according to Random Forest feature selection, so we will not drop  them. 

# In[20]:


# important features according to Random Forest
print(feature_imp)


# In[21]:


print(len(input_x.iloc[0,:]))


# We will compare distribution of each classes.  

# In[24]:


min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
np_scaled = min_max_scaler.fit_transform(input_x)
input_x_norm = pd.DataFrame(np_scaled)
headers_22= list(input_x.columns.values)
input_x_norm.columns = headers_22
input_x_norm[0:6]


# In[25]:


# Import train_test_split function
X_train, X_test, y_train, y_test = train_test_split(input_x_norm, Y, test_size=0.3)


# Decision Trees, Random Forest Classifier, ExtraTrees, AdaBoost:

# In[26]:


# Parameters
n_classes = 7
n_estimators = 100
RANDOM_SEED = 13  # fix the seed on each iteration

names = ['DecisionTreeClassifier', 'RandomForestClassifier', 'ExtraTreesClassifier', 'AdaBoostClassifier']
models = [DecisionTreeClassifier(max_depth=None),
          RandomForestClassifier(n_estimators=n_estimators),
          ExtraTreesClassifier(n_estimators=n_estimators),
          AdaBoostClassifier(DecisionTreeClassifier(max_depth=None),
                             n_estimators=n_estimators)]
for counter, model in enumerate(models):
    # Train
    model.fit(X_train, y_train)
    y_pred=model.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy " + names[counter] + ":",metrics.accuracy_score(y_test, y_pred))


# Extra Trees Classifier is the most accurate algorithm

# In[ ]:


input_x_NN = dataset[headers_input]
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
np_scaled = min_max_scaler.fit_transform(input_x_NN)
df_normalized = pd.DataFrame(np_scaled)
df_normalized.columns = headers_input
df_normalized[0:6]


# We create one-hot encoding for the output y:

# In[ ]:


#One Hot Encode our Y:
from sklearn.preprocessing import LabelBinarizer
encoder = LabelBinarizer()
Y_one_hot = encoder.fit_transform(Y)
print(Y_one_hot)


# We will create more samples for the class, which has less amount of samples:

# In[ ]:


from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
import seaborn as sns
ros = RandomOverSampler(random_state=0)
X = input_x_norm #df_normalized
ros.fit(X, Y)
X_resampled, y_resampled = ros.fit_sample(X, Y)
print('Amount of elements before:', len(X))
print('Amount of elements after:', len(X_resampled))


# We increased the amount of classes, so we have 4711 elements instead of 1941, each class has 673 elements 

# In[ ]:


unique, counts = np.unique(y_resampled, return_counts=True)
dict(zip(unique, counts))


# Split data to train and test:

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,
                                                 Y_one_hot,
                                                 test_size = 0.3,#%70 train, 30% test
                                                 random_state = 3)


# Multilayer perceptron: 

# In[ ]:


import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

model = Sequential()

model.add(Dense(64, activation='relu', input_dim=22))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(X_train, y_train,
          epochs=2000,
          batch_size=128)


# In[ ]:


score = model.evaluate(X_test, y_test, batch_size=128)
print(score)
print(model.metrics_names)


# The accuracy on test set:

# In[ ]:


Y_predicted = model.predict(X_test, batch_size=32, verbose=0)
percent = 0
for i in range(0, len(Y_predicted)):
    class_id_predicted = np.argmax(Y_predicted[i])
    class_id_real = np.argmax(y_test[i])
    if class_id_predicted == class_id_real: 
        percent += 1
print('val accuracy: ', percent/len(Y_predicted))

