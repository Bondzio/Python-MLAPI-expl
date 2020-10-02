#!/usr/bin/env python
# coding: utf-8

# Which ones are the stars escaping from the cluster ? Can we find why ? Can wee foresee that ?

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data=pd.read_csv("../input/c_0000.csv")
data['t'] = 0
data['v'] = np.sqrt(data.vx**2 + data.vy**2 + data.vz**2)
data['Ec'] = 0.5*data.m*(data.v)**2
data['r'] = np.sqrt(data.x**2 + data.y**2 + data.z**2)

for i in range(1,19):
    if i<10:
        step="0"+str(i)
    else:
        step=str(i)
    file="../input/c_"+step+"00.csv"
    d=pd.read_csv(file)
    d['t']=i*100
    d['v'] = np.sqrt(d.vx**2 + d.vy**2 + d.vz**2)
    d['Ec'] = 0.5*d.m*(d.v)**2
    d['r'] = np.sqrt(d.x**2 + d.y**2 + d.z**2)
    data=data.append(d)


# In[ ]:


plt.scatter(data[data.t==0].x,data[data.t==0].y,s=1,marker='+')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Cluster on the xy plane at t=0')
plt.grid()
plt.show()


# Positions on plane xy of all the stars for all the time steps. We can see the pathes of the stars getting away from the cluster (and coming back ?) :

# In[ ]:


plt.scatter(data.x,data.y,s=1,marker='+')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Cluster on the xy plane at all time')
plt.grid()
plt.show()


# In[ ]:


plt.hist(data[data.t==0].r,100,alpha=0.6)
plt.xlabel('r')
plt.show()
plt.hist(data[data.t==0].v,100,alpha=0.6)
plt.xlabel('v')
plt.show()


# 30 stars have got out of the cluster at the end of the simulation :

# In[ ]:


def n_stars(time):
    return len(data[data.t==time])

n_stars = np.vectorize(n_stars)

time = 100*np.arange(19)
n = n_stars(time)
print(n)
plt.plot(time,n,marker='o')
plt.grid()
plt.xlabel('time')
plt.ylabel('number of stars')
plt.show()


# Let's try to see how/why these stars have got away :

# In[ ]:


index_0 = pd.Index(data[data.t==0].id)
index_stars_in = pd.Index(data[data.t==1800].id)
index_stars_out = index_0.difference(index_stars_in)
stars_in = data[data.id.isin(index_stars_in)]
stars_out = data[data.id.isin(index_stars_out)]


# Speed and radius evolution for the 30 stars getting away from the cluster :

# In[ ]:


for i in index_stars_out:
    plt.plot(stars_out[stars_out.id==i].t,stars_out[stars_out.id==i].r)
plt.xlabel('time')
plt.ylabel('r')
plt.grid()
plt.show()

for i in index_stars_out:
    plt.plot(stars_out[stars_out.id==i].t,stars_out[stars_out.id==i].v)
plt.xlabel('time')
plt.ylabel('r')
plt.grid()
plt.show()


# Why does the simulation stop for these 30 stars before the end ?! They are not even the stars which are getting the farest from the cluster, when the simulation stops they are all at the center of the cluster (radius<6)...

# In[ ]:


plt.scatter(data.x,data.y,s=1,marker='+',color='blue',alpha=0.5,label='all stars')
plt.scatter(stars_out.x,stars_out.y,s=1,marker='o',color='red',label='stars away at t=1800')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Cluster on the xy plane at all time')
plt.grid()
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()


# Ok, as explained in the comments, the snapshots are too far away from each other, as a consequence it's unlikely to see a star with an outlying velocity, or to capture the path of the escaping star. But can we find distinguishing features for these 30 stars ?

# Distribution of the velocity in function of the radius, stars who got away in red :

# In[ ]:


plt.scatter(data.r,data.v,s=1,marker='+',color='blue',alpha=0.5,label='all stars')
plt.scatter(stars_out.r,stars_out.v,s=1,marker='o',color='red',label='stars away at t=1800')
plt.xlabel('r')
plt.ylabel('v')
plt.title('r/v distribution')
plt.grid()
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()


# Is the red distribution really different from the blue one ?

# In[ ]:


heatmap, xedges, yedges = np.histogram2d(data[data.t==0].r, data[data.t==0].v)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent,interpolation='nearest', origin='lower')
plt.xlabel('r')
plt.ylabel('v')
plt.show()

heatmap, xedges, yedges = np.histogram2d(stars_out.r, stars_out.v)

plt.clf()
plt.imshow(heatmap.T, extent=extent, interpolation='nearest',origin='lower')
plt.xlabel('r')
plt.ylabel('v')
plt.show()


# To be continued...

# Variation of the kinetic energy :

# In[ ]:


def Ec(time):
    return np.sum(data[data.t==time].Ec)

Ec = np.vectorize(Ec)

time = 100*np.arange(19)
e = Ec(time)
plt.plot(time,e)
plt.grid()
plt.xlabel('time')
plt.ylabel('Kinetic energy')
plt.show()

