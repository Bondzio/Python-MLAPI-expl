#!/usr/bin/env python
# coding: utf-8

# **Map of Traffic Cameras in Chicago**

# In[ ]:


import numpy as np 
import pandas as pd
import warnings
warnings.simplefilter("ignore")
from scipy.special import boxcox
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly
import plotly.plotly as py
import plotly.offline as offline
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import cufflinks as cf
from plotly.graph_objs import Scatter, Figure, Layout
cf.set_config_file(offline=True)
# begin secret_token
from shutil import copyfile
copyfile(src = "../input/private-mapbox-access-token/private_mapbox_access_token.py", dst = "../working/private_mapbox_access_token.py")
from private_mapbox_access_token import *
private_mapbox_access_token = private_mapbox_access_token()
# end secret_token
train = pd.read_csv('../input/chicago-red-light-and-speed-camera-data/speed-camera-locations.csv', nrows = 30_000)
train2 = pd.read_csv('../input/chicago-red-light-and-speed-camera-data/red-light-camera-locations.csv', nrows = 30_000)
#train.head()


# In[ ]:


print("Total Number of Speed Cameras: {}".format(train.shape[0]))
print("Total Number of Red Light Cameras: {}".format(train2.shape[0]))


# In[ ]:


# Adapted from from https://www.kaggle.com/shaz13/simple-exploration-notebook-map-plots-v2/
data = [go.Scattermapbox(
            lat= train['LATITUDE'] ,
            lon= train['LONGITUDE'],
            mode='markers',
            text=train['ADDRESS'],
            marker=dict(
                size= 20,
                color = 'black',
                opacity = .8,
            ),
          )]
layout = go.Layout(autosize=False,
                   mapbox= dict(accesstoken=private_mapbox_access_token,
                                bearing=0,
                                pitch=0,
                                zoom=10,
                                center= dict(
                                         lat=41.881900,
                                         lon=-87.325808),
                               ),
                    width=1800,
                    height=1200, title = "Speed Cameras in Chicago")
fig = dict(data=data, layout=layout)
iplot(fig)


# In[ ]:


# Adapted from from https://www.kaggle.com/shaz13/simple-exploration-notebook-map-plots-v2/
data = [go.Scattermapbox(
            lat= train2['LATITUDE'] ,
            lon= train2['LONGITUDE'],
            mode='markers',
            text=train2['INTERSECTION'],
            marker=dict(
                size= 20,
                color = 'black',
                opacity = .8,
            ),
          )]
layout = go.Layout(autosize=False,
                   mapbox= dict(accesstoken=private_mapbox_access_token,
                                bearing=0,
                                pitch=0,
                                zoom=10,
                                center= dict(
                                         lat=41.881900,
                                         lon=-87.325808),
                               ),
                    width=1800,
                    height=1200, title = "Red Light Cameras in Chicago")
fig = dict(data=data, layout=layout)
iplot(fig)


# In[ ]:


# delete secret token
from IPython.display import clear_output; clear_output(wait=True)
get_ipython().system('rm -rf "../working/"')

