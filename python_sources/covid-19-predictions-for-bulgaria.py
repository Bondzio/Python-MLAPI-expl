#!/usr/bin/env python
# coding: utf-8

# This notebook tracks the spread of the novel coronavirus, also known as the 2019-nCoV in Bulgaria. It is a contagious respiratory virus that first started in Wuhan in December 2019. As of 2/11/2020, the virus is officially named COVID-19 by the World Health Organization.
# 
# Learn more from the [WHO](https://www.who.int/emergencies/diseases/novel-coronavirus-2019)
# <br>Learn more from the [CDC](https://www.cdc.gov/coronavirus/2019-ncov)

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, plot_mpl
import plotly.offline as py
import folium
import Bio.SeqIO
init_notebook_mode(connected=True)
plt.rcParams.update({'font.size': 14})


# Import the data (make sure you update this on a daily basis)

# In[ ]:


confirmed_df = pd.read_csv('../input/novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv')
deaths_df = pd.read_csv('../input/novel-corona-virus-2019-dataset/time_series_covid_19_deaths.csv')
recoveries_df = pd.read_csv('../input/novel-corona-virus-2019-dataset/time_series_covid_19_recovered.csv')


# In[ ]:


# Drop date columns if they are mostly NaN
na_columns = (confirmed_df.isna().sum() / confirmed_df.shape[0]) > 0.99
na_columns = na_columns[na_columns]

confirmed_df = confirmed_df.drop(na_columns.index, axis=1)
deaths_df = deaths_df.drop(na_columns.index, axis=1)
recoveries_df = recoveries_df.drop(na_columns.index, axis=1)


# In[ ]:


## Tidy up the data
confirmed_df = confirmed_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'], var_name='date', value_name='confirmed')
deaths_df = deaths_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'], var_name='date', value_name='deaths')
recoveries_df = recoveries_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'], var_name='date', value_name='recoveries')


# In[ ]:


confirmed_df['date'] = pd.to_datetime(confirmed_df['date'])
deaths_df['date'] = pd.to_datetime(deaths_df['date'])
recoveries_df['date'] = pd.to_datetime(recoveries_df['date'])


# In[ ]:


full_df = confirmed_df.merge(recoveries_df).merge(deaths_df)
full_df = full_df.rename(columns={'Country/Region': 'Country', 'date': 'Date', 'confirmed': "Confirmed", "recoveries": "Recoveries", "deaths": "Deaths"})
# Check null values
full_df.isnull().sum()


# In[ ]:


world_df = full_df.groupby(['Date']).agg({'Confirmed': ['sum'], 'Recoveries': ['sum'], 'Deaths': ['sum']}).reset_index()
world_df.columns = world_df.columns.get_level_values(0)

def add_rates(df):
    df['Confirmed Change'] = df['Confirmed'].diff().shift(-1)
 
    df['Mortality Rate'] = df['Deaths'] / df['Confirmed']
    df['Recovery Rate'] = df['Recoveries'] / df['Confirmed']
    df['Growth Rate'] = df['Confirmed Change'] / df['Confirmed']
    df['Growth Rate Change'] = df['Growth Rate'].diff().shift(-1)
    df['Growth Rate Accel'] = df['Growth Rate Change'] / df['Growth Rate']
    return df

world_df = add_rates(world_df)


# # Worldwide Cases

# In[ ]:


def plot_aggregate_metrics(df, fig=None):
    if fig is None:
        fig = go.Figure()
    fig.update_layout(template='plotly_dark')
    fig.add_trace(go.Scatter(x=df['Date'], 
                             y=df['Confirmed'],
                             mode='lines+markers',
                             name='Confirmed',
                             line=dict(color='Yellow', width=2)
                            ))
    fig.add_trace(go.Scatter(x=df['Date'], 
                             y=df['Deaths'],
                             mode='lines+markers',
                             name='Deaths',
                             line=dict(color='Red', width=2)
                            ))
    fig.add_trace(go.Scatter(x=df['Date'], 
                             y=df['Recoveries'],
                             mode='lines+markers',
                             name='Recoveries',
                             line=dict(color='Green', width=2)
                            ))
    return fig


# In[ ]:


plot_aggregate_metrics(world_df).show()


# # Worldwide Rates

# In[ ]:


def plot_diff_metrics(df, fig=None):
    if fig is None:
        fig = go.Figure()

    fig.update_layout(template='plotly_dark')
    fig.add_trace(go.Scatter(x=df['Date'], 
                             y=df['Mortality Rate'],
                             mode='lines+markers',
                             name='Mortality rate',
                             line=dict(color='red', width=2)))

    fig.add_trace(go.Scatter(x=df['Date'], 
                             y=df['Recovery Rate'],
                             mode='lines+markers',
                             name='Recovery rate',
                             line=dict(color='Green', width=2)))

    fig.add_trace(go.Scatter(x=df['Date'], 
                             y=df['Growth Rate'],
                             mode='lines+markers',
                             name='Growth rate confirmed',
                             line=dict(color='Yellow', width=2)))
    fig.update_layout(yaxis=dict(tickformat=".2%"))
    
    return fig


# In[ ]:


plot_diff_metrics(world_df).show()


# # Daily Percent Change in Growth Rate
# 
# Useful for tracking whether the growth rate is increasing. Any positive percentage indicates exponential growth.

# In[ ]:


fig = go.Figure()
fig.update_layout(template='plotly_dark')

tmp_df = world_df.copy()
tmp_df = tmp_df[tmp_df['Growth Rate Accel'] < 10]

fig.add_trace(go.Scatter(x=tmp_df['Date'], 
                         y=tmp_df['Growth Rate Accel'],
                         mode='lines+markers',
                         name='Growth Acceleration',
                         line=dict(color='Green', width=3)))
fig.update_layout(yaxis=dict(tickformat=".2%"))

fig.show()


# # Confirmed Cases by Country

# In[ ]:


confirmed_by_country_df = full_df.groupby(['Date', 'Country']).sum().reset_index()


# In[ ]:


fig = px.line(confirmed_by_country_df, x='Date', y='Confirmed', color='Country', line_group="Country", hover_name="Country")
fig.update_layout(template='plotly_dark')
fig.show()


# In[ ]:


# Log scale to allow for view
#  (1) of countries other than China, and
#  (2) identifying linear sections, which indicate exponential growth
fig = px.line(confirmed_by_country_df, x='Date', y='Confirmed', color='Country', line_group="Country", hover_name="Country")
fig.update_layout(
    template='plotly_dark',
    yaxis_type="log"
)
fig.show()


# ***You can select individual traces above by double-clicking on the legend on the right***

# ###### Top 60 countries by confirmed cases

# In[ ]:


confirmed_by_country_df.groupby('Country').max().sort_values(by='Confirmed', ascending=False)[:60]


# In[ ]:


k_layout_kwargs = {
    'font': dict(size=12,),
    'legend': dict(x=0, y=-0.7),
}


# # Modeling Bulgaria

# In[ ]:


bg_df = confirmed_by_country_df[confirmed_by_country_df['Country'] == 'Bulgaria'].copy()
bg_df = add_rates(bg_df)


# In[ ]:


tmp_df = bg_df[bg_df['Confirmed'] > 5]

plot_aggregate_metrics(tmp_df).show()


# In[ ]:


plot_diff_metrics(tmp_df).show()


# In[ ]:


from sklearn.linear_model import LinearRegression

bg_growth_rates = {}

n_days_to_fit = 7
confirmed_bg_df = confirmed_by_country_df[(confirmed_by_country_df['Country'] == 'Bulgaria') & (confirmed_by_country_df['Date'] >= (np.datetime64('today') - np.timedelta64(n_days_to_fit,'D')))]

x = (confirmed_bg_df['Date'] - confirmed_bg_df['Date'].min()).dt.days.to_numpy().reshape(-1, 1)
y = np.log(confirmed_bg_df['Confirmed'])
reg = LinearRegression().fit(x, y)
print(f"Model fit score: {reg.score(x, y):.2f}")
print(f"Growth rate: {reg.coef_[0]:.3f}")
bg_growth_rates[n_days_to_fit] = reg.coef_[0]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x[:,0],
        y=np.exp(y),
        name='Bulgaria - Current fit'
    )
)

xx = np.linspace(0, len(x[:,0]) + 14, 100)  # Forecast 14 days out
yy = reg.predict(xx.reshape(-1,1))

fig.add_trace(
    go.Scatter(
        x=xx,
        y=np.exp(yy),
        name='Bulgaria - Exponential fit',
        mode='lines',
    )
)

fig.update_layout(
    title=f"Exponential Model of Bulgaria. Confirmed Cases<br>(fit to last {n_days_to_fit} days) with 14-Day Extrapolation",
    xaxis_title=f"Days since {confirmed_bg_df['Date'].min()}",
    yaxis_title="Number of Confirmed Cases",
    yaxis_type="log",
    template="plotly_dark",
    **k_layout_kwargs,
)

fig.show()


# In[ ]:


n_days_to_fit = 4
confirmed_bg_df = confirmed_by_country_df[(confirmed_by_country_df['Country'] == 'Bulgaria') & (confirmed_by_country_df['Date'] >= (np.datetime64('today') - np.timedelta64(n_days_to_fit,'D')))]

x = (confirmed_bg_df['Date'] - confirmed_bg_df['Date'].min()).dt.days.to_numpy().reshape(-1, 1)
y = np.log(confirmed_bg_df['Confirmed'])

reg = LinearRegression().fit(x, y)
print(f"Model fit score: {reg.score(x, y):.2f}")
print(f"Growth rate: {reg.coef_[0]:.3f}")
bg_growth_rates[n_days_to_fit] = reg.coef_[0]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=confirmed_by_country_df[confirmed_by_country_df['Country'] == 'Bulgaria']['Date'],
        y=confirmed_by_country_df[confirmed_by_country_df['Country'] == 'Bulgaria']['Confirmed'],
        name='Bulgaria - Current fit',
        line=dict(width=4)
    )
)

predict_days_out = 7*2

exponential_fit_date_range = pd.date_range(confirmed_bg_df['Date'].min(), confirmed_bg_df['Date'].max() + np.timedelta64(predict_days_out,'D'))

xx = np.linspace(0, len(x[:,0]) + predict_days_out, exponential_fit_date_range.shape[0])  # Forecast 14 days out
yy = reg.predict(xx.reshape(-1,1))

fig.add_trace(
    go.Scatter(
        x=exponential_fit_date_range,
        y=np.exp(yy),
        name='Bulgaria - Exponential fit',
        mode='lines'
    )
)

fig.update_layout(
    title=f"Exponential Model of Bulgaria Confirmed Cases<br>(fit to last {n_days_to_fit} days) with {predict_days_out}-Day Extrapolation",
    xaxis_title=f"Date",
    yaxis_title="Number of Confirmed Cases",
    yaxis_type="log",
    template="plotly_dark",
    **k_layout_kwargs,
)

fig.show()


# In[ ]:


proxy_country = 'Italy'

confirmed_italy_df = confirmed_by_country_df[(confirmed_by_country_df['Country'] == proxy_country) & (confirmed_by_country_df['Confirmed'] >= 100)]

x = (confirmed_italy_df['Date'] - confirmed_italy_df['Date'].min()).dt.days.to_numpy().reshape(-1, 1)
y = np.log(confirmed_italy_df['Confirmed'])
reg = LinearRegression().fit(x, y)
print(f"Model fit score: {reg.score(x, y):.2f}")
print(f"Growth rate: {reg.coef_[0]:.3f}")
italy_growth_rate = reg.coef_[0]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x[:,0],
        y=np.exp(y),
        name=proxy_country
    )
)

xx = np.linspace(0, len(x[:,0]) + 14, 100)  # Forecast 14 days out
yy = reg.predict(xx.reshape(-1,1))

fig.add_trace(
    go.Scatter(
        x=xx,
        y=np.exp(yy),
        name=f'{proxy_country} - Exponential fit'
    )
)

fig.update_layout(
    title=f"Exponential Model of {proxy_country} Confirmed Cases<br>with 14-Day Extrapolation",
    xaxis_title=f"Days since {confirmed_italy_df['Date'].min()}",
    yaxis_title="Number of Confirmed Cases",
    yaxis_type="log",
    template="plotly_dark",
    **k_layout_kwargs,
)

fig.show()


# ### Applying the proxy model to Bulgaria

# In[ ]:


def linear_model(x, a, b):
    return b * x + a


def linear_model_fixed_slope(slope):
    def func(x, intercept):
        return linear_model(x, a=intercept, b=slope)
    
    return func

test_model = linear_model_fixed_slope(2)
x = np.array([1, 2, 3])
test_model(x=x, intercept=2)


# In[ ]:


from scipy.optimize import curve_fit


def get_model(model, popt):
    def fitted_model(x):
        return model(x, *popt)
    return fitted_model


x = (confirmed_bg_df['Date'] - confirmed_bg_df['Date'].min()).dt.days.to_numpy()
y = np.log(confirmed_bg_df['Confirmed'].to_numpy())

# Pull the slope from the Italy model and use for the U.S., allowing only the intercept to vary
model = linear_model_fixed_slope(italy_growth_rate)
popt, pcov = curve_fit(model, x, y)

fitted_model_italy_rate = get_model(model, popt)

# Now do the same using the slope from the Bulgaria model
bg_growth_rate_n_days_to_fit = 4
print(bg_growth_rate_n_days_to_fit)

model = linear_model_fixed_slope(bg_growth_rates[bg_growth_rate_n_days_to_fit])
popt, pcov = curve_fit(model, x, y)

fitted_model_bg_rate = get_model(model, popt)

# Plot results
for layout_kwargs in [{}, {"yaxis_type": "log"}]:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=confirmed_by_country_df[confirmed_by_country_df['Country'] == 'Bulgaria']['Date'],
            y=confirmed_by_country_df[confirmed_by_country_df['Country'] == 'Bulgaria']['Confirmed'],
            name='Bulgaria - Current fit',
            line=dict(width=4)
        )
    )

    exponential_fit_date_range = pd.date_range(confirmed_bg_df['Date'].min(), confirmed_bg_df['Date'].max() + np.timedelta64(14,'D'))

    xx = np.linspace(0, len(x) + 14, exponential_fit_date_range.shape[0])  # Forecast 14 days out
    yy = fitted_model_italy_rate(xx)

    fig.add_trace(
        go.Scatter(
            x=exponential_fit_date_range,
            y=np.exp(yy),
            name=f'Bulgaria - Exponential fit based on {proxy_country} growth rate ({italy_growth_rate:.0%})',
            mode='lines'
        )
    )

    #########

    yy = fitted_model_bg_rate(xx)

    fig.add_trace(
        go.Scatter(
            x=exponential_fit_date_range,
            y=np.exp(yy),
            name=f'Bulgaria - Exponential fit based on US growth rate ({bg_growth_rates[bg_growth_rate_n_days_to_fit]:.0%}) (fitted to {bg_growth_rate_n_days_to_fit} days)',
            mode='lines'
        )
    )

    fig.update_layout(
        title="Exponential Model of Bulgaria Confirmed Cases<br>with 14-Day Extrapolation",
        xaxis_title="Date",
        yaxis_title="Number of Confirmed Cases",
        template="plotly_dark",
        **k_layout_kwargs,
        **layout_kwargs
    )

    fig.show()


# The Italy growth rate is at 25%. The U.S. growth rate is at 38%

# # Bulgaria Model with Prophet
# 
# We allow for a linear model that detects changepoints at Prophet's default significance. In effect, this is a spline of linear models. This is nice because we expect the growth rate to change at some points during the spread.

# In[ ]:


from fbprophet.plot import plot_plotly
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot


# In[ ]:


full_pop = 330e6

#floor_model = lambda x: max(x - 1, 0)  # Use the value itself because the function only increases
floor_model = lambda x: round(0.65 * x)
cap_model = lambda x: round(min(full_pop, 1.5 * x + 10000))  # 50% above plus one to ensure floor > cap at 0

# Modeling Bulgaria confirmed cases 
confirmed_training_df = confirmed_by_country_df[(confirmed_by_country_df['Country'] == 'Bulgaria') & (confirmed_by_country_df['Confirmed'] > 0)]
confirmed_training_df = confirmed_training_df.rename(columns={'Date': 'ds', 'Confirmed': 'y'}).reset_index(drop=True)

confirmed_training_df['floor'] = confirmed_training_df.y.apply(floor_model)
confirmed_training_df['cap'] = confirmed_training_df.y.apply(cap_model)


# In[ ]:


confirmed_training_df.y = confirmed_training_df.y.apply(np.log10)
confirmed_training_df.floor = confirmed_training_df.floor.apply(np.log10)
confirmed_training_df.cap = confirmed_training_df.cap.apply(np.log10)


# In[ ]:


# Total confirmed model 
m = Prophet(
    growth='linear',
    #interval_width=0.90,
    changepoint_prior_scale=0.05,
    changepoint_range=0.9,
    yearly_seasonality=False,
    weekly_seasonality=False,
    daily_seasonality=False,
    #n_changepoints=2
)
m.fit(confirmed_training_df)
future = m.make_future_dataframe(periods=14)
future['floor'] = confirmed_training_df.floor
future['cap'] = confirmed_training_df.cap
confirmed_forecast = m.predict(future)


# In[ ]:


for kwargs in [{}, {"yaxis_type": "log"}]:
    fig = plot_plotly(m, confirmed_forecast, plot_cap=False, changepoints=True)
    annotations = []
    annotations.append(dict(
        xref='paper',
        yref='paper',
        x=0.0,
        y=1.15,
        xanchor='left',
        yanchor='bottom',
        text='Predictions for log10 Confirmed cases Bulgaria',
        font=dict(
            family='Arial',
            size=30,
            color='rgb(37,37,37)'),
        showarrow=False))
    fig.update_layout(
        annotations=annotations,
        **kwargs
    )
    fig.show()


# The y-axis above is the log of the number of cases. So let's rescale that.

# In[ ]:


for kwargs in [{}, {"yaxis_type": "log"}]:
    fig = plot_plotly(m, confirmed_forecast, plot_cap=False, changepoints=True)
    annotations = []
    annotations.append(dict(
        xref='paper',
        yref='paper',
        x=0.0,
        y=1.15,
        xanchor='left',
        yanchor='bottom',
        text='Predictions for Confirmed cases Bulgaria',
        font=dict(
            family='Arial',
            size=30,
            color='rgb(37,37,37)'),
        showarrow=False))
    fig.update_layout(
        annotations=annotations,
        **kwargs
    )
    for trace in fig.data:
        trace.y = np.power(trace.y, 10)
    fig.show()


# # World Map Visualization

# In[ ]:


data= pd.read_csv("../input/novel-corona-virus-2019-dataset/covid_19_data.csv")

data['Date'] = data['ObservationDate'].apply(pd.to_datetime)
data.drop(['SNo'],axis=1,inplace=True)

#Set Date column as the index column.
#data.set_index('Last Update', inplace=True)

# Countries affected
data.rename(columns={'Country/Region':'Country'},inplace = True)
countries = data['Country'].unique().tolist()

# Combining China and Mainland China cases
data['Country'].replace({'Mainland China':'China'},inplace=True)
countries = data['Country'].unique().tolist()

d = data['Date'][-1:].astype('str')
year = int(d.values[0].split('-')[0])
month = int(d.values[0].split('-')[1])
day = int(d.values[0].split('-')[2].split()[0])

from datetime import date
data_latest = data[data['Date'] >= pd.Timestamp(date(year,month,day))]

# Creating a dataframe with total no of confirmed cases for every country
Number_of_countries = len(data_latest['Country'].value_counts())

cases = pd.DataFrame(data_latest.groupby('Country')['Confirmed'].sum())
cases['Country'] = cases.index
cases.index=np.arange(1,Number_of_countries+1)

global_cases = cases[['Country','Confirmed']]
#global_cases.sort_values(by=['Confirmed'],ascending=False)

# Importing the world_coordinates dataset
world_coordinates = pd.read_csv('../input/world-coordinates/world_coordinates.csv')

# Merging the coordinates dataframe with original dataframe
world_data = pd.merge(world_coordinates,global_cases,on='Country')
world_data.head()

# create map and display it
world_map = folium.Map(location=[10, -20], zoom_start=2.3,tiles='Stamen Toner')

for lat, lon, value, name in zip(world_data['latitude'], world_data['longitude'], world_data['Confirmed'], world_data['Country']):
    folium.CircleMarker([lat, lon],
                        radius=10,
                        popup = ('<strong>Country</strong>: ' + str(name).capitalize() + '<br>'
                                '<strong>Confirmed Cases</strong>: ' + str(value) + '<br>'),
                        color='red',
                        
                        fill_color='red',
                        fill_opacity=0.7 ).add_to(world_map)
world_map


# ## Exploring Coronavirus (SARS-CoV-2) Genome
# * Using data from https://www.nature.com/articles/s41586-020-2008-3

# In[ ]:


for sequence in Bio.SeqIO.parse('/kaggle/input/coronavirus-genome-sequence/MN908947.fna', "fasta"):
    print('Id: ' + sequence.id + '\nSize: ' + str(len(sequence))+' nucleotides')


# In[ ]:


sequence = '../input/coronavirus-genome-sequence/MN908947.txt'
with open(sequence) as text: 
    print (text.read(100000))


# The sequencing of the virus genome is essential for the development of vaccines and diagnostic tests. They are also key to understanding the spread of the virus, as well as allowing to detect possible mutations. https://panoramafarmaceutico.com.br/2020/03/02/pesquisadores-brasileiros-sequenciam-genoma-do-coronavirus-em-apenas-dois-dias/ It helps to track the virus since it changes the genetic codes.

# #### *TODO*
# 
# * Project peak of active cases
# * Apply [SIR model](https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/)
