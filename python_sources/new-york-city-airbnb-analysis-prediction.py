#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df_orig = pd.read_csv("../input/new-york-city-airbnb-open-data/AB_NYC_2019.csv")


# In[ ]:


df_orig.head(5)


# In[ ]:


df_orig.shape


# In[ ]:


df_orig.info()


# In[ ]:


df_orig.describe()


# 1. Price having minimum value as zero, maximum is higher seems to have more outliers
# 2. minimum_nights amount have much difference between min & max values also have outlier. But the 75% of values is upto 5 days so this seems to be an acceptable condition.

# In[ ]:


missing_values = df_orig.isnull().sum()
df_miss = pd.DataFrame(missing_values).rename(columns={0:'count'})
df_miss['percent'] = (missing_values / len(df_orig)) * 100
df_miss.loc[df_miss['count'] > 0]


# 1. last_review & review_per_month columns have equal number of missing values

# In[ ]:


print("Skew of price column:", df_orig['price'].skew())
print("Kurtosis of price column:", df_orig['price'].kurt())


# The target variable is skewed left, this will affect the prediction.

# In[ ]:


df_test_price = pd.DataFrame(np.log1p(df_orig['price']))
df_test_price.describe()


# 1. Price column have zero value to be avoided
# 2. Need to avoid the most outliers to get better result

# In[ ]:


#change the mean to median which will be right way
cond1=list(df_orig.loc[df_orig['price'] == 0, 'host_id'])

def fill_na_with_mode(ds, hostid):
    fill_value = np.int(ds.loc[ds['host_id'] == hostid]['price'].median())
    condit = ((ds['host_id'] == hostid) & (ds['price'] == 0))
    ds.loc[condit, 'price'] = fill_value

for h in cond1:
    fill_na_with_mode(df_orig, h)


# Replaced the zero values in price column, with median of the other properties of same "host_id"

# In[ ]:


zero_fill_neigh1 = np.int(df_orig.loc[(df_orig['neighbourhood'] == 'Williamsburg') & (df_orig['price'] > 0) & (df_orig['room_type'] == 'Entire home/apt')]['price'].mean())
zero_fill_neigh2 = np.int(df_orig.loc[(df_orig['neighbourhood'] == 'Murray Hill') & (df_orig['price'] > 0) & (df_orig['room_type'] == 'Entire home/apt')]['price'].mean())

#replaced the single zero value of neighbouhood 'williamsburg' with mean of other property
cond1 = (df_orig['price'] == 0) & (df_orig['neighbourhood'] == 'Williamsburg')
df_orig.loc[cond1, 'price'] = zero_fill_neigh1

#replaced the single zero value of neighbouhood 'Murray Hill' with mean of other property
cond2 = (df_orig['price'] == 0) & (df_orig['neighbourhood'] == 'Murray Hill')
df_orig.loc[cond2, 'price'] = zero_fill_neigh2


# In[ ]:


df_orig = df_orig[np.log1p(df_orig['price']) < 8]
df_orig = df_orig[np.log1p(df_orig['price']) > 3]


# * To reduce the skewness excluded values which are extreme outliers.

# In[ ]:


from scipy.stats import norm

plt.figure(figsize=(5,5))
sns.distplot(df_orig['price'], fit=norm)
plt.show()


# * After taking log the target variable is better distributed

# In[ ]:


df_orig.shape


# 1. About 100 outlier rows are removed

# In[ ]:


df_orig['last_review'] = df_orig['last_review'].fillna(0)
df_orig['reviews_per_month'] = df_orig['reviews_per_month'].fillna(0)


# 1. Replaced the NaN values in last review & reviews per month with zero, because the number of reviews is also zero for these rows. So the reivew may not be written hence replaced with zero. 

# In[ ]:


fig = plt.figure(figsize=(16,5))
fig.add_subplot(1,2,1)
p1 = sns.distplot(df_orig['latitude'])
p1.set_title('Latitude of listings')

fig.add_subplot(1,2,2)
p2 = sns.distplot(df_orig['longitude'])
p2.set_title('Longitude of listings')

plt.show()


# * Latitude is normally distributed than longitude

# In[ ]:


fig = plt.figure(figsize=(16,5))
fig.add_subplot(1,2,1)
p1 = sns.distplot(df_orig['minimum_nights'])
p1.set_title('Minimum nights stay')

fig.add_subplot(1,2,2)
p2 = sns.distplot(df_orig['availability_365'])
p2.set_title('Rooms availability')

plt.show()


# * Minimum nights is more skewed left.
# * The availablity days also not distiributed well

# In[ ]:


df_orig['minimum_nights'] = df_orig['minimum_nights'].apply(lambda x: 7 if x > 7 else x)


# * As found earlier let us fix a week (7 days) as the maximum value for this column.

# In[ ]:


non_availability = (len(df_orig[df_orig['availability_365'] == 0])/len(df_orig))*100
full_availability = (len(df_orig[df_orig['availability_365'] == 365])/len(df_orig))*100
print(f'Percent of rooms non availability: {non_availability:.2f}%')
print(f'Percent of rooms full availability : {full_availability:.2f}%')


# * Almost 35% of rooms are not available during this data collection, so it will affect the price
# * So let us fill categorical values as non_availability, full_availability, high_availability & low_availability.

# In[ ]:


df_orig['rooms_not_available'] = df_orig['availability_365'].apply(lambda x: 1 if x == 0 else 0)
df_orig['rooms_full_available'] = df_orig['availability_365'].apply(lambda x: 1 if x == 365 else 0)
df_orig['rooms_high_available'] = df_orig['availability_365'].apply(lambda x: 1 if x < 365 and x > 182 else 0)
df_orig['rooms_low_available'] = df_orig['availability_365'].apply(lambda x: 1 if x < 182 and x > 0 else 0)


# * Created 4 new columns based on rooms availability_365

# In[ ]:


fig = plt.figure(figsize=(18,5))
fig.subplots_adjust(wspace=0.2)
fig.add_subplot(1,3,1)
p1 = sns.distplot(df_orig['number_of_reviews'])
p1.set_title('Number of reviews')

fig.add_subplot(1,3,2)
p2 = sns.distplot(df_orig['reviews_per_month'])
p2.set_title('Reviews per month')

fig.add_subplot(1,3,3)
p3 = sns.distplot(df_orig['calculated_host_listings_count'])
p3.set_title('Total host listings count')

plt.show()


# * All the columns number of reviews, reviews per month & total host lisitings are not distributed well

# In[ ]:


factor = 3
num_review_ulimit = df_orig['number_of_reviews'].mean() + df_orig['number_of_reviews'].std() * factor
reviews_per_month_ulimit = df_orig['reviews_per_month'].mean() + df_orig['reviews_per_month'].std() * factor
calculated_host_list_ulimit = df_orig['calculated_host_listings_count'].mean() + df_orig['calculated_host_listings_count'].std() * factor


# * Calculated the upper limit of the 3 columns to remove outliers beyond the upper limit.
# * The lower limit will be 0

# In[ ]:


df_orig = df_orig[(df_orig['number_of_reviews'] < num_review_ulimit) & (df_orig['number_of_reviews'] >= 0)]
df_orig = df_orig[(df_orig['reviews_per_month'] < reviews_per_month_ulimit) & (df_orig['reviews_per_month'] >= 0)]
df_orig = df_orig[(df_orig['calculated_host_listings_count'] <= calculated_host_list_ulimit) & (df_orig['calculated_host_listings_count'] >= 0)]


# * Reduced the outlier by choosing the data in between the upper limit & lower limit

# In[ ]:


from datetime import date

df_orig['last_review'] = pd.to_datetime(df_orig.last_review, errors='coerce', format="%Y-%m-%d")
df_orig['last_review_year'] = df_orig['last_review'].dt.year
df_orig['last_review_month'] = df_orig['last_review'].dt.month
df_orig['last_review_dayofweek'] = df_orig['last_review'].dt.dayofweek


# * Created year, month & day of week columns from last_review date variable 

# In[ ]:


cond1 = (df_orig['last_review_year'] == 1970)
df_orig.loc[cond1,'last_review_dayofweek'] = 0
df_orig.loc[cond1,'last_review_month'] = 0
df_orig.loc[cond1,'last_review_year'] = 0


# * Removed the default year 1970 inserted for 0 in the last_review date column.

# In[ ]:


ext_corre = df_orig[['price','latitude', 'minimum_nights', 'number_of_reviews', 'reviews_per_month',
                    'calculated_host_listings_count', 'rooms_not_available', 'rooms_full_available',
                    'rooms_high_available', 'rooms_low_available', 'last_review_year', 'last_review_month','last_review_dayofweek']]
ext_corre = ext_corre.corr()
ext_corre


# In[ ]:


plt.figure(figsize = (18, 6))
# Heatmap of correlations
sns.heatmap(ext_corre, cmap = plt.cm.RdYlBu_r, vmin = -0.25, annot = True, vmax = 0.6)
plt.title('Correlation Heatmap')


# * last_review_year and last_review_month have correlation
# * number_of_reviews and reviews_per_month have correlation of 61%, we can use any one variable.
# * rooms_not_available and reviews_per_month have negative correlation, which means if room was not available more then reviews will be low.

# In[ ]:


fig = plt.figure(figsize=(16,6))
fig.subplots_adjust(wspace=0.2, hspace=0.2)
fig.add_subplot(1,2,1)
p1 = sns.countplot(x='room_type', data=df_orig)
p1.set_title('Room Type')

fig.add_subplot(1,2,2)
p2 = sns.countplot(x='neighbourhood_group', data=df_orig, hue='room_type')
p2.set_title('Neighbourhodd Groups')
plt.show()


# In[ ]:


fig = plt.figure(figsize=(16,6))

fig.add_subplot(1,2,1)
p1 = sns.boxplot(x=df_orig['room_type'], y=np.log1p(df_orig['price']))
p1.set_title('Room type vs Price')
p1.set_xlabel('Room Type')
p1.set_ylabel('Price')

fig.add_subplot(1,2,2)
p2 = sns.boxplot(x=df_orig['neighbourhood_group'], y=np.log1p(df_orig['price']))
p2.set_title('Neighbourhood Group vs Price')
p2.set_xlabel('Neighbourhood_group')
p2.set_ylabel('Price')

plt.show()


# In[ ]:


fig = plt.figure(figsize=(16,6))
fig.add_subplot(1,2,1)
p1 = sns.scatterplot(x=df_orig['number_of_reviews'], y=np.log1p(df_orig['price']))
p1.set_title('Reviews vs Price')
p1.set_xlabel('Reviews')
p1.set_ylabel('Price')

fig.add_subplot(1,2,2)
p2 = sns.boxplot(y=np.log1p(df_orig['calculated_host_listings_count']))
p2.set_title('Host listings')
p2.set_xlabel('host listing count')
plt.show()


# In[ ]:


total_host_listing = df_orig.groupby('neighbourhood_group')['calculated_host_listings_count'].sum()
total_host_listing = pd.DataFrame(total_host_listing).reset_index()
fig = plt.figure(figsize=(18,6))
fig.add_subplot(1,2,1)
p1 = sns.barplot(x=total_host_listing['neighbourhood_group'], y=total_host_listing['calculated_host_listings_count'])
p1.set_title('Neighbourhood_group and host listings count')

total_neighbourhood = df_orig.groupby('neighbourhood_group')['neighbourhood'].nunique()
total_neighbourhood = pd.DataFrame(total_neighbourhood).reset_index()
fig.add_subplot(1,2,2)
p2 = sns.barplot(x=total_neighbourhood['neighbourhood_group'], y=total_neighbourhood['neighbourhood'])
p2.set_title('Neighbourhood_group & total listed neigbourhoods')
p2.set_xlabel('neighbourhood_group')
p2.set_ylabel('total neighbourhood')
plt.show()


# In[ ]:


df_orig.groupby('neighbourhood')['calculated_host_listings_count'].sum()


# In[ ]:


def splitListingNeighbour(df, neighbourGroup):
    #Collecting host listings of neighbourhood group like 'Bronx'
    total_neighbour_listing = df.groupby(['neighbourhood_group', 'neighbourhood', 'room_type'])['calculated_host_listings_count'].sum()
    total_neighbour_listing = pd.DataFrame(total_neighbour_listing).reset_index()
    neigh_listing = total_neighbour_listing.loc[total_neighbour_listing['neighbourhood_group'] == neighbourGroup, ['neighbourhood','room_type','calculated_host_listings_count']]

    #Splitting the output of listings as each type of room
    neigh_type_df = neigh_listing.pivot_table('calculated_host_listings_count','neighbourhood','room_type')
    #conv_df.rename({'room_type':'neighbour'})
    neigh_type_df.reset_index(inplace=True)
    neigh_type_df = neigh_type_df.fillna(0)
    neigh_type_df['Entire home/apt'] = pd.to_numeric(neigh_type_df['Entire home/apt'])
    neigh_type_df['Private room'] = pd.to_numeric(neigh_type_df['Private room'])
    neigh_type_df['Shared room'] = pd.to_numeric(neigh_type_df['Shared room'])
    return neigh_type_df


# In[ ]:


'''''neighbour_list = ['Allerton','Baychester']
entire_home_apt = [39, 5]
private_room = [77, 7]
'''
def plotNeighbourListing(neigh_listing_room_type_df, neighbour_name):
    neighbour_list = list(neigh_listing_room_type_df['neighbourhood'])
    entire_home_apt = []
    private_room = []
    shared_room = []

    for i in neighbour_list:
        x = neigh_listing_room_type_df[neigh_listing_room_type_df['neighbourhood'] == i]
        entire_home_apt.append(int(x['Entire home/apt']))
        private_room.append(int(x['Private room']) + int(x['Entire home/apt']))
        shared_room.append(int(x['Shared room']) + int(x['Entire home/apt']) + int(x['Private room']))

    #colors = iter(sns.color_palette('Set1', n_colors=6, desat=.75))
    f,ax = plt.subplots(figsize=(9,20))
    sns.barplot(x=entire_home_apt, y=neighbour_list, color='blue', edgecolor='black', label='Entire home/apt')
    sns.barplot(x=private_room, y=neighbour_list, color='red', alpha=0.3, edgecolor='black', label='Private room')
    sns.barplot(x=shared_room, y=neighbour_list, color='white', alpha=0.2, edgecolor='black', label='Shared room')
    ax.legend(loc='lower right', frameon=True)
    ax.set(xlabel='Total type of listings', ylabel='neighbourhood', title='Total listings of neigbourhood group '+ neighbour_name)
    #sns.despine(left=True, bottom=True)
    plt.show()


# In[ ]:


bronx_type_df = splitListingNeighbour(df_orig, 'Bronx')
plotNeighbourListing(bronx_type_df, 'Bronx')


# In[ ]:


brooklyn_type_df = splitListingNeighbour(df_orig, 'Brooklyn')
plotNeighbourListing(brooklyn_type_df, 'Brooklyn')


# In[ ]:


manhattan_type_df = splitListingNeighbour(df_orig, 'Manhattan')
plotNeighbourListing(manhattan_type_df, 'Manhattan')


# In[ ]:


queens_type_df = splitListingNeighbour(df_orig, 'Queens')
plotNeighbourListing(queens_type_df, 'Queens')


# In[ ]:


staten_island_type_df = splitListingNeighbour(df_orig, 'Staten Island')
plotNeighbourListing(staten_island_type_df, 'Staten Island')


# In[ ]:


def boxplot_neighbourhood_price(df, neighbour_name):
    plt.figure(figsize=(9,18))
    p1 = sns.boxplot(x=df['price'], y=df['neighbourhood'])
    p1.set_title('Neigbourhood of Neigbourhood_group '+ neighbour_name +' vs price')
    p1.set_xlabel('Price')
    p1.set_ylabel('Neighbourhood')
    plt.show()


# In[ ]:


df_bronx_price = df_orig.loc[df_orig['neighbourhood_group'] == 'Bronx', ['neighbourhood', 'price']]
df_bronx_price = df_bronx_price.reset_index()
boxplot_neighbourhood_price(df_bronx_price, 'Bronx')


# In[ ]:


df_bronx_price = df_orig.loc[df_orig['neighbourhood_group'] == 'Brooklyn', ['neighbourhood', 'price']]
df_bronx_price = df_bronx_price.reset_index()
boxplot_neighbourhood_price(df_bronx_price, 'Brooklyn')


# In[ ]:


df_bronx_price = df_orig.loc[df_orig['neighbourhood_group'] == 'Manhattan', ['neighbourhood', 'price']]
df_bronx_price = df_bronx_price.reset_index()
boxplot_neighbourhood_price(df_bronx_price, 'Manhattan')


# In[ ]:


df_bronx_price = df_orig.loc[df_orig['neighbourhood_group'] == 'Queens', ['neighbourhood', 'price']]
df_bronx_price = df_bronx_price.reset_index()
boxplot_neighbourhood_price(df_bronx_price, 'Queens')


# In[ ]:


df_bronx_price = df_orig.loc[df_orig['neighbourhood_group'] == 'Staten Island', ['neighbourhood', 'price']]
df_bronx_price = df_bronx_price.reset_index()
boxplot_neighbourhood_price(df_bronx_price, 'Staten Island')


# 1. More outliers in neigbourhood price values 

# In[ ]:


df_orig.columns


# In[ ]:


df_orig['price'] = np.log1p(df_orig['price'])


# In[ ]:


df_x_cols = ['latitude','longitude','minimum_nights', 'number_of_reviews', 'reviews_per_month', 'calculated_host_listings_count', 
             'rooms_not_available', 'rooms_full_available', 'rooms_high_available', 'rooms_low_available', 'last_review_year', 
             'last_review_month','last_review_dayofweek','neighbourhood_group','room_type']
df_y_col = ['price'] 

df_x = df_orig[df_x_cols]
df_y = df_orig[df_y_col]


# 1. Seperated the both x & y columns

# In[ ]:


df_x_after_dummy = pd.get_dummies(df_x,columns=['neighbourhood_group','room_type'])
df_x_after_dummy = pd.get_dummies(df_x_after_dummy,drop_first=True)


# * converted the categorical features to numeric using pandas get_dummies
# * dropped neighbourhood column, because it was reducing the prediction score.

# In[ ]:


df_x_final = (df_x_after_dummy - df_x_after_dummy.mean()) / df_x_after_dummy.std()


# * Normalizing all the columns to maintain a equal range.

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

lm = LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(df_x_final, df_y, test_size=0.22, random_state=42)
reg = lm.fit(X_train, y_train)


# In[ ]:


y_predict = reg.predict(X_test)
y_predict


# In[ ]:


from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

mae = mean_absolute_error(y_test, y_predict)
mse = mean_squared_error(y_test, y_predict)
r2 = r2_score(y_test, y_predict)

print('Mean absolute error: ', mae)
print('Mean squared error:', mse)
print('r2 score:', r2)


# In[ ]:


reg.score(X_test,y_test)


# Thanks for reading.
# I'm a beginner, please provide your valuable suggestions/comments/improvements about the methods to improve better. 
