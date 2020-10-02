#!/usr/bin/env python
# coding: utf-8

# # ***COVID-19: Understanding the Growth Factor involved in the exponential growth of the Corona Virus & Inflection Point in the Curve of Growth***

# ![](https://miro.medium.com/max/4800/0*2Hb-dGkPAZU_vUtW)
# 
# Photo by Viktor Forgacs on Unsplash
# 
# ### With everything that is occurring about the Coronavirus, it may be exceptionally difficult to settle on a choice of what to do today. Would it be a good idea for you to wait for more data? Accomplish something today? What?
# 
# #### -How many cases of coronavirus will there be in your area?
# #### -What are the actual figures? Is everyone testing on time?
# #### -What should you do to prevent the spreading?
# #### -When is everything going to slow down?
# 
# ### The only way to prevent this is restricting the growth factor associated with the exponential rise in the number of cases. But what does this growth factor comprise of? 

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from scipy.integrate import odeint
import plotly.express as px
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode(connected=True)
import folium
from scipy.integrate import odeint
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


df1 = pd.read_csv('../input/novel-corona-virus-2019-dataset/COVID19_line_list_data.csv')
df1.head(2)


# In[ ]:


df1 = df1[df1.columns[:-8]]
df1.drop('Unnamed: 3', axis=1, inplace=True)


# In[ ]:


df1.head(2)


# In[ ]:


df1['reporting date'] = pd.to_datetime(df1['reporting date'])
df1['exposure_start'] = pd.to_datetime(df1['exposure_start'])
df1['exposure_end'] = pd.to_datetime(df1['exposure_end'])
df1['hosp_visit_date'] = pd.to_datetime(df1['hosp_visit_date'])
df1['symptom_onset'] = pd.to_datetime(df1['symptom_onset'])


# In[ ]:


df2 = pd.read_csv('../input/novel-corona-virus-2019-dataset/COVID19_open_line_list.csv')
df2 = df2[df2.columns[:-12]]
df2.loc[df2['sex']=='male', 'sex'] = 'Male'
df2.loc[df2['sex']=='female', 'sex'] = 'Female'
df2.head(2)


# In[ ]:


df3 = pd.read_csv("../input/corona-virus-report/covid_19_clean_complete.csv")
df3.head()


# ### **Total countries and locations affected**

# In[ ]:


df_loc = pd.DataFrame(df1.groupby(['country'])['location'].nunique()).reset_index().sort_values(by='location', ascending=False).reset_index(drop=True)
df_loc.loc[df_loc.shape[0]]=['Total: '+str(df_loc['country'].nunique()), 'Total: '+str(df_loc['location'].sum())]
df_loc


# In[ ]:


df1.head(2)


# In[ ]:


df1['sym_exp_diff'] = (df1['symptom_onset'] - df1['exposure_end']).dt.days
df1['hosp_sym_diff'] = (df1['hosp_visit_date'] - df1['symptom_onset']).dt.days


# In[ ]:


fig = px.pie(df1, values=[df1['gender'].value_counts()[0], df1['gender'].value_counts()[1]], names=['Male', 'Female'], title='Male v Female Affected Ratio')
fig.show()


# In[ ]:


fig = px.violin(df2[df2['sex']!='4000'].dropna(subset=['age', 'sex']), y="age", x='sex', color="sex",
                hover_data=df2.columns, title='Age Ratio of people affected b/w the two genders')
fig.show()


# - Comparing both of them seems like the age of the affected females are higher than that of males

# ##### Plotting the locations on the map

# In[ ]:


# Credits: https://www.kaggle.com/imdevskp/covid-19-analysis-visualization-comparisons, Devakumar Kp

m = folium.Map(location=[0, 0], tiles='cartodbpositron',
               min_zoom=1, max_zoom=4, zoom_start=1)

df3_mapping = df3.loc[:20000].dropna(subset=['Confirmed']).reset_index(drop=True)

for i in range(0, len(df3_mapping)):
    folium.Circle(
        location=[df3_mapping.iloc[i]['Lat'], df3_mapping.iloc[i]['Long']],
        color='crimson', 
        tooltip =   '<li><bold>Country : '+str(df3_mapping.iloc[i]['Country/Region'])+
                    '<li><bold>Province : '+str(df3_mapping.iloc[i]['Province/State'])+
                    '<li><bold>Confirmed : '+str(df3_mapping.iloc[i]['Confirmed'])+
                    '<li><bold>Deaths : '+str(df3_mapping.iloc[i]['Deaths'])+
                    '<li><bold>Recovered : '+str(df3_mapping.iloc[i]['Recovered']),
        radius=int(df3_mapping.iloc[i]['Confirmed'])**1.1).add_to(m)
m


# In[ ]:


ncov_df = pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv')

ncov_df['ObservationDate'] = pd.to_datetime(ncov_df['ObservationDate']) 

ncov_df["Country"] = ncov_df["Country/Region"].replace(
    {
        "Mainland China": "China",
        "Hong Kong SAR": "Hong Kong",
        "Taipei and environs": "Taiwan",
        "Iran (Islamic Republic of)": "Iran",
        "Republic of Korea": "South Korea",
        "Republic of Ireland": "Ireland",
        "Macao SAR": "Macau",
        "Russian Federation": "Russia",
        "Republic of Moldova": "Moldova",
        "Taiwan*": "Taiwan",
        "Cruise Ship": "Others",
        "United Kingdom": "UK",
        "Viet Nam": "Vietnam",
        "Czechia": "Czech Republic",
        "St. Martin": "Saint Martin",
        "Cote d'Ivoire": "Ivory Coast",
        "('St. Martin',)": "Saint Martin",
        "Congo (Kinshasa)": "Congo",
    }
)
ncov_df["Province"] = ncov_df["Province/State"].fillna("-").replace(
    {
        "Cruise Ship": "Diamond Princess cruise ship",
        "Diamond Princess": "Diamond Princess cruise ship"
    }
)


# In[ ]:


ncov_df.head()


# In[ ]:


ncov_china = ncov_df[ncov_df['Country'] == 'China']
ncov_china = pd.DataFrame(ncov_china.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=ncov_china['ObservationDate'], y=ncov_china['Confirmed'], name='Confirmed Cases'))
fig1.add_trace(go.Scatter(x=ncov_china[21:23]['ObservationDate'], y=ncov_china[21:23]['Confirmed'], mode='markers', name='Inflection', marker=dict(color='Red',line=dict(width=5, color='Red'))))
fig1.layout.update(title_text='COVID-19 Growth in China & Inflection',xaxis_showgrid=False, yaxis_showgrid=False, width=800,
        height=500,font=dict(
#         family="Courier New, monospace",
        size=12,
        color="white"
    ))
fig1.layout.plot_bgcolor = 'Black'
fig1.layout.paper_bgcolor = 'Black'
fig1.show()


# ### From the above graph I believe that the inflection point is somewhere in the region between the two red points. We see that the exponential curve stops going upwards from around 1st March. The growth factor for the next few days seems to be a constant ~1
# 
# ### But in the first place why did the curve go up so fast? What led to the growth so fast?
# 

# ![](https://miro.medium.com/max/3584/1*r-ddYhoUtP_se6x-NOEinA.png)
# 
# Source: Tomas Pueyo analysis over chart from the Journal of the American Medical Association, based on raw case data from the Chinese Center for Disease Control and Prevention

# ### In the above graph we see that the grey bars refer to the true no. of people and the yellow bars correspond to the people who got tested. Which means the ones who did not get tested were getting exposure with a lot of people outside.

# In[ ]:


fig = px.box(df1.dropna(subset=['sym_exp_diff']), y="sym_exp_diff", points='all', title='Days difference between symptom and exposure dates') # typically after how many days after the exposure do the symptoms come up
# fig.layout.plot_bgcolor = '#6A7806'
# fig.layout.paper_bgcolor = '#6A7806'
fig.show()


# ### - We see that for more the majority of the people the symptoms came up >=0 days after their last exposure date.
# 
# ### But when the symptoms showed up what did they do? Did they visit the hospital on time?

# In[ ]:


fig = px.box(df1.dropna(subset=['hosp_sym_diff']).reset_index(drop=True), y="hosp_sym_diff", points='all',              title='Days difference between hospital visit and symptom dates') # typically after how many days after the exposure do the symptoms come up
fig.show()


# ### - We see that there are so many people who go to the hospital after a few days from their symptom day. Can this delay cause more exposure and hence spread it out to more people?

# # ***First set of Hypothesis around the Growth Factor:***
# ### ***i) It majorly comprises public-exposure***
# ### ***ii) Secondly to some extent, it also comprises the delay by a person in getting tested from the symptom date***
# ### ***iii) Through unnoticed items like your smartphones, etc. Smartphone can be an extremely vulnerable item***
# 
# #### The second hypothesis has to be highly correlated with the first one

# > ### **Diving into some more EDA**
# 
# #### Lets check the top 10 countries with maximum cases and respective deaths and recoveries

# In[ ]:


ncov_italy = ncov_df[ncov_df['Country'] == 'Italy']
ncov_us = ncov_df[ncov_df['Country'] == 'US']
ncov_spain = ncov_df[ncov_df['Country'] == 'Spain']
ncov_germany = ncov_df[ncov_df['Country'] == 'Germany']
ncov_iran = ncov_df[ncov_df['Country'] == 'Iran']
ncov_france = ncov_df[ncov_df['Country'] == 'France']
ncov_uk = ncov_df[ncov_df['Country'] == 'UK']
ncov_swiss = ncov_df[ncov_df['Country'] == 'Switzerland']
ncov_soukor = ncov_df[ncov_df['Country'] == 'South Korea']

ncov_italy = pd.DataFrame(ncov_italy.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
ncov_us = pd.DataFrame(ncov_us.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
ncov_spain = pd.DataFrame(ncov_spain.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
ncov_germany = pd.DataFrame(ncov_germany.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
ncov_iran = pd.DataFrame(ncov_iran.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
ncov_france = pd.DataFrame(ncov_france.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
ncov_uk = pd.DataFrame(ncov_uk.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
ncov_swiss = pd.DataFrame(ncov_swiss.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()
ncov_soukor = pd.DataFrame(ncov_soukor.groupby(['ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index()


# In[ ]:


ncov_all = pd.DataFrame(ncov_df.groupby(['Country', 'ObservationDate'])['Confirmed', 'Deaths', 'Recovered'].sum()).reset_index().drop_duplicates(subset=['Country'], keep='last')
ncov_all.reset_index(drop=True, inplace=True)
ncov_all = ncov_all.sort_values(by=['Confirmed'], ascending=False).reset_index(drop=True)
ncov_all = ncov_all.head(10)


# In[ ]:


fig = go.Figure(data=[
    go.Bar(name='Confirmed',x=ncov_all['Country'].unique(), y=ncov_all['Confirmed']),
    go.Bar(name='Deaths', x=ncov_all['Country'].unique(), y=ncov_all['Deaths']),
    go.Bar(name='Recovered', x=ncov_all['Country'].unique(), y=ncov_all['Recovered'])
])
# Change the bar mode
fig.layout.update(barmode='stack', title='Top 10 Country-wise Corona Cases & Consequences', yaxis_showgrid=False)
fig.show()


# ### How Corona Virus fared in Rest of the World

# In[ ]:


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=ncov_italy['ObservationDate'], y=ncov_italy['Confirmed'], name='Italy'))
fig1.add_trace(go.Scatter(x=ncov_us['ObservationDate'], y=ncov_us['Confirmed'], name='USA'))
fig1.add_trace(go.Scatter(x=ncov_spain['ObservationDate'], y=ncov_spain['Confirmed'], name='Spain'))
fig1.add_trace(go.Scatter(x=ncov_uk['ObservationDate'], y=ncov_uk['Confirmed'], name='UK'))
fig1.add_trace(go.Scatter(x=ncov_germany['ObservationDate'], y=ncov_germany['Confirmed'], name='Germany'))
fig1.add_trace(go.Scatter(x=ncov_iran['ObservationDate'], y=ncov_iran['Confirmed'], name='Iran'))
fig1.add_trace(go.Scatter(x=ncov_france['ObservationDate'], y=ncov_france['Confirmed'], name='France'))

fig1.layout.update(title_text='COVID-19 Growth in Rest of the World',xaxis_showgrid=False, yaxis_showgrid=False, width=800,
        height=500,font=dict(
        size=12,
        color="white"
    ))
fig1.layout.plot_bgcolor = 'Black'
fig1.layout.paper_bgcolor = 'Black'
fig1.show()


# #### - We see that none of the countries have approached the inflection point yet

# In[ ]:


ncov_all['CD_Ratio'] = ncov_all['Deaths']/ncov_all['Confirmed']
ncov_all['CR_Ratio'] = ncov_all['Recovered']/ncov_all['Confirmed']
ncov_all = ncov_all.round(2)
ncov_all.head()


# ### Comparing the Death:Confirmed & Recovered:Confirmed Ratios

# In[ ]:


ncov_all_cdr = ncov_all.sort_values(by=['CD_Ratio'], ascending=False).reset_index(drop=True)
ncov_all_crr = ncov_all.sort_values(by=['CR_Ratio'], ascending=False).reset_index(drop=True)
fig = px.bar(ncov_all_cdr, x="Country", y="CD_Ratio", color='CD_Ratio', title='Country-wise Death:Confirmed Cases Ratio')
fig.show()


# - 1 out of 10 person dies in Italy which is too high

# In[ ]:


fig = px.bar(ncov_all_crr, x="Country", y="CR_Ratio", color='CR_Ratio', title='Country-wise Recovered:Confirmed Cases Ratio')
fig.show()


# ### Interesting Facts here:
# #### i) What did China do that there recovery rate is so high?
# #### ii) Need to understand why the deaths:confirmed ratio are so high in Iran, Italy, Spain and UK

# In[ ]:


df2_china = df2[df2['country']=='China'].dropna(subset=['age']).reset_index(drop=True)
df2_italy = df2[df2['country']=='Italy'].dropna(subset=['age']).reset_index(drop=True)
df2_china.head(2)


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Box(y=df2_china['age'], name='China'))
fig.add_trace(go.Box(y=df2_italy['age'], name='Italy'))
fig.update_layout(title='Age Comparison between Chinese and Italians')

fig.show()


# In[ ]:


def clean(x):
    if x == 'death' or x == 'died' or x == 'Death':
        return 'death'
    elif x == 'discharged' or x=='discharge':
        return 'discharge'
    elif x == 'recovered' or x=='stable':
        return 'recovered'
    else:
        return np.nan
    
def apply_int(x):
    try:
        y = int(x)
        return y
    except:
        return np.nan

    
df1_chinese = pd.DataFrame(df2_china[df2_china['outcome'].apply(clean)=='death']['age'].apply(apply_int)).assign(outcome='death')
df2_chinese = pd.DataFrame(df2_china[df2_china['outcome'].apply(clean)=='discharge']['age'].apply(apply_int)).assign(outcome='discharge')
df3_chinese = pd.DataFrame(df2_china[df2_china['outcome'].apply(clean)=='recovered']['age'].apply(apply_int)).assign(outcome='recovered')

fig = go.Figure()
fig.add_trace(go.Box(y=df1_chinese['age'], name="Deceased Patients"))
fig.add_trace(go.Box(y=df2_chinese['age'], name="Discharged Patients"))
fig.add_trace(go.Box(y=df3_chinese['age'], name="Recovered Patients"))
fig.update_layout(title_text='Chinese COVID-19 Patients Outcome Age-Wise')
fig.show()


# ## Lets analyse a bit of India's situation right now

# In[ ]:


df_india= pd.read_csv('../input/coronavirus-cases-in-india/Covid cases in India.csv')
dbd_tc_india = pd.read_excel('../input/covid19-india-complete-data/COVID19 India Complete Dataset May 2020.xlsx', sheet_name='Daily Cases Time-Series')


# In[ ]:


dbd_tc_india.head(2)


# In[ ]:


db_india = pd.DataFrame(dbd_tc_india.groupby(['Date'])['Total Confirmed'].sum()).reset_index()

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=db_india['Date'], y=db_india['Total Confirmed']))
fig1.layout.update(title_text='COVID-19 Growth in India',xaxis_showgrid=False, yaxis_showgrid=False, width=800,
        height=500,font=dict(
#         family="Courier New, monospace",
        size=12,
        color="white"
    ))
fig1.layout.plot_bgcolor = 'Black'
fig1.layout.paper_bgcolor = 'Black'
fig1.show()


# ### Compared to the Western countries (Europe & USA) although we see that although the curve is in the trend of going up exponentially, however the no. of cases have not increased drastically. Because for those countries we see that the no. of cases has increased exponentially in the multiples of 1000 over a span of 2-3 weeks, where as in India its still below 1000
# 
# ### Following are the possible reasons:
# 
# #### - **No. of testings done are less as compared to other countries, but even after that the no. of cases being a random multiple of 1000s like 50k or 60k is quite absurd**
# #### - **Community transmission never got triggered in India maybe because of climatic conditions or some other factors that we might be missing out on?**
# #### - **No community transmission happening yet**
# #### - **People here are more immunized?**

# ### State-Wise No. of cases in India

# In[ ]:


db_state_india = pd.read_excel('../input/covid19-india-complete-data/COVID19 India Complete Dataset May 2020.xlsx', sheet_name='State-Wise Data')
db_state_india = db_state_india[db_state_india['State']!='Total']
db_state_india.head(2)


# In[ ]:


fig = px.bar(db_state_india.sort_values('Confirmed', ascending=False).sort_values('Confirmed', ascending=True),
             x="Confirmed", y="State", 
             title='Total Confirmed Cases', 
             text='Confirmed', 
             orientation='h', 
             width=800, height=800, range_x = [0, max(db_state_india['Confirmed'])])
fig.update_traces(marker_color='#670404', opacity=0.8, textposition='inside')

fig.update_layout(plot_bgcolor='#CDCCA7')
fig.show()


# In[ ]:


dbd_testing_india = pd.read_excel('../input/covid19-india-complete-data/COVID19 India Complete Dataset May 2020.xlsx', sheet_name='ICMR Testing Count')
dbd_testing_india['Update Time Stamp'] = pd.to_datetime(dbd_testing_india['Update Time Stamp'], format='%d/%m/%Y %I:%M: %p')
dbd_testing_india.head(2)


# In[ ]:


df_hos_bed = dbd_testing_india.rename(columns={'Update Time Stamp':'DateTime', 'Total Individuals Tested':'TotalIndividualsTested', 'Total Positive Cases':                                              'TotalPositiveCases'}).copy()
df_hos_bed['DateTime'] = df_hos_bed['DateTime'].dt.date
df_hos_bed.head()


# In[ ]:


df_hos_bed['totalnegative'] = df_hos_bed['TotalIndividualsTested'] - df_hos_bed['TotalPositiveCases']


# In[ ]:


df_hos_bed_per_day = df_hos_bed.drop_duplicates(subset=['DateTime'], keep='last')
df_hos_bed_per_day['test_results_posratio'] = round(df_hos_bed_per_day['TotalPositiveCases']/df_hos_bed_per_day['TotalIndividualsTested'], 3)
df_hos_bed_per_day.head()


# In[ ]:


df_indi = pd.read_excel('../input/covid19-india-complete-data/COVID19 India Complete Dataset May 2020.xlsx', sheet_name='Raw Data')
df_indi.rename(columns={'Patient Number':'id','Current Status':'current_status', 'Age Bracket':'age', 'Notes':'notes'}, inplace=True)
df_indi.head(2)


# In[ ]:


df_indi.dropna(subset=['current_status', 'age'], inplace=True)
df_indi.reset_index(drop=True, inplace=True)


# In[ ]:


df_indi['current_status'].unique(), df_indi.shape


# In[ ]:


df1_indians = df_indi[df_indi['current_status'] == 'Deceased']
df2_indians = df_indi[df_indi['current_status'] == 'Hospitalized']
df3_indians = df_indi[df_indi['current_status'] == 'Recovered']

fig = go.Figure()
fig.add_trace(go.Box(y=df1_indians['age'], name="Deceased Patients"))
fig.add_trace(go.Box(y=df2_indians['age'], name="Hospitalized Patients"))
fig.add_trace(go.Box(y=df3_indians['age'], name="Recovered Patients"))
fig.update_layout(title_text='Indian COVID-19 Patients Outcome Age-Wise')
fig.show()


# ### - We see that outcome trends are similar to China w.r.t. Age

# In[ ]:


pep_no_trav_his = df_indi[df_indi['notes'].str.contains('Travel') == False]
pep_with_trav_his = df_indi[df_indi['notes'].str.contains('Travel') == True]


# In[ ]:


df_indi['id'].nunique(), pep_no_trav_his['id'].nunique()


# In[ ]:


colors = ['#B5B200', '#1300B5']
negative = round(pep_no_trav_his['id'].nunique()/df_indi['id'].nunique()*100, 2)
positive = round(pep_with_trav_his['id'].nunique()/df_indi['id'].nunique()*100, 2)
                         
fig = px.pie(pep_no_trav_his, values=[negative, positive], names=['Patients w/o Travel History', 'Patients with Travel History'],              title='Patients with and without Travel History')
fig.show()


# ### What might be the reasons that patients without travel history got infected?

# In[ ]:


from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)

def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color='black',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
).generate(str(data))

    fig = plt.figure(1, figsize=(15, 15))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

show_wordcloud(pep_no_trav_his['notes'].apply(lambda x: x.replace('travel', '')))


# ### - **From the notes it seems the other patients without any travel history, who have been affected are mainly the closed ones of the patients with travel history and few other exceptions**

# ### COVID19 Test Results comparison between India & Rest of the World

# ### COVID19 Test Results in Rest of the World

# In[ ]:


df_w_testing = pd.read_csv('../input/covid19-testing-rate-all-countries/full-list-total-tests-for-covid-19.csv')
df_w_testing.head(2)


# In[ ]:


df_w_testing = df_w_testing[(df_w_testing['Entity']=='Italy') | (df_w_testing['Entity']=='France') |                             (df_w_testing['Entity']=='Germany') | (df_w_testing['Entity']=='United Kingdom') |                             (df_w_testing['Entity']=='United States') | (df_w_testing['Entity']=='Spain') |                             ((df_w_testing['Entity']=='India'))]
df_w_testing['Date'] = pd.to_datetime(df_w_testing['Date'])
df_w_testing.reset_index(drop=True, inplace=True)


# In[ ]:


df_fra = df_w_testing[df_w_testing['Entity'] == 'France']
df_ita = df_w_testing[df_w_testing['Entity'] == 'Italy']
df_spa = df_w_testing[df_w_testing['Entity'] == 'Spain']
df_uk = df_w_testing[df_w_testing['Entity'] == 'United Kingdom']
df_us = df_w_testing[df_w_testing['Entity'] == 'United States']
df_ger = df_w_testing[df_w_testing['Entity'] == 'Germany']


# In[ ]:


df_fra_rate = pd.merge(df_fra[['Date', 'Total tests']], ncov_france[['ObservationDate', 'Confirmed']], left_on=['Date'],          right_on=['ObservationDate'], how='left')
df_ita_rate = pd.merge(df_ita[['Date', 'Total tests']], ncov_italy[['ObservationDate', 'Confirmed']], left_on=['Date'],          right_on=['ObservationDate'], how='left')
df_ger_rate = pd.merge(df_ger[['Date', 'Total tests']], ncov_germany[['ObservationDate', 'Confirmed']], left_on=['Date'],          right_on=['ObservationDate'], how='left')
df_us_rate = pd.merge(df_us[['Date', 'Total tests']], ncov_us[['ObservationDate', 'Confirmed']], left_on=['Date'],          right_on=['ObservationDate'], how='left')
df_uk_rate = pd.merge(df_uk[['Date', 'Total tests']], ncov_uk[['ObservationDate', 'Confirmed']], left_on=['Date'],          right_on=['ObservationDate'], how='left')
df_spa_rate = pd.merge(df_spa[['Date', 'Total tests']], ncov_spain[['ObservationDate', 'Confirmed']], left_on=['Date'],          right_on=['ObservationDate'], how='left')


# In[ ]:


df_fra_rate['positive_percentage'] = round(df_fra_rate['Confirmed']/df_fra_rate['Total tests'], 2)
df_ita_rate['positive_percentage'] = round(df_ita_rate['Confirmed']/df_ita_rate['Total tests'], 2)
df_ger_rate['positive_percentage'] = round(df_ger_rate['Confirmed']/df_ger_rate['Total tests'], 2)
df_us_rate['positive_percentage'] = round(df_us_rate['Confirmed']/df_us_rate['Total tests'], 2)
df_uk_rate['positive_percentage'] = round(df_uk_rate['Confirmed']/df_uk_rate['Total tests'], 2)
df_spa_rate['positive_percentage'] = round(df_spa_rate['Confirmed']/df_spa_rate['Total tests'], 2)


# In[ ]:


df_rate = pd.DataFrame(['France', 'Italy', 'Germany', 'USA', 'UK', 'Spain']).rename(columns={0:'Country'})
df_rate['positive_percentage_mean'] = [df_fra_rate['positive_percentage'].mean(), df_ita_rate['positive_percentage'].mean(),                                   df_ger_rate['positive_percentage'].mean(), df_us_rate['positive_percentage'].mean(),                                   df_uk_rate['positive_percentage'].mean(), df_spa_rate['positive_percentage'].mean()]
df_rate['positive_percentage_mean'] = df_rate['positive_percentage_mean']*100
df_rate['positive_percentage_mean'] = df_rate['positive_percentage_mean'].round(2)
df_rate


# ### COVID19 Test Results in India

# In[ ]:


df_ind_rate = pd.read_excel('../input/covid19-india-complete-data/COVID19 India Complete Dataset May 2020.xlsx', sheet_name='ICMR Testing Count')
df_ind_rate = df_ind_rate.dropna(subset=['Total Positive Cases']).reset_index(drop=True)
df_ind_rate['Total Individuals Tested'].fillna(df_ind_rate['Total Samples Tested']-900, inplace=True)
df_ind_rate['positive_percentage'] = round(df_ind_rate['Total Positive Cases']/df_ind_rate['Total Individuals Tested'], 5)
df_ind_rate_count = pd.DataFrame(['India']).rename(columns={0:'Country'})
df_ind_rate_count['positive_percentage_mean'] = round(df_ind_rate.loc[len(df_ind_rate)-1]['positive_percentage']*100, 2)


# In[ ]:


df_rate = pd.concat([df_rate, df_ind_rate_count], ignore_index=True)


# In[ ]:


fig = px.bar(df_rate.sort_values(by=['positive_percentage_mean'], ascending=False), x='Country', y='positive_percentage_mean',
            title='Percentage of People who turned out to be +ve in Testing')
fig.show()


# In[ ]:


df_hos_bed_per_day = df_hos_bed_per_day.dropna(subset=['TotalPositiveCases']).reset_index(drop=True)
df_hos_bed_per_day['TotalIndividualsTested'].fillna(df_hos_bed_per_day['Total Samples Tested']-900, inplace=True)
df_hos_bed_per_day['test_results_posratio'] = round(df_hos_bed_per_day['TotalPositiveCases']/df_hos_bed_per_day['TotalIndividualsTested'], 3)
df_hos_bed_per_day.head(2)


# In[ ]:


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_hos_bed_per_day['DateTime'], y=df_hos_bed_per_day['test_results_posratio']*100, name='Confirmed Cases',                          marker=dict(color='#D32210')))
fig1.layout.update(title_text='COVID-19 Positive Detection per Test Ratio in India w.r.t. Time',xaxis_showgrid=False, width=700, yaxis_title='% of Patients Tested +ve',
        height=500,font=dict(
#         family="Courier New, monospace",
        size=12,
        color="white"
    ))
fig1.layout.plot_bgcolor = '#097E99'
fig1.layout.paper_bgcolor = '#097E99'
fig1.show()


# In[ ]:


dbd_tc_india.rename(columns={'Daily Confirmed':'New Cases'}, inplace=True)
dbd_tc_india.head(2)


# In[ ]:


ss = []
for i in dbd_tc_india.index:
    if(i!= min(dbd_tc_india.index)):
        lm = dbd_tc_india.loc[i]['New Cases']/dbd_tc_india.loc[i-1]['New Cases']
    else:
        lm = np.NaN
    ss.append(lm)
        
dbd_tc_india['Growth_Rate'] = ss
dbd_tc_india.head(2)


# ### Analysing the Growth Factor in India

# In[ ]:


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=dbd_tc_india.iloc[35:(dbd_tc_india.shape[0]-1)]['Date'], y=dbd_tc_india.iloc[35:(dbd_tc_india.shape[0]-1)]['Growth_Rate'], name='Growth Factor',                          marker=dict(color='#008040')))
fig1.layout.update(title_text='COVID-19 Growth Factor in India w.r.t. Time',xaxis_showgrid=False, yaxis_showgrid=False, width=700, yaxis_title='Growth Factor',
        height=500,font=dict(
#         family="Courier New, monospace",
        size=12,
        color="white"
    ))
fig1.layout.plot_bgcolor = '#4d3900'
fig1.layout.paper_bgcolor = '#4d3900'
fig1.show()


# In[ ]:


print('Mean Growth Factor in India = ', round(dbd_tc_india.iloc[35:]['Growth_Rate'].mean(), 2))


# In[ ]:


df_ind_main = pd.read_excel('../input/covid19-india-complete-data/COVID19 India Complete Dataset May 2020.xlsx', sheet_name='Raw Data')
df_ind_main = df_ind_main.dropna(subset=['Date Announced'])
df_ind_main.reset_index(drop=True)
df_ind_main = df_ind_main.drop_duplicates(subset=df_ind_main.drop('Patient Number', axis=1).columns)
df_ind_main.reset_index(drop=True)
df_ind_main.head(2)


# ### Guesstimating the population that might have been affected by the Patients based on their places visited
# 

# In[ ]:


col = 'Notes'
df_ind_main['Notes'] = df_ind_main['Notes'].fillna('NA').apply(lambda x: x.replace('No Travel', 'Non-travel'))
conditions  = [ df_ind_main[col].str.contains('Travel') == True, df_ind_main[col].str.contains('Attended|attended') == True]
choices     = [1300, 350] 

# Guesstimating avg. population that might have been affected (Airport: 1200 (flight+both side airport) + 100[miscellaneous], 
# Religious Event: 250 + 100[miscellaneous])

df_ind_main["estd_population"] = np.select(conditions, choices, default=100) # default is 100 (only miscellaneous)

# Miscellaneous corresponds to local area shops, transportation, residential area, etc.)
# Since there has been no hard evidence of community transmission yet, in India, I have kept the figures on the lower side


# ### To better understand this I'm going to try out SIR models

# ### **SIR Epidemic Model for India** 
# 
# ##### This is a potential SIR model, if lockdown hadn't been imposed (14th March - 14th April, 30 days)

# #### For all the initial population (N) estimations, please refer to the notebook present in this GitHub repo of mine:
# https://github.com/debadridtt/COVID-19-Analysis/blob/master/SIR%20Modeling%20India%20%26%20State-Wise.ipynb

# In[ ]:


# Total population, N.
N = 1080000 # considering the a rough estimate of 10 lakhs as population of India who might have been exposed because 135 crore,
            
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 = 102, 19 # till India crossed 100 cases
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 2.4, 1./35 # considering Beta & Gamma value based on China's & Europe situation
# A grid of time points (in days)
t = np.linspace(0, 30, 30)

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w', figsize=(12,10))
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time in Days', size=13)
ax.set_ylabel('Number of People', size=13)
# ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
ax.set_facecolor('#dddddd')
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
ax.set_title('Potential COVID-19 Scenario from 14th March for next 30 days in India without lockdown', size=15)
plt.show()


# ### Let's see if we can estimate the Beta & Gamma parameter with splitting the dataset into train and validation considering the lockdown 

# In[ ]:


dbd_tc_india.head(2)


# In[ ]:


dbd_tc_param = pd.DataFrame(dbd_tc_india.groupby(['Date'])['Total Confirmed','Total Recovered', 'Total Deceased'].sum().reset_index())
dbd_tc_param['Total Active Cases'] = dbd_tc_param['Total Confirmed'] - dbd_tc_param['Total Recovered'] - dbd_tc_param['Total Deceased']
dbd_tc_param.head(3)


# In[ ]:


dbd_tc_pl = dbd_tc_param[(dbd_tc_param['Date']>'2020-03-01') & (dbd_tc_param['Date']<'2020-03-25')].reset_index(drop=True) # considering pre lockdown period
dbd_tc_pl.head(2)


# In[ ]:


dbd_tc_param = dbd_tc_param[dbd_tc_param['Date']>='2020-03-25'].reset_index(drop=True) # considering from lockdown date
dbd_tc_param = dbd_tc_param[:-1]
dbd_tc_param.head(2)


# In[ ]:


dbd_tc_param.tail(2)


# ## Estimating Beta & Gamma for India for SIR Modeling and Predicting for next 6 months
# 
# #### Please note that in this notebook I have shown only the best case scenario possible in India, for other cases please refer to the notebook here: 
# https://github.com/debadridtt/COVID-19-Analysis/blob/master/SIR%20Modeling%20India%20%26%20State-Wise.ipynb
# 
# 
# #### Beta and Gamma are estimated in the following way:
# - Validation data used is from 2nd Mar to 24th Mar (pre-lockdown period) and 25th Mar to 19th Apr (lockdown period)
# - Forward prediction of 60 days have been done from 20th April considering parameter values derived during lockdown period
# - Define y(t) for the SIR model, and then use RMSE as the loss function, and used L-BFGS-B gradient descent optimization to minimise the loss function 

# ### Pre-Lockdown Period (2nd March-25th March)
# 
# #### Assumptions taken:
# - An initial population of 150000 could have been potentially exposed to COVID-19 as of 2nd March
# 
# #### For all the initial population (N) estimations, please refer to the notebook present in this GitHub repo of mine:
# https://github.com/debadridtt/COVID-19-Analysis/blob/master/SIR%20Modeling%20India%20%26%20State-Wise.ipynb

# In[ ]:


data = dbd_tc_pl.set_index('Date')['Total Active Cases']
infected = dbd_tc_pl.set_index('Date')['Total Confirmed']
recovered = dbd_tc_pl.set_index('Date')['Total Recovered']


# In[ ]:


s_0 = 150000
i_0 = 5
r_0 = 3


# #### Defining Loss Function for estimating Beta and Gamma

# In[ ]:


def loss(point, data, recovered, s_0, i_0, r_0):
    size = len(data)
    beta, gamma = point
    def SIR(t, y):
        S = y[0]
        I = y[1]
        R = y[2]
        return [-beta*S*I/s_0, beta*S*I/s_0-gamma*I, gamma*I]
    solution = solve_ivp(SIR, [0, size], [s_0,i_0,r_0], t_eval=np.arange(0, size, 1), vectorized=True)
    l1 = np.sqrt(np.mean((solution.y[1] - data)**2))
    l2 = np.sqrt(np.mean((solution.y[2] - recovered)**2))
    alpha = 0.1
    return alpha * l1 + (1 - alpha) * l2


# In[ ]:


def predict(beta, gamma, data, recovered, s_0, i_0, r_0):
    new_index = list(data.index.values)
    size = len(new_index)
    def SIR(t, y):
        S = y[0]
        I = y[1]
        R = y[2]
        return [-beta*S*I/s_0, beta*S*I/s_0-gamma*I, gamma*I]
    extended_actual = np.concatenate((data.values, [None] * (size - len(data.values))))
    extended_recovered = np.concatenate((recovered.values, [None] * (size - len(recovered.values))))
    return new_index, extended_actual, extended_recovered, solve_ivp(SIR, [0, size], [s_0,i_0,r_0], t_eval=np.arange(0, size, 1))


# In[ ]:


def train(recovered, infected, data):
    recovered = recovered
    infected = infected
    data = data

    optimal = minimize(loss, [0.001, 0.001], args=(data, recovered, s_0, i_0, r_0), method='L-BFGS-B', bounds=[(0.00000001, 2), (0.00000001, 0.4)])
    print(optimal)
    beta, gamma = optimal.x
    new_index, extended_actual, extended_recovered, prediction = predict(beta, gamma, data, recovered, s_0, i_0, r_0)
    df = pd.DataFrame({'Actual Infected': extended_actual, 'Actual Recovered': extended_recovered, 'Susceptible': prediction.y[0], 'Predicted Infected': prediction.y[1], 'Predicted Recovered': prediction.y[2]}, index=new_index)
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_title('Estimating Beta and Gamma for India during pre-lockdown')
    df.plot(ax=ax)
    print(f"country=India, beta={beta:.8f}, gamma={gamma:.8f}, r_0:{(beta/gamma):.8f}")


# In[ ]:


train(recovered, infected, data)


# ### Lockdown Period (25th Mar - 4th May)
# 
# #### Assumptions taken:
# - An initial population of 750000 could have been potentially exposed to COVID-19 as of 25th March
# 
# #### For all the initial population (N) estimations, please refer to the notebook present in this GitHub repo of mine:
# https://github.com/debadridtt/COVID-19-Analysis/blob/master/SIR%20Modeling%20India%20%26%20State-Wise.ipynb
# 

# In[ ]:


dbd_tc_param.head(2)


# In[ ]:


dbd_tc_param.tail(2)


# In[ ]:


data = dbd_tc_param.set_index('Date')['Total Active Cases']
infected = dbd_tc_param.set_index('Date')['Total Confirmed']
recovered = dbd_tc_param.set_index('Date')['Total Recovered']


# In[ ]:


s_0 = 750000 
i_0 = 603
r_0 = 43


# In[ ]:


def loss(point, data, recovered, s_0, i_0, r_0):
    size = len(data)
    beta, gamma = point
    def SIR(t, y):
        S = y[0]
        I = y[1]
        R = y[2]
        return [-beta*S*I/s_0, beta*S*I/s_0-gamma*I, gamma*I]
    solution = solve_ivp(SIR, [0, size], [s_0,i_0,r_0], t_eval=np.arange(0, size, 1), vectorized=True)
    l1 = np.sqrt(np.mean((solution.y[1] - data)**2))
    l2 = np.sqrt(np.mean((solution.y[2] - recovered)**2))
    alpha = 0.1
    return alpha * l1 + (1 - alpha) * l2


# In[ ]:


pres_fut = np.array(list(data.index.values)+ list((np.array(pd.date_range('2020-05-05', periods=90))))) #  months from 5th May


# In[ ]:


def predict(beta, gamma, data, recovered, s_0, i_0, r_0):
    new_index = pres_fut
    size = len(new_index)
    def SIR(t, y):
        S = y[0]
        I = y[1]
        R = y[2]
        return [-beta*S*I/s_0, beta*S*I/s_0-gamma*I, gamma*I]
    extended_actual = np.concatenate((data.values, [None] * (size - len(data.values))))
    extended_recovered = np.concatenate((recovered.values, [None] * (size - len(recovered.values))))
    return new_index, extended_actual, extended_recovered, solve_ivp(SIR, [0, size], [s_0,i_0,r_0], t_eval=np.arange(0, size, 1))


# In[ ]:


def train(recovered, infected, data):
    recovered = recovered
    infected = infected
    data = data

    optimal = minimize(loss, [0.001, 0.001], args=(data, recovered, s_0, i_0, r_0), method='L-BFGS-B', bounds=[(0.000001, 0.5), (0.00000001, 0.4)])
    print(optimal)
    beta, gamma = optimal.x
    new_index, extended_actual, extended_recovered, prediction = predict(beta, gamma, data, recovered, s_0, i_0, r_0)
    df = pd.DataFrame({'Actual Infected': extended_actual, 'Actual Recovered': extended_recovered, 'Susceptible': prediction.y[0], 'Predicted Infected': prediction.y[1], 'Predicted Recovered': prediction.y[2]}, index=new_index)
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_title('Possible COVID19 India Scenario next 3 months from 5th May, 2020')
    df.plot(ax=ax)
    print(f"country=India, beta={beta:.8f}, gamma={gamma:.8f}, r_0:{(beta/gamma):.8f}")


# **- Estimating Beta and Gamma during lockdown period and using it to predict the figures for the next 3 months from 5th May 2020**

# In[ ]:


train(recovered, infected, data)


# In[ ]:


ncov_china['week_no'] = ncov_china['ObservationDate'].dt.week
ncov_china_infl = ncov_china.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_china_infl


# In[ ]:


ncov_china_infl_weekly = ncov_china_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_china_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_china_infl = pd.merge(ncov_china_infl, ncov_china_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_china_infl['Increased_Cases'] = np.log(ncov_china_infl['Increased_Cases'])
ncov_china_infl = ncov_china_infl.replace([np.inf, -np.inf], np.nan)
ncov_china_infl = ncov_china_infl.fillna(0)
ncov_china_infl.drop(ncov_china_infl.tail(1).index,inplace=True) 
ncov_china_infl


# In[ ]:


ncov_italy['week_no'] = ncov_italy['ObservationDate'].dt.week
ncov_italy_infl = ncov_italy.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_italy_infl


# In[ ]:


ncov_italy_infl_weekly = ncov_italy_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_italy_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_italy_infl = pd.merge(ncov_italy_infl, ncov_italy_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_italy_infl['Increased_Cases'] = np.log(ncov_italy_infl['Increased_Cases'])
ncov_italy_infl = ncov_italy_infl.replace([np.inf, -np.inf], np.nan)
ncov_italy_infl = ncov_italy_infl.fillna(0)
ncov_italy_infl.drop(ncov_italy_infl.tail(1).index,inplace=True) 
ncov_italy_infl


# In[ ]:


ncov_us['week_no'] = ncov_us['ObservationDate'].dt.week
ncov_us_infl = ncov_us.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_us_infl


# In[ ]:


ncov_us_infl_weekly = ncov_us_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_us_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_us_infl = pd.merge(ncov_us_infl, ncov_us_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_us_infl['Increased_Cases'] = np.log(ncov_us_infl['Increased_Cases'])
ncov_us_infl = ncov_us_infl.replace([np.inf, -np.inf], np.nan)
ncov_us_infl = ncov_us_infl.fillna(0)
ncov_us_infl.drop(ncov_us_infl.tail(1).index,inplace=True) 
ncov_us_infl


# In[ ]:


ncov_germany['week_no'] = ncov_germany['ObservationDate'].dt.week
ncov_germany_infl = ncov_germany.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_germany_infl


# In[ ]:


ncov_germany_infl_weekly = ncov_germany_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_germany_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_germany_infl = pd.merge(ncov_germany_infl, ncov_germany_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_germany_infl['Increased_Cases'] = np.log(ncov_germany_infl['Increased_Cases'])
ncov_germany_infl = ncov_germany_infl.replace([np.inf, -np.inf], np.nan)
ncov_germany_infl = ncov_germany_infl.fillna(0)
ncov_germany_infl.drop(ncov_germany_infl.tail(1).index,inplace=True) 
ncov_germany_infl


# In[ ]:


ncov_spain['week_no'] = ncov_spain['ObservationDate'].dt.week
ncov_spain_infl = ncov_spain.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_spain_infl


# In[ ]:


ncov_spain_infl_weekly = ncov_spain_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_spain_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_spain_infl = pd.merge(ncov_spain_infl, ncov_spain_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_spain_infl['Increased_Cases'] = np.log(ncov_spain_infl['Increased_Cases'])
ncov_spain_infl = ncov_spain_infl.replace([np.inf, -np.inf], np.nan)
ncov_spain_infl = ncov_spain_infl.fillna(0)
ncov_spain_infl.drop(ncov_spain_infl.tail(1).index,inplace=True) 
ncov_spain_infl


# In[ ]:


ncov_soukor['week_no'] = ncov_soukor['ObservationDate'].dt.week
ncov_soukor_infl = ncov_soukor.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_soukor_infl


# In[ ]:


ncov_soukor_infl_weekly = ncov_soukor_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_soukor_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_soukor_infl = pd.merge(ncov_soukor_infl, ncov_soukor_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_soukor_infl['Increased_Cases'] = np.log(ncov_soukor_infl['Increased_Cases'])
ncov_soukor_infl = ncov_soukor_infl.replace([np.inf, -np.inf], np.nan)
ncov_soukor_infl = ncov_soukor_infl.fillna(0)
ncov_spain_infl.drop(ncov_spain_infl.tail(1).index,inplace=True) 
ncov_soukor_infl


# In[ ]:


ncov_iran['week_no'] = ncov_iran['ObservationDate'].dt.week
ncov_iran_infl = ncov_iran.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_iran_infl


# In[ ]:


ncov_iran_infl_weekly = ncov_iran_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_iran_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_iran_infl = pd.merge(ncov_iran_infl, ncov_iran_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_iran_infl['Increased_Cases'] = np.log(ncov_iran_infl['Increased_Cases'])
ncov_iran_infl = ncov_iran_infl.replace([np.inf, -np.inf], np.nan)
ncov_iran_infl = ncov_iran_infl.fillna(0)
ncov_iran_infl.drop(ncov_iran_infl.tail(1).index,inplace=True) 
ncov_iran_infl


# In[ ]:


ncov_france['week_no'] = ncov_france['ObservationDate'].dt.week
ncov_france_infl = ncov_france.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_france_infl


# In[ ]:


ncov_france_infl_weekly = ncov_france_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_france_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_france_infl = pd.merge(ncov_france_infl, ncov_france_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_france_infl['Increased_Cases'] = np.log(ncov_france_infl['Increased_Cases'])
ncov_france_infl = ncov_france_infl.replace([np.inf, -np.inf], np.nan)
ncov_france_infl = ncov_france_infl.fillna(0)
ncov_france_infl.drop(ncov_france_infl.tail(1).index,inplace=True) 
ncov_france_infl


# In[ ]:


ncov_uk['week_no'] = ncov_uk['ObservationDate'].dt.week
ncov_uk_infl = ncov_uk.drop_duplicates(subset=['week_no'], keep='last').reset_index(drop=True)
ncov_uk_infl


# In[ ]:


ncov_uk_infl_weekly = ncov_uk_infl.set_index(['week_no']).diff().reset_index().fillna(0)
ncov_uk_infl_weekly.rename(columns={'Confirmed':'Increased_Cases'}, inplace=True)
ncov_uk_infl = pd.merge(ncov_uk_infl, ncov_uk_infl_weekly[['week_no', 'Increased_Cases']], how='left')
ncov_uk_infl['Increased_Cases'] = np.log(ncov_uk_infl['Increased_Cases'])
ncov_uk_infl = ncov_uk_infl.replace([np.inf, -np.inf], np.nan)
ncov_uk_infl = ncov_uk_infl.fillna(0)
ncov_uk_infl.drop(ncov_uk_infl.tail(1).index,inplace=True) 
ncov_uk_infl


# ### We all know an exponential graph keeps on increasing, and when we are in that period of exponential we are not able to predict how far is the inflection point in the curve

# ## Getting an Idea of the Inflection Point for a Country

# In[ ]:


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=ncov_china_infl['Confirmed'], y=ncov_china_infl['Increased_Cases'], name='China',                          ))
fig1.add_trace(go.Scatter(x=ncov_italy_infl['Confirmed'], y=ncov_italy_infl['Increased_Cases'], name='Italy',                          ))
fig1.add_trace(go.Scatter(x=ncov_us_infl['Confirmed'], y=ncov_us_infl['Increased_Cases'], name='USA',                          ))
fig1.add_trace(go.Scatter(x=ncov_soukor_infl['Confirmed'], y=ncov_soukor_infl['Increased_Cases'], name='South Korea',                          ))
fig1.add_trace(go.Scatter(x=ncov_france_infl['Confirmed'], y=ncov_france_infl['Increased_Cases'], name='France',                          ))
fig1.add_trace(go.Scatter(x=ncov_uk_infl['Confirmed'], y=ncov_uk_infl['Increased_Cases'], name='UK',                          ))
fig1.add_trace(go.Scatter(x=ncov_iran_infl['Confirmed'], y=ncov_iran_infl['Increased_Cases'], name='Iran',                          ))
fig1.add_trace(go.Scatter(x=ncov_spain_infl['Confirmed'], y=ncov_spain_infl['Increased_Cases'], name='Spain',                          ))
fig1.add_trace(go.Scatter(x=ncov_germany_infl['Confirmed'], y=ncov_germany_infl['Increased_Cases'], name='Germany',                          ))


fig1.layout.update(title_text='Predicting Inflection Point for the Countries',xaxis_showgrid=False, width=800, xaxis_title='Total no. of Confirmed Cases',                yaxis_title='log(Increased no. of Nwe Cases w.r.t. previous week)',
        height=600,font=dict(
#         family="Courier New, monospace",
        size=14,
        color="white"
    ))
fig1.layout.plot_bgcolor = '#3E6704'
fig1.layout.paper_bgcolor = '#3E6704'
fig1.show()


# ### The theory behind this is that, when the no. of weekly cases start dropping consistently for a few consecutive weeks w.r.t. previous week we have hit the inflection point
# ### We see that only China and South Korea have been able to hit the inflection point
# 
# For my understanding, I have taken reference from the following video:

# In[ ]:


from IPython.display import YouTubeVideo
# a talk about IPython at Sage Days at U. Washington, Seattle.
# Video credit: William Stein.
YouTubeVideo('54XLXg4fYsc')


# In[ ]:




