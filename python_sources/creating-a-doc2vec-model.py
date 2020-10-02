#!/usr/bin/env python
# coding: utf-8

# **Creating a Doc2Vec Model**
# 
# The joy of word2vec is that it will retain the context within the paragraphs, resulting in more meaningful vector values. My plan was to use this to quickly group documents together, making it faster to find resources. 
# 
# The first couple of word2vec / doc2vec models I attempted to build were a bit of a struggle, so I thought it might be useful for people to see the process here. 
# 
# At the end of this notebook the model is saved as a .model file, so there's no need to run the long training regime again, you can just laod the model and off you go. 
# 
# Other ideas were to create a new feature that represents the average vector for each text body, using this to cluster the documents together and possibly assign labels to begin automating coronavirus risk extraction. 
# 
# -------------------------------------------
# 
# As ever the first thing to do is import the libraries. 
# 

# To achieve the desired result we only need a few modules. 
# 
# 1. Gensim: An amazing word2vec / doc2vec library that allows you to build your own d2v models, as well as load pre-trained models. Brilliant documentation as well. 
# 
# 2. NLTK: Brilliant NLP library! Has everythig the aspiring NLP magician needs. 

# In[ ]:


from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pandas as pd
import sys
sys.path.insert(0, "../")


# **Replace NaN Function**
# 
# I use this function later in the notebook to replace an empty string with a np.nan object. This allows us to easily remove missing values using built-in pandas methods. 

# In[ ]:


def replace_none(X):
    if X == '':
        X = np.nan
    return X


# **Train Model Function**
# 
# To keep things tidy I put the training of the model into a little function. 
# 
# -----------------------------------------

# In[ ]:


def build_model(max_epochs, vec_size, alpha, tagged_data):
    
    model = Doc2Vec(vector_size=vec_size,
               alpha=alpha,
               min_alpha=0.00025,
               min_count=1,
               dm=1)
    
    model.build_vocab(tag_data)
    
    # With the model built we simply train on the data.
    
    for epoch in range(max_epochs):
        print(f"Iteration {epoch}")
        model.train(tag_data,
                   total_examples=model.corpus_count,
                   epochs=model.epochs)

        # Here I decrease the learning rate. 

        model.alpha -= 0.0002

        model.min_alpha = model.alpha
    
    # Now simply save the model to avoid training again. 
    
    model.save("COVID_MEDICAL_DOCS_w2v_MODEL.model")
    print("Model Saved")
    return model


# **The Data**
# 
# The data is loaded from the .csv file that was created in a previous kernel. 
# 
# https://www.kaggle.com/fmitchell259/create-corona-csv-file

# In[ ]:


corona_df = pd.read_csv("../input/covid19-medical-paperscsv/kaggle_covid-19_open_csv_format.csv")


# **The Corpus**
# 
# In order to build the model we need to provide the doc2vec object with the entire corpus. 
# 
# All paper text body and titles are used to build a skip-gram model.
# 
# ----------------------------------------
# 
# First though, I check the null values from the parsing. I've lost 944 titles, but for the purposes of building a corpus, we are just within the 5% range. 
# 
# The large missing values in abstract is negligable, as the text_body will reflect the abstract. 

# In[ ]:


corona_df.isnull().sum()


# So I drop these values and gather all the data to train the d2v model using my wee function above. 

# In[ ]:


corona_df['title'] = corona_df['title'].apply(replace_none)
corona_df['text_body'] = corona_df['text_body'].apply(replace_none)
corona_df = corona_df.dropna()

w2v_data_body = list(corona_df['text_body'])
w2v_data_title = list(corona_df['title'])

w2v_total_data = w2v_data_body + w2v_data_title


# Lastly we need to use the Gensim DocumeNt Tagger to apply some typical preprocessing steps for any NLP system. 
# 
# 1. Tokenise: Split paragraphs into tokens (each seperate word is a token), making all the words lower case. 
# 
# 2. Stemming: The word_tokenize function takes care of stemming. 
# 
# 3. Stopword Removel: Likewise the word_tokenzie function takes care of this step. 
# 
# ----------------------------
# 
# Be warned, if you're doing this yourself, this can take a while depending on computing power. 

# In[ ]:


tag_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(w2v_total_data)]


# **Setting Up The Model**
# 
# With the data all in the one list we can go ahead and  create a model using custom parameters. For more on these parameters check the gensim documentation. It's really good!
# 
# https://radimrehurek.com/gensim/auto_examples/index.html
# 
# -------------------------------
# 
# Again, be warned, this can take a while depending on compute power, for this reason I have set the epochs very low. This number is enough to generate sufficient word vectors, however it can be tuned as required. Also note that there is no need for you to run this again (unless you require more epochs), as it is very simple to load a pre-trained doc2vec model, as demonstrated at the end of this notebook.  

# In[ ]:


model = build_model(max_epochs=5, vec_size=10, alpha=0.025, tagged_data=tag_data)


# **A Demo**
# 
# So now the model is built we can ask it to vectorise unseen documents, return documents with similiar vectors or maybe create some features as mentioned above. 
# 
# --------------------------------
# 
# As a quick demo here are the words with which we can test the model, the words chosen have a particular relation to the task at hand (number 2, the risks).
# 
# I think you'll agree, even at this first pass, the results are interesting. 
# 
# --------------------------------------
# 
# 1. risk
# 2. symptoms
# 3. pregnant
# 4. economy
# 5. isolation
# 
# ----------------------------------------------------------

# In[ ]:


model.wv.similar_by_word("risk")


# In[ ]:


model.wv.similar_by_word("symptoms")


# In[ ]:


model.wv.similar_by_word("pregnant")


# In[ ]:


model.wv.similar_by_word("economy")


# In[ ]:


model.wv.similar_by_word("isolation")


# **And That's It!**
# 
# It's as simple as that to construct meaningful word vectors for documents. I really hope this helps someone get up and running with this data faster. I love building these wee tools so will aim to post anythng that might be remotely useful.
# 
# -------------------------------------------
# 
# Bear in mind the functionality you get with NLTK and Gensim is enormous, they are absoutely brilliat and powerful NLP libraries that are incredibly useful, well documented and - to be honest - an outright joy to use. 
# 
# ---------------------------------------------------------------
# 
# Please note that this model only ran for 5 iterations, and while this is good enough to achieve the needed word vectors (and easier on the kernel CPU), this parameter can be tuned as required. 
