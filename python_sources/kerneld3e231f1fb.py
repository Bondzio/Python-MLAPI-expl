#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import time
import csv
# Data processing, metrics and modeling
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold,KFold
from datetime import datetime
from sklearn.metrics import precision_score, recall_score, confusion_matrix, accuracy_score, roc_auc_score, f1_score, roc_curve, auc,precision_recall_curve
from sklearn import metrics
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
# Suppr warning
import warnings
warnings.filterwarnings("ignore")

import itertools
from scipy import interp
# Plots
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import rcParams
from matplotlib import cm
#import ggridges
# Any results you write to the current directory are saved as output.
import seaborn as sns
import statsmodels.api as sm
# Any results you write to the current directory are saved as output.
import pandas_profiling
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import plotly.graph_objects as go


# In[ ]:


df = pd.read_csv(r'/kaggle/input/videogamesales/vgsales.csv')
df.get_dtype_counts()


# In[ ]:


pandas_profiling.ProfileReport(df)

