#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sentencepiece as spm
spr = spm.SentencePieceProcessor()
spr.Load('../input/en.wiki.bpe.op1000.model')
tokens = spr.EncodeAsPieces('this is a test')
tokens


# In[ ]:


from gensim.models import KeyedVectors
model = KeyedVectors.load_word2vec_format('../input/en.wiki.bpe.op1000.d25.w2v.bin', binary=True)
bpe_embs = model[tokens]
bpe_embs.shape


# In[ ]:


bpe_embs[0]


# In[ ]:




