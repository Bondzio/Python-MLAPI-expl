#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import plotly as py
import plotly.graph_objs as go
import warnings
warnings.filterwarnings("ignore")
py.offline.init_notebook_mode(connected = True)


# In[29]:


mall_df = pd.read_csv('../input/Mall_Customers.csv')
mall_df.head()


# In[30]:


print (mall_df)


# In[31]:


mall_df.shape


# In[32]:


mall_df.columns


# In[33]:


mall_df['Gender'].head()


# In[34]:


mall1_df = mall_df.copy()
mall1_df.tail(5)


# Descriptive statistics of the data

# In[35]:


mall_df.describe().transpose()


# In[36]:


#Load the required packages
import numpy as np
import matplotlib.pyplot as plt

#Plot styling
import seaborn as sns; sns.set()  # for plot styling
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')


# Visualizing the data using "distplot"

# In[37]:


plot_annual_income = sns.distplot(mall_df["Annual Income (k$)"])


# In[38]:


plot_age = sns.distplot(mall_df["Age"])


# In[39]:


plot_spending_score = sns.distplot(mall_df["Spending Score (1-100)"])


# Violin Plot of Annual Income and Spending Score 

# In[40]:


f, axes = plt.subplots(1,2, figsize=(12,6), sharex=True, sharey=True)
v1 = sns.violinplot(data=mall_df, x='Annual Income (k$)', color="skyblue",ax=axes[0])
v2 = sns.violinplot(data=mall_df, x='Spending Score (1-100)',color="lightgreen", ax=axes[1])
v1.set(xlim=(-20,160))


# In[41]:


# Creating subset
mall_df_1 = mall_df[['Annual Income (k$)', 'Spending Score (1-100)']]
mall_df_1.head()


# Applying K-Means Clustering to find the target customers

# In[42]:


from sklearn.cluster import KMeans

#Using the elbow method to find the optimum number of clusters
wcss = []
for i in range(1,11):
    km=KMeans(n_clusters=i,init='k-means++', max_iter=300, n_init=10, random_state=0)
    km.fit(mall_df_1)
    wcss.append(km.inertia_)
plt.plot(range(1,11),wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('wcss')
plt.show()


# In[43]:


# So..number of clusters should be 5
km5=KMeans(n_clusters=5,init='k-means++', max_iter=300, n_init=10, random_state=0)
y_means = km5.fit_predict(mall_df_1)
#Visualizing the clusters
plt.scatter(mall_df_1[y_means==0]['Annual Income (k$)'],mall_df_1[y_means==0]['Spending Score (1-100)'],s=50, c='purple',label='Cluster1')
plt.scatter(mall_df_1[y_means==1]['Annual Income (k$)'],mall_df_1[y_means==1]['Spending Score (1-100)'],s=50, c='blue',label='Cluster2')
plt.scatter(mall_df_1[y_means==2]['Annual Income (k$)'],mall_df_1[y_means==2]['Spending Score (1-100)'],s=50, c='green',label='Cluster3')
plt.scatter(mall_df_1[y_means==3]['Annual Income (k$)'],mall_df_1[y_means==3]['Spending Score (1-100)'],s=50, c='cyan',label='Cluster4')
plt.scatter(mall_df_1[y_means==4]['Annual Income (k$)'],mall_df_1[y_means==4]['Spending Score (1-100)'],s=50, c='magenta',label='Cluster5')

plt.scatter(km5.cluster_centers_[:,0], km5.cluster_centers_[:,1],s=200,marker='s', c='red', alpha=0.7, label='Centroids')
plt.title('Customer segments')
plt.xlabel('Annual income of customer (k$)')
plt.ylabel('Customer: Spending Score (1-100)')
plt.legend()
plt.show()


# Clustering with 3 variables: Age, Annual Income (k$) and Spending Score (1-100) 

# In[44]:


# Creating subset
mall_df_2 = mall_df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
mall_df_2.head()


# In[45]:


#Using the elbow method to find the optimum number of clusters
wcss = []
for i in range(1,11):
    km=KMeans(n_clusters=i,init='k-means++', max_iter=300, n_init=10, random_state=0)
    km.fit(mall_df_2)
    wcss.append(km.inertia_)
plt.plot(range(1,11),wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('wcss')
plt.show()


# Hence, the optimum number of clusters = 6 (Elbow Method: Above)

# In[48]:


km6 = (KMeans(n_clusters = 6 ,init='k-means++', n_init = 10 ,max_iter=300, 
                        tol=0.0001,  random_state= 111  , algorithm='elkan') )
km6.fit(mall_df_2)
labels = km6.labels_
centroids = km6.cluster_centers_


# In[49]:


mall_df_2['labels'] =  labels
trace1 = go.Scatter3d(
    x= mall_df_2['Age'],
    y= mall_df_2['Spending Score (1-100)'],
    z= mall_df_2['Annual Income (k$)'],
    mode='markers',
     marker=dict(
        color = mall_df_2['labels'], 
        size= 20,
        line=dict(
            color= mall_df_2['labels'],
            width= 12
        ),
        opacity=0.8
     )
)
data = [trace1]
layout = go.Layout(
    title= 'Clusters',
    scene = dict(
            xaxis = dict(title  = 'Age'),
            yaxis = dict(title  = 'Spending Score'),
            zaxis = dict(title  = 'Annual Income')
        )
)
fig = go.Figure(data=data, layout=layout)
py.offline.iplot(fig)


# In[ ]:




