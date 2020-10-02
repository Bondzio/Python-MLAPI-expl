#!/usr/bin/env python
# coding: utf-8

# **Waffle chart:** Waffle chart is an interesting plot mainly used to display progress towards the goal. Github uses it to display daily efforts by its users. It has cells structure and can be used to display proportions as well ( as in the case of this visualization).<br><br>
# **About Data:** 
# * Year-wise Women Officers Commissioned in the Defence Forces from 2016 to 2018
# * Data Source: https://community.data.gov.in/women-officers-commissioned-in-the-defence-forces-during-2016-to-2018/
# 

# In[ ]:


# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches   
from matplotlib import cm


# In[ ]:


# Reading data in a dataframe
df = pd.read_csv("../input/indian-women-in-defense/WomenInDefense.csv")
df.head()


# In[ ]:


# Rename column
df.rename({'Army Medical Corps, Dental Corps & Military Nursing Service (Common for three forces)':"Others"}, axis=1, inplace=True)


# In[ ]:


# Setting index and Transpose
df=df.set_index('Year').T


# In[ ]:


# creating a column named Total for sum of all women officers commissioned in respective forces from 2016-2018
df['Total'] =  df.sum (axis = 1)
df


# creating Waffle Chart: Starts here...<br>
# * Calculate total women commissioned
# * find proportion of different categories wrt total value
# 

# In[ ]:


total_values = sum(df['Total'])
print("total values=",total_values)
each_prop = [(float(val) / total_values) for val in df['Total']]

for i, j in enumerate(each_prop):
    print (df.index.values[i] + ': ' + str(j))


# Define size of waffle chart,num_cells represents total number of cells in chart.

# In[ ]:


width = 40 
height = 5 

num_cells = width * height 
num_cells


# using the proportion of each category to determe it respective number of cells used for the category.

# In[ ]:


cells_each = [round(p * num_cells) for p in each_prop]

for i, cells in enumerate(cells_each):
    print (df.index.values[i] + ': ' + str(cells))


# creating a matrix that resembles the waffle chart and populating it.

# In[ ]:


chart = np.zeros((height, width))

item_index = 0
cell_index = 0

for col in range(width):
    for row in range(height):
        cell_index += 1

        if cell_index > sum(cells_each[0:item_index]):
            # ...proceed to the next category
            item_index += 1       
            
        # set the class value to an integer, which increases with class
        chart[row, col] = item_index
        
print ('Waffle chart populated!')


# Map the waffle chart matrix into a visual.

# In[ ]:


fig = plt.figure()
plt.matshow(chart)


# Prettify the chart.

# In[ ]:


fig = plt.figure()
colormap=plt.cm.plasma
plt.matshow(chart, cmap=colormap)

# get the axis
ax = plt.gca()

# set minor ticks
ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
ax.set_yticks(np.arange(-.5, (height), 1), minor=True)
    
# add gridlines based on minor ticks
ax.grid(which='minor', color="white")


# In[ ]:


values_cumsum = np.cumsum(df['Total'])
print(values_cumsum)


# In[ ]:


colormap(float(values_cumsum[0])/total_values)


# In[ ]:


for i, item in enumerate(df.index.values):
    label_str = item + ' (' + str(df['Total'][i]) + ')'
    color_val = colormap(float(values_cumsum[i])/total_values)
    print(label_str)
    print(color_val)


# Adding legend.

# In[ ]:


fig = plt.figure()
colormap= plt.cm.viridis
plt.matshow(chart, cmap= colormap)
ax = plt.gca()
ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
ax.set_yticks(np.arange(-.5, (height), 1), minor=True)
ax.grid(which='minor', color='w')
plt.colorbar()

values_cumsum = np.cumsum(df['Total'])
total_values = values_cumsum[len(values_cumsum) - 1]

# create legend
legend_handles = []
for i, item in enumerate(df.index.values):
    label_str = item + ' (' + str(df['Total'][i]) + ')'
    color_val = colormap(float(values_cumsum[i])/total_values)
    legend_handles.append(mpatches.Patch(color=color_val,label=label_str))

# add legend to chart
plt.legend(handles=legend_handles,
           bbox_to_anchor=(0, -0.5, 1, 0),
           loc='lower center', 
           ncol=len(df.index.values)
          )
plt.title("Women Officers Commissioned in the Defence Forces from 2016 to 2018",y=1.3)

