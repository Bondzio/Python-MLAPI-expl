#!/usr/bin/env python
# coding: utf-8

# Notebook shows various examples/functions how to work with SNAP graph library 
# https://snap.stanford.edu/snappy/index.html

# In[ ]:


get_ipython().system('python -m pip install snap-stanford')
import snap


# # Links to helpful docs

# In[ ]:


# https://snap.stanford.edu/snappy/index.html - various simple examples given here
# https://snap.stanford.edu/snappy/doc/tutorial/index-tut.html - examples by topic
# https://snap.stanford.edu/snappy/doc/reference/index-ref.html - docs topic by topic


# # Create Graph: create, AddNode, AddEdge

# In[ ]:


G = snap.TUNGraph.New() # Create UNoriented graph 
#G2 = snap.TNGraph.New() # Created DIRECTED graph
G.AddNode(1) # Add nodes 
G.AddNode(2)
G.AddNode(3)
G.AddNode(4)
G.AddEdge(1,2)
G.AddEdge(2,3)
G.AddEdge(3,4)
G.AddEdge(4,1)

print(G.GetNodes(), G.GetEdges() )    

snap.PrintInfo(G,'Test Graph','graph_info.txt') # https://snap.stanford.edu/snappy/doc/reference/PrintInfo.html
# Creates basic info on graph - numbers of edges, nodes, etc... I do not see how to make it print to screen


# # Plot graph to png and show it

# In[ ]:


snap.DrawGViz(G, snap.gvlDot, "Gsmall_grid5x3.png", "Grid 5x3") # Save image to png
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread('Gsmall_grid5x3.png')
plt.imshow(img)
plt.show()


# # Nodes and Edges number

# In[ ]:


print(G.GetNodes(), G.GetEdges() )    


# # G.IsEdge(v1,v2) - check is there an edge between nodes v1,v2

# In[ ]:


G.IsEdge(1,2), G.IsEdge(1,3) 


# # Iterate over nodes and GetDeg  for node

# In[ ]:


for n in G.Nodes():
  print(n.GetDeg() ) 


# # Get neigbours of node - GetNodesAtHop

# In[ ]:


for n in G.Nodes():
  NodeVec = snap.TIntV()
  snap.GetNodesAtHop(G, n.GetId(), 1, NodeVec, False) # Get neigbours of current node # https://snap.stanford.edu/snappy/doc/reference/GetNodesAtHop.html


# # Create different types of graphs

# ## Erdos Renyi Gnm

# In[ ]:


Graph = snap.GenRndGnm(snap.PNGraph, 1000, 10000) # https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model


# ## Preferential Attachment, Forest Fire

# In[ ]:


# generate a Preferential Attachment graph on 1000 nodes and node out degree of 3
G8 = snap.GenPrefAttach(1000, 3) # https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model
# generate a network using Forest Fire model
G6 = snap.GenForestFire(1000, 0.35, 0.35)


# # Clustering coef

# ## Globabl clustering coef - average over nodes

# In[ ]:


GraphClustCoeff = snap.GetClustCf (G, -1) # https://snap.stanford.edu/snappy/doc/reference/GetClustCf.html
print("Clustering coefficient: %f" % GraphClustCoeff)


# ## Clustering coefficient vector for all nodes 

# In[ ]:


NIdCCfH = snap.TIntFltH()
snap.GetNodeClustCf(G, NIdCCfH) # https://snap.stanford.edu/snappy/doc/reference/GetNodeClustCf.html
for item in NIdCCfH:
    print(item, NIdCCfH[item])


# ## Get clustering coefficients aggregated by degrees

# In[ ]:


Graph = snap.GenRndGnm(snap.PNGraph, 1000, 10000) # Erdos-Renyi graph 
CfVec = snap.TFltPrV()
Cf = snap.GetClustCf(Graph, CfVec, -1) # https://snap.stanford.edu/snappy/doc/reference/GetClustCf1.html
print("Average Clustering Coefficient: %f" % (Cf[0]))
print("Coefficients by degree:\n") 
for pair in CfVec:
    print("degree: %d, clustering coefficient: %f" % (pair.GetVal1(), pair.GetVal2()))


# # Connected components

# In[ ]:


# generate a Preferential Attachment graph on 1000 nodes and node out degree of 3
G8 = snap.GenPrefAttach(1000, 3)
# vector of pairs of integers (size, count)
CntV = snap.TIntPrV()
# get distribution of connected components (component size, count)
snap.GetWccSzCnt(G8, CntV)
# get degree distribution pairs (degree, count)
snap.GetOutDegCnt(G8, CntV)
# vector of floats
EigV = snap.TFltV()
# get first eigenvector of graph adjacency matrix
snap.GetEigVec(G8, EigV)
# get diameter of G8
snap.GetBfsFullDiam(G8, 100)
# count the number of triads in G8, get the clustering coefficient of G8
snap.GetTriads(G8)
snap.GetClustCf(G8)


# In[ ]:




