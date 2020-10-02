#!/usr/bin/env python
# coding: utf-8

# **Is happiness getting what we don't have ?**
# 
# For my analysis I wanted to look at the premise of "Happiness can be gained from something we don't have".
# 
# If you do a quick check of the top 20 countries that think freedom or money is important to happiness. You'll see it's the countries that don't have a lot of freedom or money that rate these items highly important to happiness. 

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

df = pd.read_csv('../input/world-happiness-report-2019.csv')

# Print the top 20 countries that rate Freedom, then money key to happiness
print("Top 20 Countries that think Freedom IS key to Happiness\n")
print(df.nlargest(20,'Freedom').sort_values('Freedom',ascending=False)[["Freedom","Country (region)"]])

print("\n\nTop 20 Countries that think Money IS key to Happiness\n")
print(df.nlargest(20,'Log of GDP\nper capita').sort_values('Log of GDP\nper capita',ascending=False)[["Log of GDP\nper capita","Country (region)"]])


# 

# Going in the reverse direction, if we look at the top 20 countries that think money is NOT important to happiness, it's probably no surprise that it's all the countries with a high GNP.
# 
# So the old statement "Money Can't Buy You Happiness" depends on where you live.

# In[ ]:


print("Top 20 Countries that think money IS NOT key to Happiness\n")
print(df.nsmallest(20,'Log of GDP\nper capita').sort_values('Log of GDP\nper capita',ascending=True)[["Log of GDP\nper capita","Country (region)"]])


# 

# **Summary**
# 
# In this data set, it appears that the statement "*Happiness is getting what you don't have*" is probably true for poorer problem areas of the world. 
# 
# Countries with similiar economies and social/political climates should probably be grouped together to find common keys to happiness.
# 
# A common factor that could be independent of a country's wealth or political situation could be generousity. Studies have found that senior citizens that regularly do charity/generousity work typically lived long life and said that they were happier. However for this data set there didn't appear to be a strong corelation between happiness and generousity.

# In[ ]:


# Show a scatter plot of Generosity vs. Happiness
ax = df.plot(kind='scatter', x='Ladder', y= 'Generosity', title ="Generosity and Happiness", figsize=(15, 10), legend=True, fontsize=12)
ax.set_xlabel("Happiness", fontsize=12)
ax.set_ylabel("Generosity", fontsize=12)
plt.show()


# 
