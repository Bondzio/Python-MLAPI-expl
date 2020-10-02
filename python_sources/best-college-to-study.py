import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import pyplot

from sklearn.preprocessing import LabelEncoder

#%matplotlib inline

college_type = pd.read_csv('../input/salaries-by-college-type.csv')
college_region = pd.read_csv('../input/salaries-by-region.csv')

#Combine the college data
cols = ['School Name','Region']
college_combined = pd.merge(left=college_type, right=college_region[cols], how='inner',on='School Name')
college_combined.head()

dollar_cols = ['Starting Median Salary','Mid-Career Median Salary']

for x in dollar_cols:
    college_combined[x] = college_combined[x].str.replace("$","")
    college_combined[x] = college_combined[x].str.replace(",","")
    college_combined[x] = pd.to_numeric(college_combined[x])
    
    
pivotinfo = pd.pivot_table(college_combined,index=['Region'],columns=['School Type'], values =['Starting Median Salary'])
colormap = pyplot.cm.cubehelix_r
sns.heatmap(pivotinfo, annot=True,  cmap=colormap)