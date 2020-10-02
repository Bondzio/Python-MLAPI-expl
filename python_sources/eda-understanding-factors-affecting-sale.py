#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv('../input/BlackFriday.csv')


# Importing Data to a pandas dataframe

# Before carrying out EDA on the dataset lets take a glimpse on the first 10 rows of the dataset.

# In[ ]:


print('Shape of dataframe--->',data.shape)
data.head(10)


# In[ ]:


data.info()


# Looks like there are missing values in 2 columns

# In[ ]:


print('Unique Values')
print('Product_Category_2--->',data['Product_Category_2'].unique())
print('Product_Category_3--->',data['Product_Category_3'].unique())


# Lets explore the dataset to see the factors affecting the sale of products and understand customer purchase behaviour

# In[ ]:


f,ax = plt.subplots(figsize=(9,6))
ax.set_title('Purchase amount distribution')
sns.distplot(data['Purchase'],ax=ax)


# Sale in the 5000 to 10000 dollars amount range are more frequent than others.

# In[ ]:


f, (ax1, ax2) = plt.subplots(1, 2,figsize=(19,6))
ax1.set_title('Purchase count in each age category')
order= data.groupby('Age').count().sort_values(by='Purchase',ascending=False).index
sns.countplot(x='Age', data=data ,ax=ax1,order=order)

ax2.set_title('Total sale in each age category')
df1 = data.groupby(['Age','Gender']).sum().sort_values(by='Purchase',ascending=False)
df1.reset_index(inplace=True)
sns.barplot(x='Age', y= 'Purchase',data=df1,hue='Gender',ax=ax2)
plt.legend()
#ax2.scatter(x, y)


# In[ ]:


f,ax = plt.subplots(2,2,figsize = (20,16))
ax[0][0].set_title('Total product sale in each occupation category')
df2 = data.groupby(['Occupation','Gender']).sum().sort_values(by='Purchase',ascending=False)
order = data.groupby('Occupation').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)

sns.barplot(y='Occupation', x= 'Purchase',orient='h',data=df2,hue='Gender',order=order,ax= ax[0][0])

ax[0][1].set_title('Average product sale in each occupation category')
df2 = data.groupby(['Occupation','Gender']).mean().sort_values(by='Purchase',ascending=False)
order = data.groupby('Occupation').mean().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)

sns.barplot(y='Occupation', x= 'Purchase',orient='h',data=df2,hue='Gender',order=order,ax = ax[0][1])

ax[1][0].set_title('Total product sale in each occupation category')
df2 = data.groupby(['Occupation','Marital_Status']).sum().sort_values(by='Purchase',ascending=False)
order = data.groupby('Occupation').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
sns.barplot(y='Occupation', x= 'Purchase',data=df2,orient='h',hue='Marital_Status',order=order,ax=ax[1][0])

ax[1][1].set_title('Average product sale in each occupation category')
df3 = data.groupby(['Occupation','Marital_Status']).mean().sort_values(by='Purchase',ascending=False)
order1 = data.groupby('Occupation').mean().sort_values(by='Purchase',ascending=False).index
df3.reset_index(inplace=True)
sns.barplot(y='Occupation', x= 'Purchase',data=df3,orient='h',hue='Marital_Status',order=order1,ax=ax[1][1])


# Unmarried male customers contribute most to the product sale across differnt occupations.
# Customers from Occupation category 4 contribute most to the overall total product sale however those from occupation category 17 contributes most on average. 

# In[ ]:


f,axes = plt.subplots(1,2,figsize=(15,4))

axes[0].set_title('Total product sale per gender category')
df1 = data.groupby(['Gender']).sum()
df1.reset_index(inplace=True)
sns.barplot(x='Gender', y= 'Purchase',data=df1,ax=axes[0])

axes[1].set_title('Average product sale per gender category')
df1 = data.groupby(['Gender']).mean()
df1.reset_index(inplace=True)
sns.barplot(x='Gender', y= 'Purchase',data=df1,ax=axes[1])


# In[ ]:


f,ax = plt.subplots(1,2,figsize=(19,6))
ax[0].set_title('Total product Sale across each product category')
df2 = data.groupby(['Product_Category_1']).sum().sort_values(by='Purchase',ascending=False)
order = data.groupby('Product_Category_1').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
sns.barplot(x='Product_Category_1', y= 'Purchase',data=df2,order=order,ax=ax[0])

ax[1].set_title('Average product Sale across each product category')
df2 = data.groupby(['Product_Category_1']).mean().sort_values(by='Purchase',ascending=False)
order = data.groupby('Product_Category_1').mean().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
sns.barplot(x='Product_Category_1', y= 'Purchase',data=df2,order=order,ax=ax[1])

f,ax = plt.subplots(figsize=(9,4))
ax.set_title('Frequency of products sold in each category')
order = data.groupby(by='Product_Category_1').count().sort_values(by='Purchase',ascending=False).index
sns.countplot('Product_Category_1',data=data,ax=ax,order=order)


# Products from category 1 contributes most to the overall total product sale while those from category 10 leads with the maximum average product sale.
# Products from product category 5 belong to the most frequently sold products. 

# In[ ]:


f,ax = plt.subplots(1,2,figsize=(15,4))
ax[0].set_title('Total sale comparison across marital status category')
df2 = data.groupby(['Marital_Status']).sum()
order = data.groupby('Marital_Status').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
sns.barplot(x='Marital_Status', y= 'Purchase',data=df2,order=order,ax=ax[0])

ax[1].set_title('Total sale comparison across different age category')
df2 = data.groupby(['Age']).sum()
order = data.groupby('Age').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
sns.barplot(x='Age', y= 'Purchase',data=df2,order=order,ax=ax[1])

f,ax = plt.subplots(1,2,figsize=(20,4))
ax[0].set_title('Total sale comparison across different age groups')
df2 = data.groupby(['Age','Marital_Status']).sum()
order = data.groupby('Age').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
sns.barplot(x='Age', y= 'Purchase',hue='Marital_Status',data=df2,order=order,ax=ax[0])

ax[1].set_title('Category wise Top 2 Age groups with maximum sale')
df1 = data.groupby(['Product_Category_1','Age']).sum().sort_values(by='Purchase',ascending=False)
df1.reset_index(inplace=True)
df2 = df1.groupby('Product_Category_1').head(2)
order = data.groupby(['Product_Category_1']).sum().sort_values(by='Purchase',ascending=False).index
sns.barplot(x = 'Product_Category_1',y='Purchase',order=order,data=df2,hue='Age',ax=ax[1])


# Unmarried customers in the 26-35 age group contribute most to the overall total product sale.

# In[ ]:


df2 = data.groupby(['Product_Category_1','Gender']).sum().sort_values(by='Purchase',ascending=False)
order = data.groupby('Product_Category_1').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
f,ax = plt.subplots(figsize=(9,6))
ax.set_title('Gender wise sale in each category')
sns.barplot(x='Product_Category_1', y= 'Purchase',data=df2,hue='Gender',order=order)


# Unmarried male customers in the 26-35 age group contribute most to the overall total product sale.

# In[ ]:


f,ax = plt.subplots(1,2,figsize=(15,4))
ax[0].set_title('Average sale comparison across different city categories')
df2 = data.groupby(['City_Category']).mean()
order = data.groupby('City_Category').mean().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
sns.barplot(x='City_Category', y= 'Purchase',data=df2,order=order,ax=ax[0])

ax[1].set_title('Total sale comparison across different city categories')
df2 = data.groupby(['City_Category']).sum()
order = data.groupby('City_Category').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
sns.barplot(x='City_Category', y= 'Purchase',data=df2,order=order,ax=ax[1])

f,ax = plt.subplots(1,2,figsize=(22,6))
df2 = data.groupby(['Product_Category_1','City_Category']).sum().sort_values(by='Purchase',ascending=False)
order = data.groupby('Product_Category_1').sum().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
ax[0].set_title('Total Sale across different city categories for each product category')
sns.barplot(x='Product_Category_1', y= 'Purchase',hue='City_Category',data=df2,order=order,ax=ax[0])

df2 = data.groupby(['Product_Category_1','City_Category']).mean()
order = data.groupby('Product_Category_1').mean().sort_values(by='Purchase',ascending=False).index
df2.reset_index(inplace=True)
ax[1].set_title('City Category wise Average revenue for each product category')
sns.barplot(x='Product_Category_1', y= 'Purchase',hue='City_Category',data=df2,order=order,ax=ax[1])


# Customers from B category city contribute most to the overall total sale while customers from C category city slightly leads with respect to the average sale of products.

# In[ ]:


f,ax= plt.subplots(1,2,figsize=(20,6))
ax[0].set_title('Total Sale across residents with varying years of stay')
df1 = data.groupby(['Stay_In_Current_City_Years']).sum()
order = data.groupby('Stay_In_Current_City_Years').sum().sort_values(by='Purchase',ascending=False).index
df1.reset_index(inplace=True)
sns.barplot(x='Stay_In_Current_City_Years', y= 'Purchase',data=df1,order=order,ax=ax[0])

ax[1].set_title('Length of residency in the city affecting sale')
df1 = data.groupby(['Product_Category_1','Stay_In_Current_City_Years']).sum().sort_values(by='Purchase',ascending=False)
df1.reset_index(inplace=True)
df2 = df1.groupby('Product_Category_1').head(2)
order = data.groupby(['Product_Category_1']).sum().sort_values(by='Purchase',ascending=False).index
sns.barplot(x = 'Product_Category_1',y='Purchase',order=order,data=df2,hue='Stay_In_Current_City_Years',ax=ax[1])


# Residents with 1 year of stay in city contribute most to the sale followed by residents with 2 years of stay. This is true across most products categories as well.
