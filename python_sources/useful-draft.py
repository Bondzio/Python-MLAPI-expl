#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 
import os


# In[ ]:


def load_data(base_dir):
    print(f"base_dir = {base_dir}")
    print(os.listdir(f"{base_dir}"))
    x_train = None
    for i in range(1, 5):
        filename = f"{base_dir}/x_train_{i}.npz"
        with np.load(filename) as data:
            print(f"files in {filename}: {data.files}")
            temp_data = data[data.files[0]]
            if x_train is None:
                x_train = temp_data
            else:
                x_train = np.concatenate((x_train, temp_data))


    with np.load(f'{base_dir}/y_train.npz') as data:
        print(f"files in {base_dir}/y_train.npz: {data.files}")
        y_train = data[data.files[0]]

    with np.load(f'{base_dir}/x_test.npz') as data:
        print(f"files in {base_dir}/x_test.npz: {data.files}")
        x_test = data[data.files[0]]
    return x_train, y_train, x_test


# In[ ]:


def save_submission(submission, name="prediction.csv"):
    result = pd.DataFrame(submission)
    result = result.rename({0: "Label", }, axis=1)
    result.index.name = "Id"
    result.index += 1
    result.to_csv(name)


# In[ ]:


x, y, t = load_data("../input")


# In[ ]:


# your code here


# In[ ]:


import catboost as cb


# In[ ]:


model = cb.CatBoostClassifier(loss_function="MultiClassOneVsAll", classes_count=5, task_type = "GPU")


# In[ ]:


model.fit(x[:1000], y[:1000])


# In[ ]:


submission = model.predict(t)


# In[ ]:


save_submission(submission)

