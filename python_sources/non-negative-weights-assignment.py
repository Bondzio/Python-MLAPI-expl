#!/usr/bin/env python
# coding: utf-8

# # Non-negative weights assignment
# 
# 
# 
# Following procedure assigns weights to **w**[*i*], so they sum up to *sum* for *i*=0...*n*-1. Weights have to sum up to *sum* exactly. If *sum*=100, just steps like 0.5,1,2,5,10,25 are allowed. As *n* is increasing and *step* is decreasing, assignments count is increasing very steeply.

# In[ ]:



def weights_exact(step,sum,n):
    if sum%step!=0:
        return "This step is not allowed."
    w=list()
    weights=list()
    w[0:n]=[0]*(n)
    w[0]=sum
    counter=0
    i=0
    weights.append(w.copy())
    while w[n-1]!=sum:
        w[i] =0
        i=i+1
        w[i]=w[i]+step        
        counter=counter+step
        if counter==sum:
            counter=counter-w[i]
        else:
            w[0]=sum-counter
            i=0
        weights.append(w.copy())
    return weights
    
        


# In[ ]:


w=weights_exact(10,50,3)
print(w)


# Following procedure does almost the same as previous procedure, but weights do not have to sum up to *sum* exactly.

# In[ ]:


def weights(step,sum,n):    
    sum_adj=round(int(sum/step)*step,5)
    w=list()
    weights=list()
    w[0:n]=[0]*n
    w[0]=sum    
    counter=0
    i=0
    weights.append(w.copy())
    while round(w[n-1],5)!=sum:
        w[i] =0        
        i=i+1     
        w[i]=round(w[i]+step,5)    
        counter=round(counter+step,5)
        if counter==sum_adj:
            counter=round(counter-w[i],5)
            w[i]=round(w[i]+sum-sum_adj,5)
        else:
            w[0]=round(sum-counter,5)
            i=0
        weights.append(w.copy())
    return weights
    


# In[ ]:


w=weights(33.33,100,3)
print(w)


# In[ ]:




