#!/usr/bin/env python
# coding: utf-8

# # **WHO-"Testing is the only way, we can defeat corona virus".**

# # **The Question is "Are We Testing Enough?"**

# ![](data:image/png;base64,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)

# # The answer to the above question lies in the analysis below.
# 
# 
# 
# 
# # **Please have a look and do UPVOTE for a better reach**.
# 
# 
# 
# 
# # Suggestions are always welcome.

# 
# 

# Dataset source="https://github.com/imdevskp/covid_19_jhu_data_web_scrap_and_cleaning"
# "https://covid19.who.int/?gclid=CjwKCAjwltH3BRB6EiwAhj0IUAmaInk4I487ZyJ_gI488Tqth9yFiBOxbi7V_GX08mM5MKIbwtXCWxoCChMQAvD_BwE"
# "https://www.mygov.in/covid-19/"

# In[ ]:


import pandas as pd
testing=pd.read_csv('../input/covid-testing/covid-testing-all-observations.csv')
testing.columns
testing['Daily change in cumulative total per thousand']=testing['Daily change in cumulative total per thousand'].fillna(testing['Daily change in cumulative total per thousand'].mean())
testing.describe


#  # Assessment of daily testing in  various countries.

# # **Date-Wise testing in USA**

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib as mp
list=[]
tot=[]
test=[]
for x in range(len(testing['ISO code'])):
    if(testing['ISO code'][x]=='USA'):
        list.append(testing['Date'][x])
        test.append(testing['Daily change in cumulative total'][x])
        tot.append(testing['Cumulative total'][x])
for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp1 = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp1
                temp2=test[idx]
                test[idx]=test[idx+1]
                test[idx+1]=temp2

usa=max(tot)
print(usa)
fig, ax = plt.subplots(figsize=(40,12))
ax.bar(list,test)
plt.title("Daily testing in USA")
plt.xticks(rotation=90)
plt.show()


# # Date-Wise testing in Italy.

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib as mp
list=[]
test=[]
tot=[]
for x in range(len(testing['ISO code'])):
    if(testing['ISO code'][x]=='ITA'):
        list.append(testing['Date'][x])
        test.append(testing['Daily change in cumulative total'][x])
        tot.append(testing['Cumulative total'][x])

for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp1 = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp1
                temp2=test[idx]
                test[idx]=test[idx+1]
                test[idx+1]=temp2
italy=max(tot)
print(italy)

fig, ax = plt.subplots(figsize=(25,12))
ax.bar(list,test,color='Red')
plt.title("Daily testing in ITALY")
plt.xticks(rotation=90)
plt.show()


# # Date-Wise testing in Russia.

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib as mp
list=[]
test=[]
tot=[]
for x in range(len(testing['ISO code'])):
    if(testing['ISO code'][x]=='RUS'):
        list.append(testing['Date'][x])
        test.append(testing['Daily change in cumulative total'][x])
        tot.append(testing['Cumulative total'][x])

for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp1 = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp1
                temp2=test[idx]
                test[idx]=test[idx+1]
                test[idx+1]=temp2
russia=max(tot)
print(russia)
fig, ax = plt.subplots(figsize=(25,12))
ax.bar(list,test,color='Green')
plt.title("Daily testing in RUSSIA")
plt.xticks(rotation=90)
plt.show()


# # Date-Wise testing in UK.

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib as mp
list=[]
test=[]
tot=[]
for x in range(len(testing['ISO code'])):
    if(testing['ISO code'][x]=='GBR'):
        list.append(testing['Date'][x])
        test.append(testing['Daily change in cumulative total'][x])
        tot.append(testing['Cumulative total'][x])

for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp1 = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp1
                temp2=test[idx]
                test[idx]=test[idx+1]
                test[idx+1]=temp2
uk=max(tot)
fig, ax = plt.subplots(figsize=(25,12))
ax.bar(list,test,color='Gray')
plt.title("Daily testing in UK")
plt.xticks(rotation=90)
plt.show()


# # Date-Wise testing in Australia.

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib as mp
list=[]
tot=[]
test=[]
for x in range(len(testing['ISO code'])):
    if(testing['ISO code'][x]=='AUS'):
        list.append(testing['Date'][x])
        test.append(testing['Daily change in cumulative total'][x])
        tot.append(testing['Cumulative total'][x])

for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp1 = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp1
                temp2=test[idx]
                test[idx]=test[idx+1]
                test[idx+1]=temp2
aus=max(tot)
fig, ax = plt.subplots(figsize=(25,12))
ax.bar(list,test,color='Yellow')
plt.title("Daily testing in AUSTRALIS")
plt.xticks(rotation=90)
plt.show()


# # Date-Wise testing in INDIA.

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib as mp
list=[]
tot=[]
test=[]
for x in range(len(testing['ISO code'])):
    if(testing['ISO code'][x]=='IND'):
        list.append(testing['Date'][x])
        test.append(testing['Daily change in cumulative total'][x])
        tot.append(testing['Cumulative total'][x])
     
for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp1 = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp1
                temp2=test[idx]
                test[idx]=test[idx+1]
                test[idx+1]=temp2
ind=max(tot)

fig, ax = plt.subplots(figsize=(25,12))
ax.bar(list,test,color='Orange')
plt.title("Daily testing in INDIA")
plt.xticks(rotation=90)
plt.show()


# Note-These all graphs are respected to the population of that given country.So lets do a comparitive study of the population vs the number of covid testing done by a particular country.

# In[ ]:


fig1, ax1 = plt.subplots(figsize=(20,10))
tested=[ind,russia,usa,uk,italy,aus]
names=['INDIA','RUSSIA','USA','UK','ITALY','AUSTRALIA']
ax1.pie([ind,russia,usa,uk,italy,aus], labels=['INDIA','RUSSIA','USA','UK','ITALY','AUSTRALIA'], autopct='%1.1f%%',
        shadow=True, startangle=90,frame=True,colors=["orange","Gray","blue","pink","red","yellow"])
ax1.set_title("COUNTRY WISE ANALYSIS OF COVID TESTING")

ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# ![](https://png.pngtree.com/png-clipart/20200401/original/pngtree-danger-area-covid19-outbreak-vector-illustration-png-image_5335445.jpg)

# # **The overall number of testing as Done by different countries till 23rd-June 2020 is as follows:-**

# In[ ]:


code=[]
for x in testing['Entity']:
    if(code.count(x)>0):
        continue
    code.append(x)
resn=[]
rest=[]
for x in code:
    grouped = testing.groupby(testing.Entity)
    ya = grouped.get_group(x)
    resn.append(x)
    rest.append(max(ya['Cumulative total']))
    print((x+"\t"+(str)(max(ya['Cumulative total']))))

    

    
    
    


# In[ ]:


import plotly.express as px
fig = px.bar(x=resn, y=rest, color=rest, height=400,title="Testing done by various countries")

fig.show()


# # **Lets focus on the countries which are worstly affected by covid-19**

# In[ ]:


tested[2]=27317035.0
tested[4]=3057902.0
tested[3]=2144626.0
tested[0]=525667.0
print("Numebr of people tested"+(str)(tested))
print("Name    of     the country"+(str)(names))
import plotly.express as px
fig = px.bar(x=tested, y=names, color=tested, height=400,title="People tested by various countries")

fig.show()






# # Population Vs Testing

# # **The Population of all world countries as in 2016**

# In[ ]:


population=pd.read_csv('../input/population/population-figures-by-country-csv_csv.csv')
population.columns
popl=[]
nas=[]
for x in range(len(population['Country'])):
    popl.append(population['Country'][x])
    nas.append((population['Year_2016'][x]))
    print(population['Country'][x]+"\t"+(str)(population['Year_2016'][x]))
    


# In[ ]:


cntry=[]
pcnt=[]
for x in range(len(population['Country_Code'])):
    chk=population['Country_Code'][x]
    if(chk=='IND'):
        cntry.append(chk)
        pcnt.append(population['Year_2016'][x])
    if(chk=='USA'):
        cntry.append(chk)
        pcnt.append(population['Year_2016'][x])
    if(chk=='ITA'):
        cntry.append(chk)
        pcnt.append(population['Year_2016'][x])
    if(chk=='RUS'):
        cntry.append(chk)
        pcnt.append(population['Year_2016'][x])
    if(chk=='GBR'):
        cntry.append(chk)
        pcnt.append(population['Year_2016'][x])
    if(chk=='AUS'):
        cntry.append(chk)
        pcnt.append(population['Year_2016'][x])


poplcnt=['INDIA', 'RUSSIA', 'USA', 'UK', 'ITALY', 'AUSTRALIA']
poplnum=[pcnt[2],pcnt[4],pcnt[5],pcnt[1],pcnt[3],pcnt[0]]
print(poplcnt)
print(poplnum)


        
        
   


# In[ ]:


import plotly.express as px
fig = px.bar(x=poplcnt, y=poplnum, color=poplnum, height=400,title="Population of Countires under our research")

fig.show()


# ![Please take safety measures.](data:image/jpeg;base64,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)

# # Population vs People Tested

# In[ ]:


import plotly.graph_objects as go



fig = go.Figure()
fig.add_trace(go.Bar(
    x=poplcnt,
    y=poplnum,
    name='Population Of the country',
    marker_color='yellow'
))
fig.add_trace(go.Bar(
    x=poplcnt,
    y=tested,
    name='Covid-19 People tested',
    marker_color='dark blue'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45,height=1000)
fig.show()


# # % testing done by these countries

# In[ ]:


perc=[]
for x in range(len(poplcnt)):
    perc.append((100*(float)(tested[x])/(float)(poplnum[x])))
print(perc)
print(poplcnt)


# ****

# **Matrix showing  number of persons tested respected to different countries (AREA-WISE PLOT)**

# In[ ]:


import matplotlib.pyplot as plt
import squarify    
 
# If you have 2 lists
squarify.plot(sizes=tested, label=poplcnt, alpha=.7 )
plt.axis('off')
plt.show()


# In[ ]:


fig1, ax1 = plt.subplots(figsize=(20,10))

ax1.pie(perc, labels=poplcnt, autopct='%1.1f%%',
        shadow=True, startangle=90,frame=True,colors=["orange","Gray","blue","pink","red","yellow"])
print("% of population tested is as follows")

ax1.axis('equal')

plt.show()


# # ***Are We Really Safe***
# 
# 

# ![CORONA THREAT](data:image/jpeg;base64,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)

# In[ ]:


import plotly.graph_objects as go


fig = go.Figure(data=[
    go.Bar(name='Tested', x=poplcnt, y=tested,marker_color='rgb(255,69,0)'),
    go.Bar(name='Total Population', x=poplcnt, y=poplnum,marker_color='rgb(255,255,0)')])

# Change the bar mode

fig.update_layout(barmode='stack',title="Relative Study OF Population vs Testing")
fig.show()


# *According to the testing details available by the countries are not testing in the apt amount and the people are in a very grave situation and the world is suffering a lot.*

# **Now lets see the comparitive study between the number of people tested vs the number of confirmed cases in these countires**

# In[ ]:


import pandas as pd
final=pd.read_csv('../input/complete-corona-details/covid_19_clean_complete.csv')
final.columns


# In[ ]:


conf=[]
conff=[]
['INDIA', 'RUSSIA', 'USA', 'UK', 'ITALY', 'AUSTRALIA']
for x in range(len(final['Country/Region'])):
    if(final['Country/Region'][x]=='India'):
        conf.append(final['Confirmed'][x])
conff.append(max(conf))
conf=[]
for x in range(len(final['Country/Region'])):
    if(final['Country/Region'][x]=='Russia'):
        conf.append(final['Confirmed'][x])
conff.append(max(conf))
conf=[]

for x in range(len(final['Country/Region'])):
    if(final['Country/Region'][x]=='US' ):
        conf.append(final['Confirmed'][x])
conff.append(max(conf))
conf=[]
for x in range(len(final['Country/Region'])):
    if(final['Country/Region'][x]=='United Kingdom' ):
        conf.append(final['Confirmed'][x])
conff.append(max(conf))
conf=[]
for x in range(len(final['Country/Region'])):
    if(final['Country/Region'][x]=='Italy' ):
        conf.append(final['Confirmed'][x])
conff.append(max(conf))
conf=[]
for x in range(len(final['Country/Region'])):
    if(final['Country/Region'][x]=='Australia' ):
        conf.append(final['Confirmed'][x])
conff.append(max(conf))
print("Covid 19 positive cases as on 23rdJune")
print(conff)
print(poplcnt)
        


# In[ ]:


import plotly.graph_objects as go


fig = go.Figure(data=[
    go.Bar(name='CONFIRMED CASES', x=poplcnt, y=conff,marker_color='rgb(255,0,0)'),
    go.Bar(name='TOTAL  TESTS DONE TILL 23rd JUNE', x=poplcnt, y=tested,marker_color='rgb(0,255,0)')])

# Change the bar mode

fig.update_layout(barmode='stack',title="Relative Study OF Testing vs Confirmation",height=1000)
fig.show()


# # Final Analysis of total active,recovered and deceased cases.

# In[ ]:


ar=['India','Russia','Australia','Italy','US','United Kingdom']
for j in ar:
    if(j=='United Kingdom'):
        break
    for i in range(len(final['Country/Region'])):
        if(final['Country/Region'][i]==j):
            deat=final['Deaths'][i]
            recov=final['Recovered'][i]
            act=final['Active'][i]

    my_circle=plt.Circle( (0,0), 0.7, color='pink')
    size=[deat,act,recov]
    fig = plt.figure()
    fig.patch.set_facecolor('pink')
    names=["Deaths","Active","Recovered"]
    plt.pie(size,  colors=['black','red','green'],radius=1,startangle=200)
    p=plt.gcf()
    patches, texts = plt.pie(size, colors=['black','red','green'], shadow=True, startangle=90)
    plt.legend(patches, labels=names, loc="best")
    p.gca().add_artist(my_circle)
    plt.axis('equal')
    plt.tight_layout()
    plt.title("NUMBER OF COVID-19 PATIENTS IN "+(str)(j)+" AS ON 23rd JUNE 2020")
    plt.show


# # *ANS-* *I suppose we found the answer to the question after such a detailed analysis that we are'nt testing in the apt amount and that has made the virus an invincible havoc.Its a request to the government of all nations to increase the daily testing cause its the only way we can defeat the virus until a particular drug is developed.*
# 
# # Now being a data-analyst I request you all to please STAY HOME & STAY SAFE and appreciate my work by giving an upvote-
# 
# 
# 
# 
# 
# 
# # A developers attempt to save the world..... 
