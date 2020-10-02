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
songs = []
cwd = '/kaggle/input/birdsongs-from-europe/mp3/'

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        #print(os.path.join(dirname, filename))
        songs.append(filename)
data = pd.read_csv('/kaggle/input/birdsongs-from-europe/metadata.csv')
songs.pop(0)

print(data.head())
print(data.info(verbose=True))


# ## Playing MP3
# Lets install and use pydub to play the MP3 files.
# You're notebook will need internet access (see settings).

# In[ ]:


get_ipython().system(' pip install pydub')


# In[ ]:


from pydub import AudioSegment
import IPython

# We will listen to this file:
# 213_1p5_Pr_mc_AKGC417L.wav
file = '/kaggle/input/birdsongs-from-europe/mp3/Hirundo-rustica-361750.mp3'
print(cwd+songs[0])
IPython.display.Audio(cwd+songs[2])


# ## Convert MP3 into WAVs.
# This process is modeled after the notebook [here](https://www.kaggle.com/rakibilly/extract-audio-starter).  
# We must include files from the ffmpeg-static-build into our notebook, and unpack them.  
# Then we use the subprocess module to use ffmpeg to convert them to WAV
# 
# ###### Because my notebook environment has limited memory, lets only convert the first 50

# In[ ]:


# https://www.kaggle.com/rakibilly/extract-audio-starter
import subprocess
import glob
import os
from pathlib import Path
import shutil
from zipfile import ZipFile


# In[ ]:


get_ipython().system(' tar xvf ../input/ffmpeg-static-build/ffmpeg-git-amd64-static.tar.xz')


# In[ ]:


# Convert MP3s to WAV for easy conversion to numpy arrays:
output_format = 'wav'  # can also use aac, wav, etc
output_dir = Path(f"{output_format}s")
Path(output_dir).mkdir(exist_ok=True, parents=True)

#Only do first 50 because notebook memory limitations...
for song in songs[:50]:
    file = cwd+song
    file_name = song.replace(".mp3","")
    command = f"../working/ffmpeg-git-20191209-amd64-static/ffmpeg -i {file} -ab 192000 -ac 2 -ar 44100 -vn {output_dir/file_name}.{output_format}"
    subprocess.call(command, shell=True)


# ## Convert WAVs to numpy arrays
# These data objects will be dictionaries that include the name of the original mp3 file, the sample rate, and left & right audio data.

# In[ ]:


from scipy.io.wavfile import read, write
#a = read("adios.wav")
wavs = []
np_arrays = []
for dirname, _, filenames in os.walk('/kaggle/working/wavs/'):
    for filename in filenames:
        wav_file = dirname+filename
        #print(wav_file)
        wavs.append(wav_file)
        try:
            fs, io_file = read(wav_file)
        except ValueError:
            continue
        data = np.array(io_file,dtype=float)
        wav_info= {
            'name': filename,
            'fs' : fs,
            'left': data[:,0],
            'right': data[:,1]
        }
        
        np_arrays.append(wav_info)

print("Succesfully converted: "+str(len(np_arrays)))


# ## Plot & Play 
# Plot a sample using a spectrogram (should really use wavelets) and then play the selected sample.
# Load the song data you want to play from the generated numpy arrays (np_arrays).
# Select the starting time in seconds (start), and ending time in seconds (end), or set to None if you want to play the whole file.

# In[ ]:


from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt

song_data = np_arrays[26]
start = 0
end = 10

if end != None:
    wav = song_data['left'][fs*start:fs*end]
else:
    wav = song_data['left'][fs*start:]
fs = song_data['fs']
plt.specgram(wav,Fs=fs)
plt.ylim(top=15000)
print(song_data['name'].replace(".wav",""))
plt.show() 

IPython.display.Audio(wav, rate=fs)


# ## To-Do: Denoise
# I suspect this should definitely be done with wavelet decomposition, not fourier methods.

# In[ ]:


get_ipython().system(' pip install pyyawt')


# In[ ]:


# Load a noisy signal
# Phylloscopus-collybita-171141

song_data = np_arrays[4]
start = 1
end = 12

if end != None:
    wav = song_data['left'][fs*start:fs*end]
else:
    wav = song_data['left'][fs*start:]
fs = song_data['fs']
plt.specgram(wav,Fs=fs)
plt.ylim(top=15000)
print(song_data['name'].replace(".wav",""))
plt.show() 

IPython.display.Audio(wav, rate=fs)


# In[ ]:


import seaborn as sns
import pywt
import pyyawt

stds = []
means = []
decomps = []
thrs = []
wavelets = pywt.wavedec(wav, 'db5', level=10)

for i, wavelet in enumerate(wavelets):
    thrs.append(pyyawt.thselect(wavelet, 'heursure'))
    stds.append(wavelet.std(0))
    means.append(wavelet.mean(0))
    decomps.append(wavelet)
    
    #ax[i+1,0].plot(wavelet)
    #ax[i+1,0].plot(wavelet)
    #sns.distplot(wavelet, ax=ax[i+1,1], hist=False, vertical=True)

thresholded = []

fig, ax = plt.subplots(len(wavelets), figsize=(20,20))


for i, decomp in enumerate(decomps):
    thresh =((np.amax(decomp)-means[i])*thrs[i])
    print(thrs[i], np.amax(decomp), thresh)
    thresholded.append(pywt.threshold(decomp, thresh, 'soft'))
    ax[i].plot(wavelets[i])
    ax[i].plot(thresholded[i])

print("Denoised: "+song_data['name'].replace(".wav",""))
reconstructed = pywt.waverec(thresholded, 'db5')
plt.specgram(reconstructed,Fs=fs)
plt.show()
IPython.display.Audio(reconstructed, rate=fs)


# In[ ]:




