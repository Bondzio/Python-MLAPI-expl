#!/usr/bin/env python
# coding: utf-8

# Yesterday I read this notebook:  
# https://www.kaggle.com/paultimothymooney/how-to-explore-the-2019-kaggle-survey-data  
#   
# This notebook originally was written using R by @seshadrikolluri and adapted by @paultimothymooney for this competition.  
# There are less than 15 lines of code to plot all bar plots for all columns.
# 
# I've decided to implement it with similar functionality using Python - bar plots for all questions, and for readability show horizontal bar plots with top 20 values by frequency for each plot (of course it can be formatted further).  
#   
# And using method chaining, it can be implemented using only 2 lines of code, without any intermediate variables created.
# 
# For convenience, I've commented lines to describe separate steps.
#   
# Enjoy :)

# In[ ]:


import pandas as pd

(pd.read_csv('../input/kaggle-survey-2019/multiple_choice_responses.csv', 
             low_memory=False, skiprows=1) # read questions with multiple choices
   .filter(regex='^((?! - Text).)*$') # remove useless free text columns
   .filter(regex='^(?!Duration)') # remove duration column
   .melt(var_name='question', value_name='answer') # transform data from wide to long data format
   .dropna(subset=['answer']) # remove any lines that don't contain any answer
   .assign(question_type = lambda x: x['question'].str.split('-', 1) 
                                                  .str[0]
                                                  .str.split('(:|\?)')
                                                  .str[0]
                                                  .str.strip()) # get shared question part (for grouping further)
   .groupby('question_type')['answer'] # group by shared question parts (question type)
   .value_counts() # calculate counts of every value for specific question type
   .rename('count') # rename series
   .reset_index() # reset index for getting access to index fields for following steps
   .groupby('question_type', as_index=False) # group by question type for plotting
   .apply(lambda data: data.sort_values('count', ascending=True)
                           .tail(20)
                           .plot.barh(y='count', x='answer', 
                                      title=data['question_type'][0], 
                                      figsize=(10, 0.7 * len(data.tail(20))))) # plot data for each question type
);


# In[ ]:




