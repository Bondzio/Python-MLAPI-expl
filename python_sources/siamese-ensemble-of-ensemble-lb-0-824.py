#!/usr/bin/env python
# coding: utf-8

# Take results from Siamese net kernel https://www.kaggle.com/seesee/siamese-pretrained-0-822 by @seesee
# 
# Take results from https://www.kaggle.com/ateplyuk/ensembling-voting-0-777 by @ateplyuk
# 
# And plug into this kernel by @suicaokhoailang
# 
# This kernel is based on the approach from https://www.kaggle.com/suicaokhoailang/ensembling-with-averaged-probabilities-0-701-lb

# In[ ]:


import csv
import pandas as pd # not key to functionality of kernel

sub_files = [
                 '../input/siamese/sub_ens_777.csv',
                 '../input/siamese/sub_822.csv',
]

# Weights of the individual subs
sub_weight = [
                0.777**2,
                0.822**2
            ]
# 15


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
out = open("sub_siamese_ens.csv", "w", newline='')
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




