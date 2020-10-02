#!/usr/bin/env python
# coding: utf-8

# # 1. Import Packages and Load Titanic Dataset

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


# In[ ]:


df_train = pd.read_csv('/kaggle/input/titanic/train.csv')
df_test = pd.read_csv('/kaggle/input/titanic/test.csv')
id_train = df_train['PassengerId']
id_test = df_test['PassengerId']
df = pd.concat([df_train, df_test])
df = df.set_index('PassengerId')
df.info()
df


# # 2. Feature Engineering

# ## 2.1. One-Hot Encode Categorical Features

# In[ ]:


def category_to_one_hot(df, name_column):
    one_hot = pd.get_dummies(df[name_column], prefix=name_column, prefix_sep='-')
    df = pd.concat([df, one_hot], axis=1)
    df = df.drop(name_column, axis=1)
    return df, one_hot

def exclude_low_category(df, name_column, threshold_using_category):
    df_value_counts = df[name_column].value_counts()
    excluding_categories = df_value_counts.loc[df_value_counts < threshold_using_category].index
    for c in excluding_categories:
        df.loc[df[name_column] == c, name_column] = None
    return df


# ### 2.1.1. Pclass

# In[ ]:


name_column = 'Pclass'
print(df[name_column].value_counts(dropna=False))
df, one_hot = category_to_one_hot(df, name_column)
one_hot


# ### 2.1.2. Name

# In[ ]:


name_column = 'Name'
df[name_column] = df[name_column].str.extract(', (.*?\.) ')
print(df[name_column].value_counts(dropna=False))
df = exclude_low_category(df, name_column, 10)
print(df[name_column].value_counts(dropna=False))
df, one_hot = category_to_one_hot(df, name_column)
one_hot


# ### 2.1.3. Sex

# In[ ]:


name_column = 'Sex'
print(df[name_column].value_counts(dropna=False))
df, one_hot = category_to_one_hot(df, name_column)
one_hot


# ### 2.1.4. Ticket

# In[ ]:


name_column = 'Ticket'
df[name_column] = df[name_column].replace('( |^)[0-9]*', '', regex=True)
df[name_column] = df[name_column].replace('(/|\.).*', '', regex=True)
df.loc[df[name_column] == '', name_column] = None
print(df[name_column].value_counts(dropna=False))
df = exclude_low_category(df, name_column, 10)
print(df[name_column].value_counts(dropna=False))
df, one_hot = category_to_one_hot(df, name_column)
one_hot


# ### 2.1.5. Cabin

# In[ ]:


name_column = 'Cabin'
df['Cabin'] = df['Cabin'].replace(' .*', '', regex=True)
df['Cabin'] = df['Cabin'].replace('[0-9]*', '', regex=True)
print(df[name_column].value_counts(dropna=False))
df = exclude_low_category(df, name_column, 10)
print(df[name_column].value_counts(dropna=False))
df, one_hot = category_to_one_hot(df, name_column)
one_hot


# ### 2.1.6. Embarked

# In[ ]:


name_column = 'Embarked'
print(df[name_column].value_counts(dropna=False))
df, one_hot = category_to_one_hot(df, name_column)
one_hot


# ## 2.2. Standardize Numerical Features

# In[ ]:


def standardize_df(df, name_column):
    x = np.array(df.loc[df[name_column].notnull(), name_column])
    standardized_x = (x - x.mean()) / x.std(ddof=1)
    df.loc[df[name_column].notnull(), name_column] = standardized_x
    df.loc[df[name_column].isnull(), name_column] = 888
    return df


# ### 2.2.1. Age

# In[ ]:


name_column = 'Age'
df = standardize_df(df, name_column)
df[name_column]


# ### 2.2.2. SibSp

# In[ ]:


name_column = 'SibSp'
df = standardize_df(df, name_column)
df[name_column]


# ### 2.2.3. Parch

# In[ ]:


name_column = 'Parch'
df = standardize_df(df, name_column)
df[name_column]


# ### 2.2.4. Fare

# In[ ]:


name_column = 'Fare'
df = standardize_df(df, name_column)
df[name_column]


# ## 2.3. Get Dataset

# In[ ]:


df.info()
df_train = df.loc[id_train]
df_test = df.loc[id_test]


# # 3. Random Forest Modeling

# ## 3.1. Get X and y

# In[ ]:


name_class = 'Survived'
y_train = np.array(df_train[name_class])
X_train = np.array(df_train.drop(name_class, axis=1))
X_test = np.array(df_test.drop(name_class, axis=1))


# ## 3.2. Hyperparameter Tuning

# In[ ]:


param_grid = {
        'max_depth': [5, 10, 15],
        'min_samples_split': [10, 20, 30],
        'n_estimators': [100, 200, 300],
        'min_samples_leaf': [5, 10, 15],
        'n_jobs': [4],
        "bootstrap": [True],
        "criterion": ["entropy"]
    }
grid = GridSearchCV(estimator=RandomForestClassifier(random_state=0),
                    param_grid=param_grid,
                    scoring="accuracy",
                    cv=10)
grid.fit(X_train, y_train)
print(f"Best Score: {grid.best_score_}, Param: {grid.best_params_}")


# You can get all CV results with the code below.

# In[ ]:


# cv_results = grid.cv_results_
# for mean, std, param in zip(cv_results['mean_test_score'], cv_results['std_test_score'], cv_results['params']):
#     print(f"Mean: {mean}, Std: {std}, Param: {param}")


# ## 3.3. Prediction

# In[ ]:


best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)
y_pred = np.array(y_pred, dtype=np.int)


# # 4. Submission

# In[ ]:


submission_df = pd.DataFrame({'PassengerId': id_test, 'Survived': y_pred})
submission_df.to_csv('submission.csv', index=False)

