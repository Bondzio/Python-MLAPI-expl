#!/usr/bin/env python
# coding: utf-8

# ![andy-li-7WHr0xmGiBA-unsplash.jpg](attachment:andy-li-7WHr0xmGiBA-unsplash.jpg)

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
from matplotlib import cm
import seaborn as sns
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)    #THIS LINE IS MOST IMPORTANT AS THIS WILL DISPLAY PLOT ON 
#NOTEBOOK WHILE KERNEL IS RUNNING
import plotly.graph_objects as go

from IPython.display import HTML,display
import warnings
warnings.filterwarnings("ignore")

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # **Introduction**
# 
# Murder is the top most category of crime in India. Currently India's homicide rate is 3.08 per 100,000 population. The objective of this notebook is to see the trend of murder victims  over the years as well as murder victims per state. first lets see the data.

# In[ ]:


murder = pd.read_csv("../input/crime-in-india/32_Murder_victim_age_sex.csv")
murder.Year.unique()
murder.Area_Name.unique()
murder.Sub_Group_Name.unique()
murder.head(10)


# This dataset contains Victim's information from year 2001 to 2010 and 35 states & Union territories. The age group is divided into 6 categories.
# * less than 10 year old victims
# * 10-15 year old victims
# * 15-18 year old victims
# * 18-30 year old victims
# * 30-50 year old victims
# * 50 + older victims

# In[ ]:


from IPython.core.display import HTML
HTML('''<div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/2693755" data-url="https://flo.uri.sh/visualisation/2693755/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>''')


# # Murder Victims Per Year

# In[ ]:




murdert = murder[murder['Sub_Group_Name']== '3. Total']  #keeping only total category of subgroup
murdery = murdert.groupby(['Year'])['Victims_Total'].sum().reset_index() #grouping
sns.set_context("talk")
plt.style.use("fivethirtyeight")
plt.figure(figsize = (14,10))
#sns.palplot(sns.color_palette("hls", 8))
ax = sns.barplot(x = 'Year' , y = 'Victims_Total' , data = murdery ,palette= 'dark') #plotting bar graph
plt.title("Total Victims of Murder per Year")
ax.set_ylabel('')
for p in ax.patches:
             ax.annotate("%.f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', fontsize=15, color='black', xytext=(0, 8),
                 textcoords='offset points')


# **Inference** : We can see that the no. of victims is gradually decresing over the years.

# Gender of the victims

# In[ ]:


murderg = murder.groupby(['Year' , 'Sub_Group_Name'])['Victims_Total'].sum().reset_index() # grouping with year and sub group
murderg = murderg[murderg['Sub_Group_Name']!= '3. Total']   # we dont need total category of sub group

plt.style.use("fivethirtyeight")
plt.figure(figsize = (14,10))
ax = sns.barplot( x = 'Year', y = 'Victims_Total' , hue = 'Sub_Group_Name' , data = murderg ,palette= 'bright') #plotting barplot
plt.title('Gender Distribution of Victims per Year',size = 20)
ax.set_ylabel('')


# Inference: Males are more prone to be murder victim as compared to women . Over the years the number of male victims has decreased but the number of female victims is almost same as the previous years.

# **Age of the victim**

# In[ ]:


murdera = murder.groupby(['Year'])['Victims_Upto_10_15_Yrs','Victims_Above_50_Yrs',
                                   'Victims_Upto_10_Yrs', 'Victims_Upto_15_18_Yrs',
                                   'Victims_Upto_18_30_Yrs','Victims_Upto_30_50_Yrs',].sum().reset_index()  #grouby year and age group
murdera = murdera.melt('Year', var_name='AgeGroup',  value_name='vals') #melting the dataset

plt.style.use("fivethirtyeight")
plt.figure(figsize = (14,10))
ax = sns.barplot(x = 'Year' , y = 'vals',hue = 'AgeGroup' ,data = murdera ,palette= 'bright') #plotting a bar
plt.title('Age Distribution of Victims per Year',size = 20)
ax.get_legend().set_bbox_to_anchor((1, 1)) #anchoring the labels so that they dont show up on the graph
ax.set_ylabel('')


# **Inference**: Compared to people of other ages the age group 18 - 30 years is more prone to be victim of the murder. The rise in 2002 numbers is **maybe** due to the riots of gujrat . Another age group which is most likely to be victim of murder is 30 - 50. Compared to these two groups other age groups are very small in number. From all the groups children are most likely to be safe.

# # Age & Gender of the victim

# In[ ]:


murderag = murder.groupby(['Sub_Group_Name'])['Victims_Upto_10_15_Yrs',
                                              'Victims_Above_50_Yrs', 'Victims_Upto_10_Yrs',
                                              'Victims_Upto_15_18_Yrs','Victims_Upto_18_30_Yrs',
                                              'Victims_Upto_30_50_Yrs',].sum().reset_index()       #grouping with the gender and age groups

murderag = murderag.melt('Sub_Group_Name', var_name='AgeGroup',  value_name='vals')  #melting the dataset for drawing the desired plot
murderag= murderag[murderag['Sub_Group_Name']!= '3. Total']

plt.style.use("fivethirtyeight")
plt.figure(figsize = (14,10))
ax = sns.barplot(x = 'Sub_Group_Name' , y = 'vals',hue = 'AgeGroup' ,data = murderag,palette= 'colorblind') #making barplot taking Agegroup as hue/category 
plt.title('Age & Gender Distribution of Victims',size = 20)
ax.get_legend().set_bbox_to_anchor((1, 1)) #using anchor so that legend doesnt show on the graph
ax.set_ylabel('')
ax.set_xlabel('Victims Gender')
for p in ax.patches:
             ax.annotate("%.f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', fontsize=15, color='black', xytext=(0, 8),
                 textcoords='offset points')


# Inference: Males of age 18-30 are more likely to be get killed as compared to the any of the age-gender group. After them male of 30-50 are prone to be victim of murder. Similar to male age groups females of age 18-30 are more likely to be get killed . 

# # Murders: Statewise

# In[ ]:


murderst = murder[murder['Sub_Group_Name']== '3. Total']   #we need only total number of victims per state
murderst= murderst.groupby(['Area_Name'])['Victims_Total'].sum().sort_values(ascending = False).reset_index()
new_row = {'Area_Name':'Telangana', 'Victims_Total':27481}
murderst = murderst.append(new_row , ignore_index=True )
murderst.sort_values('Area_Name')
import geopandas as gpd
gdf = gpd.read_file('../input/india-states/Igismap/Indian_States.shp')
murderst.at[17, 'Area_Name'] = 'NCT of Delhi'
merged = gdf.merge(murderst, left_on='st_nm', right_on='Area_Name')
merged.drop(['Area_Name'], axis=1)
#merged.describe()


# In[ ]:



merged['coords'] = merged['geometry'].apply(lambda x: x.representative_point().coords[:])
merged['coords'] = [coords[0] for coords in merged['coords']]


sns.set_context("talk")
sns.set_style("dark")
#plt.style.use('dark_background')
cmap = 'YlGn'
figsize = (25, 20)

ax = merged.dropna().plot(column= 'Victims_Total', cmap=cmap, figsize=figsize, scheme='equal_interval',edgecolor='black')


for idx, row in merged.iterrows():
   ax.text(row.coords[0], row.coords[1], s=row['Victims_Total'], horizontalalignment='center', bbox={'facecolor': 'skyblue', 'alpha':0.8, 'pad': 2, 'edgecolor':'yellow'})


ax.set_title("Murders Per State", size = 25)

norm = matplotlib.colors.Normalize(vmin=merged['Victims_Total'].min(), vmax= merged['Victims_Total'].max())
n_cmap = cm.ScalarMappable(norm=norm, cmap= cmap)
n_cmap.set_array([])
ax.get_figure().colorbar(n_cmap)
ax.set_axis_off()
plt.axis('equal')
plt.show()


# In[ ]:


murders = murder[murder['Sub_Group_Name']== '3. Total']   #we need only total number of victims per state
murders= murders.groupby(['Area_Name'])['Victims_Total'].sum().sort_values(ascending = False).reset_index()
 
murdersbad = murders.head(15) #top highest states
murdersgood = murders.tail(15) #top lowest states/ut

#sns.set_context("talk")
sns.set_style("darkgrid")
plt.style.use("fivethirtyeight")

f , axes = plt.subplots(2,1, figsize = (15,14))
ax = sns.barplot(x = 'Victims_Total' , y = 'Area_Name' , data = murdersbad, ax = axes[0],palette= 'bright') #barplot for highest numbers of victims per state
axes[0].set_title("15 states  with Highest number of Victims", size = 20)
axes[0].set_ylabel('')
axes[0].set_xlabel('No. of Victims')
ax1 = sns.barplot(x = 'Victims_Total' , y = 'Area_Name' , data = murdersgood, ax = axes[1],palette= 'dark' )#barplot for lowest numbers of victims per state
axes[1].set_title("15 states and UT with lowest number of Victims", size = 20)
axes[1].set_ylabel('')
axes[1].set_xlabel('No. of Victims')
plt.tight_layout()  #tight layout so that subplots look fitted
plt.subplots_adjust(hspace= .3) #adjusting the space between the plots
#murders.to_csv('murder.csv',index=False)
for p in ax.patches:
        ax.annotate("%.f" % p.get_width(), xy=(p.get_width(), p.get_y()+p.get_height()/2),
            xytext=(5, 0), textcoords='offset points', ha="left", va="center")

for p in ax1.patches:
        ax1.annotate("%.f" % p.get_width(), xy=(p.get_width(), p.get_y()+p.get_height()/2),
            xytext=(5, 0), textcoords='offset points', ha="left", va="center")


# **Inference**: With almost 60000  murders Uttarpradesh has highest victims of murder. Bihar has second highest number of victims which has less than 25000 victims than Uttarpradesh. Interestingly Uttarpradesh  has the highest population in the country. Bihar has less population than maharashtra still it has higher number of victims than Maharashtra.
# 
# Union Territory Lakshadweep has lowest number of Murder Victims. Factors like population of the state and **Population density** might be responsible for the number of murder victims in the state.

# Gender Distribution of victims per state

# In[ ]:


murdergs = murder.groupby(['Area_Name' , 'Sub_Group_Name'])['Victims_Total'].sum().sort_values(ascending = False).reset_index() #groupby state and gender
murdergs = murdergs[murdergs['Sub_Group_Name']!= '3. Total'] #we dont need total category of gender
plt.figure(figsize = (14,15))
plt.style.use("fivethirtyeight")
sns.barplot( x = 'Victims_Total', y = 'Area_Name' , hue = 'Sub_Group_Name' , data = murdergs,palette= 'bright') #barplot
plt.title('Gender Distribution of Victims per State',size = 20)


# **Inference** : Similar to above results males are more likely to be get murdered as compared to females. Interesting thing to notice in this graph is Mahrashtra has second highest female victims.

# Statewise Distribution of victims according to their age

# In[ ]:


murdernt = murder[murder['Sub_Group_Name']== '3. Total']
murdersa = murdernt.groupby(['Area_Name'])['Victims_Upto_10_15_Yrs','Victims_Above_50_Yrs', 
                                           'Victims_Upto_10_Yrs', 'Victims_Upto_15_18_Yrs',
                                           'Victims_Upto_18_30_Yrs','Victims_Upto_30_50_Yrs',].sum().reset_index() #grouping with state and age group
murdersa = murdersa.melt('Area_Name', var_name='AgeGroup',  value_name='vals') #melting the dataset

sns.set_style("darkgrid")
sns.set_context("talk")
plt.style.use("fivethirtyeight")


f, axes = plt.subplots(3,2, figsize = (30,30))
plt.figure(figsize = (14,15))
sns.barplot(x = 'vals', y = 'Area_Name', data = murdersa[murdersa['AgeGroup']== 'Victims_Upto_10_Yrs'].sort_values(by=['vals'],ascending = False).head(10),ax = axes[0,0],palette= 'dark')
axes[0,0].set_title(' Age 0 - 10', size = 20)
axes[0,0].set_ylabel('')
axes[0,0].set_xlabel('No.of Victims')

sns.barplot(x = 'vals', y = 'Area_Name', data = murdersa[murdersa['AgeGroup']== 'Victims_Upto_10_15_Yrs'].sort_values(by=['vals'],ascending = False).head(10), ax = axes[0,1],palette= 'bright' )
axes[0,1].set_title(' Age 10 - 15', size = 20)
axes[0,1].set_ylabel('')
axes[0,1].set_xlabel('No.of Victims')    


sns.barplot(x = 'vals', y = 'Area_Name', data = murdersa[murdersa['AgeGroup']== 'Victims_Upto_15_18_Yrs'].sort_values(by=['vals'],ascending = False).head(10),ax = axes[1,0],palette= 'dark')
axes[1,0].set_title(' Age 15 - 18', size = 20)
axes[1,0].set_ylabel('')
axes[1,0].set_xlabel('No.of Victims')  

sns.barplot(x = 'vals', y = 'Area_Name', data = murdersa[murdersa['AgeGroup']== 'Victims_Upto_18_30_Yrs'].sort_values(by=['vals'],ascending = False).head(10), ax = axes[1,1],palette= 'bright' )
axes[1,1].set_title(' Age 18 - 30', size = 20)
axes[1,1].set_ylabel('')
axes[1,1].set_xlabel('No.of Victims')  

sns.barplot(x = 'vals', y = 'Area_Name', data = murdersa[murdersa['AgeGroup']== 'Victims_Upto_30_50_Yrs'].sort_values(by=['vals'],ascending = False).head(10), ax = axes[2,0],palette= 'dark')
axes[2,0].set_title(' Age 30 - 50', size = 20)
axes[2,0].set_ylabel('')
axes[2,0].set_xlabel('No.of Victims')  

sns.barplot(x = 'vals', y = 'Area_Name', data = murdersa[murdersa['AgeGroup']== 'Victims_Above_50_Yrs'].sort_values(by=['vals'],ascending = False).head(10),ax = axes[2,1],palette= 'bright')
axes[2,1].set_title(' Age 50 +', size = 20)
axes[2,1].set_ylabel('')
axes[2,1].set_xlabel('No.of Victims')  
plt.tight_layout()
#plt.subplots_adjust(hspace= .0001)


# **Inference** : Uttarpradesh has the highest number of murder victims in all age group except age group 0 - 10 , Surprisingly Maharashtra has the highest child victims  and Gujrat ranks second in case of child victims. Assam is the only north eastern state which comes under these graphs. 

# # **Conclusion**

# Although country level murder rate is decreasing slowly over the years. State like Uttarpradesh , Bihar , Mahrashtra , West Bengal has the high number of victims over the years. The male age group of 18-30 is most unsafe. So if you belong to this age group Be Safe.

# Running Bar Chart

# In[ ]:



#murderbr = murdert.groupby(['Year', 'Area_Name'])['Victims_Total'].sum().reset_index()
#murderbr = murderbr.pivot(index='Area_Name', columns='Year', values='Victims_Total').reset_index()
#murderbr.dropna()
#murderbr.to_csv('out.csv', index=False)

