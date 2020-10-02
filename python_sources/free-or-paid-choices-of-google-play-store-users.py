#!/usr/bin/env python
# coding: utf-8

# # Free or Paid, Choices of Google Play Store Users
# by Chen Qiao (cqiaohku@gmail.com)
# 
# ## Background
# 
# Users download apps for various usage purposes. Given that paid service is usually better at offering pleasant experience, and that free apps are more accesible to everyone, what are the user opinions towards these apps? 
# 
# More specifically, the following questions are of interest:
# - How do the app ratings differ between paid and free apps in general?
# - How are the differences distributed across different app categories?
# - Are there any categories where the differences are statistically significant?
# 
# To expore answers to the above questions, I narrawed the context to Google Play Store and conducted data analysis on the Kaggle dataset [`Google Play Store`](https://www.kaggle.com/lava18/google-play-store-apps/home),
# 
# ## Acknowledgement
# I would like to thank Google Play Store and [Lavanya Gupta](https://www.kaggle.com/lava18) for offering the wonderful dataset.
# 

# In[ ]:


# import packages

import pandas as pd
import seaborn as sns
import numpy as np
import re
from scipy.stats import mannwhitneyu
from matplotlib import pyplot as plt


# In[ ]:


# Read dataframe and display data
df = pd.read_csv('../input/googleplaystore.csv')
df.head(5)


# ### Step 0. Explore and Prepare Dataframe

# In[ ]:


# check duplicates
n_duplicated = df.duplicated(subset=['App']).sum()
print("There are {}/{} duplicated records.".format(n_duplicated, df.shape[0]))
df_no_dup = df.drop(df.index[df.App.duplicated()], axis=0)
print("{} records after dropping duplicated.".format(df_no_dup.shape[0]))


# In[ ]:


# Check and clean type values, defer nan value processing to the next cell
print(set(df_no_dup.Type))
print("Dropping alien Type value '0', {} record(s) removed".format(sum(df_no_dup.Type == '0')))
df_no_dup = df_no_dup.drop(df_no_dup.index[df_no_dup.Type == '0'], axis=0)


# In[ ]:


# check and drop NaN values
print("NaA value statistics in each column")
print(df_no_dup.isnull().sum(axis=0),'\n')
df_no_dup = df_no_dup.dropna(subset=['Type'])
print("Column 'Type' with NaN values are dropped, {} records left.".format(df_no_dup.shape[0]))

# prepare rating dataframe
df_rating = df_no_dup.dropna(subset=['Rating'])
print("Cleaned dataframe for 'Rating' has {} records.".format(df_rating.shape[0]))


# In[ ]:


# we are interested in the columns Category, Rating and Type
# Drop irrelevant columns for Rating dataframe.
df_rating = df_rating.loc[:,['Rating', 'Type', 'Category']]


# In[ ]:


def plot_hist(df, col, bins=10):
    """
    Plot histograms for a column
    """
    plt.hist(df[col], bins=bins)
    plt.xlabel(col)
    plt.ylabel('counts')
    plt.title('Distribution of {}'.format(col))

def compute_app_types(df):
    """
    Given a dataframe, compute the number 
    of free and paid apps respectively
    """
    return sum(df.Type == "Free"), sum(df.Type == 'Paid')

def plot_app_types(df):
    """
    Plot app type distributions across categories
    """
    vc_rating = df.Category.value_counts()
    cat_free_apps = []
    cat_paid_apps = []
    for cat in vc_rating.index:
        n_free, n_paid = compute_app_types(df.query("Category == '{}'".format(cat)))
        cat_free_apps.append(n_free)
        cat_paid_apps.append(n_paid)

    f, ax = plt.subplots(2,1)
    ax[0].bar(range(1, len(cat_free_apps)+1), cat_free_apps)
    ax[1].bar(range(1, len(cat_free_apps)+1), cat_paid_apps)

def drop_categories(df):
    """
    Drop categories with any app type with instances fewer than 10
    """
    vc_rating = df.Category.value_counts()
    cats_to_drop = []
    for cat in vc_rating.index:
        n_free, n_paid = compute_app_types(df.query("Category == '{}'".format(cat)))
        if n_free < 10 or n_paid < 10:
            cats_to_drop.append(cat)
    for cat in cats_to_drop:
        df.drop(df.query('Category == "{}"'.format(cat)).index, axis=0, inplace=True)
    print("Deleted categories: {}".format(cats_to_drop))
    return df


# In[ ]:


# Describe Rating dataframe
plot_hist(df_rating, 'Rating')
df_rating.describe()


# In[ ]:


print("There are {} free and {} paid apps in the the Rating dataframe ".format(*compute_app_types(df_rating)))


# In[ ]:


# explore the distributions of free and paid apps across different categories
plot_app_types(df_rating)


# In[ ]:


# Exclude categories with fewer than 10 apps for any Free or Paid type
# Otherwise the categories would contain too few data to generalize the result
df_rating = drop_categories(df_rating)
print("Cleaned Rating dataframe has {} datapoints".format(df_rating.shape[0]))


# In[ ]:


df_rating.describe()


# ### Q 1. How does the ratings differ in general?

# In[ ]:


def plot_target_by_group(df, target_col, group_col, figsize=(6,4), title=""):
    """
    Plot the mean of a target column (Numeric) groupped by the group column (categorical)
    """
    order = sorted(list(set(df[group_col])))
    stats = df.groupby(group_col).mean()[target_col]
    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(x=group_col, y=target_col, data=df, ax=ax, order=order).set_title(title)
    ax.set(ylim=(3.8, 4.5))    
    return stats


# In[ ]:


stats = plot_target_by_group(df_rating, 'Rating', 'Type', title="Average Rating Groupped by App Type")
for i, s in zip(stats.index, stats):
    print("{} app has average {} {}".format(i, 'Rating',s))
mean_rating = df_rating.Rating.mean()
print("Mean rating: {}".format(mean_rating))


# #### Interpretation
# In general, Free apps, with an average rating of 4.16, are lower rated than Paid apps with an average rating of 4.27. Note that the average rating for all apps is 4.17, so Free apps are rated below average, while Paid apps are rated reletively higher than the average score.

# ### Q2 How are the differences distributed across different app categories?

# In[ ]:


paid_stats = plot_target_by_group(df_rating.query('Type == "Paid"'), 'Rating', 'Category', (16, 4), "(Paid App) Average Ratings by App Category")
free_stats = plot_target_by_group(df_rating.query('Type == "Free"'), 'Rating', 'Category', (16, 4), "(Free App) Average Ratings by App Category")


# In[ ]:


fig, ax = plt.subplots(figsize=(16,4))
sorted_idx = sorted(paid_stats.index)
rating_diff = paid_stats[sorted_idx] - free_stats[sorted_idx]
sns.barplot(x=sorted_idx, y=rating_diff, ax=ax).set_title("Difference of Ratings between Paid and Free Apps Across App Categories");
rating_diff


# #### Interpretation
# Although paid apps are in general more highly-rated than free apps, and so are in most app categories, there are still some app categories where free apps are likely to be favored more than the paid apps. For instance, COMMUNICATION, FINANCE and PHOTOGRAPHY are three such categories. In FINANCE category, the free apps on average are rated almost 0.3 higher than the paid apps, which is also the largest difference between app types across all the categories.
# 

# ### Q3 Are there any categories where the differences are statistically significant?

# In[ ]:


def compute_utest(df):
    """
    Compute Mann-Whitney rank tests
    for paid and free app ratings
    """
    paid_rating = df.query('Type == "Paid"')['Rating']
    free_rating = df.query('Type == "Free"')['Rating']
    return mannwhitneyu(paid_rating, free_rating)

def cat_utest(df):
    """
    Iteratively compute utest for each app category
    """
    cats = set(df.Category)
    res = []
    for cat in cats:
        stats, pval = compute_utest(df.query('Category == "{}"'.format(cat)))
        res.append({'Category':cat,
                    'u_statistics':stats,
                    'p_value':pval})
    return pd.DataFrame(res)

uval, pval = compute_utest(df_rating)

print("General utest result: pval {}, u {}".format(pval, uval))
df_utest = cat_utest(df_rating)   
df_utest.loc[df_utest.p_value < .05] # significant categories


# #### Interpretation
# As rating is not normally-distributed, Mann-Whitney's U test was applied to test the significance of rating differences, since this test is free from a normal assumption. At the 0.05 significance level, results of the u tests on different categories demonstrate that the free and paid apps in the following categories have significant rating differences: personalization, tools, family and games. Paid apps are on average higher rated than free apps in these categories.

# ### Concluding Remarks
# 
# Data analysis was conducted on the Kaggle Google Play Store dataset, the answers to the three questions were explored:
# - How do the ratings differ between paid and free apps in general?
#   In general, Paid apps are better-rated than free apps, which appears to support the argument that service quility of the paid apps is better.
# - How are the differences distributed across different app categories?
#   In most categories, Paid apps achieve higher ratings than free apps, however, in a few categories such as COMMUNICATION, FINANCE and PHOTOGRAPHY, the average ratings of free apps are higher than those of paid apps. Is this because many popular apps in these categories are free, like facebook and whatsapp in the COMMUNICATION category?
# - Are there any categories where the differences are statistically significant?
#   There are four categories (PERSONALIZATION, TOOLS, FAMILY and GAME) where paid apps are rated significantly higher than free apps.
#   
# This is only a very superficial exploration of the Google Play Store dataset. There are many other useful information including installation counts and app review texts, which might entail many more interesting facts and await further exploration.
#   
# 
#   
# 
# 

# In[ ]:




