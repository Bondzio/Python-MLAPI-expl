#!/usr/bin/env python
# coding: utf-8

# # Support Vector Matrix on Earthquake Data
# 
# The aim of this kernel is to help you understand the application and implementation of SVMs or SVRs. These techinques come in handy when two clusters have to be separated and then classified. In the following example, we use the Public Earthquake data to the draw the fault lines between the longitude and the latitude and also predict the Richter scale value.

# In[10]:


#Import the following packages or install them if you haven't already

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn import svm
from mlxtend.plotting import plot_decision_regions
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[11]:


#Read the Data
eq = pd.read_csv("../input/oneyear.csv")


# In[12]:


#Take a look at the dataset
eq.describe()


# In[13]:


#Since the data set doesnt have a lot of deviation in its feature, we can simply drop all the NaN values. 

eq.dropna(how='all',axis=1,inplace=True)


# In[14]:


#You can also plot a heat map to understand how each feature correlates to the other (Do they go hand in hand or are they inversely propotional)

f= plt.subplots(figsize=(21,21))
sn.heatmap(eq.corr(),annot=True,fmt='.1f',color='green')  #We can use a simple seaborn method to draw the heatmaps


# In[9]:


#The next step is to find a pattern in the scatter plots to be able to use Support Vector Machines and finding the fault line of the Earthquakes

pd.plotting.scatter_matrix(eq.loc[0:,eq.columns],c=['red','blue'],alpha=0.5,figsize=[25,25],diagonal='hist',s=200,marker='.',edgecolor='black')
plt.show()


# In[22]:


#The following is pretty clear from the plots. The diagram between magError and magNst suggests that the equation is hyperbolic
#While graphs between the latitude and longitude is a parabola.
#And looking at the deviation and the mean, we can see that Earthquakes with a Magnitude of 4.5 are at the center of all the observed Earthquakes

#Hence we create two Values. The X containing both the Latitude and the Longitude values, while the Y access segregating the values into either 1(when the Magnitude of the Earthquake is higher than 4.5)
#and 0 when the magnitude is lower than 4.5
X = eq[['latitude','longitude']]
Y = [0 if elem<4.5 else 1 for elem in eq.mag]


# In[23]:


#We call the SVC method from the sklearn library which creates the necessary object for fitting
clf = svm.SVC()


# In[24]:


#Simply fit the values of X and Y
clf.fit(X,Y)


# In[25]:


#Now all we have to do is plot the graph to show you the boundaries and fault lines

plot_decision_regions(X=np.array(X), 
                      y=np.array(Y),
                      clf=clf, 
                      legend=2)

# Update plot object with X/Y axis labels and Figure Title
plt.xlabel(X.columns[0], size=14)
plt.ylabel(X.columns[1], size=14)
plt.title('SVM Decision Region Boundary', size=16)


# In[28]:


#To predict the richter scale value, all we have to do is take a latitude and longitude and pass it across the function below
clf.predict([[69,70]])
#The output represents the magnitude of the Earthquake. If the value is 0, then the Richter Scale value at those coordinates if less than 
#4.5 or else its greater

