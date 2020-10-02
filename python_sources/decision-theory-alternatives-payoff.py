#!/usr/bin/env python
# coding: utf-8

# **Decision Theory**
# Consider the following four alternatives and the payoffs under three states of nature. Using the different criteria, select the associated decisions. (Hence we would choose the one which is financially convincing)
# ![Imgur](https://i.imgur.com/TEX5jaQ.png)
# Copyright @Tanmoy Das

# In[ ]:


# Import necessary libraries & the dataset
import pandas
data_df = pandas.read_csv("../input/Decision_Theory_alternatives_and_payoff_dataset.csv")
#df = data_df.set_index([0])
#data_matrix = data_df[1:][0:]
data_matrix = data_df.iloc[1:5, 1:4] # first two columns of data frame with all rows
print(data_matrix)


# # Applying Decision theory related optimization algorithm
# ## Lets start with Game theory
# ## Maximax
# 1. We need to determine the maximum value for each alternatives (i.e. maximum we can gain by pursuing MS in Industrial Engineering, Getting MBA, landing a job and giving a startup)
# 2. Find the maximum of the maximum values

# In[ ]:


max_inner = []  # max_inner = list()
for i in range(len(data_matrix)):  #why len NOT just type 4  #data_matrix.shape[0]
    max_inner_ith = max(data_matrix.iloc[i])
    max_inner.append(max_inner_ith)
    # print(max_inner)
maximax_dt = max(max_inner)    
max_inner.index(max(max_inner))
data_df.iloc[max_inner.index(max(max_inner))+1,0] # Call the name of the alternative


# In[ ]:


min_inner = []  # max_inner = list()
for i in range(len(data_matrix)):  #why len NOT just type 4  #data_matrix.shape[0]
    min_inner_ith = min(data_matrix.iloc[i])
    min_inner.append(min_inner_ith)
    # print(max_inner)
maximax_dt = max(min_inner)    
data_df.iloc[max_inner.index(max(min_inner))+1,0] # Call the name of the alternative


# **Bayes weighted 
# **

# In[ ]:


weight = data_df.iloc[0]
weighted_average_of_alternate = []
#Sample calculation
weighted_average_of_Pursuing_MS_in_IE = weight[1]*data_matrix.iloc[0,0]+weight[2]*data_matrix.iloc[0,1]+weight[3]*data_matrix.iloc[0,2]
weighted_average_of_alternate_1 = 0
for k in range (data_matrix.shape[0]):
    for j in range (data_matrix.shape[1]):
        weighted_average_of_alternate_1 += weight[j+1]*data_matrix.iloc[k,j]
    weighted_average_of_alternate.append(weighted_average_of_alternate_1)
bayes_weighted_dt = max(weighted_average_of_alternate)    
data_df.iloc[weighted_average_of_alternate.index(bayes_weighted_dt)+1,0] # Call the name of the alternative


# In[ ]:




