#!/usr/bin/env python
# coding: utf-8

# ## Exploration and Visualization for Card Data

# ### Abstract

# There are some insights for the card data (train.csv and test.csv). The details are in the notebook but mainly the followings are found:
# 
# * There is a sharp decrease in the number of cards which start activity at 2018 (Figure: First Active Months Count).
# 
# * The customer loyalty is much lower at 2012-04 when you compare it with other months (Figure: Monthly Customer Loyalty).
# 
# * Customer loyalty increased continuosly after 2017-01. There is an obvious trend (Figure: Monthly Customer Loyalty).
# 
# * Train and Test sets are divided very well according to the features distribution.
# 
# * There is a correlation between features and customer loyalty. It is obvious in the last figure. 

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


df_train = pd.read_csv("../input/train.csv")
df_test = pd.read_csv("../input/test.csv")


# In[ ]:


df_train.head()


# In[ ]:


df_test.head()


# In[ ]:


print("length of train dataset:", len(df_train))
print("length of test dataset:", len(df_test))


# In[ ]:


df_month_counts_train = pd.DataFrame(df_train['first_active_month'].value_counts())
df_month_counts_train = df_month_counts_train.reset_index()
df_month_counts_train.columns = ['first_active_month', 'count']
df_month_counts_train = df_month_counts_train.sort_values(by=['first_active_month'])
df_month_counts_train = df_month_counts_train.reset_index()
df_month_counts_train = df_month_counts_train.drop(columns=['index'])


# In[ ]:


df_month_counts_train.head()


# In[ ]:


df_month_counts_train.sort_values(by=['first_active_month'], ascending=False).head()


# In[ ]:


df_month_counts_test = pd.DataFrame(df_test['first_active_month'].value_counts())
df_month_counts_test = df_month_counts_test.reset_index()
df_month_counts_test.columns = ['first_active_month', 'count']
df_month_counts_test = df_month_counts_test.sort_values(by=['first_active_month'])
df_month_counts_test = df_month_counts_test.reset_index()
df_month_counts_test = df_month_counts_test.drop(columns=['index'])


# In[ ]:


df_month_counts_test.head()


# In[ ]:


df_month_counts_test.sort_values(by=['first_active_month'], ascending=False).head()


# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x="first_active_month", y="count", data=df_month_counts_train)
plt.xticks(rotation= 90)
plt.xlabel('Month')
plt.ylabel('Count')
plt.title('First Active Month Counts - Train Data')


# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x="first_active_month", y="count", data=df_month_counts_test)
plt.xticks(rotation= 90)
plt.xlabel('Month')
plt.ylabel('Count')
plt.title('First Active Month Counts - Test Data')


# Note: There is a  sharp decrease and very low counts for 2018 data.

# In[ ]:


df_month_means = df_train.groupby(['first_active_month']).mean()
df_month_means = df_month_means.reset_index()
df_month_means = df_month_means.sort_values(by=['first_active_month'])
df_month_means = df_month_means.reset_index()
df_month_means = df_month_means.drop(columns=['index'])


# In[ ]:


df_month_means


# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x="first_active_month", y="target", data=df_month_means)
#sns.relplot(x="first_active_month", y="target", kind="line", data=df_month_means);
plt.xticks(rotation= 90)
plt.xlabel('Month')
plt.ylabel('Target')
plt.title('Monthly Customer Loyalty')


# Note:
# 
# There are two points to pay attention:
# 
# 1- What happened to customer loyalty at 2012-04? It is extremely low. It should be investigated.
# 
# 2- After 2017-01, there is a continous upper trend in customer loyalty.

# In[ ]:


df_month_means.sort_values(by=['target']).head()


# In[ ]:


plt.figure(figsize=(15,10))
sns.violinplot(y="target", data=df_train, palette="muted")
plt.title('Violin Plot for Customer Loyalty')


# In[ ]:


plt.figure(figsize=(15,10))
sns.distplot(df_train["target"]);
plt.title('Histogram for Customer Loyalty')


# Note: It is obvious that customer loyalty values distribution is accumulated around the mean + median but there are some values look like potential outliers or at least should be taken into consideration for prediction.

# Now lets validate it with further analysis by removing some extreme data.

# In[ ]:


# Function: print_quantile_info(qu_dataset, qu_field)
#   Print out the following information about the data
#   - interquartile range
#   - upper_inner_fence
#   - lower_inner_fence
#   - upper_outer_fence
#   - lower_outer_fence
#   - percentage of records out of inner fences
#   - percentage of records out of outer fences
# Input: 
#   - pandas dataframe (qu_dataset)
#   - name of the column to analyze (qu_field)
# Output:
#   None

def print_quantile_info(qu_dataset, qu_field):
    a = qu_dataset[qu_field].describe()
    
    iqr = a["75%"] - a["25%"]
    print("interquartile range:", iqr)
    
    upper_inner_fence = a["75%"] + 1.5 * iqr
    lower_inner_fence = a["25%"] - 1.5 * iqr
    print("upper_inner_fence:", upper_inner_fence)
    print("lower_inner_fence:", lower_inner_fence)
    
    upper_outer_fence = a["75%"] + 3 * iqr
    lower_outer_fence = a["25%"] - 3 * iqr
    print("upper_outer_fence:", upper_outer_fence)
    print("lower_outer_fence:", lower_outer_fence)
    
    count_over_upper = len(qu_dataset[qu_dataset[qu_field]>upper_inner_fence])
    count_under_lower = len(qu_dataset[qu_dataset[qu_field]<lower_inner_fence])
    percentage = 100 * (count_under_lower + count_over_upper) / a["count"]
    print("percentage of records out of inner fences: %.2f"% (percentage))
    
    count_over_upper = len(qu_dataset[qu_dataset[qu_field]>upper_outer_fence])
    count_under_lower = len(qu_dataset[qu_dataset[qu_field]<lower_outer_fence])
    percentage = 100 * (count_under_lower + count_over_upper) / a["count"]
    print("percentage of records out of outer fences: %.2f"% (percentage))


# In[ ]:


# Function: remove_outliers_using_quantiles(qu_dataset, qu_field, qu_fence)
#   1- Remove outliers according to the given fence value and return new dataframe.
#   2- Print out the following information about the data
#      - interquartile range
#      - upper_inner_fence
#      - lower_inner_fence
#      - upper_outer_fence
#      - lower_outer_fence
#      - percentage of records out of inner fences
#      - percentage of records out of outer fences
# Input: 
#   - pandas dataframe (qu_dataset)
#   - name of the column to analyze (qu_field)
#   - inner (1.5*iqr) or outer (3.0*iqr) (qu_fence) values: "inner" or "outer"
# Output:
#   - new pandas dataframe (output_dataset)

def remove_outliers_using_quantiles(qu_dataset, qu_field, qu_fence):
    a = qu_dataset[qu_field].describe()
    
    iqr = a["75%"] - a["25%"]
    print("interquartile range:", iqr)
    
    upper_inner_fence = a["75%"] + 1.5 * iqr
    lower_inner_fence = a["25%"] - 1.5 * iqr
    print("upper_inner_fence:", upper_inner_fence)
    print("lower_inner_fence:", lower_inner_fence)
    
    upper_outer_fence = a["75%"] + 3 * iqr
    lower_outer_fence = a["25%"] - 3 * iqr
    print("upper_outer_fence:", upper_outer_fence)
    print("lower_outer_fence:", lower_outer_fence)
    
    count_over_upper = len(qu_dataset[qu_dataset[qu_field]>upper_inner_fence])
    count_under_lower = len(qu_dataset[qu_dataset[qu_field]<lower_inner_fence])
    percentage = 100 * (count_under_lower + count_over_upper) / a["count"]
    print("percentage of records out of inner fences: %.2f"% (percentage))
    
    count_over_upper = len(qu_dataset[qu_dataset[qu_field]>upper_outer_fence])
    count_under_lower = len(qu_dataset[qu_dataset[qu_field]<lower_outer_fence])
    percentage = 100 * (count_under_lower + count_over_upper) / a["count"]
    print("percentage of records out of outer fences: %.2f"% (percentage))
    
    if qu_fence == "inner":
        output_dataset = qu_dataset[qu_dataset[qu_field]<=upper_inner_fence]
        output_dataset = output_dataset[output_dataset[qu_field]>=lower_inner_fence]
    elif qu_fence == "outer":
        output_dataset = qu_dataset[qu_dataset[qu_field]<=upper_outer_fence]
        output_dataset = output_dataset[output_dataset[qu_field]>=lower_outer_fence]
    else:
        output_dataset = qu_dataset
    
    print("length of input dataframe:", len(qu_dataset))
    print("length of new dataframe after outlier removal:", len(output_dataset))
    
    return output_dataset


# In[ ]:


print_quantile_info(df_train, "target")


# In[ ]:


df_train_new = remove_outliers_using_quantiles(df_train, "target", "outer")


# In[ ]:


plt.figure(figsize=(15,10))
sns.violinplot(y="target", data=df_train_new, palette="muted")
plt.title('Violin Plot for Customer Loyalty After Removing Outer Data')


# In[ ]:


plt.figure(figsize=(15,10))
sns.distplot(df_train_new["target"]);
plt.title('Histogram for Customer Loyalty After Removing Outer Data')


# In[ ]:


sns.catplot(x="feature_1", kind="count", palette="ch:.25", data=df_train);
sns.catplot(x="feature_1", kind="count", palette="ch:.25", data=df_test);


# In[ ]:


sns.catplot(x="feature_2", kind="count", palette="ch:.25", data=df_train);
sns.catplot(x="feature_2", kind="count", palette="ch:.25", data=df_test);


# In[ ]:


sns.catplot(x="feature_3", kind="count", palette="ch:.25", data=df_train);
sns.catplot(x="feature_3", kind="count", palette="ch:.25", data=df_test);


# In[ ]:


sns.catplot(x="feature_1", y="target", kind="bar", palette="ch:.25", data=df_train);


# In[ ]:


sns.catplot(x="feature_2", y="target", kind="bar", palette="ch:.25", data=df_train);


# In[ ]:


sns.catplot(x="feature_3", y="target", kind="bar", palette="ch:.25", data=df_train);


# In[ ]:


df_feature_groups = df_train.groupby(['feature_1','feature_2','feature_3']).mean()
df_feature_groups = df_feature_groups.reset_index()
df_feature_groups.sort_values("target")


# In[ ]:


df_feature_groups["features"] = df_feature_groups["feature_1"].astype('str') + "+" + df_feature_groups["feature_2"].astype('str') + "+" + df_feature_groups["feature_3"].astype('str')


# In[ ]:


df_feature_groups


# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x="features", y="target", palette="ch:.25", data=df_feature_groups)
plt.xticks(rotation= 90)

