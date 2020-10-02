#!/usr/bin/env python
# coding: utf-8

# ## Intro: Accessing the Data
# 
# **This notebook includes some basic manipulations with the data set, and answers some of the questions about competitive BBQ you never knew you had.**
# 
# Reading the CSVs into Pandas is pretty simple, but requires a couple data-type conversions. After this cell, the data is ready to go.

# In[2]:


import numpy as np
import pandas as pd
import string
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# read in the competition data with some type conversions
df = pd.read_csv('../input/contest_data.csv',
                 dtype={'contest_key': np.int32},
                 parse_dates=['date'])

# read in the results data with some type conversions
chick_df = pd.read_csv('../input/results_chicken.csv',
                         dtype={'contest_key': np.int32, 'place': np.int32})
ribs_df = pd.read_csv('../input/results_ribs.csv',
                         dtype={'contest_key': np.int32, 'place': np.int32})
pork_df = pd.read_csv('../input/results_pork.csv',
                         dtype={'contest_key': np.int32, 'place': np.int32})
brisk_df = pd.read_csv('../input/results_brisket.csv',
                         dtype={'contest_key': np.int32, 'place': np.int32})
over_df = pd.read_csv('../input/results_overall.csv',
                         dtype={'contest_key': np.int32, 'place': np.int32})

# store category results in a dictionary for batch processing
cat_dict = {"chicken": chick_df, 
            "ribs": ribs_df, 
            "pork": pork_df, 
            "brisket": brisk_df, 
            "overall": over_df}

print("Ready to go!")


# ## The 'Contests' Dataframe
# 
# This dataframe describes the competitions. The features include date, name and location. Scoring and placing results are separate. See the data set description for a complete list of features. Here are some meta-data print outs for the contests dataframe.

# In[27]:


print("Columns: " + str(list(df.columns)) + "\n")
print("Number of rows " + str(df.shape[0]) + "\n")


# In[ ]:


df.head(5)


# ## Competition Results Dataframes
# 
# Competition results are stored across five dataframes; one for each standard category, and one for 'overall.' These dataframes share a common format: each row represents a team's results in a competition. The competition is identified by the foreign key column 'contest_key.' Here's some meta-data about the ribs results.

# In[5]:


print("Columns: " + str(list(ribs_df.columns)) + "\n")
print("Number of rows " + str(ribs_df.shape[0]) + "\n")
print("First 5 rows: \n")
print("Average number of ribs submissions per tournament: " + str(int(ribs_df.shape[0] / df.shape[0])))


# In[ ]:


ribs_df.head(5)


# ## Linking Competitions and Their Results: Filtering by State
# 
# The following cell uses the contest and chicken dataframes to produce summary statistics for chicken scores only in Tennessee.

# In[23]:


# function to aggregate all the scores for a given state within a given category
def get_state_cat_results(state, category):
    keys = df[df['state'] == state]['contest_key']
    cat_df = cat_dict[category].copy()
    cat_df = cat_df[cat_df['contest_key'].isin(keys)]
    return cat_df


# In[ ]:


tn_chicken = get_state_cat_results("TN", "chicken")
tn_chicken_scores = tn_chicken['score']
print("Tennessee chicken score stats:")
# plot a histogram
plt.figure()
bin_count = int(tn_chicken_scores.max() / 10)
_ = tn_chicken_scores.hist(bins=bin_count)
tn_chicken_scores.describe()


# ## Filtering by Year and Plotting CDFs
# 
# Filtering on states creates some interesting angles, and I'll get back to it shortly. First, here's a similar demo that subsets year-by-year rather than state-by-state. Cumulative distribution function plots help us visually compare distributions.

# In[10]:


# function to aggregate all the scores for a given year within a given category
def get_year_cat_results(year, category):
    keys = df[df['date'].dt.year == year]['contest_key']
    cat_df = cat_dict[category].copy()
    cat_df = cat_df[cat_df['contest_key'].isin(keys)]
    return cat_df
    
# function to plot each subset's cumulative distribution function
def plot_year_cdfs(years, category, lower_score_bound=0):
    plt.figure()
    for year in years:
        # subset the results data
        df = get_year_cat_results(year, category)
        data = df['score']
        # filter low scores
        data = data[data >= lower_score_bound]
        # plot CDF
        x = np.sort(data)
        y = np.arange(1, data.size + 1) / float(x.size)
        plt.plot(x, y)
    # label plot
    plt.title("CDF of Yearly " + category.title() + " Scores")
    plt.xlabel("scores")
    plt.ylabel("probability")
    plt.legend(years, loc='best')


# In[ ]:


years = [2014, 2015, 2016]
category = "chicken"
plot_year_cdfs(years, category)
plot_year_cdfs(years, category, lower_score_bound=120)


# These year-over-year score sets are almost identical. A slight trend towards higher scores may not be significant, but could be the result of competitive refinement or score inflation.
# 
# ## Comparing Score Distributions Across States
# 
# I can compare score distributions across states by putting together the previous two cells with some extra code. This code only shows the five states with the most competitions. Try changing top_n or interjecting a custom list.

# In[11]:


# Taking the top n states by number of contests:
top_n = 5
counts = df['state'].value_counts()
states = list(counts.head(top_n).index)
# states = ['MA', 'NY', 'NH']

print(states)


# In[ ]:


# plot each subset's cumulative distribution function
def plot_state_cdfs(states, category, lower_score_bound=0):
    plt.figure()
    for state in states:
        # subset the results data
        df = get_state_cat_results(state, category)
        data = df['score']
        # filter low scores
        data = data[data >= lower_score_bound]
        # plot CDF
        x = np.sort(data)
        y = np.arange(1, data.size + 1) / float(x.size)
        plt.plot(x, y)
    # label plot
    plt.title("CDF of State " + category.title() + " Scores")
    plt.xlabel("scores")
    plt.ylabel("probability")
    plt.legend(states, loc='best')

plot_state_cdfs(states, "chicken", lower_score_bound=120)
plot_state_cdfs(states, "ribs", lower_score_bound=120)
plot_state_cdfs(states, "pork", lower_score_bound=120)
plot_state_cdfs(states, "brisket", lower_score_bound=120)


# Tennessee and Georgia are out in front by a solid margin on these plots, while Missouri, Kansas and California are tied up. Again, these differences could indicate better competition BBQ, more lenient judging, regional tastes, or any number of confounding variables.
# 
# ## Show Me the Money
# 
# That's enough of scores for now. Let's look at the prize money. Where is the money? To answer this question, I'm going to capture the total prize money, and the average prizes state-by-state. I'll adjust average prize to only take prized competitions into account.

# In[12]:


# get a list of the states in the data set (AK, HI, and ND are missing)
states = list(df['state'].unique())
# create a template row for the state stats data frame
row_temp = {"total_prize": "NA", 
            "avg_prize": "NA",
            "count": "NA",
            "count_prized": "NA"}
# create a dataframe to hold the results
prize_df = pd.DataFrame(index=states, columns=row_temp.keys())

# iterate the state subsets to calculate total, average and percentage prized
for cur_state in states:
    row_new = row_temp.copy()
    prizes = df[df['state'] == cur_state]['prize']
    count_total = prizes.shape[0]
    # remove non-prized competitions
    prizes = prizes[prizes > 0]
    count_prized = prizes.shape[0]
    # calculate measures
    row_new['total_prize'] = prizes.sum()
    row_new['avg_prize'] = prizes.mean()
    row_new['count'] = count_total
    row_new['count_prized'] = count_prized
    # insert row into the results df
    prize_df.loc[cur_state] = row_new
prize_df['percent_prized'] = prize_df['count_prized'] / prize_df['count']

# function to plot measures in the prize dataframe
def prizeplot(prize_df, col, n, title, y_units):
    plt.figure()
    prize_df = prize_df.sort_values(by=col, ascending=False)
    prize_df = prize_df.head(n)
    prize_df[col].plot.bar()
    plt.title(title.title())
    plt.xlabel('State Abbrev.')
    plt.ylabel(y_units.title())

print("Total prize across the dataset: $" + str(df['prize'].sum()))


# In[ ]:


n = 10
prizeplot(prize_df, 'count', n, 'competition count', 'competitions')
prizeplot(prize_df, 'total_prize', n, 'total prizing', 'dollars')
prizeplot(prize_df, 'avg_prize', n, 'average prizing', 'dollars')


# Looks like Missouri (home of Kansas City) has the highest Total prize money at just over one million dollars accumulated   over 125 prized competitions. Georgia and California also make the nine-figures club. Nevada has the highest average prize payout at 25,315 dollars, and Arkansas has a similarly high average payout surprisingly. The total payout across the data set is 14,111,822 dollars. That's 14 million in BBQ winnings in the last four years.
# 
# ## The Best Teams
# 
# Best 'overall' is difficult because the maximum overall score varies in non-standard tournaments. I'll split things up by category, and define the best teams in a category as the ones with the highest average scores. I'll implement a minimum number of appearances as a prerequisite for consideration.
# 
# **Note:** This cell can take ~30 seconds to run.

# In[15]:


# define a string series regularizing function
def tame_names(str_series):
    str_series = str_series.str.translate(str.maketrans('', '', string.punctuation))
    str_series = str_series.str.lower()
    str_series = str_series.str.strip()
    return str_series

# standardize team names for use as comparators
for cat in cat_dict.keys():
    cat_dict[cat]['std_name'] = tame_names(cat_dict[cat]['team_name'])

# define a function to calculate highest average score for teams with 
# more than some minimum of appearences
def extract_best(category, min_appearances):
    cat_df = cat_dict[category]
    # filter the results table to only include teams that satisfy min_appearences
    team_apps = cat_df['std_name'].value_counts()
    teams = list(team_apps[team_apps >= min_appearances].index)
    cat_df = cat_df[cat_df['std_name'].isin(teams)]
    # iterate the candidate teams and calculate mean scores
    cand_teams = list(cat_df['std_name'].unique())
    row_temp = {'appearances': 0, 'score_avg': 0, 'score_std': 0}
    best_df = pd.DataFrame(index=cand_teams, columns=row_temp.keys())
    for team in list(cat_df['std_name'].unique()):
        row_new = row_temp.copy()
        scores = cat_df[cat_df['std_name'] == team]['score']
        row_new['appearances'] = scores.shape[0]
        row_new['score_avg'] = scores.mean()
        row_new['score_std'] = scores.std()
        best_df.loc[team] = row_new
    best_df = best_df.sort_values(by="score_avg", ascending=False)
    return best_df

min_apps = 10
chick_best = extract_best("chicken", min_apps)
ribs_best = extract_best("ribs", min_apps)
pork_best = extract_best("pork", min_apps)
brisk_best = extract_best("brisket", min_apps)

print("Finished computing.")


# In[ ]:


print("Top 10 teams in Chicken:")
chick_best.head(10)


# In[ ]:


print("Top 10 teams in Ribs:")
ribs_best.head(10)


# In[ ]:


print("Top 10 teams in Pork:")
pork_best.head(10)


# In[ ]:


print("Top 10 teams in Brisket:")
brisk_best.head(10)

