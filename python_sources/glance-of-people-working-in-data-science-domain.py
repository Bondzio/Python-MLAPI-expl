#!/usr/bin/env python
# coding: utf-8

# ## 1. Load the data and do exploration

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# **1.1 Explore the data**

# In[ ]:


questions = pd.read_csv('../input/kaggle-survey-2019/questions_only.csv')


# In[ ]:


questions.columns


# In[ ]:


questions.head()


# In[ ]:


questions.shape


# #### Get the question lists

# In[ ]:


for column  in questions.columns:
    print(f'{column}:{questions[column].values}')


# ### 1.2 Explore the responses

# In[ ]:


response = pd.read_csv('../input/kaggle-survey-2019/multiple_choice_responses.csv')


# #### Get the multiple choices response columns

# In[ ]:


for column in response.columns:
    print(column)


# In[ ]:


response.describe()


# In[ ]:


response.head()


# #### Explore Q5: the title of current position

# In[ ]:


work_title = response['Q5'].value_counts()[:-1]


# In[ ]:


work_title


# #### Explore Q2: Gender distribution

# In[ ]:


gender = response['Q2'].value_counts()[:-1]


# In[ ]:


gender


# In[ ]:


g = gender/sum(gender)*100


# In[ ]:


g=g.tolist()


# In[ ]:


print(f'The percentages are: {g}'+'%')


# In[ ]:


gender.plot.bar()


# #### Explore Q9: Activities that make up an important role at work

# In[ ]:


choices = ['Q9_Part_1',
'Q9_Part_2',
'Q9_Part_3',
'Q9_Part_4',
'Q9_Part_5',
'Q9_Part_6',
'Q9_Part_7',
'Q9_Part_8']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'activity counts': counts}, index=values)
df = df.sort_values(by='activity counts')
df 


# In[ ]:


ax = df.plot.barh()


# #### Explore Q10: Current yearly compensation 

# In[ ]:


income = response['Q10'].value_counts()


# In[ ]:


income[:-1].plot.bar()


# In[ ]:


gender = response['Q2'].tolist()[1:]


# In[ ]:


salary = response['Q10'].tolist()[1:]


# In[ ]:


title = response['Q5'].tolist()[1:]


# In[ ]:


a = {'gender':gender,'salary':salary,'title':title}


# In[ ]:


income = pd.DataFrame.from_dict(a)


# In[ ]:


income.describe()


# In[ ]:


income_t_s = income.groupby(by=['title','salary'])


# In[ ]:


income_t_s.describe()


# In[ ]:


income.groupby(by=['title','salary']).get_group


# In[ ]:


income.dropna()


# In[ ]:


femal_income = income.loc[income['gender'] == 'Female']
male_income = income.loc[income['gender'] == 'Male']


# In[ ]:


f_i = femal_income['salary'].value_counts()


# In[ ]:


m_i = male_income['salary'].value_counts()


# In[ ]:


f_i.plot.bar()


# In[ ]:


m_i.plot.bar()


# #### Q13: On which platforms have you begun or completed data science courses?

# In[ ]:


choices = ['Q13_Part_1',
'Q13_Part_2',
'Q13_Part_3',
'Q13_Part_4',
'Q13_Part_5',
'Q13_Part_6',
'Q13_Part_7',
'Q13_Part_8',
'Q13_Part_9',
'Q13_Part_10',
'Q13_Part_11',
'Q13_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'course platform counts': counts}, index=values)
df = df.sort_values(by='course platform counts',ascending = False)
df 


# #### Q14: Primary tools used in work

# In[ ]:


tools = response['Q14'].value_counts()
print(tools[:-1])
tools[:-1].plot.barh()


# #### Q16: Which of the following integrated development environments (IDE's) do you use on a regular basis?

# In[ ]:


choices = ['Q16_Part_1',
'Q16_Part_2',
'Q16_Part_3',
'Q16_Part_4',
'Q16_Part_5',
'Q16_Part_6',
'Q16_Part_7',
'Q16_Part_8',
'Q16_Part_9',
'Q16_Part_10',
'Q16_Part_11',
'Q16_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'IDE counts': counts}, index=values)
df = df.sort_values(by='IDE counts',ascending = False)
df 


# In[ ]:





# #### Q18:What programming languages do you use on a regular basis?

# In[ ]:


choices = ['Q18_Part_1',
'Q18_Part_2',
'Q18_Part_3',
'Q18_Part_4',
'Q18_Part_5',
'Q18_Part_6',
'Q18_Part_7',
'Q18_Part_8',
'Q18_Part_9',
'Q18_Part_10',
'Q18_Part_11',
'Q18_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'coding language': counts}, index=values)
df = df.sort_values(by='coding language',ascending = False)
df 


# #### Q20: What data visualization libraries or tools do you use on a regular basis?

# In[ ]:


choices = ['Q20_Part_1',
'Q20_Part_2',
'Q20_Part_3',
'Q20_Part_4',
'Q20_Part_5',
'Q20_Part_6',
'Q20_Part_7',
'Q20_Part_8',
'Q20_Part_9',
'Q20_Part_10',
'Q20_Part_11',
'Q20_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'libary counts': counts}, index=values)
df = df.sort_values(by='libary counts',ascending = False)
df 


# #### Q23: For how many years have you used machine learning methods?

# In[ ]:


years = response['Q23'].value_counts()
print(years[:-1])
years[:-1].plot.barh()


# #### Q24:Which of the following ML algorithms do you use on a regular basis?

# In[ ]:


choices = ['Q24_Part_1',
'Q24_Part_2',
'Q24_Part_3',
'Q24_Part_4',
'Q24_Part_5',
'Q24_Part_6',
'Q24_Part_7',
'Q24_Part_8',
'Q24_Part_9',
'Q24_Part_10',
'Q24_Part_11',
'Q24_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'ML algorithm counts': counts}, index=values)
df = df.sort_values(by='ML algorithm counts',ascending = False)
df 


# #### Q25: Category of ML tools

# In[ ]:


choices=['Q25_Part_1',
'Q25_Part_2',
'Q25_Part_3',
'Q25_Part_4',
'Q25_Part_5',
'Q25_Part_6',
'Q25_Part_7',
'Q25_Part_8']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'ML tools counts': counts}, index=values)
df = df.sort_values(by='ML tools counts',ascending = False)
df


# In[ ]:





# #### Q28: ML frames used in daily basis

# In[ ]:


choices=['Q28_Part_1',
'Q28_Part_2',
'Q28_Part_3',
'Q28_Part_4',
'Q28_Part_5',
'Q28_Part_6',
'Q28_Part_7',
'Q28_Part_8',
'Q28_Part_9',
'Q28_Part_10',
'Q28_Part_11',
'Q28_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'ML frameworks counts': counts}, index=values)
df = df.sort_values(by='ML frameworks counts',ascending = False)
df


# In[ ]:





# #### Q29: Which of the following cloud computing platforms do you use on a regular basis?

# In[ ]:


choices=['Q29_Part_1',
'Q29_Part_2',
'Q29_Part_3',
'Q29_Part_4',
'Q29_Part_5',
'Q29_Part_6',
'Q29_Part_7',
'Q29_Part_8',
'Q29_Part_9',
'Q29_Part_10',
'Q29_Part_11',
'Q29_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'cloud computing platforms counts': counts}, index=values)
df = df.sort_values(by='cloud computing platforms counts',ascending = False)
df


# #### Q31: Which specific big data / analytics products do you use on a regular basis? (Select all that apply) - Selected Choice

# In[ ]:


choices=['Q31_Part_1',
'Q31_Part_2',
'Q31_Part_3',
'Q31_Part_4',
'Q31_Part_5',
'Q31_Part_6',
'Q31_Part_7',
'Q31_Part_8',
'Q31_Part_9',
'Q31_Part_10',
'Q31_Part_11',
'Q31_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'bigdata products counts': counts}, index=values)
df = df.sort_values(by='bigdata products counts',ascending = False)
df


# #### Q32: Which of the following machine learning products do you use on a regular basis? 

# In[ ]:


choices=['Q32_Part_1',
'Q32_Part_2',
'Q32_Part_3',
'Q32_Part_4',
'Q32_Part_5',
'Q32_Part_6',
'Q32_Part_7',
'Q32_Part_8',
'Q32_Part_9',
'Q32_Part_10',
'Q32_Part_11',
'Q32_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'ML products counts': counts}, index=values)
df = df.sort_values(by='ML products counts',ascending = False)
df


# #### Q33: Which automated machine learning tools (or partial AutoML tools) do you use on a regular basis? 

# In[ ]:


choices=['Q33_Part_1',
'Q33_Part_2',
'Q33_Part_3',
'Q33_Part_4',
'Q33_Part_5',
'Q33_Part_6',
'Q33_Part_7',
'Q33_Part_8',
'Q33_Part_9',
'Q33_Part_10',
'Q33_Part_11',
'Q33_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'automated machine learning tools counts': counts}, index=values)
df = df.sort_values(by='automated machine learning tools counts',ascending = False)
df


# #### Q34:Which of the following relational database products do you use on a regular basis?

# In[ ]:


choices=['Q34_Part_1',
'Q34_Part_2',
'Q34_Part_3',
'Q34_Part_4',
'Q34_Part_5',
'Q34_Part_6',
'Q34_Part_7',
'Q34_Part_8',
'Q34_Part_9',
'Q34_Part_10',
'Q34_Part_11',
'Q34_Part_12']


# In[ ]:


values = []
counts = []
for choice in choices:
    value = response[choice][1:].value_counts().keys().tolist()[0]
    count = response[choice][1:].value_counts().tolist()[0]
    values.append(value)
    counts.append(count)

df = pd.DataFrame({'relational database products counts': counts}, index=values)
df = df.sort_values(by='relational database products counts',ascending = False)
df


# ### 1.3 Explore text files

# In[ ]:


texts = pd.read_csv('../input/kaggle-survey-2019/other_text_responses.csv')


# In[ ]:


texts.columns


# In[ ]:


texts.describe()


# In[ ]:


texts.shape


# In[ ]:


texts.tail()


# In[ ]:


for column  in questions.columns:
    print(f'{column}:{questions[column].values}')


# In[ ]:


for column in texts.columns:
    tools = texts[column].value_counts()
    print(f'{column}:{tools[:5]}')
#     tools[:-1].plot.barh()


# ### 1.4 Explore schema file

# In[ ]:


schemas = pd.read_csv('../input/kaggle-survey-2019/survey_schema.csv')


# In[ ]:


schemas.describe()


# In[ ]:


schemas.shape


# Still working on the analysis

# In[ ]:




