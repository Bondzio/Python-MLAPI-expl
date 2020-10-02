#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


from pandas import Series,DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set_style("whitegrid")
import statistics


# In[ ]:


import pandas as pd
df= pd.read_csv("../input/kaggle-survey-2019/multiple_choice_responses.csv")
other_text_responses = pd.read_csv("../input/kaggle-survey-2019/other_text_responses.csv")
questions_only = pd.read_csv("../input/kaggle-survey-2019/questions_only.csv")
survey_schema = pd.read_csv("../input/kaggle-survey-2019/survey_schema.csv")


# In[ ]:


df=df.drop(0,axis=0)


# In[ ]:


df.head()


# In[ ]:


def numriser(v):
    v1=[]
    for i in v:
        v1=np.append(v1,int(i))
    return(v1)


# In[ ]:


def co(c):
    t1=[]
    for i in np.arange(len(t)):
        if t[i]>c:
            t1=np.append(t1,t[i])   
    return(t1)


def dnumriser(c):
    v2=[]
    for i in np.arange(1,len(c)):
        if len(c[i])==5:
            v1=(int(c[i][0:2])+int(c[i][3:5]))/2
            v2=np.append(v2,v1)
        else:
            v1=(int(c[i][0:2]))
            v2=np.append(v2,v1)
    return (v2)

def cc(v,n):
    f=0
    for i in np.arange(1,len(v)):
        if (v[i])==n:
            f=f+1
    return (f)


# In[ ]:


df_b=DataFrame([df["Time from Start to Finish (seconds)"],df["Q1"],df["Q2"],df["Q3"],df["Q4"],df["Q5"],df["Q6"],df["Q7"]]).T


# In[ ]:


df_b


# In[ ]:


t=numriser(df["Time from Start to Finish (seconds)"])


# In[ ]:


m=np.repeat(np.mean(t),len(t))
me=np.repeat(np.median(t),len(t))
plt_df=DataFrame([m,me,t],index=["mean","median","obs"]).T


# In[ ]:


plt_df["obs"].plot(figsize=(20,5),alpha=.5,color="yellow")
plt_df["median"].plot(figsize=(20,5),alpha=1,color="black")
plt_df["mean"].plot(figsize=(20,5),alpha=1,color="black")


# In[ ]:


DataFrame(t).describe()


# This broad skewness indicates the fact that a few percent of people did not respond to the survey seriously and thus did not give a lot of time... On the other hand we have those people who took the survey seriouly an thus gave alot of time but the combined effect of the two is leading the mean to fall down. so we consider 200000 as the point below which we do not cosider the respondents response as a serious one

# In[ ]:


t1=co(200000)


# In[ ]:


m=np.repeat(np.mean(t1),len(t1))
me=np.repeat(np.median(t1),len(t1))
plt_df=DataFrame([m,me,t1],index=["mean","median","obs"]).T


# In[ ]:


plt_df["obs"].plot(figsize=(20,5),alpha=.8,color="yellow")
plt_df["median"].plot(figsize=(20,5),alpha=1,color="black")
plt_df["mean"].plot(figsize=(20,5),alpha=1,color="black")


# In[ ]:


m[0]  #this is the mean of the those people who are really filling our form 


# In[ ]:


(len(t1)/len(t))*100             #this response rate indicates that above only 2% people took more than 200000 time 


# In[ ]:


tp1=[]
mx=max(t)
for i in np.arange(0,mx,10000):
    t11=co(i)
    t12=len(t11)
    tp=(t12/len(t))*100
    tp1=np.append(tp1,tp)


# In[ ]:


plt.plot(np.arange(0,mx,10000),tp1)
plt.xlabel("percentage",size=20)
plt.ylabel("response_rate",size=20)


# age specified study****

# In[ ]:


t=dnumriser((df["Q1"]))


# In[ ]:


m=np.repeat(np.mean(t),len(t))
me=np.repeat(np.median(t),len(t))
plt_df=DataFrame([m,me,t],index=["mean","median","obs"]).T


# In[ ]:


plt_df["obs"].plot(figsize=(20,5),alpha=.5,color="yellow")
#plt_df["median"].plot(figsize=(20,5),alpha=1,color="black")
plt_df["mean"].plot(figsize=(20,5),alpha=1,color="black")


# In[ ]:


#so 31 is the average age of the respondents for the survey this year


# In[ ]:


DataFrame(t).describe()


# In[ ]:


#percentage wise disribution of age 


# In[ ]:


a1=0;a2=0;a3=0;a4=0;a5=0;
for i in np.arange(len(t)):
    if (t[i]>20) & (t[i]<30):
        a1=a1+1
        a11=((a1+1)/len(t))*100
    elif (t[i]>30) & (t[i]<40):
        a2=a2+1
        a21=((a2+1)/len(t))*100
    elif (t[i]>40) & (t[i]<50):
        a3=a3+1
        a31=((a3+1)/len(t))*100
    elif (t[i]>50) & (t[i]<60):
        a4=a4+1
        a41=((a4+1)/len(t))*100
    elif (t[i]>60) & (t[i]<70):
        a5=a5+1
        a15=((a5+1)/len(t))*100


# In[ ]:


a=[a11,a21,a31,a41,a15]
sns.kdeplot(a,cumulative=True,color="red",shade=True)
plt.xlabel("age",size=20)
plt.ylabel("fraction of respondents",size=20)


# In[ ]:


plt.pie(a,labels=["20-30","30-40","40-50","50-60","60-70"])


# In[ ]:


#gender_wise clssification


# In[ ]:


m=0;f=0;
for i in np.arange(1,len(df["Q2"])):
    if (df["Q2"][i])=="Male":
        m=m+1
        mp=(m/len(df["Q2"]))*100
    elif (df["Q2"][i])=="Female":
        f=f+1
        fp=(f/len(df["Q2"]))*100


# In[ ]:


gp=[mp,fp,abs(100-mp+fp)]
gp 


# In[ ]:


plt.pie(gp,labels=["Male","Female","Prefer not to say"])


# In[ ]:


#country_wise_study


# In[ ]:


t=df["Q3"]
cn=len(np.unique(t))
c=(np.unique(t))


# In[ ]:


a=[]
for i in c:
    a=np.append(a,(cc(df["Q3"],i)/len(t))*100)


# In[ ]:


df_c=DataFrame([a],columns=c,index=["percent"]).T


# In[ ]:


df_c1=df_c.sort_values(by='percent', ascending=False)
df_c1[0:20]


# In[ ]:


df_c1["percent"].plot(figsize=(20,5))


# In[ ]:


df_c1["percent"][1:20]


# In[ ]:


plt.plot(df_c1["percent"][0:5])


# In[ ]:


plt.pie((df_c1["percent"][0:20]),labels=df_c1.index[0:20])


# In[ ]:


#educational_criteria


# In[ ]:


q=[]
for i in (df["Q4"]).values:
      q=np.append(q,i)


# In[ ]:


uq=np.unique(q)


# In[ ]:


a=[]
for i in uq:
    a=np.append(a,(cc(q,i)/len(q))*100)


# In[ ]:


df_q=DataFrame([a],columns=uq,index=["percent"]).T


# In[ ]:


df_q


# In[ ]:


plt.plot(df_q["percent"])


# In[ ]:


plt.pie((df_q["percent"]),labels=uq)


# In[ ]:


#job_title


# In[ ]:


j=[]
for i in (df["Q5"]).values:
      j=np.append(j,i)
uj=np.unique(j)
a=[]
for i in uj:
    a=np.append(a,(cc(j,i)/len(j))*100)
df_j=DataFrame([a],columns=uj,index=["percent"]).T


# In[ ]:


df_j


# In[ ]:


plt.plot(df_j["percent"])


# In[ ]:


plt.pie((df_j["percent"]),labels=uj)


# In[ ]:


#team_size


# In[ ]:


s=[]
for i in (df["Q7"]).values:
      s=np.append(s,i)
us=np.unique(s)
a=[]
for i in us:
    a=np.append(a,(cc(s,i)/len(j))*100)
df_s=DataFrame([a],columns=us,index=["percent"]).T


# In[ ]:


df_s


# In[ ]:


plt.plot(df_s["percent"])


# In[ ]:


plt.pie((df_s["percent"]),labels=us)


# In[ ]:




