#!/usr/bin/env python
# coding: utf-8

# **Habermans-survival-data-set**
# 
# Attribute Information:
# * Age of patient at time of operation (numerical)
# * Patient's year of operation (year - 1900, numerical)
# * Number of positive axillary nodes detected (numerical)
# * Survival status (class attribute) 1 = the patient survived 5 years or longer 2 = the patient died within 5 years
# 
# **Objective:-** 
# * To classify whether the patient will survive  more than 5 years or die within 5 years based upon the patient's age, year of treatment and the number of positive lymph nodes

# In[ ]:


#importing important libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Input data files are available in the "../input/" directory.
import os
print(os.listdir("../input"))


# In[ ]:


#Loading the dataset
dataset = pd.read_csv("../input/haberman.csv",header=None,
        names=['age', 'year_of_operation', 'axillary_nodes', 'survival_status'])


# In[ ]:


#No. of Datapoints and features
dataset.shape


# In[ ]:


#Column names
dataset.columns


# In[ ]:


print(dataset.head(10))


# In[ ]:


#Counting number of datapoints in each class
dataset['survival_status'].value_counts()


# **Observation:-** 
# * It seems to be an imbalanced dataset as one class is almost three times of the other class. 

# In[ ]:


dataset.describe()


# **Observation:-**
# * Age of patient ranges from 30 to 83.
# * Positive axillary nodes ranges from 0 to 52.  25% of patients are having 0 positive axillary nodes. Even though maximum no. of    positive axillary is 52 but 75% of patients are having less than equal to 4 axillary nodes.

# In[ ]:


#2-D scatter plots - Multivariate Analysis
sns.set_style("whitegrid")
sns.pairplot(dataset,hue='survival_status',vars=[dataset.columns[0],dataset.columns[1],
                                                 dataset.columns[2]],height=4)


# **Observation:-**
# * From the pair plots it is clearly evident that the two classes are not linearly seperable.
# * There is better seperation between the classes when the data points are scattered between year of operation and axillary nodes.

# In[ ]:


#Univariate Analysis
#Plotting histogram along with PDF.
for i,attr in enumerate(list(dataset.columns)[:-1]):
    sns.FacetGrid(dataset,hue='survival_status',height=4).map(sns.distplot,attr).add_legend()
    plt.show()


# In[ ]:


#Plotting CDF of the survivors(after5)
after5 = dataset[dataset['survival_status']==1]
plt.figure(figsize=(15,8))
sns.set_style("whitegrid")
for i,attr in enumerate(list(dataset.columns)[:-1]):
    plt.subplot(1,3,i+1)
    print("---------",attr,"----------")
    counts,bin_edges = np.histogram(after5[attr],bins=10,density=True)
    print("Bin_Edges:- ",bin_edges)
    pdf = counts/sum(counts)
    print("PDF:- ",pdf)
    cdf = np.cumsum(pdf)
    print("CDF:- ",cdf)
    plt.plot(bin_edges[1:],pdf)
    plt.plot(bin_edges[1:],cdf)
    plt.xlabel(attr)


# **Observations:-**
# * 83.55% of the survivors have positive axillary nodes less than 5.

# In[ ]:


#Plotting CDF of those who died with in 5 years
within5 = dataset[dataset['survival_status']==2]
plt.figure(figsize=(15,8))
sns.set_style("whitegrid")
for i,attr in enumerate(list(dataset.columns)[:-1]):
    plt.subplot(1,3,i+1)
    print("-------------",attr,"--------------")
    counts,bin_edges = np.histogram(within5[attr],bins=10,density=True)
    print("Bin_Edges:- ",bin_edges)
    pdf = counts/sum(counts)
    print("PDF:- ",pdf)
    cdf = np.cumsum(pdf)
    print("CDF:- ",cdf)
    plt.plot(bin_edges[1:],pdf)
    plt.plot(bin_edges[1:],cdf)
    plt.xlabel(attr)


# **Observations:-** 
# * 97.53% of those who died within 5 years were having axillary nodes less than equal to 26.
# 

# In[ ]:


#Box plot
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i,attr in enumerate(list(dataset.columns)[:-1]):
    sns.boxplot(x='survival_status',y=attr,data=dataset, ax=axes[i])
plt.show()


# In[ ]:


#Calculating 25th,50th and 75th percentile of the survivors and those who died w.r.t to axillary nodes
print(np.percentile(after5['axillary_nodes'],(25,50,75)))
print(np.percentile(within5['axillary_nodes'],(25,50,75)))


# In[ ]:


#Violin Plot
fig,axes = plt.subplots(1,3,figsize=(15,5))
for i,attr in enumerate(list(dataset.columns)[:-1]):
    sns.violinplot(x='survival_status', y=attr, data = dataset, ax=axes[i])
plt.show()


# **Observations:-**
# * Positive axillary nodes of those whose died is highly densed from 4 to 11.
# * Positive axillary nodes of survivors is highly densed from 0 to 5.
# * The patients treated after 1965 have slighlty higher chance to surive that the rest. The patients treated before 1959 have               slightly lower chance to surive that the rest.
