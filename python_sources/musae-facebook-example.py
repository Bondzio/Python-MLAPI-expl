#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
import pandas as pd
import networkx as nx
from scipy import sparse
from sklearn.metrics import f1_score
from sklearn.decomposition import NMF, TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, ElasticNet


# In[ ]:


target = pd.read_csv("/kaggle/input/musae-facebook-pagepage-network/musae_facebook_target.csv")
features = pd.read_csv("/kaggle/input/musae-facebook-pagepage-network/musae_facebook_features.csv")
edges = pd.read_csv("/kaggle/input/musae-facebook-pagepage-network/musae_facebook_edges.csv")


# In[ ]:


def transform_features_to_sparse(table):
    table["weight"] = 1
    table = table.values.tolist()
    index_1 = [row[0] for row in table]
    index_2 =  [row[1] for row in table]
    values =  [row[2] for row in table] 
    count_1, count_2 = max(index_1)+1, max(index_2)+1
    sp_m = sparse.csr_matrix(sparse.coo_matrix((values,(index_1,index_2)),shape=(count_1,count_2),dtype=np.float32))
    return sp_m


# In[ ]:


def normalize_adjacency(raw_edges):
    raw_edges_t = pd.DataFrame()
    raw_edges_t["id_1"] = raw_edges["id_2"]
    raw_edges_t["id_2"] = raw_edges["id_1"]
    raw_edges = pd.concat([raw_edges,raw_edges_t])
    edges = raw_edges.values.tolist()
    graph = nx.from_edgelist(edges)
    ind = range(len(graph.nodes()))
    degs = [1.0/graph.degree(node) for node in graph.nodes()]
    A = transform_features_to_sparse(raw_edges)
    degs = sparse.csr_matrix(sparse.coo_matrix((degs, (ind, ind)), shape=A.shape,dtype=np.float32))
    A = A.dot(degs)
    return A


# In[ ]:


def mapper(x):
    if x =="politician":
        y = 0
    elif x =="company":
        y = 1
    elif x =="government":
        y = 2
    else:
        y = 3
    return y


# In[ ]:


target = target["page_type"].values.tolist()
y = np.array([mapper(t) for t in target])
A = normalize_adjacency(edges)
X = transform_features_to_sparse(features)
X_tilde = A.dot(X)


# In[ ]:


def eval_factorization(W,y):
    scores = []
    for i in range(10):
        X_train, X_test, y_train, y_test = train_test_split(W, y, test_size=0.9, random_state = i)
        model = LogisticRegression(C=0.01, solver = "saga",multi_class = "auto")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = f1_score(y_test, y_pred, average = "weighted")
        scores.append(score)
    print(np.mean(scores))


# In[ ]:


model = TruncatedSVD(n_components=16, random_state=0)
W = model.fit_transform(X)
model = TruncatedSVD(n_components=16, random_state=0)
W_tilde = model.fit_transform(A)


# In[ ]:


eval_factorization(W, y)
eval_factorization(np.concatenate([W,W_tilde],axis=1), y)


# In[ ]:




