#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install mip')
get_ipython().system('pip install pulp')

import os
from shutil import copyfile
import pandas as pd
import numpy as np
import random
import mip.model as mip
import pulp as pulp
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import glob
from IPython.display import Image, display


# ## Define the parameters of the model

# In[ ]:


T=200 #Training time period
C=100000 #Capital available
file=1 #Index_file
m=12 #Inital Size of Kernel
lbuck=3 #Size Of Buckets
lamda=1/(100*C) # lower_bound for capital invested in jth stock
nuh=0.65  # upper_bound
xii=0.8 # Limit for Tracking Error
k=12 #Cardinality constraint for stocks in portfolio
p=3 #If stock not selected in optimal soln in last p iters then it is to be dropped from kernel
#Rest parameters are defined inside underlying scripts


# # Initialisation Phase of Basic Kernel Search
# ### Run the Linear Relaxation part and store the results
# The linear_relaxation script takes argument --index_file --T --xii --k

# In[ ]:


copyfile(src = "../input/utility-scripts/linear_relaxation.py", dst = "../working/linear_relaxation.py")
get_ipython().system('python linear_relaxation.py 1 200 0.8 12')


# In[ ]:


""" Collect results of Linear Relaxation """
text_file=open("EIT_LP_details.txt")
lines=text_file.readlines()
failure=bool(int(lines[0][-2]))
z_lp=float(lines[1].split("=")[-1][:-2])
result_lp=pd.read_csv("result_index_{}.csv".format(file))

""" Display results of Linear Relaxation """
Image(filename='LP_EIT for index_{}.jpg'.format(file))


# ### Sort the securities and create buckets

# In[ ]:


# Import the sorting script
copyfile(src = "../input/utility-scripts/sort_and_buckets.py", dst = "../working/sort_and_buckets.py")
from sort_and_buckets import *

# Create dummy problem using PULP
LP,q_T=dummy_problem(T,C,file)
q_T.drop("index",inplace=True)
objective=LP.objective

#Create ranked list and buckets
L=sort_securities(result_lp,q_T,objective,lamda,C) #Ranked List
kernel=L[:m]
initial_kernel=L[:m] #Create copy of Initial Kernel
buckets=create_buckets(L,m,lbuck)
Nb=len(buckets)


# ### Solve EIT(kernel) and get lower-bound for kernel search and plot EIT(Kernel)

# In[ ]:


# Import the EIT_kernel script
copyfile(src = "../input/utility-scripts/EIT_kernel.py", dst = "../working/EIT_kernel.py")
from EIT_kernel import *

try:
    status,z=EIT_kernel(kernel,C,T,file,lamda,nuh,xii,k)
    failure=bool(status==1)
except:
    print ("ERROR in EIT Kernel")

execution_result=pd.DataFrame()
temp=pd.DataFrame()
temp["bucket"]=[0]
temp["kernel_size"]=[len(kernel)]
temp["problem_status"]=[status]
temp["z_value"]=[z]
execution_result=execution_result.append(temp,ignore_index=True)
result_kernel=pd.read_csv("EIT_kernel_result_index_{}.csv".format(file))
plot_results(kernel,result_kernel,file,T)


# # Execution Phase of Kernel Search

# In[ ]:


"""Initialise p_dict and z_low"""
p_dict={}
for stock in L:
    p_dict[stock]=0
z_low=0.1*z

copyfile(src = "../input/utility-scripts/EIT_bucket.py", dst = "../working/EIT_bucket.py")
from EIT_bucket import *

for i in range(1,Nb+1):
    bucket=buckets[i]
    #Add bucket to kernel
    kernel_copy=kernel.copy()
    kernel=kernel+bucket
    print ("\n\nFor bucket={}".format(str(i)))
    #Solve EIT(K+Bi)
    try:
        status,z,selected=EIT_bucket(kernel,bucket,i,failure,z_low,C,T,file,lamda,nuh,xii,k)
    except:
        print ("Error in this bucket")
        break
    if status==0: #Check if EIT(kernel+bucket) is feasible
        if failure==True: #check if EIT(Kernel) was in-feasible
            failure=False
        #Update lower_bound
        print ("Updating Lower Bound")
        if(0.2*z>z_low):
            z_low=0.2*z
        """Update Kernel"""
        #Add stocks from bucket which are selected in optimal
        print ("Updating Kernel")
        print ("Length of Old Kernel={}".format(len(kernel_copy)))
        kernel=kernel_copy+selected
        print ("Length of Updated Kernel={}".format(len(kernel)))
        #Make p=0 if stock just selected in Kernel
        for stock in selected:
            p_dict[stock]=0
        #Update p_dict
        result_bucket=pd.read_csv("EIT_bucket_{}_result_index_{}.csv".format(i,file))
        plot_results(kernel_copy+bucket,bucket,i,result_bucket,file,T)
        result_bucket.index=result_bucket["security"]
        result_bucket.drop(["security"],axis=1,inplace=True)
        for stock in kernel:
            if (result_bucket.loc[stock]['y']==0):
                p_dict[stock]+=1 #Increase by 1 if not selected in optimal
        #Remove from Kernel
        to_remove=[stock for (stock,p_value) in p_dict.items() if p_value > p]
        for stock in to_remove:
            if stock in kernel:
                print ("Removing {} from kernel".format(stock))
                kernel.remove(stock)
                p_dict[stock]=0
        print ("Current Length Kernel={}".format(len(kernel)))
    else:
        kernel=kernel_copy
    temp=pd.DataFrame()
    temp["bucket"]=[i]
    temp["kernel_size"]=[len(kernel)]
    temp["problem_status"]=[status]
    temp["z_value"]=[z]
    execution_result=execution_result.append(temp,ignore_index=True)


# In[ ]:





# ### Visualise results of the execution phase

# In[ ]:


files=glob.glob("*bucket*.jpg")
files.sort()
for file in files:
    display(Image(filename=file))

