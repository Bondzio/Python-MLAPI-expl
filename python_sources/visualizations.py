#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

##MatplotLib Styles##
print(plt.style.available)
plt.style.use('fivethirtyeight')


# In[2]:


dl = pd.read_csv('../input/likes_0.csv') 
dv = pd.read_csv('../input/views_0.csv')
dt = pd.read_csv('../input/times_0.csv')
dc = pd.read_csv('../input/idonly_no_comments.csv')
print(dl.head(1))
print(dv.head(1))
print(dt.head(1))
print(dc.head(1))


# In[3]:


import re
def values(x):
    x = x.split("-")
    return(x[0])

dv['Unnamed: 0'] = dv['Unnamed: 0'].apply(values)
dl['Unnamed: 0'] = dl['Unnamed: 0'].apply(values)
dt['Post-id'] = dt['Post-id'].apply(values)

dc['Post Id'] = dc['Post Id'].apply(values)


# In[4]:


print(dl.head(1))
print(dv.head(1))
print(dt.head(1))
print(dc.head(1))


# In[5]:


dl = dl.rename(columns={'Unnamed: 0' : 'ID', '0' : 'likes'})
dl.set_index('ID', inplace = True)

dv = dv.rename(columns={'Unnamed: 0' : 'ID', '0' : 'Views'})
dv.set_index('ID', inplace = True)

dt = dt.rename(columns={'Post-id' : 'ID', 'Time' : 'Date'})
dt.set_index('ID', inplace = True)

dc = dc.rename(columns={'Post Id' : 'ID', 'Total Comments ' : 'Comments'})
dc.set_index('ID', inplace = True) 


# In[6]:


print(dl.head(1))
print(dv.head(1))
print(dt.head(1))
print(dc.head(1))


# In[ ]:





# In[7]:




def clean(x):
    x = x.replace("likes", " ")
    x = x.replace("views", " ")
    x = x.replace(',',"")
    x = x.replace('3 DAYS AGO', 'MAY 9')
    x = x.replace('5 DAYS AGO', 'MAY 7')
    x = x.replace('7 DAYS AGO', 'MAY 5')
    x = x.replace('6 DAYS AGO', 'MAY 6')

    return(x)


dl['likes'] = dl['likes'].apply(clean)
dv['Views'] = dv['Views'].apply(clean)
dt['Date'] = dt['Date'].apply(clean)


# In[8]:


print(dl.head(1))
print(dv.head(1))
print(dt.head(1))
print(dc.head(1))


# def months(x):
#     x = x.split(" ")
#     return(x[0])
# dt['Date'] = dt['Date'].apply(months)
# dt

#  **PIE CHART for toatal Videos and Images**

# In[9]:


print('Total No. Of Viedos Posted :', dv.shape[0])
print('Total No. Of Images Posted :', dl.shape[0])
print('Total No. Of Comments Posted:',dc.shape[0])


# In[10]:



labels = ['Videos','Images']
sizes = [dv.shape[0], dl.shape[0]]
colors =['purple','pink']
plt.pie(sizes,colors = colors, shadow =True,autopct='%1.1f%%',explode = (0, 0.1))
plt.legend(labels, loc="best")
plt.title('Proportion of Videos and Images Posted')
plt.axis('equal')
plt.show()


# In[11]:


dl['likes'] = dl['likes'].astype('int')
dv['Views'] = dv['Views'].astype('int')
dc['Comments']=dc['Comments'].astype('int')


# **PIE CHART for Total Views, Likes and  Comments **

# In[12]:


print('Total Views for all Videos Posted:', dv['Views'].sum())
print('Total Likes for all Photos Posted:', dl['likes'].sum())
print('Total comments for all content:', dc['Comments'].sum())


# In[13]:


labels = ['Views','Likes','comments']
sizes = [dv['Views'].sum(),dl['likes'].sum(), dc['Comments'].sum()]
colors =['purple','pink', 'blue']
plt.pie(sizes,colors = colors, shadow =True,autopct='%1.1f%%',explode = (0.1,0,0))

plt.legend(labels, loc="best")
plt.title('Proportion of Views and Likes Posted')
plt.axis('equal')
plt.show()


# 
# 
# toplikes = dl.sort_values(by =['likes'],ascending = False)
# topviews = dv.sort_values(by =['Views'],ascending = False)
# topcomm = dc.sort_values(by = ['Comments'], ascending = False)
# toplikes
# 
# 
'''

top5likes = toplikes.head(5)
top5views = topviews.head(5)
top5comm = topcomm.head(5)
top5comm
'''
# **Joining Datasets with Time**

# In[14]:


lt = dl.join(dt, how = 'outer')
lt = lt.dropna(axis = 0)

vt = dv.join(dt, how = 'outer')
vt = vt.dropna(axis=0)

ct = dc.join(dt,how = 'outer')
ct = ct.dropna(axis=0)


# In[15]:


print(lt.head(1))
print(vt.head(1))
print(ct.head(1))


# **Getting TOP Likes, Comments, Views**

# In[16]:


lt_likes_sorted = lt.sort_values(by=['likes'], ascending = False)


vt_views_sorted = vt.sort_values(by=['Views'], ascending = False)

ct_Comm_sorted = ct.sort_values(by =['Comments'],ascending = False)

Top5comm = ct_Comm_sorted.head(5)

#lt_likes_sorted = lt_likes_sorted.drop(lt.index[[0,4]])
Top5likes = lt_likes_sorted.head(5)

Top5views = vt_views_sorted.head(5)


# In[17]:


print(Top5likes)
print(Top5views)
print(Top5comm)


# **BARPLOT for TOP5Likes**

# In[25]:


ax =Top5likes.set_index('Date').plot(kind = 'bar',color = 'purple')
ax.set_xlabel(' ')
ax.set_ylabel('Likes')
plt.title('Top 5 likes-BarPlot')


rects = ax.patches

for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label.
    space = 5
    # Vertical alignment for positive values
    

    # Create annotation
    plt.annotate(
        y_value,                     # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(0, space),          # Vertically shift label by `space`
        textcoords="offset points", # Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        )                      # Vertically align label differently for
                                    # positive and negative values.

plt.show()



# **BARPLOT for TOP5 Views**

# In[26]:


ax =Top5views.set_index('Date').plot(kind = 'bar',color = 'purple')

ax.set_ylabel('Views')
plt.title('Top 5 Views- BarPlot')
ax.set_xlabel(' ')

rects = ax.patches

for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label.
    space = 5
    # Vertical alignment for positive values
    

    # Create annotation
    plt.annotate(
        y_value,                     # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(0, space),          # Vertically shift label by `space`
        textcoords="offset points", # Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        )                      # Vertically align label differently for
                                    # positive and negative values.

plt.show()



# **BARPLOT for TOP5 Comments**

# In[27]:


ax =Top5comm.set_index('Date').plot(kind = 'bar',color = 'purple')
ax.set_xlabel(' ')
ax.set_ylabel('Comments')
plt.title('Top 5 Comments-BarPlot')


rects = ax.patches

for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label.
    space = 5
    # Vertical alignment for positive values
    

    # Create annotation
    plt.annotate(
        y_value,                     # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(0, space),          # Vertically shift label by `space`
        textcoords="offset points", # Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        )                      # Vertically align label differently for
                                    # positive and negative values.

plt.show()



# **LINE PLOT for TOP5 Likes**

# In[28]:


lt.set_index('Date').plot(kind = 'line', color = 'purple')
plt.ylabel('No. of Likes')
plt.title('Variation of Likes Count within Each Posts')
plt.xlabel('Months')

plt.show()


# **LINE PLOT for TOP5 Views**

# In[29]:


print(dv.max())
print(dv.idxmax())


# In[30]:



ax = vt.set_index('Date').plot(kind = 'line', color = 'purple')
ax.set_xlabel('Months')
ax.set_ylabel('No. of Views')
ax.set_title('Variation of Views within Each Posts')
plt.text(35, 12000, '\nPostid 0.50071 with \n16363 views')



plt.show()


# **LINE PLOT for TOP5 Comments**

# In[31]:


ax = ct.set_index('Date').plot(kind = 'line', color = 'purple')
ax.set_ylabel('No. of Comments')
ax.set_xlabel("Months")
ax.set_title('Variation of Comments within Each Posts')




plt.show()


# **HISTOGRAM  for Likes**

# In[32]:


ax =lt.plot(kind = 'hist',bins = 25,color = 'purple',figsize = (8,8))

rects = ax.patches

for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label.
    space = 5
    # Vertical alignment for positive values
    

    # Create annotation
    plt.annotate(
        y_value,                     # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(0, space),          # Vertically shift label by `space`
        textcoords="offset points", # Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        )                      # Vertically align label differently for
                                    # positive and negative values.





ax.set(xlabel ='No. of Likes')
ax.set_title('Likes Frequency-Histogram')

plt.show()


# **HISTOGRAM for  Views**

# In[33]:


ax =vt.plot(kind = 'hist',bins = 10,range = (0,2000),color = 'purple')

ax.set(xlabel ='No. of Views')
ax.set_title('Views Frequency-Histogram')

rects = ax.patches

for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label.
    space = 5
    # Vertical alignment for positive values
    

    # Create annotation
    plt.annotate(
        y_value,                     # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(0, space),          # Vertically shift label by `space`
        textcoords="offset points", # Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        )                      # Vertically align label differently for
                                    # positive and negative values.

plt.show()

plt.show()


# **HISTROGRAM for Comments**

# In[34]:


ax =dc.plot(kind = 'hist',range = (0, 30),color = 'purple')

ax.set(xlabel ='No. of Comments')
ax.set_title('Comments Frequency-Histogram')

rects = ax.patches

for rect in rects:
    # Get X and Y placement of label from rect.
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label.
    space = 5
    # Vertical alignment for positive values
    

    # Create annotation
    plt.annotate(
        y_value,                     # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(0, space),          # Vertically shift label by `space`
        textcoords="offset points", # Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        )                      # Vertically align label differently for
                                    # positive and negative values.

plt.show()

plt.show()


# **Cleaning Date Column For GettingOnly  Months**

# In[35]:


lt.head()
def month(x):
    x = x.split('-')
    return x[0]
lt['Date'] = lt['Date'].apply(month)
lt.head()
vt['Date'] = vt['Date'].apply(month)
ct['Date'] = ct['Date'].apply(month)


# In[36]:


print(lt.head(1))
print(vt.head(1))
print(ct.head(1))


# **STRIPPLOT for LIKES**

# In[37]:



sns.stripplot(x = 'Date', y= 'likes',jitter=True, data = lt,  palette = 'PuRd_r')

plt.title('Distribution of Likes across Months\n StripPlot')
plt.show()


# **STRIPPLOT for VIEWS**

# In[38]:



ax=sns.stripplot(x = 'Date', y= 'Views', data = vt, jitter=True,  palette = 'PuRd_r')
ax.set_ylim([0,2000])

plt.title('Distribution of Views across Months\n StripPlot')
plt.show()


# **STRIPPLOT for COMMENTS**

# In[39]:


ax=sns.stripplot(x = 'Date', y= 'Comments', data = ct, jitter=True,  palette = 'PuRd_r')
ax.set_ylim([0,110])

plt.title('Distribution of Comments across Months\n StripPlot')
plt.show()


# **SWARMPLOT for LIKES**

# In[40]:


sns.swarmplot(x='Date', y = 'likes',data = lt, palette = 'PuRd_r')
plt.title('SwarmPlot of Likes across Months')
plt.show()


# **SWARMPLOT for VIEWS**

# In[41]:


ax =sns.swarmplot(x='Date', y = 'Views',data = vt, palette = 'PuRd_r')
ax.set_ylim([0,2000])
plt.title('SwarmPlot of Views across Months')
plt.show()


# **SWARMPLOT for COMMENTS**

# In[42]:


ax =sns.swarmplot(x='Date', y = 'Comments',data = ct, palette = 'PuRd_r')
ax.set_ylim([0,110])
plt.title('SwarmPlot of Comments across Months')
plt.show()


# # ViolinPlot combines a boxplot with the kernel density estimation procedure

# **VIOLIN LIKES**

# In[43]:


sns.violinplot(x='Date', y ='likes', data = lt, palette = 'PuRd_r')
plt.title('Violinplot for Likes distibution')
plt.xlabel(' ')
plt.show()


# **VIOLIN VIEWS**

# In[44]:


sns.violinplot(x='Date', y ='Views', data = vt, palette = 'PuRd_r',)
plt.xlabel('Months')
plt.ylim(0,5000)
plt.title('Violinplot for Views distibution')
plt.xlabel(" ")
plt.show()


# **VIOLIN COMMENTS**

# In[45]:


sns.violinplot(x='Date', y ='Comments', data = ct, palette = 'PuRd_r',)
plt.ylim(0,110)
plt.title('Violinplot for Comments distibution')
plt.xlabel(" ")
plt.show()


# **VIOLIN AND SWARM fro LIKES**

# In[46]:


sns.violinplot(x='Date', y ='likes', data = lt, inner = None, palette = 'PuRd_r')
sns.swarmplot(x='Date', y = 'likes',data = lt, color= 'w')
plt.title('Each observation along with summary of Distribution\n Likes')
plt.xlabel(" ")
plt.show()


# **VIOLIN AND SWARM fro VIEWS**

# In[47]:


sns.violinplot(x='Date', y ='Views', data = vt, inner = None, palette = 'PuRd_r')
sns.swarmplot(x='Date', y = 'Views',data = vt, color= 'w')
plt.title('Each observation along with summary of Distribution\n Views')
plt.ylim(0,5000)
plt.xlabel(" ")
plt.show()


# **VIOLIN AND STRIP foR COMMENTS**

# In[48]:


sns.violinplot(x='Date', y ='Comments', data = ct, inner= None, palette = 'PuRd_r')
sns.stripplot(x='Date', y = 'Comments',data = ct, color= 'w')
plt.title('Each observation along with summary of Distribution\n Comments')
plt.ylim(-20,110)
plt.xlabel(" ")
plt.show()


# **COUNTPLOT for LIKES**

# In[49]:


ax = sns.countplot(x = 'Date', data = lt, palette = 'PuRd_r')
plt.title('CountPlot for Likes')
ncount = len(lt)

for p in ax.patches:
    x=p.get_bbox().get_points()[:,0]
    y=p.get_bbox().get_points()[1,1]
    ax.annotate('{:.1f}%'.format(100.*y/ncount), (x.mean(), y), 
            ha='center', va='bottom')

plt.xlabel(" ")
plt.show()


# **COUNTPLOT for VIEWS**

# In[50]:


ax = sns.countplot(x = 'Date', data = vt, palette = 'PuRd_r')
plt.title('CountPlot for Views')
ncount = len(lt)

for p in ax.patches:
    x=p.get_bbox().get_points()[:,0]
    y=p.get_bbox().get_points()[1,1]
    ax.annotate('{:.1f}%'.format(100.*y/ncount), (x.mean(), y), 
            ha='center', va='bottom')

plt.xlabel(" ")
plt.show()


# **COUNTPLOT for COMMENTS**

# In[51]:


ax = sns.countplot(x = 'Date', data = ct, palette = 'PuRd_r')
plt.title('CountPlot for Comments')
ncount = len(lt)

for p in ax.patches:
    x=p.get_bbox().get_points()[:,0]
    y=p.get_bbox().get_points()[1,1]
    ax.annotate('{:.1f}%'.format(100.*y/ncount), (x.mean(), y), 
            ha='center', va='bottom')

plt.xlabel(" ")
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




