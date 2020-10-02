#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#%reset -f  
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt   
#%matplotlib  qt5
import os


# In[ ]:


#os.getcwd()
import seaborn as sns  
#path = "C:\\Backup\\My Documents\\My Documents\\Training\\Data ScienceAnalytics\\Python"


# In[ ]:


#os.chdir(path)
#df = pd.read_csv("superstore-data.zip", encoding = "ISO-8859-1")
df = pd.read_csv("../input/superstore_dataset2011-2015.csv", encoding = "ISO-8859-1")


# In[ ]:


df.shape


# In[ ]:


df.head()
df.columns
df.dtypes


# In[ ]:


#===============================================================================
#1. Who are the top-20 most profitable customers. Show them through plots.
#===============================================================================


# In[ ]:


result = df.groupby(["Customer Name"])['Profit'].aggregate(np.sum).reset_index().sort_values('Profit',ascending = False).head(20)


# In[ ]:


result.head
type(result)
result.shape
result
sns.barplot(x = "Customer Name",y= "Profit",data=result)


# In[ ]:


fig = plt.figure(figsize = (5,5))


# In[ ]:


ax1 = fig.add_subplot(111)
sns.barplot(x = "Customer Name",y= "Profit",
            data=result,
            ax = ax1
             )


# In[ ]:


ax1.set_ylabel("Profit", fontname="Arial", fontsize=12)


# In[ ]:


# Set the title to Comic Sans
ax1.set_title("Top 20 Customers", fontname='Comic Sans MS', fontsize=18)


# In[ ]:


# Set the font name for axis tick labels to be Comic Sans
for tick in ax1.get_xticklabels():
    tick.set_fontname("Comic Sans MS")
    tick.set_fontsize(12)
for tick in ax1.get_yticklabels():
    tick.set_fontname("Comic Sans MS")
    tick.set_fontsize(12)


# for tick in ax1.get_yticklabels():
#     tick.set_fontname("Comic Sans MS")
#     tick.set_fontsize(12)

# In[ ]:


# Rotate the labels as the Customer names overwrites on top of each other
ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 45)
plt.show()


# In[ ]:


#---Observations
## The top 3 customers in that order are Tamara Chand, Raymond Buch & Sanjit Chand


# In[ ]:


#=================================================================================
# 2. What is the distribution of our customer segment
#=================================================================================
descending_order = df['Segment'].value_counts().index


# In[ ]:


df.Segment.value_counts()


# In[ ]:


df['Segment'].unique()


# In[ ]:


sns.countplot("Segment", data = df, order = descending_order)


# In[ ]:


#---Observations
# Segment is categorical attribute with 3 levels - Consumer, Corporate & Home Office. The distribution is highest in Consumer
# followed by Corporate and Home Office


# In[ ]:


#=====================================================================================
#3. Who are our top-20 oldest customers
#=====================================================================================


# In[ ]:


df.dtypes.value_counts()


# In[ ]:


df.dtypes


# In[ ]:


df['Order Date'] = pd.to_datetime(df['Order Date'])


# In[ ]:


oldest = pd.DataFrame({'Count' : df.groupby(["Order Date","Customer Name"]).size()}).reset_index()


# In[ ]:


oldest.head(20)


# In[ ]:


# Top oldest customers are Annie Thurman, Eugene Moren, Joseph Holt, Toby Braunhardt, Dave Hallsten


# In[ ]:


#=========================================================================================
#4. Which customers have visited this store just once
#==========================================================================================


# In[ ]:


Customers_visit = pd.DataFrame({'Count' : df.groupby(["Customer Name"]).size()}).reset_index()


# In[ ]:


Customers_visit[Customers_visit['Count'] == 1]


# In[ ]:


#Since it returns an empty data frame, there are no customers that have visited this store just once


# In[ ]:


#==========================================================================================
#5. Relationship of Order Priority and Profit
df['Order Priority'].value_counts()

sns.boxplot(
            "Order Priority",
            "Profit",
             data= df
             )


# In[ ]:


#there does not appear to be any relationship between Order Priority & Profit


# In[ ]:


#6. What is the distribution of customers Market wise?
df.shape
df['Market'].value_counts()
Customers_market = pd.DataFrame({'Count' : df.groupby(["Market","Customer Name"]).size()}).reset_index()
Customers_market.shape


# In[ ]:


sns.barplot(x = "Market",     # Data is groupedby this variable
             y= "Count",    # Aggregated by this variable
             data=Customers_market
             )


# In[ ]:


sns.countplot("Market",        # Variable whose distribution is of interest
                data = Customers_market)


# In[ ]:


# Market has 7 levels. APAC has the largest # of customers followed by LATAM, and US in that order
 # Canada has the least # of customers


# In[ ]:


#7. What is the distribution of customers Market wise and Region wise
df['Region'].value_counts()
Customers_market_region = pd.DataFrame({'Count' : df.groupby(["Market","Region","Customer Name"]).size()}).reset_index()

sns.countplot("Market",        # Variable whose distribution is of interest
              hue= "Region",    # Distribution will be gender-wise
              data = Customers_market_region)


# In[ ]:


#for APAC, the largest # of customers are basd out of Oceania, followed by Southeast Asia
#for US, the largest # of customers are based out of Western Region followed by East


# In[ ]:


#8.Distribution of  Customers by Country & State - top 15
Customers_Country = pd.DataFrame({'Count' : df.groupby(["Country","State"]).size()}).reset_index().sort_values('Count',ascending = False).head(15)
Customers_Country

sns.barplot(x = "Country",     # Data is groupedby this variable
            y= "Count",  
            hue="State",
            data = Customers_Country.sort_values('Country')
            )
## US has the largest number of customers -California being the largest followed by New York, Washington, Illinois & Ohio
## UK has the next largest population of Customers -England


# In[ ]:


# Top 20 Cities by Sales Volume
sale_cities = df.groupby(["City"])['Quantity'].aggregate(np.sum).reset_index().sort_values('Quantity',ascending = False).head(20)
sns.barplot(x = "City",     # Data is groupedby this variable
            y= "Quantity",          
            data=sale_cities,
            )


# In[ ]:


# top 10 products
sale_Products = df.groupby(["Product Name"])['Quantity'].aggregate(np.sum).reset_index().sort_values('Quantity',ascending = False).head(20)
sns.barplot(x = "Product Name",     # Data is groupedby this variable
            y= "Quantity",          
            data=sale_Products)
#Staples is the largest selling product


# In[ ]:


# top selling products by countries (in US)
df.columns
sale_Products_Country = df.groupby(["Product Name","Country"])['Quantity'].aggregate(np.sum).reset_index().sort_values('Quantity',ascending = False)
sale_Products_Country = df.groupby(["Product Name","Country"])['Quantity'].sum().reset_index().sort_values('Quantity',ascending = False)
sale_Products_Country
type(sale_Products_Country)
spc = sale_Products_Country[sale_Products_Country['Country'] == "United States"].sort_values('Quantity',ascending = False).head(20)
sns.barplot(x = "Product Name",     # Data is groupedby this variable
            hue="Country",
            y= "Quantity",          
            data=spc)
# top selling products by countries (in US)
df.columns
sale_Products_Country = df.groupby(["Product Name","Country"])['Quantity'].aggregate(np.sum).reset_index().sort_values('Quantity',ascending = False)
sale_Products_Country = df.groupby(["Product Name","Country"])['Quantity'].sum().reset_index().sort_values('Quantity',ascending = False)
sale_Products_Country
type(sale_Products_Country)
spc = sale_Products_Country[sale_Products_Country['Country'] == "United States"].sort_values('Quantity',ascending = False).head(20)
sns.barplot(x = "Product Name",     # Data is groupedby this variable
            hue="Country",
            y= "Quantity",          
            data=spc)


# In[ ]:


# sales by product Category, Sub-category
sale_category = df.groupby(["Category","Sub-Category"])['Quantity'].aggregate(np.sum).reset_index().sort_values('Quantity',ascending = False)
sale_category
sns.barplot(x = "Category",     # Data is groupedby this variable
            hue="Sub-Category",
            y= "Quantity",          
            data=sale_category)

