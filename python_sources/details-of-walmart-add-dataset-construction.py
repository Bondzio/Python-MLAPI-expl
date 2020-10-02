#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from tqdm import tqdm
import gc


# In[ ]:


#============================#
def get_cat(inp):
    tokens = inp.split("_")
    return tokens[0]
#============================#
def get_dept(inp):
    tokens = inp.split("_")
    return tokens[0] + "_" + tokens[1]
#============================#


# ### Building all the aggregation levels

# In[ ]:


l12 = pd.read_csv("../input/m5-forecasting-uncertainty/sales_train_evaluation.csv")
l12.id = l12.id.str.replace('_evaluation', '')


# In[ ]:


COLS = [f"d_{i+1}" for i in range(1941)]


# In[ ]:


get_ipython().run_cell_magic('time', '', 'print("State & Item")\nl11 = l12.groupby([\'state_id\',\'item_id\']).sum().reset_index()\nl11["store_id"] = l11["state_id"]\nl11["cat_id"] = l11["item_id"].apply(get_cat)\nl11["dept_id"] = l11["item_id"].apply(get_dept)\nl11["id"] = l11["state_id"] + "_" + l11["item_id"]\nprint("Item")\nl10 = l12.groupby(\'item_id\').sum().reset_index()\nl10[\'id\'] = l10[\'item_id\'] + \'_X\'\nl10["cat_id"] = l10["item_id"].apply(get_cat)\nl10["dept_id"] = l10["item_id"].apply(get_dept)\nl10["store_id"] = \'X\'\nl10["state_id"] = \'X\'\nprint("Store & Dept")\nl9 = l12.groupby([\'store_id\',\'dept_id\']).sum().reset_index()\nl9["cat_id"] = l9["dept_id"].apply(get_cat)\nl9["state_id"] = l9["store_id"].apply(get_cat)\nl9["item_id"] = l9["dept_id"]\nl9["id"] = l9["store_id"] + \'_\' + l9["dept_id"]\nprint("Store & Cat")\nl8 = l12.groupby([\'store_id\',\'cat_id\']).sum().reset_index()\nl8[\'dept_id\'] = l8[\'cat_id\']\nl8[\'item_id\'] = l8[\'cat_id\']\nl8[\'state_id\'] = l8[\'store_id\'].apply(get_cat)\nl8["id"] = l8["store_id"] + \'_\' + l8["cat_id"]\nprint("State & Dept")\nl7 = l12.groupby([\'state_id\',\'dept_id\']).sum().reset_index()\nl7["store_id"] = l7["state_id"]\nl7["cat_id"] = l7["dept_id"].apply(get_cat)\nl7["item_id"] = l7["dept_id"]\nl7["id"] = l7["state_id"] + \'_\' + l7["dept_id"]\nprint("State & Cat")\nl6 = l12.groupby([\'state_id\',\'cat_id\']).sum().reset_index()\nl6["store_id"] = l6["state_id"]\nl6["dept_id"] = l6["cat_id"]\nl6["item_id"] = l6["cat_id"]\nl6["id"] = l6["state_id"] + "_" + l6["cat_id"]\nprint("Dept")\nl5 = l12.groupby(\'dept_id\').sum().reset_index()\nl5["cat_id"] = l5["dept_id"].apply(get_cat)\nl5["item_id"] = l5["dept_id"]\nl5["state_id"] = "X"\nl5["store_id"] = "X"\nl5["id"] = l5["dept_id"] + "_X"\nprint("Cat")\nl4 = l12.groupby(\'cat_id\').sum().reset_index()\nl4["store_id"] = l4["cat_id"]\nl4["item_id"] = l4["cat_id"]\nl4["store_id"] = "X"\nl4["state_id"] = "X"\nl4["id"] = l4["cat_id"] + "_X"\nprint("Store")\nl3 = l12.groupby(\'store_id\').sum().reset_index()\nl3["state_id"] = l3["store_id"].apply(get_cat)\nl3["cat_id"] = "X"\nl3["dept_id"] = "X"\nl3["item_id"] = "X"\nl3["id"] = l3["store_id"] + "_X"\nprint("State")\nl2 = l12.groupby(\'state_id\').sum().reset_index()\nl2["store_id"] = l2["state_id"]\nl2["cat_id"] = "X"\nl2["dept_id"] = "X"\nl2["item_id"] = "X"\nl2["id"] = l2["state_id"] + "_X"\nprint("Total")\nl1 = l12[COLS].sum(axis=0).values\nl1 = pd.DataFrame(l1).T\nl1.columns = COLS\nl1["id"] = \'Total_X\'\nl1[\'state_id\'] = \'X\'\nl1[\'store_id\'] = \'X\'\nl1[\'cat_id\'] = \'X\'\nl1[\'dept_id\'] = \'X\'\nl1[\'item_id\'] = \'X\'')


# In[ ]:


df = pd.DataFrame()
df = df.append([l12, l11, l10, l9, l8, l7, l6, l5, l4, l3, l2, l1])


# In[ ]:


sub = pd.read_csv("../input/m5-forecasting-uncertainty/sample_submission.csv")
sub['id'] = sub.id.str.replace('_evaluation', '')
grps =sub.iloc[-42840:, 0].unique()
grps = [col.replace("_0.995","") for col in grps]


# In[ ]:


for col in ['id','item_id','dept_id','cat_id','store_id','state_id']:
    print(col, df[col].nunique())


# In[ ]:





# ## Computing scale and start date

# In[ ]:


X = df[COLS].values
x = (X>0).cumsum(1)
x = x>0
st = x.argmax(1)
den = 1941 - st - 2
diff = np.abs(X[:,1:] - X[:,:-1])
norm = diff.sum(1) / den


# In[ ]:


df["start"] = st
df["scale"] = norm


# In[ ]:


df.tail(5)


# In[ ]:


plt.plot(X[-1]/norm[-1])
plt.show()


# In[ ]:


df.to_csv("sales.csv", index=False)


# In[ ]:




