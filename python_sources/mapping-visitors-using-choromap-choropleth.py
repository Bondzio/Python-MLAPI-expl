#!/usr/bin/env python
# coding: utf-8

# # Introduction
# Within this notebook, we are going to plot the number of visitor using choroplet plotly. The number of IP is unique for each visitor, and they will be our reference to see the where thraffic of the website visitors are coming. We also gonna put some exploratory analysis at the end regarding the country and the language being used by the top contributive traffic visitor country. Enjoy!

# # Import Library

# In[ ]:


import pandas as pd
import plotly.graph_objs as go 
import seaborn as sns
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
get_ipython().run_line_magic('matplotlib', 'inline')


# # Get the Data
# In here we see the data of the website traffic and the visitors countries. Somehow, for those who are not familiar with the Alpha-2 code for each country might be puzzeled with those country code. Hence, I will merge this data with the information of code from iban.com/country-codes (which I already import to csv file manually since I always failed to import the data as HTML) so we could see clearly the country name. The data from iban.com also provides Alpha-3 code column that can be used to plot the country using choroplet plotly. 

# In[ ]:


df = pd.read_csv('../input/web-visitor-interests/visitor-interests.csv')
df.head(5)


# In[ ]:


df_code = pd.read_csv('../input/countrycode-from-ibancom/CountryCode')
df_code.head()


# don't forget to change tha name of the columns to make it mergeable.

# In[ ]:


dx=df_code[['Country','Alpha-2 code','Alpha-3 code']]
dx.columns = ['Country full name','Country','Alpha-3 code']


# # Merge the Data
# After changing the columns name to make the data inline, now we can merge the data on the country column. Note that at the end of working for this notebook, I just realize that there are some Alpha-2 codes that are not listed. Since the number is not so big I decided to drop the unlisted country code.

# In[ ]:


df_all = pd.merge(df,dx,on='Country').dropna(axis=0)
df_all.head()


# Now our data is ready, lets see how many visitor we have in each country by count the number of IP address.

# In[ ]:


df_IP = df_all.groupby('Alpha-3 code',as_index=False).count()
df_IP.head()


# # Start Using the Choromap
# After obtaining the information about the number of visitors we can now put our data to be plot by the choroplet. I start by separate the choromap parmeter by data and layout before plotting to make it easier on setting the parameters.

# In[ ]:


data = dict(
        type = 'choropleth',
        locations = df_IP['Alpha-3 code'],
        z = df_IP['IP'],
        text = df_IP['IP'],
        colorbar = {'title' : 'Number of visitors'},
    colorscale='Oranges'
    ,
      ) 


# In[ ]:


layout = dict(
    title = 'Number of Visitors',
    geo = dict(
        showframe = False,
        projection = {'type':'equirectangular'}
    )
)


# In[ ]:


choromap = go.Figure(data = [data],layout = layout)
iplot(choromap)


# # Exploratory Analysis

# **5 most traffict contributor countries** 

# In[ ]:


df_all.groupby('Country full name')['IP'].count().sort_values(ascending=False).head(5)


# **5 most used languages**

# In[ ]:


df_bylang = df_all.groupby(by='Languages',as_index=False)['IP'].count()
df_bylang.sort_values('IP',ascending=False).head(5)


# **Visitor Interest**

# In[ ]:


df_byint = df_all.groupby(by='Interests',as_index=False)['IP'].count()
df_byint.sort_values('IP',ascending=False).head(5)


# Now we will see the the visitor's country by the language they are used to access the website. This data can be used to manage the language version of website and also match the advertisement's language embed in the website to make sure the contain can be understood by the visitors.

# In[ ]:


#English
df_all[df_all['Languages']=='english'].groupby('Country full name').count().sort_values(by='IP',ascending=False).head(5)


# In[ ]:


#Russian
df_all[df_all['Languages']=='russian'].groupby('Country full name').count().sort_values(by='IP',ascending=False).head(5)


# In[ ]:


#Chinese
df_all[df_all['Languages']=='chinese'].groupby('Country full name').count().sort_values(by='IP',ascending=False).head(5)


# In[ ]:


#French
df_all[df_all['Languages']=='french'].groupby('Country full name').count().sort_values(by='IP',ascending=False).head(5)

