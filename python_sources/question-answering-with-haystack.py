#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system(' pip install farm-haystack')
get_ipython().system('pip install PyPDF2')
get_ipython().system('pip install wget')


# In[ ]:


from haystack import Finder
from haystack.indexing.cleaning import clean_wiki_text
from haystack.indexing.io import write_documents_to_db, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.database.memory import InMemoryDocumentStore
document_store = InMemoryDocumentStore()


# In[ ]:


import os
doc_dir = "data/article"
if not os.path.exists(doc_dir):
        os.makedirs(doc_dir)


# In[ ]:


import wget
wget.download(url='https://docsmsftpdfs.blob.core.windows.net/guides/azure/azure-ops-guide.pdf', out=doc_dir)


# In[ ]:


import PyPDF2
article=[]
pdfFileObj = open('data/article/azure-ops-guide.pdf', 'rb') 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
for page in range(pdfReader.numPages):
  pageObj = pdfReader.getPage(page)
  article.append(pageObj.extractText())
article_text = open('data/article/azure-ops-guide.txt',"w")
article_text.writelines(article)


# In[ ]:


write_documents_to_db(document_store=document_store, document_dir=doc_dir, clean_func=clean_wiki_text, only_empty_db=True)


# In[ ]:


from haystack.retriever.tfidf import TfidfRetriever
retriever = TfidfRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False, no_ans_boost=-5)
finder = Finder(reader, retriever)


# In[ ]:


prediction = finder.get_answers(question="What is Azure Portal?", top_k_retriever=10, top_k_reader=5)
print('\n\n')
top_answer=prediction['answers'][0]['answer']


# In[ ]:


print('Answer:',top_answer)


# In[ ]:


prediction = finder.get_answers(question="Who is Anirban?", top_k_retriever=10, top_k_reader=5)
print('\n\n')
top_answer=prediction['answers'][0]['answer']


# In[ ]:


print('Answer:',top_answer)

