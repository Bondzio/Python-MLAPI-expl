#!/usr/bin/env python
# coding: utf-8

# # Titanic : three lines of code for LB = 0.78947

# Before making predictions with complex algorithms, I tried to make it simple. 
# Immediate prediction - three lines of code based on three statements. This provides a LB of at least 80% of teams - Titanic Top 20%.
# After the code I have justified in the form of graphs (EDA), from which the statements are obvious.

# Thanks to:
# 
# https://www.kaggle.com/mylesoneill/tutorial-1-gender-based-model-0-76555
# https://nbviewer.jupyter.org/github/agconti/kaggle-titanic/blob/master/Titanic.ipynb
# https://www.kaggle.com/pavlofesenko/simplest-top-10-titanic-0-80861
# 

# In[ ]:


import pandas as pd
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn


# In[ ]:


# Preparatory part of the code
test = pd.read_csv('../input/titanic/test.csv') # load test dataset
test['fare'] = (test.Name.str.split().str[1] == 'Master.').astype('int')
submission = pd.DataFrame({'PassengerId': test['PassengerId'], 'Survived': pd.Series(dtype='int32')})

# Three lines of code for LB = 0.78947 (not less 80% teams - Titanic Top 20%) 
# Reasoning the statements see below (EDA)
test['Survived'] = [1 if (x == 'female') else 0 for x in test['Sex']]     # Statement 1
test.loc[(test.Fare == 1), 'Survived'] = 1                                 # Statement 2
test.loc[((test.Pclass == 3) & (test.Embarked == 'S')), 'Survived'] = 0   # Statement 3

# Saving the result
submission.Survived = test.Survived
submission.to_csv('submission_S_Boy_Sex.csv', index=False)


# # Reasoning (EDA)

# ### Statement 1. Women all survived and men all died

# In[ ]:


# Reasoning for Statement 1 
# Thanks for the idea to: https://www.kaggle.com/mylesoneill/tutorial-1-gender-based-model-0-76555 
# Thanks for the idea of plot to: https://www.kaggle.com/pavlofesenko/simplest-top-10-titanic-0-80861
import matplotlib.pyplot as plt

def highlight(value):
    if value >= 0.5:
        style = 'background-color: palegreen'
    else:
        style = 'background-color: pink'
    return style

train = pd.read_csv('../input/titanic/train.csv') # load train dataset
pd.pivot_table(train, values='Survived', index=['Sex']).style.applymap(highlight)


# ![](http://) Statement 2. o('Master') from the 1-2 all the fare survived

# In[ ]:


# Reasoning for Statement 2
# Thanks for the plot to: https://www.kaggle.com/pavlofesenko/simplest-top-10-titanic-0-80861
train['fare'] = (train.Name.str.split().str[1] == 'Master.').astype('int')
pd.pivot_table(train, values='Survived', index='Pclass', columns='Fare').style.applymap(highlight)


# ### Statement 3. Everybody from the class 3 cabins that were sat in Southampton ('S') were died

# In[ ]:


# Reasoning for Statement 3
# Thanks for the plot to: https://www.kaggle.com/pavlofesenko/simplest-top-10-titanic-0-80861
pd.pivot_table(train, values='Survived', index=['Pclass', 'Embarked'], columns='Sex').style.applymap(highlight)

