#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# From Sratch


# In[ ]:


import matplotlib.pylab as plt
import seaborn as sns
from pylab import rcParams
import networkx as nx


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('darkgrid')
rcParams['figure.figsize']=6,5


# # creating Graph Object

# In[ ]:


G=nx.Graph()
nx.draw(G)


# In[ ]:


G.add_node(1)
nx.draw(G)


# In[ ]:


G.add_nodes_from([2,3,4,5,6,8,9,12,15,16])
nx.draw(G)


# In[ ]:


G.add_edges_from([(2,4),(2,6),(2,8),(2,12),(2,16),(3,6),(3,9),(3,12),(3,15),(4,8),(4,12),(4,16),(6,12),(8,16)])
nx.draw(G)


# In[ ]:


nx.draw_circular(G)


# In[ ]:


nx.draw_spring(G)


# In[ ]:


nx.draw_circular(G, node_color='bisque', with_labels=True)


# In[ ]:


G.remove_node(1)
nx.draw_circular(G, node_color='bisque', with_labels=True)


# # Identifying Graph Properties

# In[ ]:


summary_stats=nx.info(G)
print(summary_stats)


# In[ ]:


print(nx.degree(G))


# # Using Graph Generators

# In[ ]:


G=nx.complete_graph(25)
nx.draw(G, node_color='bisque', with_labels=True)


# In[ ]:


G=nx.gnc_graph(7, seed=25)
nx.draw(G, node_color='bisque', with_labels=True)


# In[ ]:


ego_G=nx.ego_graph(G, 3, radius=5) 
nx.draw(G, node_color='bisque', with_labels=True)


# # Simulate a social network

# In[ ]:


DG = nx.gn_graph(7, seed=25)
for line in nx.generate_edgelist(DG, data=False):
    print(line)


# # Assigning attributes to nodes

# In[ ]:


print(DG.node[0])


# In[ ]:


DG.node[0]['name']=['Alice']
print(DG.node[0])


# In[ ]:


DG.node[1]['name']=['Bob']
DG.node[2]['name']=['Claire']
DG.node[3]['name']=['Dennis']
DG.node[4]['name']=['Esther']
DG.node[5]['name']=['Frank']
DG.node[6]['name']=['George']


# In[ ]:


DG.add_nodes_from([(0,{'age':25}),(1,{'age':31}), (2,{'age':18}), (3,{'age':47}), (4,{'age':22}), (5,{'age':23}),(6,{'age':50})])
print(DG.node[0])


# In[ ]:


DG.node[0]['gender']='f'
DG.node[1]['gender']='m'
DG.node[2]['gender']='f'
DG.node[3]['gender']='m'
DG.node[4]['gender']='f'
DG.node[5]['gender']='m'
DG.node[6]['gender']='m'


# In[ ]:


nx.draw_circular(DG, node_color='bisque', with_labels=True)


# In[ ]:


labeldict={0:'Alice', 1:'Bob', 2:'Claire', 3:'Dennis', 4: 'Esther', 5: 'Frank', 6: 'George'}
nx.draw_circular(DG,labels=labeldict, node_color='bisque', with_labels=True)


# In[ ]:


G = DG.to_undirected()


# In[ ]:


nx.draw_spectral(G, labels= labeldict, node_color='bisque', with_labels=True)


# # Generate stats on nodes and inspect graphs

# In[ ]:


print(nx.info(DG))


# # Considering degrees in a social network

# In[ ]:


DG.degree()


# # Identifying Successor Nodes

# In[ ]:


nx.draw_circular(DG, node_color='bisque', with_labels=True)


# In[ ]:


DG.successors(3)


# In[ ]:


DG.neighbors(4)


# In[ ]:


G.neighbors(4)

