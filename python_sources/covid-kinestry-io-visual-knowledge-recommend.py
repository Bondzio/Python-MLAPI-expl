#!/usr/bin/env python
# coding: utf-8

# # [covid.kinestry.io](https://covid.kinestry.io/) - A Visual Knowledge Recommendation
# 
# .

# In[ ]:


from IPython.display import IFrame
IFrame(src='https://covid.kinestry.io', width=900, height=600)


# 
# 
# As coronavirus (COVID-19) continues to spread around the world and as of this writing, there are almost 8 million confirmed cases with about 430,000 total deaths. COVID-19 has affected people in different ways. There have been numerous reports of people having various symptoms, from mild to severe. The variety of symptoms makes it difficult for healthcare professionals to stay up-to-date with the most relevant information about prevention, diagnosis, treatment, recovery, and potential cures for COVID-19.
# 
# To help provide a clear understanding of the epidemiological landscape during this pandemic, we focused on the critical topic of "What has been published about medical care?" with 16 [specific questions](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks?taskId=572).
# 
# 1) To cover as many relevant respected medical resources as possible, we didn't limit the study in the given CORD-19 dataset. We investigated multiple data resources and integrated the CDC's latest literature collections with the CORD-19 dataset. We cleaned and analyzed the integrated dataset as the data foundation for our study.
# 
# 2) To gain quick data insights, we constructed a Keywords-Article Matrix as an overview approach to get a profile and a preliminary evaluation of the dataset. 
# 
# 3) To extract valuable information from this dataset, we investigated various NLP methods and narrowed the focus to BioBERT, the Bidirectional Encoder Representations from Transformers for Biomedical Text Mining. We, then, built our  BioBERT encoder-decoder database and a Question-Answer model to get the answers for 16 specific questions and further related literature. 
# 
# 4) To help users quickly and efficiently find essential information, we applied professional visual design principles and techniques to structure the information in a way that is intuitive to most users instead of a traditional search engine or a linear text. ([link to website](https://covid.kinestry.io/))
# 
# We are honored to participate in the competition and to join forces with a global community of devoted people helping humanity come through this terrible crisis. We are a team of passionate and talented Kinestry alumni and friends that you may learn more about at [the About Us page](https://covid.kinestry.io/about-us.html). 
# 
# Thank you all for your hard work, time, commitment, and compassion.
# 
# 
# 
# ## Data Preprocessing
# 
# The CORD-19 dataset was cleaned by removing records that did not contain any abstracts and URLs, as well as removing non-English records. Another dataset containing more recent COVID-19 articles maintained by the CDC (Center for Disease Control), has unnamed columns and some skewed data. We corrected that. 
# 
# We then used the SpaCy language detection [module](https://www.cdc.gov/library/researchguides/2019novelcoronavirus/researcharticles.html) combined with a SciSpaCy model trained on medical [data](https://allenai.github.io/scispacy/) to create a language detection score on the title column. Only records with non-zero English detection scores were kept. Despite the care and effort taken in cleaning this data, it was found that both datasets, (particularly the CDC dataset) were still full of erroneous data containing nonsense text, data that was shifted over by a column, missing abstracts, etc... However, with the level of data cleaning applied here, it was clean enough to produce useful results when we ran the dataset through our model.
# 
# Since the Coronavirus was discovered at the end of the year 2019, we focused on the topic to analyze the articles published after September of 2019. 
# 
# The code for the data preprocessing can be found [here](https://www.kaggle.com/gregpawin/covid-19-data-cleaning/).
# 
# 
# 
# ## Keywords-Article Matrix Model
# 
# We created a Keywords-Article Matrix model to select the dataset associated with COVID-19. The purpose of this model was to reduce the amount of data needed to train the BioBert model. Prior to running this model, additional cleaning of the dataset was needed in order to remove special characters and transpose the text to the lowercase form. Thus, this allowed the model to catch all of the keywords.
# 
# This model can reduce the size of the dataset to fit into the BioBert model. While the Biobert model is good at understanding and calculating similarities between text, it requires a lot of time to train. This is why we attempted to reduce the size of the dataset eligible for consideration. 
# 
# The code for the Keywords-Article Matrix Model can be found [here](https://www.kaggle.com/kinestry/covid-19-keywords-article-matrix-kinestry-ipynb/edit/run/32084950).
# 
# 
# 
# ## Integrated BioBERT Model
# 
# We integrated the Keywords-Article Matrix model and the state-of-art pre-trained domain-specific [BioBERT](https://arxiv.org/ftp/arxiv/papers/1901/1901.08746.pdf) (Biomedical Bidirectional Encoder Representations for Transformers) to build a Question and Answer model for biomedical corpora effectively and comprehensively understood by the machines in the medical text mining tasks. 
# 
# The tasks, each of the sub-questions, are involved heavily with the technical corpus in the medical and healthcare domains. Therefore, this integrated BioBERT model appeared to be the most suitable for the tasks. We can fetch and exhibit the most helpful and useful articles for each of these questions and related articles.
# 
# The code for the Integrated BioBERT Model can be found [here](https://drive.google.com/file/d/1OkQmu0tAItrWQ0WLlcWd6IUBH8q4KdWT/view?usp=sharing).  
# 
# 
# 
# ## Product Design and Development
# 
# Before product design and development, we conducted user research and discovered that many need to quickly learn information without knowing where to start, and a search engine is not a very effective solution. This is the dilemma we faced in understanding COVID-19 better.
# 
# Therefore, we created a place for users to freely browse the content about COVID-19 under the guidance of our 16 original questions.
# 
# We utilized the knowledge graph to demonstrate better our understanding of the disease at-large.
# 
# Please visit our website https://covid.kinestry.io, or the interactive version https://covid.kinestry.io/beta.
# 
# 
# ## Pros and Cons
# 
# 
# ### Pros
# 
# * We built a Knowledge Graph website to share insights from large amounts of data in an easy to navigate manner.
# * We had a medical expert double check our training results because unsupervised learning makes it challenging to verify the results, and to improve the accuracy of the integrated model.
# * The combined CORD-19 dataset with updated articles published by CDC are more comprehensive, relevant and respected medical resources.
# * The optimized timescale helps the model to focus on the healthcare topic during COVID-19.
# * Established keyword-article matrix model optimizes data input from the large data set.
# * The latest biomedical NLP model BioBERT model is applied to extract valuable information from the biomedical data set.
# 
# 
# ### Cons
# 
# * Removal of non-English records could lose some insight (but this is only a small part of the entire dataset).
