#!/usr/bin/env python
# coding: utf-8

# CORD-19 Models and Open Questions
# ======
# 
# This notebook shows the query results for a single task. CSV summary tables can be found in the output section.
# 
# The report data is linked from the [CORD-19 Analysis with Sentence Embeddings Notebook](https://www.kaggle.com/davidmezzetti/cord-19-analysis-with-sentence-embeddings).

# In[ ]:


from cord19reports import install

# Install report dependencies
install()


# In[ ]:


get_ipython().run_cell_magic('capture', '--no-display', 'from cord19reports import run\n\ntask = """\nid: 4\nname: models_and_open_questions\n\n# Field definitions\nfields:\n    common: &common\n        - name: Date\n        - name: Study\n        - name: Study Link\n        - name: Journal\n        - name: Study Type\n\n    methods: &methods\n        - {name: Method, query: confirmation method, question: What rna confirmation method used}\n        - {name: Result, query: $QUERY conclusions findings results, question: What is conclusion on $QUERY}\n        - {name: Measure of Evidence, constant: "-"}\n\n    appendix: &appendix\n        - name: Sample Size\n        - name: Sample Text\n        - name: Study Population\n        - name: Matches\n        - name: Entry\n\nAre there studies about phenotypic change_:\n    query: Phenotypic genetic change\n    columns:\n        - *common\n        - *methods\n        - *appendix\n\nEfforts to develop qualitative assessment frameworks:\n    query: qualitative assessment frameworks\n    columns:\n        - *common\n        - {name: Addressed Population, query: $QUERY, question: What group studied}\n        - {name: Challenge, query: $QUERY, question: What challenge discussed}\n        - {name: Solution, query: solutions recommendations interventions, question: What is solution} \n        - {name: Measure of Evidence, constant: "-"} \n        - *appendix\n\nHow can we measure changes in COVID-19_s behavior in a human host as the virus evolves over time_:\n    query: Human immune response to COVID-19\n    columns:\n        - *common\n        - *methods\n        - *appendix\n\nSerial Interval (time between symptom onset in infector-infectee pair):\n    query: Serial Interval (for infector-infectee pair)\n    columns:\n        - *common\n        - {name: Age, query: median patient age, question: What is median patient age}\n        - {name: Sample Obtained, query: throat respiratory fecal sample, question: What sample}\n        - {name: Serial Interval (days), query: serial interval days, question: What is median serial interval}\n        - *appendix\n\nStudies to monitor potential adaptations:\n    query: studies monitor adaptations\n    columns:\n        - *common\n        - *methods\n        - *appendix\n\nWhat do models for transmission predict_:\n    query: Transmission model predictions\n    columns:\n        - *common\n        - {name: Method, query: statistical model approach, question: What model used}\n        - {name: Excerpt, query: r0 predict, question: What is model prediction}\n        - *appendix\n\nWhat is known about adaptations (mutations) of the virus_:\n    query: Virus mutations\n    columns:\n        - *common\n        - *methods\n        - *appendix\n\nWhat regional genetic variations (mutations) exist:\n    query: Regional genetic variations (mutations)\n    columns:\n        - *common\n        - *methods\n        - *appendix\n"""\n\n# Build and display the report\nrun(task)')

