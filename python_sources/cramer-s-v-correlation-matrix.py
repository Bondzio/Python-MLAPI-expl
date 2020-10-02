#!/usr/bin/env python
# coding: utf-8

# # Cramer's V correlation matrix 

# We will see here how to create a matrix of correlation for categorical features with the Cramer's V

# **Dataset import**

# Source : https://www.kaggle.com/blastchar/telco-customer-churn

# In[ ]:


import pandas as pd
data = pd.read_csv("../input/telco-customer-churn/WA_Fn-UseC_-Telco-Customer-Churn.csv") 


# **Keeping of categorical features**

# In[ ]:


data = data[[i for i in data.columns if i not in ('customerID','Churn','tenure','MonthlyCharges', 'TotalCharges')]]

data.head()


# **Label encoding**

# In[ ]:


from sklearn import preprocessing

label = preprocessing.LabelEncoder()
data_encoded = pd.DataFrame() 

for i in data.columns :
  data_encoded[i]=label.fit_transform(data[i])


# In[ ]:


data_encoded.head()


# **Building of the Cramer's V function**

# In[ ]:


from scipy.stats import chi2_contingency
import numpy as np




def cramers_V(var1,var2) :
  crosstab =np.array(pd.crosstab(var1,var2, rownames=None, colnames=None)) # Cross table building
  stat = chi2_contingency(crosstab)[0] # Keeping of the test statistic of the Chi2 test
  obs = np.sum(crosstab) # Number of observations
  mini = min(crosstab.shape)-1 # Take the minimum value between the columns and the rows of the cross table
  return (stat/(obs*mini))


# **Building of the matrix**

# In[ ]:


rows= []

for var1 in data_encoded:
  col = []
  for var2 in data_encoded :
    cramers =cramers_V(data_encoded[var1], data_encoded[var2]) # Cramer's V test
    col.append(round(cramers,2)) # Keeping of the rounded value of the Cramer's V  
  rows.append(col)
  
cramers_results = np.array(rows)
df = pd.DataFrame(cramers_results, columns = data_encoded.columns, index =data_encoded.columns)



df


# **Add a heatmap to the matrix**

# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt



mask = np.zeros_like(df, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True




with sns.axes_style("white"):
  ax = sns.heatmap(df, mask=mask,vmin=0., vmax=1, square=True)

plt.show()

