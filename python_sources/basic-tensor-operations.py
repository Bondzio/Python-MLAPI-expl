#!/usr/bin/env python
# coding: utf-8

# # Basic Torch tensor functions
# 
# 
# An short introduction about PyTorch and about the chosen functions. 
# - torch.add
# - torch.bernoulli
# - torch.randn
# - torch.dot
# - torch.rot90

# ## What is a Tensor
# 
# Tensor is a datasturcuture that can store data in N dimensions. Tensors have uniform data type and are immutable

# In[ ]:


# Import torch and other required modules
import torch


# ## Function 1 - torch.add
# 
# This functions adds 2 tensor. The 2 tensor can be of different shape but broadcastable.
# The data type of resulting tensor is that of larger data type to avoid the loss of data.

# In[ ]:


# Example 1 - working (change this)
first_tensor = torch.tensor([[1, 2], [3, 4]])
second_tensor = torch.tensor([[3.2, 5]])

result = torch.add(first_tensor, second_tensor)
print(result)
print("Data type of result",result.dtype)
print("Data type of first_tensor",first_tensor.dtype)
print("Data type of second_tensor",second_tensor.dtype)


# The example 2 shows the usage of optional argument alpha.
# If alpha is set then each element of the second tensor  is multiplied by the scalar alpha and added to each element of the first tensor.
# Also even Boolean data type tensor can be added to int data type tensor

# In[ ]:


# Example 2 - working
first_tensor = torch.tensor([[1, 2], [3, 4.]])
second_tensor = torch.tensor([[False, True]])
result = torch.add(first_tensor, second_tensor)
print(result)
print("Result after setting alpha to 2")
result = torch.add(first_tensor, second_tensor, alpha = 2)
print(result)


# The 3rd example shows when the function add can break.
# One of the top reasons for this function to fail if if 2 tensors are not broadcastable as shown below

# In[ ]:


# Example 3 - breaking (to illustrate when it breaks)
first_tensor = torch.tensor([[1, 2], [3, 4]])
second_tensor = torch.tensor([[3.2, 5, 3]])

result = torch.add(first_tensor, second_tensor)


# torch.add function is handly anytime 2 tensor are to be added or the tensor has to be inflated by a scalar value.

# ## Function 2 -  torch.bernoulli
# 
# Draws binary random numbers (0 or 1) from a Bernoulli distribution.
# 
# Here input tensor to function bernoulli is probabilities and should be between 0 and 1

# In[ ]:


# Example 1 - working
input_prob = torch.tensor([[0.5, 0.5],[1,0], [0.3, 0.7]])
torch.bernoulli(input_prob)


# The example 2 below shows that shape of input probabilities and output tensor is always same

# In[ ]:


# Example 2 - working
input_prob = torch.tensor([[0, 0.5, 1]])
torch.bernoulli(input_prob)


# Input proabilities tensor given to bernoulii must be of type float. In teh below example, whiule the probailities are between 0 and 1 but are of data type int. This breaks the bernoulii function

# In[ ]:


# Example 3 - breaking (to illustrate when it breaks)
input_prob = torch.tensor([[0, 0, 1]])
print("Data Type of input probabilities", input_prob.dtype)
torch.bernoulli(input_prob)


# torch.bernoulli is a statistical function and is useful when objective is to draw numbers based on pre-determined (in this case bernoulli distribution) distribution.

# ## Function 3 - torch.randn
# 
# This function returns a tensor filled with random numbers from a uniform distribution.
# This function mandatorily requires one argument which is is size of expected output tensor
# 
# The example below shows working of randn

# In[ ]:


# Example 1 - working
torch.randn((3,4))


# The example below shows how to set data type for randn and that scalar tensor can also be generated by this

# In[ ]:


# Example 2 - working
torch.randn((1), dtype = torch.float32 )


# The example below shows that randn is not yet implemented for data type long for CPU exdecution

# In[ ]:


# Example 3 - breaking (to illustrate when it breaks)
torch.randn((1), dtype = torch.long )


# This function can be used to initialize weights and bias of Neural networks layers

# ## Function 4 - torch.dot
# 
# torch.add computes inner product of 2 1-D tensors

# In[ ]:


# Example 1 - working
torch.dot(torch.tensor([2, 3, 4]), torch.tensor([2, 1, 5]))


# The above example shows simple matrix multiplication of 1-D tensors

# In[ ]:


# Example 2 - working
torch.dot(torch.tensor([0.0, 2, 3, 4]), torch.tensor([2.0, 5.5, 0, 1]))


# The above 2 examples show output datatype is same as data type of input tensors

# In[ ]:


# Example 3 - breaking (to illustrate when it breaks)
torch.dot(torch.tensor([2.0, 5.5, 0, 1]), torch.tensor([0, 2, 3, 4]))


# The above example shows that data type of both input tensors should be samee

# This function to be used when funding inner product of 2 1-D tensors of same data type

# ## Function 5 - torch.rot90
# 
# Function to rotate the given tensor by 90 degrees

# In[ ]:


# Example 1 - working
input_tensor = torch.tensor([[1, 2], [3, 4]])
torch.rot90(input_tensor, k = 1, dims= [0,1])


# The above tensor is rotated 90 degrees anticlockwise based on axis 1

# In[ ]:


# Example 2 - working
input_tensor = torch.tensor([[1, 2], [3, 4]])
torch.rot90(input_tensor, k = 1, dims= [1,0])


# The above tensor is rotated 90 degrees clockwise based on axis 0

# In[ ]:


# Example 3 - breaking (to illustrate when it breaks)
input_tensor = torch.tensor([[1, 2], [3, 4]])
torch.rot90(input_tensor, k = 1, dims= [1])


# torch.rot90 requires both dimesnions of tensor as input else it breaks

# Closing comments about when to use this function

# ## Conclusion
# 
# This notebook summarizes some of the basic functionalities provided by torch tensors. To know more about these basic functionalities refer https://pytorch.org/docs/stable/tensors.html

# ## Reference Links
# Provide links to your references and other interesting articles about tensors
# * Official documentation for `torch.Tensor`: https://pytorch.org/docs/stable/tensors.html

# In[ ]:


get_ipython().system('pip install jovian --upgrade --quiet')


# In[ ]:


import jovian


# In[ ]:


jovian.commit()


# In[ ]:




