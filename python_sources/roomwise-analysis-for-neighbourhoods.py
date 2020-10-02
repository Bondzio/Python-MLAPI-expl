#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


data_dir = "../input/new-york-city-airbnb-open-data/AB_NYC_2019.csv"
df=pd.read_csv(data_dir)
df.head()


# In[ ]:


df.shape


# In[ ]:


df.info()


# ### Dealing with Nulls

# In[ ]:


null_df = df.isnull().sum() != 0
columns_having_null = null_df[null_df == True].index
number_of_nulls = df[list(columns_having_null)].isnull().sum()

dict(zip(columns_having_null,number_of_nulls))


# * The 'last_review' is null because there was no review.
# * 'name' and 'host_name' are typically insignificant to our analysis, so we can replace nulls with 'None' or even drop these columns.
# * replace null values by 0 in 'reviews_per_month' column

# In[ ]:


df.last_review.fillna('None',inplace=True)
df.reviews_per_month.fillna(0,inplace = True)
df.name.fillna('None',inplace = True)
df.host_name.fillna('None',inplace=True)


# In[ ]:


assert sum(df.isnull().sum()) == 0


# ## Explaratory Data Analysis

# In[ ]:


sns.set_style('darkgrid')
palettes=['inferno','plasma','magma','cividis','Oranges','Greens','YlOrBr', 'YlOrRd', 'OrRd','Greys', 'Purples', 'Blues']


# In[ ]:


def plot_unique_num(dataframe):
    
    column=[]
    unique_values=[]
    for col in dataframe.columns:
        column.append(col)
        unique_values.append(df[col].nunique())

    fig, ax = plt.subplots(figsize=(8,8))
    sns.barplot(x = unique_values, y = column, ax = ax, palette =palettes[np.random.randint(0,12)])

    for i,p in enumerate(ax.patches):
        ax.annotate('{}'.format(unique_values[i]),(p.get_width(),p.get_y()+0.4),fontsize=12)
        
    
    plt.xlabel('No. of unique values')
    plt.ylabel('columns')
    plt.show()


# #### Unique Categorical Features

# In[ ]:


categorical_features = df.select_dtypes(include='object')
plot_unique_num(categorical_features)


# #### Unique Numeric Features

# In[ ]:


numeric_features = df.select_dtypes(include=['float','integer'])
plot_unique_num(numeric_features)


# #### Neighbourhood Groups

# In[ ]:


plt.figure(figsize=(15,10))
sns.countplot(x=df['neighbourhood_group'],palette=palettes[np.random.randint(0,12)])


# #### Price variation across groups for various room types

# In[ ]:


plt.figure(figsize=(15,6))
sns.boxenplot(x='neighbourhood_group',y='price',hue='room_type',data=df,palette=palettes[np.random.randint(0,12)])


# #### Varition in Average Minimum Nights across different Gropus

# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x='neighbourhood_group',y='minimum_nights',hue='room_type',data=df,palette=palettes[np.random.randint(0,12)])


# #### Varition in Average Price across different Gropus

# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x='neighbourhood_group',y='price',hue='room_type',data=df,palette=palettes[np.random.randint(0,12)])


# #### Varition in Average calculated_host_listings_count across different Gropus

# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x='neighbourhood_group',y='calculated_host_listings_count',hue='room_type',data=df,palette=palettes[np.random.randint(0,12)])


# #### Varition in Average Availability across different Gropus

# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x='neighbourhood_group',y='availability_365',hue='room_type',data=df,palette=palettes[np.random.randint(0,12)])


# #### Varition in Average reviews_per_month across different Gropus

# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x='neighbourhood_group',y='reviews_per_month',hue='room_type',data=df,palette=palettes[np.random.randint(0,12)])


# #### No. of different rooms in each group

# In[ ]:


plt.figure(figsize=(15,10))
sns.countplot(x='neighbourhood_group',hue='room_type',data=df,palette = palettes[np.random.randint(0,12)])


# #### Exploring each and every group

# In[ ]:


neigh_groups = df['neighbourhood_group'].unique()
features = ['price','minimum_nights','calculated_host_listings_count','availability_365']
neigh_groups


# In[ ]:


def stats_within_group(group,feature):
    sub_df = df.loc[df['neighbourhood_group']==group]
    sub_df = sub_df.pivot_table(index ='neighbourhood',columns='room_type',values=feature,aggfunc='mean')
    sub_df.fillna(0,inplace=True)
    
    fig,ax = plt.subplots(3,1,figsize=(15,15))
    f_size=15
    
    entire_df = sub_df.sort_values(by='Entire home/apt',ascending=False)[:10]
    sns.barplot(x=entire_df['Entire home/apt'],y=entire_df.index,palette=palettes[np.random.randint(0,12)],ax=ax[0])
    for i, p  in enumerate(ax[0].patches):
            ax[0].annotate('{:.1f}'.format(entire_df['Entire home/apt'][i]),(p.get_width(),p.get_y()+0.5),fontsize=f_size)
            ax[0].tick_params(labelsize=12)
            ax[0].set_xlabel('Entire home/apt',fontsize=12)
            ax[0].set_ylabel('Neighbourhood',fontsize=12)

    private_df = sub_df.sort_values(by='Private room',ascending=False)[:10]
    sns.barplot(x=private_df['Private room'],y=private_df.index,palette=palettes[np.random.randint(0,12)],ax=ax[1])
    for i, p  in enumerate(ax[1].patches):
            ax[1].annotate('{:.1f}'.format(private_df['Private room'][i]),(p.get_width(),p.get_y()+0.5),fontsize=f_size)
            ax[1].tick_params(labelsize=12)
            ax[1].set_xlabel('Private room',fontsize=12)
            ax[1].set_ylabel('Neighbourhood',fontsize=12)

    shared_df = sub_df.sort_values(by='Shared room',ascending=False)[:10]
    sns.barplot(x=shared_df['Shared room'],y=shared_df.index,palette=palettes[np.random.randint(0,12)],ax=ax[2])
    for i, p  in enumerate(ax[2].patches):
            ax[2].annotate('{:.1f}'.format(shared_df['Shared room'][i]),(p.get_width(),p.get_y()+0.5),fontsize=f_size)
            ax[2].tick_params(labelsize=12)
            ax[2].set_xlabel('Shared room',fontsize=12)
            ax[2].set_ylabel('Neighbourhood',fontsize=12)
    plt.suptitle(feature+' in '+group,fontsize=20)


# In[ ]:


def correlation_within_groups(group_name):
    
    sub_df = df[df['neighbourhood_group'] == group_name]
    plt.figure(figsize=(8,8))
    sns.heatmap(sub_df.corr(),cmap=palettes[np.random.randint(5,12)],annot=True,fmt='.2f')
    plt.xlabel('Features',fontsize=10)
    plt.ylabel('Features',fontsize=10)
    plt.title(group_name,fontsize=18)


# ### *Explore Brooklyn*

# In[ ]:


correlation_within_groups(neigh_groups[0])


# In[ ]:


stats_within_group(neigh_groups[0],features[0])


# In[ ]:


stats_within_group(neigh_groups[0],features[1])


# In[ ]:


stats_within_group(neigh_groups[0],features[2])


# In[ ]:


stats_within_group(neigh_groups[0],features[3])


# ### *What has Manhattan got !*

# In[ ]:


correlation_within_groups(neigh_groups[1])


# In[ ]:


stats_within_group(neigh_groups[1],features[0])


# In[ ]:


stats_within_group(neigh_groups[1],features[1])


# In[ ]:


stats_within_group(neigh_groups[1],features[2])


# In[ ]:


stats_within_group(neigh_groups[1],features[3])


# ### *Hey Queens !!*

# In[ ]:


correlation_within_groups(neigh_groups[2])


# In[ ]:


stats_within_group(neigh_groups[2],features[0])


# In[ ]:


stats_within_group(neigh_groups[2],features[1])


# In[ ]:


stats_within_group(neigh_groups[2],features[2])


# In[ ]:


stats_within_group(neigh_groups[2],features[3])


# ### *Let's dig into the Staten Islands*

# In[ ]:


correlation_within_groups(neigh_groups[3])


# In[ ]:


stats_within_group(neigh_groups[3],features[0])


# In[ ]:


stats_within_group(neigh_groups[3],features[1])


# In[ ]:


stats_within_group(neigh_groups[3],features[2])


# In[ ]:


stats_within_group(neigh_groups[3],features[3])


# ### *Explore Bronx*

# In[ ]:


correlation_within_groups(neigh_groups[4])


# In[ ]:


stats_within_group(neigh_groups[4],features[0])


# In[ ]:


stats_within_group(neigh_groups[4],features[1])


# In[ ]:


stats_within_group(neigh_groups[4],features[2])


# In[ ]:


stats_within_group(neigh_groups[4],features[3])

