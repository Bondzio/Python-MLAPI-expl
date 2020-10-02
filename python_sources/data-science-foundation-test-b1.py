#!/usr/bin/env python
# coding: utf-8

# # Instructions: Read carefully before starting the test 
# ### This test is based on Data Science Foundation topics and exercises covered so far. It is an open book, open notes, open internet test. So feel free to refer to any sources. 
# ## Total Marks: 50
# ## Minimum  qualifying marks : 30
# ## Total Questions: 13
# ## Total Duration of test: 1 hour 15 min
# ## Submission instructions
# #### Ensure that your session is live. You draft code will be saved automatically. Commit your code when half way through the test to ensure there are no bugs and you don't face any huddle at last minute. Once done, commit your code. Now go to Kaggle Kernal page and click on the tab "Your Work". The code that you commited will be visible there. Click on the code. From top right corner, click on the three dots and click download code. Now share the copy of this code over email to Chandan.
# 
# ### All submissions must be received before 11.50AM. Any submission received later will not be evaluated.
# 
# ### The marks will be decided on the basis of following:
# 1. Accuracy of the code
# 1. Code length to get the results. Least is better
# 1. Usage of comments and good indenting for better readability
# 1. Authenticity of the code. It's ok to refer to the internet, however not ok to copy the code as is
# 
# ### Input data files are available in the "../input/" directory. Refer to the data files to answer questions. No external data is required for this test.
# 
# ### Python Packages
# You can choose to install custom package, if required using below command:
# 
# !pip install packagename

# ## Start

# ## Q1: Write a custom function to return if a given day is a holiday or not. Use below list of holidays to check against. (2 marks)

# In[ ]:


holidays_in_March =[5,10,21,26,30]

#Complete below function
def check_holiday(list_):
    print("enter the date")
    date_ = int(input())
    if date_ in list_:
        return "Given date is  holiday"
    else:
        return "Mention date is a not a holiday"
    
    
check_holiday(holidays_in_March)


# ## Q2: Write a custom function to create an array of Multiplication Table from 2 to user defined value. (3 marks)

# In[ ]:


# If the use passes the value 4, the output should be in below format:
# [[2,4,6,8,10,12,14,16,18,20],[3,6,9,12,15,18,21,24,27,30],[4,8,12,16,20,24,28,32,36,40]]

#Complete below function
def table():
    user_defined_value = int(input())
    table = []
    for i in user_
    for i in range(0,(11)*user_defined_value,user_defined_value):
        table_ = []
        table_.append(i)
        table.append(table_)
    return table
        
'''        
for i in range(0,11*4,4):
    print(i)
'''
table()


# ## Q3: Write a list comprehension to show days of the month that are even using below list. (2 marks)  

# In[ ]:


# Use this list as input
days = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,16,18,19,20,21,22,23,24,25,25,27,28,29,30]
even_days  = [x for x in days if x%2==0 ]


even_days


# ## Q4: Create a 4D array of dimension 4, 4, 5, 10. Fill all values with #. (3 marks)  

# In[ ]:


#Your code here
import numpy as np
output_array = np.full((4,4,5,10),'#')
output_array


# ## Q5: Write a program to return the positional value of every character as a list from A-Z alphabet.  Use zero to show spaces. (8 marks)
# 
# ### String to use:  "The quick brown fox jumps over the lazy little dog"
# #### Expected output
# #### [20,8,5,0,17,21,9,3...................0,4,15,7]
# 

# In[ ]:


#Your code here
string = "The quick brown fox jumps over the lazy little dog"

alphabet = list(' abcdefghijklmnopqrstuvwxyz')
dict_ = {}
for counter, value in enumerate(alphabet):
    dict_[value] = counter

exp_output = []
for x in string.lower():
    exp_output.append(dict_[x])
exp_output


# 
# ## Q6 Similar to question number 2, write a function to return the values as dictionary where respective Multiplication table is a key.  (4 marks)

# In[ ]:


# If the use passes the value 4, the output should be in below format:
# {2:[2,4,6,8,10,12,14,16,18,20],3:[3,6,9,12,15,18,21,24,27,30],4:[4,8,12,16,20,24,28,32,36,40]}

#Your code here


# ## Q7 Read the Canadian data as Pandas DataFrame. Assign date as index and show first 10 rows of 4th, 5th and 19th column as a DataFrame. (3 marks)

# In[ ]:


#Your code here
import pandas as pd
canadian_da = pd.read_excel('../input/canada.xlsx')
canadian_da.set_index('date', inplace=True)
canadian_da


# ## Q8 Find out the date when Total number of influenza positive was maximum in Canada. (2 Marks)

# In[ ]:


#Your code here
date_ = canadian_da.loc[canadian_da['Total number of influenza positive viruses'] == canadian_da['Total number of influenza positive viruses'].max()]
date_.index


# ## Q9 Create a dataframe to show the average number of influenza positive cases for respective months in each year in descending order. (5 marks)
# 
#                   Total number of influenza positive viruses
#     year month                                            
#     2019 1                                           11046
#          2                                            2037
#     2018 2                                           18133
#          1                                           17611
#          3                                           11247
#          12                                          10191
#          4                                            5077
#          11                                           2724
#          5                                             765
#          10                                            466
#          6                                             112
#          9                                              70
#          7                                              51
#          8                                              35
#     2017 1                                           14004

# In[ ]:


#Your code here
df1 = canadian_da[['year', 'month', 'Total number of influenza positive viruses']]
df1 = df1.groupby(['year', 'month']) .mean()
df1.sort_values(by = ['year','Total number of influenza positive viruses'], ascending = False)
#canadian_da.columns


# ## Q10 Create two subplots (line) of 'Total number of influenza positive' and 'influenza: (Canada)'. (3 marks)

# In[ ]:


import matplotlib.pyplot as plt
#Your code here


# ## Q11  Find out which variables are closely correlated with 'Total number of influenza positive' by creating a correlation heatmap from below link for Canada dataset. Use the first 25 columns for better visibility. Each block should show the correlation value. (5 marks)
# 
# [Correlation Heatmap](https://seaborn.pydata.org/examples/many_pairwise_correlations.html)

# In[ ]:


#Your code here


# ## Q12  Using tables 'post_answers' and 'users', find out how many answers were submitted from India. (5 marks)
# 
#                                 loc        ans_submitted
#     0                           India         363527
#     1                Bangalore, India         164905
#     2     Bangalore, Karnataka, India         114064
#     3        Pune, Maharashtra, India          86423
#     4       Ahmedabad, Gujarat, India          79479
#     5                  Chennai, India          68915

# In[ ]:


import bq_helper

# create a helper object for this dataset
stack = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                     dataset_name="stackoverflow")
stack.head('users',num_rows=50)

# Your code here
ans1 = """
"""
#Uncomment below
# ans_results = stack.query_to_pandas_safe(ans1, max_gb_scanned=25) # this query reads a lot of data
# print(users_results.head(14))


# ## Q13 Using tables posts_answers and users, find out the user that gave the maximum answers in 2017. Your table should show following columns 'name' and 'ans_submitted'. If you query is right, it will take few seconds to pull the results. (5 marks)
# 
#           name                         ans_submitted
#         0    Gordon Linoff            8744
#         1    jezrael                  4757
#         2    akrun                    3525
#         3    Alex                     2931
#         4    Tim Biegeleisen          2889

# In[ ]:


# Your code here


# ## End

# 
