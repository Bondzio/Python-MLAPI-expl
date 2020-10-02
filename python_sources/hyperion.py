#!/usr/bin/env python
# coding: utf-8

# 

# # Hyperion - Data Visualisation effort on CORD-19 and associated Coronavirus COVID-19 data
# 
# This page is the entry point for my data visualisation efforts on this topic, in support of the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/). Here you'll find links and info for reviewing the visualisations, technical info on how they were made (relying heavily on Power BI), and the source files.
# 
# It builds upon the work in these Notebooks & Datasets by various authors:
# - [CORD-19 Analysis with Sentence Embeddings](https://www.kaggle.com/davidmezzetti/cord-19-analysis-with-sentence-embeddings/) 
# - [CORD-19: Match Clinical Trials](https://www.kaggle.com/danielwolffram/cord-19-match-clinical-trials)
# - [CORD-19 Study Metadata export](https://www.kaggle.com/davidmezzetti/cord-19-study-metadata-export)
# - [CoronaWhy](http://datasets.coronawhy.org/) 
# - [CoronaWhy.org - Task: Risk Factors](https://www.kaggle.com/arturkiulian/coronawhy-org-task-risk-factors) 
# - [CoronaWhy.org - Task: Transmission & Incubation](https://www.kaggle.com/crispyc/coronawhy-task-ties-patient-descriptions) 
# - [COVID-19 International Clinical Trials](https://www.kaggle.com/panahi/covid-19-international-clinical-trials)
# - [COVID-19 Thematic tagging with Regular Expressions](https://www.kaggle.com/ajrwhite/covid-19-thematic-tagging-with-regular-expressions/) 
# - [COVID-19 Transmission and incubation](https://www.kaggle.com/ajrwhite/covid-19-transmission-and-incubation)
# 
# This work was made possible with the support of:
# [Manga Solutions](https://www.mangasolutions.com/), [NASA Jet Propulsion Laboratory](https://www.jpl.nasa.gov/), [The Gordon and Betty Moore Foundation](https://www.moore.org/), [ZoomCharts](https://www.zoomcharts.com/), [MapBox](https://www.mapbox.com/), [Craydec](craydec.com), [Slack](https://www.slack.com/), [Trello](https://www.trello.com/) 
# 
# ### Contents
# 
# - [AI-Powered Literature Review - Key Scientific Questions](#AI-Powered-Literature-Review---Key-Scientific-Questions) 
# - [AI-Powered Literature Review - Risk Factors](#AI-Powered-Literature-Review---Risk-Factors) 
# - [AI-Powered Literature Review - CoronaWhy Team Task-TIES](#AI-Powered-Literature-Review---CoronaWhy-Team-Task-TIES) 
# - [AI-Powered Literature Review - EDA](#AI-Powered-Literature-Review---EDA) 
# - [CORD-19 Analysis with Sentence Embeddings](#CORD-19-Analysis-with-Sentence-Embeddings)
# - [CORD-19: Match Clinical Trials](#CORD-19:-Match-Clinical-Trials)
# - [CoronaWhy.org - Literature Review](#CoronaWhy.org---Literature-Review)
# - [CoronaWhy.org - Named Entity Recognition](#CoronaWhy.org---Named-Entity-Recognition)
# - [CoronaWhy.org - Task: Risk Factors](#CoronaWhy.org---Task:-Risk-Factors)
# - [CoronaWhy.org - Task: Transmission & Incubation](#CoronaWhy.org---Task:-Transmission-&-Incubation)
# - [COVID-19 Thematic tagging with Regular Expressions](#COVID-19-Thematic-tagging-with-Regular-Expressions)
# - [CORD-19 metadata with CoronaWhy attributes](#CORD-19-metadata-with-CoronaWhy-attributes)
# - [World map of CORD-19 affiliations](#World-map-of-CORD-19-affiliations)
# - [World map of CoronaWhy Team](#World-map-of-CoronaWhy-Team)

# # AI-Powered Literature Review - Key Scientific Questions
# The source dataset is the /Kaggle/target_tables files within the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/) dataset. This data has been curated by a large team of domain experts, based on ouput from ML authors attacking the various questions & topics. 
# 
# What's new:
# * 2020-06-10 08:00 UTC - refreshed for CORD-19 v29 2020-06-09.
# * 2020-06-04 03:50 UTC - refreshed for CORD-19 v28 2020-06-03.
# * 2020-06-03 07:00 UTC - refreshed for CORD-19 v27 2020-06-02.

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiODg5ODk5ZGEtYTViMy00ODAzLThiNzMtNWY2MjM5ZWUyNzU3IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiODg5ODk5ZGEtYTViMy00ODAzLThiNzMtNWY2MjM5ZWUyNzU3IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# This visualisation helps to explore the data behind the AI-powered literature review. The viewer can use the slicers (top-right) to filter the set of papers by several attributes.  Then you can scan the paper attributes in the table (tooltips for overflowed text) and decide if you want to dive in via the  Study Link - this will open the full paper in your browser.
# 
# As the source dataset columns are very diverse, a "matrix" visual has been used - the columns will change for each Question selected. This offers minimal control and some columns may need to be resized - the user can do that to suit by clicking and dragging the column header boundaries (as in Excel or similar).
# 
# A notebook is used to clean the data and prepare it for easy visualisation: [AI-Powered Literature Review - with submissions](https://www.kaggle.com/mikehoney/ai-powered-literature-review-with-submissions)
# 

# # AI-Powered Literature Review - Risk Factors
# The source dataset is the /Kaggle/target_tables files within the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/) dataset. This data has been curated by a large team of domain experts, based on ouput from ML authors attacking the various questions & topics. 
# 
# What's new:
# * 2020-06-10 08:00 UTC - refreshed for CORD-19 v29 2020-06-09.
# * 2020-06-04 03:50 UTC - refreshed for CORD-19 v28 2020-06-03.
# * 2020-06-03 07:00 UTC - refreshed for CORD-19 v27 2020-06-02.

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiN2VmMDI3MzYtNzQyZC00NGFhLWFhOGYtY2IwMzgzNGNkNzVmIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiN2VmMDI3MzYtNzQyZC00NGFhLWFhOGYtY2IwMzgzNGNkNzVmIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# This visualisation helps to explore the data behind the AI-powered literature review. The viewer can use the slicers (top-right) to filter the set of papers by several attributes.  The main table can also be sorted by the viewer - just click on any column heading (shift-click so sort multiple columns). Then you can scan the paper attributes in the table (tooltips for overflowed text) and decide if you want to dive in via the Study Link - this will open the full paper in your browser.
# 
# A notebook is used to clean the data and prepare it for easy visualisation: [AI-Powered Literature Review - with submissions](https://www.kaggle.com/mikehoney/ai-powered-literature-review-with-submissions)

# # AI-Powered Literature Review - CoronaWhy Team Task-TIES
# The [CoronaWhy](www.coronawhy.org) Team Task-TIES (Transmission, Incubation and Environmental Stability) submitted a [notebook](https://www.kaggle.com/crispyc/coronawhy-task-ties-patient-descriptions) to Round 2 of the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/).  This report was included in the submission, to present the selected papers to answer various questions in an interactive way.

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiMzU2YTk5ZjMtODU5My00ZjgyLWFmMWEtZDE4NzRjNzJhZTg1IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiMzU2YTk5ZjMtODU5My00ZjgyLWFmMWEtZDE4NzRjNzJhZTg1IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. The viewer can use the slicers (top-right) to filter the set of papers by several attributes.  The main table can also be sorted by the viewer - just click on any column heading (shift-click so sort multiple columns). Then you can scan the paper attributes in the table (tooltips for overflowed text) and decide if you want to dive in via the Study Link - this will open the full paper in your browser.
# 
# This data visualisation has multiple pages - use the page navigation control (bottom center) e.g. **< 1 of 3 >**. Pro-tip: click between the **<** and **>** for a menu of the pages. The first 2 pages are for Risk Factors, the 3nd page shows results for Key Scientific Questions.
# 
# 

# # AI-Powered Literature Review - EDA
# 
# The source dataset is the /Kaggle/target_tables files within the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/) dataset. This data has been curated by a large team of domain experts, based on ouput from ML authors attacking the various questions & topics. In this report, the input data is presented in some visuals to assist exploration and understanding of the data.
# 
# What's new:
# * 2020-08-13 02:30 UTC - refreshed for CORD-19 v42 2020-08-08 and refreshed submission notebooks
# * 2020-06-26 14:00 UTC : Added output from [CoronaWhy Team Task-TIES notebook](https://www.kaggle.com/crispyc/coronawhy-task-ties-patient-descriptions) and [COVID-19 Temperature and Humidity Summary Tables notebook](https://www.kaggle.com/javiersastre/covid-19-temperature-and-humidity-summary-tables). Copied pages: Risk Factors and Key Scientific Questions from their respective reports, with added Slicer for ML Author.
# * 2020-06-21 01:20 UTC : Refreshed from [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/) dataset v31 2020-06-18. Replaced box plots with violin plots. Improved extraction of Severe/Fatality components.

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiNWNkZWEzOWItYjE1Ni00NTI1LTljZmEtMWE5YzY2MDU4ZGI0IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiNWNkZWEzOWItYjE1Ni00NTI1LTljZmEtMWE5YzY2MDU4ZGI0IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a cell or row in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).
# 
# This data visualisation has multiple pages - use the page navigation control (bottom center) e.g. **< 1 of 2 >**. Pro-tip: click between the < and > for a menu of the pages. The first page is for **Risk Factors**, the 2nd page shows results for other **Key Scientific Questions**.
# 
# The visualisations help to explore the data behind the AI-powered Literature Review effort. The default view is "birds-eye" across all the papers included. The user can use the slicers (top-right) to filter the set of papers by several attributes.  The main table can also be sorted by the user - just click on any column heading (shift-click so sort multiple columns).
# 
# I do understand that the different ratios are often not directly comparable (e.g. OR vs RR), but you can use the slicers on the left to narrow down the types of ratios you want to compare.
# 
# There are slicers (filter) for **ML Author** and **Question**, so you can filter those charts (and every other tile) e.g. just for **Age**, **Heart Disease** etc.  Then you can scan the paper attributes in the table (tooltips for overflowed text) and decide if you want to dive in via the URL column - clicking those cells will open the full paper in your browser.
# 
# The fields for Severe/Fatality Metric and Value were extracted from the source column using [this notebook](https://www.kaggle.com/mikehoney/ai-powered-literature-review-with-submissions). Results may vary as the source data is manually created and updated frequently.  

# # CORD-19 Analysis with Sentence Embeddings
# 
# [David Mezzetti](https://www.kaggle.com/davidmezzetti) has built an index over the CORD-19 dataset to assist with analysis and data discovery. 
# 
# What's new:
# * 2020-05-03 08:00 UTC : Refreshed from CORD-19 Analysis with Sentence Embeddings v44 2020-05-02.
# * 2020-05-02 08:20 UTC : Refreshed from CORD-19 Analysis with Sentence Embeddings v42 2020-05-02.
# * 2020-04-26 07:40 UTC : Refreshed from CORD-19 Analysis with Sentence Embeddings v38 2020-04-24.
# 
# 

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiZjdjMTgzOWQtNzI1Ni00ODY1LWEyNzYtZDViNDY4MDI3OTM5IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiZjdjMTgzOWQtNzI1Ni00ODY1LWEyNzYtZDViNDY4MDI3OTM5IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a bar or row in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).
# 
# This visualisation helps to explore the data from the CORD-19 and Analysis datasets.
# 
# **Suggested method of use:**
# First use the slicers and visuals at the top of the page to narrow the list of Risk Factors, Questions and papers down to your topic of interest. Then click the column headers in the detailed table to sort the rows - shift-click to sort by multiple columns. To review the details table in full screen, use the Focus mode button in the top-right corner of the visual frame. 
# 
# The primary data source is the fulltext_processed and tables_processed files from the dataset: [CORD-19 Analysis with Sentence Embeddings](https://www.kaggle.com/davidmezzetti/cord-19-analysis-with-sentence-embeddings). 
# 
# The input data is presented in some quick visuals to assist exploration and understanding of the data.

# # CORD-19: Match Clinical Trials
# 
# [Daniel Wolffram](https://www.kaggle.com/danielwolffram) has identified clinical trial ids CORD-19 dataset (COVID-19 related papers only). These have been connected to a dataset prepared by [Ali Panahi](https://www.kaggle.com/panahi) detailing Clinical Trials.
# 
# What's new:
# * 2020-04-19 23:40 UTC : Added timeline visual on Trial Start and Completion dates.

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiOGEwYzUwMzctYzJhNS00MjcwLTgzYTktYjQ2ODZmOGM2ZjRkIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiOGEwYzUwMzctYzJhNS00MjcwLTgzYTktYjQ2ODZmOGM2ZjRkIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a bar or row in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).
# 
# **Suggested method of use:**
# First use the slicers and visuals at the top of the page to narrow the list of studies and papers down to your topic of interest. Then click the column headers in the detailed table to sort the rows - shift-click to sort by multiple columns. To review the details table in full screen, use the **Focus mode** button in the top-right corner of the visual frame.
# 
# This visualisation helps to explore the results from the [COVID-19 International Clinical Trials](https://www.kaggle.com/panahi/covid-19-international-clinical-trials) dataset. The resuls of the notebook: [CORD-19: Match Clinical Trials](#CORD-19-Match-Clinical-Trials) are used to connect the Clinical Trial data to the CORD-19 data.
# 
# The secondary data source is the metadata file and associated json files from the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/).  
# 
# > The input data is presented in some quick visuals to assist exploration and understanding of the data.

# # CoronaWhy.org - Literature Review
# 
# The [CoronaWhy](coronawhy.org) team is working on a Literature Review tool. This report was built as a "Proof of Concept" to help spark ideas and review data. 
# 
# What's new:
# * 2020-08-02 12:00 UTC : v1.8 improved the modeling of the Mentions of Gender and Age, so they now work independently of the Search
# * 2020-08-02 12:00 UTC : v1.7 refreshed from CORD-19 v39 2020-07-27, including Named Entity Recognition (SciSpacy)
# * 2020-07-29 09:00 UTC : v1.6 added Sample Size to the table (right)
# * 2020-07-23 14:00 UTC : v1.5 refreshed input data for Altmetrics score, and for Literature Reviews. The "Mentioned in Literature Reviews" tile now shows the source "ML Author", and they are also shown in the table of papers
# * 2020-07-21 12:15 UTC : v1.4 added the altmetrics dataset, with the score showing as a new slicer (left-middle) and also in the table of papers.
# * 2020-07-20 01:00 UTC : v1.3 expanded the report dataset to include CORD-19 papers back to 2018, so there are now 12k+ papers included (were 5k).

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiMDMyMzFiOTMtZDcyMi00MmI2LTljMjItYWVhMWYxYjU3ZjA2IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiMDMyMzFiOTMtZDcyMi00MmI2LTljMjItYWVhMWYxYjU3ZjA2IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a bar or row in almost any visual to cross-filter the other visuals on the page. 
# 
# **Input data:**
# 
# This report helps to explore the data from the CORD-19 and CoronaWhy datasets. The primary data source is the [CoronaWhy NER CORD-19 dataset](https://www.kaggle.com/mikehoney/coronawhy-plus), created by the [Coronawhy](http://www.coronawhy.org/) data team. This is the result of a Named Entity Recognition (NER) analysis, run across all the papers in the CORD-19 v9 datatset that offer full text data. 
# 
# It also uses the metadata file and associated json files from the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/). This is joined to the metadata file using the column: "cord\_uid". This adds paper attributes such as "Journal" and Publication Date". To keep the dataset size manageable while we iterate, the papers are filtered on Publication Date being 2018 or later.  
# 
# Study Design is sourced from David Mezzetti's Study Design categorisations from [this notebook]( https://www.kaggle.com/davidmezzetti/cord-19-study-metadata-export).
# 
# The map is based on the location of author affiliations, provided by CoronaWhy (MongoDB).
# 
# The "Included in Literature Review" visual highlights papers that have been included in the "AI Powered-Literature Review", which is explored in detail in other reports above. The dataset used here is all the "Kaggle Community" and submissions by ML Authors, as included in the EDA report above.  [This notebook](https://www.kaggle.com/mikehoney/ai-powered-literature-review-with-submissions) is used to collate that dataset.
# 
# 
# **Suggested method of use:**
# 
# First use the Search box, slicers and other tiles (at the top and left of the page) to narrow the table of papers (right) down to your topic of interest. Click the link button on each row to open the paper via doi.org. Hover over a row in the table to see a pop-up table of the most frequent Named Entity Values in that paper (dynamically filtered).
# 
# To review the details table in full screen, use the **Focus mode** button in the top-right corner of the visual frame. You can click the column headers in the detailed table to sort the rows - shift-click to sort by multiple columns. 
# 
# Each tile has a tooltip that appears when you hover over it - look for the ? icons. These explain the source and give hints on how to use each tile.

# # CoronaWhy.org - Named Entity Recognition
# 
# The [CoronaWhy](coronawhy.org) team has built Named Entity Recognition across the entire corpus of CORD-19 papers with full text.
# 
# What's new:
# * 2020-04-28 13:00 UTC : Refreshed from CORD-19 dataset v9 2020-04-24.  
# * 2020-04-06 12:15 UTC : Refreshed from CoronaWhy dataset v30 2020-04-05. 

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiMGExNTY3ZjEtMTA3MC00NDYyLTg3YjAtMzZjYTZlMmQ3Mzk3IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiMGExNTY3ZjEtMTA3MC00NDYyLTg3YjAtMzZjYTZlMmQ3Mzk3IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a bar or row in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).
# 
# **Suggested method of use:**
# First use the slicers and visuals at the top of the page to narrow the list of Named Entities, Values and papers down to your topic of interest. Then click the column headers in the detailed table to sort the rows - shift-click to sort by multiple columns. To review the details table in full screen, use the Focus mode button in the top-right corner of the visual frame. Hover over a row in the table to see a pop-up table of the most frequent Named Entity Values in that paper (dynamically filtered).
# 
# This visualisation helps to explore the data from the CORD-19 and CoronaWhy datasets. The primary data source is the **text** file from the dataset: [Coronawhy](http://datasets.coronawhy.org/). This is the result of a Named Entity Recognition (NER) analysis, run across all the papers in the CORD-19 datatset that offer full text data. They are appended together as a Natural Entities table.  
# 
# It also uses the metadata file and associated json files from the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/). This is joined to the metadata file using the column: "cord\_uid". This adds paper attributes such as "Journal" and Publication Date".  
# 
# The input data is presented in some quick visuals to assist exploration and understanding of the data.

# # CoronaWhy.org - Task: Risk Factors
# 
# The Task-Risk team within the [CoronaWhy](http://www.coronawhy.org) community have started producing some sample results on: understanding COVID-19 risk factors. Please note these are shared for review by that team as they refine their ML models.
# 
# What's new:
# * 2020-05-05 06:50 UTC : Refreshed from datasets.coronawhy.org, v1.
# * 2020-04-17 15:50 UTC : Added word cloud page.
# * 2020-04-15 23:50 UTC : Added 3rd page - Risk Factor Analysis, then a page specific to each Risk Factor (e.g. Age). Each Risk Factor page shows visuals on papers and keyword results.
# 

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiY2E5YjFkZjItN2Q2ZS00MGI5LWFiMWQtZmY0OWRiZTlkNDVmIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiY2E5YjFkZjItN2Q2ZS00MGI5LWFiMWQtZmY0OWRiZTlkNDVmIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# This data visualisation has multiple pages - use the page navigation control (bottom center) e.g. **< 1 of 9 >**. Pro-tip: click between the **<** and **>** for a menu of the pages. The first page is for detailed analysis of the results, the later pages are summary statistics to help explain the task-risk methods.
# 
# Like all Power BI reports, the visuals are highly interactive. Select a bar or row in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).
# 
# **Suggested method of use:**
# First use the slicers and visuals at the top of the page to narrow the list of papers down to your topic of interest. Then click the column headers in the central table to sort the rows - shift-click to sort by multiple columns. Then select a paper of interest from the central table - that will filter the details table below. To review a table in full screen, use the **Focus mode** button in the top-right corner of the visual frame.
# 
# This visualisation helps to explore the results from the CoronaWhy Task-Risk team datasets.  [More info in this Notebook](https://www.kaggle.com/arturkiulian/coronawhy-org-task-risk-factors). The key attributes focused on are the Risk Factor and Keywords/Ngrams used to search the papers for that Risk Factor.  
# 
# The secondary data source is the metadata file and associated json files from the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/).  
# 
# > The input data is presented in some quick visuals to assist exploration and understanding of the data.

# # CoronaWhy.org - Task: Transmission & Incubation
# 
# The Task-ties team within the [CoronaWhy](http://www.coronawhy.org) community have started producing some sample results on: transmission, incubation and environment stability. Please note these are shared for review by that team as they refine their ML models.
# 
# What's new:
# * 2020-06-02 00:50 UTC : Added page for Knowledge Graph using [ZoomCharts](https://www.zoomcharts.com/) Graph visual.
# * 2020-05-31 10:20 UTC : Added page for Knowledge Graph using [ZoomCharts](https://www.zoomcharts.com/) Network visual.
# * 2020-05-06 08:40 UTC : Replaced **score** with **score (normalized %)**, to allow comparisons across **source** methods.
# * 2020-05-05 10:30 UTC : Refreshed from datasets.coronawhy.org, v1.
# * 2020-04-11 04:50 UTC : On Search Engine page: added bar chart of Search Engine Results by disease.
# 

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiOWYwM2Y0OTgtZGE0YS00YjM3LTkwZmYtZTM1NWE5NjJmY2JjIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiOWYwM2Y0OTgtZGE0YS00YjM3LTkwZmYtZTM1NWE5NjJmY2JjIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a bar or row in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).
# 
# The Knowledge Graph page helps explore the results from this [Task-Ties team notebook](https://colab.research.google.com/drive/1pYVWxG5hXZfkolWe9Q_CZg2hRIfg2Q9u?usp=sharing).
# 
# The Search Results page helps to explore the data from the CoronaWhy Task-Ties team datasets. For more info:  [CoronaWhy.org - Task: Transmission & Incubation](https://www.kaggle.com/crispyc/coronawhy-org-task-transmission-incubation) ).
# 
# The secondary data source is the metadata file and associated json files from the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/). 
# 
# > The input data is presented in some quick visuals to assist exploration and understanding of the data.

# # COVID-19 Thematic tagging with Regular Expressions
# 
# A visualisation of the question tagging results.
# 
# What's new:
# * 2020-04-25 05:00 UTC : Refreshed from CORD-19 dataset v9 2020-04-24.  
# * 2020-04-19 11:00 UTC : Refreshed from CORD-19 dataset v8 2020-04-17.  
# 

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiMWE1MjUyYTAtNzBkMy00NjRiLTg5MTEtNDM3Mzk2OTJjMzgyIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=450)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiMWE1MjUyYTAtNzBkMy00NjRiLTg5MTEtNDM3Mzk2OTJjMzgyIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a bar or row in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).
# 
# This visualisation helps to explore the results from the notebook: [COVID-19 Thematic tagging with Regular Expressions](https://www.kaggle.com/ajrwhite/covid-19-thematic-tagging-with-regular-expressions/) by [Andy White](https://www.kaggle.com/ajrwhite). The extended tagging results from notebook: [COVID-19 Transmission and incubation](https://www.kaggle.com/ajrwhite/covid-19-transmission-and-incubation) are also included.
# 
# The data from the 1st notebook's output **thematic_tagging_output_full.csv** is combined with **augmented_metadata_full.csv** from the 2nd notebooks and shredded into "tags", within "tag categories".  "tag categories" are also collected into "questions", based on the comments and tables presented in those notebooks. These are presented in the Power BI slicers and visuals on the middle and right side of the page, and also in the last 2 columns in the bottom table.  
# 
# The **Tag Count** attribute counts cells from the notebook output in columns named "tag...", that contain "True".
# 
# The other primary data source is the metadata.csv file and associated json files from the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/).  The connection to the notebook output (described above) uses columns: "cord_uid", "sha". 
# 
# Note there are multple pages included. Use the page navigation control at bottom centre, e.g. **< 1 of 2 >**
# 
# The 2nd page uses a Q&A visual at (top right). This is an preview (beta) automated AI feature that understands the attributes of the metadata including the contents of the rows. At present it is "untrained" but it can be refined and improved. Type in your question and it will generate a result instantly. It's output is constrained by the other visuals on the page e.g. Slicers.  Contact me if you are interested in exploring the results from this visual. 
# 
# ![thematic%20tagging%20with%20QnA.PNG](attachment:thematic%20tagging%20with%20QnA.PNG)

# 

# # CORD-19 metadata with CoronaWhy attributes
# **Base Power BI Report for exploring data, basis for new reports**
# 
# What's new:
# 
# * 2020-08-13 02:30 UTC - refreshed for CORD-19 v42 2020-08-08
# 

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiMzczODQ1MTMtMWNlYy00YzI5LWI2OGItZDFhZmQxNzVjYmM1IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=450)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiMzczODQ1MTMtMWNlYy00YzI5LWI2OGItZDFhZmQxNzVjYmM1IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a bar or row in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).
# 
# This visualisation helps to explore the metadata data from the CORD-19 and CoronaWhy datasets.
# 
# The primary data source is the metadata file and associated json files from the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/).    
# 
# The input data is presented in some quick visuals to assist exploration and understanding of the data.
# 
# This file is ideal as a base for creating a more specific analysis based on results from a data science notebook/project.
# 

# # World map of CORD-19 affiliations
# 
# Explore the locations of authors affiliated with CORD-19 papers. Several map styles are presented, along with the list of papers.

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiMmU2MjNmYTItNzk2MC00NWEzLWIxOGUtNzAxMWEyZjJiZTMxIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiMmU2MjNmYTItNzk2MC00NWEzLWIxOGUtNzAxMWEyZjJiZTMxIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a point or cell in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual).  The maps can be zoomed in and out and there are polygon and lasso selection tools.
# 
# This visualisation helps to explore the metadata data from the CORD-19 and CoronaWhy datasets.
# 
# The primary data source is the metadata file and associated json files from the [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/).    
# 
# It also uses the enhanced metadata file from the dataset: [Coronawhy](https://coronawhy.org). This is joined to the metadata file using the column: "cord_uid". This adds attributes for the location of each Author's Institution (where that can be derived) including the latitude and longitude.  
# 
# This report inlcudes multiple pages, showcasing various map styles and functionality. Use the controls at the bottom to navigate through the pages.

# # World map of CoronaWhy Team
# Explore the locations and skills of CoronaWhy Team members.

# In[ ]:


from IPython.display import IFrame
IFrame('https://app.powerbi.com/view?r=eyJrIjoiOTMzNjliNDQtM2M1MC00MjM0LThhYjctMjllMGM0MTZhYmJlIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D', width="100%", height=500)


# Here's the link to view it in Full Screen:
# 
# https://app.powerbi.com/view?r=eyJrIjoiOTMzNjliNDQtM2M1MC00MjM0LThhYjctMjllMGM0MTZhYmJlIiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D
# 
# Like all Power BI reports, the visuals are highly interactive. Select a point or cell in almost any visual to cross-filter the other visuals on the page. Ctrl-click to multi-select (across visuals and/or within a visual). The maps can be zoomed in and out and there are polygon and lasso selection tools.
# 
# This visualisation helps to explore the CoronaWhy Team.  Only team members who provided their location are included.  No personal or identifable information is included.
