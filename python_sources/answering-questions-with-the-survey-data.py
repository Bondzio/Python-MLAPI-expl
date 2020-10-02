#!/usr/bin/env python
# coding: utf-8

# # ANALYSIS OF 2018 KAGGLE ML & DS SURVEY 

# ![img](https://www.kaggle.com/static/images/home/computer.png)

# In[ ]:


import numpy as np 
import pandas as pd 
import warnings
import seaborn as sns
from matplotlib_venn import venn3
from matplotlib_venn import venn2
warnings.filterwarnings("ignore")
import matplotlib.pylab as plt
import squarify    


# In[ ]:


mcr = pd.read_csv('../input/multipleChoiceResponses.csv')
ffr = pd.read_csv('../input/freeFormResponses.csv')
ss = pd.read_csv('../input/SurveySchema.csv')


# In[ ]:


mcr.head()


# In[ ]:


time = mcr['Time from Start to Finish (seconds)']
time.pop(0)
minutes = [round(int(i)/60) for i in time]


# ## Time Taken by users to fill the Survey 

# In[ ]:


print("Maximum Time Taken By a User to fill the survey is:",max(minutes), 'Minutes' )
print("Minimum Time Taken By a User to fill the survey is:",min(minutes), 'Minutes' )
print("Average Time Taken By a User to fill the survey is:",sum(minutes)/len(minutes), 'Minutes' )


# ## Gender Distribution of users who filled the Survey 
# 
# > Looks like only 17% of the survey participant are females, Gotta pump those Numbers up

# In[ ]:


gender = mcr['Q1']
gender.pop(0)
names= mcr['Q1'].value_counts().index
names = np.array(names).tolist()
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
explode = (0, 0.1, 0, 0) 
size= mcr['Q1'].value_counts().values
plt.pie(size,explode=explode,labels=names,colors=colors,autopct='%1.1f%%', shadow=True)
plt.style.use('classic')
plt.show()


# ## Age Distribution of users who filled the Survey 
# > Most of the survey participants are between 25-29

# In[ ]:


val = mcr.groupby("Q2").filter(lambda x: len(x) > 1)
sns.countplot(x='Q2', palette="Pastel2",data = val);
plt.xticks(rotation=45)


# ## Usage of machine learning  in Various industries 

# In[ ]:


k = []
for i in val['Q7'].value_counts().index: 
    k.append(val[(val['Q7'] == i)]['Q10'].value_counts())


# In[ ]:


exploring = [k[i]['We are exploring ML methods (and may one day put a model into production)'] for i in range(0,19)]
started = [k[i]['We recently started using ML methods (i.e., models in production for less than 2 years)'] for i in range(0,19)]
established = [k[i]['We have well established ML methods (i.e., models in production for more than 2 years)'] for i in range(0,19)]
not_using = [k[i]['No (we do not use ML methods)'] for i in range(0,19)]
using = [k[i]['We use ML methods for generating insights (but do not put working models into production)'] for i in range(0,19)]
no = [k[i]['I do not know'] for i in range(0,19)]


# In[ ]:


barWidth = 0.25
plt.figure(figsize=(20,10))
r1 = np.arange(len(exploring))
plt.bar(r1,exploring, width=barWidth, edgecolor='white', label='Exploring ML methods')
plt.bar(r1,started, width=barWidth, edgecolor='white', label='Started using ML methods')
plt.bar(r1,established, width=barWidth, edgecolor='white', label='Have been using ML')
plt.bar(r1,not_using, width=barWidth, edgecolor='white', label='We dont use ML')
plt.bar(r1,using, width=barWidth, edgecolor='white', label='Use ML for insights not production')
plt.bar(r1,no, width=barWidth, edgecolor='white', label='I dont know')
params = {'legend.fontsize': 20,
          'legend.handlelength': 2}
plt.xlabel('group', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(exploring))], list(val['Q7'].value_counts().index))
plt.legend()
plt.rcParams.update(params)
plt.xlabel('Industry Type',fontsize=20)
plt.xticks(fontsize=20,rotation=90)
plt.style.use('ggplot')
plt.show()


# ##  Comparison of Data science students in India vs USA vs China vs Russia 
# 
# - Majority of the American, Chinese and Russian data scientists hold a masters degreee
# -  Only in India majority of data scientists have a bachelors degree

# In[ ]:


coun = val[(val['Q3'] == 'United States of America') |( val['Q3'] == 'India')|( val['Q3'] == 'China')|( val['Q3'] == 'Russia')]
plt.figure(figsize=(10,6))
params = {'legend.fontsize': 7,
          'legend.handlelength': 2}
plt.rcParams.update(params)

sns.countplot(x="Q3",hue="Q4", data=coun)
plt.show()


# ## Analysis with respect to Experience in USA, India, Russia and China
# - India has Highest numbers Noobs.....No suprise given the craze
# -  China has the best balance between Noobs/Experts

# In[ ]:


#val['Q8'].value_counts()
plt.figure(figsize=(10,6))
sns.countplot(x="Q3",hue="Q8", data=coun)
plt.title('Experience of ML practitioners')
plt.show()


# ## Age of Survey participants with respect to their designation
# 
# - Most of the data scientists, analysts and consultants are in their 20s and early 30s
# - As expected Students are between 18- 24 (Undergraduates and Postgraduates)
# - Managers , Chief officers, Business analysts and Statisicians tend to be older
# 

# In[ ]:


plt.figure(figsize=(10,40))
sns.countplot(y="Q6",hue="Q2", data=val, palette ='muted')
params = {'legend.fontsize': 10,
          'legend.handlelength': 2}
plt.rcParams.update(params)
plt.show()


# **Primary Tools of Data scientists**

# In[ ]:


val['Q12_MULTIPLE_CHOICE'].value_counts()
l = ['Jupyter/Rstudio','Statistical software(Excel etc)','Other','SAS,SPSS etc','Cloud based','BI software']
squarify.plot(sizes=val['Q12_MULTIPLE_CHOICE'].value_counts().values, label=l, alpha=.8 )
plt.axis('off')
plt.show() 


# ## Venn Diagram of the Programming Languages/IDE's used 

# In[ ]:


jupyter = val['Q13_Part_1'].count()
rstudio = val['Q13_Part_2'].count()
matlab = val['Q13_Part_7'].count()
jup_r = len(val[(val['Q13_Part_1']=='Jupyter/IPython') & (val['Q13_Part_2']=='RStudio')])
jup_mat = len(val[(val['Q13_Part_1']=='Jupyter/IPython') & (val['Q13_Part_7']=='MATLAB')])
r_mat = len(val[(val['Q13_Part_2']=='RStudio') & (val['Q13_Part_7']=='MATLAB')])
jup_r_mat = len(val[(val['Q13_Part_1']=='Jupyter/IPython') & (val['Q13_Part_2']=='RStudio')& (val['Q13_Part_7']=='MATLAB')])


# In[ ]:





# In[ ]:


v=venn3(subsets = (jupyter, rstudio, jup_r, matlab,jup_mat,r_mat,jup_r_mat), set_labels = ('Jupyter Notebook', 'R studio', 'Matlab'))
plt.title("ML and DL")
plt.show()


# In[ ]:


spy = val['Q13_Part_13'].count()
pyc = val['Q13_Part_3'].count()
s_p = len(val[(val['Q13_Part_13']=='Spyder') & (val['Q13_Part_3']=='PyCharm')])


# In[ ]:


v = venn2(subsets = (spy, pyc, s_p), set_labels = ('Spyder', 'Pycharm'))
plt.title("Python IDE's Pycharm vs Spyder")
plt.show()


# In[ ]:


sublime = val['Q13_Part_1'].count()
atom = val['Q13_Part_6'].count()
note = val['Q13_Part_7'].count()
sub_atom = len(val[(val['Q13_Part_10']=='Sublime Text') & (val['Q13_Part_6']=='Atom')])
sub_note = len(val[(val['Q13_Part_9']=='Notepad++') & (val['Q13_Part_7']=='MATLAB')])
atom_note = len(val[(val['Q13_Part_6']=='Atom') & (val['Q13_Part_9']=='Notepad++')])
sub_at_not = len(val[(val['Q13_Part_10']=='Sublime Text') & (val['Q13_Part_6']=='Atom')& (val['Q13_Part_9']=='Notepad++')])


# In[ ]:


v=venn3(subsets = (sublime, atom, sub_atom, note,sub_note,atom_note,sub_at_not), set_labels = ('Sublime ', 'Atom', 'Notepad++'))
plt.title("Source code editors")
plt.show()


# In[ ]:




