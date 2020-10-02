#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install pandas-profiling')


# In[ ]:


# Imports
import numpy as np
import pandas as pd


# In[ ]:


# Read the training data
data = pd.read_csv("../input/eval-lab-2-f464/train.csv")


# In[ ]:


# Pandas profile
import pandas_profiling
data.profile_report(style={'full_width':True})


# In[ ]:


# Correlation heatmap
from seaborn import heatmap
heatmap(data.corr(), vmin=-1, vmax=+1, center=0.0)


# In[ ]:


# Separate out training and validation data
from sklearn.model_selection import train_test_split
X = data[["chem_1", "chem_4", "chem_6", "attribute"]]
y = data["class"]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.0000000001)
X_train.shape, X_val.shape, y_train.shape, y_val.shape


# In[ ]:


# Model : RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=2000).fit(X_train, y_train)


# In[ ]:


# Prediction
import csv
ids = pd.read_csv("../input/eval-lab-2-f464/test.csv")["id"]
X_test = pd.read_csv("../input/eval-lab-2-f464/test.csv")[["chem_1", "chem_4", "chem_6", "attribute"]]
y_pred = model.predict(X_test)
submission = open("submission.csv", "w+")
writer = csv.writer(submission)
writer.writerow(["id", "class"])
for i in range(len(y_pred)):
    writer.writerow([ids[i], y_pred[i]])
submission.close()


# Click <a href="submission.csv">here</a> to download submission file.
