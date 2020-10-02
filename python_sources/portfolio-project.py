#!/usr/bin/env python
# coding: utf-8

# # PORTFOLIO PROJECT - Data Science analytical abilities
# A case study on Chronic Disease Indicators

# **INRTODUCTION**
# 
# My passion for Data Science started by chance, during the first explosion of COVID-19. I've stared mapping cases and traking developments through dashboards. I wanted to learn more, not about the COVID it self, but rather about dataframes and all the tecnologies realted to implement reserches where data and numbers become significant insights to confirm a theory or to enlight new aspects of a topic.
# The most remarkable definition of Data Scientist is the well known IBM statement: "A data scientist represents an evolution from the business or data analyst role. The formal training is similar, with a solid foundation typically in computer science and applications, modeling, statistics, analytics and math. What sets the data scientist apart is strong business acumen, coupled with the ability to communicate findings to both business and IT leaders in a way that can influence how an organization approaches a business challenge. Good data scientists will not just address business problems, they will pick the right problems that have the most value to the organization"
# 
# 
# 
# 

# **METHODOLOGY**
# 
# The structure of this project refers to John Rollins' Methodology insights. The most common methodology applications in Data science are CRISP-DM Methodology and the Foundational Methodology. 
# 
# The CRISP-DM (Cross Industry Process for Data Mining) methodology is a process aimed at increasing the use of data mining over a wide variety of business applications and industries. The intent is to take case specific scenarios and general behaviors to make them domain neutral.  CRISP-DM is comprised of six steps with an entity that has to implement in order to have a reasonable chance of success. The six steps are shown in the following diagram:![crisp-md.png](attachment:crisp-md.png)
# 

# More in details, the Foundational Methotodolgy Outline marks the steps of the analytic process that leads the data scientist in standardized path of development that can be applicapale to any field of reserch.![foundational-methodology.png](attachment:foundational-methodology.png)

#  
# **Business Understanding:**  
# This is the first stage where the intention of the project is outlined. The understanding of business requests and needs will determine what data would be collected, from what sources and by what methods
# 
# **Analytic Approach:**  
# Once the problem to be addressed is defined, the appropriate analytic approach for the problem is selected in the context of the business requirements. This means identifying what type of patterns will be needed to address the question most effectively: 
# <ul>
#     <li> Descriptive models: current status evaluation. </li>
#     <li> Diagnostic approach: statistical analysis </li>
#     <li> Predictive models: determines probability of an action</li>
#     <li> Classification models: answers to yes/no questions forecasting a response </li>
#     <li> Prescriptive approach: Utilize AI strategies to enlight a solution for a problem
#     Machine Learning can be used to identify relationships and trends in data that might otherwise not be accessible or identifie. For exemple the decision tree classifier provides both the predicted outcome, as well as the likelihood of that outcome. This would allowd to discover and fix failures in systems organization, or other structural problems according to the benchmark Industry.
#         </ul>
#     
# **Data Requirements | Data Collection | Data Understanding:**  
# The decision about which data can be meaningful relies on business understanding. Through a real comprhension of the stakholders' requests and of the analytical approach that will be implemented is possible to identifying the necessary data content, formats and sources for initial data collection. Data understanding encompasses all activities related to constructing the data set. Essentially, the data understanding section of the data science methodology ensures that the data collected is representative of the problem to be solved.  
# 
# **Data Preparation:**  
# Once the data has been collected, it must be transformed into a useable subset unless it is determined that more data is needed. Once a dataset is chosen, it must then be checked for questionable, missing, or ambiguous cases. Together with data collection and data understanding, data preparation is the most time-consuming phase of a data science project, typically taking seventy percent and even up to ninety percent of the overall project time.  
# 
# **Modeling:**  
# Once prepared for use, the data must be expressed through whatever appropriate models, give meaningful insights, and hopefully new knowledge. This is the purpose of data mining: to create knowledge information that has meaning and utility. The use of models reveals patterns and structures within the data that provide insight into the features of interest.  
# 
# **Evaluation:**  
# The selected model must be tested. This is usually done by having a pre-selected test to see the effectiveness of the model. Results from this are used to determine efficacy of the model and foreshadows its role in the next and final stage.  
# 
# **Deployment:**  
# In the deployment step, the model is used on new data outside of the scope of the dataset and by new stakeholders. The new interactions at this phase might reveal the new variables and needs for the dataset and model.   
# 
# **Feedback:**  
# A constant monitoring of feedback enable further adjustemnts to modeling. The feedback process is rooted in the notion that, the more you know, the more that you'll want to know, this makes the methodology cyclical ensuring constant assessment for performance and impact of the model. 

# REPORT
# 
# About The Data set:  
# 
# Kaggle is an online platform and community of data scientist and machine learning developers, that offers tools and public data for pratcticing pourposes.
# As a Life science student my favourite industry is Health and Biology, so I've utilized Kaggle for searching a pertaining set.
# The aim of the project is to demonstrate my abilities in reporting a comprhensive analysis of data frames operating a variety of Data science tools. The purpose of the research is merely demonstrative of technical capabilities and it doesn't set the goal of pursuing an evaluation of the contents.  
# 
# 
# The Kaggle's data set under esamination is "Chronic Disease Indicator -  A Disease Data across the US, 2001-2016" collected by CDC - Centers for Diseases Control and Prevention  
# 
# From CDC Data set's Description:
# 
# >"Context:
# CDC's Division of Population Health provides cross-cutting set of 124 indicators that were developed by consensus and that allows states and territories and large metropolitan areas to uniformly define, collect, and report chronic disease data that are important to public health practice and available for states, territories and large metropolitan areas. In addition to providing access to state-specific indicator data, the CDI web site serves as a gateway to additional information and data resources.
# 
# >Content:
# A variety of health-related questions were assessed at various times and places across the US over the past 15 years. Data is provided with confidence intervals and demographic stratification."
# 
# About the Analytical Approach:  
# 
# The objective is to create an abstract that investigates the most common chronic diseases in the US, pointing at correlations between indicators and locality Hospital spendings, gender, etnicity. In a second step, the focus will be mantained about alcohol comsumption, comparing it to other diseases, advocating abuse prevention.
# For this purposes, a descriptive model is applied, upcoming insights are expressed in visualizations and dashboards enchancing the meanings of the findings and providing a straightfoward understanging of correlations, patterns and trends.
# 
# 
# IMPLEMETATION
# 
# 
# 

# In[ ]:


# Loading Libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

#Import needed packages to process data
import sklearn
import matplotlib as mpl
import matplotlib.pyplot as plt


# In[ ]:


# Loading Data Set

csv_path = "../input/chronic-disease/U.S._Chronic_Disease_Indicators.csv"
df_src=pd.read_csv(csv_path, low_memory=False)


# In[ ]:


# Visualizing first 5 lines of Data

df_src.head()


# **Data Understanding:**

# In[ ]:


# Data Understanding

df_src.info()


# In[ ]:


# check completely filled features

(df_src.count()/len(df_src))*100


# In[ ]:


# defining an indexed function that explores the features of each columnt

def df_values(df):
    for i in range(0, len(df.columns)):
        print("***** Feature:", df.columns[i], "*****")
        print (df.iloc[:,i].value_counts())
        print("\n ")

df_values(df_src)


# **Data Preparation:**

# In[ ]:


# dropping unmeaningful columns by index

df_src.drop([2,4,7,11,12,14,15,18,19,20,21,23,24,26,27,28,29,30,31,32,33])


# In[ ]:


# Dropping rows with muissing value in the Data Value column

df_src.dropna(subset=['DataValue'])


# **Modeling:**

# In[ ]:


# Getting insights about diseases analyzing the 'Topic' subset

CountStatus=df_src['Topic'].value_counts()
print (CountStatus)

CountStatus.plot.barh()


# In[ ]:


#selecting the amount of dollars values

df_exp= df_src[df_src['DataValueUnit']=='$']
df_exp.info()


# In[ ]:


# evaluating sanitary expenses by location 
df_exp['LocationDesc'].value()


# In[ ]:




