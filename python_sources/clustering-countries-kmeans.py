#!/usr/bin/env python
# coding: utf-8

# # **1. Load In Libraries and Data**

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from sklearn import preprocessing
from math import log10, floor
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


plt.rcParams["figure.figsize"] = [20,10]
df_Data = pd.read_csv('/kaggle/input/unsupervised-learning-on-country-data/Country-data.csv')

# convert exports, health and imports into montery values
df_Data['exports'] = df_Data['exports']/100 * df_Data['gdpp']
df_Data['health'] = df_Data['health']/100 * df_Data['gdpp']
df_Data['imports'] = df_Data['imports']/100 * df_Data['gdpp']


# # **2. Exploratory Analysis**

# **2.1 Check For Nulls**

# In[ ]:


df_Data.info()


# The findings here show there are no nulls in the data set

# **2.2 Correlation heat map**

# In[ ]:


plt.figure()
sb.heatmap(df_Data.corr(),annot=True)


# Strong positive linear correlation between:
# 1. Imports and exports
# 2. Health and gdpp
# 3. Income and gdpp
# 4. Exports and gdpp
# 5. Imports and gdpp
# 6. Total fertility and Child mortality
# 
# Strong negative linear correlation between:
# 1. life expectancy and child mortality
# 2. life expectancy and total fertility
# 
# 
# This is not the full list, just most obvious ones

# **2.3 Univariate Analysis - boxplot**

# In[ ]:


####  9 features so 9 subplots (3 columns and 3 rows)
num_rows=3
num_cols=3
fig = plt.figure()
count=0

for criteria in df_Data.columns.to_list()[1:]:# don't use first column
    count=count+1
    ax = fig.add_subplot(num_rows,num_cols,count)
    ax = sb.boxplot(y=df_Data[criteria])
    ax.set_title(criteria)


# All features have outliers ==> should not remove since only 167 countries (removing data will ahve large effect)
# 
# All data is skewed

# **2.4 Bivariate Analysis - pairplot**

# In[ ]:


sb.pairplot(df_Data,diag_kind='kde',corner=True) 


# # **3. PCA**

# **3.1 Scale Data**

# Here we isolate the numerical data and scale it (vital step for PCA)

# In[ ]:


#### Isolate numerical data from the dataframe

# Drop the countries
df_X = df_Data.drop(['country'],axis=1) # ==> so that data is numerical and can scale
X = df_X.values # get only the values from it ==> array

# Scale the data (mean = 0 and sd = 1)
scaler = preprocessing.StandardScaler().fit(X)
X_scaled = preprocessing.scale(X)


# **3.2 Explained Variance vs Number of Components**

# In[ ]:


## Define function to found to a certain number of significant figures
def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)


# In[ ]:


#### Set up PCA and get explained variances
pca = PCA()
principalComponents = pca.fit_transform(X_scaled) # principle components for each country (row), for each feature
ExplainedVariance = pca.explained_variance_ratio_ # explained variance of each principle component


# In[ ]:


#### Plot the explained variances against number of components

# create dataframe from the explained variance data
df_ExplainedVariance = pd.DataFrame(np.array([list(range(1,len(ExplainedVariance)+1)),ExplainedVariance]).transpose(),
                                    columns=['No. Components','ExplainedVariance'])

# calculate cumulative sum of the explained variances
df_ExplainedVariance['EV Cum Sum'] = df_ExplainedVariance['ExplainedVariance'].cumsum()


# plot the explained variances agianst number of components
fig = plt.figure()

ax = fig.add_subplot(2,1,1) # first subplot is plot of the cumulative sum
ax.plot(df_ExplainedVariance['No. Components'].values,
        df_ExplainedVariance['EV Cum Sum'].values,
        linestyle='-', marker='x')
ax.set_xlabel('Total Number of Components, N')
ax.set_xticks(df_ExplainedVariance['No. Components'].values)
ax.set_xlim(0,10)
ax.set_ylabel('Cumulative Sum of Explained Variance')
ax.set_ylim(0,1.05)
plt.grid()
for i, txt in enumerate(df_ExplainedVariance['EV Cum Sum'].values): # annotate
    ax.annotate(round_sig(txt,3), (df_ExplainedVariance['No. Components'].values[i]+0.1, df_ExplainedVariance['EV Cum Sum'].values[i]-0.04))



ax = fig.add_subplot(2,1,2) #second suplot is plot of the bar chart
ax.bar(df_ExplainedVariance['No. Components'].values,
        df_ExplainedVariance['ExplainedVariance'].values)
ax.set_xlabel('Component, n')
ax.set_xticks(df_ExplainedVariance['No. Components'].values)
ax.set_xlim(0,10)
ax.set_ylim(0,0.65)
ax.set_ylabel('Explained Variance')
plt.grid(axis='y')
for i, txt in enumerate(df_ExplainedVariance['ExplainedVariance'].values): # annotate
    ax.annotate(round_sig(txt,3), (df_ExplainedVariance['No. Components'].values[i]-0.1, df_ExplainedVariance['ExplainedVariance'].values[i]+0.01))


# top plot shows the cumulative explained variance plotted agianst the number of components.
# The bototm plot shows the individual expained variances for different components.
# 
# If we take 4 principle components then we have over 0.90 of the explained variance ==> do this

# **3.3 K-Means Clustering**

# In[ ]:


#### Get Training data for 4 principle components

n_PC = 4 # this is the number of principle components used for the ML model, set based on previous graphs

# redo PCA with the number of components = n_PC  and fit to scaled data to get the data used for clustering
pca = PCA(n_components = n_PC)
principalComponents = pca.fit_transform(X_scaled) # this is the data used for clustering


# In[ ]:


#### Find elbow point to get most appropriate nubmer of clusters (plot inertia vs number of clusters)

# loop through different numbers of clusters and plot effects of number of clusters on intertias

ks = range(1, 10)
inertias = []
for k in ks:
    # Create a KMeans instance with k clusters: model
    model = KMeans(n_clusters=k)
    # Fit model to samples
    model.fit(principalComponents)
    # Append the inertia to the list of inertias
    inertias.append(model.inertia_)

    
    
plt.figure()
plt.plot(ks, inertias, '-o')
plt.xlabel('number of clusters, k')
plt.ylabel('inertia')
plt.title('Inertia vs Clusters for ' +str(n_PC)+' Principle Components')
plt.xticks(ks)
plt.grid()
plt.show()


# This shows that the elbow point is when there are 3 clusters. Use this for to train clustering model

# In[ ]:


# Train model, using prescribed number of clusters
n_k_means_Clusters = 3 #from elbow point identification
MYSEED = 5 # set random seed so that the clusters are always the same

# set up and trian model
model = KMeans(n_clusters=n_k_means_Clusters, random_state=MYSEED)
model.fit(principalComponents)

# Combine the predicted clusters with the orginal data and make new dataframe
Groups = model.labels_ # Groups relates o the clusters found by the K-means model
df_Groups = pd.DataFrame(Groups, columns = ['Groups'])
df_KMeans = df_Data.join(df_Groups)


# The df_KMeans can now be used for visualisation of the clusters

# # **4. Visualising the clusters**

# **4.1 Scatter Plots**

# To visualise the clusters, I use plotly.
# 
# I loop through all combinations of features and within each feature I plot the different clusters as points on a scatter graph. This therefore plots every cluster for every unique combination of features as a different layer. I then use plotly to create buttons in a dropdown menu to isolate each unique ocmbination of features, one at a time.

# In[ ]:


import plotly.graph_objs as go # use plotly
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot
init_notebook_mode()

#rename df_KMeans as df_Data
df_Data = df_KMeans

Groups = np.sort(df_Data['Groups'].unique()) # this is a list of the unique gorups in ascending order



#### loop through different combinations of columns (for cluster plot) and within each different colouring for each group

# set up empty lists
data = [] # This stores the different layers
buttons_list=[] # this stores the buttons

   

# get column names (names of the features)
col_names = df_Data.columns.to_list()
col_names = col_names[1:len(col_names)-1]# drop first and last columns (this is the country and the group)

# Create own names for the buttons and the point labels in plotly
button_names = ['Child Mortality','Exports','Health Spending','Imports','Income','Inflation','Life Expectency','Fertility Rate','GDP per Capita']
Label_Names = ['Child mortality [deaths children under 5 per 1000 live births]','Exports [% gdp per capita]','Health spending [% gdp per capita]','Imports [% gdp per capita]','Net income per person [$]','Inflation [% growth rate of GDP]','Life expectency','Fertility rate [Children per woman]','GDP per capita [$/person]']


# find pairs of unique combinations of these names
import itertools
comb_cols = list(itertools.combinations(col_names, 2)) # pairs of unique combinations for the dataframe columns
comb_button_names = list(itertools.combinations(button_names, 2)) #unique names for the buttons
comb_Label_Names = list(itertools.combinations(Label_Names, 2)) # unique names for the labels

count = -1 # This is used to count what layer we are on (in the loops)
count_button = -1 # this is a counter for what button/label we are on

for comb in comb_cols: # loop through the different combinations of column names
    
    feature_1 = comb[0] # first feature in the unique combination
    feature_2 = comb[1] # second feature in the unique combination
    
    count_button = count_button+1
    button_name_1 = comb_button_names[count_button][0] # first feature in the unique button name
    button_name_2 = comb_button_names[count_button][1] # second feature in the unique button name
    
    label_name_1 = comb_Label_Names[count_button][0] # first feature in the unique label
    label_name_2 = comb_Label_Names[count_button][1] # second feature in the unique label
    
    df_comb = df_Data[['country','Groups',feature_1,feature_2]] # dataframe for that combination of columns + country name + group
    Bool_Button = [False] * len(Groups) * len(comb_cols) # Initialise a list which will be used by the correpsonding button to turn layers on and off
    # ==> length of it is equal to number of layers
    
    # within each unique column combination, loop through the different groups and create scatter plot for each
    for group in Groups:
        count = count+1
        df_comb_group = df_comb[df_comb['Groups']==group]
        
        data.append(go.Scatter(
            x=df_comb_group[feature_1],
            y=df_comb_group[feature_2],
            mode='markers',
            marker=go.scatter.Marker(
                size=10,
                opacity=1),
            text='<br><b>'+ df_comb_group['country'] + '</b>' +
            '<br>'+
            '<br>' + label_name_2 + ': ' + df_comb_group[feature_2].astype(str)+
            '<br>' + label_name_1 + ': ' + df_comb_group[feature_1].astype(str),
            hoverinfo='text',
            name = str(group),
            visible=False))
        
        Bool_Button[count] = True  # This links the button to the layers plotted in this for loop. e.g. the first button will turn on the groups for the first unique combination of columns
    
    # Create the different buttons (one for each unique combination of columns)
    buttons_list.append(dict(args=['visible', Bool_Button],
                label= button_name_2 + ' vs ' + button_name_1,
                method='restyle'))


# turn on the layers for the first button
for  i in range(len(Groups)):
    data[i]['visible']=True


layout = go.Layout(width = 900, height=550)

layout.update(updatemenus=list([
        dict(x=-0.05,
            y=1,
            yanchor='top',
            buttons=buttons_list)]),
    legend=dict(x=-0.25, y=0.5))


fig=go.Figure(data=data, layout = layout)
iplot(fig, filename = 'clusters') 


# You may need to zoom out in your browser to view this visualisation properly!
# 
# I could not figure out how to do the axes for each layer so the axes labels are within the hover text (hover over each  point for that information)
# 
# The dropdown menu on the left shows all the unique combinations of columns (36 of them).
# 
# By going through them we can see that in most of them the clusters don't overlap (or show minimal overlap). There is however alot of overlap  when plotting against inflation data (e.g. Inflation vs income)
# 
# For each option in the drop down menu we can isolate a cluster in the graph by double clicking on the correpsonding legend on the left of the figure.
# 
# For this model and the seed i have set, cluster 1 represents the top priority countries for aid. The full list of countries is below
# 

# **4.2 Countries by groups**

# 4.2.1 Below is a choropleth map showing countries by group

# In[ ]:


import pycountry
import plotly.graph_objs as go # use plotly

country_geo = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json' # country information


#### Change several country names so pycountry can find the isocode
df_Data['country'] = df_Data['country'].str.replace('Cape Verde', 'Cabo Verde')
df_Data['country'] = df_Data['country'].str.replace('Congo, Dem. Rep.', 'Congo, The Democratic Republic of the')
df_Data['country'] = df_Data['country'].str.replace('Congo, Rep.', 'Republic of the Congo')
df_Data['country'] = df_Data['country'].str.replace('Macedonia, FYR', 'North Macedonia')
df_Data['country'] = df_Data['country'].str.replace('Micronesia, Fed. Sts.', 'Micronesia, Federated States of')
df_Data['country'] = df_Data['country'].str.replace('South Korea', 'Korea, Republic of')
df_Data['country'] = df_Data['country'].str.replace('St. Vincent and the Grenadines', 'Saint Vincent and the Grenadines')


#### Turn country names into isocodes and put the codes into dataframe
list_countries = df_Data['country'].unique().tolist() # unique list of countries

dict_country_code = {}  # To hold the country names and their ISO
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country) # try searching for country ==> fuzzy matching
        country_code = country_data[0].alpha_3
        dict_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        dict_country_code.update({country: ' '})

# Output:
#could not add ISO 3 code for -> Cape Verde
#could not add ISO 3 code for -> Congo, Dem. Rep.
#could not add ISO 3 code for -> Congo, Rep.
#could not add ISO 3 code for -> Macedonia, FYR
#could not add ISO 3 code for -> Micronesia, Fed. Sts.
#could not add ISO 3 code for -> South Korea
#could not add ISO 3 code for -> St. Vincent and the Grenadines
# ==> used above to change names of these so same as in the isocode

#### create a new column iso_alpha in the data and fill it with appropriate iso 3 code
for key in dict_country_code:
    df_Data.loc[(df_Data.country == key), 'iso_alpha_3'] = dict_country_code[key]

    
#### Check for duplicate codes
duplicateRows = df_Data[df_Data['iso_alpha_3'].duplicated(keep=False)]

# Niger's iso code is wrong ==> change to NER
df_Data['iso_alpha_3'] = df_Data['iso_alpha_3'].str.replace('NGA', 'NER')



layout_Ch = go.Layout(width = 1100, height=700)

data_Ch = go.Choropleth(geojson=country_geo, 
              locations=df_Data['iso_alpha_3'].to_list(), 
              z=df_Data['Groups'].to_numpy(),
              text =df_Data['country'],
              #autocolorscale=True,
              colorscale  = [[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']],
              hoverinfo  = 'text+z',
              colorbar = dict(thickness=20, ticklen=3, title = 'Groups'),
              zmin = df_Data['Groups'].to_numpy().min(),
              zmax = df_Data['Groups'].to_numpy().max(),
              marker_line_width=0,
              marker_opacity=0.7,
              visible=True)

fig2=go.Figure(data=data_Ch, layout = layout_Ch)
iplot(fig2) 


# May need to zoom out a bit to see this properly. there is a color bar on the right to help deintify the cluster number

# 4.2.2 Below is list of priority countries for aid

# In[ ]:


df_AID = df_Data[df_Data['Groups']==1]['country'].reset_index()
df_AID = df_AID.drop(['index'],axis=1)
Aid_Countries = df_AID.values.tolist()


# In[ ]:


print(Aid_Countries)
print('\n')
print(len(Aid_Countries))


# This is the list of top priority countries in alphabetical order found by:
# 1. turning imports, exports and health into monetary values (rather than percentages)
# 2. scaling the data
# 3. using 4 principle components (0.934 explained variance)
# 4. Using 3 clusters (elbow point)
# 
# 
# Can use this list in addition to the visual in 4.2.1 to select certain countries for aid ==> might be most beneficaial to give aid to countries that are geographically close together (i.e. give aid to regions, not just individual countries). Can use the visual in 4.2.1 to achieve this.
# 
# 
# 
# Improvements to what have been done here could be:
# 1. removing the inflation data (due to the observations at end of section 4.1) and reclustering
# 2. Investigating effect of using different number of clusters and principle components
# ==> right now 48 potential countries is definitely too many for $10 million of aid. Should find ways to narrow this down a bit. one way was, as i suggested, selecting countries that are geographically close together. Another could be by using more clusters.
# 3. Trying out other clustering models
# 
