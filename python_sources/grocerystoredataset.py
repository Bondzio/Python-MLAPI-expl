#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori


# In[ ]:


df = pd.read_csv('../input/supermarket/GroceryStoreDataSet.csv',names=['products'],header=None)
df.head()


# In[ ]:


df.values


# In[ ]:


data=[]
for i in range(len(df.products)):
    data.append(df["products"][i].split(","))


# In[ ]:


data[1]


# In[ ]:


te = TransactionEncoder()
te_data = te.fit(data).transform(data)
df = pd.DataFrame(te_data,columns=te.columns_)
df


# In[ ]:


frequent_itemsets = apriori(df,min_support=0.10, use_colnames=True)
frequent_itemsets


# In[ ]:


from mlxtend.frequent_patterns import association_rules
association_rules(frequent_itemsets, metric = "confidence", min_threshold = 0.4)


# In[ ]:


rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
rules


# In[ ]:


rules["antecedent_len"] = rules["antecedents"].apply(lambda x: len(x))
rules


# In[ ]:


rules[ (rules['antecedent_len'] >= 2) &
       (rules['confidence'] > 0.75) &
       (rules['lift'] > 1.2) ]

