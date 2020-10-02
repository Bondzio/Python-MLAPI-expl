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


import pickle

DATA_DIR = '/kaggle/input/data-molecules/'
STRUCTURE_FILE = 'structures.csv'
TEST_FEATURES_FILE = 'test_features.csv'
TRAIN_FEATURES_FILE = 'train_features.csv'

molecules_test_edge = {}
structure_file = pd.read_csv(DATA_DIR + STRUCTURE_FILE)

for test_features_file in pd.read_csv(DATA_DIR + TEST_FEATURES_FILE, chunksize=1000):
    for name, data in test_features_file.groupby('molecule_name'):
        num_nodes_molecule = structure_file.loc[structure_file['molecule_name'] == name].shape[0]
        molecule = np.zeros(( num_nodes_molecule ** 2, 9))
        data_ = data.values
        for row in data_:
            i = row[7]
            j = row[8]
            m = row[[18, 19, 20, 21, 23, 24, 25, 26, 27]]
            molecule[i * num_nodes_molecule + j] = m
            molecule[i + j * num_nodes_molecule] = m
      
        molecules_test_edge[name] = molecule  
    print(len(molecules_test_edge)) 
    with open('test_edge_features.pkl', 'wb') as f:
        pickle.dump(molecules_test_edge, f)
    with open('test_edge_features.pkl', 'rb') as f:
        molecules_test_edge = pickle.load(f)
        
    print(len(molecules_test_edge))

print('finish_gen')


# In[ ]:


df = pd.read_csv(DATA_DIR + TEST_FEATURES_FILE)
print(df['molecule_name'].nunique())

print('_________________________')
print('DONE')


# In[ ]:


from subprocess import check_output
print(check_output(["ls", "../working"]).decode("utf8"))


# In[ ]:


from IPython.display import FileLink
FileLink(r'test_edge_features.pkl')

