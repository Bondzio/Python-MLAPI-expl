#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# This is the third notebook in my series about machine learning. I previously wrote [ML Bootcamp: Intro to NumPy](https://www.kaggle.com/rafidka/ml-bootcamp-intro-to-numpy) and [Intro to Pandas](https://www.kaggle.com/rafidka/ml-bootcamp-intro-to-pandas). If you don't already know NumPy and pandas, you should still be able to follow this notebook and understand the basic ideas, though I still highly recommend that you read and experiment with the previous notebooks
# 
# In this notebook, I will take the reader through [matplotlib](https://matplotlib.org/), which is the most famous package for visualization in Python. Machine learning deals with a huge amount of data and without proper insignt into the data, it is hard to come up with something useful. `matplotlib` supports a variety of [plot types](https://matplotlib.org/gallery/index.html) which can be exteremely useful within machine learning and outside it.
# 
# For good visualization we need good data. As such, I will mostly be using [Stack Overflow Developer Survey for 2019](https://www.kaggle.com/mchirico/stack-overflow-developer-survey-results-2019) throughout this notebook, except at the beginning where I will be using elementary mathematical functions.

# # Loading the Data
# 
# 

# Let's start by loading the Stack Overflow Developer Survey so we could employ it in the subsequent sections.

# In[ ]:


import numpy as np
import pandas as pd

complete_survey = pd.read_csv("../input/stack-overflow-developer-survey-results-2019/survey_results_public.csv")
complete_survey_schema = pd.read_csv("../input/stack-overflow-developer-survey-results-2019/survey_results_schema.csv")


# Having load the complete survey, let's pick the some columns which are interesting to study:

# In[ ]:


survey = complete_survey[[
    'MainBranch',
    'Hobbyist',
    'OpenSourcer',
    'Employment',
    'Country',
    'Student',
    'EdLevel',
    'UndergradMajor',
    'DevType',
    'YearsCode',
    'Age1stCode',
    'YearsCodePro',
    'ConvertedComp',
    'LanguageWorkedWith',
    'Age',
    'Gender'
]]


# # Simple 2D Plots
# 
# Let's start with a simple 2D plot. We use NumPy to generate 50 equally spaced X values between `-2*Pi` and `2*Pi`, and then calculate the sine of those points to draw the sine function.

# In[ ]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
# Enable inline usage of matplotlib within the notebook. See for more information:
# https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-matplotlib 
get_ipython().run_line_magic('matplotlib', 'inline')

x1 = np.linspace(-2*np.pi, 2*np.pi, 50)
y1 = np.sin(x1)
plt.plot(x1, y1)
plt.show()


# # Multilpe 2D Plots
# 
# In many cases, we need to plot multiple graphs on the same plot. We can do that easily with matplotlib.

# In[ ]:


x2 = np.linspace(-2*np.pi, 2*np.pi, 50)
plt.plot(x2, np.sin(x2))
plt.plot(x2, np.cos(x2))
plt.show()


# As easy as that, just another call to the `plot` method and we have two graphs. However, we cannot easily tell which graph is for which function. We will see in the next section how we can enhance the graph by adding more features.

# # Enhancing Plots: Title, Labels, Legends, and Grid
# 
# Let's first add legends to the graph so we can distinguish which curve belong to which function:

# In[ ]:


x3 = np.linspace(-2*np.pi, 2*np.pi, 50)
plt.plot(x3, np.sin(x3), label='sin(x)') # Notice the additional label argument.
plt.plot(x3, np.cos(x3), label='cos(x)') # Notice the additional label argument.
plt.legend() # You need this call for the legends to show.
plt.show()


# The plot above is nice, especially that it was generated by 5 lines of code. However, it misses multiple features that would be really helpful:
# 
# 1. The plot misses a title; we want to let the reader knows what the plot is about.
# 2. The axes don't have labels. It is not clear what the horizontal and vertical axes represent.
# 3. Lack of grid makes it harder to estimate values at certain points.
# 
# With a few additional calls, we can add those features.
# 

# In[ ]:


x4 = np.linspace(-2*np.pi, 2*np.pi, 50)
plt.plot(x4, np.sin(x4), label='sin(x)')
plt.plot(x4, np.cos(x4), label='cos(x)')
plt.legend()
plt.title("Comparison of sine and cosine") # Add a title to the graph
plt.xlabel("x")                            # Add a label to the x-axis
plt.ylabel("sin(x)\ncos(x)")               # Add a label to the y-axis
plt.grid(True)                             # Enable grid
plt.show()


# # Further Enhancements to Plots: Plot Style, Figure Size and Axes Limits
# 
# We might also want to change the format of the graphs just to add more clarity. This can be particularly useful with plots containing multiple curves. Let's try to do this. While at it, let's also add two more functions to make the plot more sophisticated.

# In[ ]:


x5 = np.linspace(-2*np.pi, 2*np.pi, 50)

# Notice the additional 'linestyle' and 'color' args.
plt.plot(x5, np.sin(x5), linestyle='-', color='r', label='sin(x)')
plt.plot(x5, np.cos(x5), linestyle='--', color='g', label='cos(x)')
plt.plot(x5, x5**2, linestyle=':', color='b', label='x^2')          # Added the x-squared function.
plt.plot(x5, np.exp(x5), linestyle='-.', color='y', label='cos(x)') # Added the exp(x) function.

plt.legend()
plt.title("Comparison of sine, cosine, x^2, and exp(x)")
plt.xlabel("x")
plt.ylabel("""sin(x)
cos(x)
x^2
exp(x)""")
plt.grid(True)
plt.show()


# As you can see, by passing the `linestyle` and `color` optional arguments to the `plot()` method, we were able to format the curves differently. However, with the introduction of the exponetial function and `matplotlib` trying to guess the limits of the x- and y-axis, the sine and cosine functions are almost gone now. In such cases, we can manually specify those limits via the [xlim](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.xlim.html) and [ylim](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.ylim.html) functions. Let's also make the figure larger by employing the [figure](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib.pyplot.figure) method of [pyplot](https://matplotlib.org/api/pyplot_summary.html).

# In[ ]:


plt.figure(figsize=(10, 8))              # Made the graph larger as we have more functions now.
                                         # Notice that this call has to come before the calls to
                                         # the plot() methods, as this call instructs matplotlib
                                         # to start a new plot.
plt.xlim(-2*np.pi, 2*np.pi)              # Manually specifying the limits of the x and y axes.
plt.ylim(-5, 5)                          # This is necessary because the x^2 and the exp(x)
                                         # functions grow large quickly, making the sine and
                                         # cosine functions hard to notice.

# Notice the additional 'linestyle' and 'color' args.
plt.plot(x5, np.sin(x5), linestyle='-', color='r', label='sin(x)')
plt.plot(x5, np.cos(x5), linestyle='--', color='g', label='cos(x)')
plt.plot(x5, x5**2, linestyle=':', color='b', label='x^2')
plt.plot(x5, np.exp(x5), linestyle='-.', color='y', label='cos(x)')


plt.legend()
plt.title("Comparison of sine, cosine, x^2, and exp(x)")
plt.xlabel("x")
plt.ylabel("""sin(x)
cos(x)
x^2
exp(x)""")
plt.grid(True)
plt.show()


# ## Note About Formatting
# 
# If you find it too long to write the additional arguments for formatting, i.e. `color`, `linestyle`, etc., there is a third argument which you can pass (after the x and y arrays) which can combine multiple formatting styles in one value. For example, to specify a dotted green curve, you pass `'.g'` to the `plot()` method:
# 

# In[ ]:


x6 = np.linspace(-2*np.pi, 2*np.pi, 50)
plt.figure(figsize=(10, 8))              # Made the graph larger as we have more functions now.
                                         # Notice that this call has to come before the calls to
                                         # the plot() methods, as this call instructs matplotlib
                                         # to start a new plot.

# Notice the additional 'linestyle' and 'color' args.
plt.plot(x6, np.sin(x6), '.g', label='sin(x)')

plt.legend()
plt.title("Graph of sin(x)")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.grid(True)
plt.show()


# # Bar Charts
# 
# Having generated some nice 2D plots, let's move on to a different plot type: [bar chart](https://en.wikipedia.org/wiki/Bar_chart). Bar charts are very useful to visualize categoral data. For this, let's use some real data from the Stack Overflow Developer Survey.
# 
# To plot a bar chart with matplotlib, we need to use the [bar](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.bar.html#matplotlib.pyplot.bar) method. To get a basic understanding of how this works, let's see the following example:

# In[ ]:


plt.bar([1, 2, 3, 4], [10, 20, 30, 40])


# I am simply passing a list containing the numbers 1, 2, 3, and 4, which act as the categories of the plot, and then another sequence containing the height of each category, respectively.
# 
# Let's now move to a more realistic example. Say we want to plot the number of respondants in each age group. We can use pandas's [groupby](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html) method and find the [count](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.GroupBy.count.html#pandas.core.groupby.GroupBy.count) to find the count of each group.

# In[ ]:


survey_with_age = survey.dropna(subset=['Age']) # First, drop rows which don't have a value in Age
survey_by_age = survey_with_age.groupby(pd.cut(survey_with_age['Age'], np.arange(0, 101, 10)))['Age'].count()
survey_by_age


# In[ ]:


cats = list(map(lambda x: str(x), survey_by_age.index))
values = survey_by_age.values
plt.figure(figsize=(14, 8))
plt.bar(cats, values)


# # Multiple Bar Charts
# 
# It is sometimes useful to have multiple bar charts for better comparison. For example, taking the respondants from the top 15 countries, what is the number of developers who are actively contributing to open source vs those who are not? Let's try to plot this. First, let's examine the `OpenSourcer` column to see the possibly values:

# In[ ]:


survey['OpenSourcer'].unique()


# Let's use the value of `Once a month or more ofter` as a definition for actively contributing to open source, and the rest is an indicator of not actively contributing to open source.
# 
# Let's first find the countries with top respondants to this servey:

# In[ ]:


top_countries = survey.groupby('Country')['Country'].count().sort_values(ascending=False).head(10)
top_countries


# Next, let's filter the data frame to those countries only:

# In[ ]:


# Notice that we use .index to extract the country names, e.g. United States.
top_countries_names = top_countries.index
survey_top_countries = survey[survey['Country'].isin(top_countries_names)]

# verify that we indeed only has those countries.
survey_top_countries['Country'].unique()


# Next, let's filter the data frame even further to respondans which are either actively or not actively contributing to open source:

# In[ ]:


survey_top_countries_active_in_os = survey_top_countries[survey_top_countries['OpenSourcer'] == 'Once a month or more often']
survey_top_countries_inactive_in_os = survey_top_countries[survey_top_countries['OpenSourcer'] != 'Once a month or more often']


# Finally, let's find the values of the bar charts and plot them.

# In[ ]:


bar1_heights = survey_top_countries_active_in_os.groupby('Country')['Country'].count()[top_countries_names]
bar2_heights = survey_top_countries_inactive_in_os.groupby('Country')['Country'].count()[top_countries_names]

plt.figure(figsize=(14, 8))
plt.bar(top_countries_names, bar1_heights, color='orange')
plt.bar(top_countries_names, bar2_heights, color='blue')


# Hmm, we only see one graph! The reason is that we plotted the taller bars before the shorter. Let's swap the order of plot:

# In[ ]:


plt.figure(figsize=(14, 8))
plt.bar(top_countries_names, bar2_heights, color='blue')
plt.bar(top_countries_names, bar1_heights, color='orange')


# What if we want to the draw side adjacent to each others instead of overlapping? In this case, we need somoe manual processing here. Specifically:
# 
# 1. Instead of passing in categories, i.e. country names, as the first parameter to the `bar()` method, we pass x-coordinates. This way we can shift the bars to the left or right, depending on which set of bars we want to show.
# 
# 2. Now that we are passing in x-coordinates instead of the actual country names, we need to use the [set_xticks](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_xticks.html) and [set_xticklabels](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xticklabels.html).

# In[ ]:


plt.figure(figsize=(14, 8))

width = 0.4 # A width of 1.0 spans the whole area between two consecutive
            # tickts in the x-axis. Since we want to show two bars at each
            # tick, the width should be less than 0.5 for each bar so bars
            # from different tickts don't touch or overlap each other
x = np.arange(len(top_countries_names))
plt.bar(x - width/2, bar2_heights, width=width, color='blue') # left-shifted
plt.bar(x + width/2, bar1_heights, width=width, color='orange') # right-shifted

# Set the x-ticks and their labels.
ax = plt.axes()
ax.set_xticks(x)
ax.set_xticklabels(top_countries_names)

plt.show()


# One last thing we can do to improve the plot is to add legends:

# In[ ]:


plt.figure(figsize=(14, 8))

width = 0.4
x = np.arange(len(top_countries_names))
plt.bar(x - width/2, bar2_heights, width=width, color='blue',
        label="Not actively contributing to open source") # Add label
plt.bar(x + width/2, bar1_heights, width=width, color='orange',
        label="Actively contributing to open source") # Add label

# Set the x-ticks and their labels.
ax = plt.axes()
ax.set_xticks(x)
ax.set_xticklabels(top_countries_names)
plt.legend() # Enable legends

plt.show()


# # Pie Chart

# In[ ]:


survey['EdLevel'].unique()


# In[ ]:


survey_by_edlevel = survey.groupby('EdLevel')['EdLevel'].count().sort_values()
survey_by_edlevel = survey_by_edlevel * 100 / survey_by_edlevel.sum() # convert to percentages

labels = list(map(lambda x: str(x), survey_by_edlevel.index))
values = survey_by_edlevel.values

plt.figure(figsize=(14, 8))
plt.pie(values, labels=labels,
        explode=[0.1] * len(labels), # if the values here are non-zero, the slices of
                                     # the pie chart are moved away from the centre.
        autopct='%1.1f%%')           # tell matplotlib to print the percentages on the slices.


# # Heatmaps
# 
# In this section, we will demonstrate how to plot a [heat map](https://en.wikipedia.org/wiki/Heat_map). The way [a heat map is plotted using matplotlib](https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html) is with a little trick. matplotlib has a function called [imshow](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.imshow.html) which is used to display an image. So, to display a heat map, we could treat the values of the heat map matrix as an image (think a low resolution image). 
# 
# 

# In[ ]:


heatmap = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                    [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])


fig, ax = plt.subplots()
fig.set_size_inches(6, 6)
im = ax.imshow(heatmap)


# What if we want to annotate the blocks of the heat map with the values they represent? We can do that by calling the [text](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.text.html) method of `ax`. What if we want to add a color bar so we get a sense of the value of each color? We could use [colorbar](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.colorbar.html). As you can see, things are getting complicated quickly. Obviously, you could wrote your method for plotting a heat map with all required features and re-use it, but you don't have to since others have already done in other libraries that extend the functionality of matplotlib. One such library is [seaborn](https://seaborn.pydata.org/). Let's use its [heat map plotting](https://seaborn.pydata.org/generated/seaborn.heatmap.html) functionality:

# In[ ]:


import seaborn as sns;
plt.figure(figsize=(7, 6)) # increased the width to 7 compared to the
                           # previous code to account for the color bar
ax = sns.heatmap(heatmap)


# Notice that we got the color bar automatically. If we want to get annotation, we simply pass `annot=True`. We could also easily add labels 

# In[ ]:


import seaborn as sns;
plt.figure(figsize=(7, 6))
ax = sns.heatmap(heatmap, annot=True)


# As a practical application of heat maps on the Stack Overflow Developer Survey, let's plot the a heat map for open source contribution among the top countries with respect to the number of years coding. In other words, how likely are people to contribute based on their number of years coding?
# 
# Let's first see the different values of the `OpenSourcer` fields to know what what to make of it:

# In[ ]:


list(survey_top_countries['OpenSourcer'].unique()) # Converting to list to make it easier to read


# We need to convert this field to a numerical representation so we could plot a heat map. Let's map `Never` and `Less than once per year` to 0, map `Once a month or more ofter` to 12, i.e. at least 12 contributions a year, and `Less than once a month but more than once per year` to 6 (since it is more than once but less than 12 contributions a year, picking a value in the middle). Let's define this conversion function:

# In[ ]:


def map_os(value):
    return {
      'Never': 0,
      'Less than once per year': 0,
      'Less than once a month but more than once per year': 6,
      'Once a month or more often': 12,
    }[value]


# Next, let's inspect the value of the `YearsCode` field:

# In[ ]:


list(survey_top_countries['YearsCode'].unique()) # Converting to list to make it easier to read


# We can notice two things about this:
# 
# 1. It is not always numeric, e.g. `Less than 1 year`.
# 2. Even when it is numeric, it is still a string type.
# 
# Let's define a function to make this numeric:

# In[ ]:


def to_int(value):
    try:
        return int(value)
    except:
        return None


# With these, let's go ahead and create a pivot table for the 

# In[ ]:



survey_temp = survey_top_countries[['Country', 'YearsCode', 'OpenSourcer']].copy()
survey_temp['OpenSourcer'] = survey_temp['OpenSourcer'].transform(lambda x: map_os(x))
survey_temp['YearsCode'] = survey_temp['YearsCode'].transform(lambda x: to_int(x))
survey_temp = survey_temp[(survey_temp['YearsCode'] >= 1) & (survey_temp['YearsCode'] <= 20)]

ptable = survey_temp.pivot_table(
    index='Country',
    columns='YearsCode',
    values='OpenSourcer'
)

plt.figure(figsize=(14, 6))
sns.heatmap(ptable, annot=True)


# Notice that seaborn automatically used the values of the `Country` and `YearsCode` to set the labels. Such a graph in matplotlib would have required much more code. This is why you should always check whether there are helper functionalities in seaborn or similar libraries before implementing graphs in plain matplotlib.
# 

# # Multiple Plots
# 
# Before ending this notebook, I would like to talk about how to draw multiple plots within the same figure. The way this is done in matplotlib is via the [plt.subplot](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplot.html) method. This method instrurcts matplotlib that the upcoming plot-related instructions belong to particular subplot of the figure. The method accepts three parameters, one for the number of subplot rows in the figure, one for the number of subplot columns, and the last is for the index of the subplot currently being created starting from the top-left corner with index 1 and moving right. For example, the following call:
# ```Python
# plt.subplot(3, 3, 4)
# ```
# instruct matplotlib that our figure should have 3 rows and 3 columns of subplots, and that we are currently created the plot number of 4.
# 
# As a demonstration, let's modify our code at the beginning for plotting the sine function to draw multiple plots of the sine function, each having different frequency:

# In[ ]:


x1 = np.linspace(-2*np.pi, 2*np.pi, 200)
y1 = np.sin(x1)

plt.figure(figsize=(10, 6))

for i in range(1, 10):
    plt.subplot(3, 3, i)
    #plt.plot(x1, y1)
    plt.plot(x1, np.sin(i*x1))
plt.show()


# # Summary
# 
# I hope this gave you a taste of how to work with matplotlib. The number of different [kinds](https://matplotlib.org/gallery/index.html) of graphs you can do with matplotlib is huge, so this notebook is no way a representation of the power of matplotlib. Instead, I hope I managed to take you through the basics of matplotlib that, with a little googling or Stack Overflow reading, you could easily generate the plot type you need to visualize your data.
# 
# Another thing worth mentioning is that I focused on 2D plots here. It is frequently necessary to deal with 3D plots. However, the notebook is already long, so I thought I would refer you to [matplotlib 3D plotting tutorials](https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html) if you need such plots.
# 
# It is also worth pointing out that matplotlib is not the only visualization library in Python. In fact, there are [many more](https://www.anaconda.com/python-data-visualization-2018-why-so-many-libraries/) libraries and matplotlib is just one of them, though it is one of the oldest and most popular library and many other libraries build on top of it. One interesting library which extends matplotlib is [seaborn](seaborn.pydata.org) as mentioned in the section about heat maps. Another interesting library I came to know about recently is [altair](https://altair-viz.github.io/getting_started/installation.html).
# 

# In[ ]:




