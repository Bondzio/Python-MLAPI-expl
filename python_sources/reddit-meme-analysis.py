#!/usr/bin/env python
# coding: utf-8

# # **Reddit Meme Analysis**
# The project is divided into the following parts
#     1. Getting the Data and preparing it
#     2. factors affecting the upvote ie day, month , year , hour, lenght of title

# # 1. Getting the Data and preparing it
#   - First of all getting the json data into DataFrame as it is easy to work with.
#   - convert the time in created_utc (unixtime) into a DateTime then extract year, month and day and hour.

# In[1]:


import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import json 
from pandas.io.json import json_normalize


# In[2]:


with open("../input/db.json",'r') as f:
    d = json.load(f)
d = d['_default']


# In[3]:


k=DataFrame([])
dframe=DataFrame([])
for i in d:
    k = json_normalize(d[i])
    dframe = dframe.append(k)


# In[4]:


dframe.index=range(len(d))
dframe.head()


# In[5]:


# Converting the time into DateTime format
i1=0
dc = Series(range(len(dframe['created_utc'])))
for i in dframe['created_utc']:
    dc[i1]= datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
    i1=i1+1
dframe['date_created'] = dc


# In[6]:


# Splitting the DataTime to get different values of Day Month Year and Hour
import re
k = Series(range(len(dframe['date_created'])))
for i in range(len(dframe['date_created'])):
    k[i]= re.split('[ :-]',dframe['date_created'][i])
dframe['daytime'] = k


# In[7]:


y1 = Series(range(len(dframe['daytime'])))
m1 = Series(range(len(dframe['daytime'])))
d1 = Series(range(len(dframe['daytime'])))
h1 = Series(range(len(dframe['daytime'])))
min1 = Series(range(len(dframe['daytime'])))
sec1 = Series(range(len(dframe['daytime'])))
for i in range(len(dframe['daytime'])):
    y1[i] = dframe['daytime'][i][0]
    m1[i] = dframe['daytime'][i][1]
    d1[i] = dframe['daytime'][i][2]
    h1[i] = dframe['daytime'][i][3]
    min1[i] = dframe['daytime'][i][4]
    sec1[i] = dframe['daytime'][i][5]
mm1=m1
dframe['year'] = y1
dframe['day'] = d1
dframe['hour'] = h1 + min1/60.0 + sec1/3600.0
dframe['abs_hour'] = np.round(dframe['hour'])
dframe['mm1'] = mm1


# In[8]:


for m2 in range(len(m1)):
    if (m1[m2]==1):
        m1[m2]='Jan'
    elif (m1[m2]==2):
        m1[m2]='Feb'
    elif (m1[m2]==3):
        m1[m2]='Mar'
    elif (m1[m2]==4):
        m1[m2]='Apr'
    elif (m1[m2]==5):
        m1[m2]='May'
    elif (m1[m2]==6):
        m1[m2]='June'
    elif (m1[m2]==7):
        m1[m2]='July'
    elif (m1[m2]==8):
        m1[m2]='Aug'
    elif (m1[m2]==9):
        m1[m2]='Sept'
    elif (m1[m2]==10):
        m1[m2]='Oct'
    elif (m1[m2]==11):
        m1[m2]='Nov'
    elif (m1[m2]==12):
        m1[m2]='Dec'
dframe['month'] = m1


# In[9]:


# getting area of thumbnail
dframe['area_thumbnail']=dframe['thumbnail.height']*dframe['thumbnail.width']
dframe.head(3)


# In[10]:


dframe.describe()


# So there are 3226 entries,
# the std of ups(upvoted) is greater than its mean may be due to data is spreaded away from its center

# # Factors affecting the upvotes
#  - area of thumbnail, hour month year and day when it is posted
#  - top contributers
#  - does uploading more gets more upvotes
#  - leght of thumbnail

# In[11]:


# Box plot
fig, ax = plt.subplots()
ax.boxplot([dframe['ups'],dframe['area_thumbnail']],sym='')
plt.show()


# ups data is spreaded away from its center

# In[12]:


# Distribution of ups
sns.distplot(dframe['ups'], color="r")


# There are few post with ups greater han 150000

# In[13]:


sns.distplot(dframe['area_thumbnail'], color="b")


# The area of thumbnail for most post is around 19000

# In[14]:


f1= plt.subplots(1, figsize=(7, 7))
sns.violinplot(data=dframe,y='area_thumbnail', palette="Set3",axis1=[0])


# This shows a better representation, most of the area data is concentrated at the top

# In[15]:


f1= plt.subplots(1, figsize=(7, 4))
sns.regplot(x='area_thumbnail', y='ups', data=dframe,order=3)


# Area of thumbnail not much effect the ups unless it is less than 6000, ups reduces significantly

# In[16]:


f1= plt.subplots(figsize=(7, 7))
sns.violinplot(y=dframe['mm1'], palette="Set3",axis1=[0])
plt.title('Distribution of data wrt Month')


# peak shows maximum upload of meme around march, and second peak around end of october

# In[17]:


f1= plt.subplots(1, figsize=(10, 8))
sns.violinplot(x='month',y='ups',data=dframe, palette="Set3")
plt.title('violin plot of ups for differrent month')


# violin plot shows ups in december are more spread out

# In[18]:


f1= plt.subplots(1, figsize=(10, 5))
sns.barplot(x='month',y='ups',data=dframe)
plt.title('Upvotes vs Month')


# Even though March has maximum uploades, the avg upvotes are minimum and the total upvotes in October are maximum and uploades are high too.

# In[19]:


f1= plt.subplots(1, figsize=(10, 8))
dfs = pd.pivot_table(dframe,values='ups',index='month',columns='year')
sns.heatmap(dfs,annot=True,fmt='f')
plt.title('Heatmap for ups at different month and year')


# The heatmap shows the total ups for different month and year, May 2016 has the highest upvotes

# In[20]:


f1= plt.subplots(1, figsize=(7, 6))
sns.barplot(x='year',y='ups',data=dframe)


# The average ups of 2017 and 2018 are very less as compaired to the 2015

# In[21]:


f1= plt.subplots(1, figsize=(10, 7))
from collections import Counter
yyy = Counter(dframe['year'])
yyy1 = DataFrame(yyy,index=range(1))
for i in yyy1:
    plt.bar(i,yyy1[i], align='center',color='lightsteelblue')
plt.grid()
plt.title('Memes in a year')


# as most of the data is from 2017 and 2018 because of this the average ups is less

# In[22]:


f1= plt.subplots(1, figsize=(7, 4))
sns.distplot(dframe['abs_hour'], color="indianred")
plt.title('memes distribution wrt hour')


# the plot shows,most memes are uploaded around late afternoon and at late night

# In[23]:


f1= plt.subplots(1, figsize=(10, 8))
dfs1 = pd.pivot_table(dframe,values='ups',index='abs_hour',columns='year')
sns.heatmap(dfs1,annot=True,fmt='f')
plt.title('Heatmap showing ups at different hour and year')


# Consider 2017 memes are upvoted more during late night than there is dip in the afternoon and rises again in later afternoon and night

# In[24]:


f1= plt.subplots(1, figsize=(15, 6))
sns.barplot(x='abs_hour',y='ups',data=dframe)
plt.title('Hour vs Upvotes')


# So the best time to post the meme to get maximum upvotes is early morning aroung 8 o clock

# In[25]:


f1= plt.subplots(1, figsize=(7, 4))
sns.distplot(dframe['day'], color="indianred")


# Number of memes uploaded are same throughout the month

# In[26]:


from collections import Counter
mylist = dframe['author'] 
counts = Counter(mylist)


# In[27]:


# Getting the top 10 contributor
z=0
z1=0
k=Series(range(11))
k1=pd.Series(range(11))
a1_sorted_keys = sorted(counts, key=counts.get, reverse=True)
for r in a1_sorted_keys:
    z=z+1
    if(z<12):
        k[z1]=r
        k1[z1]=counts[r]
        z1=z1+1
print (k)


# In[28]:


# Getting total upvotes avg upvotes and times uploaded
z1=0
kk=Series(range(11))
kk1=pd.Series(range(11))
for r1 in a1_sorted_keys:
        kk[z1]=r1
        kk1[z1]=counts[r1]
        z1=z1+1


# In[29]:


sum=0
up1=pd.Series(range(2168))
up2=pd.Series(range(2168))
for i1 in range(2168):
    for i in range(3162):
        if (dframe['author'][i]== kk[i1]):
            sum = sum + dframe['ups'][i]
            up1[i1]=sum
    sum = 0


# In[30]:


df1 = DataFrame()
df1['top']=kk
df1['times_uploaded']=kk1
df1['total_ups']=up1
df1['avg_ups'] = up1/kk1


# In[31]:


plt.rcParams['figure.figsize'] = (18,8)
plt.bar(k,k1,align='center',color='skyblue')
plt.title("Top 10 contributers")
plt.ylabel('No of memes posted')
plt.xlabel('Author')


# plot shows that HoLoFan4life is the maximum contributor of memes with 90 memes

# In[32]:


sns.lmplot(x='times_uploaded', y='avg_ups', data=df1)
plt.title("Relation B/w times uploaded by a person and avg ups got")


# The plot shows posting too many dosen't help you get more upvotes

# **now we will see does lenght of title of thumbnail have any effect on its upvote,
# we will consider for 2017 as most of the data is available for this year**

# In[33]:


dfs3=pd.pivot_table(dframe,values='ups',index=['mm1','day'],columns=['year'])
dd=dfs3[2017]
dd=DataFrame(dd)
dd.sort_index(axis=0)


# In[34]:


# the 1st Jan is Sunday
from datetime import date
import calendar
my_date = datetime.date(2017, 1, 1)
calendar.day_name[my_date.weekday()]


# In[35]:


# Get the rest
aa = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
aa = 52*aa
aa = aa + ['Sunday']
dd['weekday'] = aa


# In[36]:


f1= plt.subplots(1, figsize=(2, 8))
dfs4 = pd.pivot_table(dd,values=2017,index='weekday')
sns.heatmap(dfs4,annot=True,fmt='f')


# Memes posted on Saturday gets maximum upvotes but the weekday dosen't have much effect on upvotes

# In[37]:


# Getting the lenght of title thumbnail
lentitle = Series([])
ups = Series([])
z=0
for i in range(3162):
    try:
        ll = len(dframe['title'][i])
        lentitle[z] = ll
        ups[z] = dframe['ups'][i]
        z=z+1
    except Exception:
        pass
lu = DataFrame()
lu['len_of_title'] = lentitle
lu['ups'] = ups
lu.describe()


# In[38]:


f1= plt.subplots(1, figsize=(7, 7))
sns.violinplot(data=lu,y='len_of_title', palette="Set3",axis1=[0])


# most of the memes have thumbnail title of lenght around avg of 25 characters

# In[39]:


f1= plt.subplots(1, figsize=(10, 5))
sns.regplot(x='len_of_title', y='ups', data=lu,order=3)


# Generally a thumbnail title of lenght between 70 - 150 will have greater upvotes, if lenght is increased beyond 200 
# upvotes decreases significantly.

# **Most Frequent words in title for different years**

# In[45]:


# breaking the senatace in title to words
import re
words = Series([])
year = Series([])
w=0
for i in range(3162):
    try:
        wo = re.compile('\w+').findall(dframe['title'][i])
        words[w] = wo
        year[w] = dframe['year'][i]
        w=w+1
    except Exception:
        pass
word = DataFrame()
word['word_in_title'] = words
word['year'] = year


# In[46]:


# Creating a function to find top ten words in title whoose lenght is greater than four as to avoid letters like i,for,and etc.
def get_top_word(y):
    y=word[word['year'] == y]
    w=0
    wor=Series([])
    for w1 in y['word_in_title']:
        for w2 in range(len(w1)):
            wor[w]=w1[w2]
            w=w+1
    counts_word = Counter(wor)
    sorted_word = sorted(counts_word, key=counts_word.get, reverse=True)
    w1=0
    ww1=Series([])
    for r1 in sorted_word:
        if(w1<10 and len(r1)>4):
            ww1[w1]=r1
            w1=w1+1
    return ww1


# In[47]:


# Getting top words for different year
wordss = DataFrame([])
wordss['2014'] = get_top_word(2014)
wordss['2015'] = get_top_word(2015)
wordss['2016'] = get_top_word(2016)
wordss['2017'] = get_top_word(2017)
wordss['2018'] = get_top_word(2018)


# In[48]:


from wordcloud import WordCloud
fig = plt.figure(dpi=100)

ax1 = plt.subplot2grid((3, 3), (0, 0))
ax2 = plt.subplot2grid((3, 3), (0, 1))
ax3 = plt.subplot2grid((3, 3), (1, 0))
ax4 = plt.subplot2grid((3, 3), (1, 1))
ax5 = plt.subplot2grid((3, 3), (2, 0), colspan=2)

wordcloud = WordCloud(background_color='white',max_words=200,max_font_size=40,random_state=3).generate(str(wordss['2014']))
ax1.imshow(wordcloud)
ax1.set_title('Top Word in title of Meme in 2014')
ax1.axis('off')

wordcloud1 = WordCloud(background_color='white',max_words=200,max_font_size=40,random_state=1).generate(str(wordss['2015']))
plt.imshow(wordcloud1)
ax2.imshow(wordcloud1)
ax2.set_title('Top Word in title of Meme in 2015')
ax2.axis('off')

wordcloud2 = WordCloud(background_color='white',max_words=200,max_font_size=40,random_state=1).generate(str(wordss['2016']))
ax3.imshow(wordcloud2)
ax3.set_title('Top Word in title of Meme in 2016')
ax3.axis('off')

wordcloud3 = WordCloud(background_color='white',max_words=200,max_font_size=40,random_state=1).generate(str(wordss['2017']))
ax4.imshow(wordcloud3)
ax4.set_title('Top Word in title of Meme in 2017')
ax4.axis('off')

wordcloud4 = WordCloud(background_color='white',max_words=200,max_font_size=40,random_state=1).generate(str(wordss['2018']))
ax5.imshow(wordcloud4)
ax5.set_title('Top Word in title of Meme in 2018')
ax5.axis('off')

plt.tight_layout()


# In[ ]:




