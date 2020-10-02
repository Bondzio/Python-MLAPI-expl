#!/usr/bin/env python
# coding: utf-8

# ## Understanding Data science work beyond Designation

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

from IPython.display import Image
import pandas as pd
#import matplotlib as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from IPython.display import HTML, display
import tabulate
import matplotlib.pyplot as plt
def replace_str(row,axis=1):
    if (isinstance(row,str)):
        return 1
    else:
        return 0

# Any results you write to the current directory are saved as output.


# ### What are the roles and responsibilities of Data Scientist?
# 
# To be Honest, Job nature of Data Scientist is quite vague and not clearly defined.

# In[ ]:


x = Image(filename='/kaggle/input/memesdata/Analyst.jpg') 
y = Image(filename='/kaggle/input/memesdata/Stastics_meme.jpg') 
display(x, y)


# ## Based on Garner, roles and responsibities of the data science are 

# In[ ]:


x = Image(filename='/kaggle/input/memesdata/responsibilites.jpg')
display(x)


# Several Similair definition are found in the Internet. 
# 
# The Data Science role is too boarder term just like the software enginner role. Many unique software engineer roles are created to handle different problems. Different software engineer roles in the market are Backend engineer, Full Stack development, IT Admin, Android Developer etc. The skills required to master each roles are clearly defined.
# 
# Similarly, different roles in data science are defined as below

# In[ ]:


x = Image(filename='/kaggle/input/memesdata/udacity_images.jpg')
display(x)


# In data science world, roles are not uniformly defined and nature of work changes from company to company. Few contradictions are 
# * A company X may define data scientist work as providing insights to better business development
# * A Company Y may define data scientist work as developing end to end machine learning product
# * A person may be designed as the Data scientist but his work may involve only sql queries
# * A Person may be designed at software engineer in startup but actually solving machine learning problems.

# ## In this given casestudy, the attempt is made to understand different nature of the work (based on the Question 9)
# 
# Select any activities that make up an important part of your role at work: (Select all that apply) - Other - Text
# 
# 1. Analyze and understand data to influence product or business decisions
# 1. Build and/or run the data infrastructure that my business uses for storing, analyzing, and operationalizing data
# 1. Build prototypes to explore applying machine learning to new areas
# 1. Build and/or run a machine learning service that operationally improves my product or workflows
# 1. Experimentation and iteration to improve existing ML models
# 1. Do research that advances the state of the art of machine learning

# In[ ]:


multi_choice = pd.read_csv('/kaggle/input/kaggle-survey-2019/multiple_choice_responses.csv')
#print(len(multi_choice))
required_columns = multi_choice.columns
Activity_column=[x for x in required_columns if "Q9_Part" in x]
Activity_column = Activity_column[:-2]
Activity_column_value = ['Analyze and understand data to influence product or business decisions',
'Build and/or run the data infrastructure that my business uses for storing, analyzing',
'Build prototypes to explore applying machine learning to new areas',
'Build and/or run a machine learning service that operationally improves my product or workflows',
'Experimentation and iteration to improve existing ML models',
'Do research that advances the state of the art of machine learning']
for i in range(0,len(Activity_column)):
    multi_choice[Activity_column_value[i]]= multi_choice[Activity_column[i]].apply(replace_str)
multi_choice['Combined_Role'] = multi_choice[Activity_column_value].apply(
    lambda x: ','.join(x.dropna().astype(str)),
    axis=1
)
multi_choice = multi_choice[multi_choice.Combined_Role!="0,0,0,0,0,0"]
db = DBSCAN(eps=0.2, min_samples=200,metric='jaccard').fit(multi_choice[Activity_column_value])
multi_choice['cluster_labels'] = db.labels_

cluster_list=list(dict(multi_choice.cluster_labels.value_counts()).items())
designation_list = ["Fullstack Data Scientist","Noise","Data Analyst","Operational Data Analyst","Data Science Analyst","Operational Data Science Analyst","POC Data Scientist","Product Data Scientist"
                   ,"Data Engineer","Software Engineer","Researcher","Machine Learning Engineer"]
cluster_info = []
#print(len(designation_list),len(cluster_list))
for i in range(0,len(cluster_list)):
    cluster_info.append([cluster_list[i][0],cluster_list[i][1],designation_list[i]])
header_column = ["cluster_labels","No of people","Assumed Designation"]
cluster_df = pd.DataFrame(cluster_info,columns=header_column)
multi_choice =pd.merge(cluster_df,multi_choice,on=['cluster_labels'])
#multi_choice.cluster_labels.value_counts()


# ##### Based on the nature of the work, data scientist are clustered into different group. 
# ##### Clustering is done using density based clustering with Jaccard distance
# ##### For simiplicity purpose, People who perform atleast one of the above 6 task is taken into study
# 
# ## Different Clusters and assumed nature of work is added below

# In[ ]:





# 

# In[ ]:


cluster_df


# ### FullStack Data Scientist:
#     # Roles of the FullStack Data Scientist is to deliever end to end machine learning product.
#     # This folks works in all areas in the data science projects.
# 

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Fullstack Data Scientist'][Activity_column_value].head(3)


# ### Data Analyst:
#     # Roles of the Data Analyst is to give insight for improving business product and developing better product. 
#     # Their works may or may not use machine learning algorithm

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Data Analyst'][Activity_column_value].head(3)


# ### Operational Data Analyst:
#     #Operational Data Analyst work focuses on extracting data from product and tools and give insights for improving business product and developing better product. 
#     #This folks works may or may not use machine learning algorithm

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Operational Data Analyst'][Activity_column_value].head(3)


#  ### Data Science Analyst:
#     Data Science Analyst are data analyst with Data science experience

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Data Science Analyst'][Activity_column_value].head(3)


# ### Operational Data Science Analyst:
#     Operational Data Science Analyst are Operational analyst with Data science experience

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Operational Data Science Analyst'][Activity_column_value].head(3)


# ### POC Data Scientist:
#     POC Data Scientist roles focus morely on creating POC data projects. 

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='POC Data Scientist'][Activity_column_value].head(3)


# ### Product Data Scientist:
# Product Data Scientist role focus on building machine learning products. In large companies, there will be others to take care of pushing these models to production 

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Product Data Scientist'][Activity_column_value].head(3)


# ### Data Engineer:
#     DRole is to build and run data infrastructure required to extract data

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Data Engineer'][Activity_column_value].head(3)


# ### Software Engineer- Machine learning:
#      Software engineer role is to integrate machine learning into the product. They may or may not involve in machine learning work

# ### Researcher
#     Data scientist who working on Research and Development team

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Researcher'][Activity_column_value].head(3)


# Machine learning engineer
#     Roles is combination of Product Data scientist and Software engineer

# In[ ]:


multi_choice[multi_choice['Assumed Designation']=='Machine Learning Engineer'][Activity_column_value].head(3)


# In[ ]:


def build_heat_map(df,Main_Column,Main_Column_Description,Column_Name,Column_Desription):
    total_value = []
    each_value = []
    Designation = df[Column_Name].unique()
    #print(Designation)
    Assumed_Designation = df[Main_Column].unique()
    for each_assumed in Assumed_Designation:
        each_assumed_df = df[multi_choice[Main_Column]==each_assumed]
        each_assumed_count = len(each_assumed_df)
        each_value = []
        for each in Designation:
        #pr
            each_count = len(each_assumed_df[each_assumed_df[Column_Name]==each])/each_assumed_count
            each_value.append(each_count)
        total_value.append(each_value)
    heaf_map_df = pd.DataFrame(total_value,index=Assumed_Designation,columns=Designation)
    #print(heaf_map_df.columns)
    plt.figure(figsize=(20, 20))
    plt.imshow(heaf_map_df, cmap="YlGnBu")
    plt.colorbar()
    plt.xticks(range(len(heaf_map_df.columns)),heaf_map_df.columns, rotation=20)
    plt.yticks(range(len(heaf_map_df)),heaf_map_df.index)
    plt.show()


# In[ ]:


multi_choice = multi_choice[multi_choice["Assumed Designation"]!='Noise']
multi_choice.drop(multi_choice.index[0],inplace=True)
build_heat_map(multi_choice,'Assumed Designation','Assumed Designation','Q5','Designation')


# Inference
# * Full Data Scientist, Product Data Scientist, Machine Learning Engineer are highly seen as data scientist
# * Data Science Analyst and Operation Data Scientist Analyst are clearly seen as Data scientist but sometimes seen as data analyst
# * Data Analyst and Operation Analyst as commonly seen as data analyst but some companies name them as data scientist
# * Data Engineer are generally seen as software engineer and data engieer. Data engineer sometimes overlaps with data scientist role
# * POC Data Scientist, Software Engineer - Machine Learning are seen as software engineer, data scientist, research scientist. Role is not that very defined
# * Researcher is strong seen as Research Scientist

# In[ ]:


build_heat_map(multi_choice,'Assumed Designation','Assumed Designation','Q4','Qualification')


# ### Inference
# * Researcher are mostly Master and Ph.d. This is expected as the entry is high for R&D
# * Most of Data Engineer and Software Engineer have Master and few have Bachelor Degree. Bachelor Degree is bar for software engieer
# * Data Science Analyst and Operation Science Analyst have more number of Master Degree compared to Data Analyst and Operation Analyst. 
# * Machine Learning Engineer Role is  highly filled Master Degree guys
# * It is better to go for Master Degree if you want Data Science Career. 
# * Software Engineer and Data Analyst Jobs can be found with Bachelor degree itseld

# In[ ]:


def convert_integer(salary):
    if isinstance(salary,str):
        return int(salary)
    else:
        -1

multi_choice['higher_salary'] = multi_choice.Q10.str.replace(">$","")
multi_choice['higher_salary'] = multi_choice.higher_salary.str.replace(",","")
filled_salary = multi_choice[pd.notnull(multi_choice.higher_salary)]
filled_salary.drop(filled_salary.index[0],inplace=True)
filled_salary['higher_salary'] = filled_salary.higher_salary.str.split(pat="-", n=-1, expand=True)[1]
filled_salary['higher_salary']=filled_salary.higher_salary.apply(convert_integer)
filled_salary = filled_salary[filled_salary.higher_salary!=-1]

def plot_salary(salary_df):
    total_value = []
    each_value = []
    Assumed_Designation = multi_choice['Assumed Designation'].unique()
    index = Assumed_Designation
    for each_assumed in Assumed_Designation:
        mean_value = salary_df[salary_df['Assumed Designation']==each_assumed].higher_salary.mean()
        min_value = salary_df[salary_df['Assumed Designation']==each_assumed].higher_salary.median()
        #max_value = salary_df[salary_df['Assumed Designation']==each_assumed].higher_salary.quantile(0.75)
        #max_value2 = salary_df[salary_df['Assumed Designation']==each_assumed].higher_salary.quantile(0.25)
        each_value = [mean_value,min_value] #,max_value,max_value2]
        total_value.append(each_value)
    
    group_labels = ['mean','median'] #,'75%','25%']
    Data_analytics = pd.DataFrame(total_value,index=Assumed_Designation,columns=group_labels)
    
# Convert data to pandas DataFrame.
    
# Plot.
    pd.concat(
        [Data_analytics[group_labels[0]],Data_analytics[group_labels[1]]],
        axis=1).plot.bar(figsize=(20, 20))
    
    return


# ## Salary Range in United States

# In[ ]:


usa_salary = filled_salary[filled_salary.Q3=="United States of America"]
plot_salary(usa_salary)


# ### Salary Range in India

# In[ ]:


usa_salary = filled_salary[filled_salary.Q3=="India"]
plot_salary(usa_salary)


# ### Inference
# 
# Common pattern in both countries
# 1. Data Science Analyst paid more than Data Analyst.
# 2. Full Stack Data Scientist is paid more than everyone
# 3. Product Data Scientist is paid more than POC Data Scientist

# In[ ]:




