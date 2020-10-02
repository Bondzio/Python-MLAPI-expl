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
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()


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


nRowsRead = 1000 # specify 'None' if want to read whole file
df1 = pd.read_csv('../input/cusersmarildownloadsmastercsv/master.csv', delimiter=';', nrows = nRowsRead)
df1.dataframeName = 'master.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


df1.head(5)


# In[ ]:


df1.shape


# In[ ]:


df1.info


# In[ ]:


df1.describe()


# In[ ]:


plotPerColumnDistribution(df1, 10, 5)


# In[ ]:


plotCorrelationMatrix(df1, 8)


# In[ ]:


plotScatterMatrix(df1, 15, 10)


# Thank's to Kaggle's bot. I'm just a copier and paster! 

# In[ ]:


df1.annee.describe()


# In[ ]:


df1.taux_de_chomage_national.describe()


# In[ ]:


df1.salaire_net_mensuel_median_national.describe()


# In[ ]:



print ("Skew is:", df1.salaire_net_mensuel_median_national.skew())
plt.hist(df1.salaire_net_mensuel_median_national, color='blue')
plt.show()


# In[ ]:


target = np.log(df1.salaire_net_mensuel_median_national)
print ("Skew is:", target.skew())
plt.hist(target, color='blue')
plt.show()


# In[ ]:


numeric_features = df1.select_dtypes(include=[np.number])
numeric_features.dtypes


# In[ ]:


corr = numeric_features.corr()

print (corr['salaire_net_mensuel_median_national'].sort_values(ascending=False)[1:11], '\n')
print (corr['salaire_net_mensuel_median_national'].sort_values(ascending=False)[-10:])


# In[ ]:


# How many unique features are there?

df1.secteur_indus.unique()


# In[ ]:



#Define a function which can pivot and plot the intended aggregate function 
def pivotandplot(data,variable,onVariable,aggfunc):
    pivot_var = data.pivot_table(index=variable,
                                  values=onVariable, aggfunc=aggfunc)
    pivot_var.plot(kind='bar', color='blue')
    plt.xlabel(variable)
    plt.ylabel(onVariable)
    plt.xticks(rotation=0)
    plt.show()


# In[ ]:


pivotandplot(df1,'secteur_indus','salaire_net_mensuel_median_national',np.median)


# In[ ]:


# numpy, matplotlib, seaborn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# It is a continous variable and hence lets look at the relationship of GrLivArea with SalePrice using a Regression plot

_ = sns.regplot(df1['secteur_indus'], df1['salaire_net_mensuel_median_national'])


# In[ ]:


df1 = df1.drop(df1[(df1['secteur_info']>4000) & (df1['salaire_net_mensuel_median_national']<300000)].index)
_ = sns.regplot(df1['secteur_info'], df1['salaire_net_mensuel_median_national'])


# SAGAR thank you so much. I copied your codes in Housing Prices competition for Kaggle learn users. So I left Saleprice in comments code above TO REMENBER ME that I'm just in a "copy level" kerneler (and sometimes I do it wrong, even doing ctrl+C plus ctrl+V)  

# It takes me "only" 1:38 min. to run these codes.
