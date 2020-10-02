#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# # 1. Suppose S is a list of n bits, that is, n 0s and 1s. How long will it take to sort S with the merge-sort algorithm? What about quick-sort?

# * Merge-Sort Time: O(n log n) as it divides the input data creating the height of the tree (lg n) and sorts the input data by comparing nodes at the lowest depth (n). 
# * Quick-Sort Time: O(n log n) is to be expected, however, if the pivot point of 1 is chosen, then the data set will be divided into two segments in one iteration:
#     * Segment 1: All elements equal to 1
#     * Segment 2: All elements Less than 1
# * Therefore, Quick-Sort Time: O(n)

# # 2. Suppose we are given two n-element sorted sequences A and B that may contain duplicate entries. Describe an O(n)-time method for computing a sequence representing all elements in A or B with no duplicates.

# In[2]:


def merge(src, result, start, inc):
    """Merge src[start:start+inc] and src[start+inc:start+2*inc] into result."""
    end1 = start + inc  # boundary for run 1
    end2 = min(start + 2 * inc, len(src))  # boundary for run 2
    x, y, z = start, start + inc, start  # index into run 1, run 2, result
    while x < end1 and y < end2:
        if src[x] < src[y]:
            result[z] = src[x]
            x += 1
        else:
            result[z] = src[y]
            y += 1
        z += 1  # increment z to reflect new result
    if x < end1:
        result[z:end2] = src[x:end1]  # copy remainder of run 1 to output
    elif y < end2:
        result[z:end2] = src[y:end2]  # copy remainder of run 2 to output


# In[3]:


def merge_sort(S):
    """Sort the elements of Python list S using the merge-sort algorithm."""
    n = len(S)
    logn = math.ceil(math.log(n, 2))
    src, dest = S, [None] * n  # make temporary storage for dest
    for i in (2 ** k for k in range(logn)):  # pass i creates all runs of length 2i
        for j in range(0, n, 2 * i):  # each pass merges two length i runs
            merge(src, dest, j, i)
        src, dest = dest, src  # reverse roles of lists
    if S is not src:
        S[0:n] = src[0:n]  # additional copy to get results to S


# In[4]:


def remove_duplicates(S):
    seen = set()
    seen_add = seen.add
    return [x for x in S if not (x in seen or seen_add(x))]


# In[7]:


# Create Initial Sequences
s1 = [4,2,3,1,5]
s2 = [9,8,7,6,5]


# Sort each Sequence
merge_sort(s1)
merge_sort(s2)
print(s1)
print(s2)

# Add sequence one to sequence 2
s1.extend(s2)
s3 = s1
print(s3)

# Create new list with no duplicates
s3_new = remove_duplicates(s3)
print(s3_new)


# # 3. Given an array A of n entries with keys equal to 0 or 1, describe an in-place method for ordering A so that all 0s are before every 1.

# In[68]:


def inplace_quick_sort(S, a, b):
    """Sort the list from S[a] to S[b] inclusive using the quick-sort algorithm."""
    print(S) # Show the stage of the list
    if a >= b: return  # range is trivially sorted
    pivot = S[b]  # last element of range is pivot
    left = a  # will scan rightward
    right = b - 1  # will scan leftward
    while left <= right:
        # scan until reaching value equal or larger than pivot (or right marker)
        while left <= right and S[left] < pivot:
            left += 1
        # scan until reaching value equal or smaller than pivot (or left marker)
        while left <= right and pivot < S[right]:
            right -= 1
        if left <= right:  # scans did not strictly cross
            S[left], S[right] = S[right], S[left]  # swap values
            left, right = left + 1, right - 1  # shrink range

    # put pivot into its final place (currently marked by left index)
    S[left], S[b] = S[b], S[left]
    # make recursive calls
    inplace_quick_sort(S, a, left - 1)
    inplace_quick_sort(S, left + 1, b)


# In[71]:


array = [0,1,0,0,1,0,1,1,0,1]
array = inplace_quick_sort(array, 0, 9)


# # 4. Suppose we are given an n-element sequence S such that each element in S represents a different vote for president, where each vote is given as an integer representing a particular candidate. Design an O(n lg n)-time algorithm to see who wins the election S represents, assuming the candidate with the most vote wins - even if there are O(n) candidates.

# In[85]:


candidates = {1 : 'Justin', 2 : 'Linda', 3 : 'Paul', 4 : 'Melissa', 5: 'Danny'}
votes = [1,2,1,3,4,5,4,2,3,1,2,2,5,4,5,5,5,5] 
# Justin: 3 votes, Linda: 4 votes, Paul: 2 votes, Melissa: 3 votes, Danny: 6 votes

# Use Merge Sort Algorithm (Running Time: O(n lg n))
merge_sort(votes)
print(votes)

# Determine Winner (Running Time: O(n)
vote_count = 0
winner = 0
for vote in votes:
    current_vote_count = votes.count(vote)
    current_winner = vote
    if current_vote_count > vote_count:
        vote_count = current_vote_count
        winner = current_winner
print('The winner is:', candidates.get(winner), 'with', vote_count, 'votes.') 


# # 5. Consider the voting problem from above, but now suppose the number of candidates are a smallconstant number. Describe an O(n)-time algorithm for determining who wins the election.

# # Bucket Sort (Reference: https://www.sanfoundry.com/python-program-implement-bucket-sort/)

# In[114]:


def bucket_sort(alist):
    largest = max(alist)
    length = len(alist)
    size = largest/length
 
    buckets = [[] for _ in range(length)]
    for i in range(length):
        j = int(alist[i]/size)
        if j != length:
            buckets[j].append(alist[i])
        else:
            buckets[length - 1].append(alist[i])
 
    for i in range(length):
        insertion_sort(buckets[i])
 
    result = []
    for i in range(length):
        result = result + buckets[i]
 
    return result
 
def insertion_sort(alist):
    for i in range(1, len(alist)):
        temp = alist[i]
        j = i - 1
        while (j >= 0 and temp < alist[j]):
            alist[j + 1] = alist[j]
            j = j - 1
        alist[j + 1] = temp


# In[118]:


candidates = {1 : 'Danny', 2 : 'Linda', 3 : 'Paul', 4 : 'Melissa', 5: 'Justin'}
votes = [1,2,1,3,4,5,4,2,3,1,2,2,5,4,4,4,4,4] 
# Justin: 3 votes, Linda: 4 votes, Paul: 2 votes, Melissa: 3 votes, Danny: 6 votes

print(votes)
# Use Bucket Sort
votes = bucket_sort(votes)
print(votes)

# Determine Winner (Running Time: O(n)
vote_count = 0
winner = 0
for vote in votes:
    current_vote_count = votes.count(vote)
    current_winner = vote
    if current_vote_count > vote_count:
        vote_count = current_vote_count
        winner = current_winner
print('The winner is:', candidates.get(winner), 'with', vote_count, 'votes.') 


# # 6. Demonstrate merge-sort on the numbers [1000, 80, 10, 50, 70, 60, 90, 20].

# In[119]:


numbers = [1000, 80, 10, 50, 70, 60, 90, 20]

print(numbers)
merge_sort(numbers)
print(numbers)

