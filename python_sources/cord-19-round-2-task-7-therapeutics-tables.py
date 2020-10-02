#!/usr/bin/env python
# coding: utf-8

# # Extracting highly specific information on therapeutic studies and building a manually curated benchmark dataset

# # Summary
# 
# We developed a pipeline and a set of approaches to create the summary tables as specified in task 7 using the [CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) last updated on June 09. We identified 209 articles relevant to the question, '*What is the best method to combat the hypercoagulable state seen in COVID-19_.csv*', and 1,352 articles relevant to the question, '*What is the efficacy of novel therapeutics being tested currently_.csv*'. As the the [CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) still has many duplicated records, we excluded the duplicated ones and some irrelevant articles. At the end, we identified 174 articles (after excluding 2 irrelevant and 33 duplicated articles) and 1,095 articles (after excluding 52 irrelevant and 205 duplicated articles) for the two questions respectively, and extracted information from these articles to fill the summary tables following their specific formats. The summary tables are listed as follows, and can be downloaded from the following links:
# 
# - [Summary table of '*What is the best method to combat the hypercoagulable state seen in COVID-19_.csv*'](https://www.kaggle.com/gdsttian/cord19round2task7?select=summary_table_hypercoagulability.csv)
# - [Summary table of '*What is the efficacy of novel therapeutics being tested currently_.csv*'](https://www.kaggle.com/gdsttian/cord19round2task7?select=summary_table_therapeutic_efficacy.csv)
# 
# We call the first table, hypercoagulable table, and the second table, therapeutics table.

# In[ ]:


import pandas as pd

table_hypercoagulability = pd.read_csv(f"/kaggle/input/cord19round2task7/summary_table_hypercoagulability.csv", na_filter= False)
print(f"Table 1: What is the best method to combat the hypercoagulable state seen in COVID-19_.csv")
print(f"{'Number of entries in the table:':20}{table_hypercoagulability.shape[0]:5}")
table_hypercoagulability.head()


# In[ ]:


table_therapeuticefficacy = pd.read_csv(f"/kaggle/input/cord19round2task7/summary_table_therapeutic_efficacy.csv", na_filter= False)
print(f"Table 2: What is the efficacy of novel therapeutics being tested currently_.csv")
print(f"{'Number of entries in the table:':20}{table_therapeuticefficacy.shape[0]:5}")
table_therapeuticefficacy.head()


# We compared our summary tables with those curated by experts provided on Kaggle website. We retrieved 9 out of the 19 articles from the hypercoagulable table and 19 out of the 34 articles from the therapeutics table curated by experts. For the articles not retrieved in our results, we identified the reasons, which are listed in the following table. 
# 
# 
# |Category|Table of Combating Hypercoagulable State|Table of Novel Therapeutics Efficacy|
# |:-|-|-|
# |Total articles in the sample table curated by experts|19|34|
# |Articles in our final result|9|19|
# |Articles not in our final result|10|15|
# |Articles without an abstract|5|5|
# |Articles without relevant keywords in title and abstract|0|6|
# |Articles without chemicals tagged|5|2|
# |Articles not in the CORD-19 dataset|0|2|

# # Introduction
# 
# The COVID-19 pandemic has caused nearly 8 million confirmed infected patients and more than 430 thousand deathes worldwide. In response to the pandemic, the [CORD-19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) including scholarly articles related to COVID-19 was created for global research community to generate helpful insight for the ongoing combat against this infectious disease using state-of-the-art text mining, NLP and other AI technologies. The [CORD-19 competition](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) was organized by Kaggle as a call for actions to develop tools and information for answering scientific questions with high priority. [Round \#2](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/discussion/150921) of the [CORD-19 challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) asked participants to create summary tables with specific structures derived by expert curators.
# 
# To tackle the challenges, we have organized a collaborative team including scientists from [Insilicom Inc.](https://insilicom.com/) and the department of statistics of Florida State University. Insilicom specializes in providing innovative technologies to help scientists effectively use Big Data to accelerate their research and development efforts. It recently developed the [Biomedical Knowledge Discovery Engine (BioKDE)](https://biokde.com/), a deep-learning powered search engine for biomedical literature. 
# 
# Our information extraction pipeline consists of the following components. 
# First, based on the [CORD-19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge), we developed a dataset which is clean and annotated with different entities such as genes, disease, chemicals, etc. using [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/index.html), [BeFree](http://ibi.imim.es/befree/) and [scispacy](https://allenai.github.io/scispacy/) annotated entities; Second, we used extended keywords to query articles relevant to a paticular topic; Third, we used synonyms to further increase the coverage of the retrieved relevant articles; Fourth, we used regular expressions to extract specific information for filling certain columns of the tables; Fifth, we parsed the relevant sentences to obtain typed dependency graphs, which were used to compute the shortest pathes between relevant keywords, such as chemical names and COVID-19 related terms. The shortest pathes are used to further curate the relevant sentences. They will also be used in the future for building predictive models for the corresponding information extraction tasks; Finally, we have manually verified the summary tables before submitting to obtain a manually curated dataset, which can be used in future studies as benchmark data. These manually curated data can also be used to build machine learning models. 
# 
# Task 7 of the challenge is to "[create summary tables that address therapeutics, interventions, and clinical studies](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks?taskId=887)". This task targets to answer two questions:
# 
# 1. What is the best method to combat the hypercoagulable state seen in COVID-19?
# 2. What is the efficacy of novel therapeutics being tested currently? 
# 
# by creating two summary tables:
# 
# 1. What is the best method to combat the hypercoagulable state seen in COVID-19_.csv
# 2. What is the efficacy of novel therapeutics being tested currently_.csv
# 
# This notebook was organized in the following structure:
# 
# 1. Developing a Cleaned Dataset with Annotated Entity Types
#    - Processing the [CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)
#    - Entity Annotation
#    - Aggregation and Indexing of CORD-19 Articles
# 2. Creating the Summary Tables
#    - Retrieving COVID-19 Related Articles
#    - Keywords for Retrieving Articles Related to the Summary Table
#    - Extracting relevant information
#    - Generating the Summary Tables

# # Developing a Cleaned Dataset with Annotated Entity Types
# 
# ## Processing the CORD-19 Dataset
# 
# To process the [CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge), we verified the ids of doi, pmid and pmcid of each article and organized all the articles in a consistent format. For articles with pmids and/or pmcids, the pmids and pmcids will be used for getting entities annotations from [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/index.html). Each article was stored in a JSON file after the above pre-processing. The codes for extracting ids and article pre-processing can be found as listed:
# - [code for getting ids](https://www.kaggle.com/gdsttian/preprocess-get-ids)
# - [code for article process](https://www.kaggle.com/gdsttian/preprocess-cord-data).

# In[ ]:


# !python preprocess_get_ids.py
# !python preprocess_cord_data.py


# ## Entity Annotation
# 
# Entity annotation is very helpful for extracting relevant information. [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/) provides annotations of biomedical concepts in PubMed abstracts and PMC full-text articles. Using the [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/) API, we acquired annotations for the articles in the [CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) when they are available. For those without pre-calculated annotations, we used the [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/) web interface to retrieve the annotations. All [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/) annotations were then parsed and organized in a consistent format for each article. The entities annotated by [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/) include:
# 
# - Genes
# - Diseases
# - Chemicals
# - Species
# - Mutation
# - Cellline
# 
# Beside [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/) annotations, we also used [BeFree](http://ibi.imim.es/befree/) and [scispacy](https://allenai.github.io/scispacy/) to annotate additional entities. [BeFree](http://ibi.imim.es/befree/) annotates entities of **genes** and **diseases** (a python package needs to be installed from the [BeFree repo](https://bitbucket.org/nmonath/befree/src/master/)). In order to use [BeFree](http://ibi.imim.es/befree/) in our pipeline, we modified a function of the package, which can be found [here](https://www.kaggle.com/gdsttian/befree-ner-covid19).
# 
# [scispacy](https://allenai.github.io/scispacy/) includes different models for biomedical concept annotation, among which two were used in our pipeline. The two models and the entities annotated by each model are listed as follows:
# 
# - en_ner_craft_md: genes, taxonomies, sequence ontologies, chemicals, gene ontologies and cellline
# - en_ner_jnlpba_md: DNA, cell type, cellline, RNA and protein
# 
# All annotations were combined into a final set of annotations. When annotations by different tools overlap with each other, we selected the annotations with the largest span. When different tools annotate entities at the same span, we gave priority to [PubTator](https://www.ncbi.nlm.nih.gov/research/pubtator/).
# 
# All codes for annotations are available through the following links:
# 
# - [code for acquiring existing PubTator annotations](https://www.kaggle.com/gdsttian/entities-get-pubtator-annotation)
# - [code for posting titles abd abstracts to PubTator for annotations](https://www.kaggle.com/gdsttian/entities-post-tiabs-to-pubtator)
# - [code for retrieving completed title and abstract annotations from PubTator](https://www.kaggle.com/gdsttian/entities-retrieve-tiabs-from-pubtator)
# - [code for parsing PubTator annotations](https://www.kaggle.com/gdsttian/entities-process-pubtator-annotation)
# - [code for adding BeFree and scispacy annotations](https://www.kaggle.com/gdsttian/entities-additional-annotation)

# In[ ]:


# !pip install git+https://bitbucket.org/nmonath/befree.git
# !python entities_get_pubtator_annotation.py
# !python entities_post_tiabs_to_pubtator.py
# !python entities_retrieve_tiabs_from_pubtator.py
# !python entities_process_pubtator_annotation.py
# !python entities_additional_annotation.py


# ## Aggregation and Indexing of CORD-19 Articles
# 
# With all the CORD-19 articles processed and the annotations combined, they were aggregated into a single JSON file. For each article, the entities identified were summarized and relations between entities were extracted if they co-occur in the same sentence. 
# 
# Query of relevant articles plays an important role in creating the summary tables. In order to retrieve target articles, we created indices of articles by publication time and keywords in titles and abstracts. We used [spaCy](https://spacy.io/) for tokenization of titles and abstracts. Articles returned from the query were ranked by the counts of the keywords occuring in the articles.
# 
# All codes for data aggregation and indexing were given as follows:
# 
# - [code for data aggregation](https://www.kaggle.com/gdsttian/data-aggregation)
# - [code for entities summary and relation building](https://www.kaggle.com/gdsttian/data-nodes-relations)
# - [code for index by time](https://www.kaggle.com/gdsttian/data-indexing-time)
# - [code for index by words](https://www.kaggle.com/gdsttian/data-indexing-word)

# In[ ]:


# !python data_aggregation.py
# !python data_nodes_relations.py
# !python data_indexing_time.py
# !python data_indexing_word.py


# # Creating the Summary Tables
# 
# After the clean annotated dataset was created, we can start the query and information extraction process.
# 
# ## Configuration and Import of Python Packages and Tools
# 
# At the beginning, we define the data pathes and all the data needed during the process.

# In[ ]:


# data pathes
data_path = '/kaggle/input/cord-19-data-with-tagged-named-entities/data' # folder for system data
json_path = '/kaggle/input/cord-19-data-with-tagged-named-entities/data/json_files/json_files' # path of final json files
mapping_pnid = 'mapping_corduid2nid.json' # dictionary mapping cord_uid to numeric id for each paper

index_year = 'index_time_year.json' # dictionary of list of papers for each publish year
index_title = 'index_word_title.json' # dictionary of list of papers for each word in title
index_abstract = 'index_word_abstract.json' # dictionary of list of papers for each word in abstract
word_counts = 'paper_word_counts.json' # word counts by paper
index_table = 'index_word_table.json'
paper_tables = 'paper_tables.json'

entity_lists = 'entity_lists.json' # entity checking lists including disease list, blacklist etc.
entity_nodes = 'entity_nodes.json' # entities dictionary
entity_relations = 'entity_relations.json' # entity relation dictionary

mapping_sents = 'mapping_sents2nid.json' # mapping sent id to numeric id
index_sents = 'index_word_sents.json' # mapping word to a list of numeric sent id
sentences = 'sentences.json' # dictionary of all sentences with unique id


# We import the python packages and the tools we developed for the process. These tools can be used for data loading, article query and display. Codes of the tools can be accessed by the following links:
# 
# - [code for utility tools](https://www.kaggle.com/gdsttian/utils)
# - [code for search tools](https://www.kaggle.com/gdsttian/mining-search-tool)

# In[ ]:


# packages
from utils import *
from mining_search_tool import *
import os
csv_path = 'csv'
os.makedirs(csv_path, exist_ok=True)


# ## Loading the Data
# 

# In[ ]:


papers = SearchPapers(data_path, json_path, mapping_pnid, index_year,
                      index_title, index_abstract, word_counts, index_table, paper_tables,
                      entity_lists, entity_nodes, entity_relations, index_sents, mapping_sents, sentences)


# ## Retrieving COVID-19 Related Articles
# 
# Information for the summary tables need to be extracted from the articles relevant to COVID-19. These articles were queried using a list of keywords. We defined the list of extended keywords based on those used by the [PMC COVID-19 Initiative](https://www.ncbi.nlm.nih.gov/pmc/about/covid-19/) and manual reading of some relevant articles.
# 
# As most of the articles associated with COVID-19 were published in 2020, we limited the publication time to year 2020.
# 
# There are more than 35 thousand articles identified as relevant to COVID-19 in the [CORD-19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) updated on June 9.
# 
# One of the articles was displayed as follows.

# In[ ]:


covid19_names = """covid-19, covid19, covid, sars-cov-2, sars-cov2, sarscov2,
                   novel coronavirus, 2019-ncov, 2019ncov, wuhan coronavirus
                """


# In[ ]:


papers_covid19 = papers.search_papers(covid19_names, section = None, publish_year = '2020')
print(f"{'Total papers relevant to COVID-19:':20}{len(papers_covid19):6}")


# In[ ]:


papers.display_papers(papers_covid19[:1])


# ## Keywords for Retrieving Articles Related to the Summary Table
# 
# Based on our preliminary research, we defined the lists of keywords for querying articles for the two summary tables as follows.
# 
# The keywords for querying articles for the summary table of '*What is the best method to combat the hypercoagulable state seen in COVID-19_.csv*' include the synonyms and phrases related to coagulation. We assume that any articles containing anyone of the keywords in title or abstract are relevant to the summary table.

# In[ ]:


query_coagulation = """coagulation, anticoagulant, decoagulant, anticoagulation,
                       hypercoagulable, hypercoagulability, coagulopathy, vasoconstrictive,
                       thromboprophylaxis, thrombosis, thrombotic, thromboembolism, thromboprophylaxis
                    """


# The keywords for querying articles for the summary table, '*What is the efficacy of novel therapeutics being tested currently_.csv*', include two lists: a list of synonyms and phrases related to therapeutics and a list of synonyms and phrases related to efficacy. We assume that any articles containing anyone of the therapeutic keywords and anyone of the efficacy keywords in title or abstract are relevant to the summary table.

# In[ ]:


query_therapy = """therapy, therapeutic, therapeutics,inhibitor,
                   inhibitors, medicine, medication, drug, drugs,
                   treat, treatment, pharmaceutical, pharmaceutic
                """


# In[ ]:


query_effect = """effect, effects, efficacy, effective, effectiveness, benifit, benifits
               """


# ## Extracting relevant information 
# 
# The information we extracted for each table includes study type, therapeutic methods, sample size, severity, general outcome, primary endpoint and clinical improvement in addition to other information that can be extracted from the metadata of the articles such as article IDs, publication date, journal etc..
# 
# ### Study Types
# 
# The study types specified in the [CORD-19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) includes systematic review and meta-analysis, prospective observational study, retrospective observational study, case series, expert review, editorial, ecological regression, and simulation. As there is no information of study type in the metadata of the articles, we classified the articles into only four types: systematic review, retrospective study, simulation and other studies. For each study type, we defined a list of keywords, whose presence in the abstracts determines the corresponding article type. When an article contains keywords of more than one study type, its study type was decided in the priority order of systematic review, retrospective study, simulation and other studies.
# 
# The lists of keywords for study type classification are given below. 

# In[ ]:


sys_review = ['systematic review', 'meta-analysis',
              'search: PubMed, PMC, Medline, Embase, Google Scholar, UpToDate, Web of Science',
              'searched: PubMed, PMC, Medline, Embase, Google Scholar, UpToDate, Web of Science',
              'in: PubMed, PMC, Medline, Embase, Google Scholar, UpToDate, Web of Science']
retro_study = ['record review','retrospective', 'observational cohort', 'scoping review']
simulation = ['modelling','model','molecular docking','modeling','immunoinformatics', 'simulation', 'in silico', 'in vitro']


# In[ ]:


def get_papers_by_study_type(study_type_list):
    papers_for_the_type = set()
    for phrase in study_type_list:
        papers_by_phrase = papers.search_papers(phrase, section = 'abs', publish_year = '2020')
        papers_for_the_type = papers_for_the_type.union(set(papers_by_phrase))
    return papers_for_the_type

papers_review = get_papers_by_study_type(sys_review).intersection(set(papers_covid19))
print(f"{'Systematic Review: ':25}{len(papers_review):6}")

papers_retro = get_papers_by_study_type(retro_study).intersection(set(papers_covid19))
papers_retro = papers_retro - (papers_retro & papers_review)
print(f"{'Retrospective Study: ':25}{len(papers_retro):6}")

papers_simulation = get_papers_by_study_type(simulation).intersection(set(papers_covid19))
papers_simulation = papers_simulation - (papers_simulation & (papers_retro | papers_review))
print(f"{'Simulation: ':25}{len(papers_simulation):6}")

papers_others = set(papers_covid19) - (papers_review | papers_retro | papers_simulation)
print(f"{'Other Studies: ':25}{len(papers_others):6}")


# ### Therapeutic Methods
# 
# Therapeutic methods include the annotated chemicals contained in title and abstract of each article relevant to the according summary table. Due to false positive annotations of chemicals (i.e. proteins, molecule, etc.), we manually defined a list of entity names to exclude them.

# In[ ]:


drug_blocklist = ['/fio2', '04-MAY-2020', '2-o', '25-hydroxycholecalcifoerol', '25ohd', '3350',
                  '3mtm', "5'-tp", '6-o', '80-82 oc', 'acid', 'adverse drug', 'alcohol',
                  'alcohols', 'alkaline', 'amino acid-related', 'amp', 'amplify', 'androgen',
                  'antagonist', 'asp355asn', 'atp', 'bi', 'biopharmaceutical', 'bipap',
                  'bis(monoacylglycero)phosphate', 'bmp', 'cai', 'calcium channel', 'carbon dioxide',
                  'cationic', 'chemical', 'chemical compounds', 'chemical space', 'chemicals', 'co',
                  'co2', 'compound', 'compounds', 'copper', 'cov-2 poc', 'covalent', 'covalent fragments',
                  'covid-19', 'creatinine', 'cs', 'ctpa', 'cu', 'cys141', 'd-d', 'd-dimer', 'daegu', 'dfu',
                  'dic', 'dmec', 'drug molecules', 'drug products', 'effector', 'electron', 'electrophile',
                  'electrophilic fragment', 'eosin', 'ethylene oxide', 'eto', 'exoflo', 'extracellularly',
                  'fdp', 'fio2', 'food', 'food vacuole', 'foods', 'fumigants', 'gdp', 'glu166',
                  'glucose', 'glycan', 'h2o2', 'h7gmu', 'heme', 'hemoglobin', 'hemoglobin molecule',
                  'hepatocellular type', 'hfc%', 'hfno', 'hg', 'his', 'hormone', 'hormones',
                  'hpgp', 'hs', 'hydrogen', 'hydrogen peroxide', 'immunomodulators', 'immunomodulatory',
                  'in10', 'ingredients', 'inhibitor', 'inhibitors', 'iron', 'iso13485', 'ketone',
                  'l506a-f', 'lipid bis(monoacylglycero) phosphate', 'lipid', 'low-dose', 'lu',
                  'lysosomotropic drugs', 'magnesium', 'magnesium sulfate', 'mesh', 'metabolites', 'metal',
                  'metal ions', 'metals', 'meteorological', 'mineral', 'molecular', 'molecular electrostatic',
                  'molecular probes', 'molecule', 'molecules', 'mrna', 'mt039887', 'mt184913', 'mt259229',
                  'n', 'n-95', 'n95', 'nacl', 'ncpp', 'nct04330638', 'nct04355364', 'nct04359654',
                  'nitric oxide', 'nitrogen', 'niv', 'nmdd', 'no2', 'non-toxic', 'nps', 'nucleic acid',
                  'nucleoside', 'nucleotide', 'nutrients', 'o2', 'organs', 'outbroke', 'oxygen',
                  'oxygen heterocyclic compounds', 'oxygen partial', 'oxygen species', 'ozone', 'pao(2)/fio(2',
                  'pao2', 'peptidomimetics', 'pergamum', 'pesticides', 'pharmaceuticals', 'pharmacies',
                  'pharmacist', 'pharmacologically active substances', 'phd', 'phospholipid', 'phosphorus',
                  'phytochemicals', 'pic', 'pico', 'pigmented', 'plant', 'pm', 'pollutants', 'ppe',
                  'prodrug', 'progesterone', 'protein', 'proteins', 'quarantine', 'r +', 'radical', 'reagent',
                  'renine', 'residue', 'residues', 'ribose', 's2', 'sanitizer', 'sao2', 'se', 'ser', 'silica',
                  'silver', 'small-molecule inhibitors', 'sodium', 'spo(2)', 'spo2', 'srq-20', 'steroid',
                  'steroids', 'substance', 'substances', 'supplements', 'therapeutic', 'therapeutic agents',
                  'therapeutic anticoagulation', 'therapeutic drugs', 'thr27arg', 'topical', 'toxic',
                  'trizol', 'ultraviolet', 'urea', 'urea nitrogen', 'vdi', 'vph', 'water', 'xenobiotics']


# In[ ]:


print(len(drug_blocklist))


# ### Sample Size
# 
# Sample size information was extracted from abstract by regular expression. Types of sample size differ by study types, e.g. sample size of systematic reviews could be the number of articles being reviewed, while sample size of retrospective study or clinical trial could be the number of patients involved. As such, we defined two regex for extracting sample size information for different study types. Usually simulation articles do not have sample size information. 

# In[ ]:


ss_patient = re.compile(r'(\s)([0-9,]+)(\s|\s[^0-9,\.\s]+\s|\s[^0-9,\.\s]+\s[^0-9,\.\s]+\s)(patients|persons|cases|subjects|records)')
ss_review = re.compile(r'(\s)([0-9,]+)(\s|\s[^0-9,\.\s]+\s|\s[^0-9,\.\s]+\s[^0-9,\.\s]+\s)(studies|papers|articles|publications|reports|records)')


# ### Severity
# 
# Information on severity was extracted by searching abstracts for occurences of a list of severity keywords defined as follows.

# In[ ]:


severity_words = ['mild', 'moderate', 'severe', 'critical', 'icu', 'non-icu',
                  'fatality','mortality','mortalities','death','deaths','dead','casualty']


# ### General Outcome
# 
# When conclusion section is included in an abstract, it can be considered as the general outcome. Otherwise the last sentence containing the therapeutic methods or the last two sentences of the abstract are considered as general outcome.

# ### Primary Endpoint and Clinical Improvement
# 
# Any sentences in the abstract containing either the phrases of '*primary outcome*' or '*primary endpoint*' can be extracted as the primary endpoint. For clinical improvement, we defined a list of clinical improvement keywords, whose presence in an abstract indicates clinical improvement.

# In[ ]:


primary_phrase = ['primary outcome', 'primary endpoint']
improve_phrase = ['improve', 'better', 'amend', 'ameliorate', 'meliorate']


# ## Generating the Summary Tables
# 
# With the approach and relevant keywords defined above, we were able to build the two summary tables as follows. In the process, we excluded the articles without abstract or without mention of any therapeutic methods.

# ### Table 1:
# ### What is the best method to combat the hypercoagulable state seen in COVID-19_.csv
# 
# Total of 224 articles were identified as relevant to the above question.

# In[ ]:


papers_coagulation = papers.search_papers(query_coagulation, section = None, publish_year = '2020')
papers_coagulation = list(set(papers_coagulation) & set(papers_covid19))
print(f"{'Papers containing any hypercoagulability keywords: ':60}{len(papers_coagulation):6}")

selectpapers_coagulation = []
for paper in papers_coagulation:
    if 'Chemical' in papers.entity_nodes[str(paper)]:
        chemicals = [chem for chem in papers.entity_nodes[str(paper)]['Chemical'].keys() if chem.lower() not in drug_blocklist]
        if len(chemicals) > 0:
            selectpapers_coagulation.append(paper)

print(f"{'Selected papers addressing hypercoagulability:':60}{len(selectpapers_coagulation):6}")


# In[ ]:


papers.display_papers(selectpapers_coagulation[:1])


# The top therapeutic methods mentioned in the relevant articles were listed as follows:

# In[ ]:


entity_stats = papers.get_entity_stats(selectpapers_coagulation)
therapeutics = {}
for k, v in entity_stats['Chemical'].items():
    if k.lower() not in drug_blocklist:
        if k.lower() not in therapeutics:
            therapeutics[k.lower()] = v
        else:
            therapeutics[k.lower()] += v
print('-'*45)
print(f"| {'Chemicals':32} | {'Counts':6} |")
print('-'*45)
for i in sorted(therapeutics.items(), key = lambda x:x[1], reverse = True)[:15]:
      print(f"| {i[0]:32} | {i[1]:6} |")
print('-'*45)


# After excluding articles without abstracts or without mention of any therapeutic methods, 209 relevant articles were identified for extracting relevant information.

# In[ ]:


import csv
from datetime import date
from spacy.lang.en import English
nlp = English()
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)
file_name = 'summary_table_hypercoagulability'
with open(f"{csv_path}/{file_name}.csv", 'w', encoding = 'utf-8') as fcsv:
    csv_writer = csv.writer(fcsv)
    csv_writer.writerow(['Date', 'Study', 'Study Link', 'Journal', 'Study Type',
                         'Therapeutics', 'Sample Size', 'Severity', 'General Outcome',
                         'Primary Endpoints', 'Clinical Improvement', 'Added On',
                         'DOI', 'CORD_UID'])

    for pid in selectpapers_coagulation:
        file = json.load(open(f'{json_path}/{papers.nid2corduid[int(pid)]}.json', 'r', encoding = 'utf-8'))
        abstract = file['abstract']['text']
        if abstract == '': continue
        doc = nlp(abstract)
        sents_abs = list(doc.sents)
        if len(sents_abs) == 1:
            if 'copyright' in sents_abs[0].text:
                continue
        elif len(sents_abs) == 2:
            if 'copyright' in sents_abs[0].text:
                continue
            elif 'copyright' in sents_abs[1].text:
                sents_abs = sents_abs[0]
        else:
            if 'copyright' in sents_abs[-2].text:
                sents_abs = sents_abs[:-2]
            elif 'copyright' in sents_abs[-1].text:
                sents_abs = sents_abs[:-1]
        if len(sents_abs) == 0: continue
        pub_date = file['publish_time']
        study = file['title']['text']
        study_link = file['url']
        journal = file['journal']
        #study type
        if int(pid) in papers_review:
            study_type = 'Systematic Review'
        elif int(pid) in papers_retro:
            study_type = 'Retrospective Study'
        elif int(pid) in papers_simulation:
            study_type = 'Simulation'
        else:
            study_type = 'Other'
        # therapeutics
        chemicals = list(set(chem.lower() for chem in papers.entity_nodes[str(pid)]['Chemical'].keys() if chem.lower() not in drug_blocklist))
        therapeutics = ', '.join(chemicals)
        # sample size
        sample_size = ''
        if study_type == 'Systematic Review':
            matches = re.findall(ss_review, abstract)
            for match in matches:
                if match[1].isdigit() and int(match[1]) != 2019:
                    sample_size = sample_size + ''.join(match[1:]) + '; '
        elif study_type == 'Retrospective Study' or study_type == 'Other' :
            matches = re.findall(ss_patient, abstract)
            for match in matches:
                if match[1].isdigit() and int(match[1]) != 2019:
                    sample_size = sample_size + ''.join(match[1:]) + '; '
        # severity
        severity = []
        for phrase in severity_words:
            if phrase in abstract.lower():
                severity.append(phrase)
        severity = ', '.join(severity)
        # general outcome
        conclusion = ''
        conclusion_match = re.search(r'(?<=\s)(Conclusion[^,]?:\s?)(.*)', abstract, flags = re.I)
        if conclusion_match != None:
            conclusion = conclusion_match[2].strip()
        if conclusion != '':
            gen_outcome = conclusion
        else:
            if len(sents_abs) <= 2:
                gen_outcome = ' '.join(sent.text for sent in sents_abs)
            else:
                sents = []
                num = len(sents_abs)
                for sent_i, sent in enumerate(sents_abs):
                    if any(chem.lower() in sent.text.lower() for chem in chemicals) and sent_i < num-2:
                        sents.append(sent.text)
                if len(sents) > 0:
                    gen_outcome = sents[-1] + ' ' + sents_abs[-2].text + ' ' + sents_abs[-1].text
                else:
                    gen_outcome = sents_abs[-2].text + ' ' + sents_abs[-1].text
        # primary endpoint
        primary_endponit = ''
        for sent in doc.sents:
            if any(phrase.lower() in sent.text.lower() for phrase in primary_phrase):
                primary_endponit = primary_endponit + sent.text + ' '
        # clinical improvement
        clinical_improvement = ''
        if any(phrase.lower() in sent.text.lower() for phrase in improve_phrase):
            clinical_improvement = 'Y'
        # added on
        added_on = date.today().strftime('%m/%d/%Y')
        doi = file['doi']
        cord_uid = file['cord_uid']
            
        csv_writer.writerow([pub_date, study, study_link, journal, study_type, therapeutics, sample_size,
                             severity, gen_outcome, primary_endponit, clinical_improvement, added_on, doi, cord_uid])


# In[ ]:


import pandas as pd
table_hypercoagulability = pd.read_csv(f"{csv_path}/{file_name}.csv", na_filter= False)
print(f"{'Total papers:':20}{table_hypercoagulability.shape[0]:5}")
table_hypercoagulability.head()


# ### Table 2:
# ### What is the efficacy of novel therapeutics being tested currently_.csv
# 
# Total of 1,372 articles were filtered as associated with efficacy of novel therapeutics being tested currently.

# In[ ]:


papers_therapy = papers.search_papers(query_therapy, section = None, publish_year = '2020')
papers_therapy = list(set(papers_therapy) & set(papers_covid19))
print(f"{'Papers containing any therapeutic keywords:':60}{len(papers_therapy):6}")

papers_effect = papers.search_papers(query_effect, section = None, publish_year = '2020')
papers_effect = list(set(papers_effect) & set(papers_covid19))
print(f"{'Papers containing any efficacy keywords:':60}{len(papers_effect):6}")

papers_therapyeffects = list(set(papers_therapy) & set(papers_effect))
print(f"{'Papers containing both therapeutic and efficacy keywords:':60}{len(papers_therapyeffects):6}")

selectpapers_therapyeffects = []
for paper in papers_therapyeffects:
    if 'Chemical' in papers.entity_nodes[str(paper)]:
        chemicals = [chem for chem in papers.entity_nodes[str(paper)]['Chemical'].keys() if chem.lower() not in drug_blocklist]
        if len(chemicals) > 0:
            selectpapers_therapyeffects.append(paper)

print(f"{'Selected papers addressing therapeutic efficacy:':60}{len(selectpapers_therapyeffects):6}")


# In[ ]:


papers.display_papers(selectpapers_therapyeffects[:1])


# The top therapeutic methods mentioned in the associated articles were listed as follows:

# In[ ]:


entity_stats = papers.get_entity_stats(selectpapers_therapyeffects)
therapeutics = {}
for k, v in entity_stats['Chemical'].items():
    if k.lower() not in drug_blocklist:
        if k.lower() not in therapeutics:
            therapeutics[k.lower()] = v
        else:
            therapeutics[k.lower()] += v
print('-'*45)
print(f"| {'Chemicals':32} | {'Counts':6} |")
print('-'*45)
for i in sorted(therapeutics.items(), key = lambda x:x[1], reverse = True)[:15]:
      print(f"| {i[0]:32} | {i[1]:6} |")
print('-'*45)


# After the articles without abstract and the articles without mention of any therapeutic methods were excluded, there were 1,352 associated articles identified from which relevant information was extracted.

# In[ ]:


import csv
from datetime import date
from spacy.lang.en import English
nlp = English()
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)
file_name = 'summary_table_therapeutic_efficacy'
with open(f"{csv_path}/{file_name}.csv", 'w', encoding = 'utf-8') as fcsv:
    csv_writer = csv.writer(fcsv)
    csv_writer.writerow(['Date', 'Study', 'Study Link', 'Journal', 'Study Type',
                         'Therapeutics', 'Sample Size', 'Severity', 'General Outcome',
                         'Primary Endpoints', 'Clinical Improvement', 'Added On',
                         'DOI', 'CORD_UID'])

    for pid in selectpapers_therapyeffects:
        file = json.load(open(f'{json_path}/{papers.nid2corduid[int(pid)]}.json', 'r', encoding = 'utf-8'))
        abstract = file['abstract']['text']
        if abstract == '': continue
        doc = nlp(abstract)
        sents_abs = list(doc.sents)
        if len(sents_abs) == 1:
            if 'copyright' in sents_abs[0].text:
                continue
        elif len(sents_abs) == 2:
            if 'copyright' in sents_abs[0].text:
                continue
            elif 'copyright' in sents_abs[1].text:
                sents_abs = sents_abs[0]
        else:
            if 'copyright' in sents_abs[-2].text:
                sents_abs = sents_abs[:-2]
            elif 'copyright' in sents_abs[-1].text:
                sents_abs = sents_abs[:-1]
        if len(sents_abs) == 0: continue
        pub_date = file['publish_time']
        study = file['title']['text']
        study_link = file['url']
        journal = file['journal']
        #study type
        if int(pid) in papers_review:
            study_type = 'Systematic Review'
        elif int(pid) in papers_retro:
            study_type = 'Retrospective Study'
        elif int(pid) in papers_simulation:
            study_type = 'Simulation'
        else:
            study_type = 'Other'
        # therapeutics
        chemicals = list(set(chem.lower() for chem in papers.entity_nodes[str(pid)]['Chemical'].keys() if chem.lower() not in drug_blocklist))
        therapeutics = ', '.join(chemicals)
        # find relevant information from abstract
        abstract = file['abstract']['text']
        doc = nlp(abstract)
        # sample size
        sample_size = ''
        if study_type == 'Systematic Review':
            matches = re.findall(ss_review, abstract)
            for match in matches:
                if match[1].isdigit() and int(match[1]) != 2019:
                    sample_size = sample_size + ''.join(match[1:]) + '; '
        elif study_type == 'Retrospective Study' or study_type == 'Other' :
            matches = re.findall(ss_patient, abstract)
            for match in matches:
                if match[1].isdigit() and int(match[1]) != 2019:
                    sample_size = sample_size + ''.join(match[1:]) + '; '
        # severity
        severity = []
        for phrase in severity_words:
            if phrase in abstract.lower():
                severity.append(phrase)
        severity = ', '.join(severity)
        # general outcome
        conclusion = ''
        conclusion_match = re.search(r'(?<=\s)(Conclusion[^,]?:\s?)(.*)', abstract, flags = re.I)
        if conclusion_match != None:
            conclusion = conclusion_match[2].strip()
        if conclusion != '':
            gen_outcome = conclusion
        else:
            if len(sents_abs) <= 2:
                gen_outcome = ' '.join(sent.text for sent in sents_abs)
            else:
                sents = []
                num = len(sents_abs)
                for sent_i, sent in enumerate(sents_abs):
                    if any(chem.lower() in sent.text.lower() for chem in chemicals) and sent_i < num-2:
                        sents.append(sent.text)
                if len(sents) > 0:
                    gen_outcome = sents[-1] + ' ' + sents_abs[-2].text + ' ' + sents_abs[-1].text
                else:
                    gen_outcome = sents_abs[-2].text + ' ' + sents_abs[-1].text
        # primary endpoint
        primary_endponit = ''
        for sent in doc.sents:
            if any(phrase.lower() in sent.text.lower() for phrase in primary_phrase):
                primary_endponit = primary_endponit + sent.text + ' '
        # clinical improvement
        clinical_improvement = ''
        if any(phrase.lower() in sent.text.lower() for phrase in improve_phrase):
            clinical_improvement = 'Y'
        # added on
        added_on = date.today().strftime('%m/%d/%Y')
        doi = file['doi']
        cord_uid = file['cord_uid']
            
        csv_writer.writerow([pub_date, study, study_link, journal, study_type, therapeutics, sample_size,
                             severity, gen_outcome, primary_endponit, clinical_improvement, added_on, doi, cord_uid])


# In[ ]:


import pandas as pd
table_therapeuticefficacy = pd.read_csv(f"{csv_path}/{file_name}.csv", na_filter= False)
print(f"{'Total papers:':20}{table_therapeuticefficacy.shape[0]:5}")
table_therapeuticefficacy.head()

