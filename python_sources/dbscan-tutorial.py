#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import DBSCAN
        
finch_data_2012 = "../input/geospiza-scandens-beak-evolution/finch_beaks_2012.csv"
finch_data_1975 = "../input/geospiza-scandens-beak-evolution/finch_beaks_1975.csv"

finch_2012_df = pd.read_csv(filepath_or_buffer=finch_data_2012)
finch_1975_df = pd.read_csv(filepath_or_buffer=finch_data_1975)
finch_1975_df.columns = finch_2012_df.columns


# First lets plot the two datasets and see what they look like visually. For now all we're concerned with are the beak widths and depths.

# In[ ]:


sns.relplot(x="blength", y="bdepth", data=finch_1975_df,)
sns.relplot(x="blength", y="bdepth", data=finch_2012_df)


# You'll notice quickly, especially in the data from 1975, that there a two clear groups (clusters). The data from 2012 is a bit "messier" since the clusters aren't separated nicely by a lot of space. However, there are still two clusters with what we might call some "noise" in between. Although this is easy to see visually we are interested in clustering the data algorithmically. As a final note, it may be interesting at the end to run some analysis to see if the two clusters from 2012 and 1975 are statistically different. You can return to the post for now. See you in a bit!

# Lets go ahead and run DBSCAN on our two datasets. Remember the two parameters we need to choose are Eps and MinPts. Lets try the defaults first and see what we get.

# In[ ]:


# Lets prepare out data for clustering by pairing out blength and bdepth columns into a single column repsrsenting a point in 2D space.
finch_2012_beak_points = list(zip(finch_2012_df["blength"], finch_2012_df["bdepth"]))
finch_1975_beak_points = list(zip(finch_1975_df["blength"], finch_1975_df["bdepth"]))
finch_1975_df["beak_points"] = finch_1975_beak_points
finch_2012_df["beak_points"] = finch_2012_beak_points

# Cluster time!
finch_1975_df["cluster"] = DBSCAN().fit(finch_1975_beak_points).labels_
finch_2012_df["cluster"] = DBSCAN().fit(finch_2012_beak_points).labels_
print(finch_1975_df.head())
print()
print(finch_2012_df.head())


# Okay now that we have out cluster assignment using all the defaults lets plot our data and see the results.

# In[ ]:


sns.relplot(x="blength", y="bdepth", hue="cluster", data=finch_1975_df)
sns.relplot(x="blength", y="bdepth", hue="cluster", data=finch_2012_df)


# Well this is quite interesting isn't it! In our first finch dataset from 1975 it looks like the dfault values did alright! We identified the two distinct clusters and for the most part all the assignments look correct although you could debate about the noise points. However, in our second dataset from 2012 things don't look so hot. What we ended up with was one giant cluster! Why is that? Take a second before reading on and see if you can figure it out...No seriously think about it first...Last chance... 
# 
# The reason this occurs is due to the default parameter values. If we take a look at how our data is distributed in the second dataset we can see that the clusters aren't so clearly seprated instead, there is a "smear" of data points between them. Now remember how the realtionships work in DBSCAN if one point is density-reachable from another it means there is a series of directly-density reachable points in between them. Uh-oh. This means that if we don't select our parameters carefully we end up merging the two clusters since DBSCAN thinks there's some core points connecting the. Let's try and fix this. 
# 
# Well actually you try and fix this! This is your homework assignment! Go back to the post and click the link to the DBSCAN paper. Read the seciton on selecting values for Eps and MinPts on page 5 and see if you can come back and select values taht actually produce realistic cluster assignments. BONUS ALERT!!!! If you are really feeling it, after you finish the previous task go ahead and do some statistical analysis between the clusters in the 1975 and 2012. See if there is any statistical difference and what that might imply if there is! Good luck! You can complete this now or go back to the post and finish up first. 
