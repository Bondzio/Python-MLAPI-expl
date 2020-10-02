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

dat = pd.read_csv('../input/pedometer-walking-data/Pedometer.csv')
dat.head()


# In[ ]:


sns.lmplot(x="kcal", y="Mile", hue="Rain", data=dat)


# In[ ]:


f, ax = plt.subplots(figsize=(6, 6))
sns.kdeplot(dat.kcal, dat.Mile, ax=ax)
sns.rugplot(dat.kcal, color="g", ax=ax)
sns.rugplot(dat.Mile, vertical=True, ax=ax);


# In[ ]:


f, ax = plt.subplots(figsize=(6, 6))
cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
sns.kdeplot(dat.kcal, dat.Mile, cmap=cmap, n_levels=60, shade=True);


# In[ ]:


g = sns.jointplot(x="kcal", y="Mile", data=dat, kind="kde", color="m")
g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
g.ax_joint.collections[0].set_alpha(0)
g.set_axis_labels("$kcal$", "$Miles$");

