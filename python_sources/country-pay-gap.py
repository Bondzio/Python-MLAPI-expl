#!/usr/bin/env python
# coding: utf-8

# # Country Pay Gap
# 
# In the [2018 Kaggle ML & DS Survey Challenge](https://www.kaggle.com/kaggle/kaggle-survey-2018/home) kagglers are asked to explore a dataset with survey results of themselves.
# <br><br>
# Among tens of multiple choice questions, the survey takers were asked to disclose a range of their yearly compensation, and about 2/3 respondents did.

# In[ ]:


import pandas as pd
import numpy as np

import operator

import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

df = pd.read_csv('../input/multipleChoiceResponses.csv')
df.drop([0],inplace=True)

### ###
### DROP SOME DATA ###
# Start of time column
df['Time from Start to Finish (seconds)'] = df['Time from Start to Finish (seconds)'].apply(int)
# Rejecting those who answered questions too fast:
df = df[df['Time from Start to Finish (seconds)']>60]
# drop "Time" column
df.drop(['Time from Start to Finish (seconds)'],axis=1,inplace=True)
# End of time column
### ###


# In[ ]:


def is_salary_known(x):
    if (x=='I do not wish to disclose my approximate yearly compensation'): return 'unknown'
    if (x!=x): return 'unknown'
    return 'known'

df['is salary known']=df['Q9'].apply(lambda x: is_salary_known(x))

# all valid salary ranges:
all_salaries = ['0-10,000','10-20,000','20-30,000','30-40,000','40-50,000','50-60,000','60-70,000',
                       '70-80,000','80-90,000','90-100,000','100-125,000','125-150,000','150-200,000',
                       '200-250,000','250-300,000','300-400,000','400-500,000','500,000+']


# In[ ]:


fig = plt.subplots(figsize=(12,6))
df_with_unknown_salaries = df
g1 = sns.countplot(x='is salary known',data=df_with_unknown_salaries, 
                   order=['unknown','known'],palette='pastel')
g1.set_xlabel('')
g1.set_ylabel('')
g1.tick_params(labelsize=16)
out = g1.set_title('A compensation of how many respondents is known?',fontsize=24)


# _this study excludes respondents who spent less than a minute to complete the survey_
# <br><br>
# All possible yearly compensations are split into 18 ranges, from '0-10,000' to '500,000+':

# In[ ]:


### ###
### DROP SOME DATA ###
# drop those who didn't disclose disclose their salary
# and those whose salary is unknown
df = df[(df['is salary known']=='known')]
### ###

# def: plot salary distribution
def plot_salary_distribution(df,col='Q9',x_label='yearly compensation, [USD]',order=None):
    fig, ax2 = plt.subplots(figsize=(18,6))
    g2 = sns.countplot(x=col,data=df, order=order, ax=ax2)
    g2.set_xticklabels(ax2.get_xticklabels(),rotation=90)
    g2.set_title('Yearly compensation distribution',fontsize=24)
    g2.set_ylabel('')
    g2.set_xlabel(x_label,fontsize=20)
    g2.tick_params(labelsize=14)
    #ax2.set(yscale="log")
    for p in ax2.patches:
        x=p.get_bbox().get_points()[:,0]
        y=p.get_bbox().get_points()[1,1]
        ax2.annotate(p.get_height(), (x.mean(), y), ha='center', va='bottom',fontsize=14)
        
# plot salary distribution
plot_salary_distribution(df,order=all_salaries)


# The peak around '100-125,000' corresponds to the average compensation of USA data scientists while the peak at '0-10,000' indicates a large representation of kagglers from countries with lower salary scales.
# <br><br>

# In[ ]:


renamed_columns = {
    'Q1': 'gender',
    'Q2': 'age [years]',
    'Q3': 'country',
    'Q4': 'education',
    'Q5': 'undergraduate major',
    'Q6': 'job title',
    'Q7': 'industry',
    'Q8': 'experience in current role [years]',
    'Q9': 'yearly compensation [USD]',
    'Q10': 'Does your current employer use ML?',
    'Q24': 'experience writing data analysis code [years]',
    'Q25': 'experience using ML [years]'
}

def rename_columns(x):
    if x in renamed_columns.keys():
        return renamed_columns[x]
    return x

df.rename(columns=lambda x: rename_columns(x), inplace=True)


# shorten names of some countries
def rename_some_countries(x):
    if (x=='United States of America'): return 'USA'
    if (x=='United Kingdom of Great Britain and Northern Ireland'): return 'United Kingdom'
    if (x=='Iran, Islamic Republic of...'): return 'Iran'
    if (x=='Hong Kong (S.A.R.)'): return 'Hong Kong'
    return x

df['country']=df['country'].apply(lambda x: rename_some_countries(x))

# distribution over salary ranges
df_USA = df[(df['country']=='USA')]
df_India = df[(df['country']=='India')]
df_for_plot = pd.concat([df_USA,df_India])

fig, ax2 = plt.subplots(figsize=(18,6))
g2 = sns.countplot(x='yearly compensation [USD]',data=df_for_plot, 
                   order=all_salaries, ax=ax2, hue='country')
smth0 = g2.set_xticklabels(ax2.get_xticklabels(),rotation=90)
smth1 = g2.set_title('Yearly compensation distribution',fontsize=24)
smth2 = g2.set_ylabel('')
smth3 = g2.set_xlabel('yearly compensation [USD]',fontsize=20)
smth4 = g2.tick_params(labelsize=14)
smth5 = plt.gca().legend().set_title('')
smth6 = plt.setp(ax2.get_legend().get_texts(), fontsize='20') # for legend text


# This kernel concentrates on the study of these discrepancies between compensations of kagglers residing in different countries which are refered as a __country pay gap__.

# ## Salary Quantification
# 
# The ranges are good for such comparison plots as one above and are distributed fairly well for USA, but for more in-depth compensation studies the ranges need to be quantified. It is essential to measure the difference in typical compensation for any kaggler groups whether it is by a country of residence, an education, experience, main activities at work or a job title. 
# <br><br>
# Three quantification methods are used in this study:
# - simple enumeration of compensation ranges<br>
#     ('0-10,000' $\rightarrow$ 1, '10-20,000' $\rightarrow$ 2, '500,000+' $\rightarrow$ 18);
# - averages of compensation range boundaties<br>
#     ('0-10,000' $\rightarrow$ 5000, '10-20,000' $\rightarrow$ 15000, '500,000+' $\rightarrow$ 650000); and
# - minimal values of range boundaries<br>
#     ('0-10,000' $\rightarrow$ 0, '10-20,000' $\rightarrow$ 10000, '500,000+' $\rightarrow$ 500000)

# In[ ]:


# average salary values in each salary range
dict_averages = {'0-10,000':5000,'10-20,000':15000,'20-30,000':25000,
                '30-40,000':35000,'40-50,000':45000,'50-60,000':55000,
                '60-70,000':65000,'70-80,000':75000,'80-90,000':85000,
                '90-100,000':95000,'100-125,000':112500,'125-150,000':137500,
                '150-200,000':175000,'200-250,000':225000,'250-300,000':275000,
                '300-400,000':350000,'400-500,000':450000,'500,000+':650000}

dict_mins = {'0-10,000':0,'10-20,000':10000,'20-30,000':20000,
                 '30-40,000':30000,'40-50,000':40000,'50-60,000':50000,
                '60-70,000':60000,'70-80,000':70000,'80-90,000':80000,
                '90-100,000':90000,'100-125,000':100000,'125-150,000':125000,
                '150-200,000':150000,'200-250,000':200000,'250-300,000':250000,
                '300-400,000':300000,'400-500,000':400000,'500,000+':500000}

# quantify salary ranges by enumerating them
def quantify_enumerate(x):
    for i in range(1,len(all_salaries)+1):
        if (x==all_salaries[i-1]): return i
    return -100

# quantify salary ranges by getting an average for each range
def quantify_average(x):
    return dict_averages[x]

# quantify salary ranges by getting an average for each range
def quantify_min(x):
    return dict_mins[x]

df['enum salary ranges'] = df['yearly compensation [USD]'].apply(lambda x: quantify_enumerate(x))

df['salary averages'] = df['yearly compensation [USD]'].apply(lambda x: quantify_average(x))

df['salary mins'] = df['yearly compensation [USD]'].apply(lambda x: quantify_min(x))

# replace nans in all data with a string value
df.fillna('nan_value', inplace=True)


# In[ ]:


df_USA = pd.DataFrame(df[df['country']=='USA'])
df_India = pd.DataFrame(df[df['country']=='India'])

fig,(ax1,ax2,ax3) = plt.subplots(figsize=(18,6),ncols=3)

p1 = ax1.hist(df_USA['enum salary ranges'],bins=18)
p2 = ax1.hist(df_India['enum salary ranges'],bins=18,alpha=0.5)
p3 = ax1.set_title('India vs USA',fontsize=20)
p4 = ax1.set_xlabel('simple enum. of a compensation range',fontsize=16)
p5 = ax1.set_xlim(1,18)

p1 = ax2.hist(df_USA['salary averages'],bins=65)
p2 = ax2.hist(df_India['salary averages'],bins=65,alpha=0.5)
p3 = ax2.set_title('India vs USA',fontsize=20)
p4 = ax2.set_xlabel('compensation range average [USD]',fontsize=16)
p5 = ax2.set_xlim(0,650000)
ax2.legend(('USA', 'India'),fontsize='16')

p1 = ax3.hist(df_USA['salary mins'],bins=50)
p2 = ax3.hist(df_India['salary mins'],bins=50,alpha=0.5)
p3 = ax3.set_title('India vs USA',fontsize=20)
p4 = ax3.set_xlabel('compensation range min [USD]',fontsize=16)
p5 = ax3.set_xlim(0,650000)


# In[ ]:


# print out number of events in a given category
# and also mean and std salary
def print_mean_std_name_n(name,n,mean,std):
    print('{}: count={}, mean={},std={}'.
              format(name,n,int(mean),int(std),int(100*std/mean)))

# mean and std salary of all categories for a given df column
# df_col is usually a df[[col]] but could be an original df
def cats_mean_and_std(df_col,col,n_cut,salary_quantification_col):
    categories = df_col[col].unique()
    n_cats = categories.size
    dict_cats = {}
    for cat in categories:
        df_local = df_col[df_col[col]==cat]
        n = df_local.shape[0]
        if (n<n_cut): continue
        val_mean = df_local[salary_quantification_col].mean(axis=0)
        val_std = df_local[salary_quantification_col].std(axis=0)
        val_mean=int(val_mean)
        val_std=int(val_std)
        dict_cats[cat] = [val_mean, val_std]
    return dict_cats


# calculate separation of salary
# between two categories
# it's defined as |mean1-mean2|-sqrt(std1^2+std2^2)
# if it's bigger than zero, 
# the separation is significant
def separation(mean1,mean2,std1,std2):
    diff = abs(mean1-mean2)
    std = (std1**2+std2**2)**0.5
    return diff-std

# an array of all salary separations
# for all category pairs
def separations(dict_cats):
    n = len(dict_cats)
    keys = list(dict_cats.keys())
    seps = []
    sep_max = ['key1','key2',-100]
    for i in range(n):
        for j in range(i,n):
            key1 = keys[i]
            key2 = keys[j]
            mean1,std1 = dict_cats[key1]
            mean2,std2 = dict_cats[key2]
            sep = separation(mean1,mean2,std1,std2)
            if (sep>0): seps.append([key1,key2,int(sep)])
            if (sep>sep_max[2]): 
                sep_max[0] = key1
                sep_max[1] = key2
                sep_max[2] = int(sep)
    return sep_max,seps


# In[ ]:


cols_to_check = []
for col in df.columns:
    if (col=='yearly compensation [USD]'): continue
    if (col=='enum salary ranges'): continue
    if (col=='salary averages'): continue
    if (col=='salary mins'): continue
    if (col=='is salary known'): continue
    if (col=='N salary 0-10,000'): continue
    n = len(df[col].unique())
    if (n<100):
        cols_to_check.append(col)
        


# ## What Factors Affect Kaggler's Compensation the Most

# In[ ]:


def run_salary_separations(df,salary_quantification_col,n_cut):
    seps_max = []
    for col in cols_to_check:
        df_col = df[[col,salary_quantification_col]]
        dict_cats = cats_mean_and_std(df_col,col,n_cut,salary_quantification_col)
        sep_max,seps = separations(dict_cats)
        if (len(seps)>0):
            #print(col, 'sep max =',sep_max)
            seps_max.append([col,sep_max[0],sep_max[1],sep_max[2]])
        seps_max = sorted(seps_max, key = lambda x: int(x[3]))
    print('')
    print('The most significant factors affecting yearly compensation')
    print('estimated based on {}:'.format(salary_quantification_col))
    print('')
    for i in range(len(seps_max)-1,-1,-1):
        print(seps_max[i][0], ':',seps_max[i][1],'vs',seps_max[i][2],'( score =',seps_max[i][3],')')
    
run_salary_separations(df,'enum salary ranges',n_cut=20)
print('_______________________________________')
run_salary_separations(df,'salary averages',n_cut=20)


# Both methods found country of residence to be the most significant factor affecting a kaggler's yearly compensation.
# <br><br>
# Some other parameters like experience with data analysis and machine learning algorithms also affect one's compensation by factor of several but for a closer investigation we have to exclude one very important group of kagglers. 

# In[ ]:


def is_student(row):
    if (row['job title']=='Student'): return 'Student'
    if (row['industry']=='I am a student'): return 'Student'
    return 'Not a student'

df['is_student'] = df.apply(lambda row: is_student(row),axis=1)

fig = plt.subplots(figsize=(12,6))
g1 = sns.countplot(x='is_student',data=df, order=['Student','Not a student'],
                   palette='pastel')
g1.set_xlabel('')
g1.set_ylabel('')
out = g1.set_title('Are you a student?',fontsize=24)
g1.tick_params(labelsize=16)


# In[ ]:


def plot_one_count_and_box_plot(df,col,salary_quantification_col,y_label,order=None):
    if (col=='country'): # Q3 is country
        fig, (ax1,ax2) = plt.subplots(figsize=(18,28),ncols=2)
    else:
        fig, (ax1,ax2) = plt.subplots(figsize=(18,12),ncols=2)
    g1 = sns.boxplot(y=col,x=salary_quantification_col,data=df, ax=ax1,order=order)
    g2 = sns.countplot(y=col,data=df, ax=ax2,order=order)
    #g1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
    #g2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    g2.set_yticklabels([])
    g1.set_xlabel(salary_quantification_col,fontsize=20)
    g2.set_xlabel('counts',fontsize=20)
    g1.set_title(salary_quantification_col+' by '+y_label,fontsize=24)
    g2.set_title('N of respondents by '+y_label,fontsize=24)
    g1.set_ylabel('')
    g2.set_ylabel('')
    g1.tick_params(labelsize=16)
    g2.tick_params(labelsize=16)
    for p in ax2.patches:
        x=p.get_bbox().get_points()[:,1]
        y=p.get_bbox().get_points()[1,0]
        ax2.annotate(p.get_width(),(1.05*p.get_width(),p.get_y()+0.4),fontsize=16)
    if (col=='country' or col=='job title' or col=='industry'):  
        ax2.set(xscale="log")


# In[ ]:


def values_by_salary_order(df,col,salary_quantification_col):
    d = df.groupby(by=col).mean().to_dict()[salary_quantification_col]
    sorted_d = sorted(d.items(), key=operator.itemgetter(1))
    countries_order = ['X']*len(sorted_d)
    for i in range(len(sorted_d)):
        countries_order[i]=sorted_d[i][0]
    return countries_order


# In[ ]:


# Start with Q6
# Q6 - job title

salary_quantification_col = 'enum salary ranges'
df_title = df[['job title',salary_quantification_col]]
df_title = df_title[df_title['job title']!='Other']
order = values_by_salary_order(df_title,'job title',salary_quantification_col)
plot_one_count_and_box_plot(df_title,'job title',
                            salary_quantification_col,'job title',order)


# In[ ]:


# Q7 - industry

salary_quantification_col = 'enum salary ranges'
df_industry = df[['industry',salary_quantification_col]]
df_industry = df_industry[df_industry['industry']!='Other']
order = values_by_salary_order(df_industry,'industry',salary_quantification_col)
plot_one_count_and_box_plot(df_industry,'industry',salary_quantification_col,'industry',order)


# Students appear in "job title" and "industry you are working in" questions, and in both cases they are the least paid categories as expected.
# <br><br>
# Students affect compensation distributions by country differently for different countries because the fraction of students among the survey respondents differ from country to country.

# In[ ]:


df_for_plot = df[(df['country']=='USA') | (df['country']=='India')]

fig = plt.subplots(figsize=(12,6))
g1 = sns.countplot(x='is_student',data=df_for_plot, order=['Student','Not a student'],
                   hue='country')
g1.set_xlabel('')
g1.set_ylabel('')
out = g1.set_title('Are you a student?',fontsize=24)
g1.tick_params(labelsize=16)
plt.gca().legend().set_title('')
smth5 = plt.setp(g1.get_legend().get_texts(), fontsize='20') # for legend text


# In[ ]:


df_for_plot_non_student = df_for_plot[df_for_plot['is_student']=='Not a student']

fig, (ax1,ax2) = plt.subplots(figsize=(18,12),nrows=2)

g1 = sns.countplot(x='yearly compensation [USD]',data=df_for_plot, 
                   order=all_salaries, ax=ax1, hue='country',hue_order=(['USA','India']))
smth0 = g1.set_xticklabels(ax1.get_xticklabels(),rotation=90)
smth1 = g1.set_title('Yearly compensation distribution, India vs USA \n\n (INCLUDING students)',fontsize=24)
smth2 = g1.set_ylabel('')
smth3 = g1.set_xlabel('')
smth4 = g1.tick_params(labelsize=14)
g1.set_xticklabels([])
l = ax1.legend()
l.set_title('')
smth5 = plt.setp(ax1.get_legend().get_texts(), fontsize='20') # for legend text

g2 = sns.countplot(x='yearly compensation [USD]',data=df_for_plot_non_student, 
                   order=all_salaries, ax=ax2, hue='country',hue_order=(['USA','India']))
smth0 = g2.set_xticklabels(ax2.get_xticklabels(),rotation=90)
smth1 = g2.set_title('(EXCLUDING students)',fontsize=24)
smth2 = g2.set_ylabel('')
smth3 = g2.set_xlabel('yearly compensation [USD]',fontsize=20)
smth4 = g2.tick_params(labelsize=14)
plt.gca().legend().set_title('')
smth5 = plt.setp(ax2.get_legend().get_texts(), fontsize='20') # for legend text


# In[ ]:


print('# of respondents before removing students: ',df.shape[0])
df = df[df['is_student']=='Not a student']
print('# of respondents after students: ',df.shape[0])


# ## What Factors Affect Kaggler's non-Student Compensation the Most

# In[ ]:


run_salary_separations(df,'enum salary ranges',n_cut=20)
print('_______________________________________')
run_salary_separations(df,'salary averages',n_cut=20)


# For non-students respondents, country is the most significant factor to affect the compensation.

# In[ ]:


# Q3 - country
salary_quantification_col='enum salary ranges'

# shorten names of some countries
def rename_some_countries(x):
    if (x=='United States of America'): return 'USA'
    if (x=='United Kingdom of Great Britain and Northern Ireland'): return 'United Kingdom'
    if (x=='Iran, Islamic Republic of...'): return 'Iran'
    if (x=='Hong Kong (S.A.R.)'): return 'Hong Kong'
    return x

df['country']=df['country'].apply(lambda x: rename_some_countries(x))

df_countries = df[['country',salary_quantification_col]]
print('N of respondents: ',df_countries.shape[0])
df_countries = df_countries[df_countries['country']!='Other']
df_countries = df_countries[df_countries['country']!='I do not wish to disclose my location']
print('N of respondents from known countries: ',df_countries.shape[0])

n_countries = len(dict(df_countries['country'].value_counts()))
print('N of countries:',n_countries)

#print(dict(df_countries['country'].value_counts()))

###
### plot known vs unknown country
###

order = values_by_salary_order(df_countries,'country',salary_quantification_col)
plot_one_count_and_box_plot(df_countries,'country',salary_quantification_col,'country',order)


# Kagglers residing in **Nigeria**, **Viet Nam**, **Egypt**, **Iran** and **Turkey** have the smallest compensations, while kagglers living in **Switzerland**, **USA**, **Australia**, **Denmark** and **Isarael** are paid the best, although almost any country with a sufficient number of respondents have highly paid outliers.

# In[ ]:


# x is enum salary rages
def is_lower_10000(x):
    if (x<=1): return 1
    return 0

def is_lower_20000(x):
    if (x<=2): return 1
    return 0

def is_lower_30000(x):
    if (x<=3): return 1
    return 0

# x is enum salary rages for 100000+
def is_bigger_100000(x):
    if (x>=11):return 1
    return 0

# introduce new aggregate features
df['N salary 0-10,000'] = df['enum salary ranges'].apply(lambda x: is_lower_10000(x))
df['N salary 0-20,000'] = df['enum salary ranges'].apply(lambda x: is_lower_20000(x))
df['N salary 0-30,000'] = df['enum salary ranges'].apply(lambda x: is_lower_30000(x))
df['N salary 100,000+'] = df['enum salary ranges'].apply(lambda x: is_bigger_100000(x))
df_by_country = df.groupby(by='country').agg({
    'enum salary ranges': 'mean',
    'salary averages': 'mean',
    'salary mins': 'mean',
    'country':'count',
    'N salary 0-10,000': 'sum',
    'N salary 0-20,000': 'sum',
    'N salary 0-30,000': 'sum',
    'N salary 100,000+': 'sum'
})

df_by_country['N respondents'] = df_by_country['country']
df_by_country.drop('country',axis=1,inplace=True)

# remove the entries of unknown countries
df_by_country.drop('Other',axis=0,inplace=True)
df_by_country.drop('I do not wish to disclose my location',axis=0,inplace=True)

def fraction_below_10000(row):
    return 100*row['N salary 0-10,000']/row['N respondents']

def fraction_below_20000(row):
    return 100*row['N salary 0-20,000']/row['N respondents']

def fraction_below_30000(row):
    return 100*row['N salary 0-30,000']/row['N respondents']

def fraction_above_100000(row):
    return 100*row['N salary 100,000+']/row['N respondents']

df_by_country['% with salary 0-10,000'] = df_by_country.apply(lambda row: fraction_below_10000(row),axis=1)
df_by_country['% with salary 0-10,000'] = df_by_country['% with salary 0-10,000'].apply(int)

df_by_country['% with salary 0-20,000'] = df_by_country.apply(lambda row: fraction_below_20000(row),axis=1)
df_by_country['% with salary 0-20,000'] = df_by_country['% with salary 0-20,000'].apply(int)

df_by_country['% with salary 0-30,000'] = df_by_country.apply(lambda row: fraction_below_30000(row),axis=1)
df_by_country['% with salary 0-30,000'] = df_by_country['% with salary 0-30,000'].apply(int)

df_by_country['% with salary 100,000+'] = df_by_country.apply(lambda row: fraction_above_100000(row),axis=1)
df_by_country['% with salary 100,000+'] = df_by_country['% with salary 100,000+'].apply(int)

df_by_country.sort_values(by='salary averages',
                          ascending=True,inplace=True)

df_by_country_percent = df_by_country[['% with salary 0-10,000',
                                '% with salary 0-20,000',
                                 '% with salary 0-30,000',
                                  '% with salary 100,000+']]
df_by_country_percent['<$10K'] = df_by_country_percent['% with salary 0-10,000']
df_by_country_percent['<$20K'] = df_by_country_percent['% with salary 0-20,000']
df_by_country_percent['<$30K'] = df_by_country_percent['% with salary 0-30,000']
df_by_country_percent['>$100K'] = df_by_country_percent['% with salary 100,000+']


# In[ ]:


import seaborn as sns

f,ax = plt.subplots(figsize=(12,28))

out = sns.heatmap(df_by_country_percent[['<$10K','<$20K','<$30K','>$100K']],
                 annot=True, annot_kws={"size": 16}, cmap='coolwarm')
ax.set_title('% of Respondents with Yearly Compensation of\n',
             fontsize=24)
ax.xaxis.set_ticks_position('top')
out = ax.tick_params(labelsize=16)
out = ax.set_ylabel('')


# #### Observations:
# - In **Iran** and **Nigeria**, 71% of non-student respondents have a yearly compensation of less than \$10K;
# - in 9 out of 56 countries more than 50% of non-student respondents make less than \$10K;
# - in 40% of 56 countries more than 50% of non-student respondents make less than \$20K;
# - in **USA**, **Switzerland**, **Australia** and **Israel**, more than 30\% of non-student respondents have a yearly compensation of over \$100K.
# <br><br>
# The countries in the heatmap above above are sorted by 'salary averages'. Thus, we expect left and middle plots to appear in ascending and right plot to appear in descending order. While it is generally the case, I want to emphasize outliers:
# <br><br>
# - **Republic of Korea** is in top 10 country with the largest average yearly compensations, but has only 3% of respondents in >\$100K range 
# - **Kenya**, with 66% of respondents making less than \$20K, has a relatively large fraction (8%) of kagglers with yearly compensation of above \$100K
# - **Israel** while being among the top 4 countries by a fraction of kagglers making over \$100K (35%), has a relatively large fraction of low-paid kagglers (11% of respondents in Israel make less than \$20K, and almost half of them - less than \$10K)

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns

# distribution over salary ranges
df_Kenya = df[(df['country']=='Kenya')]
df_Republic_of_Korea = df[(df['country']=='Republic of Korea')]
df_Israel = df[(df['country']=='Israel')]
df_for_plot = pd.concat([df_Israel,df_Kenya,df_Republic_of_Korea])

fig, ax2 = plt.subplots(figsize=(18,6))
g2 = sns.countplot(x='yearly compensation [USD]',data=df_for_plot, 
                   order=all_salaries, ax=ax2, hue='country',
                   palette=["#9b59b6", "#95a5a6","#34495e"])
smth0 = g2.set_xticklabels(ax2.get_xticklabels(),rotation=90)
smth1 = g2.set_title('Yearly compensation distribution',fontsize=24)
smth2 = g2.set_ylabel('')
smth3 = g2.set_xlabel('yearly compensation [USD]',fontsize=20)
smth4 = g2.tick_params(labelsize=14)
smth5 = plt.gca().legend().set_title('')
plt.legend(loc='upper right')
smth6 = plt.setp(ax2.get_legend().get_texts(), fontsize='20')

print('N of non-student respondents with known salaries residing in:')
print('')
print('Israel:',df_Israel.shape[0])
print('Kenya:',df_Kenya.shape[0])
print('Republic of Korea:',df_Republic_of_Korea.shape[0])


# ## Kaggle Popularity in Different Countries
# 
# To have a deeper look into the country effect, let us attract some relevant external data: 
# 
# - [average income](https://www.worlddata.info/average-income.php)
# - [cost index](https://www.numbeo.com/cost-of-living/rankings_by_country.jsp)
# - [population](http://www.worldometers.info/world-population/population-by-country/)

# In[ ]:


# [average_income, cost_index, population(millions)]
# average income: https://www.worlddata.info/average-income.php
# https://www.numbeo.com/cost-of-living/rankings_by_country.jsp
# http://www.worldometers.info/world-population/population-by-country/
dict_countries_additional_info = {
    'USA': [58270, 68.95, 326.77], 
    'India': [1820, 23.81, 1354.05], 
    'Russia': [9230, 36.73, 143.96], 
    'China': [8690, 40.43, 1415.05], 
    'Brazil': [8580, 40.48, 210.87], 
    'United Kingdom': [40530, 67.18, 66.57], 
    'Germany': [43490, 67.89, 82.29], 
    'Canada': [42870, 64.54, 36.95], 
    'France': [37970, 74.83, 65.23], 
    'Japan': [38550, 79.87, 127.19], 
    'Spain': [27180, 55.43, 46.40], 
    'Italy': [31020, 69.68, 59.29], 
    'Poland': [12710, 38.69, 38.10], 
    'Australia': [51360, 73.87, 24.77], 
    'Turkey': [10930, 35.52, 81.92], 
    'Netherlands': [46180, 75.93, 17.08], 
    'Ukraine': [2390, 27.08, 44.01],
    'Mexico': [8610, 30.54, 130.76], 
    'Israel': [37270, 74.86, 8.45], 
    'Singapore': [54530, 80.40, 5.79], 
    'Sweden': [52590, 70.39, 9.98], 
    'Switzerland': [80560, 119.98, 8.54], 
    'Argentina': [13040, 36.41, 44.69], 
    'Nigeria': [2080, 32.25, 195.88], 
    'Colombia': [5830, 32.61, 49.46], 
    'South Africa': [5430, 42.11, 57.39], 
    'Portugal': [19820, 50.64, 10.29], 
    'South Korea': [28380, 76.62, 51.16], 
    'Indonesia': [3540, 36.16, 266.80], 
    'Viet Nam': [2170, 36.91, 96.49], 
    'Greece': [18090, 57.64, 11.14], 
    'Pakistan': [1580, 22.17, 200.81], 
    'Hungary': [12870, 41.34, 9.69], 
    'Denmark': [55220, 82.65, 5.75], 
    'Belgium': [41790, 74.39, 11.49], 
    'Ireland': [55290, 77.08, 4.80], 
    'Malaysia': [9650, 40.69, 32.04], 
    'Chile': [13610, 48.20, 18.20], 
    'Belarus': [-1, 32.03, 9.45], 
    'Kenya': [1440, 38.29, 50.95], 
    'Norway': [75990, 104.09, 5.35], 
    'Finland': [44580, 72.73, 5.54], 
    'Romania': [9970, 36.70, 19.58], 
    'Czech Republic': [18160, 44.53, 10.63], 
    'Peru': [-1, 38.32, 32.55], 
    'New Zealand': [38970, 72.41, 4.75], 
    'Thailand': [5960, 44.55, 69.18], 
    'Philippines': [3660, 32.78, 106.51], 
    'Iran': [5400, 30.86, 82.01], 
    'Egypt': [3010, 24.67, 99.38], 
    'Hong Kong': [46310, 74.73, 7.43], 
    'Bangladesh': [1470, 30.18, 166.37], 
    'Austria': [45440, 72.31, 8.75], 
    'Republic of Korea': [-1, -1, 25.61], 
    'Morocco': [2860, 33.59, 36.19],
    'Tunisia': [-1, 24.53, 11.66]
}

df_add_info = pd.DataFrame(dict_countries_additional_info)
df_add_info = df_add_info.transpose()
df_add_info.rename(columns={0:'country average income',1:'cost of living index',2:'population'},
                  inplace=True)


# In[ ]:


df_by_country['salary averages']=df_by_country['salary averages'].apply(int)
df_by_country['salary mins']=df_by_country['salary mins'].apply(int)
df_by_country['enum salary ranges']=df_by_country['enum salary ranges'].apply(int)

df_by_country=df_by_country.join(df_add_info)
df_by_country.dropna(inplace=True)
df_by_country['country average income']=df_by_country['country average income'].apply(int)
df_by_country['population']=df_by_country['population'].apply(int)

# compose more features
def N_responders_per_million(row):
    return row['N respondents']/row['population']

def kaggler_salary_over_country_average(row):
    return row['salary averages']/row['country average income']

def kaggler_min_salary_over_country_average(row):
    return row['salary mins']/row['country average income']

def kaggler_salary_over_cost_index(row):
    return row['salary averages']/row['cost of living index']

df_by_country['N respondents per million of population'] = df_by_country.apply(lambda row: N_responders_per_million(row),axis=1)
df_by_country['N respondents per million of population'] = df_by_country['N respondents per million of population'].apply(lambda x: 
                                                                                                                        round(x,2))
df_by_country['kaggler salary over country average'] = df_by_country.apply(lambda row:
                                                                            kaggler_salary_over_country_average(row),axis=1)
df_by_country['kaggler salary over country average'] = df_by_country['kaggler salary over country average'].apply(lambda x: 
                                                                                                                    round(x,2))
df_by_country['kaggler salary over country average low estimate'] = df_by_country.apply(lambda row:
                                                                            kaggler_min_salary_over_country_average(row),axis=1)
df_by_country['kaggler salary over country average low estimate'] = df_by_country['kaggler salary over country average low estimate'].apply(lambda x: 
                                                                                                                    round(x,2))
df_by_country['kaggler salary over cost index'] = df_by_country.apply(lambda row:
                                                                            kaggler_salary_over_cost_index(row),axis=1)
df_by_country['kaggler salary over cost index'] = df_by_country['kaggler salary over cost index'].apply(int)

# sort countries by number of respondents
df_by_country.sort_values(by='N respondents',ascending=False,inplace=True)

# print table
df_by_country[['N respondents','N respondents per million of population',
               'kaggler salary over cost index','kaggler salary over country average',
              '% with salary 0-10,000','% with salary 0-20,000','% with salary 0-30,000',
              '% with salary 100,000+']].head()


# The table above shows only a few out of a number of aggregate features for five countries with the largest numbers of respondents. 
# - **N respondents** and **N respondents per million of population**: total number of respondents (except students, people with unknown salaries and people who answered the survey too fast) and the same number divided over the country population;
# - **kaggler salary over cost index**: the 'salary average' divided over country living cost index;
# - **kaggler salary over country average**: the 'salary average', average yearly compensation of a kaggler residing in a given country, divided over the average income of a resident of this country (regardless whether the resident is a kaggler or not);
# - **% with salary X**: % of respondents from a number 'N respondents' with a given annual compensation (below \$10K, below \$20K, below \$30K and above \$100K, as shown on a heatmap above).
# 
# If you are interested to stare at these numbers for all 56 countries, you are welcome to check the table hidden below.
# 
# *Note: negative values means some of data were not available in the external sources I used.*

# In[ ]:


df_by_country[['N respondents','N respondents per million of population',
               'kaggler salary over cost index','kaggler salary over country average',
              '% with salary 0-10,000','% with salary 0-20,000','% with salary 0-30,000',
              '% with salary 100,000+']]


# In[ ]:


import matplotlib.pyplot as plt

col1 = 'N respondents'
col2 = 'N respondents per million of population'

df_by_country.sort_values(by=col2,
                          ascending=True,inplace=True)

fig, (ax2,ax1) = plt.subplots(figsize=(18,45),ncols=2,sharey=True)
ax1.set_title('N respondents total',fontsize=24)
out = df_by_country[col1].plot(kind='barh',ax=ax1, color='cyan')
ax2.set_title(col2,fontsize=24)
out = df_by_country[col2].plot(kind='barh',ax=ax2, color='cyan')
out = ax1.tick_params(labelsize=16)
out = ax2.tick_params(labelsize=16)
out = ax1.set_ylabel('')
out = ax2.set_ylabel('')
out = ax1.set(xscale="log")
out = ax2.set(xscale="log")

for p in ax1.patches:
    x=p.get_bbox().get_points()[:,1]
    y=p.get_bbox().get_points()[1,0]
    ax1.annotate(p.get_width(),(1.05*p.get_width(),p.get_y()+0.1),fontsize=16)
    
for p in ax2.patches:
    x=p.get_bbox().get_points()[:,1]
    y=p.get_bbox().get_points()[1,0]
    ax2.annotate(p.get_width(),(1.05*p.get_width(),p.get_y()+0.1),fontsize=16)


# The distribution of the number of respondents by country per capita (left plot) is more indicative of the kaggle popularity in a given country rather than the total number of respondents (right plot).
# <br><br>
# *Note: the plots exclude students*
# <br><br>
# **India** and **China** have one of the highest numbers of the total respondents but the kaggle popularity in these countries is closer to the lowest boundary (or they didn't participate in the survey).
# <br><br>
# **Do you know if kaggle is allowed in China?**
# <br><br>
# In contrast, look at **Singapore**. With fewer than 6 million of population, this country does not have a large enough total number of respondents to be as noticible as USA or India, but 22 respondents per million of population makes it absolutely stand out in terms of kaggle popularity with the second place (**Ireland**) left behind by over 30%! 
# <br><br>
# **A kaggle popularity in a given country is strongly correlated with a kaggler's yearly compensation in the country. **

# In[ ]:


fig, ax =plt.subplots(1,2,figsize=(18,12),sharey=True)
g1 = sns.regplot(x='N respondents per million of population',
           y='salary averages',data=df_by_country, ax=ax[0])
out = ax[0].set_ylim(0,130000)
out = ax[0].set_xlim(0,23)
g2 = sns.regplot(x='N respondents',
           y='salary averages',data=df_by_country,ax=ax[1])
out = ax[1].set_ylim(0,130000)
out = ax[1].set_xlim(0,3000)
out = g1.set_xlabel('N respondents per million of population',fontsize=20)
out = g1.set_ylabel('kaggler salary average [USD]',fontsize=20)
out = g2.set_xlabel('N respondents total',fontsize=20)
out = g2.set_ylabel('')
g1.tick_params(labelsize=14)
g2.tick_params(labelsize=14)


# 
# ## Kagglers salary divided by country living cost index and by country average income

# In[ ]:


def kaggler_salary_by_cost_index(row):
    country = row['country']
    salary_average = row['salary averages']
    cost_index = dict_countries_additional_info[country][1]
    if (cost_index==-1): return -1
    return salary_average/cost_index 

def kaggler_salary_by_country_average_income(row):
    country = row['country']
    salary_min = row['salary mins']
    country_salary = dict_countries_additional_info[country][0]
    if (country_salary==-1): return -1
    return salary_min/country_salary

df = df[df['country']!='Other']
df = df[df['country']!='I do not wish to disclose my location']

df['kaggler salary over cost index'] = df.apply(lambda row: kaggler_salary_by_cost_index(row),axis=1)
df['kaggler salary over country average'] = df.apply(lambda row: kaggler_salary_by_country_average_income(row),axis=1)

df = df[df['kaggler salary over cost index']!=-1]
df = df[df['kaggler salary over country average']!=-1]


# In[ ]:


order = values_by_salary_order(df,'country','salary averages')

fig, (ax1,ax2,ax3) = plt.subplots(figsize=(18,28),ncols=3,sharey=True)

def plot_one_col(col,title,ax):
    g = sns.boxplot(y='country',x=col,
                 data=df,ax=ax,order=order)
    g.set_xlabel(title,fontsize=20)
    g.set_title(title,fontsize=24)
    g.set_ylabel('')
    g.tick_params(labelsize=16)
    return g
    
g1 = plot_one_col('salary averages','kaggler \n salary average [USD]',ax1)
out = ax1.set_xlim(0,122000)
g2 = plot_one_col('kaggler salary over cost index','kaggler \n salary average \n over cost index',ax2)
out = ax2.set_xlim(0,2000)
g3 = plot_one_col('kaggler salary over country average','kaggler \n salary min \n over country average',ax3)
out = ax3.set_xlim(0.5,50)
out = ax3.set_xscale('log')


# In[ ]:


col_by = 'salary averages'
n_top_or_bottom = 5

def top_and_bottom(col_by,n_top_or_bottom):
    df_top = df_by_country.sort_values(by=col_by,ascending=False).head(n_top_or_bottom)
    df_bottom = df_by_country.sort_values(by=col_by,ascending=True).head(n_top_or_bottom)
    bottom_mean = df_bottom[col_by].mean()
    top_mean = df_top[col_by].mean()
    top_by_bottom = top_mean/bottom_mean
    top_countries = df_top.index.tolist()
    bottom_countries = df_bottom.index.tolist()
    print(col_by,':')
    if (col_by=='kaggler salary over country average'):
        print('top',n_top_or_bottom,':',round(top_mean,2),top_countries)
        print('bottom',n_top_or_bottom,':',round(bottom_mean,2),bottom_countries)
    else:
        print('top',n_top_or_bottom,':',int(top_mean),top_countries)
        print('bottom',n_top_or_bottom,':',int(bottom_mean),bottom_countries)        
    print('top/bottom:',round(top_by_bottom,2))
    print('')
    return(top_countries,bottom_countries)
    
(tc1,bc1)=top_and_bottom('salary averages',n_top_or_bottom)
(tc2,bc2)=top_and_bottom('kaggler salary over cost index',n_top_or_bottom)


# #### Observations
# Generally, countries with higher compensations also have higher comtensations to cost index ratios but the difference between 'top 5' and 'bottom 5' countries becomes better: 7 times difference in absolute compensation values vs 3 times difference in compensation-over-cost index ratios.
# <br><br>
# **USA**, **Australia**, and **Israel** are among top 5 countries both in terms of the highest absolute values of yearly compensations as well as in terms of ratios of the compensation over the cost index.
# <br><br>
# **Nigeria**, **Viet Nam**, **Iran**, and **Turkey** are among both groups of five countries with the five lowest absolute values of yearly compensations as well as the compensations divided over the cost index. 
# <br><br>
# **Switzerland** has the highest absolute value of an average yearly kaggler's compensation, however, due to it's very high cost index, it is not among top five countries in terms of compensation-over-cost index ratio.
# <br><br>
# **India** is among 20 the least paying countries from our list but is in top 5 if the kaggle's compensation is divided over the cost index
# 
# <br><br>
# More interesting observations can be made if in addition to the two quantities discussed above we take a look into 
# #### the ratio of the country kaggler's average yearly compensation over the average annual income for residents of a given country

# In[ ]:


(tc1,bc1)=top_and_bottom('salary averages',n_top_or_bottom)
(tc2,bc2)=top_and_bottom('kaggler salary over cost index',n_top_or_bottom)
(tc3,bc3)=top_and_bottom('kaggler salary over country average',n_top_or_bottom)

#print(set(tc1+bc1+tc2+bc2+tc3+bc3))


# The largest professional kaggler's groups are data scientists, software engineers and data analysts. As one would expect, these professionals have a higher-than-average income in their countries - in no countries this ratio is found to be less than 1.
# <br><br>
# The largest ratios of kaggler's to country-wide average salary compensatons are found for **Kenya**, **India**, **Pakistan**, **Bangladesh**, and **Ukraine** averaging to as high as over 15(!) for these 5 countries. For that reason 'salary mins' are used to estimate this quantity rather than 'salary averages' - so that these estimates are at the lower boundary, and actual ratios are even higher. **If you reside in one of these countries, please feel free to comment.** (And, by the way, if you are not residing in one of these countries, still feel free to comment).
# <br><br>
# *Note: **India** is also in the top 5 of the best of kaggler compensation to the cost of living ratio.*
# <br><br>
# The smallest ratios of kaggler to country-wide average salary compensatons are found for **Norway**, **Austria**, **Greece**, **Finland**, and **Sweden**. The average value of the mean values of a kaggler income divided over a country wide income only slightly exceeds 1 (1.14). **Greece** is also among 5 countries with the worsk kaggler over the cost index ratio.
# <br><br>
# I wonder who the non-student **Greek kagglers** are

# In[ ]:


salary_quantification_col = 'salary averages'
df_title = df[['job title','country',salary_quantification_col]]
df_title = df_title[df_title['country']=='Greece']
df_title = df_title[df_title['job title']!='Other']
order = values_by_salary_order(df_title,'job title',salary_quantification_col)
plot_one_count_and_box_plot(df_title,'job title',
                            salary_quantification_col,'job title',order)


# Thus, Greek kagglers are mostly data scientists and software engineers, just as for the community in general.

# In[ ]:


df_by_country = df_by_country[df_by_country['country average income']!=-1]
df_by_country = df_by_country[df_by_country['cost of living index']!=-1]

fig, ax =plt.subplots(1,2,figsize=(18,12),sharey=True)
g1 = sns.regplot(x='kaggler salary over cost index',
           y='salary averages',data=df_by_country, ax=ax[0])
out = ax[0].set_ylim(0,120000)
out = ax[0].set_xlim(250,1750)
g2 = sns.regplot(x='kaggler salary over country average low estimate',
           y='salary averages',data=df_by_country,ax=ax[1])
out = ax[1].set_ylim(0,120000)
out = ax[1].set_xlim(0,30)
out = g1.set_xlabel('kaggler salary over cost index',fontsize=20)
out = g2.set_xlabel('kaggler salary over country average (low estimate)',fontsize=20)
out = g1.set_ylabel('kaggler salary average [USD]',fontsize=20)
out = g2.set_ylabel('')
g1.tick_params(labelsize=14)
g2.tick_params(labelsize=14)
out = fig.suptitle('Kaggler salary average vs the same thing \n divided over living cost index and over country-wide average income \n (one dot - one country)',fontsize=24)


# The right plot shows us that while for most countries the kagglers salary is about two times higher than a country-wide average income, for some countries this ratio is much higher. All such countries are in a group of a relatively low-paying standards.

# ## Conclusions
# 
# The primary focus of this kernel is to investigate kaggler's yearly compensations in different countries. 56 countries with the highest numbers of respondents in the 2018 Kaggle Survey are considered. Countries with at least 50 respondents are featured in the released dataset. After removing respondens with unknown salaries, students, and people who answered the survey too fast, countries with the lowest number of respondents become **Tunisia** (19 respondents) and **Morocco** (25 respondents).
# <br><br>
# While a total number of respondents from a country shows a little effect on the average country's compensation, a ratio of a number of non-student kagglers divided over the total country's population is found to correlate with a kaggler's yearly compensation. 
# <br><br>
# Countries with the highest and lowest kaggler's yearly compensations are identified

# In[ ]:


(tc1,bc1)=top_and_bottom('salary averages',n_top_or_bottom)


# which significantly overlap with countries with the highest and lowest compensations divided over the country living cost index 

# In[ ]:


(tc2,bc2)=top_and_bottom('kaggler salary over cost index',n_top_or_bottom)


# and have very little in common with the ratio of a kaggler's compensation over the country-wide average income

# In[ ]:


(tc3,bc3)=top_and_bottom('kaggler salary over country average',n_top_or_bottom)


# If one is interested in a combination of the absolute values of yearly compensations and it's ratio to the living cost index, the best countries to work in are **USA**, **Australia**, and **Israel**.
# <br><br>
# For someone who cares more about having a higher living standards compared to people around but doesn't care that much about the absolute amount of $$, **India** might be the best option.

# ## Are you happy with the situation in your country? 
# ## What are you willing to change?

# In[ ]:




