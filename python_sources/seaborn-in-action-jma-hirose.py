#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
import os 
import pandas as pd

dat = pd.read_csv('../input/failure-time-of-pet-film/hirose.csv')
dat.head()


# In[ ]:


sns.lmplot(x="volt", y="time", hue="cens", data=dat)


# In[ ]:


f, ax = plt.subplots(figsize=(6, 6))
sns.kdeplot(dat.volt, dat.time, ax=ax)
sns.rugplot(dat.volt, color="g", ax=ax)
sns.rugplot(dat.time, vertical=True, ax=ax);


# In[ ]:


f, ax = plt.subplots(figsize=(6, 6))
cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
sns.kdeplot(dat.volt, dat.time, cmap=cmap, n_levels=60, shade=True)


# In[ ]:


g = sns.jointplot(x="volt", y="time", data=dat, kind="kde", color="m")
g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
g.ax_joint.collections[0].set_alpha(0)
g.set_axis_labels("$Volt$", "$Cens$");

