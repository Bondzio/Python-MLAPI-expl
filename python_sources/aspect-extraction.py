#!/usr/bin/env python
# coding: utf-8

# In[23]:


from nltk import pos_tag
import pandas as pd


# In[24]:


dataset = pd.read_csv('../input/amazon-reviews-unlocked-mobile-phones/Amazon_Unlocked_Mobile.csv')
dataset['Reviews']=dataset['Reviews'].astype(str) #it is used to convert the type of Reviews from float to string


# In[25]:


dataset.head()


# In[ ]:


tagged_Reviews = dataset['Reviews'].str.split().map(pos_tag)
tagged_Reviews.head()
dataset['Tagged_Review'] = tagged_Reviews


# *Download created csv*

# In[ ]:


from IPython.display import HTML
import numpy as np

dataset.to_csv('submission.csv') #dataframe that will be downloaded as csv

def create_download_link(title = "Download CSV file", filename = "data.csv"):  
    html = '<a href={filename}>{title}</a>'
    html = html.format(title=title,filename=filename)
    return HTML(html)

# create a link to download the dataframe which was saved with .to_csv method
create_download_link(filename='submission.csv')


# In[26]:


dataset = pd.read_csv('../input/tagged-amazon-reviews/Amazon_Unlocked_Mobile_Tagged.csv')


# In[27]:


# selecting a part of the dataframe
sample_df = dataset[:10]
sample_df


# In[28]:


import spacy
nlp = spacy.load('en')

dataset.review = sample_df.Reviews.str.lower()


# In[29]:


aspect_terms = []
for review in nlp.pipe(dataset.review):
    chunks = [(chunk.root.text) for chunk in review.noun_chunks if chunk.root.pos_ == 'NOUN']
    aspect_terms.append(' '.join(chunks))


# In[30]:


sample_df['aspect_terms'] = aspect_terms


# In[31]:


sample_df

