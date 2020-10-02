#!/usr/bin/env python
# coding: utf-8

# # Behind the Medals !
# 
# 
# *Hamza El Bouatmani*  - March 7th, 2019
# 
# ----
# 
# 

# # Introduction
# Although registered two years ago, I just started using the platform a couple of months ago, and was curious about how to become a Kaggle Expert or Master, so I decided to use the Kaggle Meta Dataset to dig into and examine some statistics related to Top Kernels and Top Kernel Authors.
# 
# I hope this Kernel will be useful.
# 
# Notes:
# * The Meta Kaggle Dataset is updated frequently, if you want to get the most up-to-date numbers, feel free to fork this kernel and run it.
# * I found a great amount of inconsistencies in the data, especially when it comes to KernelVersions. I write in the 'note' sections ([8](#8), [9](#9) )) how I deal with these inconsistencies, I hope that the Kaggle Team will look into them.. (Feel also free to check the code to see the details)

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Visualization
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
from plotly import tools
import plotly.figure_factory as ff
init_notebook_mode(connected=True)
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


from IPython.display import display

import os
input_data = os.listdir("../input")
#print('Files: ', input_data)


# # 1. Some Filtering <a id="1" />
# 

# In order to get the purest insights, we must take some time to clean the data we'll be working with. 
# Not all Kernels in the dataset are relevant to us. We filter the kernels as follows:
# - **Exclude Kernels with no UrlSlug**
# - **Exclude Kernels whose authors are members of the Kaggle Team (we're interested in normal users and how they get medals)**
# - **Exclude Kernels which are solutions to exercises (from Kaggle Learn section)**
# - **Exclude Kernels where CreationDate & MadePublicDate are BOTH NULL ( we don't have any idea when they were created, maybe it's a Data Collection problem )**

# In[ ]:


kernels_df = pd.read_csv('../input/Kernels.csv', usecols=['Id', 'AuthorUserId', 'CurrentKernelVersionId', 'ForkParentKernelVersionId', 'CreationDate', 'EvaluationDate', 'MadePublicDate', 'CurrentUrlSlug', 'Medal', 'MedalAwardDate', 'TotalVotes'])

init_nbr_kernels = len(kernels_df)

# Parse Date Columns
kernels_df['MadePublicDate'] = pd.to_datetime(kernels_df['MadePublicDate'])
kernels_df['CreationDate'] = pd.to_datetime(kernels_df['CreationDate'])
kernels_df['MedalAwardDate'] = pd.to_datetime(kernels_df['MedalAwardDate'])

# Exclude Kernels without Url Slug ( just two for at the time of writing )
kernels_df = kernels_df[~kernels_df['CurrentUrlSlug'].isnull()]

users_df = pd.read_csv('../input/Users.csv', index_col='Id')

# Exclude Kernels from the Kaggle Team
normal_users = users_df[users_df['PerformanceTier'] != 5]
# Replace DisplayName with UserName where DisplayName is NaN
normal_user_kernels = kernels_df[kernels_df['AuthorUserId'].isin(normal_users.index)]
normal_user_kernels = normal_user_kernels.set_index('Id')
for i, r in normal_users[pd.isnull(normal_users['DisplayName'])].iterrows():
    normal_users.at[i, 'DisplayName'] = r['UserName']
assert not normal_users['DisplayName'].isnull().any()


# Exclude Exercise Kernels which are Forked (most if not all are just forks of exercises to learn a topic from the section Kaggle Learn, they're not relevant to us)
normal_user_kernels = normal_user_kernels[ ~((normal_user_kernels['CurrentUrlSlug'].str.contains('exercise')) & (~normal_user_kernels['ForkParentKernelVersionId'].isnull()) ) ]
#assert len(normal_user_kernels[ (~normal_user_kernels['ForkParentKernelVersionId'].isnull()) & (normal_user_kernels['CurrentUrlSlug'].str.contains('exercise'))]) == 0

# Drop rows which have both dates (creation & madepublic) NULL ( ~ 190 at time of writing )
normal_user_kernels = normal_user_kernels.drop(normal_user_kernels[ (normal_user_kernels['MadePublicDate'].isnull()) & (normal_user_kernels['CreationDate'].isnull()) ].index)

# Rows that have MadePublicDate NULL and CreationDate NOT NULL: we replace the NULL in MadePublicDate with the value of CreationDate
for i, r in normal_user_kernels.iterrows():
    if pd.isnull(r['MadePublicDate']) and not pd.isnull(r['CreationDate']):
        normal_user_kernels.at[i, 'MadePublicDate'] = r['CreationDate']

# Replace NaN in 'Medal' with Zero
normal_user_kernels['Medal'] = normal_user_kernels['Medal'].fillna(0)        

# Join Kernels with Authors ( to have the author name on the same row to make things easy)
normal_user_kernels = normal_user_kernels.join(users_df, on='AuthorUserId')


oldest_date = normal_user_kernels['MadePublicDate'].min()
newest_date = normal_user_kernels['MadePublicDate'].max()
range_dates_str = f"{oldest_date.strftime('%b %Y')} ~ {newest_date.strftime('%b %Y')}"

del kernels_df
del users_df

after_nbr_kernels = len(normal_user_kernels)
print('Number of Kernels after Filtering (', range_dates_str , '): ', after_nbr_kernels, f'({init_nbr_kernels - after_nbr_kernels} Kernels filtered)')


# # 2. Medals are *<span style="color: #dca917">RARE</span>* ! <a id="2" />

# Most of us, beginners in Kaggle, might look at the Top Kernels and Top authors and think that getting Medals is easy. However, a quick look into the Meta Kaggle data shows that Kernels awarded with Medals are ***extremely RARE*** compared to the number of kernels without medals.
# 
# **(You can hover to see the actual number values)**

# In[ ]:


# Pie Chats for Total Number of Kernels

PLOT_BG_COLOR = '#f1f1f1'

kernel_colors = ['#FF9999', '#66B3FF'] # ['awarded', 'not awarded']
medal_colors  = ['#ffd448', '#e9e9e9', '#f0ba7c' ] # ['Gold', 'Silver', 'Bronze']

medal_kernels = normal_user_kernels[normal_user_kernels['Medal'] > 0]

# First Pie Chart: Awarded vs Not Awarded Kernels
vals = []
vals.append(len(medal_kernels))
vals.append(len(normal_user_kernels[normal_user_kernels['Medal'] == 0]))
chart1 = {
            'type': 'pie',
            'title': 'Awarded vs Not Awarded',
            'titlefont': {'size': 16},
            'labels': ['Kernels Awarded', 'Kernels Not Awarded'],
            'values': vals,
            'hoverinfo': 'label+value',
            'textinfo': 'percent',
            'textposition': 'inside',
            'textfont': {'size': 12},
            'marker': {'colors': kernel_colors, 'line': {'color': 'white', 'width': 2,}},
            'domain': {'x': [0, 0.4], 'y': [0, 1]}
        }

# Second Pie Chart: Gold, Silver & Bronze Kernels
vals = []
vals.append(len(medal_kernels[medal_kernels['Medal'] == 1]))
vals.append(len(medal_kernels[medal_kernels['Medal'] == 2]))
vals.append(len(medal_kernels[medal_kernels['Medal'] == 3]))



chart2 = {
            'type': 'pie',
            'title': 'Gold, Silver & Bronze',
            'titlefont': {'size': 16},
            'showlegend': False,
            'labels': ['Gold', 'Silver', 'Bronze'],
            'values': vals,
            'hoverinfo': 'label+value',
            'textinfo': 'percent+label',
            'textfont': {'size': 12},
            'marker': {'colors': medal_colors, 'line': {'color': 'white', 'width': .5,}},
            'domain': {'x': [0.6, 1], 'y': [0,1]}
        }

fig = {
    'data': [ chart1, chart2 ],
    'layout': {
        'height': 500,
        'title': {
            'text': f'Total number of Public Kernels ({range_dates_str})',
            'font': {'size': 18}
        }, 'legend': {
            'orientation': 'h'
        }
    }
}

iplot(fig)


# In[ ]:


years = list(normal_user_kernels.MadePublicDate.dt.year.unique())
years.remove(2019) # Remove this year because it has just started and has few entries
years.sort()
nbr_all_vals = []
nbr_awarded_vals = []
nbr_not_awarded_vals = []
nbr_gold_vals = []
nbr_silver_vals = []
nbr_bronze_vals = []

for y in years:
    if not np.isnan(y):
        years_kernels = normal_user_kernels[normal_user_kernels['MadePublicDate'].dt.year == y]
        nbr_all_vals.append(len(years_kernels))
        golds = len(years_kernels[years_kernels['Medal'] == 1])
        silvers = len(years_kernels[years_kernels['Medal'] == 2])
        bronzes = len(years_kernels[years_kernels['Medal'] == 3])
        nbr_awarded_vals.append(golds+silvers+bronzes)
        nbr_not_awarded_vals.append(nbr_all_vals[-1] - nbr_awarded_vals[-1])
        nbr_gold_vals.append(golds)
        nbr_silver_vals.append(silvers)
        nbr_bronze_vals.append(bronzes)
#print(years, nbr_all_vals, nbr_awarded_vals, nbr_gold_vals, nbr_silver_vals, nbr_bronze_vals)


# In[ ]:


# Bar Chart for Number of Kernels per year

fig = { 'data': [
        {   'type': 'bar',
            'name': 'Kernels w/o Awards',
            'x': years,
            'y': nbr_not_awarded_vals,
            'marker': {'color': kernel_colors[1] },
            'xaxis': 'x1',
            'yaxis': 'y1'
        },
        {   'type': 'bar',
            'name': 'Awarded Kernels',
            'x': years,
            'y': nbr_awarded_vals,
            'marker': {'color': kernel_colors[0] },
            #'line': {'color': '#ffd448' },
            'xaxis': 'x1',
            'yaxis': 'y1'
        }
], 'layout': {
        'plot_bgcolor': PLOT_BG_COLOR,
        'height': 600,
        'title': 'Change of Number of Kernels per year',
        'legend': {'orientation': 'h'},
        'xaxis': {'dtick': 1},
        'yaxis': {'dtick': 5000, 'title': 'Number of Kernels'}
    }}
iplot(fig)


# In[ ]:


# Bar & Line Chart for Awarded Kernels per Year by Medal

fig = { 'data': [
        {
            'type': 'bar',
            'name': 'Gold',
            'x': years,
            'y': nbr_gold_vals,
            'marker': {'color': medal_colors[0]},
        },
        {
            'type': 'bar',
            'name': 'Silver',
            'x': years,
            'y': nbr_silver_vals,
            'marker': {'color': medal_colors[1]},
        },
        {
            'type': 'bar',
            'name': 'Bronze',
            'x': years,
            'y': nbr_bronze_vals,
            'marker': {'color': medal_colors[2]},
        },
        {   'type': 'scatter',
            'name': 'Number of Awarded Kernels',
            'x': years,
            'y': nbr_awarded_vals,
            'line': {'color': kernel_colors[0] },
        },
    ], 'layout': {
        'title': 'Change of Number of Awarded Kernel per year',
        'legend': {'orientation': 'h'},
        'height': 600,
        'plot_bgcolor': PLOT_BG_COLOR,
        'xaxis': {'dtick': 1},
        'yaxis': {'dtick': 250, 'title': 'Number of Kernels'}
        
    }
}
iplot(fig)


# ### **<span style="color: red">Observation</span>**: Although the number of Kernels not awarded ***is much greater*** than the number of Kernels awarded, we can note a ***steady increase*** in the number of Awarded Kernels each year

# # 3. Who publishes Top Kernels ? <a id="3" />

# Let's now have a quick look at some of the Top Authors in Kaggle

# In[ ]:


nbr_medals_per_author = pd.crosstab( [normal_user_kernels['AuthorUserId'], normal_user_kernels['DisplayName']], normal_user_kernels['Medal'])
nbr_medals_per_author = nbr_medals_per_author.rename(columns={0: 'NotAwarded', 1.0: 'Gold', 2.0: 'Silver', 3.0: 'Bronze'})
nbr_medals_per_author['Awarded'] = nbr_medals_per_author['Gold'] + nbr_medals_per_author['Silver'] + nbr_medals_per_author['Bronze']
nbr_medals_per_author = nbr_medals_per_author.sort_values(by='Awarded', ascending=False)
nbr_medals_per_author = nbr_medals_per_author.reset_index(level=1) # Make DisplayName a column

n = 30
top = nbr_medals_per_author[:n]


fig = {
    'data': [
        {
            'type': 'bar',
            'y': top['Bronze'].values,
            'x': top['DisplayName'].values,
            'name': 'Bronze',
            'marker': {'color': medal_colors[2]}
        }, {
            'type': 'bar',
            'y': top['Silver'].values,
            'x': top['DisplayName'].values,
            'name': 'Silver',
            'marker': {'color': medal_colors[1]}
        }, {
            'type': 'bar',
            'y': top['Gold'].values,
            'x': top['DisplayName'].values,
            'name': 'Gold',
            'marker': {'color': medal_colors[0]}
        }
    ], 'layout': {
        'title': f'Top {n} Kernel Authors ({range_dates_str})',
        'barmode': 'stack',
        'yaxis': {'title': 'Number of Awarded Kernels'},
        'legend': {'x': 0.92, 'y': 1},
        'margin': {'r': 0},
        #'plot_bgcolor': PLOT_BG_COLOR,
    }
}

iplot(fig)


# ### **<span style="color: red">Impressive !</span> **   [Bojan Tunguz](https://www.kaggle.com/tunguz/kernels) comes in top with 72 Awarded Kernels, but there is a lot of competition between the Top 4.
# 
# *(Note: There are many other great Kernel Authors not figuring in the list. You can fork this kernel and play with the n parameter in the code, to get the Top n Authors in terms of number of awarded Kernels)*

# # 4. It's not always **<span style="color: #dca917">Gold</span>** ! <a id="4" />

# After seeing the last graph, one might think that those authors are ***Super Humans*** ! However, the **DATA** says that it's the product of **<span style="color: red">HARDWORK</span>** and **<span style="color: red">PASSION</span>**!
# 
# The following graph illustrates the proportion of Awarded & Not Awarded Kernels for each of the Top Authors :

# In[ ]:



fig = {
    'data': [
        {
            'type': 'bar',
            'y': top['NotAwarded'].values,
            'x': top['DisplayName'].values,
            'name': 'Not Awarded Kernels',
            'marker': {'color': kernel_colors[1]}
        },{
            'type': 'bar',
            'y': top['Awarded'].values,
            'x': top['DisplayName'].values,
            'name': 'Awarded Kernels',
            'marker': {'color': kernel_colors[0]}
        }
    ], 'layout': {
        'title': f'Top {n} Kernel Authors ({range_dates_str})',
        'barmode': 'stack',
        'yaxis': {'title': 'Number of Kernels'},
        'legend': {'x': 0.78, 'y': 1},
        'plot_bgcolor': PLOT_BG_COLOR,
        'margin': {'r': 0}
    }
}

iplot(fig)


# ### **<span style="color: red">Observation</span>**: Many Top Authors wrote *several non-awarded Kernels*. This shows that their success is the product of *<span style="color: red">HARDWORK</span>* ! It's not always *<span style="color: #dca917">GOLD</span>* !
# 
# *(Note: It is possible that an author deletes some of his previously published Kernels. The graph is based on the Meta Kaggle dataset which only shows currently public Kernels )*

# # 5. You <span style="color: red">CAN</span> do it too ! <a id="5" />

# ### One might also think that these Top Authors are the ones who publish the most in Kaggle. However, the **DATA** says something else !
# 
# The following graph shows the how many kernels were published by each Author Category (Preformance Tier):

# In[ ]:


nbr_awarded_kernels_per_tier = medal_kernels['PerformanceTier'].value_counts()
nbr_awarded_kernels_per_tier = nbr_awarded_kernels_per_tier.sort_index()
#nbr_awarded_kernels_per_tier

tier_colors = ['#5AC995', '#00BBFF', '#976591', '#F96517', '#DCA917']

fig = {
    'data': [{
        'type': 'pie',
        'labels': ['Novices', 'Contributors', 'Experts', 'Masters', 'Grandmasters'],
        'values': nbr_awarded_kernels_per_tier,
        'hole': .3,
        'textinfo': 'percent+label',
        'marker': {'colors': tier_colors}
    }],
    'layout': {
        'title': f'Number of Awarded Kernels by Author Tier',
        'showlegend': False
    }
}
iplot(fig)


# ### **<span style="color: red">Observation</span>**: <span style="color: #976591"> Experts</span> produce the most number of Kernels ( probably because they want to become Masters). Then followed by <span style="color: #00BBFF">Contributors</span> ! After them come <span style="color: #F96517">Masters</span> and then <span style="color: #5AC995">Novices</span> ! Lastly we have <span style="color: #DCA917">Grandmasters</span> producing ~7.8% of the Awarded Kernels (probably because there only according to the [first chart](#2) only 8.5% of the authors have reached that level)

# # 6. When did the Top Authors start publishing ?<a id="6" />

# Another interesting thing to examine, is when did the Top authors start publishing their first Kernels. In other words, how much time did it take them to reach this level.

# In[ ]:


# Date of first kernel
n = 50
top = nbr_medals_per_author.head(n)
oldest_kernel_dates = []
for userid in top.index:
    oldest_kernel_date = normal_user_kernels[normal_user_kernels['AuthorUserId'] == userid]['MadePublicDate'].min()
    oldest_kernel_dates.append(oldest_kernel_date)
oldest_kernel_dates = pd.Series(oldest_kernel_dates, index=top.index).sort_values()

# Date of first kernel

#fig = ff.create_distplot(s, [f'Top {n} authors'])


fig= {
    'data': [
        {
            'type': 'histogram',
            #'bin_size': .4,
            'marker': {"color": 'red', 'line': {'color': 'white', 'width': 2}}, 
            'x': oldest_kernel_dates,
            "opacity": 0.5, 
        }
    ],
    'layout': {
        'title': f'Dates of First Published Kernel (top {n} Authors)',
        'xaxis': {'title': 'Date of First Published Kernel'},
        'yaxis': {'title': 'Number of Authors'}
    }
}

iplot(fig)


# ### **<span style="color: red">Observation</span>**:  **More than 50%** of the Top Authors started before January 2017 ( **more than one year ago** )
# 
# (*Note: This only shows how much experience the top authors have on Kaggle, we're not taking into account their Data Science experience prior to Kaggle*)

# # 7. Tags in Top Kernels <a id="7" />

# Lastly, we examine the most used tags in the awarded Kernels.

# In[ ]:


tags_df = pd.read_csv('../input/Tags.csv')
normal_user_kernel_tags = pd.read_csv('../input/KernelTags.csv')
normal_user_kernel_tags = normal_user_kernel_tags[normal_user_kernel_tags['KernelId'].isin(normal_user_kernels.index)]
medal_kernels_tag_ids = normal_user_kernel_tags[normal_user_kernel_tags['KernelId'].isin(medal_kernels.index)]['TagId']
tags_df = tags_df.set_index('Id')
tags_dic = tags_df[['Slug', 'Name']].to_dict('index')
slugs = []
for tid in medal_kernels_tag_ids:
    slugs.append(tags_dic[tid]['Slug'])

wc=WordCloud(width=800, height=400).generate(' '.join(slugs))
plt.clf()
plt.figure( figsize=(16,9) )
plt.title('Most used Tags in Awarded Kernels', fontsize=20)
plt.imshow(wc)
plt.axis('off')
plt.show()


# In[ ]:


# Bar chart for Top used Tags in Awarded Kernels

n = 30
slug_counts = pd.Series(slugs).value_counts().head(n)

fig = {
    'data': [
        {
            'type': 'bar',
            #'orientation': 'h',
            'y': slug_counts,
            'x': slug_counts.index,
            'marker': {'color': slug_counts, 'colorscale': 'Viridis', 'showscale': True}
        }
    ], 'layout': {
        'title': f'Top {n} most used Tags in Awarded Kernels',
        'yaxis': {'title': 'Number of times used'}
    }
}
iplot(fig)


# ### **<span style="color: red">Observation</span>**:  It seems that top Kernels are directed towards **Beginners**, and are centered around **Exploratory Data Analysis** and **Visualization**

# # 8. Python vs R <a id="8" />

# Let's now see which language is most used in Awarded Kernels

# In[ ]:


normal_user_kernel_versions = pd.read_csv('../input/KernelVersions.csv', 
                                          usecols=['Id', 'KernelId', 'KernelLanguageId', 'AuthorUserId', 'VersionNumber', 'CreationDate'])
normal_user_kernel_versions.set_index('Id', inplace=True)

#normal_user_kernels.set_index('Id', inplace=True)

# Drop All versions which have KernelId NaN
normal_user_kernel_versions = normal_user_kernel_versions.drop(
    normal_user_kernel_versions[normal_user_kernel_versions['KernelId'].isnull()].index, axis=0)

# Drop All versions which have VersionNumber NaN
normal_user_kernel_versions = normal_user_kernel_versions.drop(
    normal_user_kernel_versions[normal_user_kernel_versions['VersionNumber'].isnull() ].index, axis=0)

kernel_ids_with_null_current_version = list(normal_user_kernels[pd.isnull(normal_user_kernels['CurrentKernelVersionId'])].index)
#print('There are ', len(kernel_ids_with_null_current_version), 'Kernels with null CurrentKernelVersionId')
null_kvs = normal_user_kernel_versions[normal_user_kernel_versions['KernelId'].isin(kernel_ids_with_null_current_version)]

# Try to find the CurrentKernelVersionId for the Kernels that have them NaN
for i, r in normal_user_kernels[normal_user_kernels.index.isin(kernel_ids_with_null_current_version)].iterrows():
    kvs = null_kvs[null_kvs['KernelId'] == i]
    if len(kvs) == 1:
        normal_user_kernels.at[i, 'CurrentKernelVersionId'] = kvs.index.values[0]
    elif len(kvs) == 0:
        pass
        #print('WTF: Kernel ', i )
    else:
        r= kvs[kvs['CreationDate'] == kvs['CreationDate'].max()]
        if len(r) == 1:
            normal_user_kernels.at[i, 'CurrentKernelVersionId'] = r.index.values[0]
        else:
            normal_user_kernels.at[i, 'CurrentKernelVersionId'] = r.iloc[0].index.values[0]

kernel_languages_dic = pd.read_csv('../input/KernelLanguages.csv', usecols=['Id', 'DisplayName'],index_col='Id')
kernel_languages_dic = kernel_languages_dic.to_dict('index')

# For each kernel which has a valid CurrentKernelVersionId, fill the language column with the appropriate Language
normal_user_kernels['KernelLanguage'] = 'Unknown'
for i,k in normal_user_kernels[normal_user_kernels['CurrentKernelVersionId'].isin(normal_user_kernel_versions.index)].iterrows():
    kv_id = k['CurrentKernelVersionId']
    x = normal_user_kernel_versions.loc[kv_id]
    lan_id = x['KernelLanguageId']
    #print(lan_id)
    if lan_id in kernel_languages_dic.keys():
        language = kernel_languages_dic[lan_id]['DisplayName']
        normal_user_kernels.at[i, 'KernelLanguage'] = language


# In[ ]:


ct1 = pd.crosstab(normal_user_kernels['AuthorUserId'], normal_user_kernels['KernelLanguage'])
ct2 = pd.crosstab(normal_user_kernels['AuthorUserId'], normal_user_kernels['Medal'])
author_stats = ct1.join(ct2)
author_stats = author_stats.join(normal_users['DisplayName'])
for i, r in author_stats.iterrows():
    if (r['Unknown'] > 0):
        if r['Python'] != r['R']:
            if r['Python'] > r['R']:
                author_stats.at[i, 'Python'] = r['Python']+r['Unknown']
            elif r['R'] > r['Python']:
                author_stats.at[i, 'R'] = r['Unknown']+r['R']
            author_stats.at[i, 'Unknown'] = 0
        elif (r['Python'] == r['R']) and (r['Python'] > 0):
            x = int(r['Unknown']/2)
            author_stats.at[i, 'Python'] = x
            author_stats.at[i, 'R'] = x
            author_stats.at[i, 'Unknown'] = 0 if x%2 == 0 else 1
author_stats = author_stats.rename(columns={
    0:'NbrNotAwardedKernels',
    'Python':'NbrPythonKernels',
    'R':'NbrRKernels',
    'Unknown':'UnknownLanguageKernels',
    'DisplayName': 'UserDisplayName',})
author_stats['NbrAwardedKernels'] = author_stats[1] + author_stats[2] + author_stats[3]
author_stats.drop([1,2,3], axis=1, inplace=True)
medal_author_stats = author_stats[author_stats['NbrAwardedKernels'] > 0]
nbr_python_awarded_kernels = medal_author_stats['NbrPythonKernels'].sum()
nbr_r_awarded_kernels = medal_author_stats['NbrRKernels'].sum()
nbr_unknown_awarded_kernels = medal_author_stats['UnknownLanguageKernels'].sum()


# In[ ]:



fig = {
    'data': [
        {
            'type': 'pie',
            'values': [nbr_python_awarded_kernels, nbr_r_awarded_kernels, nbr_unknown_awarded_kernels],
            'labels': ['Python', 'R', 'Other'],
            'marker': {'colors': ['#FFD548','#2167BA', 'grey']},
            'textinfo': 'percent+label',
            'hole': .3,
            'showlegend': False
        }
    ],
    'layout': {
        'title': 'Awarded Kernels by Language'
    }

}

iplot(fig)


# ### **<span style="color: red">Observation</span>**:  Python is largely used and preferred in Awarded Kernels.
# 
# 
# #### **<span style="color: red">Important Note</span>**
# 
# ***I found many inconsistencies in the KernelVersions table:***
# * Many Kernels have a NaN CurrentKernelVersionId (~32.000)
# * Many Kernels have no KernelVersions !
# * Many KernelVersions have unknown Kernel Language Ids
# 
# ***To mitigate the effect of those problems on the results, I did the following:***
# * I manually searched for and set the latest versions of Kernels who don't have a CurrentKernelVersionId 
# * For the Kernels with unknown KernelLanguageId, I assumed that they were written in the language that their Authors wrote most of their kernels with.
# ** *

# # 9. Top Kernel Data Sources <a id="9" />

# Kernels can have as a data source a **competition's dataset** or in a **normal dataset** ( or both ). Let's examine the data sources of Awarded Kernels.

# In[ ]:


# Imports
normal_user_kernel_version_competitions = pd.read_csv('../input/KernelVersionCompetitionSources.csv')
#print(len(normal_user_kernel_version_competitions))
normal_user_kernel_version_competitions = normal_user_kernel_version_competitions[normal_user_kernel_version_competitions['KernelVersionId'].isin(normal_user_kernel_versions.index.values)]
#print(len(normal_user_kernel_version_competitions))

normal_user_kernel_version_datasets = pd.read_csv('../input/KernelVersionDatasetSources.csv')
#print(len(normal_user_kernel_version_datasets))
normal_user_kernel_version_datasets = normal_user_kernel_version_datasets[normal_user_kernel_version_datasets['KernelVersionId'].isin(normal_user_kernel_versions.index.values)]
#print(len(normal_user_kernel_version_datasets))

#dataset_nbr_kernels = pd.read_csv('../input/Datasets.csv', usecols=['Id', 'TotalKernels'], index_col='Id')
#dataset_nbr_kernels['NbrAwardedKernels'] = 0

#competition_nbr_kernels = pd.read_csv('../input/Competitions.csv', usecols=['Id', 'HasKernels'], index_col='Id')
#competition_nbr_kernels = competition_nbr_kernels[competition_nbr_kernels['HasKernels'] == True]
#competition_nbr_kernels['NbrAwardedKernels'] = 0


# Add NbrCompetitions & NbrDatasets to normal_user_kernels
normal_user_kernels['NbrCompetitions'] = 0
normal_user_kernels['NbrDatasets'] = 0

for i, r in normal_user_kernels.iterrows():
    ckvid = r['CurrentKernelVersionId']
    if not np.isnan(ckvid):
        ckvid = int(ckvid)
        comps = set(normal_user_kernel_version_competitions[normal_user_kernel_version_competitions['KernelVersionId'] == ckvid]['SourceCompetitionId'])
        dats  = set(normal_user_kernel_version_datasets[normal_user_kernel_version_datasets['KernelVersionId'] == ckvid]['SourceDatasetVersionId'])
        normal_user_kernels.at[i, 'NbrCompetitions'] += len(comps)
        normal_user_kernels.at[i, 'NbrDatasets'] += len(dats)
#        if r['Medal'] > 0:
#            #print(ckvid)
#        #    if nbr_comps > 0:
#                for compID in comps:
#                    if compID in competition_nbr_kernels.index.values:
#                        competition_nbr_kernels.at[compID, 'NbrAwardedKernels'] += 1
#            if nbr_dats > 0:
#                for datID in dats:
#                    if datID in dataset_nbr_kernels.index.values:
#                        dataset_nbr_kernels.at[datID, 'NbrAwardedKernels'] += 1
#                    else:
#                        print(datID)


medal_kernels = normal_user_kernels[normal_user_kernels['Medal'] > 0]

nbr_competitions = medal_kernels['NbrCompetitions'].sum()
nbr_datasets = medal_kernels['NbrDatasets'].sum()


# In[ ]:



fig = {
    'data': [
        {
            'type': 'pie',
            'values': [nbr_competitions, nbr_datasets],
            'labels': ['Competitions', 'Datasets'],
            'marker': {'colors': ['#FFCD07','#00BF77']},
            'textinfo': 'percent+label',
            'hole': .3,
            'showlegend': False
        }
    ],
    'layout': {
        'title': 'Awarded Kernels by Data Source'
    }

}

iplot(fig)


# ### **<span style="color: red">Observation</span>**:  There is no stark preference for either. Awarded Kernels use as Dataset Sources both Competition Datasets & Normal Datasets with approximately the same proportion.
# 
# **Note**: 
# * There are Kernels which have multiple sources, I counted all the sources of each kernel)*
# * Many *DatasetSourceIds* in *KernelVersionDatasetsources* are not present in the *Datasets* table.

# # 10. Time for some Correlation ! <a id="10" />

# In[ ]:


# Add MonthsOfExperience Field
oldest_kernel_dates = []
for userid in author_stats.index:
    oldest_kernel_date = normal_user_kernels[normal_user_kernels['AuthorUserId'] == userid]['MadePublicDate'].min()
    oldest_kernel_dates.append(oldest_kernel_date)

oldest_kernel_dates = pd.Series(oldest_kernel_dates, index=author_stats.index)
oldest_kernel_dates = ((pd.Timestamp.now() - oldest_kernel_dates)/ np.timedelta64(1,'M')).astype('int')
nbr_medals_per_author['MonthsOfExperience'] = oldest_kernel_dates
#nbr_medals_per_author.head()

# Add NumberPublishedKernels Field
author_stats['NbrPublishedKernels'] = author_stats['NbrNotAwardedKernels'] + author_stats['NbrAwardedKernels']
#author_stats.head()

top_tags = tags_df[tags_df['Slug'].isin(slug_counts.index)].index

author_stats['NbrTopTagsUsed'] = 0
for userid in author_stats.index:
    kernel_ids = list(normal_user_kernels[normal_user_kernels['AuthorUserId'] == userid].index.values)
    tag_ids = normal_user_kernel_tags[normal_user_kernel_tags['KernelId'].isin(kernel_ids)]['TagId']
    relevant_tag_ids = [tid for tid in tag_ids if tid in top_tags]
    author_stats.at[userid, 'NbrTopTagsUsed'] = len(relevant_tag_ids)
#author_stats.sample(5)


# In[ ]:


df = author_stats[['NbrAwardedKernels', 'NbrPublishedKernels', 'NbrTopTagsUsed', 'NbrPythonKernels', 'NbrRKernels', 'NbrNotAwardedKernels',]]
corr = df.corr()
fig = {
    'data': [
        {
            'type': 'heatmap',
            'z': corr,
            'x': df.columns,
            'y': df.columns,
            'colorscale': 'Reds'
        }
    ],
    'layout': {
        'title': 'Correlation Heatmap',
        'margin':{
            'l': 140
        }
    }
}

iplot(fig)


# ### **<span style="color: red">Observation</span>**:  We are interested in **Number of Awarded Kernels** and what it's most correlated with, and the results are :
# 1. Number of Top Tags User
# 2. Number of Published Kernels
# 3. Number of Python Kernels
# 4. Number of R Kernels
# 5. Number of Not Awarded Kernels

# # Conclusions:

# 
# * Most Awarded Kernels are Tutorials and Visualizations
# 
# * Most Awarded Kernels are written in Python
# 
# * There are of course many criteria other than the ones mentioned for a Kernel to be successful, for example: It must be written and formatted nicely, must add value to the reader and be interesting.
# 
# * In Data Science as in Every Discipline, Success comes with two principal ingredients: **<span style="color: red">PASSION & HARDWORK</span>**

# ## References:
# 
# * [Kaggle Progression System](https://www.kaggle.com/progression) (Page)
# * [Kaggle Trends](https://www.kaggle.com/gaborfodor/kaggle-trends) (Kernel)
# * [How to get upvotes in Kaggle](https://www.kaggle.com/aleksandradeis/how-to-get-upvotes-for-a-kernel-on-kaggle) (Kernel)
