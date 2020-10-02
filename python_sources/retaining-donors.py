#!/usr/bin/env python
# coding: utf-8

# <HTML>
# <div id="home"></div>
# <DIV style="height:450px;"> 
# 
# 
# <p style="color:goldenrod;font-family:Calibri;font-size:40px;position:absolute;top:25px;left:160px"> Retaining Donors</p>
# <a href="https://www.donorschoose.org/">
# <IMG SRC="https://kaggle2.blob.core.windows.net/organizations/1318/thumbnail.png%3Fr=621" style="height:80px; position:absolute; left:50px;top:20px;"></IMG>
# </a>
# 
# <a href="https://www.kaggle.com/donorschoose/io/discussion/56026">
# <IMG SRC="https://kaggle2.blob.core.windows.net/datasets-images/23690/31950/f2908d9c26b87050c04ddc0f5f0e8409/dataset-cover.jpg?t=2018-05-04-22-07-00"  style="position:absolute; left:50px;top:100px;"></IMG>
# </a>
# 
# 
# </DIV>
# </HTML>

# ## Problem Statement
# *DonorsChoose.org has funded over 1.1 million classroom requests through the support of 3 million donors, the majority of whom were making their first-ever donation to a public school. If DonorsChoose.org can motivate even a fraction of those donors to make another donation, that could have a huge impact on the number of classroom requests fulfilled.*
# 
# *A good solution will enable DonorsChoose.org to build targeted email campaigns recommending specific classroom requests to prior donors. *
# 
# *Part of the challenge is to assess the needs of the organization, uncover insights from the data available, and build the right solution for this problem. Submissions will be evaluated on the following criteria:
# Performance - How well does the solution match donors to project requests to which they would be motivated to donate? DonorsChoose.org will not be able to live test every submission, so a strong entry will clearly articulate why it will be effective at motivating repeat donations.*
# *Adaptable - The DonorsChoose.org team wants to put the winning submissions to work, quickly. Therefore a good entry will be easy to implement in production.
# Intelligible - A good entry should be easily understood by the DonorsChoose.org team should it need to be updated in the future to accommodate a changing marketplace.*

# ## Contents
# 
# ### 1. Exploration of Donation.csv dataset
#  1.1 Loading the required packages
#  
# 1.2 Data Understanding
# 
# 1.3 Summarising the data
# 
# 1.4 Understandng the Key Metrics
# 
# ### 2. Exploration of Projects.csv dataset
# 2.1 Loading the required packages
# 
# 2.2 Data understanding is provided in this section
# 
# 2.3 Understanding which subjects are more frequent
# 
# 2.4 Understanding which Subjects are more frequent
# 
# ### 3. To be added
# ###  

# In[18]:


from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
if (code_show){
$('div.input').hide();
} else {
$('div.input').show();
}
code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="SHOW CODES"></form>''')


# ## 1. Exploration of Donation.csv dataset

# ## 1.1 Loading the required packages

# In[3]:


#Declaring the required libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ## 1.2 Data understanding is provided in this section
# #### The data provides information of donations made by different donors for various projects

# In[4]:


#Loading data for Donations
Donations = pd.read_csv('../input/Donations.csv')
Donations.head(3)


# ## 1.3 Summarising the Donation data

# In[5]:


#describe function is used to get the statistics associated to Donations made
summary =Donations["Donation Amount"].describe()

#Preparation of the summary in presentable format
summary1 = {'Category': ['Total Records', 'Mean', 'Standard deviation', 'Max', 'Min', '25th Percentile', '50th Percentile',
                         '75th Percentile'
                        ],
            'Values (in $) ': [round(summary[0],0), round(summary[1],2), round(summary[2],2) , round(summary[7],2),
                       round(summary[3],2), round(summary[4],2), round(summary[5],2), round(summary[6],2)
                      ] 
           }
index = [0,1,2,3,4,5,6,7]

tabular_summary = pd.DataFrame(summary1, index=index)

#final table which provides the summary
tabular_summary


# ## 1.4 Understanding the Key Metrics
# 
# #### The key metrics from this table (Donations.csv) are Project ID, Donor ID and Donation Amount
# 
# #### In order to fetch insights from these metrics, it would be better to get the total Projects and Donors across different groups of Donation amount. 
# #### To achieve this, a new category needs to be created with grouping of Donation amounts in 4-5 categories. Here I have considered 5, based on the distribution of the donation amount
# 
# #### The below chart depicts the distribution of Projects and Donors across five donation amount categories.
# 

# In[6]:


#-------------------------------------------------------------------------------------------------------------------------------

#Creating a derived column 'Donation Amount Category' to categorise the donations into 4 groups namely :
#Below 100, Between 100 and 300, Between 300 and 500, Above 500

#user defined function created for the above mentioned category creation
def Donation_Category (row):
    if row['Donation Amount'] <100 :
        return 'Below 100'
    if row['Donation Amount'] <300:
        return 'Between 100 and 300'
    if row['Donation Amount'] <500 :
        return 'Between 300 and 500'
    if row['Donation Amount'] >=500:
        return 'Above 500'
    else:
        return 'Invalid'

#calling the above user defined function for adding the new column to 'Donations' dataframe
Donations['Donation Amount Category'] = Donations.apply (lambda row: Donation_Category (row),axis=1)

#-------------------------------------------------------------------------------------------------------------------------------

#Creating dataframe to get the total no. of unique donors across different Donation Categories
DonorID_Donations = Donations.groupby('Donation Amount Category')['Donor ID'].nunique().reset_index()
#Renaming the columns in the above dataframe
DonorID_Donations.columns = ['Donation Amount Category', 'Total Donations']


#Creating dataframe to get the total no. of projects across different Donation Categories
ProjectID_Donations = Donations.groupby('Donation Amount Category')['Project ID'].count().reset_index()
#Renaming the columns in the above dataframe
ProjectID_Donations.columns = ['Donation Amount Category', 'Total Projects']


#-------------------------------------------------------------------------------------------------------------------------------

#Inorder to sort the categories in the below created graph, create an additional column to assign row number 
#to the 'Donation Amount Categories' 

def Donation_Category (row):
    if row['Donation Amount Category'] =='Below 100' :
        return 1
    if row['Donation Amount Category'] =='Between 100 and 300':
        return 2
    if row['Donation Amount Category'] =='Between 300 and 500' :
        return 3
    if row['Donation Amount Category'] =='Above 500':
        return 4
    else:
        return 0

#calling the above user defined function for adding the new column to 'Donations' dataframe
DonorID_Donations['Sort Order'] = DonorID_Donations.apply (lambda row: Donation_Category (row),axis=1)

#Creating a dataframe with sorted categories using the above dataframe, this is for the graph created below
DonorID_Donations_sorted = DonorID_Donations.sort_values(by='Sort Order', ascending=True)


#-------------------------------------------------------------------------------------------------------------------------------

#Inorder to sort the categories in the below created graph, create an additional column to assign row number 
#to the 'Donation Amount Categories'
def Donation_Category (row):
    if row['Donation Amount Category'] =='Below 100' :
        return 1
    if row['Donation Amount Category'] =='Between 100 and 300':
        return 2
    if row['Donation Amount Category'] =='Between 300 and 500' :
        return 3
    if row['Donation Amount Category'] =='Above 500':
        return 4
    else:
        return 0

#calling the above user defined function for adding the new column to 'Donations' dataframe
ProjectID_Donations['Sort Order'] = ProjectID_Donations.apply (lambda row: Donation_Category (row),axis=1)

#Creating a dataframe with sorted categories using the above dataframe, this is for the graph created below
ProjectID_Donations_sorted = ProjectID_Donations.sort_values(by='Sort Order', ascending=True)

#-------------------------------------------------------------------------------------------------------------------------------

#Below code is used to plot a graph with dual axis
#To show the total number of Projects and donors across different categories of donation amount

#Set the graph size
plt.rcParams['figure.figsize'] = [12,8]


#Paramter inputs for creating a decent dual axis bar + line graph
graph = DonorID_Donations_sorted[['Donation Amount Category', 'Total Donations']].plot(
    x='Donation Amount Category', markerfacecolor='beige',linestyle='-', color ='green', markersize=10 , marker='o', fontsize=13)
ProjectID_Donations_sorted[['Donation Amount Category', 'Total Projects']].plot(x='Donation Amount Category', kind='bar', ax=graph, color ='goldenrod')

#add labels to the y axis
plt.ylabel('No. of Projects / No. of Donors (refer Legends)')

plt.xticks(rotation=30)
#command to show the plot
plt.show()


# ## 2. Exploration of Projects.csv dataset

# ## 2.1 Loading the required packages

# In[7]:


from wordcloud import WordCloud
from datetime import date
from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


# ## 2.2 Data understanding is provided in this section
# #### The data provides information of each project i.e. Project type, Sub Project Type, Posted date, Status, Cost, Resource Category, Grade Level

# In[8]:


#ParserError: Error tokenizing data. C error: Expected 15 fields in line 10, saw 18
Projects = pd.read_csv('../input/Projects.csv', usecols=range(0, 15))
print("Top 3 rows:")
Projects.head(3)


# ## 2.3 Understanding which subjects are more frequent
# #### Grouping all projects by Project Subject Category

# In[9]:


Project_Sub_category = Projects.groupby(['Project Subject Subcategory Tree'])['Project ID'].count().reset_index()
Project_Sub_category.columns = [ 'Project Subject Subcategory','Total Projects']
Project_Sub_category_sorted = Project_Sub_category.sort_values(by='Total Projects', ascending=False)
print("Top 10 rows:")
Project_Sub_category_sorted.head(10)


# #### The visual below shows the WordCloud of all subjects

# In[10]:


Project_Sub_category_list  = Projects['Project Subject Subcategory Tree'].to_string()
def wordcloud_draw(data, color = 'black'):
    wordcloud = WordCloud(background_color=color,
                      width=2000,
                      height=2000
                     ).generate_from_text(data)
    plt.figure(1,figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    
wordcloud_draw(Project_Sub_category_list,'white')


# In[11]:


array_of_subjects= ['Mathematics', 'Literature', 'Literacy', 'Special Needs', 'Writing', 'Visual Art', 
                    'Technology', 'Computer', 'Engineering','Health','Wellness','Sports','Music', 'Dance',
                    'Care', 'Nutrition', 'Life Science', 'Foreign Language', 'Gym', 'History', 'Geography', 
                    'Civics', 'Economics', 'Community Service' , 'Social Science','ESL','Early Development',
                    'Performing Art','Environmental Science']


df_structure = {'Subject': [],'Total Projects': []}
Project_Subjects = pd.DataFrame(df_structure)

for i in range(len(array_of_subjects)):
    Project_Subjects.loc[i]= [array_of_subjects[i],
                              int(Project_Sub_category_sorted[Project_Sub_category_sorted['Project Subject Subcategory']
                                                              .str.contains(array_of_subjects[i],case=False)]['Total Projects'].sum())
                             ]
    
Project_Subjects['Total Projects']=Project_Subjects['Total Projects'].astype(int)


# #### Below graph depicts the total no. of projects for each subject

# In[12]:


#Set the graph size
plt.rcParams['figure.figsize'] = [14,11]
Project_Subjects.plot(kind='barh', x='Subject',color='teal',fontsize=13)


# ## 2.4 Understanding which Resource are more frequent
# #### Grouping all projects by Project Resource Category

# In[13]:


Project_Resource_category = Projects.groupby(['Project Resource Category'])['Project ID'].count().reset_index()
Project_Resource_category.columns = [ 'Project Resource Category','Total Projects']
Project_Resource_category_sorted = Project_Resource_category.sort_values(by='Total Projects', ascending=False)
print("Top 10 rows:")
Project_Resource_category_sorted.head(10)


# #### The visual below shows the WordCloud of all resources

# In[14]:


Project_Resource_category_list  = Projects['Project Resource Category'].to_string()

def wordcloud_draw(data, color = 'black'):
    wordcloud = WordCloud(background_color=color,
                      width=2000,
                      height=2000
                     ).generate_from_text(data)
    plt.figure(1,figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    
wordcloud_draw(Project_Resource_category_list,'white')


# #### Below graph depicts the total no. of projects for each resources

# In[16]:


array_of_resources= Projects['Project Resource Category'].unique()

df_structure = {'Resource': [],'Total Projects': []}
Project_Resources = pd.DataFrame(df_structure)

for i in range(len(array_of_resources)):
    Project_Resources.loc[i]= [array_of_resources[i],
                              int(Project_Resource_category_sorted[Project_Resource_category_sorted['Project Resource Category']==array_of_resources[i]]['Total Projects'].sum())
                              ]

Project_Resources['Total Projects']=Project_Resources['Total Projects'].astype(int)


# In[17]:


#Set the graph size
plt.rcParams['figure.figsize'] = [14,11]
Project_Resources.plot(kind='barh', x='Resource',color='goldenrod',fontsize=13)


# In[ ]:




