#!/usr/bin/env python
# coding: utf-8

# # COVID-19 Symptoms
# 
# There has been some concern that severe Covid-19 infections can present in multiple different ways. See: https://www.esicm.org/wp-content/uploads/2020/04/684_author-proof.pdf
# 
# This notebook uses augmented metadata from [@davidmezzetti](https://www.kaggle.com/davidmezzetti) created in https://www.kaggle.com/davidmezzetti/cord-19-study-metadata-export

# In[ ]:


import covid19_tools as cv19
import pandas as pd
import re
from IPython.core.display import display, HTML
import html

METADATA_FILE = '../input/CORD-19-research-challenge/metadata.csv'

# Load metadata
meta = cv19.load_metadata(METADATA_FILE)
# Add tags
meta, covid19_counts = cv19.add_tag_covid19(meta)


# In[ ]:


print('Loading full text for tag_disease_covid19')
full_text = cv19.load_full_text(meta[meta.tag_disease_covid19],
                                '../input/CORD-19-research-challenge/')


# In[ ]:


full_text_df = pd.DataFrame(full_text)


# In[ ]:


meta2 = pd.read_csv('../input/cord-19-study-metadata-export/metadata_study.csv')


# In[ ]:


DESIGNS = [
    'Unknown Design (Default for no match)',
    'Systematic Review',
    'Experimental Study (Randomized)',
    'Experimental Study (Non-Randomized)',
    'Ecological Regression',
    'Prospective Cohort',
    'Time Series Analysis',
    'Retrospective Cohort',
    'Cross Sectional',
    'Case Control',
    'Case Study',
    'Simulation'
]


# In[ ]:


meta2['Design'] = meta2.Design.apply(lambda x: DESIGNS[x])


# In[ ]:


case_sensitive_keywords = [
    'PEEP'
]
case_insensitive_keywords = [
    'paO2/fiO2',
    'cmh20',
    'lung injury',
    'ground glass',
    'bilateral infiltrate',
    'recruitability',
    'hypoxia',
    'hypercapnic',
    'hypocapnic'
]


# In[ ]:


hape_df = full_text_df[full_text_df.body_text.astype(str)
                       .str.lower()
                       .str.contains('|'.join(case_insensitive_keywords)) |
                       full_text_df.body_text.astype(str)
                       .str.contains('|'.join(case_sensitive_keywords))]


# In[ ]:


analysis_df = cv19.term_matcher(hape_df, meta,
                           case_sensitive_keywords,
                           case_insensitive_keywords)


# In[ ]:


temp_id = []
html_string = f'<h1>Relevant papers</h1><p><b>{len(hape_df)} papers found</b><br><br>'
for i, row in enumerate(analysis_df.itertuples()):
    current_id = [row.doi, row.authors, row.title]
    if current_id != temp_id:
        temp_id = current_id
        if i > 0:
            html_string += '</ul><br><br>'
        html_string += f'<b><a href="{row.doi}">{html.escape(row.title)}</a></b><br>'
        html_string += f'{row.authors} ({row.publish_time})<br>'
        html_string += f'<i>Research design: {row.design}</i>'
        html_string += '<ul>'
    html_string += f'<li>{html.escape(row.extracted_string)}</li>'
html_string += '</ul'
display(HTML(html_string))
        


# In[ ]:


analysis_df.to_csv('symptoms_hape.csv', index=False)

