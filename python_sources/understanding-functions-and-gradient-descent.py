#!/usr/bin/env python
# coding: utf-8

# # Study about functions and Gradient descent

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np

get_ipython().run_line_magic('matplotlib', 'inline')


# 
# 
# ## $f(x) = x^2 + x +1$

# In[ ]:


def f(x):
    return x**2+x+1


# In[ ]:


x = np.linspace(start=-3, stop=3, num=500) #returns evenly spaced numbers over specified interval
#print(x);


# In[ ]:


plt.xlim([-3,3])
plt.ylim([0,8])
plt.xlabel('x', fontsize=18,color='red');
plt.ylabel('f(x)',fontsize=18,color='red');
plt.plot(x,f(x));


# # Finding the lowest steep

# ### Idea : The point where the slop stops to change when we descend from the right side of the parabola

# The derivate of the function $f(x) = x^2 + x +1$ is $2x+1$ , so creating a python function for that

# In[ ]:


def df(x):
    return 2*x+1


# In[ ]:


plt.figure(figsize=[15, 5])

#Graph for the function
plt.subplot(1,2,1)
plt.xlim([-3,3])
plt.ylim([0,8])
plt.title('Function')
plt.xlabel('x', fontsize=18,color='red')
plt.ylabel('f(x)',fontsize=18,color='red')
plt.style.use('ggplot')
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}                          
plt.rc('font', **font);
plt.plot(x,f(x));

#Graph for the slope
plt.subplot(1,2,2)
plt.title('Derivative of the function')
plt.xlabel('x', fontsize=18,color='red')
plt.ylabel('df(x)',fontsize=18,color='red')
plt.xlim([-2,3])
plt.ylim([-3,6])
plt.style.use('ggplot')
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}                          
plt.rc('font', **font);
plt.plot(x,df(x),color='red');


# #### To recall, we need to find the point where the slop stops to change when we descend from the right side of the parabola

# In[ ]:


start = 3
previous = 0
learningrate = 0.1
precision = 0.0001
runcount =0


x_list = [start]
y_list = [df(start)]

#stop the loop once we reach limit
for i in range(500):
    previous  = start 
    #calculate the error (if the slope is very high which means it is very far from zero)
    gradient = df(previous)
    #print('slope at the point ' +str(previous)+' is '+ str(gradient))
    start = previous - learningrate*gradient
    
    step_size = abs(start-previous)
    x_list.append(start)
    y_list.append(df(start))
    print(step_size)
    runcount = runcount+1
    if(step_size<precision):break
        
    

print('Local Minimum is ', start)    
print('slope at the point is ', df(start))
print('f(x) is ',f(start))
print('loop ran ', runcount)
    


# #### Superimpose the previous outputs on the graph

# In[ ]:


plt.figure(figsize=[15, 5])

#Graph for the function
plt.subplot(1,2,1)
plt.xlim([-3,3])
plt.ylim([0,8])
plt.title('Function')
plt.xlabel('x', fontsize=18,color='red')
plt.ylabel('f(x)',fontsize=18,color='red')
plt.style.use('ggplot')
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}                          
plt.rc('font', **font)
plt.plot(x,f(x),alpha=0.8);

#Just the below two lines added to superimpose the scatter plot on the existing image
values = np.array(x_list)
plt.scatter(x_list, f(values), color='green', s=100, alpha=0.6); #scatter plot the previous results

#Graph for the slope
plt.subplot(1,2,2)
plt.title('Derivative of the function')
plt.xlabel('x', fontsize=18,color='red')
plt.ylabel('df(x)',fontsize=18,color='red')
plt.xlim([-2,3])
plt.ylim([-3,6])
plt.style.use('ggplot')
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}                          
plt.rc('font', **font)
plt.plot(x,df(x),color='red');
plt.scatter(x_list, y_list,color='blue',s=100,alpha=0.6);

