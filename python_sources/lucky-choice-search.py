#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# I would like to test an intereting propability-based lucky choice searching method in this kernel, which is only suitable for those Santa thinks are lucky enough (He may offer you the optimal solution!). For those who is not lucky enough (including myself), this is just a test kernel and does not guanrantee better solutions ; ).
# 
# This algorithm is modified from [Santa's 2019: Stochastic Product Search][1]. The main difference is that extremely large family sizes (even 5000) are allowed in this kernel by introducing more randomness. If you have found any mistake, please leave your comments below. I will try my best to fix it. 
# 
# Here's a simple description of the algorithm, which is defined as lucky_choice_search:
# * Sample a number of families, call this fam_size, with a probability distribution estimated by each family's original cost (See the discussion in [Santa's 2019: Stochastic Product Search][1]).
# * Give them top-k choices, with a probability distribution estimated from a diversity of their choices in your history submissions. (**Get more diverse submissions and create a better distribution!**)
# * For each iteration, you create a new assignment by updating your current best assignment. If the new_score is better than the current best_score, update both of those values and save.
# * Repeat that for the number of iterations desired, given by parameter n_iter.
# 
# # References
# * Fast Cost Function (C): [fast scoring using C (42 usec)][2]
# * history submissions: [Using a baseline][3], [Santa IP][4], [How to improve a little bit][5], [Santa's 2019: Stochastic Product Search][1], [Santa's Assistant - Learning LP from others][6], [Santa's Seed Seeker][7], [Hill climbing][8]
# * random_choice_prob_index function: [Vectorizing numpy.random.choice for given 2D array of probabilities along an axis
# ][9]
# 
# [1]: https://www.kaggle.com/xhlulu/santa-s-2019-stochastic-product-search
# [2]: https://www.kaggle.com/sekrier/fast-scoring-using-c-42-usec
# [3]: https://www.kaggle.com/jazivxt/using-a-baseline
# [4]: https://www.kaggle.com/vipito/santa-ip
# [5]: https://www.kaggle.com/davide0burba/how-to-improve-a-little-bit
# [6]: https://www.kaggle.com/kathakaliseth/santa-s-assistant-learning-lp-from-others
# [7]: https://www.kaggle.com/hengzheng/santa-s-seed-seeker
# [8]: https://www.kaggle.com/nagadomi/hill-climbing
# [9]: https://stackoverflow.com/questions/47722005/vectorizing-numpy-random-choice-for-given-2d-array-of-probabilities-along-an-a?noredirect=1&lq=1

# In[ ]:


import os
import ctypes
from numpy.ctypeslib import ndpointer
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from numba import njit, prange


# In[ ]:


get_ipython().run_cell_magic('writefile', 'score.c', '\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <math.h>\n\n#define NF 5000\nint cost[NF][101];\nint fs[NF];\n\nint cf[NF][10];\n\nint loaded=0;\n\nfloat acc[301][301];\n\nvoid precompute_acc() {\n    \nfor(int i=125;i<=300;i++) \n    for(int j=125;j<=300;j++)\n      acc[i][j] = (i-125.0)/400.0 * pow(i , 0.5 + fabs(i-j) / 50 );    \n}\n\nvoid read_fam() {\n  FILE *f;\n  char s[1000];\n  int d[101],fid,n;\n  int *c;\n\n  f=fopen("../input/santa-workshop-tour-2019/family_data.csv","r");\n  if (fgets(s,1000,f)==NULL)\n    exit(-1);\n\n  for(int i=0;i<5000;i++) {\n    c = &cf[i][0];\n    if (fscanf(f,"%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d",\n               &fid,&c[0],&c[1],&c[2],&c[3],&c[4],&c[5],&c[6],&c[7],&c[8],&c[9],&fs[i])!=12)\n      exit(-1);\n\n    //    printf("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\\n",\n    //fid,c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],fs[i]);\n    n = fs[i];\n\n    for(int j=1;j<=100;j++) {\n      if (j==c[0]) cost[i][j]=0;\n      else if (j==c[1]) cost[i][j]=50;\n      else if (j==c[2]) cost[i][j]=50 + 9 * n;\n      else if (j==c[3]) cost[i][j]=100 + 9 * n;\n      else if (j==c[4]) cost[i][j]=200 + 9 * n;\n      else if (j==c[5]) cost[i][j]=200 + 18 * n;\n      else if (j==c[6]) cost[i][j]=300 + 18 * n;\n      else if (j==c[7]) cost[i][j]=300 + 36 * n;\n      else if (j==c[8]) cost[i][j]=400 + 36 * n;\n      else if (j==c[9]) cost[i][j]=500 + 36 * n + 199 * n;\n      else cost[i][j]=500 + 36 * n + 398 * n;\n    }\n  }\n\n}\n\nfloat max_cost=1000000000;\n\nint day_occ[102];\n\nstatic inline int day_occ_ok(int d) {\n  return !(d <125 || d>300);\n}\n\nfloat score(int *pred) {\n  float r=0;\n    \n  if (!loaded) {\n      read_fam();\n      precompute_acc();\n      loaded = 1;\n  }\n\n  // validate day occupancy\n  memset(day_occ,0,101*sizeof(int));\n\n  for(int i=0;i<NF;i++) {\n    day_occ[pred[i]]+=fs[i];\n    r+=cost[i][pred[i]];\n  }\n       \n  day_occ[101]=day_occ[100];\n\n  for (int d=1;d<=100;d++) {\n    if (day_occ[d]<125)                                                       \n      r += 100000 * (125 - day_occ[d]);                                      \n    else if (day_occ[d] > 300)                                               \n      r += 100000 * (day_occ[d] - 300);      \n    r += acc[day_occ[d]][day_occ[d+1]];\n  }\n  return r;\n} ')


# In[ ]:


get_ipython().system('gcc -O5 -shared -Wl,-soname,score     -o score.so     -fPIC score.c')
get_ipython().system('ls -l score.so')


# In[ ]:


lib = ctypes.CDLL('./score.so')
cost_function = lib.score
cost_function.restype = ctypes.c_float
cost_function.argtypes = [ndpointer(ctypes.c_int)]


# In[ ]:


score = []
sub = []
name = os.listdir('/kaggle/input/santa-public')
for item in name:
    score.append(int(item.split('_')[1].split('.')[0]))
    sub.append(pd.read_csv('../input/santa-public/'+item, index_col='family_id'))
print(np.min(score))
print(len(sub))


# In[ ]:


# Set Choice Selection Range
top_k = 3

# Load Data
base_path = '/kaggle/input/santa-workshop-tour-2019/'
sub_path = '/kaggle/input/greedy-dual-and-tripple-shuffle-with-fast-scoring/'
data = pd.read_csv(base_path + 'family_data.csv', index_col='family_id')

submission = pd.read_csv(f'../input/santa-public/submission_{np.min(score)}.csv', 
                         index_col='family_id')

# Run it on default submission file
original = submission['assigned_day'].values
original_score = cost_function(np.int32(original))
choice_matrix = data.loc[:, 'choice_0': 'choice_9'].values
print(cost_function(np.int32(original)))


# Generate Family Probability Distribution

# In[ ]:


fam_weight = []

for i, s in enumerate(submission.iterrows()):
    for c in range(choice_matrix.shape[1]):
        if s[1].values==choice_matrix[i, c]:
            fam_weight.append(c+1)
fam_weight = np.array(fam_weight)
fam_weight = fam_weight / sum(fam_weight)
print(fam_weight)


# Generate Choice Probability Distribution

# In[ ]:


# The redundancy is used to ensure evey choice can be selected with some probability since some choices are not selected in history submission
redundancy = 5 # any number larger than 0
choice_weight = np.zeros((5000, top_k))

for i in tqdm(range(5000)):
    for j in range(top_k):
        for s in sub:
            if choice_matrix[i, j] == s.loc[i, 'assigned_day']:
                choice_weight[i, j] += 1
                
choice_weight += redundancy
for j in range(choice_weight.shape[0]):
    choice_weight[j] /= sum(choice_weight[j])
    
print(choice_weight)


# # Novel Algorithm

# In[ ]:


# A fast function for sampling indices from a 2-D probability array in a vectorised way
def random_choice_prob_index(a, axis=1):
    r = np.expand_dims(np.random.rand(a.shape[1-axis]), axis=axis)
    return (a.cumsum(axis=axis) > r).argmax(axis=axis)


# In[ ]:


def lucky_choice_search(top_k, fam_size, original, choice_matrix, 
                   disable_tqdm=False, n_iter=100000000, 
                   verbose=10000, random_state=2019):
    
    best = original.copy()
    best_score = cost_function(np.int32(best))
    
    if random_state is not None:
        np.random.seed(random_state)
    
    # Select fam_size families from 5000 families with probability distribution fam_weight
    fam_indices = np.random.choice(range(choice_matrix.shape[0]), size=fam_size, p=fam_weight)

    for i in tqdm(range(n_iter), disable=disable_tqdm):
        new = best.copy()
        
        # Select choices for each family based on the probability distribution of their choices from multiple history submissions
        new[fam_indices] = choice_matrix[fam_indices, random_choice_prob_index(choice_weight[fam_indices])]
        new_score = cost_function(np.int32(new))

        if new_score < best_score:
            best_score = new_score
            best = new
            print(f'{i} NEW BEST SCORE: ', best_score)
            submission['assigned_day'] = best
            submission.to_csv(f'submission_{best_score}.csv')

        if verbose and i % verbose == 0:
            print(f"Iteration #{i}: Best score is {best_score:.2f}")
            
    return best, best_score


# # Usage

# In[ ]:


best, best_score = lucky_choice_search(
    choice_matrix=choice_matrix, 
    top_k=top_k,
    fam_size=20, 
    original=original, 
    n_iter=250000000, # run more iterations and find the optimal if you are lucky enough ;)
    disable_tqdm=False,
    random_state=20191217,
    verbose=None
)


# In[ ]:


submission['assigned_day'] = best
submission.to_csv(f'submission_{best_score}.csv')

