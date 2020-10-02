#!/usr/bin/env python
# coding: utf-8

# # CORD-19 Metadata Enrichment [3/x]: Augmenting data with information from Microsoft Project Academic Knowledge

# [<img src = "https://docs.microsoft.com/en-us/academic-services/media/project-academic-knowledge-banner.png">](https://docs.microsoft.com/en-us/academic-services/project-academic-knowledge/introduction)
# 
# 

# >Welcome to Project Academic Knowledge. With this service, you will be able to interpret user queries for academic intent and retrieve rich information from the Microsoft Academic Graph (MAG). The MAG knowledge base is a web-scale heterogeneous entity graph comprised of entities that model scholarly activities: field of study, author, institution, paper, venue, and event.

# ## [CORD-19 Metadata Enrichment Dataset](https://www.kaggle.com/dannellyz/cord19-metadata-enrichment)
# 
# This notebook builds on other work seeking to provide additional, augmented, and normalized data across the CORD-19 dataset. Those other notebooks can be found here:
# 1. [CORD-19 Metadata Enrich NIH API](https://www.kaggle.com/dannellyz/cord19-metadata-enrich-nih-api)
# 2. [CORD-19 Metadata Enrich Altmetric API](https://www.kaggle.com/dannellyz/cord19-metadata-enrich-altmetric-api)

# ### Start by adding the Metadata Enrichment dataset with the * + Add data * button on right --> 
# #### Search by url: https://www.kaggle.com/dannellyz/cord19-metadata-enrichment

# In[ ]:


import pandas as pd
import numpy as np

base_file_path = "/kaggle/input/CORD-19-research-challenge/"
enrich_file_path = "/kaggle/input/cord19-metadata-enrichment/"

#Can either go ahead with the enriched metdata or the base
metadata = pd.read_csv(base_file_path + "metadata.csv", index_col="cord_uid")

#Grab those that have DOIs as its the selector for the API
meta_has_doi = metadata[metadata.doi.notnull()]
meta_has_doi.shape


# In[ ]:


#Get the API Features of the Microsoft Academic API
micsoft_api_feats = pd.read_csv(enrich_file_path + "microsoft_api_features.csv")
micsoft_api_feats


# In[ ]:


#Get a list of the attributes to add to the search strings
micro_attrib_list = list(micsoft_api_feats.Attribute)

#Drop those you are not interested in
#E: Extended metadata has been depreciated
micro_attrib_list.remove("E")

#Take the attributes and format the API search string
search_string = ",".join(list(micsoft_api_feats.Attribute))
search_string


# In[ ]:


#Load API key from Kaggle Secret
#Can add-on secret at top of notebook
#Can apply for a free API key here: https://msr-apis.portal.azure-api.net/products

from kaggle_secrets import UserSecretsClient
secret_label = "microsoft_api_key"
secret_value = UserSecretsClient().get_secret(secret_label)
api_key = secret_value


# ## Utilize threading in order to greatly increase call speed

# In[ ]:


import requests
import json
import concurrent.futures
import itertools
from tqdm.notebook import tqdm

#Base API Url
base_url = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate"

#Format the DOIs for query
#Each should read "DOI = '[DOI]'"
doi_list = list(meta_has_doi.doi)
query_list = ["DOI = '" + doi +"'" for doi in doi_list]

#Code to split the DOI list into sublsists len = 10
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]      
split_querys = list(chunks(query_list,10))

#DOI Query is all DOIs joined enclosed with OR(...)
def make_doi_query(dois):
    prefix = "OR("
    dois = ",".join(dois)
    suffix = ")"
    return prefix + dois + suffix

api_responses = []
headers = {'Ocp-Apim-Subscription-Key': api_key}

def api_call(query_list):
    params = {"expr": make_doi_query(query_list), "attributes": search_string}
    r = requests.get(base_url, headers=headers, params=params)
    if r.ok:
        return r.json()["entities"]
    else:
        return 

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    map_obj = tqdm(executor.map(api_call, split_querys), total=len(split_querys))
    microsoft_api_df = pd.DataFrame(list(itertools.chain(*map_obj)))


# In[ ]:


#Available Data
val_counts = pd.DataFrame(microsoft_api_df.notna().sum(axis=0), columns=["present_count"])
val_counts["pct_avail_microsoft"] = val_counts["present_count"] / len(microsoft_api_df)
val_counts["pct_avail_all_data"] = val_counts["present_count"] / len(metadata)
val_counts[val_counts["present_count"] > 0].sort_values(by="present_count", ascending=False)


# In[ ]:


#Save to csv
microsoft_api_df.to_csv("microsoft_academic_metadata.csv")

