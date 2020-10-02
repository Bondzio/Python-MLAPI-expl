#!/usr/bin/env python
# coding: utf-8

# # Crash Course Pandas 2
# Im creating these series for people that have beginner/intermediate knowledge about pandas library.I m going to share my working notes(after tidying) to pass the info,nothing more. Certain codeblocks could get repetitive. Some info looks contradictory even though i have tried to remove most of them. Sorry for it beforehand. Also goodluck on your learning journey. This is my first kernel as well. Wish me luck. Contact me for any question, i will help you out if i can.
# 
# Contents:
# * [Dataset](#1)
# * [Most provoking Talks in Online Discussion](#2)
# * [Visualizing Comment Distribution](#3)
# * [Number of Talks From Each Year](#4)
# * [Best Event in TED History](#5)
# * [Unpacking Ratings Column](#6)
# * [Total Number of Ratings Received by Each Talk](#7)
# * [Which Occupations Have the Funniest TED Talks on AVG](#8)
# 

# In[ ]:



import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
ri = pd.read_csv("../input/police.csv")
ted = pd.read_csv("../input/ted.csv")


# <a id="1"></a> 
# ## Dataset

# In[ ]:


ted.head()


# In[ ]:


ted.shape


# In[ ]:


ted.dtypes


# In[ ]:


#6 speakers with nan occupation.
ted.isna().sum()


# <a id="2"></a> 
# ## Most provoking Talks in Online Discussion

# In[ ]:


ted.head()


# In[ ]:


#you should sort the data with respect to online comments-Only the col itself.
ted.comments.sort_values(ascending=False)


# In[ ]:


#this could work out also and also its much more better approach.Also its good idea to check event date.Bcs theyre relevant
ted.sort_values("comments",ascending=False)


# In[ ]:


#but how can we use event date? We can use views.its much more clear approach.
ted["comments_per_view"]=ted.comments/ted.views


# In[ ]:


ted.sort_values("comments_per_view",ascending=False)


# In[ ]:


#another approach-same mentality
ted["views_per_comment"]=ted.views/ted.comments


# In[ ]:


ted.sort_values("views_per_comment")


# <a id="3"></a> 
# ## Visualizing Comment Distribution

# In[ ]:



ted.shape


# In[ ]:


#x is index,y is # of comments
ted.comments.plot()
#kind->line,bar,barh,hist,box,kde,density,area,pie.default is line which is not very informative


# In[ ]:


#most of the comments (nearly all of them) has btw 0 to ~600 comments.but changing binwidth could be more helpful.
ted.comments.plot(kind="hist")


# In[ ]:


#via using seaborn we could get much more good looking visuals however this is pandas workout so...
ted[ted.comments<=1000].comments.plot(kind="hist")
#this could help out.


# In[ ]:


#using loc
ted.loc[ted.comments<=1000,"comments"].plot(kind="hist")
#loc is very good,u can select single col,multi col,list of cols,range of cols.


# In[ ]:


#increasing bin size makes our plot more informative.50-100 comment range is the real deal.
ted.loc[ted.comments<=1000,"comments"].plot(kind="hist",bins=20)
#choose 


# In[ ]:


#choose your plot type carefully
#histogram for distribution
#barplot for comparing categories
#lineplot good for timeseries(change w time)
#scatterplot good for comparing multiple variable (comparing 2 variables)
#check pandas visualization page for more info
#https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
#pandas plots are more exploratory data analysis friendly however matplotlib is much more customizable


# <a id="4"></a> 
# ## Number of Talks From Each Year

# In[ ]:


ted.head()


# In[ ]:


#as u can see data doesnt always have "ted2014" format. so ted.event.str.split(2,6) doesnt work.
ted.event.value_counts()


# In[ ]:


#value_counts() do the job however just for sake of using dif argument lets use sample
ted.event.sample(10)


# In[ ]:


#so event col doesnt help us lets look another field, film_date which is created by unix timestamps
ted.film_date.head()
#believe it or not pd.to_datetime very smart tool...


# In[ ]:


#its somewhat achievement but not totally.
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
#search the bottom of the manual/documentation to see sth about unix timestamps.
pd.to_datetime(ted.film_date).head()


# In[ ]:


#this is much better.
pd.to_datetime(ted.film_date,unit="s").head()


# In[ ]:


#lets store it
ted["film_datetime"]=pd.to_datetime(ted.film_date,unit="s")


# In[ ]:


#lets check it out.but not with head() this time.we should use other data control tools from time to time
ted.loc[:,["event","film_datetime"]].sample(10)


# In[ ]:


#OR
ted[["event","film_datetime"]].sample(10)


# In[ ]:


#checking data types is useful.our film_datetime is datetime dtype.
ted.dtypes


# In[ ]:


#datetime methods/attributes have same logic like string(str) methods(attributes) data.col.str.method()
ted.film_datetime.dt.year.head()


# In[ ]:


#ted.film_datetime.dt.year.value_counts().index -> 2013,2011 etc are all indexex/indices.check their order...
ted.film_datetime.dt.year.value_counts()


# In[ ]:


#plotting time.lets try couple.
ted.film_datetime.dt.year.value_counts().plot(kind="bar")
#not the one we are looking for,barplots are good for catg data.and you cant consider years as categories for this case.


# In[ ]:


#x=no of talks y=no of occurence/freq. however this doesnt help us either.
ted.film_datetime.dt.year.value_counts().plot(kind="hist")


# In[ ]:


#this could help us,however there is a problem.its sort index issue.
ted.film_datetime.dt.year.value_counts().plot(kind="line")


# In[ ]:


#looks like there is a sharp decline in tedtalk talk counts.lets investigate further.
ted.film_datetime.dt.year.value_counts().sort_index().plot(kind="line")


# In[ ]:


#latest talk datetime.so we cant be sure for present time(2019)
ted.film_datetime.max()


# In[ ]:


#tip:read the documentation if u have a clue about how to achieve sth but you dont get a proper result completely.
#always remember to_datetime/datetime when you are working w date.


# <a id="5"></a> 
# ## Best Event in TED History

# In[ ]:


ted


# In[ ]:


#count the no of talks? 1. parameter to look up to.
ted.event.value_counts().head()


# In[ ]:


#here is a long series of explanation..starts from here
#this data has 896 values.groupby uses max 5 values from that dset for each group.therefore dset w 2550 rows becomes 896
ted.groupby("event").event.head()


# In[ ]:


#and here is their views col.
ted.groupby("event").views.head()


# In[ ]:


#here is the whole dataframe.
ted.groupby("event").head()


# In[ ]:


#lets check out multiple aggregate functions at once.dont get confused not all ted talks has "TED" in their event names.
ted.groupby("event").views.mean().sort_values(ascending=False)
#why use mean->because some talks occurred on same place.


# In[ ]:


#ted.groupby("event").views.count().sort_values(ascending=False) is unnecessary to look bcs
#ted.event.value_counts() does the same job.
#Now lets try to put count and mean in same table.


# In[ ]:


ted.groupby("event").views.agg(["count","mean"]).sort_values(by="mean",ascending=False)


# In[ ]:


#lets add sum too.Now we can see the total no of views
ted.groupby("event").views.agg(["count","mean","sum"]).sort_values(by="sum",ascending=False)
#there are many criterias to measure performance.1 time mass hit talk vs many talks-good amount of views...


# <a id="6"></a> 
# ## Unpacking Ratings Column

# In[ ]:


ted.head()


# In[ ]:


#ratings=there used to be a way on ted website to tag talks for site visiters.
ted.ratings.head()


# In[ ]:


#to get first row.
#ted.ratings[0]
ted.loc[0,"ratings"]


# In[ ]:


#ratings col data is "stringified list of dictionaries" its not a list of dictionaries,its a string.
type(ted.ratings[0])
#now how can we unpack this complex data?


# In[ ]:


import ast
#abstract syntax tree.


# In[ ]:


#if i enter string that looks like a list, literal_eval returns a list.
ast.literal_eval("[1,2,3]")


# In[ ]:


type(ast.literal_eval("[1,2,3]"))
#stringified integer,stringified list.. it can deal with it.


# In[ ]:


#here is our list.its a list of dictionaries.now we need to apply this to all col.
ast.literal_eval(ted.ratings[0])


# In[ ]:


#first solve it via f()
def str_to_list(ratings_str):
    return ast.literal_eval(ratings_str)


# In[ ]:


#that result looks good.str_to_list(ratings) doesnt needed.bcs we are looking to the ratings col.python gets what we are
#trying to accomplish.
ted.ratings.apply(str_to_list).head()


# In[ ]:


#however no function is necessary.
ted.ratings.apply(ast.literal_eval).head()


# In[ ]:


#lets do lambda f() version to see what is lambda f() does
ted.ratings.apply(lambda x: ast.literal_eval(x)).head()


# In[ ]:


#lets save it as actual col
ted["rating_list"]=ted.ratings.apply(lambda x: ast.literal_eval(x))


# In[ ]:


#rating_list considered as object.its not a string columns!,its a column that contains list.
ted.dtypes


# In[ ]:


#apply and map f() are closely related.if i want to apply x function to whole col i use apply.
#i use map to do dictionary mapping. {"a":1,"b":2} etc. For creating new col with old cols data.
#tip:pay attention to dtypes,use apply even its considered slow (from time to time)


# <a id="7"></a> 
# ## Total Number of Ratings Received by Each Talk

# In[ ]:


ted.head()


# In[ ]:


#function time (step by step)
def get_num_ratings(list_of_dicts):
    return list_of_dicts[0]


# In[ ]:


get_num_ratings(ted.rating_list[0])


# In[ ]:


def get_num_ratings2(list_of_dicts):
    return list_of_dicts[0]["count"]


# In[ ]:


get_num_ratings2(ted.rating_list[0])


# In[ ]:


def get_num_ratings3(list_of_dicts):
    num=0
    for d in list_of_dicts:
        num=num+d["count"]
    return num


# In[ ]:


get_num_ratings3(ted.rating_list[0])


# In[ ]:


ted.rating_list.apply(get_num_ratings3)


# In[ ]:


ted["num_ratings"]=ted.rating_list.apply(get_num_ratings3)


# In[ ]:


ted.num_ratings.describe()


# In[ ]:


#alternative methods.
#for first item in rating_list these are the results.
pd.DataFrame(ted.rating_list[0])


# In[ ]:


#sort it out
pd.DataFrame(ted.rating_list[0]).sort_values("count",ascending=False)
#for first talk in list top count is inspiring with 24k, id is emotion_id(10 is for inspiring)
#for first talk in the list there are total of 93k tags.If u put 1 inside of sqr brackets u see the dif results for 2nd data


# In[ ]:


#to get total count
#u cant use use .count.sum() bcs colname conflicts with attribute.thats the result.U can change it to 1-2 etc to see others.
pd.DataFrame(ted.rating_list[0])["count"].sum()


# <a id="8"></a> 
# ## Which Occupations Have the Funniest TED Talks on AVG

# In[ ]:


#step by step process.lets dive in.
#step1:count the no of funny ratings


# In[ ]:


ted.rating_list.head()


# In[ ]:


#we want to check if all talks have funny tags in them
ted.ratings.str.contains("Funny").value_counts()
#its always there.


# In[ ]:


#function time again.
def get_funny_ratings(list_of_dicts):
    for d in list_of_dicts:
        if d["name"]=="Funny":
            return d["count"]


# In[ ]:


ted["funny_ratings"]=ted.rating_list.apply(get_funny_ratings)


# In[ ]:


#now we have every talks "funny" tag count in id order.
ted.funny_ratings.head()


# In[ ]:


#step2:lets get a percentage approach.
#lets get percentage based approach to see how much of our "tags" are funny in that specific talk
ted["funny_rate"]=ted.funny_ratings/ted.num_ratings


# In[ ]:


#lets do a fact check.to see our data is correct-here is the whole data.
#what should i check from here to see if our approach is correct.speakers.occupation.comedian=higher,scientist=lower...
ted.sort_values("funny_rate",ascending=False).head()


# In[ ]:


#reasonable.these dudes are funniest by their sheer funny_rate sorting results.
ted.sort_values("funny_rate",ascending=False).speaker_occupation.head()


# In[ ]:


#least funny dudes.
ted.sort_values("funny_rate",ascending=True).speaker_occupation.head()


# In[ ]:


#step3:Analyze the funny rate by occupation


# In[ ]:


#x by y or x for each y wordsets used with groupby most of the time.
#for each occupation analyze funny rate.Is this dude's occupation funny or Is it about that dude specificly?


# In[ ]:



ted.groupby("speaker_occupation").funny_rate.mean().sort_values(ascending=False)
#a lot of these occupations have very small sample size 1 most of the time.


# In[ ]:


#as u can see.why its 2544 rather than 2550.bcs there are 6 null cases.
ted.speaker_occupation.describe()


# In[ ]:


#another approach-more cleaner one.the most highest ones have only 1 or 2 samples.
ted.groupby("speaker_occupation").funny_rate.agg(["mean","count"]).sort_values(by="mean",ascending=False)


# In[ ]:


#step4:focus on occupations that are well represented in the data.


# In[ ]:


occupation_counts=ted.speaker_occupation.value_counts()
occupation_counts


# In[ ]:


#lets define a frequency for our sample.then use filters.
occupation_counts[occupation_counts>=5]


# In[ ]:


#save these top occupations.
top_occupations=occupation_counts[occupation_counts>=5].index
top_occupations


# In[ ]:


#here is the result's type.Index.Index can be treated like a list.thats the key.
type(top_occupations)


# In[ ]:


#filter time using isin() returns true for the ones thats inside of that col and only true results ll be shown.
ted[ted.speaker_occupation.isin(top_occupations)]
#isin is sth like multiple OR's.lets save it.


# In[ ]:


ted_top_occupations=ted[ted.speaker_occupation.isin(top_occupations)]


# In[ ]:


#from 2544 speaker occupations,this is what we have left.786.
ted_top_occupations.shape


# In[ ]:


ted_top_occupations.groupby("speaker_occupation").funny_rate.mean().sort_values(ascending=False)
#weaknesses of these approach=5 is small sample size.
#also that performance poet dude that has done at least 5 ted talks however its all the same dude so result for performance
#poets is quite high.
#data is problematic in a sense that most of the speakers have more than 1 occupation..

