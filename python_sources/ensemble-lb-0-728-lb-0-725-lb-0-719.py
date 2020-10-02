#!/usr/bin/env python
# coding: utf-8

# This kernel is based on the approach from https://www.kaggle.com/matthewa313/ensembling-algorithm-for-average-precision-metric
# 
# Take predictions for LB 0.728 from https://www.kaggle.com/ateplyuk/ensembling-0-728
# 
# Using my previous Resnet ensemble with 0.726 LB score
# 
# New Ensemble with LB Score 0.713 (Experimental ensemble)
# 
# Plug your outputs to this kernel and you're good to go.

# In[ ]:


get_ipython().system('pip install fastai==0.7.0 --no-deps')
get_ipython().system('pip install torch==0.4.1 torchvision==0.2.1')


# NOTE: Files sub_725.csv & sub_719.csv are named wrongly in folder, sub_725 has 0.719 LB score and sub_719.csv has 0.725 LB score

# In[ ]:


import csv
import pandas as pd # not key to functionality of kernel

sub_files = [
              '../input/results/sub_725.csv',
              '../input/results/sub_728.csv',
              '../input/results-/sub_719.csv',
]

# Weights of the individual subs
sub_weight = [
              0.719**2,
              0.728**2,
              0.725**2]


# In[ ]:


Hlabel = 'Image' 
Htarget = 'Id'
npt = 5 # number of places in target

place_weights = {}
for i in range(npt):
    place_weights[i] = ( 1 / (i + 1) )
    
print(place_weights)

lg = len(sub_files)
sub = [None]*lg
for i, file in enumerate( sub_files ):
    ## input files ##
    print("Reading {}: w={} - {}". format(i, sub_weight[i], file))
    reader = csv.DictReader(open(file,"r"))
    sub[i] = sorted(reader, key=lambda d: str(d[Hlabel]))

## output file ##
out = open("new_sub.csv", "w", newline='')
writer = csv.writer(out)
writer.writerow([Hlabel,Htarget])

for p, row in enumerate(sub[0]):
    target_weight = {}
    for s in range(lg):
        row1 = sub[s][p]
        for ind, trgt in enumerate(row1[Htarget].split(' ')):
            target_weight[trgt] = target_weight.get(trgt,0) + (place_weights[ind]*sub_weight[s])
    tops_trgt = sorted(target_weight, key=target_weight.get, reverse=True)[:npt]
    writer.writerow([row1[Hlabel], " ".join(tops_trgt)])
out.close()


# In[ ]:




