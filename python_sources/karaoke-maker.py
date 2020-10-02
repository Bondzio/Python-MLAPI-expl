#!/usr/bin/env python
# coding: utf-8

# # Karaoke Maker
# 
# version 1.0.0.0:001
# 
# The code follows a paper published on researchgate.com by Andrew J.R. Simpson #1, Gerard Roma #2, Mark D. Plumbley #3
# 
# ## Abstract
# 
# > Identification  and  extraction  of  singing  voice  from  within  musical mixtures is a key challenge in source separation and machine audition. Recent-ly, deep neural networks (DNN) have been used to estimate 'ideal' binary masks for carefully controlled cocktail party speech separation problems. However, it is not yet known whether these methods are capable of generalizing to the dis-crimination of voice and non-voice in the context of musical mixtures. Here, we trained a convolutional DNN (of around a billion parameters) to provide proba-bilistic  estimates  of  the  ideal  binary  mask  for  separation  of  vocal  sounds  from real-world musical mixtures. We contrast our DNN results with more traditional linear  methods.  Our  approach  may  be  useful  for  automatic  removal  of  vocal sounds from musical mixtures for 'karaoke' type applications.  
# 
# Access the complete document 
# <a href="https://www.researchgate.net/publication/275279991_Deep_Karaoke_Extracting_Vocals_from_Musical_Mixtures_Using_a_Convolutional_Deep_Neural_Network">here<a/>
# 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import scipy
import librosa
import librosa.display
import matplotlib.pyplot as plt
from librosa.core import stft, istft
from pydub import AudioSegment
import soundfile
import audioread
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


#importing all the necessary libraries
#do not run the code multiple times
get_ipython().system('conda install -c conda-forge librosa -y')
get_ipython().system('conda install -c conda-forge pydub -y')


# In[ ]:


#loading the song in the music library
y, sr = librosa.load("/kaggle/input/2k.wav", sr=44100)
y1,sr62=librosa.load('/kaggle/input/2.wav',sr=44100)

#getting the spectogram of the above music files
view_spec(y,sr)
view_spec(y1,sr62)

#getting the stft of the given audio wave
tst=stft(y)
print(tst.shape)
tstk=stft(y1)
print(tstk.shape)

#asking for threshold
#provide threshold if the begining or the is different for the clips
#requested to refer to the spectogram for this part

tb=input("Enter threshold for the begining: ** 0 if not required ")
tb=int(tb)
te=input("Enter threshold for ending : ** -1 if not required")
te=int(te)
if te == -1:
    te=tst.shape[1]


# In[ ]:


#equifying the datasets

if tstk.shape[1] != tst.shape[1]:
    
    mini=min(tst.shape[1],tstk.shape[1])
    c=mini%20
    mini=mini-c
    sn=int(mini/20)
    tst=tst[:,tb:mini]
    tstk=tstk[:,tb:mini]
    
    #sampling the data set for 20 samples in one example
    tst=np.array(np.hsplit(tst,sn))
    
    #print(tst.shape)
    tstk=np.array(np.hsplit(tstk,sn))
   
    #print(tstk.shape)
    print(tst.shape,tstk.shape)  
    print("Total examples to be sampled: ",mini,"\nTotal example lost: ",c,"\nTotal number of groups formed: ",sn)

#test out the matrices
#print(tst[0:5])

tst=tst.reshape(tst.shape[0],20500)
tstk=tstk.reshape(tstk.shape[0],20500)
print("final shapes of audioset and karaoke audio set: ",tst.shape,tstk.shape)


# ## Spectrogram Fuction

# In[ ]:


def view_spec(y,sr):
    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

    # Convert to log scale (dB). We'll use the peak power (max) as reference.
    log_S = librosa.power_to_db(S, ref=np.max)

    # Make a new figure
    plt.figure(figsize=(12,4))

    # Display the spectrogram on a mel scale
    # sample rate and hop length parameters are used to render the time axis
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')

    # Put a descriptive title on the plot
    plt.title('mel power spectrogram')

    # draw a color bar
    plt.colorbar(format='%+02.0f dB')

    # Make the figure layout compact
    plt.tight_layout()


# ## Defining the DNN Model
# 
# Our input layer comes out to be 1025 x 20 = 20500
# 
# * We will have a DNN of 3 layers. Each layer will have 20500 hidden units.<br/>
# * The activation function is going to be * biased sigmoid* function.<br/> 
# * It shall have no bias in the output layer.<br/>
# * NN size= 20500 x 20500 x 20500<br/>
# * It is implemented in this way to form a digital mask over the frequency spectogram
# 

# In[ ]:


#creating our model
model=Sequential()
model.add(Dense(20500,activation="sigmoid",input_shape=(20500,1)))
model.add(Dense(20500,activation="sigmoid"))
model.add(Dense(20500,activation="sigmoid"))
model.summary()

