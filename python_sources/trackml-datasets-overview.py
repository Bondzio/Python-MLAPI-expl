#!/usr/bin/env python
# coding: utf-8

# # Introduction and table of contents
# ___
# 
# In this notebook, I made some exploratory analysis in order to better understand what we are dealing with in this competition. The trajectories (both in position and momentum space) of some particles are visualized using the Truth dataset. There are still lots of possible explorations and I'll be adding more analyses as the competetion goes on. 
# 
# ## Contents
# 
# -[Hits dataset](#Hits-dataset)
# 
# -[Truth dataset](Truth-dataset)
# 
# -[Particles dataset](Particles-dataset)

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
get_ipython().run_line_magic('matplotlib', 'inline')

from trackml.dataset import load_event
from trackml.randomize import shuffle_hits
from trackml.score import score_event


# ## Load event 1000

# In[2]:


hits, cells, particles, truth = load_event('../input/train_1/event000001000')


# ## Exploring the datasets
# 
# ### Hits dataset

# In[ ]:


sns.jointplot(x = "x", y= "y", data = hits, alpha = 0.05, size = 8);


# Here I set alpha = 0.05 so that each blue point represents 20 actual points. With this alpha number, it is possible to see where the particles are mostly concentrated. They concentric rings, with a few particles outside them (few compared to the actual number of particles, of course).

# In[3]:


sns.jointplot(x = "x", y= "z", data = hits, alpha = 0.05, size = 8);


# In[ ]:


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(
    xs=hits.x.values,
    ys=hits.y.values,
    zs=hits.z.values,
    alpha = 0.05
)
ax.set_title('Hit Locations of event 1000')
ax.set_xlabel('X (millimeters)')
ax.set_ylabel('Y (millimeters)')
ax.set_zlabel('Z (millimeters)')
plt.show()


# In[ ]:


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(
    xs=truth.tpx.values,
    ys=truth.tpy.values,
    zs=truth.tpz.values,
    alpha = 0.01
)
ax.set_title('Momentum space of event 1000')
ax.set_xlabel('Px (GeV/c)')
ax.set_ylabel('Py (GeV/c)')
ax.set_zlabel('Pz (GeV/c)')
plt.show()


# When alpha = 0.01, we can see that lots of particles have high momenta pointing towards z-direction (there are two clear points on the north and south pole of the "momentum sphere").

# In[ ]:


hits_per_layer = pd.DataFrame(hits.groupby("layer_id", as_index=False)["hit_id"].count())
hits_per_layer = hits_per_layer.rename(columns = {"hit_id": "num_of_hits"})

sns.barplot(x = hits_per_layer.layer_id, y = hits_per_layer.num_of_hits);


# Some layers have way less number of hits than others. Let's see how the cross section is looking at the different layers (based on [Joshua Bonatt's kernel](https://www.kaggle.com/jbonatt/trackml-eda-etc))

# In[ ]:


g = sns.jointplot(hits.x, hits.y,  s=1, size=10)
g.ax_joint.cla()
plt.sca(g.ax_joint)

layers = hits.layer_id.unique()
for layer in layers:
    lay_hit = hits[hits.layer_id == layer]
    plt.scatter(lay_hit.x, lay_hit.y, s=1, label='layer {}'.format(layer))

plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.legend()
plt.show()


# Note that the layers doesn't have a specific order, as there are lots of colored points all over the cross section. However, there are concentric circles with apparently only one type of layer.

# In[ ]:


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

#get the unique layer values
layers = hits.layer_id.unique()

#for each layer
for layer in layers:
    #get the data belonging to that layer alone
    lay_hit = hits[hits.layer_id == layer]
    #make a scatterplot of only points of a specific layer
    #and give them colors (using label)
    ax.scatter(lay_hit.x, lay_hit.y, lay_hit.z, s=1, label='layer {}'.format(layer))

#set axes names
ax.set_xlabel('x (mm)')
ax.set_ylabel('y (mm)')
ax.set_zlabel('z (mm)')
ax.legend()
plt.show()


# In[44]:


hits_per_vol = pd.DataFrame(hits.groupby("volume_id", as_index=False)["hit_id"].count())
hits_per_vol = hits_per_vol.rename(columns = {"hit_id": "num_of_hits"})

sns.barplot(x = hits_per_vol.volume_id, y = hits_per_vol.num_of_hits);


# Similar to the layers, some volumes were more hit than others. Let's make a scatterplot to actually "see" the different volumes.

# In[57]:


fig = plt.figure(figsize=(25, 8))
gs = gridspec.GridSpec(nrows=2, ncols=3, left=0.05, right=0.48, wspace=0.5, hspace = 0.3)
ax = fig.add_subplot(gs[0:2,0:2], projection = '3d')
ax2 =fig.add_subplot(gs[0,2])
ax3 =fig.add_subplot(gs[1,2])

#get the unique volume values
volumes = hits.volume_id.unique()

#for each volume
for volume in volumes:
    #get the data belonging to that volume alone
    vol_hit = hits[hits.volume_id == volume]
    #make a scatterplot of only points of a specific volume
    #and give them colors (using label)
    ax.scatter(
        vol_hit.x, 
        vol_hit.y, 
        vol_hit.z, 
        s=0.1, 
        label='volume {}'.format(volume))

    ax2.scatter( 
    x = vol_hit.x,
    y = vol_hit.y,
    s = 0.1,
    label='volume {}'.format(volume))
        
    ax3.scatter(
    x = vol_hit.x,
    y = vol_hit.z,
    s = 0.1,
    label='volume {}'.format(volume))
    
#set axes names
ax.set_xlabel('x (mm)')
ax.set_ylabel('y (mm)')
ax.set_zlabel('z (mm)')
ax.set_title('Colored volumes')
ax.legend(loc = "upper left")

ax2.set_xlabel('x (mm)')
ax2.set_ylabel('y (mm)')
ax2.set_title('Colored volumes x-y cross section')

ax3.set_xlabel('x (mm)')
ax3.set_ylabel('z (mm)')
ax3.set_title('Colored volumes x-z cross section')

plt.show()


# Here I made the points very tiny so it becomes better to see where each volume is located. 

# ### Truth dataset
# 
# For starters, let's see some trajectories from the truth dataset.

# In[ ]:


#get the information for some particles
truth_0 = truth[truth.particle_id == particles.iloc[20,0]]
truth_1 = truth[truth.particle_id == particles.iloc[10,0]]
truth_2 = truth[truth.particle_id == particles.iloc[5,0]]

#create figure instance
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

#plot each particle's path
ax.plot(
    xs=truth_0.tx,
    ys=truth_0.ty,
    zs=truth_0.tz, marker='o')
ax.plot(
    xs=truth_1.tx,
    ys=truth_1.ty,
    zs=truth_1.tz, marker='o')
ax.plot(
    xs=truth_2.tx,
    ys=truth_2.ty,
    zs=truth_2.tz, marker='o')

ax.set_title('Trajectories of 3 different particle_id')
ax.set_xlabel('x (mm)')
ax.set_ylabel('y (mm)')
ax.set_zlabel('z (mm)')
plt.show()


# Now let's automate this a bit and see a larger number of trajectories. Not too large so we can still see some distinct paths.

# In[39]:


#get the information of a given particle from the truth dataframe
information = []

#append the information of each desired particle on a list
for i in np.arange(0,20,1):
    #select the true values for a given particle_id
    particle_information = truth[truth.particle_id == particles.iloc[i,0]]
    #append on the list
    information.append(particle_information)

#create figure instance
fig = plt.figure(figsize=(25, 8))
gs = gridspec.GridSpec(nrows=2, ncols=3, left=0.05, right=0.48, wspace=0.5, hspace = 0.3)
ax = fig.add_subplot(gs[0:2,0:2], projection = '3d')
ax2 =fig.add_subplot(gs[0,2])
ax3 =fig.add_subplot(gs[1,2])

#plot the trajectory for each particle on the information list
for trajectory in information:
    
    ax.plot(
    xs=trajectory.tx,
    ys=trajectory.ty,
    zs=trajectory.tz, marker='o')
    
    ax2.scatter( 
    x = trajectory.tx,
    y = trajectory.ty)
    
    
    ax3.scatter(
    x= trajectory.tx,
    y = trajectory.tz)
    
#labels
ax.set_xlabel('x (mm)')
ax.set_ylabel('y (mm)')
ax.set_zlabel('z (mm)')
ax.set_title('20 different trajectories')

ax2.set_xlabel('x (mm)')
ax2.set_ylabel('y (mm)')
ax2.set_title('Detector x-y cross section')

ax3.set_xlabel('x (mm)')
ax3.set_ylabel('z (mm)')
ax3.set_title('Detector x-z cross section')
plt.show()


# I think this image is really beautiful. All particles are moving from the center towards all directions, changing their paths according to their charges and other properties on the instant they were created, such as initial energy and momentum.
# 
# Now a similar plot but in the momentum space (I decided to leave the first two blocks of code - the ones that store information about the particles we will plot - because one might want to see a different number of "momentum trajectories" than what they saw in position space.

# In[42]:


#get the information of a given particle from the truth dataframe
information = []

#append the information of each desired particle on a list
for i in np.arange(0,20,1):
    #select the true values for a given particle_id
    particle_information = truth[truth.particle_id == particles.iloc[i,0]]
    #append on the list
    information.append(particle_information)

#create figure instance
import matplotlib.gridspec as gridspec
fig = plt.figure(figsize=(25, 8))
gs = gridspec.GridSpec(nrows=2, ncols=3, left=0.05, right=0.48, wspace=0.3, hspace = 0.3)
ax = fig.add_subplot(gs[0:2,0:2], projection = '3d')
ax2 =fig.add_subplot(gs[0,2])
ax3 =fig.add_subplot(gs[1,2])

#plot the trajectory for each particle on the information list
for trajectory in information:
    
    ax.plot(
    xs=trajectory.tpx,
    ys=trajectory.tpy,
    zs=trajectory.tpz, marker='o')
    
    ax2.scatter( 
    x = trajectory.tpx,
    y = trajectory.tpy)
    
    ax3.scatter(
    x= trajectory.tpx,
    y = trajectory.tpz)

#labels
ax.set_xlabel('Px (GeV/c)')
ax.set_ylabel('Py (GeV/c)')
ax.set_zlabel('Pz (GeV/c)')
ax.set_title("Trajectories in momentum space")

ax2.set_xlabel('Px (GeV/c)')
ax2.set_ylabel('Py (GeV/c)')
ax2.set_title ("Trajectories in momentum space x-y cross section")

ax3.set_xlabel('Px (GeV/c)')
ax3.set_ylabel('Pz (GeV/c)')
ax3.set_title ("Trajectories in momentum space x-z cross section")
plt.show()


# The momentum plot didn't look as pretty as the position one due to one outlier. This particle had too much momentum in all three directions. Over 12 GeV/c of magnitude in both x and y directions and about 40 GeV/c in z direction.

# In[ ]:


plt.hist(truth.weight, bins = 100)
plt.xlabel("Weight")
plt.ylabel("Number of observations")
plt.title("Weight distribution");


# The weight properties are the following, according to the project description:
#  - the few first (starting from the center of the detector) and last hits have a larger weight
#  - hits from the more straight tracks (more rare, but more interesting) have a larger weight
#  - random hits or hits from very short tracks have weight zero
# 
# From these points and the above histogram, we can conclude that:
# - there are indeed very few straight tracks - with higher weights -, as explained on the description
# - there is a considerable amount of random hits or hits with very short tracks.

# ### Particles dataset
# 
# First, how many hits do particles of different charges have?

# In[4]:


g = sns.FacetGrid(data = particles, col = "q", hue = "q", size = 5)
g.map(sns.distplot, "nhits", kde=False)
g.add_legend();


# Let's compute the absolute momentum of a particle and see if its somehow correlated with the number of hits.

# In[23]:


#computing absolute velocity
particles["abs_p"] = np.sqrt(particles.pz**2 + particles.px**2 + particles.py**2)

#making a scatterplot
plt.scatter(particles.nhits, particles.abs_p)
plt.title("Number of hits x Absolute momentum")
plt.xlabel("Number of hits")
plt.ylabel("Absolute momentum (GeV/c)");

#computing correlation
particles.abs_p.corr(particles.nhits)


# Both scatterplot and correlation coefficient indicate that there is no linear relationship between absolute momentum and the number of hits. 

# In[38]:


#create figure instance
fig = plt.figure(figsize=(25, 8))
gs = gridspec.GridSpec(nrows=2, ncols=3, left=0.05, right=0.48, wspace=0.5, hspace = 0.3)
ax = fig.add_subplot(gs[0:2,0:2], projection = '3d')
ax2 =fig.add_subplot(gs[0,2])
ax3 =fig.add_subplot(gs[1,2])

#plot the initial position for each particle on the information list
ax.scatter(
xs=particles.vx,
ys=particles.vy,
zs=particles.vz,
alpha = 0.1)
    
ax2.scatter( 
x = particles.vx,
y = particles.vy,
alpha = 0.1)
    
    
ax3.scatter(
x= particles.vx,
y = particles.vz,
alpha = 0.1)
    
#labels
ax.set_xlabel('x (mm)')
ax.set_ylabel('y (mm)')
ax.set_zlabel('z (mm)')
ax.set_title('Initial position 3d view')

ax2.set_xlabel('x (mm)')
ax2.set_ylabel('y (mm)')
ax2.set_title('Initial position x-y cross section')

ax3.set_xlabel('x (mm)')
ax3.set_ylabel('z (mm)')
ax3.set_title('Initial position x-z cross section')
plt.show()


# Particles were generated very close to the origin of the detector, according to the global coordinates system, with some created in other parts of the apparatus.
