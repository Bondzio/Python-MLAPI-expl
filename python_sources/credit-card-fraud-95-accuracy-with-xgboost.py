#!/usr/bin/env python
# coding: utf-8

# ## Import modules

# In[ ]:


import numpy as np
import pandas as pd

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style
from matplotlib.pyplot import plot

style.use("fivethirtyeight")
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', 'InlineBackend.figure_format = "retina"')


# ## Import data

# In[ ]:


df = pd.read_csv("/kaggle/input/creditcardfraud/creditcard.csv")


# In[ ]:


data_size_mb = df.memory_usage().sum() / 1024 / 1024
print("Data memory size: %.2f MB" % data_size_mb)


# ## Data exploration

# In[ ]:


df.head(5)


# In[ ]:


df.shape


# In[ ]:


df.info()


# In[ ]:


df.isnull().sum().sort_values(ascending = False).head(5)


# ## Data visualization

# ### Distribution of transaction class

# In[ ]:


plt.figure(figsize = (12,6))
df.groupby("Class").size().plot.bar()
plt.xticks(rotation = 360)
plt.title("Class of transactions")
plt.ylabel("Number of transactions")
plt.show()


# ### Balance the dataset

# In[ ]:


nofraud = df.loc[df.Class == 0]
fraud = df.loc[df.Class == 1]


# In[ ]:


print(nofraud.shape)
print(fraud.shape)


# In[ ]:


nofraud = nofraud.sample(738)


# In[ ]:


data = pd.concat([nofraud, fraud])
data.sample(frac = 1)
data.shape


# In[ ]:


plt.figure(figsize = (12,6))
data.groupby("Class").size().plot.bar()
plt.xticks(rotation = 360)
plt.title("Class of transactions (balanced)")
plt.ylabel("Number of transactions")
plt.show()


# ## Correlation

# In[ ]:


corr = data.corr()

plt.figure(figsize = (10,8))
sns.heatmap(corr, cmap = "coolwarm", linewidth = 2, linecolor = "white")
plt.title("Correlation")
plt.show()


# In[ ]:


upper = corr.where(np.triu(np.ones(corr.shape), k = 1).astype(np.bool))
to_drop = [column for column in upper.columns if any(upper[column] > 0.90)]
print(to_drop)


# In[ ]:


data = data.drop(["V17", "V18"], axis = 1)


# ## PCA

# In[ ]:


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

data["Time"] = scaler.fit_transform(data['Time'].values.reshape(-1,1))
data['Amount'] = scaler.fit_transform(data['Amount'].values.reshape(-1,1))

X = data.drop("Class", axis = 1)
Y = data["Class"]


# In[ ]:


from sklearn.decomposition import PCA

X_pca = scaler.fit_transform(X)

pca = PCA(n_components = 2)
X_pca_transformed = pca.fit_transform(X_pca)

plt.figure(figsize = (12,6))

for i in Y.unique():
    X_pca_filtered = X_pca_transformed[Y == i, :]
    plt.scatter(X_pca_filtered[:, 0], X_pca_filtered[:, 1], s = 30, label = i, alpha = 0.5)
    
plt.legend()
plt.title("PCA")
plt.show()


# ## Machine Learning

# In[ ]:


from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier


# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(X, 
                                                    Y, 
                                                    random_state = 0, 
                                                    test_size = 0.25)


# ### XGBoost

# In[ ]:


clf_xgb = XGBClassifier()

params = {"n_estimators" : [300, 500, 700],
          "learning_rate" : [0.005, 0.01, 0.05, 0.1],
          "max_depth" : [5, 7, 9],
          "max_features" : [3, 5, 7]}

gsc_xgb = GridSearchCV(clf_xgb, params, cv = 5) 
gsc_xgb = gsc_xgb.fit(X_train, Y_train)

print(gsc_xgb.best_estimator_)
clf_xgb = gsc_xgb.best_estimator_
clf_xgb.fit(X_train, Y_train)
print(round(clf_xgb.score(X_test, Y_test), 4))

