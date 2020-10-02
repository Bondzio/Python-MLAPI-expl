#!/usr/bin/env python
# coding: utf-8

# # Importing The Libraries

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import stats
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)

get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings("ignore")

import os
print(os.listdir("../input"))


# In[ ]:


get_ipython().system('pip install chart_studio')


# In[ ]:


from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode,plot,iplot
init_notebook_mode(connected=True) 
import chart_studio.plotly as py
import plotly.graph_objs as go
from PIL import Image
import requests
from io import BytesIO


# ## Loading the Data

# In[ ]:


fifa = pd.read_csv('../input/fifa19/data.csv')


# ## To Display all the Columns

# In[ ]:


pd.set_option('display.max_columns',None)


# In[ ]:


fifa.head()


# # Data Cleaning

# In[ ]:


del fifa['Unnamed: 0']


# In[ ]:


fifa.isnull().sum()


# In[ ]:


fifa.head()


# ## Converting Value and Wage into simpler form

# In[ ]:


list_val = []
for i in fifa.Value:
    if i[-1] == 'M':
        list_val.append(float(i[1:-1])*1000000)
    elif i[-1] == 'K':
        list_val.append(float(i[1:-1])*1000)
    else:
        list_val.append(float(i[1]))


# In[ ]:


fifa['Value'] = list_val


# In[ ]:


fifa.head()


# In[ ]:


list_wage = []
for i in fifa.Wage:
    if i[-1] == 'K':
        list_wage.append(float(i[1:-1])*1000)
    else:
        list_wage.append(float(i[1]))


# In[ ]:


fifa['Wage'] = list_wage


# ## Filling The Missing values in 'Preferred Foot' by their Binomial Distribution 

# In[ ]:


fifa['Preferred Foot'].value_counts()


# In[ ]:


foot = fifa['Preferred Foot'].value_counts(normalize=True)
foot_null = fifa['Preferred Foot'].isnull()
fifa.loc[fifa['Preferred Foot'].isnull(),'Preferred Foot'] = np.random.choice(
    foot.index, size=foot_null.sum(), p=foot.values)


# In[ ]:


fifa['Preferred Foot'].value_counts()


# ## Filling other columns by their mean.

# In[ ]:


fifa['Weak Foot'].fillna(round(float(fifa['Weak Foot'].mean()),0), inplace=True)


# In[ ]:


fifa['International Reputation'].fillna(round(float(fifa['International Reputation'].mean()),0), inplace=True)


# In[ ]:


fifa['Skill Moves'].fillna(round(float(fifa['Skill Moves'].mean()),0), inplace=True)


# In[ ]:


fifa.isnull().sum()


# ## Treating the Position and Attribute columns

# In[ ]:


for i in range(27,53):
    fifa.iloc[:,i].fillna(method="ffill", inplace=True)


# In[ ]:


for i in range(27,53):
    fifa.iloc[:,i] = fifa.iloc[:,i].str[:2]


# In[ ]:


list1 = []
for i in range(27,53):
    for j in fifa.iloc[:,i]:
        list1.append(float(j))
    fifa.iloc[:,i] = list1
    list1.clear()   


# In[ ]:


fifa.head()


# In[ ]:


fifa['Position Mean'] = round(fifa.iloc[:,[i for i in range(27,53)]].median(axis=1),0)


# In[ ]:


for i in range(53,87):
    fifa.iloc[:,i].fillna(method="ffill", inplace=True)


# In[ ]:


fifa['Attribute Mean'] = round(fifa.iloc[:,[i for i in range(53,87)]].median(axis=1),0)


# In[ ]:


fifa.head()


# ## Treating the Height & Weight Columns and Calculating every player's BMI.

# In[ ]:


fifa['Weight'].fillna(method='ffill', inplace=True)


# In[ ]:


list_weight = []
for i in fifa.Weight.str[0:3]:
    list_weight.append(float(i))
fifa['Weight'] = list_weight


# In[ ]:


fifa.head()


# In[ ]:


fifa['Height'].fillna(method='ffill', inplace=True)


# In[ ]:


fifa.Height.isnull().sum()


# In[ ]:


list_height = []
for i in fifa.Height:
    list_height.append((int(i[0])*12)+int(i[2])) 
fifa['Height'] = list_height


# In[ ]:


fifa.head()


# In[ ]:


fifa['BMI'] = round((fifa.Weight*703)/(fifa.Height)**2,2)


# In[ ]:


list_bmi = []
for i in fifa.BMI:
    if i < 18.5:
        list_bmi.append('Underweight')
    elif (i >= 18.5)and(i < 25):
        list_bmi.append('Normal')
    elif (i >= 25) and (i < 30):
        list_bmi.append('Overweight')
    elif (i >= 30):
        list_bmi.append('Obese')


# In[ ]:


fifa['Weight Class'] = list_bmi


# In[ ]:


fifa.head()


# # Looking at the Missing Values throughout the Dataset
# ### The Relevant columns are already cleaned.

# In[ ]:


import missingno
missingno.matrix(fifa, figsize=(40,20))


# # To Find out the Significant Features that determine a Player's value.

# In[ ]:


x_train = fifa[['Age','Overall','Wage','Special','International Reputation',
         'Weak Foot','Skill Moves','Height','Weight','Position Mean','Attribute Mean',
         'BMI']]
y_train = fifa.Value


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()


# In[ ]:


x_train.head()


# In[ ]:


from mlxtend.feature_selection import SequentialFeatureSelector as sfs

sfs1 = sfs(rf,k_features=5,cv=2)
sfs1 = sfs1.fit(x_train,y_train)
feat_cols = list(sfs1.k_feature_idx_)
print(feat_cols)


# ## So The 5 most Significant Features which play a vital role in determining a Player's Value are:- Overall Ratings, Wage, International Reputation, Weak Foot and Skill Moves.

# In[ ]:


x_train.iloc[:,feat_cols].head()


# # Fifa Best 11

# In[ ]:


a=3
b=2
c=1


# ## Best Goalkeeper

# In[ ]:


fifa['GK_Overall'] = (b*fifa.Balance + b*fifa.Stamina + b*fifa.ShortPassing + c*fifa.Aggression + b*fifa.LongPassing + 
                      a*fifa.Agility + a*fifa.Reactions + a*fifa.Jumping +  b*fifa.Vision +  b*fifa.Composure +  
                      a*fifa.GKDiving +  a*fifa.GKHandling +  a*fifa.GKKicking+  a*fifa.GKPositioning+ 
                      a*fifa.GKReflexes + a*fifa.Strength + a*fifa.Overall + a*fifa["International Reputation"])


# In[ ]:


gk = fifa.sort_values('GK_Overall', ascending=False)[:5]


# In[ ]:


trace_gk=go.Bar(
            x=gk.Name,
            y=gk.GK_Overall,
            name="GK_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=gk.Nationality)
data_gk=[trace_gk]
layout_gk=dict(title="Best Goalkeepers"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_gk=go.Figure(data=data_gk, layout=layout_gk)
iplot(fig_gk)


# In[ ]:


sns.stripplot(x=gk['Name'], y=gk['GK_Overall'], data=fifa, hue='Preferred Foot')
plt.show()


# ## Best Center Backs

# In[ ]:


fifa['CB_Overall'] = (a*fifa.Agility + a*fifa.Strength + a*fifa.Composure+ a*fifa.Aggression+ a*fifa.Balance+ a*fifa.Reactions+ 
                      a*fifa.StandingTackle+ a*fifa.SlidingTackle+ a*fifa.Marking+ a*fifa.Positioning
                     + a*fifa.Interceptions+ b*fifa.Jumping + b*fifa.BallControl + b*fifa.HeadingAccuracy +
                      b*fifa.LongPassing + b*fifa.ShortPassing+ b*fifa.Vision+ b*fifa.Stamina+ c*fifa.Dribbling + 
                      a*fifa.Overall + a*fifa['International Reputation'])


# In[ ]:


cb = fifa.sort_values('CB_Overall', ascending=False)


# In[ ]:


lcb = cb[(cb['Position']=='CB') | (cb['Position']=='LCB')]
lcb1 = lcb.sort_values('CB_Overall',ascending=False)[:5]


# In[ ]:


rcb = cb[(cb['Position']=='CB') | (cb['Position']=='RCB')]
rcb1 = rcb.sort_values('CB_Overall',ascending=False)[:5]


# In[ ]:


trace_lcb=go.Bar(
            x=lcb1.Name,
            y=lcb1.CB_Overall,
            name="CB_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=lcb1.Nationality)
data_lcb=[trace_lcb]
layout_lcb=dict(title="Best Left Center Backs"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_lcb=go.Figure(data=data_lcb, layout=layout_lcb)
iplot(fig_lcb)


# In[ ]:


sns.stripplot(x=lcb1['Name'], y=lcb1['CB_Overall'], data=lcb1, hue='Preferred Foot')
plt.show()


# In[ ]:


trace_rcb=go.Bar(
            x=rcb1.Name,
            y=rcb1.CB_Overall,
            name="RCB_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=rcb1.Nationality)
data_rcb=[trace_rcb]
layout_rcb=dict(title="Best Right Center Backs"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_rcb=go.Figure(data=data_rcb, layout=layout_rcb)
iplot(fig_rcb)


# In[ ]:


sns.stripplot(x=rcb1['Name'], y=rcb1['CB_Overall'], data=rcb1, hue='Preferred Foot')
plt.show()


# ## Best Full Backs

# In[ ]:


fifa["FullBacks"] = (a*fifa.SprintSpeed + a*fifa.Acceleration + a*fifa.Agility + a*fifa.Stamina + a*fifa.Aggression +
                    a*fifa.Positioning + a*fifa.Marking + a*fifa.SlidingTackle + a*fifa.StandingTackle + a*fifa.Crossing+ 
                    a*fifa.Dribbling + a*fifa.Reactions + 
                    b*fifa.Strength + b*fifa.BallControl + b*fifa.Curve + b*fifa.HeadingAccuracy +
                    b*fifa.Interceptions + b*fifa.Composure + b*fifa.Vision+ 
                    b*fifa.Jumping + b*fifa.Balance + b*fifa.LongPassing + b*fifa.ShortPassing +
                    c*fifa.Volleys )


# In[ ]:


fb = fifa.sort_values('FullBacks', ascending=False)


# In[ ]:


lfb = fb[(fb['Position']=='LB') | (fb['Position']=='LWB')]
lfb1 = lfb.sort_values('FullBacks',ascending=False)[:5]


# In[ ]:


rfb = fb[(fb['Position']=='RB') | (fb['Position']=='RWB')]
rfb1 = rfb.sort_values('FullBacks',ascending=False)[:5]


# In[ ]:


trace_lfb=go.Bar(
            x=lfb1.Name,
            y=lfb1.FullBacks,
            name="Fullbacks",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=lfb1.Nationality)
data_lfb=[trace_lfb]
layout_lfb=dict(title="Best Left Backs"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_lfb=go.Figure(data=data_lfb, layout=layout_lfb)
iplot(fig_lfb)


# In[ ]:


sns.stripplot(x=lfb1['Name'], y=lfb1['FullBacks'], data=lfb1, hue='Preferred Foot')
plt.show()


# In[ ]:


trace_rfb=go.Bar(
            x=rfb1.Name,
            y=rfb1.FullBacks,
            name="FullBacks",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=rfb1.Nationality)
data_rfb=[trace_rfb]
layout_rfb=dict(title="Best Right Backs"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_rfb=go.Figure(data=data_rfb, layout=layout_rfb)
iplot(fig_rfb)


# In[ ]:


sns.stripplot(x=rfb1['Name'], y=rfb1['FullBacks'], data=rfb1, hue='Preferred Foot')
plt.show()


# ## Best Center Defensive Midfielder

# In[ ]:


fifa['CDM_Overall'] = (a*fifa.ShortPassing + a*fifa.LongPassing +a*fifa.BallControl 
            +a*fifa.Composure + a*fifa.Balance
            +a*fifa.Positioning +a*fifa.Strength +
            a*fifa.Agility +a*fifa.Vision +
            b*fifa.Reactions + b*fifa.Dribbling +b*fifa.Acceleration +b*fifa.Stamina +
            b*fifa.LongShots +b*fifa.Interceptions +b*fifa.StandingTackle 
            +b*fifa.SlidingTackle +
            b*fifa.Marking +b*fifa.Jumping + b*fifa.HeadingAccuracy +
            c*fifa.Finishing)


# In[ ]:


cdm = fifa.sort_values('CDM_Overall', ascending=False) 


# In[ ]:


cdm1 = cdm[(cdm['Position'] == 'CDM') | (cdm['Position'] == 'LDM') | (cdm['Position'] == 'RDM')][:5]


# In[ ]:


trace_cdm=go.Bar(
            x=cdm1.Name,
            y=cdm1.CDM_Overall,
            name="CDM_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=cdm1.Nationality)
data_cdm=[trace_cdm]
layout_cdm=dict(title="Best Center Defensive Midfielders"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_cdm=go.Figure(data=data_cdm, layout=layout_cdm)
iplot(fig_cdm)


# In[ ]:


sns.stripplot(x=cdm1['Name'], y=cdm1['CDM_Overall'], data=cdm1, hue='Preferred Foot')
plt.show()


# In[ ]:


fifa['CM_Overall'] = (a*fifa.ShortPassing + a*fifa.LongPassing +a*fifa.BallControl 
            +a*fifa.Composure + a*fifa.Balance
            +a*fifa.Positioning +a*fifa.Strength +
            a*fifa.Agility +a*fifa.Vision +
            b*fifa.Reactions + b*fifa.Dribbling +b*fifa.Acceleration +b*fifa.Stamina +
            b*fifa.LongShots +b*fifa.Interceptions +b*fifa.StandingTackle 
            +b*fifa.SlidingTackle +
            b*fifa.Marking +b*fifa.Jumping + b*fifa.HeadingAccuracy +
            c*fifa.Finishing)


# In[ ]:


cm = fifa.sort_values('CM_Overall', ascending=False) 


# In[ ]:


cm1 = cm[(cm['Position'] == 'CM') | (cm['Position'] == 'LCM') | (cm['Position'] == 'RCM')][:5]


# In[ ]:


trace_cm=go.Bar(
            x=cm1.Name,
            y=cm1.CM_Overall,
            name="CM_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=cm1.Nationality)
data_cm=[trace_cm]
layout_cm=dict(title="Best Center Midfielders"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_cm=go.Figure(data=data_cm, layout=layout_cm)
iplot(fig_cm)


# In[ ]:


sns.stripplot(x=cm1['Name'], y=cm1['CM_Overall'], data=cm1, hue='Preferred Foot')
plt.show()


# ## Best Attacking Midfielder

# In[ ]:


fifa['CAM_Overall'] = (a*fifa.Marking + a*fifa.Positioning +a*fifa.BallControl
                       +a*fifa.ShortPassing + a*fifa.Dribbling +a*fifa.Agility
                       +a*fifa.Composure +a*fifa.Stamina +
                       a*fifa.LongShots +a*fifa.Aggression +a*fifa.Vision
                       +a*fifa.Acceleration + b*fifa.Finishing + b*fifa.Crossing
                       + b*fifa.HeadingAccuracy+ b*fifa.ShotPower + b*fifa.SprintSpeed
                       + b*fifa.Curve+ b*fifa.Volleys + c*fifa.Strength + 
                       c*fifa.StandingTackle + c*fifa.SlidingTackle)


# In[ ]:


cam = fifa.sort_values('CAM_Overall', ascending=False) 


# In[ ]:


cam1 = cam[(cam['Position'] == 'CAM') | (cam['Position'] == 'LAM') | (cam['Position'] == 'RAM')][:5]


# In[ ]:


trace_cam=go.Bar(
            x=cam1.Name,
            y=cam1.CAM_Overall,
            name="CAM_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=cam1.Nationality)
data_cam=[trace_cam]
layout_cam=dict(title="Best Center Attacking Midfielders"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_cam=go.Figure(data=data_cam, layout=layout_cam)
iplot(fig_cam)


# In[ ]:


sns.stripplot(x=cam1['Name'], y=cam1['CAM_Overall'], data=cam1, hue='Preferred Foot')
plt.show()


# ## Best Left Winger

# In[ ]:


fifa['LW_Overall'] = (a*fifa.Crossing + a*fifa.Dribbling +a*fifa.Aggression +
                      a*fifa.Stamina +a*fifa.Agility +a*fifa.BallControl +
                      a*fifa.Curve +a*fifa.Balance +a*fifa.Positioning +
                      a*fifa.Marking +a*fifa.SprintSpeed +a*fifa.Acceleration +
                      b*fifa.Strength + b*fifa.ShotPower +b*fifa.Finishing +
                      b*fifa.ShortPassing +b*fifa.Volleys +b*fifa.Vision +
                      b*fifa.Interceptions + c*fifa.Jumping)


# In[ ]:


lw = fifa.sort_values('LW_Overall', ascending=False)


# In[ ]:


lw1 = lw[(lw['Position'] == 'LW') | (lw['Position'] == 'LM') | (lw['Position'] == 'LF')][:5]


# In[ ]:


trace_lw=go.Bar(
            x=lw1.Name,
            y=lw1.LW_Overall,
            name="LW_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=lw1.Nationality)
data_lw=[trace_lw]
layout_lw=dict(title="Best Left Wingers"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_lw=go.Figure(data=data_lw, layout=layout_lw)
iplot(fig_lw)


# In[ ]:


sns.stripplot(x=lw1['Name'], y=lw1['LW_Overall'], data=lw1, hue='Preferred Foot')
plt.show()


# ## Best Right Winger

# In[ ]:


fifa['RW_Overall'] = (a*fifa.Crossing + a*fifa.Dribbling +a*fifa.Aggression +
                      a*fifa.Stamina +a*fifa.Agility +a*fifa.BallControl +
                      a*fifa.Curve +a*fifa.Balance +a*fifa.Positioning +
                      a*fifa.Marking +a*fifa.SprintSpeed +a*fifa.Acceleration +
                      b*fifa.Strength + b*fifa.ShotPower +b*fifa.Finishing +
                      b*fifa.ShortPassing +b*fifa.Volleys +b*fifa.Vision +
                      b*fifa.Interceptions + c*fifa.Jumping)


# In[ ]:


rw = fifa.sort_values('RW_Overall', ascending=False)


# In[ ]:


rw1 = rw[(rw['Position'] == 'RW') | (rw['Position'] == 'RM') | (rw['Position'] == 'RF')][:5]


# In[ ]:


trace_rw=go.Bar(
            x=rw1.Name,
            y=rw1.RW_Overall,
            name="RW_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=rw1.Nationality)
data_rw=[trace_rw]
layout_rw=dict(title="Best Right Wingers"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_rw=go.Figure(data=data_rw, layout=layout_rw)
iplot(fig_rw)


# In[ ]:


sns.stripplot(x=rw1['Name'], y=rw1['RW_Overall'], data=rw1, hue='Preferred Foot')
plt.show()


# ## Best Striker

# In[ ]:


fifa['ST_Overall'] = (a*fifa.Finishing + a*fifa.HeadingAccuracy +a*fifa.Volleys +
                      a*fifa.BallControl +a*fifa.Composure +a*fifa.Balance +
                      a*fifa.Strength +a*fifa.Positioning +a*fifa.Jumping +
                      a*fifa.ShotPower +a*fifa.Agility +a*fifa.Acceleration +
                      b*fifa.Dribbling + b*fifa.ShortPassing +b*fifa.Curve +
                      b*fifa.SprintSpeed +b*fifa.Stamina +b*fifa.Aggression +
                      c*fifa.Crossing)


# In[ ]:


st = fifa.sort_values('ST_Overall', ascending=False)


# In[ ]:


st1 = st[(st['Position'] == 'ST') | (st['Position'] == 'ST') | (st['Position'] == 'ST')][:5]


# In[ ]:


trace_st=go.Bar(
            x=st1.Name,
            y=st1.ST_Overall,
            name="ST_Overall",
            marker=dict(color="rgba(72,240,224,0.8)"),
            text=st1.Nationality)
data_st=[trace_st]
layout_st=dict(title="Best Strikers"
            ,xaxis=dict(title="Names",ticklen=5,zeroline=False),
            yaxis=dict(title="Overall Ratings",ticklen=5,zeroline=False))
fig_st=go.Figure(data=data_st, layout=layout_st)
iplot(fig_st)


# In[ ]:


sns.stripplot(x=st1['Name'], y=st1['ST_Overall'], data=st1, hue='Preferred Foot')
plt.show()


# # Plotting the Team

# In[ ]:


list_photo = [gk.Photo.iloc[0],lfb1.Photo.iloc[0],lcb1.Photo.iloc[0],rcb1.Photo.iloc[0],
            rfb1.Photo.iloc[0],cdm1.Photo.iloc[0],cam1.Photo.iloc[0],cm1.Photo.iloc[0],
            lw1.Photo.iloc[0],st1.Photo.iloc[0],rw1.Photo.iloc[0]]


# In[ ]:


list_team = [gk.Name.iloc[0],lfb1.Name.iloc[0],lcb1.Name.iloc[0],rcb1.Name.iloc[0],
            rfb1.Name.iloc[0],cdm1.Name.iloc[0],cam1.Name.iloc[0],cm1.Name.iloc[0],
            lw1.Name.iloc[0],st1.Name.iloc[0],rw1.Name.iloc[0]]
list_team


# In[ ]:


list_posi_x = [10  , 1.5, 6.8, 13.5, 18.5, 10  , 5.5 , 14  , 1.5 , 10   , 18.5]
list_posi_y = [2.9 , 6  , 6  , 6   ,    6, 10  , 13.5, 13.5, 17.5, 18.5 , 17.5]
list_name_x = [10.7, 2.2, 7.5, 14.2, 19.2, 10.7, 6.2 , 14.7, 2.2 , 10.8 , 19.3]
list_name_y = [0   , 3.1, 3.1, 3.1 ,  3.1, 7.1 , 10.6, 10.6, 14.6, 15.6 , 14.6]


# In[ ]:


play = []
for i in list_photo:
    response = requests.get(i)
    img_play = Image.open(BytesIO(response.content))
    play.append(np.array(img_play))


# In[ ]:


fig, ax = plt.subplots(figsize=(10,10))

def plot(x,y,image):
    xy = [x, y]
    imagebox = OffsetImage(image, zoom=1)
    imagebox.image.axes = ax
    ab = AnnotationBbox(imagebox, xy,)
    ax.add_artist(ab)

    
def names(x,y,text):
    xy1 = [x,y]
    offsetbox = TextArea(text, minimumdescent=False)
    ab1 = AnnotationBbox(offsetbox, xy1,
                        xybox=(-20, 40),
                        xycoords='data',
                        boxcoords="offset points")
    ax.add_artist(ab1)
ax.set_facecolor('#4FB352')
for i in range(0,11):
    plot(list_posi_x[i],list_posi_y[i],play[i])
    names(list_name_x[i],list_name_y[i],list_team[i])
    
ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
plt.title('Fifa Best 11')
plt.show()


# # Some Plots

# ### Age vs Overall vs Potential

# In[ ]:


sns.lmplot(x='Age', y='Overall', data=fifa, hue='Preferred Foot',markers=['o','v'],
          scatter_kws={'s':100}, size=10, palette='inferno')
plt.show()


# ### The average overall player rating is somewhere between 65 to 70

# In[ ]:


sns.distplot(fifa.Overall)
plt.axvline(x=fifa.Overall.mean())
plt.show()


# # Football Players Around the World

# In[ ]:


nations = pd.DataFrame(fifa.Nationality.value_counts())


# In[ ]:


nations.rename({'England':'UK'}, inplace=True)


# In[ ]:


nations.head()


# In[ ]:


data1 = dict(
        type = 'choropleth',
        locations = list(nations.index),
        locationmode = 'country names',
        colorscale = "Speed",
        z = list(nations.Nationality),
        colorbar = {'title' : 'Number Of Players'},
      ) 


# In[ ]:


layout1 = dict(
    title = 'Football Players Around the World',
    geo = dict(
        showframe = False
    )
)


# In[ ]:


choromap = go.Figure(data = [data1],layout = layout1)
iplot(choromap)


# In[ ]:




