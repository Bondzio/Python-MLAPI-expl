#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# Code below I received from my friend @dcstang.  Thanks David Tang.  

# In[ ]:


df1 = pd.read_csv('../input/cusersmarildownloadsresearcherscsv/researchers.csv', delimiter=';', encoding = "ISO-8859-1")
nRow, nCol = df1.shape
df1.dataframeName = 'researchers.csv'
f'There are {nRow} rows and {nCol} columns'


# In[ ]:


df1.head(5)


# In[ ]:


df1.info


# In[ ]:


df1.describe()


# In[ ]:


from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()


# Pie charts from Melih Kanbay @melihkanbay

# In[ ]:


labels=df1.time.value_counts().index
sizes=df1.time.value_counts().values
plt.figure(figsize=(11,11))
plt.pie(sizes,labels=labels,autopct="%1.f%%")
plt.title("time",size=25)
plt.show()


# In[ ]:


labels1=df1.country.value_counts().index
sizes1=df1.country.value_counts().values
plt.figure(figsize=(11,11))
plt.pie(sizes1,labels=labels1,autopct="%1.1f%%")
plt.title("country",size=25)
plt.show()


# In[ ]:


plotPerColumnDistribution(df1, 10, 5)


# In[ ]:


# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    filename = df.dataframeName
    df = df.dropna('columns') # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='g', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()


# In[ ]:


plotCorrelationMatrix(df1, 8)


# In[ ]:


# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()


# In[ ]:


plotScatterMatrix(df1, 15, 10)


# In[ ]:


df1.time.describe()


# In[ ]:


print ("Skew is:", df1.time.skew())
plt.hist(df1.time, color='green')
plt.show()


# In[ ]:


target = np.log(df1.time)
print ("Skew is:", target.skew())
plt.hist(target, color='pink')
plt.show()


# In[ ]:


numeric_features = df1.select_dtypes(include=[np.number])
numeric_features.dtypes


# In[ ]:


corr = numeric_features.corr()

print (corr['time'].sort_values(ascending=False)[1:11], '\n')
print (corr['time'].sort_values(ascending=False)[-10:])


# In[ ]:


df1.time.unique()


# In[ ]:


#Define a function which can pivot and plot the intended aggregate function 
def pivotandplot(data,variable,onVariable,aggfunc):
    pivot_var = data.pivot_table(index=variable,
                                  values=onVariable, aggfunc=aggfunc)
    pivot_var.plot(kind='bar', color='orange')
    plt.xlabel(variable)
    plt.ylabel(onVariable)
    plt.xticks(rotation=0)
    plt.show()


# In[ ]:


pivotandplot(df1,'time','time.1',np.median)


# In[ ]:


# numpy, matplotlib, seaborn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# It is a continous variable and hence lets look at the relationship of time with time.1 using a Regression plot

_ = sns.regplot(df1['time'], df1['time.1'])


# The codes below are from Fatih Bilgin. Thank you.

# In[ ]:


df1.plot(kind='scatter', x='time', y='time.1', alpha=0.5, color='darkblue', figsize = (12,9))
plt.title('time And time.1')
plt.xlabel("time")
plt.ylabel("time.1")
plt.show()


# In[ ]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_profiling as pp
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px


# In[ ]:


trace1 = go.Box(
    y=df1["time"],
    name = 'time',
    marker = dict(color = 'rgb(0,145,119)')
)
trace2 = go.Box(
    y=df1["time.1"],
    name = 'time.1',
    marker = dict(color = 'rgb(5, 79, 174)')
)

data = [trace1, trace2]
layout = dict(autosize=False, width=700,height=500, title='time', paper_bgcolor='rgb(243, 243, 243)', 
              plot_bgcolor='rgb(243, 243, 243)', margin=dict(l=40,r=30,b=80,t=100,))
fig = dict(data=data, layout=layout)
iplot(fig)


# In[ ]:


import matplotlib.pyplot as plt
plt.style.use(style='ggplot')
plt.rcParams['figure.figsize'] = (10, 6)


# In[ ]:


df1.plot(kind='scatter', x='time', y='indicator', alpha=0.5, color='mediumorchid', figsize = (12,9))
plt.title('time And indicator')
plt.xlabel("time")
plt.ylabel("indicator")
plt.show()


# In[ ]:


# libraries
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
# Dataset
df=pd.DataFrame({'X': range(1,101), 'Y': np.random.randn(100)*15+range(1,101), 'Z': (np.random.randn(100)*15+range(1,101))*2 })
 
# plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df1['indicator'], df1['time.1'], df1['time'], c='darkolivegreen', s=60)
ax.view_init(30, 185)
plt.show()


# In[ ]:


ax = sns.violinplot(x="time", y="time.1", data=df1, 
                    inner=None, color=".8")
ax = sns.stripplot(x="time", y="time.1", data=df1, 
                   jitter=True)
ax.set_title('time vs time.1')
ax.set_ylabel('time time.1')


# I still don't known how to play with violins, and a lot of other things too.
