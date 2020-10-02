#!/usr/bin/env python
# coding: utf-8

# # Day3-30 PLots
# ## Pls UPVOTE!!if you liked it!!

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly
import plotly.express as px
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


data_student=pd.read_csv("../input/students-performance-in-exams/StudentsPerformance.csv")


# In[ ]:


data_student['Language']=data_student['reading score']+data_student['writing score']


# In[ ]:


data_student.head(10)


# In[ ]:


data_student.info()
#it's complete and happy


# In[ ]:


data_student.describe()


# #most people don't score too high around 65-70 is good and 25%,50%,75%show that
# BUt there are people who like marks,we have top scorers too who scored 100 on 100

# In[ ]:



#question:how race/ethnicity affect math score and how male and female from different ethinicity perform ??
fig1=px.scatter(data_student,x='race/ethnicity',y='math score',color='gender')
fig1.show()
#1-Inference:Male perform in 4 out of 5 groups perform better,and in 2 out of 5 groups male perform worst too...


# In[ ]:


fig1=px.scatter(data_student,x='race/ethnicity',y='Language',color='gender')
fig1.show()
#2-Inference:Females perform better than males in language in all grops except group E


# In[ ]:


fig=px.scatter(data_student,x='gender',y='math score',color='Language')
fig.show()
#3-Inference-Top performing females  perform at par with top performing males but female score mean is lower than males  


# In[ ]:


fig=px.scatter(data_student,x='gender',y='Language',color='math score')
fig.show()
#5-Inference-Females perform better than males in language and Average females score is higher than males one
#top performing student perform better in both maths and language


# In[ ]:


#how parents education affects children maths score and language score
fig=px.scatter_3d(data_student,x='race/ethnicity',y='parental level of education',z='math score',color='Language',symbol='gender')
fig.show()
#5-Inference:I can't make an inference how you can,circle is for females and square for males


# In[ ]:


fig=px.scatter_3d(data_student,x='test preparation course',y='parental level of education',z='math score',color='gender')
fig.show()
#6-Inference-with test preparation courses ,score imporove and all group send their kids for test preparation especially who went to unknown colleges or just high school,showing parents care about their childeren eduaction and put effort to improve it
#and weirdly who are more educated tend to more girls in their family


# In[ ]:


#question:what happens if you you take preparation and is there a difference between males and females overalll
fig = px.scatter_3d(data_student, x='Language', y='test preparation course', z='math score',color='gender',symbol='race/ethnicity')
fig.show()
#7-Inference:Its doesn't affect the score of the top scorers but does give a boost to low scoring people
#,top scoring females score better or at par with males...otherwise males perform better in all lower score ranges


# In[ ]:


#question:does being poor affect scores??
fig = px.scatter_3d(data_student, x='Language', y='test preparation course', z='math score',color='lunch',symbol='race/ethnicity')
fig.show()
#8-Inference:Yes it does ,poor people perform poorly on test..and one interesting thing,a lot of poor people are from group B,a lot smart,rich are from group D


# In[ ]:


fig = px.scatter_3d(data_student, x='math score', y='writing score', z='reading score',color='gender',symbol='gender')
fig.show()
#9-Inference -It seems to me that women dominate and lag behind doing both more than men...more on top and also more on bottom...I could have given more conclusive inferene if I had science score too


# In[ ]:


data_games=pd.read_csv("../input/videogamesales/vgsales.csv")
data_games.head()


# Fields include
# *     Rank - Ranking of overall sales
# *     Name - The games names
# *     Platform - Platform of the games release (i.e. PC,PS4, etc.) 
# *     Year - Year of the game's release
# *     Genre - Genre of the game 
# *     Publisher - Publisher of the game
# *     NA_Sales - Sales in North America (in millions) 
# *     EU_Sales - Sales in Europe (in millions)
# *     JP_Sales - Sales in Japan (in millions)
# *     Other_Sales - Sales in the rest of the world (in millions) 
# *     Global_Sales - Total worldwide sales.

# In[ ]:


data_games.info()
data_games.describe()


# In[ ]:


fig = px.scatter_3d(data_games, x='NA_Sales', y='EU_Sales', z='JP_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#10-Inference:Some games do well in certain part of world and soem do well in other...sales shouldn't be the single factor if a game is successful or not


# In[ ]:


fig = px.scatter(data_games, x='NA_Sales', y='EU_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#11-Inference:There is clear indication EU_Sales are proportional to NA_Sales...but there is huge no of games that do well in only NA_sales


# In[ ]:


fig = px.scatter(data_games, x='NA_Sales', y='JP_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#12-Inference:This shows that there are games that are developed to cater to particular area only


# In[ ]:


fig = px.scatter(data_games, x='Rank', y='JP_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#12-Inference:POkemon BLue is king in japanese market by quite some margin


# In[ ]:


fig = px.scatter(data_games, x='Rank', y='NA_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#13-Inference:WII sports is king in north american market by quite bigger margin than japanese market margin...One more thing,There is more money in american markets


# In[ ]:


fig = px.scatter(data_games, x='Rank', y='EU_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#14-Inference:Domination Dekh re ho.. :)(some hindi slang)


# In[ ]:


fig = px.bar(data_games, x='Year', y='Global_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#15-Inference-So overall video games sales was highest around the year of reccesion..weird why is that??


# In[ ]:


fig = px.scatter(data_games, x='Year', y='Global_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#16-There is some weird pattern in this graph like a increasing sine wave...but there are outliers in this too


# In[ ]:


fig = px.bar(data_games, x='Year', y='Genre',color='Genre',hover_data=['Rank','Genre','Name'])
fig.show()
#17-Inference-Sports got popular in year 2008,I can't make any more inferences form this


# In[ ]:


fig = px.scatter_3d(data_games, x='Year', y='Genre',z='Publisher',color='Global_Sales',size='NA_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#18-Inference Most Big Games have been published by Nintendo


# In[ ]:


fig = px.bar(data_games, x='Publisher', y='Global_Sales',color='Global_Sales',hover_data=['Rank','Genre','Name'])
fig.show()
#19-Video game industry is a monopoly ,Our monopoly king :Nintendo..most publisher are completely  non existent compared to nintendo


# In[ ]:


data_pokemon=pd.read_csv("../input/pokemon/Pokemon.csv")


# In[ ]:


data_pokemon.tail()


# In[ ]:


fig1=px.scatter(data_pokemon,x='Generation',y='Attack',color='Generation',size='HP',hover_data=['Name'])
fig1.show()
#20-Inference:Attack reaches peak in 3 generation then comes down again


# In[ ]:


fig1=px.scatter(data_pokemon,x='Generation',y='Defense',color='Generation',size='HP',hover_data=['Name'])
fig1.show()     
#21-Inference:Defense also seem to reach peak in middle then downgrades


# In[ ]:


fig1=px.scatter(data_pokemon,x='Type 1',y='Total',color='Generation',hover_data=['Name'])
fig1.show()  
#22-inference:water ground pschyic and dragon types are most powerful


# In[ ]:


fig1=px.scatter(data_pokemon,x='Name',y='Total',color='Generation',hover_data=['Name'])
fig1.show()  
#23-Inference-Peaks are at generation 3 then it goes downs


# In[ ]:


fig1=px.scatter(data_pokemon,x='Sp. Atk',y='Sp. Def',color='Total',hover_data=['Name'])
fig1.show()     
#24-Inference:This is graph that makes sense..shows how pokemon grow in their skills and most on right hand are grandmasters with special skills


# In[ ]:


data_avacado=pd.read_csv("../input/avocado-prices/avocado.csv")


# In[ ]:


data_avacado.head()


# In[ ]:


data_avacado.columns


# In[ ]:


fig2=px.bar(data_avacado,x='Date',y='Total Volume',color='region')
fig2.show()
#25:Inference:There seems pattern in here,Atlanta,Washington,HOuston buy a lot of avacados


# In[ ]:


fig2=px.bar(data_avacado,x='year',y='Total Volume',color='region')
fig2.show()
#25:Inference:Demand for avacado decreased in 2018 maybe cause the report from 2018 in this dataset,and there is a healthy upward slop ein the graph


# In[ ]:


fig2=px.scatter(data_avacado,x='Date',y='AveragePrice',color='region')
fig2.show()
#26-Inference Prices arehighest in san francisco,2nd no is Hartford springfield,lowest in phoenix tucson,pretty consistent low in san diego,los angeles too


# In[ ]:


fig2=px.bar(data_avacado,x='Date',y='Total Bags',color='region')
fig2.show()
#27-People are picking up more avacados,as they know it is good food their health


# In[ ]:


fig2=px.bar(data_avacado,x='Date',y='Small Bags',color='region')
fig2.show()


# In[ ]:


fig2=px.bar(data_avacado,x='Date',y='Large Bags',color='region')
fig2.show()


# In[ ]:


#28-Inference-Demand is increasing faster as compared to larger bags but it good that both are growing,Atlanta people are going crazy on avacado after 2016 lol


# In[ ]:


fig2=px.bar(data_avacado,x='Date',y='XLarge Bags',color='region')
fig2.show()
#29-Inference -Seemsthe need of eating and buying is july(onseason)..where people buy a lot of avacados altogether in one time...seems avacados fresh avacados are in market in month of summers


# # So That's about it for today,I will do 40 plots tommorrow
# ## Don't Forget to UPVOTE!!if you like the effort I am putting in...:)
