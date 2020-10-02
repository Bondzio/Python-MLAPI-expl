#!/usr/bin/env python
# coding: utf-8

# # Gender diversity and Hollywood
# There is extensive [research](http://https://www.google.com/search?q=gender+diversity+impact+on+business) showing that gender-diverse teams are more productive and  produce better business results.
# Let's explore if this is true for Hollywood as well. We'll look at gender in the crew of movies, and how it affects revenue.
# ![](https://www.star2.com/wp-content/uploads/2017/05/wonder-woman-embargo-lift-image-full-236508-e1495691267826-770x470.jpg)

# In[ ]:


# Import
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import os
from collections import Counter
import time
from sklearn.preprocessing import LabelEncoder
from matplotlib import rcParams
get_ipython().run_line_magic('matplotlib', 'inline')
rcParams['axes.titlesize'] = 20
rcParams['figure.figsize'] = 15,5


# # Prepare the data

# In[ ]:


rcParams['figure.figsize'] = 15,5

# Load files
# print(os.listdir("../input"))
train = pd.read_csv("../input/train.csv")
test = pd.read_csv("../input/test.csv")


# In[ ]:


# Combine train and test to allow feature engineering on the combined data. Store the ids and the revenue for future use
train_rows = train.shape[0]
all_data = pd.concat([train, test], sort=False)


# In[ ]:


# Several columns (e.g. genres) are lists of values - split them to dictionaries for easier processing
import ast
for c in ['belongs_to_collection', 'genres', 'production_companies', 'production_countries', 'spoken_languages', 
          'Keywords', 'cast', 'crew']:
    all_data[c] = all_data[c].apply(lambda x: {} if pd.isna(x) else ast.literal_eval(x))


# # crew EDA

# In[ ]:


# Let's take a look at how crew looks. The crew of a movie can be quite long, so only displaying the first few.
all_data.crew.head(1).apply(lambda x: print(x[0:4]))


# In[ ]:


# We can see that crew members have a gender property. Let's look at the values
all_data.crew.head(5).apply(lambda crew_members: set([crew_member["gender"] for crew_member in crew_members]))


# We can see that gender has 3 possible values: 0, 1 and 2.
# According to [this](http://https://www.themoviedb.org/talk/58ee5022c3a3683ded00a887),  0 means "not specified", 1 means female, and 2 means male.
# Let's look at the distribution.

# In[ ]:


gender_labels = {0: "unspecified", 1: "female", 2: "male"}
# Now let's look at the distribution of values
gender_list_list = list(all_data.crew.apply(lambda x: [cm["gender"] for cm in x]).values)
gender_list = [gender for gender_list in gender_list_list for gender in gender_list]
gender_counter = Counter(gender_list)
print("Number of crew members by gender:", gender_counter)
gender_indexes = np.arange(len(gender_counter))
plt.barh(gender_indexes, list(gender_counter.values()))
plt.yticks(gender_indexes, [gender_labels[i] for i in gender_counter.keys()])
plt.title("Number of crew members by gender")
plt.show()


# # Input unspecified gender
# We can see in the chart above that most crew members don't have a gender specified.
# We'll try to determine the gender by looking at other crew members (and cast) who have a gender specified and have the same first name.
# Some first names are both male and female. If a name is 90% or more male or female, we'll use that gender, otherwise we'll keep it as unspecified.

# In[ ]:


# Create a DataFrame of all the names in the cast and crew columns and how many times they appear as each gender
tuple_list_list = list(all_data["cast"].apply(lambda x: [(cm["name"].split(" ")[0], cm["gender"]) for cm in x]).values)
tuple_list_list.extend(list(all_data["crew"].apply(lambda x: [(cm["name"].split(" ")[0], cm["gender"]) for cm in x]).values))
tuple_list = [i for tuple_list in tuple_list_list for i in tuple_list]
names = set()
c = [None] * 3
for gender in range (0, 3):
    t = [i[0] for i in tuple_list if i[1] == gender]
    names.update(set(t))
    c[gender] = Counter(t)
names_df = pd.DataFrame(data = list(names), columns=["name"])
names_df["appears_as_female"] = names_df["name"].apply(lambda x: c[1][x])
names_df["appears_as_male"] = names_df["name"].apply(lambda x: c[2][x])
names_df["total_appearences"] = names_df.apply(lambda x: x["appears_as_female"]+x["appears_as_male"], axis=1)
names_df.sort_values("total_appearences", ascending=False).head()


# In[ ]:


# Determine the gender of each name. We'll use the following heuristic
# If there are less than 5 samples, don't classify
# Otherwise, if more than 90% are male or female, use that gender
# Otherwise, don't classify
def ClassifyName(row):
    fcount = row["appears_as_female"]
    mcount = row["appears_as_male"]
    if (fcount + mcount < 5):
        gender = 0
    elif (fcount == 0):
        gender = 2
    elif (mcount == 0):
        gender = 1
    else:  # both are > 0
        # If a name is 90+% male or female, even if unisex, we'll bet on the majority
        if (mcount / float(fcount) < 0.1):
            gender = 1
        elif (fcount / float(mcount) < 0.1):
            gender = 2
        else: #unisex, no sex more than 90% - leave as undefined
            gender = 0
    return (gender)

names_df["gender"] = names_df.apply(lambda x: ClassifyName(x), axis=1)
names_df.head()

# Create a dictionary that maps each name that as male or female (to not add names with undefined gender)
names_to_gender = dict()
def update_names_to_gender(row):
    if (row["gender"] > 0):
        names_to_gender[row["name"]] = row["gender"]
j = names_df.apply(lambda x: update_names_to_gender(x), axis=1)
# names_to_gender


# In[ ]:


# We'll use the above dictionary to fix the items with unspecified gender in cast and crew
def fix_unknown_gender_row(row):
    for cm in row:
        if cm["gender"] == 0:
            name = cm["name"]
            first_name = name.split(" ")[0]
            if (first_name in names_to_gender):
                cm["gender"] = names_to_gender[first_name]

j = all_data["crew"].apply(lambda x: fix_unknown_gender_row(x))
j = all_data["cast"].apply(lambda x: fix_unknown_gender_row(x))

# Let's see if that helped
plt.figure(figsize=(12, 5))
gender_labels = {0: "unspecified", 1: "female", 2: "male"}
# Now let's look at the distribution of values
gender_list_list = list(all_data.crew.apply(lambda x: [cm["gender"] for cm in x]).values)
gender_list = [gender for gender_list in gender_list_list for gender in gender_list]
gender_counter = Counter(gender_list)
print("Updated number of crew members by gender:", gender_counter)
gender_indexes = np.arange(len(gender_counter))
plt.barh(gender_indexes, list(gender_counter.values()))
plt.yticks(gender_indexes, [gender_labels[i] for i in gender_counter.keys()])
plt.title("Number of crew members by gender (after classifying unspecified)", fontsize=20)
plt.show()


# We were able to categorize most of the crew members who had unspecified gender. 
# We can  see that there are significantly more male cast members than female cast members.
# Let's break the numbers down by the job of the cast members (Producer, Director, etc.)

# In[ ]:


# Get a list of jobs
job_list_list = list(all_data.crew.apply(lambda crew_members: [crew_member["job"] for crew_member in crew_members]).values)
job_list = [job for job_list in job_list_list for job in job_list]
job_counter = Counter(job_list)
print("The most common jobs are:", job_counter.most_common(10))
top_jobs = [x[0] for x in job_counter.most_common(10)]


# In[ ]:


# We will also want to track the aggregate of the top jobs
top_jobs.append("Top jobs")

# For each combination of top job and gender, create a column with the count of crew members of that job and gender
for job in top_jobs:
    for gender in range(0, 3):
        cname = "crew_" + job + "_" + str(gender)
        all_data[cname] = all_data.crew.apply(
            lambda x: len([c for c in x if ((c["job"]==job) or ((job=="Top jobs") and (c["job"] in top_jobs))) and (c["gender"]==gender)]))
all_data.head(5)


# Let's plot the distribution of gender by job.

# In[ ]:


# Let's look at the gender distribution by job
tj1 = top_jobs[:-1]
ind = np.arange(len(tj1))
prev_values = np.zeros(len(tj1))

def crewcol(job, suffix):
    return ("crew_" + job + "_" + suffix)

for gender in range(0, 3):
    values = np.zeros(0)
    for job in tj1:
        cname = crewcol(job, str(gender))
        n = all_data[cname].sum()
        values = np.append(values, n)
    p = plt.barh(ind, values, left=prev_values)
    prev_values += values
plt.yticks(ind, top_jobs)
plt.legend(["unspecified", "female", "male"])
plt.title("Proportion of gender by job")
plt.show()


# We can see that in most of the top 10 jobs, male crew members are the majority. 
# Casting seems to be the only exception - it has significantly more female cating crew members than male.
# 
# We'll now create a column for each of the top jobs, which has the average gender (excluding crew members with unspecified gender). An average gender of 1.0 means that the crew is all female, 1.5 means it's 50-50, and 2.0 is all male, and look at the distribution of the average gender.

# In[ ]:


# Let's create a new column for each top job which is the average gender (excluding 0s)
avg_col_names = []
count_col_names = []

def crewcolavg(job):
    return (crewcol(job, "avg_gender"))
def crewcolcnt(job):
    return (crewcol(job, "count_gender"))

for job in top_jobs:
    c_avg = crewcolavg(job)
    avg_col_names.append(c_avg)
    c1 = crewcol(job, "1")
    c2 = crewcol(job, "2")
    all_data[c_avg] = all_data.apply(lambda x: round((x[c1]*1 + x[c2]*2) / (x[c1] + x[c2]), 1) if (x[c1]+x[c2]>0) else None, axis=1)
    c_count = crewcolcnt(job)
    count_col_names.append(c_count)
    all_data[c_count] = all_data.apply(lambda x: x[c1] + x[c2] if (x[c1]+x[c2]>0) else None, axis=1)
    
all_data[avg_col_names].head()


# In[ ]:


all_data[avg_col_names].boxplot(vert=False, grid=False)
plt.title("Average gender distribution by job")
plt.yticks(range(1, len(top_jobs)+1), top_jobs);


# # Let's look back in time
# We can see that the median crew is 100% male for all jobs other than Casting. All up for the top 10 jobs, the median crew is about 90% male.
# 
# Was it always like this? Did it get better or worse over time? Let's take a look at how the gender composition of crews looks by release date.

# In[ ]:


# release_date
# Check for nulls
all_data.loc[all_data["release_date"].isnull()]
# There is 1 movie w/o a release date. Looking it up in imdb by imdb_id = tt0210130, it was released in March 2000
all_data.loc[all_data["release_date"].isnull(), "release_date"] = "05/01/2000"
# Parse the string to a date
all_data["release_date"] = pd.to_datetime(all_data["release_date"])
# Create columns for each part of the date
all_data["release_date_weekday"] = all_data["release_date"].dt.weekday.astype(int)
all_data["release_date_month"] = all_data["release_date"].dt.month.astype(int)
all_data["release_date_year"] = all_data["release_date"].dt.year.astype(int)
# The year is formatted as yy as opposed to yyyy, and therefore the century is sometimes incorrect.
all_data["release_date_year"] = np.where(all_data["release_date_year"]>2019, all_data["release_date_year"]-100, all_data["release_date_year"])
all_data["release_date_decade"] = (all_data["release_date_year"]/10).astype(int)*10


# In[ ]:


all_data.groupby("release_date_decade").mean()[avg_col_names].plot(figsize=(15,8), grid=True)
plt.xlabel("Release decade")
plt.ylabel("Average gender")
plt.title("Change in gender composition of crew over time");


# We can see that **Casting** started as a distinct job in the 1940s with 100% male crews, and it gradually changed to 75-80% female crews over the next 70 years. 
# For the other jobs, the 1970s saw most male crew members, and since there has been a slight change towards more female crew members, especially **Art Direction** (about 25% female), **Production Design** and **Editor** (about 20% female).
# The least change is in **Original Music Composer** and **Director of Photography** - both jobs continue to be at less than 5% female crew members.

# In[ ]:


# Split back to train and test
train = all_data[:train_rows]
test = all_data[train_rows:]


# # Relationship between gender diversity and revenue
# Let's see if there is any relationship between the composition of crews in terms of gender and the revenue of the movie.
# We will only look at crews that had 2 or more crew members.

# In[ ]:


all_data[count_col_names[:-1]].boxplot(vert=False, grid=False, showfliers=True)
plt.title("Average number of crew members by job")
plt.yticks(range(1, len(top_jobs)), top_jobs[:-1]);
plt.xticks(np.arange(0,25));


# We can see that only 5 jobs had a significant number of movies with 2 or more crew members: 
# * Producer
# * Executive Producer
# * Screenplay
# * Casting
# * Art Direction
# 
# We will focus on those.

# In[ ]:


multi_member_jobs = ["Executive Producer", "Producer", "Screenplay", "Casting", "Art Direction"]
plt.figure(figsize=(15, 20))
plt.subplots_adjust(hspace=0.35, wspace=0.1)
for i in range(0, len(multi_member_jobs)):
    job = multi_member_jobs[i]
    plt.subplot(5, 2, i+1)
    train[train[crewcolcnt(job)]>1].groupby(crewcolavg(job)).median()["revenue"].plot()
    plt.xlabel(job)
plt.suptitle("Revenue by average gender", fontsize=20, y=0.91);


# We can see 2 peaks: one for crews which are mostly male with some female members and a second one for crews which are mostly female with some male members. Crews which are 100% male or 100% female tend to have lower revenue. Crews which are 50-50 male and female also have lower revenue.
# # Conclusion
# This analysis clearly shows that mixed crews of Executive Producers, Producers, Screenplay, Casting and Art Directors tend to produce movies with higher revenue than those with are all-female or all-male. 
# Still, it's interesting that gender distribution which is about 1/3 to 2/3 in either direction produces best results. Crews which are balanced (half female and half male) don't do as well.
# # Next steps
# I will try to control for various factors and see the impact. E.g. is this a cultural thing - does it change by country?

# In[ ]:


train.groupby("release_date_decade").median()["revenue"].plot(figsize=(15,8))
plt.xlabel("Release decade")
plt.ylabel("Median revenue")
plt.title("Median revenue by decade");

