#!/usr/bin/env python
# coding: utf-8

# In this notebook, we will work construct and analyze the group-to-group graph of Nashville MeetUp data. For this graph, each node is an independent Nashville Meetup, and each edge is the number of shared members between each group. Example: if PyNash has 100 members and 50 of them are also members of the Nashville Hiking MeetUp, there will be an edge between those two with a weight of 50.
# 
# We first import the data and create a graph, then we read in some group metadata. Next, we derive measures of the graph and add them to our dataframe. Throughout, we visualize this information using `seaborn` and `matplotlib`.

# # Import data and setup environment

# In[ ]:


# First, import the important packages
import pandas as pd
import networkx as nx
import numpy as np


# In[ ]:


# Next read in the edges and create a graph
df = pd.read_csv('../input/group-edges.csv')
g = nx.from_pandas_edgelist(df, 
                            source='group1', 
                            target='group2', 
                            edge_attr='weight')

print('The member graph has {} nodes and {} edges.'.format(len(g.nodes),
                                                          len(g.edges)))


# In[ ]:


# Now, let's read in some member metadata
groups = pd.read_csv('../input/meta-groups.csv', index_col='group_id')
print('There are {} groups with metadata.'.format(groups.shape[0]))

# Let's trim the metadata down to those we have in the graph
groups = groups.loc[[x for x in g.nodes]]
print('After trimming, there are {} groups with metadata.'.format(groups.shape[0]))

groups.head()


# # Run NetworkX graph measures and add to DataFrame
# 
# Getting the graph-based measures is typically a simple matter of running a function. To add them to a DataFrame, however, you should have a `df` that is indexed by the node ID (i.e. `group_id` here), and convert your `networkx` output to a Series. This will make it very simple to add data into your existing DataFrame.

# In[ ]:


# Let's run some measures and populate our DataFrame
groups['degree'] = pd.Series(dict(nx.degree(g)))
groups['clustering'] = pd.Series(nx.clustering(g))
groups['centrality'] = pd.Series(nx.betweenness_centrality(g))

# Path length is a little trickier
avg_length_dict = {}
for node, path_lengths in nx.shortest_path_length(g):
    path_lengths = [x for x in path_lengths.values()]
    avg_length_dict[node] = np.mean(path_lengths)
groups['path_length'] = pd.Series(avg_length_dict)


# # Plot and describe measures

# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


# First, we plot a pairplot to get a sense of the overall relationships
# between each of the measures we derived. On the diagonal is the 
# distribution of values within the variable; off the diagonal are 
# scatterplots showing the correlation between variables.

grid = sns.pairplot(groups[['degree', 'clustering', 'path_length', 'centrality']])

plt.show()


# In[ ]:


# Now, let's look at clustering.
fig, ax = plt.subplots(1,1, figsize=(5,10), dpi=100)

sns.barplot(data=groups, x='clustering', y='category_name', 
            order=groups.groupby('category_name').clustering.mean().sort_values().index)
ax.set_title('Average clustering coefficient by Category')

plt.show()


# In[ ]:


# Next, let's plot the Number of Members (not degree!) vs. centrality
fig, ax = plt.subplots(1,1, figsize=(10,5))

sns.regplot(data=groups, x='num_members', y='centrality')
ax.set_title('Centrality vs. Number of Group Members')
ax.set_xlim([0,7000])

plt.show()


# In[ ]:


print('The ten most "central" groups are...')
print(groups.sort_values(by='centrality', ascending=False).group_name.head(10))

