#!/usr/bin/env python
# coding: utf-8

# [My Github](https://github.com/pykeras/fastai)  
# *I'm a tensorflow(keras) user and try to learn how fastai library work, but prefer to do it on realworld datasets*

# In[ ]:


from fastai import *
from fastai.vision import *


# In[ ]:


import matplotlib.pyplot as plt
from matplotlib.backend_bases import RendererBase
from scipy import signal
from scipy.io import wavfile
from scipy.fftpack import fft
import pandas as pd

import os, glob, numpy as np
from PIL import Image


# In[ ]:


audio_path = '../input/environmental-sound-classification-50/audio/audio/44100/'
label_csv = '../input/environmental-sound-classification-50/esc50.csv'


# In[ ]:


waves = glob.glob(audio_path+'*.wav');
print(len(waves))


# In[ ]:


df = pd.read_csv(label_csv, usecols=['filename', 'target', 'category'], index_col=['filename'])
df.head()


# In[ ]:


def create_dir(dirname):
    if os.path.exists(dirname):
        pass
    else:
        os.makedirs(dirname)


# In[ ]:


def save_spectogram(file, output, figsize=(4,4)):

    freq, sound = wavfile.read(file)
    freq, time, specto = signal.spectrogram(sound)
    specto = 10*np.log(specto.astype(np.float32))
    
    fig = plt.figure(figsize=figsize, frameon=False) # make images 288x288
    ax = plt.Axes(fig, [0.,0.,1.,1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.pcolormesh(time/100, freq, specto)
    fig.savefig(output, dpi=100)
    plt.close()


# In[ ]:


import matplotlib
matplotlib.use('Agg') #stop display output in ipython

for item in waves:
    name=item.split('/')[-1]
#     print(name)
    dirname='./prep/' + df.loc[name].category
    create_dir(dirname)
    out_file = dirname+ '/' + name.split('.wav')[0] + '.jpg'
    save_spectogram(item, out_file)
    
print('done')


# In[ ]:


tfms = get_transforms(do_flip=False, max_rotate=0.)
data = ImageDataBunch.from_folder('./prep/', valid_pct=0.1, ds_tfms=tfms, size=224)
data.normalize()


# In[ ]:


#from Settings(on the right panel) Turn on Internet to download resnet50 pretrained
learner_model = cnn_learner(data, models.resnet50, metrics=error_rate)


# In[ ]:


learner_model.fit_one_cycle(4)


# In[ ]:


learner_model.unfreeze()
learner_model.fit_one_cycle(4, max_lr=slice(1e-5, 1e-2))


# In[ ]:


interp = ClassificationInterpretation.from_learner(learner_model)
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


interp.plot_top_losses(9, figsize=(15,15))


# In[ ]:


interp.plot_confusion_matrix(figsize=(15,15))


# In[ ]:


interp.most_confused(min_val=2)


# In[ ]:




