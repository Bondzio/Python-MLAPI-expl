#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# keep only documents with covid -cov-2 and cov2
def search_focus(df):
    dfa = df[df['abstract'].str.contains('covid')]
    dfb = df[df['abstract'].str.contains('-cov-2')]
    dfc = df[df['abstract'].str.contains('cov2')]
    dfd = df[df['abstract'].str.contains('ncov')]
    frames=[dfa,dfb,dfc,dfd]
    df = pd.concat(frames)
    df=df.drop_duplicates(subset='title', keep="first")
    return df

# load the meta data from the CSV file using 3 columns (abstract, title, authors),
df=pd.read_csv('/kaggle/input/CORD-19-research-challenge/metadata.csv', usecols=['title','journal','abstract','authors','doi','publish_time','sha','full_text_file'])
print (df.shape)
#drop duplicates
#df=df.drop_duplicates()
#drop NANs 
df=df.fillna('no data provided')
df = df.drop_duplicates(subset='title', keep="first")
# convert abstracts to lowercase
df["abstract"] = df["abstract"].str.lower()+df["title"].str.lower()
#show 5 lines of the new dataframe
df=search_focus(df)
print (df.shape)
df.head()


# In[ ]:


from search_func_py import *

################ main program
# list of lists of search terms
search=[['incubation','period','age', 'statistical', 'significance', 'quarantine']]

for search_words in search:
    str1=''
    # a make a string of the search words to print readable version above table
    str1=' '.join(search_words)
    
    #search the dataframe for all words
    df1=search_dataframe(df,search_words)

    # analyze search results for relevance 
    df1=search_relevance(df1,search_words)

    # get best sentences
    df_table=get_sentences(df1,search_words)
    
    #convert df to html
    df_table=HTML(df_table.to_html(escape=False,index=False))
    # display search topic
    display(HTML('<h3>Search: '+str1+'</h3>'))
    #display table
    display(df_table)

print ('done')

