#!/usr/bin/env python
# coding: utf-8

# In[ ]:


print("Kaggle Workshop")


# In[ ]:


import pandas as pd
gender_submission = pd.read_csv("../input/titanic/gender_submission.csv")
test = pd.read_csv("../input/titanic/test.csv")
train = pd.read_csv("../input/titanic/train.csv")

