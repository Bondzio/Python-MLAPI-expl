#!/usr/bin/env python
# coding: utf-8

# ## Working with Pandas

# ### Pandas Series

# In[15]:


import numpy as np
import pandas as pd


# In[16]:


data = [10,20,30]
labels = ['a','b','c']
arr = np.array(data)
adict = {'a': 10, 'b':20, 'c': 40}


# In[17]:


pd.Series(data = data, index = labels)


# In[18]:


pd.Series(data, labels)


# In[19]:


pd.Series(arr, labels)


# In[20]:


pd.Series(adict)


# Series can hold references to functions as well

# In[21]:


pd.Series([print,sum,max])


# In[22]:


f = pd.Series([print,sum,max])


# In[23]:


f[0]("Hello")


# In[24]:


ser1 = pd.Series( [1,2,3,5],['USA','Japan','USSR','Germany'])


# In[25]:


ser2 = pd.Series([6,7,4,2],['USA','Italy','Germany','USSR'])


# In[26]:


ser1 + ser2


# ### DataFrames

# In[27]:


df = pd.DataFrame(np.linspace(0,1,25).reshape(5,5),['A','B','C','D','E'],['V','W','X','Y','Z'])
df


# In[28]:


df['W']  #or df.W  however not recommended


# In[29]:


print(type(df))
print(type(df['W']))


# In[30]:


df[['W','Y']]


# In[31]:


df['NEW'] = df['W']+df['Y']
df


# In[32]:


df.drop('NEW', axis = 1, inplace = True)
#or
#df = df.drop('NEW', axis = 1)
df


# Rows are axis = 0 while Columns are exis = 1

# In[33]:


df.shape 


# As tuple shows the occurence of rows first at 0 index while columns at 1 index, hence the axis names.

# In[34]:


df.loc[['A','B']]


# To get row wise indexing and selection

# In[35]:


df.iloc[1]


# 'iloc' takes only integers as indexing values.

# ### Conditional Selection

# In[36]:


df = pd.DataFrame(np.random.randn(25).reshape(5,5),['A','B','C','D','E'],['V','W','X','Y','Z'])
df


# In[37]:


df[ df < 0.5]


# In[38]:


df[df['V'] < 0]


# In[39]:


df[df['V'] < 0][['W','X']]


# In[40]:


df[(df['V'] < 0) & (df['W'] > 0)]


# 'and' operator cannot be used because it can only handle sing instances of booleans. Same is the case with 'or'.

# In[41]:


df[(df['W'] < 0) | (df['X'] > 1)]


# In[42]:


df.reset_index()


# Notice that the old index has been moved to a column.

# In[43]:


states = 'CO NY WY OK CH'.split()
df['states'] = states
df


# In[44]:


df.set_index(df['states']).drop('states', axis = 1)


# Unlike 'reset_index', 'set_index' does not makes a copy of previous index as column.

# ## -----------------------------------------------------------------------------------------------------------------------------------
# ### Multilevel Indexing and Heirarchy

# In[45]:


outside = ['G1','G1','G1','G2','G2','G2']
inside  =  [1,2,3,1,2,3]
hier_index  = list(zip(outside, inside))
print(hier_index)
hier_index  = pd.MultiIndex.from_tuples(hier_index)
hier_index


# In[46]:


ddf = pd.DataFrame(np.random.randn(6,2),hier_index, ['A','B'])
ddf


# In[47]:


ddf.index.names = ['Groups', 'Nums']
ddf


# In[48]:


ddf.loc['G2'].loc[3]['B']


# ## -----------------------------------------------------------------------------------------------------------------------------------
# ### Handling Missing Values

# In[49]:


daf  = {'A': [1, 2, np.nan], 'B': [4, np.nan, np.nan], 'C': [7,8,9]}
daf = pd.DataFrame(daf)
daf


# In[50]:


daf.dropna()


# In[51]:


daf.dropna(axis = 1)


# In[52]:


daf.dropna(thresh = 2)


# 'thresh' sets the minimum occurence of nan to be dropped

# In[53]:


daf.fillna(value = 'FILLED')


# In[54]:


daf['A'].fillna(value = (daf['A'].mean()), inplace = True)
daf['B'].fillna(value = (daf['B'].mean()), inplace = True)
daf


# ## -----------------------------------------------------------------------------------------------------------------------------------
# ### Grouping By

# In[55]:


sa = pd.DataFrame({'Sales': [450,120,345,334,232,100],'Person': ['Prashant','Shivam','Shiva','Ankit','Arpit','Abhi']
                  ,'Company':['Microsoft','Microsoft','Google','Google','Apple','Apple']
                   })
sa


# In[56]:


byComp = sa.groupby('Company')
byComp


# In[57]:


byComp.mean()


# Non Numeric column 'Person' ignored due to non relevance to the mean function.

# In[58]:


byComp.median()


# In[59]:


byComp.median().loc['Microsoft']


# Summing up all above steps as one:

# In[60]:


sa.groupby('Company').median().loc['Microsoft']


# In[61]:


sa.groupby('Company').count()


# In[62]:


sa.groupby('Company').max()


# Gave the individual entry from each company with max values.

# In[63]:


sa.groupby('Company').min()


# In[64]:


sa.groupby('Company').describe().transpose()


# In[65]:


sa.groupby('Company').describe().transpose()['Microsoft']


# ## -----------------------------------------------------------------------------------------------------------------------------------
# ### Merging, Joining and Concatenating

# In[66]:


df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']},
                        index=[0, 1, 2, 3])


# In[67]:


df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                        'B': ['B4', 'B5', 'B6', 'B7'],
                        'C': ['C4', 'C5', 'C6', 'C7'],
                        'D': ['D4', 'D5', 'D6', 'D7']},
                         index=[4, 5, 6, 7]) 


# In[68]:


df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                        'B': ['B8', 'B9', 'B10', 'B11'],
                        'C': ['C8', 'C9', 'C10', 'C11'],
                        'D': ['D8', 'D9', 'D10', 'D11']},
                        index=[8, 9, 10, 11])


# In[69]:


df1


# In[70]:


df2


# In[71]:


df3


# In[72]:


pd.concat([df1, df2, df3])


# In[73]:


pd.concat([df1, df2, df3], axis = 1)


# In[74]:


left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
   
right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                          'C': ['C0', 'C1', 'C2', 'C3'],
                          'D': ['D0', 'D1', 'D2', 'D3']})    


# In[75]:


left


# In[76]:


right


# In[77]:


pd.merge(left, right, how = 'inner', on = 'key')


# In[78]:


left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                        'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3']})
    
right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                               'key2': ['K0', 'K0', 'K0', 'K0'],
                                  'C': ['C0', 'C1', 'C2', 'C3'],
                                  'D': ['D0', 'D1', 'D2', 'D3']})


# In[79]:


left


# In[80]:


right


# In[81]:


pd.merge(left, right, on = ['key1', 'key2'])


# In[82]:


pd.merge(left, right, how = 'outer', on = ['key1','key2'])


# In[83]:


pd.merge(left, right, how = 'left', on = ['key1', 'key2'])


# In[84]:


left = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2']},
                      index=['K0', 'K1', 'K2']) 

right = pd.DataFrame({'C': ['C0', 'C2', 'C3'],
                    'D': ['D0', 'D2', 'D3']},
                      index=['K0', 'K2', 'K3'])


# In[85]:


left.join(right)


# In[86]:


left.join(right, how = 'outer')


# ## ------------------------------------------------------------------------------------------------------------------------------------
# ### Operations

# In[87]:


import pandas as pd
df = pd.DataFrame({'col1':[1,2,3,4],'col2':[444,555,666,444],'col3':['abc','def','ghi','xyz']})
df


# In[88]:


df['col2'].unique()


# In[89]:


df['col2'].nunique() #equivalent to using len(df['col2'].unique())


# In[90]:


df['col2'].value_counts()


# In[91]:


df[(df['col1'] > 1) & (df['col2'] == 444)]


# In[92]:


def times2(n):
    return n*2


# In[93]:


df['col2'].apply((lambda n: n*2)) #or df['col2'].apply(times2)


# In[94]:


df.columns


# In[95]:


df.index


# In[96]:


df.sort_values('col2', ascending = False)


# In[97]:


df.isnull()


# In[98]:


data = {'A':['foo','foo','foo','bar','bar','bar'],
     'B':['one','one','two','two','one','one'],
       'C':['x','y','x','y','x','y'],
       'D':[1,3,2,5,4,1]}

df = pd.DataFrame(data)
df


# In[99]:


df.pivot_table(values = 'D', index = ['A','B'], columns = 'C')


# ## ------------------------------------------------------------------------------------------------------------------------------------
# ### Data Input and Output
# #### in CSV, HTML, SQL, Excel

# In[100]:


dff = pd.read_csv('../input/example')
dff


# In[101]:


dff.to_csv('ToCSVoutput.csv', index = False)


# Make sure you put index as False. Or index will be added as a column.

# In[102]:


pd.read_csv('ToCSVoutput.csv')


# In[103]:


ddff = pd.read_excel('../input/Excel_Sample.xlsx', sheet_name= 'Sheet1')
ddff


# In[104]:


ddff.to_excel('ToXLoutput.xlsx', sheet_name= 'Sheet1')


# ## Finally! 
