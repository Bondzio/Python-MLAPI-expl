#!/usr/bin/env python
# coding: utf-8

# # Exercise 6 - Corona Virus Case in Brazil

# To simply put, a podcast by BBC [(broadcasted through BBC Global News Podcast on Friday, June 5th 2020)](https://www.bbc.co.uk/sounds/play/p08g3rft) mentioned that Brazil was affected badly by COVID-19. Confirmed cases have reached [more than 710,000 cases](https://www.worldometers.info/coronavirus/country/brazil/) last week and it is  likely to suffer from increase due to poor governance, denying that the country needs to address a more stringent strategy asap.
# Therefore, this intrigued me to look further of how badly Brazil was hit by the pandemic, has the number increased all day or has it reached the peak. 
# Also, as a country which is resided by one of biggest indigenous group of Amazon, this community has been majorly impacted due to their lack of education, tools and access to neither a sufficient health care system nor to a prevention measures (like mask, alcohol, disinfectant to name a few). If possible, this will be looked out further.
# While it is obvious that Brazilian's President has been handling this case poorly, as reported by many that he actually ordered for a change in [reporting into only cases and deaths in the last 24 hours instead of accumulating it](https://www.bbc.com/news/world-latin-america-52952686), which is unclear of why), I think it is interesting to discuss and to clarify the steps/measures the government has taken amidst this hard time.

# ### 6.1 Daily confirmed cases, casualties and recoveries

# a) Shown below is accumulated data until Sunday, June 7th 2020.

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
np.set_printoptions(threshold=np.inf)

selected_country='Brazil'
df = pd.read_csv("../input/novel-corona-virus-2019-dataset/covid_19_data.csv",header=0)
df = df[df['Country/Region']==selected_country]
df = (df.groupby('ObservationDate').sum())

print(df)


# b) Shown below is day to day confirmed cases, deaths and recovered (increase and decrease).
# By using diff function to calculate the daily gap.
# By adding a new column called daily_xxx by extracting from existing columns containing datas of Confirmed, Deaths and Recovered in Brazil.

# In[ ]:


df['daily_confirmed'] = df['Confirmed'].diff()
df['daily_deaths'] = df['Deaths'].diff()
df['daily_recovered'] = df['Recovered'].diff()
print(df)


# c) To show a graphic using above data

# In[ ]:


df['daily_confirmed'].plot(color='blue')
df['daily_recovered'].plot(color='yellow')
df['daily_deaths'].plot(color='red')
plt.show()


# d) making it interactive by adding 2 modules: plotly.offline and plotly.graph_objs

# In[ ]:


from plotly.offline import iplot
import plotly.graph_objs as go

daily_confirmed_object = go.Scatter(x=df.index,y=df['daily_confirmed'].values,name='Daily Confirmed')
daily_deaths_object = go.Scatter(x=df.index,y=df['daily_deaths'].values,name='Daily Deaths')
daily_recovered_object = go.Scatter(x=df.index,y=df['daily_recovered'].values,name='Daily Recovered')

layout_object = go.Layout(title='Brazil Daily Case 19M58558',xaxis=dict(title='Date'),yaxis=dict(title='Number of people'))
fig = go.Figure(data=[daily_confirmed_object,daily_deaths_object,daily_recovered_object],layout=layout_object)
iplot(fig)
fig.write_html('Brazil_Daily_Case_19M58558.html')


# e) as an interractive table

# In[ ]:


df1 = df#['daily_confirmed']
df1 = df1.fillna(0.)
styled_object = df1.style.background_gradient(cmap='Pastel1').highlight_max('daily_confirmed').set_caption('Daily_Summaries')
display(styled_object)
f = open('Table_19M58558.html','w')
f.write(styled_object.render())


# ### 6.2 Global Ranking

# In[ ]:


df = pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/covid_19_data.csv')
df.index=df['ObservationDate']
df = df.drop(['SNo','ObservationDate'],axis=1)
df_Brazil = df[df['Country/Region']=='Brazil']

latest = df[df.index=='06/16/2020']
latest = latest.groupby('Country/Region').sum()
latest = latest.sort_values(by='Confirmed',ascending=False).reset_index()

print('Brazil Rank: ', latest[latest['Country/Region']=='Brazil'].index.values[0]+1)


# ### 6.3 Discussion

# Only behind USA in number of confirmed case of Novel Corona Virus, Brazil suffered a great deal from the pandemic. Firstly, as shown in Interactive Graph that in March 4th two patients were confirmed to be infected by the virus. From there, the number has been growing significantly until it reached its peak in May 30th, where 33,274 people were infected in one day (in total 498,440 confirmed cases). It decreased half the usual number on the start of June (over 11,500 newly infected persons) but the number spiked again daily new confirmed cases have never been lower than 12 thousands (the lowest happening again in 8th June, confirming at least 15 thousands case). Lastest recorded date, on June 16th, shows spike in last two days confirmed cases spiked quite significantly to 20,647 cases (on 15th) then to 34,918 (on 16th). Following high number of day to day confirmed case, daily deaths have been increasing as well, with 1,473 dead casualties as top numbers (on 4th). The latest record implicited that the fluctuating growth actually never staled below 500 since June began. 
# 
# Since 8th, amount of recovered patients has been fluctuating. Notable decrease happened on 14th when it dropped to 9,705 from 14,313 the preceeding day. While the death line graph seems to be following its own distinguished path compared to daily confirmed and daily recovered, I think it is curious that daily recovered and daily confirmed seem to be reflecting each other fluctuating movement, aside of some notable spikes in recovered data (April 15th and 19th, then June 8th).
# 
# Several notable fluctuations happened in June 8, aside of second lowest number of newly confirmed number. The recovered numbers hit the rooftop (reaching 94,305 cases) at this day, a stark difference compared to older cases, following the [order to change way of reporting confirmed cases and erasing the accumulative data from official website by President Bolsonaro](https://www.theguardian.com/world/2020/jun/07/brazil-stops-releasing-covid-19-death-toll-and-wipes-data-from-official-site) reasoning that 'cummulative data might be misleading and inaccurate'. Fortunately, the reporting has been returned into its original way due to public uproar followed by [court ruling](https://www.bbc.com/news/world-latin-america-52980642). Either way, corona virus patients are still increasing and there is a chance that current number of 730,000 cases is lower than real number considering the amount of test they do.
# 
# As reported by NYTimes (updated in June 10th), southern Brazil is affected the most including Sao Paolo, Rio de Janeiro and Espirito Santo (over 156,300, 74,300 and 23,300 confirmed cases respectively). Their high reliance in public transportation, high population density and low economic and social resiliency are among some factors causing high risk of spreading. [Amazonas is also among regions wherein cases confirmed the most](https://www.nytimes.com/interactive/2020/world/americas/brazil-coronavirus-cases.html), about 52,800 cases. It was reported that out of 256 existing indigenous groups in Amazon, 75 or more have been affected. This community may have [higher risk than common residents](https://brazilian.report/coronavirus-brazil-live-blog/2020/04/23/over-80000-indigenous-people-critically-vulnerable-due-to-covid-19/) due to low body immune, because of their lack of contact with modern sickness.
# 
# The most concerning thing about this situation is that Brazil has never regulated a lockdown despite the huge number of confirmed cases. This decision is affected by [several factors](https://brazilian.report/coronavirus-brazil-live-blog/2020/06/10/covid-19-seven-brazilian-states-likely-to-need-lockdown/) including country's suffering economy (over 960,000 new unemployment reported cases in May triggered by COVID-19), lack of support toward lockdown idea, as well as insufficient law enforcement that may support the implementation of lockdown. Despite high risk and actual number of confirmed cases, combined with no comprehensive strategy to prevent more cases, [major cities including Sao Paolo and Rio de Janeiro are to reopen this month.](https://brazilian.report/newsletters/brazil-daily/2020/06/10/sao-paulo-rio-reopen-supreme-court-fake-news-petrobras-oil/) This is expected as a response to Brazilian President ordering to reopen economy and business activities and accuse toward local leaders to have taken advantage of this situation for political gain. It is unfortunate considering that back in May it was reported that [hospitals in Sao Paolo were in near-collapse](https://www.bbc.com/news/world-latin-america-52701524) situation due to overwhelming increase in patients.
# 
# On the other hand, following high level of daily deaths by COVID-19 in Brazil, [the country has been participating in vaccine testing](https://www.forbes.com/sites/kenrapoza/2020/06/04/brazil-to-be-first-to-test-oxfords-covid-19-vaccine/#6a1c4a543212), developed by Oxford University. There is a high chance that Brazil is one of first countries that will be benefitted once the cure is found.
