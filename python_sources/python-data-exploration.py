#!/usr/bin/env python
# coding: utf-8

# Here is a simple exploratory data analysis of suicide rates in python using Seaborn, Pandas, and Matplot. This is my first ever Kernel so please leave criticisms and advice. Thanks! I will start by importing the required packages, setting the style of plotting I want to use, and printing the columns contained in the dataset after reading it in.

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from numpy import mean
plt.style.use('ggplot')
data = pd.read_csv('../input/suicide-rates-overview-1985-to-2016/master.csv')
data.columns


# I will rename the columns in the dataset for my ease of use and understandment.

# In[ ]:


data=data.rename(columns={'country':'Country',
                          'year':'Year',
                          'sex':'Sex',
                          'age':'Age',
                          'suicides_no':'SuicidesNo',
                          'population':'Population',
                          'suicides/100k pop':'Suicides100kPop',
                          'country-year':'CountryYear',
                          'HDI for year':'HDIForYear',
                          ' gdp_for_year ($) ':'GdpForYear',
                          'gdp_per_capita ($)':'GdpPerCapita',
                          'generation':'Generation'})


# Before we begin, we should check to see if there is any null data in our dataset that may cause problems...

# In[ ]:


data.isnull().sum()


# As you can see, there is no null data except for HDIForYear, which contains a lot of null data. Therefore I am gonna avoid using that column in my data exploration to make things easier on myself.

# Lets just start by looking at the top 10 countries with the highest average number of suicides. By looking at average instead of sum, I can work to avoid countries that don't have as many observations in our dataset...

# In[ ]:


df = data.groupby(['Country'])
df.SuicidesNo.mean().nlargest(10).plot(kind='barh')
plt.xlabel("Average Number of Suicides (1985-2015)")
plt.title("Top 10 Countries by No. of Suicides")

Here you can see that the Russian Federation has the largest average number of suicides; however, it's important to remeber that this is most likely largely coorelated to population. More people, a higher number of suicides. To get a clearer picture, lets look at the proportion between suicides per 100k people...
# In[ ]:


df = data.groupby(['Country'])
df.Suicides100kPop.mean().nlargest(10).plot(kind='barh')
plt.xlabel("Avg. Number of Suicides per 100k (1985-2015)")
plt.title("Top 10 Countries by Prop. of Suicides per 100k")


# This shows us that while the Russian Federation has the highest average number of suicides, Lithuania actually has the highest rate of Suicide, but due to it's low population, the number of suicides of low.

# Next, let's look at the relationship Sex has on suicide. Before we do this, we should make sure that the number of observations between Male and Female is the same. If we had much more observations on the male population, it would skew our data. Lets plot a bar graph on the value_counts function in pandas...

# In[ ]:


data['Sex'].value_counts().plot.bar()
plt.xlabel('Sex')
plt.ylabel('# of Observations')
plt.title('Number of Observations by Sex')


# As you can see, the number of observations is the same. Now we can begin our exploration.

# Let's start by using a pie chart to examine the differences of the proportions Men and Women have on the overall number of suicides observed.

# In[ ]:


df = data.groupby(['Sex'])
df.SuicidesNo.sum().plot(kind='pie', autopct='%1.1f%%', label='World Suicides by Sex')


# As this chart shows, Men make up over 75% of the population that commited suicide according to our dataset

# It would be interesting to look into this relationship more and see if it changes with age. We can use Seaborns catplot, with age set for column. Lets also make sure our column order goes from youngest to oldest to make our charts easier to understand...

# In[ ]:



sb.catplot(x='Sex', y='SuicidesNo', col='Age', data=data, estimator=mean, kind='bar', col_wrap=3, ci=False, col_order=['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years'])


# As you can see, this relationship doesn't remain constant for all age groups. The difference seems to be most prevelant during young and middleaged Men and Women.

# Lets also look to see if this relationship has remained constant over time. Using the seaborn barplot, we can examine the relationship between Year and Number of Suicides with a hue on Sex...

# In[ ]:


plt.figure(figsize=(35,15))
sb.set_context("paper", 2.5, {"lines.linewidth": 4})
sb.barplot(data=data,x='Year',y='SuicidesNo',hue='Sex', ci=False)


# It seems that this is a pretty constant relationship over time. It's also interesting to not that there appears to be more variance in Male suicides numbers over the years than Female.

# Lets use Seaborns lineplot to see if we can examine this relationship any clearer...

# In[ ]:


plt.figure(figsize=(30,10))
sb.lineplot(x='Year', y='SuicidesNo', data=data, hue='Sex', estimator=mean)


# This graph paints the same story as the bar chart. A constant relationship over the years.

# There is one more important thing we must do before we can really show that this relationship between Male and Female rates is true. We must look at the population difference of our observations. If we found at that the populations of Men we obsereved is much larger than the populations of Females we observed. It would make sense why the Number of Suicides is much larger for Men. Lets look at a line plot of the average populations of Male and Female across the observed years...

# In[ ]:


sb.lineplot(x='Year', y='Population', data=data, hue='Sex', estimator=mean, ci=False)


# As you can see, the population for Male observations is actually less than the Female observations on average. Making our the relationships should by our charts significant.
