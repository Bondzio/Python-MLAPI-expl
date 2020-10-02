#!/usr/bin/env python
# coding: utf-8

# ## Inspirations For Your Kaggle Story
# ![](https://cdn.pixabay.com/photo/2019/05/14/21/50/storytelling-4203628_1280.jpg)
# 
# Kaggle is an amazing community, and it always stood up for learning and sharing more than anything. I have been on Kaggle for some time, but only have been active very recently. In this competition, we get to dig into the Kaggle Survey dataset, that some of us might have participated recently. This is a different kind of competition, where you can do analysis on the data (rather than machine learning) and tell a story. 
# 
# ### Instead of keeping my notebook private, I thought about spending my time to create a notebook with inspiration for many stories. I hope the community shows some love back to me by upvoting my Kernel.

# ## Import & Data Description

# In[ ]:


# imports
# data wranglers 
import pandas as pd 
# for visualizing with plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# for frequent pattern mining
from mlxtend.frequent_patterns import fpgrowth


# In[ ]:


# load all main data into dataframe
mcq_resp_df = pd.read_csv('/kaggle/input/kaggle-survey-2019/multiple_choice_responses.csv', low_memory=False)
questions_df = pd.read_csv('/kaggle/input/kaggle-survey-2019/questions_only.csv')
schema_df = pd.read_csv('/kaggle/input/kaggle-survey-2019/survey_schema.csv')
other_resp_df = pd.read_csv('/kaggle/input/kaggle-survey-2019/other_text_responses.csv')


# In[ ]:


# questions are basically in questions_df. To make life easier I will print out all the questions here for reference.
for q in questions_df.columns:
    print(q +':'+ questions_df[q][0])


# ## Location & Gender
# 
# In the response field we have the question Q3 (In which country do you currently reside?) and Q2 (What is your gender?). First, I will look into the geographical distribution of the response. Then I want to look at the ratio of male to female in the response of our survey. 

# In[ ]:


# get response by country for different gender types
resp_by_country = mcq_resp_df[1:].groupby(['Q3', 'Q2']).count()['Q1'].reset_index().pivot(index='Q3', columns='Q2', values='Q1')
resp_by_country = resp_by_country.fillna(0).reset_index()
resp_by_country['Total Response'] = resp_by_country['Female'] + resp_by_country['Male'] + resp_by_country['Prefer not to say'] + resp_by_country['Prefer to self-describe']


# In[ ]:


# get male to female ratio
resp_by_country['Male To Female Ratio'] = resp_by_country['Male'] / resp_by_country['Female'] 


# In[ ]:


# plot the distribution of the response by country on a choropleth map

fig = px.choropleth(resp_by_country, locations="Q3", locationmode='country names',
                    color="Total Response", # lifeExp is a column of gapminder
                    hover_name="Q3", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Kaggle ML & DS Survey Response Distribution" )

fig.show()


# In[ ]:


# plot the distribution of the male to female response by country on a choropleth map

fig = px.choropleth(resp_by_country, locations="Q3", locationmode='country names',
                    color="Male To Female Ratio", # lifeExp is a column of gapminder
                    hover_name="Q3", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title='Kaggle ML & DS Survey Male To Female Ratio')

fig.show()


# #### Inspirations for your story: 
# 
# * **India vs Rest of The World:** By far the Kaggle community is big in India (or they responded very well to the survey). You can look into which countries are well connected to Kaggle, and which countries are not so well connected to Kaggle. I did the plot without normalizing the response by the total number population or members. Perhaps, more interesting insights would pop out if one did do that. For example, we know India and China almost has the same number of population. However, Kaggle community in India is far greater than Kaggle community in China.
# 
# * **Male to Female Ratio:** The gender ratio in Kaggle community (according to this survey) looks a little sad. If you look at the top five countries with very low male to female respondant ratio, it is Norway, Bangladesh, Denmark, Belgium, and Japan. The odd thing is, Bangladesh is the only developing country on that list! Furthermore, if you look at the top 5 countries in terms of balanced male to female Kaggler ratio, you would find: Tunasia, Phillippines, Iran, Malaysia, and Kenya. All of them are developing countries, where women face many challenges to obtain basic education. This in my humble opinion could make for a great story!

# ## Age Group & Gender
# 
# To further go into the gender gap in Kaggle response, you can also further dive into the age groups. In this section, we will take a look at the distribution of age and also see if anything interesting is in the ratio of male to female kaggler per age group.

# In[ ]:


# count responds per age group and gender type
age_and_gender = mcq_resp_df[1:].groupby(['Q1', 'Q2']).count()['Q3'].reset_index().pivot(index='Q1', columns='Q2', values='Q3')
age_and_gender = age_and_gender.fillna(0).reset_index()
age_and_gender['Total Response'] = age_and_gender['Female'] + age_and_gender['Male'] + age_and_gender['Prefer not to say'] + age_and_gender['Prefer to self-describe']
age_and_gender['Male To Female Ratio'] = age_and_gender['Male'] / age_and_gender['Female']


# In[ ]:


# make a scatter plot for male and female responses per age group, and also the ratio
fig = make_subplots(rows=1, cols=2)

fig.add_trace(go.Scatter(x=age_and_gender['Q1'], y=age_and_gender['Male'], mode='markers', name='Male'), row=1, col=1)
fig.add_trace( go.Scatter(x=age_and_gender['Q1'], y=age_and_gender['Female'], mode='markers', name='Female'), row=1, col=1)
fig.add_trace( go.Scatter(x=age_and_gender['Q1'], y=age_and_gender['Male To Female Ratio'], mode='markers', name='Male To Female Ratio'), row=1, col=2)

fig.update_layout(height=600, width=800, title_text="Kaggle Survey Response by Age Group and Gender")
fig.show()


# #### Inspirations for your story: 
# 
# * **Elderly Population:** Based on the subset of data we have on the Kaggle survey, we can assume that most people that are active on Kaggle are young. I guess it makes sense, as perhaps as most people want to learn (new things) and code less as they become older. In your story, you could further concencrate on for the older age group that did responde (50+) and see what more could be done to make other people from that age group engage more with Kaggle.
# * **Male To Female Ratio For Elderly:** On another note, the male to female ratio becomes worse as the age of the responder increases. Could this be because women have to take more responsibilities as they become older? 

# ## Salary and Kaggle Participation 
# 
# In Q10, the survey asks to indicate in which range of salary the Kaggler belongs. In this section, I want to use this figure to get an understanding if people who earn less salary (in context of the country) are more likely to participate in Kaggle. To do this, basically I will look into three countires with relatively less income (India, Russia, and China) and three countries with relatively higher income (USA, Canada, Germany). 
# 
# To do this, first I will convert the the salary data from categorical to numeric. This will allow me to do histogram with ease. I will take the middle of the range the Kaggler have indicated as an estimated salary. Furthermore, in order to make the graph more intuitive, I will only consider up to the 95th percentile of salary data per country. 

# In[ ]:


# a function to convert range of salary to a middle figure
def conv_salary_to_num(salary_cat):
    
    if '> $500,000' in salary_cat:
        return 500000.0
    
    salary_cat = salary_cat.replace('$','')
    low = float(salary_cat.split('-')[0].replace(',',''))
    high = float(salary_cat.split('-')[1].replace(',',''))
    
    return low + ((high - low) / 2)


# In[ ]:


# keep gender, country, and salary range
salary_est_df = mcq_resp_df[1:][['Q2','Q3','Q10']].dropna()
# convert salary range to an estimated salary
salary_est_df['salary_est'] = salary_est_df.apply(lambda row: conv_salary_to_num(row['Q10']), axis=1)


# In[ ]:


# a function to get salary array for a given country up to an indicated quantile
def get_quantile_salary_est(salary_est_df, country, quantile):

    quantile_salary_est_df = salary_est_df[salary_est_df['Q3']==country]
    quantile_salary_est_df = quantile_salary_est_df[quantile_salary_est_df.salary_est < quantile_salary_est_df.salary_est.quantile(quantile)]
    return quantile_salary_est_df['salary_est']


# In[ ]:


# histogram of our salary for India, Russia, China, USA, Canada, and Germany
fig = make_subplots(rows=2, cols=3, subplot_titles=("India", "Russia", "China", "USA", "Canada", "Germany"))

fig.add_trace(go.Histogram(x=get_quantile_salary_est(salary_est_df, 'India', 0.95)), row=1, col=1)
fig.add_trace(go.Histogram(x=get_quantile_salary_est(salary_est_df, 'Russia', 0.95)), row=1, col=2)
fig.add_trace(go.Histogram(x=get_quantile_salary_est(salary_est_df, 'China', 0.95)), row=1, col=3)

fig.add_trace(go.Histogram(x=get_quantile_salary_est(salary_est_df, 'United States of America', 0.95)), row=2, col=1)
fig.add_trace(go.Histogram(x=get_quantile_salary_est(salary_est_df, 'Canada', 0.95)), row=2, col=2)
fig.add_trace(go.Histogram(x=get_quantile_salary_est(salary_est_df, 'Germany', 0.95)), row=2, col=3)

fig.update_layout(height=600, width=800, title_text="Kaggle Survey Response by Salary and Country", showlegend=False)
fig.show()


# #### Inspirations for your story: 
# 
# * **Kaggler's at low & high income countries:** In low income countires, more Kaggler's have a starter or student salary. For Kaggler's who are earning a decent amount, the number of participation is very little. On the contrary, on the higher income countries, Kaggler with average and above average salary seems to participate more. Could this be because in lower income countries stress from work is very high? One could really dig more deep into this!

# ## Thirst For Knowledge
# One thing I know from my experience of being on Kaggle community is that people here loves to learn. Why else would you be on Kaggle right? Question 12 asks regarding the respondent about favorite blog to gain more knowledge. Let's analyze this question to see if Kaggler's thirst for knowledge also extends beyond Kaggle. 
# 
# Since this is a question where the respondent is allowed to select more than one choice, the data is given to us in parts. So before we can analyze it we need to process it a little bit to make our life easier. Then we will do two calculation and visualization. First, the simple one is to do a value count of reader per knowledge source and do a pie chart to show which knowledge sources dominate. Second, I will do a frequent pattern mining to extract combination of different choices that are popular amongst our Kagglers. If you want to read more about FP Mining, you can [read this awesome article](https://medium.com/@ciortanmadalina/an-introduction-to-frequent-pattern-mining-research-564f239548e).

# In[ ]:


# Get all of the column names (they are given in parts)
q12_col_names = [Q12 for Q12 in list(mcq_resp_df[1:].columns) if 'Q12' in Q12]
# remove the last one as it is the open ended other question living in another file
q12_col_names = q12_col_names[:-1]


# In[ ]:


# select a subset of data for analysis
q12_resp_df = mcq_resp_df[1:][q12_col_names]


# In[ ]:


# the actual sources are in the content of the dataframe and not the header
# here we collect the name per column, and then format it and replace it as the header
sources = []

for q12_col_name in q12_col_names:
    sources.append([val for val in mcq_resp_df[1:][q12_col_name].unique() if (type(val)==str)][0])
    
sources = [source.split('(')[0].rstrip() for source in sources]

q12_resp_df.columns = sources  


# In[ ]:


# do a count per knowledge source
q12_resp_df_count = q12_resp_df.count()


# In[ ]:


# change the dataframe to a format fpgrowth algorithm library likes
q12_resp_df = q12_resp_df.fillna(0).applymap(lambda x: True if type(x)==str else False)
# get frequent pattern
q12_fp_df = fpgrowth(q12_resp_df, min_support=0.01, use_colnames=True).sort_values(by='support', ascending=False)


# In[ ]:


# calculate items per row
q12_fp_df['items'] = q12_fp_df['itemsets'].apply(lambda x: len(x))
# format itemsets into nice strings
q12_fp_df['itemsets'] = q12_fp_df['itemsets'].apply(lambda x: ', '.join(x))
# we are interested in more than one item and we will just consider the top 10
q12_fp_df = q12_fp_df[q12_fp_df['items']>1][:10]


# In[ ]:


# make two plots, one for frequent pattern and another one pie chart
fig = make_subplots(rows=1, cols=2,subplot_titles=("Frequent Pattern", "Pie Chart"), specs=[[{'type':'xy'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=q12_resp_df_count.index, values=q12_resp_df_count.values), 1, 2)
fig.add_trace(go.Bar(x=q12_fp_df.itemsets, y=q12_fp_df.support, ), 1, 1)


# #### Inspirations for your story: 
# 
# * **Kaggle is also a source for Knowledge:** Kagglers are not on Kaggle just to use the infrastructure for free, they also use Kaggle as a source of learning more about data science. This is visible on both of the graphs. On the FP graph, we can see that people a large percentage of the population combines Kaggle with other mediums like Blog, YouTube and etc.
# * **Kaggler's are well read:** Kagglers seems to gather their knowledge from a wide variety of sources outside of Kaggle as well. The pie graph is somewhat well distributed, with heaviest weight on Kaggle, Blogs, YouTube, and Journals. These sources are often read in tandem, as shown in the FP graph.
# 
# Of course these two points can be further zoomed into per country, gender, and age group to see how the source for knowledge changes for different demographics.

# ## Experience & ML Techniques
# 
# There are a lot of technology and machine learning affinity related questions between question 24 to question 34. In this section, I want to explore how experience of working in machine learning has anything to do with the techniques and technologies people adopt. Furthermore, I want to understand some general trends in ML technologies and techniques vs experience with ML.

# In[ ]:


def get_col_info(question_num, df):
    '''
    return column names and answers for columns that are given in multiple parts
    question_name
    
    Args:
      question_num (str): question number of the question, i.e. Q23
      df (pandas dataframe): dataframe that contains all the parts of the question number
      
    Returns:
      tuple: returns a tuple of list, containing column names and the answers
    
    '''
    # loop over all the column names in the dataframe and create a list that 
    # contains the question number in the column name
    col_names = [q for q in list(df.columns) if question_num in q]
    # pop the OTHER column, as this links to open ended text questions
    col_names = [q for q in col_names if 'OTHER' not in q]
    
    # create a list where all the answers will be stored
    answers = []

    # go over the column names and get the unique value of this column
    # this is the answer people have picked for this part of the question
    for col_name in col_names:
        answers.append([val for val in df[col_name].unique() if (type(val)==str)][0])
    
    # remove the explanation in bracket
    answers = [answer.split('(')[0].strip() for answer in answers]
    
    # return column names and answers
    return (col_names, answers)


# In[ ]:


def get_count_for_heatmap(df, y_col, y_list, x_list):
    
    '''
    returns a tuple containing x, y, and z value required to do a heatmap given the response 
    dataframe. for each y value, the percentage of x value present is calculated and returned, 
    along with the original x and y variable list.
    
    Args:
      df (pandas dataframe): dataframe that contains all the parts of the question number
      y_col (str): name of the column for which we are interested to get count
      y_list (list): list containing different values which we consider for our y column
      x_list (list): list of columns for which we do the count per y value
      
    Returns:
      tuple: returns a tuple of list, containing x, y, and percentage of x per y needed 
      to do a heatmap
    '''
    
    # a list to contain the x count for each y values
    y_count_list = []
    # loop over all the y values
    for y in y_list:
        # a list to contain all the x values for a given y
        x_count_list = []
        # count total number of samples (used for normalization)
        x_total = len(df[df[y_col] == y])
        # loop over the x value and count it
        for x in x_list:
            count = df[df[y_col]==y][x].value_counts()[0]
            # divide x value by total number of x samples present
            x_count_list.append((count / x_total) * 100)
        # append all x percentage count for a given y
        y_count_list.append(x_count_list)
    return (x_list, y_list, y_count_list)


# In[ ]:


# question 23 asks how many years have you used machine learning methods.
# take this column and remove all the samples where this is null
q23_resp_df = mcq_resp_df[1:][~ mcq_resp_df[1:]['Q23'].isnull()]


# In[ ]:


# re order the list of values for q23 so it is chronological in heatmap
exp_list = q23_resp_df['Q23'].unique()
exp_list = exp_list[2], exp_list[0], exp_list[1], exp_list[4], exp_list[5], exp_list[6], exp_list[3], exp_list[7]


# First, I want to look at question 24 and 28. Question 24 asks regarding the ML algorithms and question 28 asks regarding the ML frameworks the respondent uses. Here I will do two heatmaps to see how the machine learning algorithm and framework picked up differs accross different ML experience groups. 

# In[ ]:


fig = make_subplots(rows=1, cols=2,subplot_titles=("ML Algorithm", "ML Framework"), specs=[[{'type':'heatmap'}, {'type':'heatmap'}]])

# get column names and answers for question 25
cols_24, answers_24 = get_col_info('Q24', mcq_resp_df[1:])
x_24, y_24, z_24 = get_count_for_heatmap(q23_resp_df, 'Q23', exp_list, cols_24)

# get column names and answers for question 28
cols_28, answers_28 = get_col_info('Q28', mcq_resp_df[1:])
x_28, y_28, z_28 = get_count_for_heatmap(q23_resp_df, 'Q23', exp_list, cols_28)

fig.add_trace(go.Heatmap(z=z_24, y=y_24, x=answers_24, showscale=False), 1, 1)
fig.add_trace(go.Heatmap(z=z_28, y=y_28, x=answers_28, showscale=False), 1, 2)

fig.show()


# Second, I want to use Question 25 and Question 33 to see the different categories of ML tools and automated ML tools being used accross different ML experience groups. 

# In[ ]:


fig = make_subplots(rows=1, cols=2,subplot_titles=("ML Tools", "Automated ML Tools"), specs=[[{'type':'heatmap'}, {'type':'heatmap'}]])

# get column names and answers for question 25
cols_25, answers_25 = get_col_info('Q25', mcq_resp_df[1:])
x_25, y_25, z_25 = get_count_for_heatmap(q23_resp_df, 'Q23', exp_list, cols_25)

# get column names and answers for question 28
cols_33, answers_33 = get_col_info('Q33', mcq_resp_df[1:])
x_33, y_33, z_33 = get_count_for_heatmap(q23_resp_df, 'Q23', exp_list, cols_33)

fig.add_trace(go.Heatmap(z=z_25, y=y_25, x=answers_25, showscale=False), 1, 1)
fig.add_trace(go.Heatmap(z=z_33, y=y_33, x=answers_33, showscale=False), 1, 2)
 
fig.show()


# In[ ]:


fig = make_subplots(rows=1, cols=2,subplot_titles=("Cloud Platforms", "Big Data - SaaS"), specs=[[{'type':'heatmap'}, {'type':'heatmap'}]])

# get column names and answers for question 25
cols_30, answers_30 = get_col_info('Q30', mcq_resp_df[1:])
x_30, y_30, z_30 = get_count_for_heatmap(q23_resp_df, 'Q23', exp_list, cols_30)

# get column names and answers for question 28
cols_31, answers_31 = get_col_info('Q31', mcq_resp_df[1:])
x_31, y_31, z_31 = get_count_for_heatmap(q23_resp_df, 'Q23', exp_list, cols_31)

fig.add_trace(go.Heatmap(z=z_30, y=y_30, x=answers_30, showscale=False), 1, 1)
fig.add_trace(go.Heatmap(z=z_31, y=y_31, x=answers_31, showscale=False), 1, 2)

fig.show()


# #### Inspirations
# 
# Coming Soon!

# #### If you like my work please upvote this Kernel. This encourages or motivates people like me, who contributes to Kaggle on their own time with the intention to share knowledge, to continue the effort. Furthermore, if I made a mistake or can do something more, please leave a comment in the comments section to help me out. Many thanks in advance!
