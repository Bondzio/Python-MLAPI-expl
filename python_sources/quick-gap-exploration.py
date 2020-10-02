#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import seaborn as sns
sns.set()
sns.set_palette("pastel")

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Just a first brief look at the data given by this competition and the data that is available on the github page https://github.com/google-research-datasets/gap-coreference.
# 
# In order to directly load the data from github you need to use the raw content of the page and enable the Internet connection in the kernel settings. Probably this is obvious but it took me some time to realize and maybe it helps someone to save time ;)

# ## Load GAP Coreference Data
# 
# 

# In[ ]:


gap_train = pd.read_csv("https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-development.tsv", delimiter='\t')
gap_test = pd.read_csv("https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-test.tsv", delimiter='\t')
gap_valid = pd.read_csv("https://raw.githubusercontent.com/google-research-datasets/gap-coreference/master/gap-validation.tsv", delimiter='\t')


# ## Load Competition Data

# In[ ]:


test_stage_1 = pd.read_csv('../input/test_stage_1.tsv', delimiter='\t')
sub = pd.read_csv('../input/sample_submission_stage_1.csv')


# ## Exploration

# ### Gap Train

# In[ ]:


gap_train.head()


# ### Gap Test

# In[ ]:


gap_test.head()


# ### Gap Valid

# In[ ]:


gap_valid.head()


# ### Test Stage 1

# In[ ]:


test_stage_1.head()


# ### Countplot Pronouns

# In[ ]:


fig, ax = plt.subplots(1, 4, figsize=(20,6))
ordering = ['her', 'his', 'she', 'he', 'She', 'He', 'him', 'Her', 'His', 'hers']

sns.countplot(y='Pronoun',order = ordering, ax=ax[0], data=gap_train)
ax[0].set_title("GAP Train")

sns.countplot(y='Pronoun',order = ordering, ax=ax[1], data=gap_test)
ax[1].set_title("GAP Test")

sns.countplot(y='Pronoun',order = ordering, ax=ax[2], data=gap_valid)
ax[2].set_title("GAP Valid")

sns.countplot(y='Pronoun',order = ordering, ax=ax[3], data=test_stage_1)
ax[3].set_title("Test Stage 1");


# ### Distplot Pronoun-offset, A-offset, B-offset

# In[ ]:


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20,12))

sns.distplot(gap_train["Pronoun-offset"], ax=ax1, label="Pronoun-offset", kde=True)
sns.distplot(gap_train["A-offset"], ax=ax1, label="A-offset", kde=True)
sns.distplot(gap_train["B-offset"], ax=ax1, label="B-offset", kde=True)
ax1.set_title("GAP Train")
ax1.set(xlabel='Offset')

sns.distplot(gap_test["Pronoun-offset"], ax=ax2, label="Pronoun-offset", kde=True)
sns.distplot(gap_test["A-offset"], ax=ax2, label="A-offset", kde=True)
sns.distplot(gap_test["B-offset"], ax=ax2, label="B-offset", kde=True)
ax2.set_title("GAP Test")
ax2.set(xlabel='Offset')

sns.distplot(gap_valid["Pronoun-offset"], ax=ax4, label="Pronoun-offset", kde=True)
sns.distplot(gap_valid["A-offset"], ax=ax4, label="A-offset", kde=True)
sns.distplot(gap_valid["B-offset"], ax=ax4, label="B-offset", kde=True)
ax4.set_title("GAP Valid")
ax4.set(xlabel='Offset')

sns.distplot(test_stage_1["Pronoun-offset"], ax=ax3, label="Pronoun-offset", kde=True)
sns.distplot(test_stage_1["A-offset"], ax=ax3, label="A-offset", kde=True)
sns.distplot(test_stage_1["B-offset"], ax=ax3, label="B-offset", kde=True)
ax3.set_title("Test Stage 1")
ax3.set(xlabel='Offset')
plt.legend();


# ### Countplot A-coref

# In[ ]:


fig, ax = plt.subplots(1, 3, figsize=(20,3))
ordering = [True, False]

sns.countplot(y='A-coref', order = ordering, ax=ax[0], data=gap_train)
ax[0].set_title("GAP Train")

sns.countplot(y='A-coref',order = ordering, ax=ax[1], data=gap_test)
ax[1].set_title("GAP Test")

sns.countplot(y='A-coref',order = ordering, ax=ax[2], data=gap_valid)
ax[2].set_title("GAP Valid");


# ### Countplot B-coref

# In[ ]:


fig, ax = plt.subplots(1, 3, figsize=(20,3))
ordering = [True, False]

sns.countplot(y='B-coref', order = ordering, ax=ax[0], data=gap_train)
ax[0].set_title("GAP Train")

sns.countplot(y='B-coref',order = ordering, ax=ax[1], data=gap_test)
ax[1].set_title("GAP Test")

sns.countplot(y='B-coref',order = ordering, ax=ax[2], data=gap_valid)
ax[2].set_title("GAP Valid");

