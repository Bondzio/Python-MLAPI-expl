#!/usr/bin/env python
# coding: utf-8

# Task: Create a Machine Learning Model to classify images of digits into a number between 0 and 9.
# 
# Problem Type: Multiclass Classification.
# 
# Algorithm: RandomForestClassification.
# 
# Published by Adedayo Okubanjo.

# In[ ]:


#import libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


dig = load_digits() #initialization
dir(dig) #returns the properties of an object without it's values


# In[ ]:


plt.gray() #display images in grayscale
#Loop through the top 5 rows of the images and display each of the images
for i in range(5): 
    plt.matshow(dig.images[i])


# In[ ]:


data_df = pd.DataFrame(dig.data) #convert data to a DataFrame 
data_df["Target"] = dig.target #add target from initial data to see the target number for each line of data in the data frame
data_df


# In[ ]:


#import scikit learn libraries for machine learning
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


# In[ ]:


#assign independent variables to x
x = data_df.drop(["Target"], axis = "columns")
#assign dependent variable to y
y = dig.target
#split your data into train and test samples
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2)
#initialize randomforestclassifier and fit model
classifier = RandomForestClassifier()
classifier.fit(x_train, y_train)


# In[ ]:


classifier.score(x_test,y_test)


# In[ ]:


y_pred = classifier.predict(x_test)


# In[ ]:


c_matrix = confusion_matrix(y_test,y_pred)


# In[ ]:


import seaborn as sb
#plot actual and predicted values in a confusion matrix to visualize how accurate the model predictions are
plt.subplots(figsize=(8,8))
ax = sb.heatmap(c_matrix, annot = True)
ax.set_xlabel("Actual")
ax.set_ylabel("Predicted")
ax.set_title("Confusion Matrix")


# In[ ]:


accuracy_score(y_test,y_pred)


# Model has an accuracy score of 97%.
