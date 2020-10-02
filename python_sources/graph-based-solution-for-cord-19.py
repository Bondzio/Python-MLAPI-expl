#!/usr/bin/env python
# coding: utf-8

# # About this notebook
# This notebook is focused on the task: "What has been published about ethical and social science considerations?" of the COVID-19 Open Research Dataset Challenge (CORD-19). For calculation purposes, a smaller part of the CORD-19 corpus will be used, filtered by social and ethical terms. Nevertheless, the whole approach can be perfectly replicated for the whole dataset resulting in meaningfull outcomes.
# 
# The **objective** of this submission is to map the CORD-19 articles' corpus in a network. The graph structure will allow the scientific community to reveal 'hidden' properties otherwise hardly distinguishable. We believe that articles could be mapped closer together in the topological space of a graph when sharing many and different attributes. This characteristic of graphs could be of great use in future analysis and exploitation.
# 
# <a id="section-one"></a>
# # 1. Contents
# * [1. Contents](#section-one)
# * [2. The idea](#section-two)
# * [3. The data](#section-three)
# * [4. Building the graph](#section-four)
#     - [4.1 Similarity-based links](#section-four-one)
#     - [4.2 Other attribute-based links](#section-four-two)
#     - [4.3 Transforming into a multigraph](#section-four-three)
# * [5. Common neighbours](#section-five)
# * [6. Future work](#section-six)
# 
# <a id="section-two"></a>
# # 2. The idea
# The initial, most adecuate idea as a response to the challenge was to build a graph database containing all information related to the corpus as visualised in the following diagram. This approach would allow the use of graph algorithms and metrics to infer more information on the corpus.

# In[ ]:


from IPython.display import Image
Image("../input/cord19images/GraphDatabase.png")


# Of course, space, time and means were limited, so the decision was to explore the functionalities of [networkx](http://https://networkx.github.io/) library of Python and transform the initial idea of a graph database into a graph of type Multigraph. A multigraph permits the use of multiple connections between elements. For example, article A can share with B different attributes, such as being written by the same author, published in the same journal, talking about the same subject, etc. In this approach, all those sharing attributes will be represented as links and with the articles forming the nodes. The following diagram gives an example of possible connections between articles. 

# In[ ]:


Image("../input/cord19images/Mulltigraph.png")


# As you may have observed, links between articles in the previous diagram differ in thicknesses. The idea is to assign a weight in each link and work with weighted networks. Higher weights will allow articles to be mapped closer together in the topological space of the graph. This distribution in the "graph's space" will allow in the future the application of metrics and algorithms that will reveal the important properties of the nodes (articles). Some examples are: centrality measures,  communities or clusters, closer neighbours, etc.

# <a id="section-three"></a>
# # 3. The data
# 
# As mentioned previously, the focus here will be on articles related to COVID and to social and ethical considerations. The imported dataset is a filtered, by social and ethical terms, version of the initial CORD-19 corpus. It includes the full text of the articles and also contains further information. This information is a result of a previous [notebook](http://www.kaggle.com/jredondopizarro/cord-19-semantic-similarities-with-use-and-doc2vec) containing similarities between titels, abstracts and full texts. The similarities between titles and between abstracts were calculated using the Universal Sentence Encoder (USE) model applying cosine distance between vector embeddings and the ones between the full texts using a doc2vec model.

# In[ ]:


# Import libraries
import covid19_tools as cv19
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pickle
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt


# In[ ]:


with open(r"/kaggle/input/semantic-similarities-with-use-and-doc2vec/output_data/data.pkl", "rb") as input_file:
    df = pickle.load(input_file)
df.head()


# In[ ]:


df.columns


# <a id="section-four"></a>
# # 4. Building the graph
# <a id="section-four-one"></a>
# ## 4.1 Similarity-based links
# We will start building the graph using the three similarities calculated in the previous [notebook](http://www.kaggle.com/jredondopizarro/cord-19-semantic-similarities-with-use-and-doc2vec). The similarity scores will be used as weights for the graphs.

# In[ ]:


#Loading the similarity matrices
use_title_sim_matrix = np.load("/kaggle/input/semantic-similarities-with-use-and-doc2vec/output_data/title_sim.npy")
use_abstract_sim_matrix = np.load("/kaggle/input/semantic-similarities-with-use-and-doc2vec/output_data/abstract_sim.npy")
doc2vec_full_text_sim_matrix = np.load("/kaggle/input/semantic-similarities-with-use-and-doc2vec/output_data/full_text_sim.npy")

#Extracting the articles' ids
index_id = df['cord_uid'].values

#Preparing the dfs that include the ids both as indexes and columns
title_sim_df = pd.DataFrame(use_title_sim_matrix, index = index_id, columns = index_id)
abstract_sim_df = pd.DataFrame(use_abstract_sim_matrix, index = index_id, columns = index_id)
text_sim_df = pd.DataFrame(doc2vec_full_text_sim_matrix, index = index_id, columns = index_id)
title_sim_df.head()


# We may now start building the individual networks, one for each similarity type.

# In[ ]:


#Creating a dictionary with the nodes (articles)
nodes_dict = dict([x for x in enumerate(index_id)])

#Initialise graph of title similarities
G_title = nx.from_numpy_matrix(np.matrix(use_title_sim_matrix), create_using=nx.Graph) # Creates a graph from a numpy matrix
G_title = nx.relabel_nodes(G_title,nodes_dict) # Relabels the nodes using the Ids
G_title.remove_edges_from(nx.selfloop_edges(G_title)) # Removes selfloops
print("Number of title-graph nodes: {0}, Number of graph edges: {1} ".format(len(G_title.nodes()), G_title.size()))

#Initialise graph of abstract similarities
G_abstract = nx.from_numpy_matrix(np.matrix(use_abstract_sim_matrix), create_using=nx.Graph) # Creates a graph from a numpy matrix
G_abstract = nx.relabel_nodes(G_abstract,nodes_dict) # Relabels the nodes using the Ids
G_abstract.remove_edges_from(nx.selfloop_edges(G_abstract)) # Removes selfloops
print("Number of abstract-graph nodes: {0}, Number of graph edges: {1} ".format(len(G_abstract.nodes()), G_abstract.size()))

#Initialise graph of abstract similarities
G_text = nx.from_numpy_matrix(np.matrix(doc2vec_full_text_sim_matrix), create_using=nx.Graph) # Creates a graph from a numpy matrix
G_text = nx.relabel_nodes(G_text,nodes_dict) # Relabels the nodes using the Ids
G_text.remove_edges_from(nx.selfloop_edges(G_text)) # Removes selfloops
print("Number of text-graph nodes: {0}, Number of graph edges: {1} ".format(len(G_text.nodes()), G_text.size()))


# As an example, we may check the edges of a concrete node to see its connections. 

# In[ ]:


# Check edges of node 'wyz5jyjh'
G_title.edges('wyz5jyjh', data = True)


# We can now save the individual graphs to dfs. We will use those dfs later to build the multigraph.

# In[ ]:


#Save title-graph to df
df_G_title = nx.to_pandas_edgelist(G_title)
df_G_title = df_G_title.dropna()
df_G_title['sharing'] = 'title_similarity'
print(df_G_title.shape)

#Save abstract-graph to df
df_G_abstract = nx.to_pandas_edgelist(G_abstract)
df_G_abstract = df_G_abstract.dropna()
df_G_abstract['sharing'] = 'abstract_similarity'
print(df_G_abstract.shape)

#Save text-graph to df
df_G_text = nx.to_pandas_edgelist(G_text)
df_G_text = df_G_text.dropna()
df_G_text['sharing'] = 'text_similarity'
print(df_G_text.shape)
df_G_text.head()


# <a id="section-four-two"></a>
# ## 4.2 Other attribute-based links
# 
# The similarity links where the only direct links between articles of the graph. All the other links are projections of bipartite graphs.
# 
# There is a long list of existing attributes in the dataset that could be used as sharing properties of the articles and translated into links in our graph. For example, articles could share Journal, Authors, Citations, Tag, etc.

# In[ ]:


df.columns


# <a id="section-four-two-one"></a>
# ### 4.2.1 Sharing Journal attribute
# Of the previously mentioned sharing attribute we selected to represent the sharing journal one. The process can be repeated for the rest of the attributes. 
# 
# We believe that articles appearing in the same Journal usually share similar context and should be mapped closer together. The process is similar to the similarities' graphs but here we will start working with bipartite networks, i.e., networks that include two types of nodes. In our case the types of nodes will be articles and journals.
# 
# We detected 649 journals missing, those rows will be exluded.

# In[ ]:


# Create article-journal df and drop na
article_journal_df = df[['cord_uid', 'journal']].dropna()
print(article_journal_df.shape)
article_journal_df.head()


# In[ ]:


#Initialise the article journal graph
G_article_journal = nx.Graph()

#Add nodes from df
G_article_journal.add_nodes_from(article_journal_df['cord_uid'].unique(), bipartite = 'articles')
G_article_journal.add_nodes_from(article_journal_df['journal'].unique(), bipartite = 'journals')

#Add edges from df
G_article_journal.add_edges_from(zip(article_journal_df['cord_uid'], article_journal_df['journal']))

print("Number of graph nodes: {0}, Number of graph edges: {1} ".format(len(G_article_journal.nodes()), G_article_journal.size()))


# It's important here to understand the difference between a normal and a bipartite graph: The bipartite nodes contain an extra attribute indicating the type. In our case this would be 'article' or 'journal'.

# In[ ]:


G_article_journal.nodes['wyz5jyjh']


# Now that we have the bipartite graph created we will check again for our favourite first node. We see that it is only connected to one journal: Clinical eHealth.

# In[ ]:


# Check edges of node 'wyz5jyjh'
G_article_journal.edges('wyz5jyjh', data = True)


# We will now extract the projection of the bipartite article - journal graph on the articles type of nodes. Extracting the projection on journals makes no sense as they are not connected. They would be if an article (or more) was written in two journals which is not possible. 

# In[ ]:


# Prepare the nodelists needed for computing projections: articles, journals
articles = [n for n in G_article_journal.nodes() if G_article_journal.nodes[n]['bipartite'] == 'articles']
journals = [n for n, d in G_article_journal.nodes(data=True) if d['bipartite'] == 'journals']

# Compute the article projections: articlesG
articlesG = nx.bipartite.projected_graph(G_article_journal, articles)
print("Number of articles graph nodes: {0}, Number of graph edges: {1} ".format(len(articlesG.nodes()), articlesG.size()))


# While we create those graphs we can play with and check different metrics, for example, the degree centrality distribution.

# In[ ]:


# Calculate the degree centrality using nx.degree_centrality: dcs
dcs = nx.degree_centrality(articlesG)
# Plot the histogram of degree centrality values
plt.hist(list(dcs.values()))
#plt.yscale('log')  
plt.show() 


# We will now transform the projection of the bipartite graph on articles to a simple graph. We'll do that because we want to add the weight attribute to the edges. As mentioned previously, weights are important as they indicate if articles should be mapped closer together. In this case, the weight is not trivial as it was with the similarity scores but could try with a weight of 0.2. In any case it can be changed in the future.

# In[ ]:


# Transform graph into a simple graph (not bipartite) and add a weight of 0.2
G_journals = nx.Graph()
for (u, v) in articlesG.edges():
    G_journals.add_edge(u,v,weight=0.2)

print("Number of articles graph nodes: {0}, Number of graph edges: {1} ".format(len(G_journals.nodes()), G_journals.size()))


# In[ ]:


G_journals.edges('aeogp8c7', data = True)


# We can now save the graph in a df format as we deed with the similarities ones. We will use it to build the multigraph.

# In[ ]:


#Save text-graph to df
df_G_journals = nx.to_pandas_edgelist(G_journals)
#df_G_journals = df_G_text.dropna()
df_G_journals['sharing'] = 'journal'
print(df_G_journals.shape)
df_G_journals.head()


# <a id="section-four-three"></a>
# ## 4.3 Transforming into a Multigraph
# To build the multifgraph we will first append all individual dfs we created from the graphs.

# In[ ]:


#Append the edgelists dfs
df_G_similarities = df_G_title.append(df_G_abstract, ignore_index=True)
df_G_similarities = df_G_similarities.append(df_G_text, ignore_index=True)
df_G_similarities = df_G_similarities.append(df_G_journals, ignore_index=True)
print(df_G_similarities.shape)
df_G_similarities.head()


# And then initialise a graph of type Multigraph. We can see that although the number of nodes haven't increased, the number of edges is almost the triple.

# In[ ]:


# Create Multigraph
M = nx.to_networkx_graph(df_G_similarities, create_using=nx.MultiGraph)
print("Number of multigraph nodes: {0}, Number of graph edges: {1} ".format(len(M.nodes()), M.size()))


# If we now check again the initial example node we will see that it has multiple edges with different weights and sharing attributes with other nodes (articles).

# In[ ]:


# Check edges of node 'wyz5jyjh'
M.edges('wyz5jyjh', data = True)


# We will now export the multigraph in a pickle for future use.

# In[ ]:


nx.write_gpickle(M, '/kaggle/working/cord19_multigraph.gpickle')


# <a id="section-five"></a>
# # 5. Common neighbours
# A simple analysis towards building a recommender system is that of a node's neighbours and common neighbours between two nodes. 

# In[ ]:


nbrs1 = M.neighbors('wyz5jyjh')
print(len(list(nbrs1)))


# In[ ]:


def shared_nodes(G, node1, node2):

    # Get neighbors of node 1: nbrs1
    nbrs1 = G.neighbors(node1)
    # Get neighbors of node 2: nbrs2
    nbrs2 = G.neighbors(node2)

    # Compute the overlap using set intersections
    overlap = set(nbrs1).intersection(nbrs2)
    return overlap

#Check the number of shared nodes between the first and second article
print(len(shared_nodes(M, 'wyz5jyjh', 'aeogp8c7')))


# Of course, as we have already added 4 different graphs in our multigraph, almost all nodes will be connected to each other. What we should create is a recommender system using and based on the weights of the edges.

# <a id="section-six"></a>
# # 6. Future work
# * Build visual representations of parts of the network
# * Recommender systems
# * Integrate more data sources as attributes in the graph (sharing authors, citations, tags...)
# * Apply a clustering or community detection algorithm to find the articles closely related together
# * Apply topic modelling and extract main concepts of each cluster
# * Extend analysis to the complete corpus

# In[ ]:




