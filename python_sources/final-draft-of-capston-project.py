#!/usr/bin/env python
# coding: utf-8

# ## Importing Libraries

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


#Loading necessary packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori 
from mlxtend.preprocessing import TransactionEncoder

# Warnings
# import warnings
# warnings.filterwarnings('ignore')

# Style
sns.set(style='darkgrid')
plt.rcParams["patch.force_edgecolor"] = True


# ### DATA CLEANING

# In[ ]:


groceries=pd.read_csv("/kaggle/input/groceriesdata/Groceries.csv",header=None) #reading data
groceries.shape


# In[ ]:


groceries.dropna(how="all",inplace=True) #drop rows with all missing values
groceries.shape


# In[ ]:



groceries.tail() #column 9001 has values in between


# In[ ]:


groceries.loc[9001,:] = groceries.loc[9001,:].shift(-26) #shifting the values to left
groceries.tail()


# In[ ]:


# Converting dataframe into list of lists
records=[]
for i in range (0,7835):
    records.append([str(groceries.values[i,j]) for j in range (0,32)])
records=np.array(records)
print(records.shape)
print(records[:2])


# In[ ]:


#deleteing the missing values
new_record=[]
for j in records:
    j=[j for j in j if str(j) != 'nan']
    new_record.append(j)
new_record[:2]


# In[ ]:


#Converting entire data into a single list to plot frequency of each item
b=[j for i in records for j in i]
b=[b for b in b if str(b)!='nan']
print(b[:2])  
print(len(b)) 


# ## Question 1
# 
# 
# # DATA VISUALIZATION

# In[ ]:


#Frequency Plot
plt.rcParams['figure.figsize'] = (18, 7)
color = plt.cm.ocean(np.linspace(0, 1, 40))
pd.DataFrame(b)[0].value_counts().head(20).plot.bar(color = color)
plt.title('Frequency Plot for Top 20 Products', fontsize = 30)
plt.xticks(rotation = 90 ,fontsize=20)
plt.grid(b=False)
plt.show()


# ### TREE MAP

# In[ ]:


y = pd.DataFrame(b)[0].value_counts().head(50).to_frame()
y.index
import squarify
plt.rcParams['figure.figsize'] = (20, 20)
color = plt.cm.cool(np.linspace(0, 1, 50))
squarify.plot(sizes = y.values, label = y.index, alpha=.8, color = color)
plt.title('Tree Map for top 50 Popular Items',fontsize=30)
plt.axis('off')
plt.savefig('books_read.png')
plt.show()


# In[ ]:


groceries["frequency"] = groceries.notnull().sum(axis=1)
groceries["frequency"].head()


# In[ ]:


plt.rcParams['figure.figsize'] = (18, 7)
color = plt.cm.rainbow(np.linspace(0, 1, 40))
groceries["frequency"].value_counts().plot.bar(color = color)
plt.title('Product frequency per transaction', fontsize = 30)
plt.xticks(rotation = 45 ,fontsize=15)
plt.grid(b=False)
plt.show()


# In[ ]:


groceries.drop("frequency",axis=1,inplace=True)


# In[ ]:


te = TransactionEncoder()
groceries = te.fit(new_record).transform(new_record)
groceries = pd.DataFrame(groceries, columns = te.columns_)
groceries.head()


# In[ ]:


groceries.drop('`',axis=1,inplace=True) #false entry in data


# # Question 2 
# ## FILTERING TRANSACTIONS
# 

# In[ ]:


from mlxtend.frequent_patterns import apriori

#Now, let us return the items and itemsets with suitable support:
rule_size = []
for i in np.arange(0.01,0.1,0.005):
    rule = apriori(groceries, min_support = i, use_colnames = True)
    size=rule.shape[0]
    rule_size.append(size)
print(rule_size)   #179 rules were considered based on the support(1.5%)


# In[ ]:


#Choosing a suitable support
plt.figure(figsize=(16, 6))
ax = sns.lineplot(np.arange(0.01,0.1,0.005),rule_size)
ax.set_xlabel("Support",fontsize=20)
ax.set_ylabel("Number of rules",fontsize=20)
ax.grid(False)


# In[ ]:


rules_final = frequent_items=apriori(groceries, min_support = 0.015, use_colnames = True) 
rules_final.shape


# In[ ]:


from mlxtend.frequent_patterns import association_rules
 #Choosing a suitable confidence metric
rule_size = []
for i in np.arange(0.1,1,0.05):
    rule = association_rules(rules_final, metric="confidence", min_threshold=i)
    size=rule.shape[0]
    rule_size.append(size)
print(rule_size)


# In[ ]:


#Choosing a suitable confidence
plt.figure(figsize=(16, 6))
ax = sns.lineplot(np.arange(0.1,1,0.05),rule_size)
ax.set_xlabel("Confidence",fontsize=20)
ax.set_ylabel("Number of rules",fontsize=20)
ax.grid(False)


# In[ ]:


final_rule = association_rules(rules_final, metric="confidence", min_threshold=0.35)
final_rule.shape


# ## Question no 3

# In[ ]:


final_rule.sort_values("lift",ascending=False)[:10] #top 10 rules based on lift


# In[ ]:


final_rule.sort_values("confidence",ascending=False)[:10] #top 10 rules based on confidence 
#


# In[ ]:


#Finding length of antecedents
final_rule['length'] = final_rule['antecedents'].apply(lambda x: len(x))


# ## Question no 4
# 
# ##Intesting rules

# In[ ]:


#thetopfinalrules
f = final_rule[ (final_rule['length'] == 1) &
                   (final_rule['lift'] >= 1.8)  &
                   (final_rule['confidence'] >= 0.35)]
f


# ## Question no 5
# 
# 
# ## Validating on test data

# In[ ]:


testdata=pd.read_excel("../input/testdata/test.xlsx")
testdata.shape


# In[ ]:


testdata.dropna(how='all',inplace=True)
testdata.shape


# In[ ]:


#Preparing data
strings = []
for i in range(0,2000):
    strings.append([str(testdata.values[i,j]) for j in range(0,25) ])
new=[]
for j in strings:
    j=[j for j in j if str(j)!='nan']
    new.append(j)


# In[ ]:


te = TransactionEncoder()
te_ary = te.fit_transform(new)
df = pd.DataFrame(te_ary, columns=te.columns_)
df.shape


# In[ ]:


frequent_itemsets_test = apriori(df, min_support=0.015,use_colnames=True)


# In[ ]:


rule_test = association_rules(frequent_itemsets_test, metric="confidence",min_threshold=0.35)


# # TOP RULES

# In[ ]:


pd.merge(rule_test,final_rule[['antecedents','consequents']],on = ['antecedents','consequents'] )

