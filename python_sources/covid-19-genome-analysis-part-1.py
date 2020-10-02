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


import Bio
from Bio.SeqIO import parse,read , to_dict


# ### Parsing the Genome Sequence to get a generator Object

# In[ ]:


# Getting a generator object.
cor_seq = [cor_seq for cor_seq in parse("/kaggle/input/coronavirus-genome-sequence/MN908947.fna","fasta")]
# Converting this sequence into a dictionary.
cor_seq_dict = to_dict(cor_seq)


# In[ ]:


print(cor_seq_dict)


# ### Reading the Genome Sequence

# In[ ]:


cor = read("/kaggle/input/coronavirus-genome-sequence/MN908947.fna","fasta")
print(cor.seq)


# In[ ]:


# As we can see the T's in the Sequence we can predict that it is either a DNA or a Protein. By the information of
# data we can say that it cannot be a protein sequence.                                                    


# At last of this sequence we can see there are multiple A's , this is due to the Polymerase chain Reaction.

# ### Taking complement of the sequence

# In[ ]:


# Taking the compliment.
cor_com = cor_seq[0].seq.complement()
repr(cor_com)


# ### Transcribing the Sequence to get a RNA Sequence

# In[ ]:


# Transcribing the sequence
cor_rna = cor_seq[0].seq.transcribe()
print(cor_rna)


# ### Translating the Sequence to Protein

# Translating the 
# 1. DNA Sequence 
# 2. RNA Sequence<br>
# 
# Both to Protein Sequence

# In[ ]:


# Translation
# 1.
protein = cor_seq[0].seq.translate()
print(protein)
# 2.
pr = cor_rna.translate()
pr


# In[ ]:


# Getting the positions of Stop codons
# Stop in the first occurences of stop codons
cor_seq[0].seq.translate(to_stop=True)


# ### Getting the Transition Table

# In[ ]:


# The translation table that we used is standard transition table and it is by-default in used in BioPython
import Bio.Data.CodonTable as CodonTable
print(CodonTable.unambiguous_dna_by_name["Standard"])


# ### Splitting the Protein

# In[ ]:


# Spltting the protein according to the stop codons
protn = protein.split("*")
for each in protn:
    if each==" ":
        continue
    print(each)


# ### GC percent of Sequence

# In[ ]:


# Now calculating the GC% in the given sequence
from Bio.SeqUtils import GC
print(f"GC% :{GC(cor_seq[0].seq)}")


# #### In the Next part I'll be discussing some other information regarding the genome sequence.
# If u liked my work please hit upvote !

# In[ ]:




