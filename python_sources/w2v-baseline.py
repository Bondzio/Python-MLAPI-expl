#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tqdm
import gensim
import pickle


# In[ ]:


meta = pd.read_csv('../input/track_meta.tsv', sep='\t')
meta['band'] = meta['band'].astype(str)

id_to_band = meta.set_index('song_id')['band'].to_dict()


# In[ ]:


get_ipython().system('rm playlists.csv')


# In[ ]:


for chunk in pd.read_csv('../input/user_item_interaction.csv', 
                                   iterator=True,
                                   chunksize=1000000,
                                   lineterminator='\n',
                                   # remove this to use whole dataset
                                   nrows=5000000,
                                   ##################################
                                  ):

    chunk.columns = ['user', 'track']
    chunk['band'] = chunk['track'].apply(lambda song_id: id_to_band.get(song_id, ''))
    chunk = chunk.groupby('user')['band'].apply(','.join).reset_index()

    chunk[['band']].to_csv('playlists.csv', header=None, index=None, mode='a')


# In[ ]:


class TextToW2V(object):
    def __init__(self, file_path):
        self.file_path = file_path


    def __iter__(self):
        for line in open(self.file_path, 'r'):
            yield line.lower().split(',')[::-1]  # reverse order (make old -> new)

playlists = TextToW2V('playlists.csv')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'estimator = gensim.models.Word2Vec(playlists,\n                                   window=15,\n                                   min_count=30,\n                                   sg=1,\n                                   workers=4,\n                                   iter=10,\n                                   ns_exponent=0.8,\n                                  )')


# In[ ]:


with open('/kaggle/working/w2v_small.pkl', 'wb') as f:
    pickle.dump(estimator, f)


# In[ ]:


user_music = ['led zeppelin', 'Nirvana', 'Pink Floyd']
user_music = [m.lower().strip() for m in user_music]
predicted = estimator.predict_output_word(user_music)

[a[0] for a in predicted if a[0] not in user_music]


# In[ ]:




