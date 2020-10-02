#!/usr/bin/env python
# coding: utf-8

# # Central Limit Theorem 
# 
# ### In probability theory, the central limit theorem establishes that, in some situations, when independent random variables are added, their properly normalized sum tends toward a normal distribution even if the original variables themselves are not normally distributed.
# 
# #### In simpler terms, it states that if we have a sample S, with a probability distribution which is NOT normally distributed, and we take sample Si multiple number of times, then the probability distribution for an independent random variable which is calculated from Si (like the sample mean), will tend to be normally distributed if we take a sufficiently large number of samples.

# ### We will try to implement the concepts as discussed in this video by Khan Academy. We will additionaly repeat this experiment with other independent random variables like the sum, median etc. Watch the video below to understand the concepts more clearly.

# In[ ]:


from IPython.display import YouTubeVideo
# a talk about IPython at Sage Days at U. Washington, Seattle.
# Video credit: William Stein.
YouTubeVideo('JNm3M9cqWyc')


# In[ ]:


#import dependencies
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


# ## Sampling distribution of Sample Means

# In[ ]:


#create a list to store sample means
means = []
#repeat experiment 100 times
for i in range(100):
    #generate a random array of 5 values, with values between 0 and 1
    arr = np.random.rand(5)
    #calculate mean of random sample
    s_mean = np.mean(arr)
    #add s_mean to list 
    means.append(s_mean)


# In[ ]:


#Plot it along with the mean of the distribution
sns.distplot(means, hist=True, kde=True, 
             bins=100, color = 'darkblue', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 3})

#Calculate the mean
mean = sum(means)/ len(means)

#Plot the mean over the distribution to get a sense of the central tendency
plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
min_ylim, max_ylim = plt.ylim()
plt.text(mean*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean))

plt.title("Sampling distribution of sample means of randomly generated samples (no of samples = 100)")
plt.xlabel("Sample mean")
plt.ylabel("Frequency")

plt.show()


# In[ ]:


#Lets repeat this with 1000 and 10000 samples
#for 1000 times
means = []
for i in range(1000):
    arr = np.random.rand(5)
    s_mean = np.mean(arr)
    means.append(s_mean)

sns.distplot(means, hist=True, kde=True, 
             bins=100, color = 'yellow', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 3})

mean = sum(means)/ len(means)

plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
min_ylim, max_ylim = plt.ylim()
plt.text(mean*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean))

plt.title("Sampling distribution of sample means of randomly generated samples (no of samples = 1000)")
plt.xlabel("Sample mean")
plt.ylabel("Frequency")

plt.show()    


# In[ ]:


#for 10000 times
means = []
for i in range(10000):
    arr = np.random.rand(5)
    s_mean = np.mean(arr)
    means.append(s_mean)

sns.distplot(means, hist=True, kde=True, 
             bins=100, color = 'green', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 3})

mean = sum(means)/ len(means)

plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
min_ylim, max_ylim = plt.ylim()
plt.text(mean*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean))

plt.title("Sampling distribution of sample means of randomly generated samples (no of samples = 10000)")
plt.xlabel("Sample mean")
plt.ylabel("Frequency")

plt.show()    


# ### Great! Doesn't this look similar to a normal distribution? (with a little left skew). If we keep on increasing the number of samples, the distribution should become almost identical to a normal distribution.

# ## Let's try replicating it with other independent random variables. 

# ### Sample median

# In[ ]:


medians = []
for i in range(10000):
    arr = np.random.rand(5)
    s_median = np.median(arr)
    medians.append(s_median)

sns.distplot(medians, hist=True, kde=True, 
             bins=100, color = 'pink', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 3})

mean = sum(medians)/ len(medians)

plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
min_ylim, max_ylim = plt.ylim()
plt.text(mean*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean))

plt.title("Sampling distribution of sample medians of randomly generated samples (no of samples = 10000)")
plt.xlabel("Sample median")
plt.ylabel("Frequency")

plt.show()  


# ### Sample Sum

# In[ ]:


sums = []
for i in range(10000):
    arr = np.random.rand(5)
    s_sum = np.sum(arr)
    #normalize it to get a value between 0 and 1
    s_sum /= 5
    sums.append(s_sum)

sns.distplot(sums, hist=True, kde=True, 
             bins=100, color = 'cyan', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 3})

mean = sum(sums)/ len(sums)

plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
min_ylim, max_ylim = plt.ylim()
plt.text(mean*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean))

plt.title("Sampling distribution of sample sums of randomly generated samples (no of samples = 10000)")
plt.xlabel("Sample sum")
plt.ylabel("Frequency")

plt.show()  


# In[ ]:




