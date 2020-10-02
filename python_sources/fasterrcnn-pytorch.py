#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#import os
#for dirname, _, filenames in os.walk('/kaggle/input'):
    #for filename in filenames:
        #print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import pandas as pd
import numpy as np 
import cv2 
import os 
import re 

from PIL import Image

import albumentations as A   # image transformation / augmentation
from albumentations.pytorch.transforms import ToTensorV2 

import torch 
import torchvision 

from torchvision.models.detection.faster_rcnn import FastRCNNPredictor 
from torchvision.models.detection import FasterRCNN 
from torchvision.models.detection.rpn import AnchorGenerator 

from torch.utils.data import DataLoader, Dataset 
from torch.utils.data.sampler import SequentialSampler 

from matplotlib import pyplot as plt 

DIR_INPUT = '/kaggle/input/global-wheat-detection '


# In[ ]:




