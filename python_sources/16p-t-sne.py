#!/usr/bin/env python
# coding: utf-8

# [Rapids](https://rapids.ai) is an open-source GPU accelerated Data Sceince and Machine Learning library, developed and mainatained by [Nvidia](https://www.nvidia.com). It is designed to be compatible with many existing CPU tools, such as Pandas, scikit-learn, numpy, etc. It enables **massive** acceleration of many data-science and machine learning tasks, oftentimes by a factor fo 100X, or even more. 
# 
# Rapids is still undergoing developemnt, and as of right now it's not availabel in the Kaggle Docker environment. If you are interested in installing and riunning Rapids locally on your own machine, then you should [refer to the followong instructions](https://rapids.ai/start.html).
# 
# In order to install Rapids locally we'll be follow the setup that was inmplemented by Chris Deotte in [the following kernel](https://www.kaggle.com/cdeotte/rapids-data-augmentation-mnist-0-985).

# In[ ]:


get_ipython().run_cell_magic('time', '', '# INSTALL RAPIDS OFFLINE (FROM KAGGLE DATASET). TAKES 1 MINUTE :-)\nimport sys\n!cp ../input/rapids/rapids.0.11.0 /opt/conda/envs/rapids.tar.gz\n!cd /opt/conda/envs/ && tar -xzvf rapids.tar.gz\nsys.path = ["/opt/conda/envs/rapids/lib"] + ["/opt/conda/envs/rapids/lib/python3.6"] + ["/opt/conda/envs/rapids/lib/python3.6/site-packages"] + sys.path\n!cp /opt/conda/envs/rapids/lib/libxgboost.so /opt/conda/lib/')


# In this exercise we'll try to use tSNE for dimensionality reduction of the 16P Psychological Personality Dataset. The resulting dataset will be viewed on scatterplot in 2D. It turns out to be overall rather featureless, but that's **exactly** what we would expect from the way that personality is understood - no clear clusters, and use of typology for personality is unwarranted. Nonetheless, we'll take a look at how geneder is distributed in the big persoanlity cluster. It turns out that a simple [logistic regression trained on the original item features can achieve AUC of 0.87.](https://www.kaggle.com/tunguz/16p-gender-with-logistic-regression). A simple look at the gender distribution on the tSNE plot will reveal *some* overall features, but nothing that jumps conclusively out.  

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import cudf, cuml
import cupy as cp
import numpy as np
import pandas as pd
from cuml.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.pyplot import ylim, xlim
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv("/kaggle/input/cattells-16-personality-factors/16PF/data.csv", sep="\t")


# In[ ]:


data.head()


# In[ ]:


gendered_data = data[(data['gender'] == 1) | (data['gender'] == 2)]


# In[ ]:


gendered_data['gender'] = gendered_data['gender'].values -1


# In[ ]:


features = gendered_data.columns[:-6]
gendered_data[features] = gendered_data[features].values/5.
gendered_data['std'] = gendered_data[features].std(axis=1)
gendered_data = gendered_data[gendered_data['std'] > 0.0]
X = gendered_data[features].values
Y = gendered_data['gender'].values


# In[ ]:


get_ipython().run_cell_magic('time', '', 'tsne = TSNE(n_components=2)\ntrain_2D = tsne.fit_transform(X)')


# In[ ]:


ylim(-150, 150)
xlim(-150, 150)


# In[ ]:


plt.scatter(train_2D[:,0], train_2D[:,1], c = Y, s = 0.5)


# In[ ]:




