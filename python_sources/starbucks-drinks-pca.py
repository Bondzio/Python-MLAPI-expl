#!/usr/bin/env python
# coding: utf-8

# # Introduction to Principal Component Analysis 
# I chose Starbucks drinks as my data because I thought, 'everyone loves food.' Also, because it has numerical nutrition data without any particular label, so it's unsupervised learning. A lot of the code is copied from [this python notebook](https://github.com/mGalarnyk/Python_Tutorials/blob/master/Sklearn/PCA/PCA_Data_Visualization_Iris_Dataset_Blog.ipynb).

# ### Import Libraries and Data

# In[ ]:


# Import a bunch of machine learning libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # plotting for the graphs at the end
from sklearn.decomposition import PCA # the principal component analysis
from sklearn.preprocessing import StandardScaler # scaling for the features

# Get the data
# In this case, I wrote out the feature names, because the first one was empty in the data
features = ['Drink', 'Calories', 'Fat (g)', 'Carb. (g)', 'Fiber (g)', 'Protein', 'Sodium']
# I skipped over the first row of the data, which had the features names, because I supplied my own
data = pd.read_csv('/kaggle/input/starbucks-menu/starbucks-menu-nutrition-drinks.csv', names=features, skiprows=1)
# Display the first couple of drinks
data.head()


# ### Clean Up Data

# In[ ]:


# x for the data, aka all the nutritional information
# y for the label I want to use in the graphs later, which I've chosen to be the drink name
cutoff_features = features[1:]
x_raw = data.loc[:, cutoff_features].values
y_raw = data.loc[:,['Drink']].values

# Let's remove all the rows with no data in them
# For example, Pink Drink only has '-' in all the features
x=[]
y=[]
for i, row in enumerate(x_raw):
    if '-' not in row:
        x.append(row)
        y.append(y_raw[i][0])

# df for data frame
x_df = pd.DataFrame(data = x, columns = cutoff_features)
y_df = pd.DataFrame(data = y, columns=['Drink'])
example_df = pd.concat([y_df, x_df], axis = 1)
# Show the first 10 drinks that have all the data
example_df.head(10)


# ### Standardize Data
# Make sure to [standardize your data](https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html)

# In[ ]:


# Standardize each feature according to its mean and standard deviation (aka z score or standard score)
x = StandardScaler().fit_transform(x)
pd.DataFrame(data = x, columns = cutoff_features).head()


# ### Perform Principal Component Analysis

# In[ ]:


# Do PCA, reduce down to 2 dimensions
pca = PCA(n_components=2)
principal_components = pca.fit_transform(x)

# Show the principal components for the first 5 drinks
# comp_df aka the data frame for the principal components
comp_df = pd.DataFrame(data = principal_components, columns = ['principal component 1', 'principal component 2'])
final_df = pd.concat([y_df, comp_df], axis = 1)
final_df.head(5)


# In[ ]:


print("First component explains {0:.0%} of variance".format(pca.explained_variance_ratio_[0]))
print("Second component explains {0:.0%} of variance".format(pca.explained_variance_ratio_[1]))


# # Let's Graph That!
# After doing all the math and setup for the principal components, I wanted to visualize how the drinks looked in the new coordinate space of the principal components. 
# To me, it looks like all the teas and coffees are in a line on the left. And then there's a cluster of mochas and machiattos in the bottom right. I find it funny how hot chocolate is all the way to the right. I suspect the difference is because of the presence of milk or fruit.

# ### Graph First 2 Principal Components

# In[ ]:


# Graph the first two principal components
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15) # Add x-axis label
ax.set_ylabel('Principal Component 2', fontsize = 15) # Add y-axis label
ax.set_title('Starbucks Drinks - 2 Principal Components', fontsize = 20) # Add overall title
ax.scatter(comp_df['principal component 1'], comp_df['principal component 2'], s = 50) # Add all the data points
ax.grid() # Add gridlines

#Annotate each data point
for i, txt in enumerate(y):
    # Annotate the datapoint (from comp_df) with the associated Drink name (from y)
    annot = ax.annotate(txt, (comp_df['principal component 1'][i],comp_df['principal component 2'][i]))
    annot.set_visible(False) # Default to not showing any annotations
    
    # Show only some of the annotations
    # Mainly a hacky way to do that, because there are too many labels and I didn't feel like doing extra work
    if i % 8 == 0:
        annot.set_visible(True)

# Show the graph
plt.show()


# # 3 Dimensions
# After seeing how the drinks looked like in two dimensions, I was curious how much information we'd gain by using three principal components instead of three. I start off by graphing it in 3d. Then I decided that I can't read 3d graphs and so made a bunch of 2d graphs.

# ### Perform Principal Component Analysis (with 3 pcs)

# In[ ]:


# Do PCA, reduce down to 3 dimensions
x = StandardScaler().fit_transform(x)
pca = PCA(n_components=3)
principal_components = pca.fit_transform(x)

# Show the principal components for the first 5 drinks
# comp_df aka the data frame for the principal components
comp_df = pd.DataFrame(data = principal_components, columns = ['pc1', 'pc2', 'pc3'])
final_df = pd.concat([y_df, comp_df], axis = 1)
final_df.head(5)


# In[ ]:


print("First component explains {0:.0%} of variance".format(pca.explained_variance_ratio_[0]))
print("Second component explains {0:.0%} of variance".format(pca.explained_variance_ratio_[1]))
print("Third component explains {0:.0%} of variance".format(pca.explained_variance_ratio_[2]))


# ### Graph PCs 1, 2, and 3

# In[ ]:


# Import the 3d projection so I can plot in 3 dimensions
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize = (8,8))
ax = fig.gca(projection='3d') # 3D graph
ax.set_xlabel('Principal Component 1', fontsize = 15) # Add x-axis label
ax.set_ylabel('Principal Component 2', fontsize = 15) # Add y-axis label
ax.set_zlabel('Principal Component 3', fontsize = 15) # Add z-axis label
ax.set_title('Starbucks Drinks - 3 Principal Components', fontsize = 20) # Add overall title
ax.scatter(comp_df['pc1'], comp_df['pc2'], comp_df['pc3'], s = 50) # Add all the data points
ax.grid() # Add gridlines

#Annotate each data point
for i, txt in enumerate(y):
    # Annotate the datapoint (from comp_df) with the associated Drink name (from y)
    # this time with three coordinates
    annot = ax.text(comp_df['pc1'][i],comp_df['pc2'][i], comp_df['pc3'][i], txt)
    annot.set_visible(False) # Default to not showing any annotations
    
    # Show only 'Iced Coffee' because I didn't want to put in the effort to be able to see all the labels
    if i == 4:
        annot.set_visible(True)
        
# Show the graph of PCs 1, 2, and 3
plt.show()


# ### Graph PCs 1 and 3

# In[ ]:


# PCs 1 and 3
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15) # Add x-axis label
ax.set_ylabel('Principal Component 3', fontsize = 15) # Add y-axis label
ax.set_title('Starbucks Drinks - 3 Principal Components (1 and 3)', fontsize = 20) # Add overall title
ax.scatter(comp_df['pc1'], comp_df['pc3'], s = 50)
ax.grid() # Add gridlines

#Annotate each data point
for i, txt in enumerate(y):
    # Annotate the datapoint (from comp_df) with the associated Drink name (from y)
    annot = ax.annotate(txt, (comp_df['pc1'][i],comp_df['pc3'][i]))
    annot.set_visible(False) # Default to not showing any annotations
    
    # Show only some of the annotations
    # Mainly a hacky way to do that, because there are too many labels and I didn't feel like doing extra work
    if i % 8 == 0:
        annot.set_visible(True)

# Show the graph for PCs 1 and 3
plt.show()


# ### Graph PCs 2 and 3

# In[ ]:


# PCs 2 and 3
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 2', fontsize = 15) # Add x-axis label
ax.set_ylabel('Principal Component 3', fontsize = 15) # Add y-axis label
ax.set_title('Starbucks Drinks - 3 Principal Components (2 and 3)', fontsize = 20) # Add overall title
ax.scatter(comp_df['pc2'], comp_df['pc3'], s = 50)
ax.grid() # Add gridlines

#Annotate each data point
for i, txt in enumerate(y):
    # Annotate the datapoint (from comp_df) with the associated Drink name (from y)
    annot = ax.annotate(txt, (comp_df['pc2'][i],comp_df['pc3'][i]))
    annot.set_visible(False)
    
    # Show only some of the annotations
    # Mainly a hacky way to do that, because there are too many labels and I didn't feel like doing extra work
    if i % 8 == 0:
        annot.set_visible(True)

# Show the graph for PCs 2 and 3
plt.show()

