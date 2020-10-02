#!/usr/bin/env python
# coding: utf-8

# **[Data Visualization for All Micro-Course Home Page](https://www.kaggle.com/learn/data-viz-for-all)**
# 
# ---
# 

# ### Welcome to [Kaggle Learn](https://www.kaggle.com/learn/overview)'s _Data Visualization Made Easy_ micro-course!  
# In this hands-on micro-course, you'll learn how to take your data visualizations to the next level through the use of [seaborn](https://seaborn.pydata.org/index.html), a powerful but easy-to-use data visualization library.  To take a peek at some of the charts you'll make in this micro-course, check out the figures below!
# 
# ![tut1_plots_you_make](https://i.imgur.com/54BoIBW.png)
# 
# To use seaborn, you'll also learn a bit about how to write code in Python, a popular programming language.  That said,
# - **the micro-course is aimed at those with no prior programming experience**, and
# - each chart uses short and simple code, making seaborn much faster and easier to use than many other data visualization tools (_such as Excel, for instance_).  
# 
# So, if you've never written a line of code, and you want to learn the bare minimum to start making faster, more attractive plots today, you're in the right place! :)
# 
# In this first tutorial, you'll learn just enough Python to create your own professional looking **line charts**.  Then, in the following exercise, you'll put your new skills to work on a real-world dataset.  
# 
# _Note: If you have a strong background in Python (and Pandas), you might prefer to take our more advanced [Data Visualization micro-course](https://www.kaggle.com/learn/data-visualisation)._
# 
# # Set up the notebook
# 
# Take the time now to scroll quickly up and down this page.  You'll notice that there are a lot of different types of information on the page, including:
# 1. segments of code, 
# 2. figures containing line charts, and 
# 3. text (_like the text you're reading right now!_).
# 
# These pages are especially useful for organizing code, figures, and plots in a single place.  We refer to these pages as **Jupyter notebooks** (or, often just **notebooks**).  You're currently looking at a static version of a notebook that we have already created for you, and you will learn how to work with editable notebooks soon (_where you'll get a chance to run your own code!_).  
# 
# > In this notebook, we've already run all of the code for you, and any code output is printed directly below the code.
# 
# There are a few lines of code that you'll need to run at the top of every notebook to set up your coding environment.  **It's not important to understand these lines of code now**, and so we won't go into the details just yet.  We had to include them here, and if you'd like to take a look, you can do so by clicking on the "Code" button below this text.  (_To hide the code **after** making it visible, you need only click on the "Code" button once more._)

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
print("Setup Complete")


# # Select a dataset
# 
# In this course, with every new topic, you'll work with a different dataset.  The dataset for this tutorial tracks global daily streams on the music streaming service [Spotify](https://en.wikipedia.org/wiki/Spotify).  We focus on five popular songs from 2017 and 2018:
# 1. "Shape of You", by Ed Sheeran [(link)](https://en.wikipedia.org/wiki/Shape_of_You)
# 2. "Despacito", by Luis Fonzi [(link)](https://en.wikipedia.org/wiki/Despacito)
# 3. "Something Just Like This", by The Chainsmokers and Coldplay [(link)](https://en.wikipedia.org/wiki/Something_Just_like_This)
# 4. "HUMBLE.", by Kendrick Lamar [(link)](https://en.wikipedia.org/wiki/Humble_(song))
# 5. "Unforgettable", by French Montana [(link)](https://en.wikipedia.org/wiki/Unforgettable_(French_Montana_song))
# 
# The dataset is stored as a CSV file (*short for [comma-separated values](https://en.wikipedia.org/wiki/Comma-separated_values) file*).  Opening the CSV file in Excel shows a row for each date, along with a column for each song.  
# 
# ![tut1_spotify_head](https://i.imgur.com/GAGf6Td.png)
# 
# Notice that the first date that appears is January 6, 2017, corresponding to the release date of "The Shape of You", by Ed Sheeran.  And, using the table, you can see that "The Shape of You" was streamed 12,287,078 times globally on the day of its release.  Notice that the other songs have missing values in the first row, because they weren't released until later!
# 
# # Load the data
# 
# To open the dataset in the notebook, we'll use two distinct steps, implemented in the code cell below as follows:
# - begin by specifying the location (or [filepath](https://bit.ly/1lWCX7s)) where the dataset can be accessed, and then
# - use the filepath to load the contents of the dataset into the notebook.

# In[ ]:


# Path of the file to read
spotify_filepath = "../input/spotify.csv"

# Read the file into a variable spotify_data
spotify_data = pd.read_csv(spotify_filepath, index_col="Date", parse_dates=True)


# ![tut1_read_csv](https://i.imgur.com/18LKa03.png)
# 
# Note that the code cell above has **four** different lines of text.
# 
# ### Code comments
# 
# Two of the lines are preceded by a pound sign (`#`) and contain text that appears faded and italicized. 
# 
# Both of these lines are completely ignored by the computer when the code is run, and they only appear here so that any human who reads the code can quickly understand it.  We refer to these two lines as **code comments**, and it's good practice to include them to make sure that your code is readily interpretable.
# 
# ### Executable code
# 
# The other two lines are **executable code**, or code that is run by the computer (_in this case, to find and load the dataset_). 
# 
# The first line sets the value of `spotify_filepath` to the location where the dataset can be accessed.  In this case, we've provided the filepath for you (in quotation marks).  _Note that the **code comment** immediately above this line of **executable code** provides a quick description of what it does!_
# 
# The second line sets the value of `spotify_data` to contain all of the information in the dataset.  This is done with `pd.read_csv`.  It is immediately followed by three different pieces of text (underlined in the image above) that are enclosed in parentheses and separated by commas.  These are used to customize the behavior when the dataset is loaded into the notebook:
#  - `spotify_filepath` - The filepath for the dataset always needs to be provided first.
#  - `index_col="Date"` - When we load the dataset, we want each entry in the first column to denote a different row.  To do this, we set the value of `index_col` to the name of the first column (`"Date"`, found in cell A1 of the file when it's opened in Excel).
#  - `parse_dates=True` - This tells the notebook to understand the each row label as a date (as opposed to a number or other text with a different meaning).
#  
# These details will make more sense soon, when you have a chance to load your own dataset in a hands-on exercise.  For now, it's important to remember that **the end result of running both lines of code is that we can now access the dataset by using `spotify_data`**.
# 
# > You might have noticed that these lines of code don't have any printed output (whereas the lines of code you ran earlier in the notebook returned `Setup Complete` as output).  This is expected behavior -- not all code will return output, and this line is a prime example!
# 
# # Examine the data
# 
# Now, we'll take a quick look at the dataset in `spotify_data`, to make sure that it loaded properly.  
# 
# We print the _first_ five rows of the dataset by writing one line of code as follows:
# - begin with the variable containing the dataset (in this case, `spotify_data`), and then 
# - follow it with `.head()`.
# 
# You can see this in the line of code below.  

# In[ ]:


# Print the first 5 rows of the data
spotify_data.head()


# Check now that the first five rows agree with the image of the dataset (_from when we saw what it would look like in Excel_) above.
# 
# > Empty entries will appear as `NaN`, which is short for "Not a Number".
# 
# We can also take a look at the _last_ five rows of the data by making only one small change (where `.head()` becomes `.tail()`):

# In[ ]:


# Print the last five rows of the data
spotify_data.tail()


# Thankfully, everything looks about right, with millions of daily global streams for each song, and we can proceed to plotting the data!
# 
# # Plot the data
# 
# In this course, you'll learn about many different plot types.  In this tutorial, we'll focus on **line charts**.
# 
# _And the good news is_: once the dataset is loaded into the notebook, we need only one line of code to make a line chart!  

# In[ ]:


# Line chart showing daily global streams of each song 
sns.lineplot(data=spotify_data)


# As you can see above, the line of code is relatively short and has two main components:
# - `sns.lineplot` tells the notebook that we want to create a line chart.
# - `data=spotify_data` selects the data that will be used to create the chart.
# 
# Note that you will always use this same format when you create a line chart, and **_the only thing that changes with a new dataset is the name of the dataset_**.  So, if you were working with a different dataset named `financial_data`, for instance, the line of code would appear as follows:
# ```
# sns.lineplot(data=financial_data)
# ```
# 
# Sometimes there are additional details we'd like to modify, like the size of the figure and the title of the chart.  Each of these options can easily be set with a single line of code.

# In[ ]:


# Set the width and height of the figure
plt.figure(figsize=(14,6))

# Add title
plt.title("Daily Global Streams of Popular Songs in 2017-2018")

# Line chart showing daily global streams of each song 
sns.lineplot(data=spotify_data)


# The first line of code sets the size of the figure to `14` inches (in width) by `6` inches (in height).  To set the size of _any figure_, you need only copy the same line of code as it appears.  Then, if you'd like to use a custom size, change the provided values of `14` and `6` to the desired width and height.
# 
# The second line of code sets the title of the figure.  Note that the title must *always* be enclosed in quotation marks (`"..."`)!
# 
# # Plot a subset of the data
# 
# So far, you've learned how to plot a line for **_every_** column in the dataset.  In this section, you'll learn how to plot a **_subset_** of the columns.
# 
# We'll begin by printing the names of all columns.  This is done with one line of code and can be adapted for any dataset by just swapping out the name of the dataset (in this case, `spotify_data`).

# In[ ]:


list(spotify_data.columns)


# In the next code cell, we plot the lines corresponding to the first two columns in the dataset.

# In[ ]:


# Set the width and height of the figure
plt.figure(figsize=(14,6))

# Add title
plt.title("Daily Global Streams of Popular Songs in 2017-2018")

# Line chart showing daily global streams of 'Shape of You'
sns.lineplot(data=spotify_data['Shape of You'], label="Shape of You")

# Line chart showing daily global streams of 'Despacito'
sns.lineplot(data=spotify_data['Despacito'], label="Despacito")

# Add label for horizontal axis
plt.xlabel("Date")


# The first two lines set the title and size of the figure (_and should look very familiar!_).
# 
# The next two lines of code each add a line to the line chart.  For instance, consider the first one, which adds the line for "Shape of You":
# 
# ```python
# # Line chart showing daily global streams of 'Shape of You'
# sns.lineplot(data=spotify_data['Shape of You'], label="Shape of You")
# ```
# This line looks really similar to the code we used when we plotted every line in the dataset, but it has a few key differences:
# - Instead of setting `data=spotify_data`, we set `data=spotify_data['Shape of You']`.  In general, to plot only a single column, we use this format with putting the name of the column in single quotes and enclosing it in square brackets.  (_To make sure that you correctly specify the name of the column, you can print the list of all column names using the command you learned above._)
# - We also add `label="Shape of You"` to make the line appear in the legend and set its corresponding label.
# 
# The final line of code modifies the label for the horizontal axis (or x-axis), where the desired label is placed in quotation marks (`"..."`).
# 
# # What's next?
# 
# Put your new skills to work in the **[first coding exercise](https://www.kaggle.com/kernels/fork/2951524)**!

# ---
# **[Data Visualization for All Micro-Course Home Page](https://www.kaggle.com/learn/data-viz-for-all)**
# 
# 
