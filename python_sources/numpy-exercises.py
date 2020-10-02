#!/usr/bin/env python
# coding: utf-8

# ![Alt Text](https://i.ibb.co/LkdVVgV/numpy-logo.jpg)
# 

# #  Numpy For Machine Learning
# 
# NumPy, which stands for Numerical Python, is a library consisting of multidimensional array objects and a collection of routines for processing those arrays. Using NumPy, mathematical and logical operations on arrays can be performed.
# 
# NumPy is a Python package. It stands for 'Numerical Python'. It is a library consisting of multidimensional array objects and a collection of routines for processing of array.NumPy has in-built functions for linear algebra and random number generation
# 

# #### Import the numpy package

# In[ ]:


import numpy as np


# #### Print Multiple Outputs from the Cell

# In[ ]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# #### Print the numpy version

# In[ ]:


print(np.__version__)


# #### Create a 1D null vector of size 10 and 2D matrix by 2*2

# In[ ]:


np.zeros(10)
np.zeros(10,dtype=int)
np.zeros((3,2))


# #### Create a null vector of size 10 but the fifth value set to 1.

# In[ ]:


Z = np.zeros(10)
Z
Z[4] = 1
Z


# #### Create a vector with values ranging from 10 to 20

# In[ ]:


np.arange(10,20)
np.linspace(10,20,5)


# #### Reverse a vector (first element becomes last)

# In[ ]:


Z = np.arange(20)
Z = Z[::-1]
print(Z)


# #### Creating the Complex number array

# In[ ]:


np.array([1, 2, 3], dtype = complex)


# #### DataType

# In[ ]:


x = np.array([1, 2])   # Default datatype
print(x.dtype)
x = np.array([1.0, 2.0])
print(x.dtype)
x = np.array([1, 2], dtype=np.int64)
print(x.dtype) 


# #### Create a 3x3 matrix with values ranging from 0 to 8.

# In[ ]:


np.arange(9).reshape(3,3)


# #### Find indices of non-zero elements from array \[1,2,0,0,4,0\] 

# In[ ]:


np.nonzero([1,2,0,0,4,0])


# #### Create a 3x3 identity matrix

# In[ ]:


np.eye(3)


# #### Create a 3x3x3 array with random values

# In[ ]:


Z = np.random.random((3,3,3))
print(Z)


# #### Create a 5x5 array with random values and find the minimum and maximum values

# In[ ]:


Z = np.random.random((5,5))
Z
Z.min()
Z.max()
Z.mean()


# #### Create a 2d array and Pad with zeros

# In[ ]:


Z = np.ones((5,5))
Z
np.pad(Z, pad_width=1, mode='constant', constant_values=0)


# #### Print Result of expression involving nan & inf

# In[ ]:


print(0 * np.nan)
print(np.nan == np.nan)
print(np.inf > np.nan)
print(np.nan - np.nan)
print(np.nan in set([np.nan]))
print(0.3 == 3 * 0.1)


# #### Slicing and Dicing 1D and 2D array with Advanced Indexing

# In[ ]:


a = np.arange(10)
a
##(start:stop:step)
a[2:7:2] 
a[4:]


# In[ ]:


a = np.array([[1,2,3],[3,4,5],[4,5,6]]) 
a 
# Returns array of items in the second column 
a[...,1]
# Will slice all items from the second row 
a[1,...] 
# Will slice all items from column 1 onwards 
a[...,1:]
# Slicing using advanced index for column
a[1:3,[1,2]]


# #### Broadcasting the array with multiplication and addition of arrays

# ![Alt Text](https://i.ibb.co/ZHC17vD/Broadcasting-Array.png)

# In[ ]:


a = np.array([1,2,3,4]) 
b = np.array([10,20,30,40]) 
a * b
# First Array + Second Array
a = np.array([[0.0,0.0,0.0],[10.0,10.0,10.0],[20.0,20.0,20.0],[30.0,30.0,30.0]]) 
b = np.array([0.0,1.0,2.0]) 
a + b


# #### Multiply a 5x3 matrix by a 3x2 matrix (real matrix product)

# ![Alt Text](https://i.ibb.co/2vcTD8w/matrix-product.png)

# In[ ]:


np.dot(np.ones((5,3)), np.ones((3,2)))
np.dot(np.array([[1,7],[2,4]]),np.array([[3,3],[5,2]]))


# #### Given a 1D array, negate all elements which are between 3 and 8, in place.

# In[ ]:


Z = np.arange(11)
Z
Z[(3 < Z) & (Z <= 8)] *= -1
Z
# Will print the items greater than 5
Z[Z > 5]


# #### Iterating Over all item in array and transposed the array

# In[ ]:


a = np.arange(0,60,5).reshape(3,4)
a
for x in np.nditer(a):
    print(x,end=' ')
# The flattened array is
a.flatten()
# Transposed from (3,4) to (4,3)
a.T


# #### Horizontal and Vertical Stacking

# In[ ]:


a = np.array([[1,2],[3,4]])
b = np.array([[5,6],[7,8]])
# Horizontal stacking
np.hstack((a,b))
# Vertical stacking
np.vstack((a,b)) 


# #### Finding Sine and tan

# In[ ]:


a = np.array([0,30,45,60,90])
# Sine of different angles:
np.sin(a*np.pi/180)
# Tangent values for given angles:
np.tan(a*np.pi/180)


# #### Numpy Statistical Functions

# ![Alt Text](https://i.ibb.co/rf6tYcb/matrix.jpg)

# In[ ]:


a = np.array([[3,7,5],[8,4,3],[2,4,9]])
a
np.amin(a,axis=1)
np.amin(a,axis=0)
# returns the range (maximum-minimum)
np.ptp(a,axis=1)
# Applying mean() function along axis 0
np.mean(a, axis = 0) 


# #### Get the dates of yesterday, today and tomorrow.

# In[ ]:


yesterday = np.datetime64('today', 'D') - np.timedelta64(1, 'D')
today     = np.datetime64('today', 'D')
tomorrow  = np.datetime64('today', 'D') + np.timedelta64(1, 'D')
print(yesterday)
print(today)
print(tomorrow)


# #### Get all the dates corresponding to the month of July 2016

# In[ ]:


Z = np.arange('2016-07', '2016-08', dtype='datetime64[D]')
print(Z)


# #### Vector of size 10 with values ranging from 0 to 1, both excluded.then find the inverse of the matrix.

# In[ ]:


x = np.linspace(0,1,10,endpoint=False)[1:]
print(x)
aa = np.linalg.inv(x.reshape(3,3))
aa.dot(x.reshape(3,3))


# #### Vector with size of 10 and replace the maximum value by 0

# In[ ]:


Z = np.random.random(10)
Z[Z.argmax()] = 0
print(Z)


# #### Equivalent of enumerate for numpy arrays

# In[ ]:


Z = np.arange(9).reshape(3,3)
for index, value in np.ndenumerate(Z):
    print(index, value)


# #### Subtract mean of each row of a matrix

# In[ ]:


X = np.random.rand(5, 5)
Y = X - X.mean(axis=1, keepdims=True)
print(Y)


# #### Swap two rows of an array

# In[ ]:


A = np.arange(25).reshape(5,5)
A
A[[0,1]] = A[[1,0]]
print(A)


# #### Compute a matrix rank

# In[ ]:


Z = np.random.uniform(0,1,(10,10))
U, S, V = np.linalg.svd(Z) # Singular Value Decomposition
rank = np.sum(S > 1e-10)
print(rank)


# #### Get the n largest values of an array

# In[ ]:


Z = np.arange(10000)
np.random.shuffle(Z)
n = 5
print (Z[np.argpartition(-Z,n)[:n]])


# #### Load and Save data to npy & txt Format

# In[ ]:


a = np.array([1,2,3,4,5]) 
np.save('outfile',a)
b = np.load('outfile.npy') 
b
# with txt file format
a = np.array([1,2,3,4,5]) 
np.savetxt('out.txt',a) 
b = np.loadtxt('out.txt') 
b 


# ### Conclusion

# Mentioned Above are the most important numpy functionality which every machine learning practitioner should know.

# ![Alt Text](https://i.ibb.co/8xPLvZW/Thank-You.png)
