#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json

# Input data files are available in the "../input/" directory.
#####################################################################################
#thanks for your work vasuji https://www.kaggle.com/vasuji/i-covid19-nlp-data-parsing
#####################################################################################
import os

datafiles = []
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        ifile = os.path.join(dirname, filename)
        if ifile.split(".")[-1] == "json":
            datafiles.append(ifile)


# In[ ]:


with open(datafiles[0], 'r')as f1:
    sample = json.load(f1)


# In[ ]:


for key,value in sample.items():
    print(key)


# In[ ]:


print(sample['metadata'].keys())
print('abstract: ',sample['abstract'][0].keys())
print('body_text: ',sample['body_text'][0].keys())
print('bib_entries: ',sample['bib_entries'].keys())
print('ref_entries: ', sample['ref_entries'].keys())
print('back_matter: ',sample['back_matter'][0].keys())


# In[ ]:


id2title = []
for file in datafiles:
    with open(file,'r')as f:
        doc = json.load(f)
    id = doc['paper_id'] 
    title = doc['metadata']['title']
    id2title.append({id:title})


# In[ ]:


id2title[0:5]


# In[ ]:


id2abstract = []
for file in datafiles:
    with open(file,'r')as f:
        doc = json.load(f)
    id = doc['paper_id'] 
    abstract = ''
    for item in doc['abstract']:
        abstract = abstract + item['text']
        
    id2abstract.append({id:abstract})


# In[ ]:


id2bodytext = []
for file in datafiles:
    with open(file,'r')as f:
        doc = json.load(f)
    id = doc['paper_id'] 
    bodytext = ''
    for item in doc['body_text']:
        bodytext = bodytext + item['text']
        
    id2bodytext.append({id:bodytext})


# In[ ]:


id2abstract[0]


# In[ ]:


id2bodytext[0]


# scispaCy is a Python package containing spaCy models for processing biomedical, scientific or clinical text.

# In[ ]:


get_ipython().system('pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_ner_bionlp13cg_md-0.2.4.tar.gz')
get_ipython().system('pip install scispacy')


# In[ ]:


import scispacy
import en_ner_bionlp13cg_md
#A spaCy NER model trained on the BIONLP13CG corpus


# In[ ]:


from spacy import displacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.umls_linking import UmlsEntityLinker


# In[ ]:


nlp = en_ner_bionlp13cg_md.load()


# In[ ]:


text = id2abstract[0].get(list(id2abstract[0].keys())[0])


# In[ ]:


doc = nlp(text)
d_i=displacy.render(doc,jupyter=True,style='ent')


# > **We can also visualise dependency parses**

# In[ ]:


displacy.render(next(doc.sents), style='dep', jupyter=True)


# In[ ]:


for x in doc.ents:
    print(x.text,x.label_)


# In[ ]:


text1 = id2bodytext[0].get(list(id2bodytext[0].keys())[0])


# In[ ]:


doc1 = nlp(text1)
d_i=displacy.render(doc1,jupyter=True,style='ent')


# In[ ]:


for x in doc1.ents:
    print(x.text,x.label_)


# In[ ]:


chemicals = []
for i in range (len(id2abstract)):
    pid = list(id2abstract[i].keys())[0]
    text = id2abstract[i].get(pid)
    doc = nlp(text)
    for en in doc.ents:
        if en.label_== 'SIMPLE_CHEMICAL':
            chemicals.append(en)


# In[ ]:





# In[ ]:


chemicals[0:100]


# In[ ]:


type(chemicals[0])


# In[ ]:


chem = list(map(str, chemicals)) # => [1,2,3]


# In[ ]:


from collections import Counter
c = Counter(chem) #stuck near getting the frequency of chemicals


# In[ ]:


common_chem = c.most_common(10)
common_chem


# In[ ]:


import matplotlib.pyplot as plt
common_chem = dict(common_chem)


plt.bar(range(len(common_chem)), list(common_chem.values()),align='center')
plt.xticks(range(len(common_chem)), list(common_chem.keys()))
plt.show()


# In[ ]:




