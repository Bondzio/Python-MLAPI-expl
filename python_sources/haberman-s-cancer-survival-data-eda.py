#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


# reading the Haberman's cancer survival data
data=pd.read_csv("../input/haberman.csv",header=None)


# In[ ]:


data.columns=["Age","Year","Node","S_S"]
s=data["S_S"]
s[s==1]="One"
s[s==2]="Two"


# In[ ]:


print(data.info())


# In[ ]:


print(data['S_S'].value_counts())


# In[ ]:


data['S_S'].unique()


# In[ ]:


print("About the data : ")
print("The dataset contains cases from a study that was conducted between 1958 and 1970 at the University of Chicago's Billings Hospital Survival status on the survival of patients who had undergone surgery for breast cancer.")
print("We have 3 features :")
print("1. Age : Age of patient at time of operation ")
print("2. Year : Patient's year of operation (year - 1900)")
print("3. Node : Number of positive axillary nodes detected")
print("We have 1 Class Label : ")
print("S_S : Survival status")
print("There are two classes :")
print(" (i) One = the patient survived 5 years or longer")
print("(ii) Two = the patient died within 5 year")
print("There  are total 306 Observations")
print("Out of which 225 Observations are related to Class One")
print("And 81 Observations are related to Class Two")
print("\nData Sample :\n\n")
print(data.head())

print(data.tail())


# In[ ]:


# Objective
print("Our objective is to find the important features that can help in Classifying the data")


# In[ ]:


print("Descriptive Statistics of Data\n")
print(data.drop("S_S",axis=1).describe())


# In[ ]:


print("Descriptive Statistics of Data related to Class One\n")
o=data[data["S_S"]=="One"]
print(o.describe())


# In[ ]:


print("Descriptive Statistics of Data related to Class Two\n")
t=data[data["S_S"]=="Two"]
print(t.describe())


# In[ ]:


sns.set_style("white")
sns.distplot(data["Age"])
plt.show()


# In[ ]:


print("Conclusion:")
print("Most patients are of Age between 50 to 55")
print("Very few patients are of age 80 to 85")


# In[ ]:


# Now we will perform Univariate Analysis to understand which features are useful towards Classification


# In[ ]:


sns.set_style("whitegrid")
sns.distplot(o["Age"],label="One")
sns.distplot(t["Age"],label="Two")
plt.legend()
plt.show()


# In[ ]:


print("Conclusion:")
print("Highest Survival rate is of Age 30 to 40 patients")


# In[ ]:


# Cumulative Distribution of Age in Class One and Two
x=o["Age"].sort_values()
y=t["Age"].sort_values()
plt.plot(x,np.cumsum(x)/np.sum(x),label="One")
plt.plot(y,np.cumsum(y)/np.sum(y),label="Two")
plt.xlabel("Age")
plt.legend()
plt.show()


# In[ ]:


sns.set_style("whitegrid")
sns.boxplot(x="S_S",y="Age",data=data)
plt.show()


# In[ ]:


print("Conclusion :")
print("No person of age greater than 77 could not survived")
print("Every person of age less 34 survived")


# In[ ]:


sns.set_style("whitegrid")
sns.violinplot(x="S_S",y="Age",data=data)
plt.show()


# In[ ]:


sns.set_style("whitegrid")
sns.distplot(o["Year"],label="One")
sns.distplot(t["Year"],label="Two")
plt.legend()
plt.show()


# In[ ]:


# Cumulative Distribution of Year in Class One and Two
x=o["Year"].sort_values()
y=t["Year"].sort_values()
plt.plot(x,np.cumsum(x)/np.sum(x),label="One")
plt.plot(y,np.cumsum(y)/np.sum(y),label="Two")
plt.xlabel("Year")
plt.legend()
plt.show()


# In[ ]:


sns.set_style("whitegrid")
sns.boxplot(x="S_S",y="Year",data=data)
plt.show()


# In[ ]:


sns.set_style("whitegrid")
sns.violinplot(x="S_S",y="Year",data=data)
plt.show()


# In[ ]:


sns.set_style("whitegrid")
sns.distplot(o["Node"],label="One",hist=False)
sns.distplot(t["Node"],label="Two")
plt.legend()
plt.show()


# In[ ]:


# Cumulative Distribution of Nodes in Class One and Two
x=o["Node"].sort_values()
y=t["Node"].sort_values()
plt.plot(x,np.cumsum(x)/np.sum(x),label="One")
plt.plot(y,np.cumsum(y)/np.sum(y),label="two")
plt.xlabel("Node")
plt.legend()
plt.show()


# In[ ]:


sns.set_style("whitegrid")
sns.boxplot(x="S_S",y="Node",data=data)
plt.show()


# In[ ]:


sns.set_style("whitegrid")
sns.violinplot(x="S_S",y="Node",data=data)
plt.show()


# In[ ]:


print("Conclusion :")
print("Mostly patients who survived had less than 5 positive axillary nodes")
print("Around 50% patients who could not survive had more than 4 positive axillary nodes")


# In[ ]:


# Bivariate Analysis


# In[ ]:


# Pair Plot
sns.pairplot(data,hue="S_S")
plt.show()


# In[ ]:


# Scatter Plot between Node and Age
sns.scatterplot("Node","Age",hue="S_S",data=data)
plt.show()


# In[ ]:


print("Conclusion :")
print("Scatter Plot between Age and Node gives better separation between the Survived and not survived patients")


# In[ ]:


# Scatter Plot between Node and Year
sns.scatterplot("Node","Year",hue="S_S",data=data)
plt.show()


# In[ ]:


# Scatter Plot between Age nad Year
sns.scatterplot("Age","Year",hue="S_S",data=data)
plt.show()


# In[ ]:


# 3D plot of Data
from mpl_toolkits import mplot3d
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(o['Age'],o["Year"],o["Node"],label="One",c='r')
ax.scatter3D(t['Age'],t["Year"],t["Node"],label="Two",c='k')
plt.xlabel("Age")
plt.ylabel("Year")
plt.legend()
plt.show()


# In[ ]:


print("Observations: ")
print("Data is imbalanced and Randomly Distributed")
print("Scatter Plot between Age and Node gives better separation between the Survived and not Srvived patient")
print("Node and Age are the most important features")
print("Most patients are of Age between 50 to 55")
print("Very few patients are of age 80 to 85")
print("Highest Survival rate is of Age 30 to 40 patients")
print("No person of age greater than 77 could not survived")
print("Every person of age less 34 survived")
print("Mostly patients who survived had less than 5 positive axillary nodes")
print("Around 50% patients who could not survive had more than 4 positive axillary nodes")


# In[ ]:




