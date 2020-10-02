#!/usr/bin/env python
# coding: utf-8

# This is an attemp to implement [Christofides algorithm](https://en.wikipedia.org/wiki/Christofides_algorithm) using existing libraries for Python, such as scipy, sklearn, networkx.
# 
# First let's import dependencies, that we will be using.

# In[ ]:


import numpy as np
from scipy.spatial import distance, Delaunay, cKDTree
from scipy.sparse import csgraph, coo_matrix
from sklearn.metrics.pairwise import paired_euclidean_distances
import networkx as nx


# Next, let's load cities data from [Traveling Santa 2018](https://www.kaggle.com/c/traveling-santa-2018-prime-paths/data)

# In[ ]:


all_cities = np.loadtxt("../input/cities.csv", delimiter=",", skiprows=1)
N = all_cities.shape[0]
cities = all_cities[0:N,1:3]


# Then, we'll define methods to calculate distances for path and for list of edges, as well as transition methods between sparse matrices and lists of edges. 

# In[ ]:


def pathDists(path):
    pcities = cities[path]
    return paired_euclidean_distances(pcities[1:], pcities[:-1])

def linesToDists(lines):
    return paired_euclidean_distances(cities[lines[:,0]],cities[lines[:,1]])

def linesToMatrix(lines):
    dists = linesToDists(lines)
    return coo_matrix((dists, (lines[:,0],lines[:,1])), (N, N)).todok()

def linesToCountMatrix(lines):
    return coo_matrix((np.full((lines.shape[0],), 1), (lines[:,0],lines[:,1])), (N, N)).tocsr()

def matrixToLines(matrix):
    mTuple = np.nonzero(matrix)
    return np.column_stack(mTuple)

def matrixNormalize(matrix):
    mTuple = np.nonzero(matrix)
    matrix[mTuple[::-1]] = matrix[mTuple]


# Step 1: Get sparce matrix of distances only for Delaunay triangulation

# In[ ]:


tri = Delaunay(cities)
indptr, indv2 = tri.vertex_neighbor_vertices
indv1 = np.arange(indv2.shape[0])
for i in range(N):
    indv1[indptr[i]:indptr[i+1]] = i
triLines = np.column_stack((indv1,indv2))
triMatrix = linesToMatrix(triLines)


# Step 2: Get list of edges of Minimum Spanning Tree

# In[ ]:


mstMatrix = csgraph.minimum_spanning_tree(triMatrix, True)
mstLines = matrixToLines(mstMatrix)
order = mstLines.argsort(axis=1)
mstLines = mstLines[np.arange(order.shape[0])[:,None], order]
mstLines = np.unique(mstLines, axis=0)
print("MST", linesToDists(mstLines).sum(), np.sum(mstMatrix))


# Step 3: Reduce number of vertices with odd rank by linking closest vertices with odd rank.

# In[ ]:


mstRanks = np.bincount(mstLines.flatten())
mstOddIndices = np.nonzero(mstRanks % 2 == 1)[0]
oddCities = cities[mstOddIndices]
mstOddTree = cKDTree(oddCities)
mstOddClosestDists, mstOddClosestIndices = mstOddTree.query(oddCities, 2)
mstOddClosestLines1 = np.column_stack((mstOddIndices,mstOddIndices[mstOddClosestIndices[:, 1]]))
order = mstOddClosestLines1.argsort(axis=1)
mstOddClosestLines1 = mstOddClosestLines1[np.arange(order.shape[0])[:,None], order]
mstOddClosestLines1 = np.unique(mstOddClosestLines1, axis=0)
mstOverLines = np.concatenate((mstLines, mstOddClosestLines1), axis=0)
mstRanks = np.bincount(mstOverLines.flatten())


# Step 3.5: Remove duplicated edges added on previous step if they don't reduce number of vertices with odd rank.

# In[ ]:


mstUniqueLines, counts = np.unique(mstOverLines, axis=0, return_counts=True)
goodRepeats = mstUniqueLines[(counts > 1) * ((mstRanks[mstUniqueLines[:,0]] % 2 == 0) + (mstRanks[mstUniqueLines[:,1]] % 2 == 0))]
mstLines = np.concatenate((mstUniqueLines, goodRepeats), axis=0)
mstRanks = np.bincount(mstLines.flatten())
goodRepeats = goodRepeats[(mstRanks[goodRepeats[:,0]] == 2) + (mstRanks[goodRepeats[:,1]] == 2) + (mstRanks[goodRepeats[:,0]] % 2 == 0) * (mstRanks[goodRepeats[:,1]] % 2 == 0)]
mstLines = np.concatenate((mstUniqueLines, goodRepeats), axis=0)
mstRanks = np.bincount(mstLines.flatten())
goodRepeats = goodRepeats[(mstRanks[goodRepeats[:,0]] % 2 == 0) + (mstRanks[goodRepeats[:,1]] % 2 == 0)]
mstLines = np.concatenate((mstUniqueLines, goodRepeats), axis=0)
print("MST odd", linesToDists(mstLines).sum())


# Step 4: Among vertices, that still have odd rank, for each vertex find 5 closest vertices.

# In[ ]:


mstRanks = np.bincount(mstLines.flatten())
mstOddIndices = np.nonzero(mstRanks % 2 == 1)[0]
M = mstOddIndices.shape[0]
invOddIndices = np.full((N,), -1)
invOddIndices[mstOddIndices] = np.arange(M)
oddCities = cities[mstOddIndices]
mstOddTree = cKDTree(oddCities)
mstOddClosestDists, mstOddClosestIndices = mstOddTree.query(oddCities, 6)
mstOddClosestLines1 = np.column_stack((np.arange(M),mstOddClosestIndices[:, 1]))
mstOddClosestLines2 = np.column_stack((np.arange(M),mstOddClosestIndices[:, 2]))
mstOddClosestLines3 = np.column_stack((np.arange(M),mstOddClosestIndices[:, 3]))
mstOddClosestLines4 = np.column_stack((np.arange(M),mstOddClosestIndices[:, 4]))
mstOddClosestLines5 = np.column_stack((np.arange(M),mstOddClosestIndices[:, 5]))


# Step 5: And build sparse matrix only of those edges, making sure they all create single Connected Component.

# In[ ]:


triOddLines = triLines[(mstRanks[triLines[:,0]] % 2 == 1) * (mstRanks[triLines[:,1]] % 2 == 1)]
triOddLines = invOddIndices[triOddLines]
oddLines = np.concatenate((triOddLines, mstOddClosestLines1, mstOddClosestLines2, mstOddClosestLines3, mstOddClosestLines4, mstOddClosestLines5), axis=0)
oddDists = paired_euclidean_distances(oddCities[oddLines[:,0]],oddCities[oddLines[:,1]])
oddMatrix = coo_matrix((oddDists, (oddLines[:,0],oddLines[:,1])), (M, M)).todok()
n_components, labels = csgraph.connected_components(oddMatrix, directed=False, return_labels=True)
print(n_components, np.bincount(labels))
nxMatrix = nx.from_scipy_sparse_matrix(-oddMatrix)


# Step 6: Find Minimum Weight Perfect Matching for matrix built on previous step

# In[ ]:


matching = nx.max_weight_matching(nxMatrix, maxcardinality=True)
matchingLines = np.array([[key,val] for (key,val) in list(matching)])
matchingLines = mstOddIndices[matchingLines]
print("Perfect", linesToDists(matchingLines).sum())

# leave only necessary edges
mstLines = np.concatenate((mstLines, matchingLines), axis=0)
mstRanks = np.bincount(mstLines.flatten())
matchingLines = mstLines[(mstRanks[mstLines[:,0]] % 2 == 1) + (mstRanks[mstLines[:,1]] % 2 == 1)]


# Step 7: Join found edges with edges found previously to produce Eulerian graph. Find Eulerian Circuit in that graph

# In[ ]:


eulerianMatrix = nx.MultiGraph()
eulerianMatrix.add_edges_from(mstLines)
eulerianMatrix.add_edges_from(matchingLines)
circuit = nx.eulerian_circuit(eulerianMatrix,source=0)
circuitLines = np.array([[key,val] for (key,val) in list(circuit)])
print("Circuit", linesToDists(circuitLines).sum())


# Step 8: Shortcut Eulerian circuit to produce Path

# In[ ]:


path, order = np.unique(circuitLines.flatten(), return_index=True)
path = order.argsort()


# Finally, validate and save produced path

# In[ ]:


print("Path", pathDists(path).sum())
zeroIdx = np.argmin(path)
path = np.roll(path, -zeroIdx)
path = np.append(path, 0)

np.savetxt('submission.csv', path, fmt='%d', header='Path', comments='')
np.savetxt('submission_inv.csv', path[::-1], fmt='%d', header='Path', comments='')

