#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
import plotly.graph_objs as go
import matplotlib
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df=pd.read_csv('../input/breast-cancer-wisconsin-data/data.csv')


# In[ ]:


df.head()


# drop the unnecessary columns which won't help in predictions

# In[ ]:


y=df['diagnosis']
dropcols=['id','Unnamed: 32','diagnosis']
x=df.drop(dropcols,axis=1)
x.head()


# In[ ]:


patients=y.value_counts()

fig=go.Figure(data=[go.Pie(labels=patients.index,values=patients.values,hole=.3)])
colors=['gold','mediumturquoise']
fig.update_traces(textfont_size=20,marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.update_layout(title="<b>% distribution in patients",title_x=0.5)
fig.show()


# In[ ]:


data=x
data_std=(data-data.mean())/(data.std())
data1=pd.concat([y,data_std.iloc[:,0:10]],axis=1)
data2=pd.concat([y,data_std.iloc[:,10:20]],axis=1)
data3=pd.concat([y,data_std.iloc[:,20:31]],axis=1)


# In[ ]:


#?pd.melt
data1 = pd.melt(data1,id_vars='diagnosis',
                    var_name='factors',
                    value_name='value')

data2 = pd.melt(data2,id_vars='diagnosis',
                    var_name='factors',
                    value_name='value')

data3 = pd.melt(data3,id_vars='diagnosis',
                    var_name='factors',
                    value_name='value')


# In[ ]:


data1.head()


# In[ ]:


fig = px.box(data1,x="factors",y="value", color='diagnosis',notched=True)
fig.update_traces(quartilemethod="exclusive")
fig.update_layout(title='<b>notched boxplot for first 10 features',title_x=0.5)
fig.update_xaxes(tickangle=-90,title='factors')
fig.update_yaxes(title='Count')
fig.show()


# Conclusion from above could be that fractal_dimension_mean is not a good feature to classify tumor into benign/malignant since the median value of both the tumors is not well separated

# A similar conclusion can be made for the following 2 plots

# In[ ]:


plt.figure(figsize=(10,10))
sns.set_style("darkgrid")
plot = sns.violinplot(x="factors", y="value", hue="diagnosis", data=data2,split=True,inner="quart",palette = 'cool')
plt.xticks(rotation=45)
plt.legend()
plt.xlabel('factors',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.title('next 10 features',fontsize=20, fontweight='bold');


# In[ ]:


plt.figure(figsize=(10,10))
sns.set_style("dark")
sns.boxenplot(x="factors", y="value", hue="diagnosis", data=data3,palette="RdPu")
plt.xticks(rotation=90)
plt.legend()
plt.xlabel('factors',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.title('last 10 features',fontsize=20, fontweight='bold');


# A conclusion from the above violinplot can be that concavity_worst and concave_points_worst are pretty similar(apart from outliers), so while doing the classification, one of them can be dropped 

# In[ ]:


fig = px.scatter(df, x=x.loc[:,'concavity_worst'], y=x.loc[:,'concave points_worst'])
fig.update_layout(title='<b>check corr',title_x=0.5)
fig.update_xaxes(title='concavity_worst')
fig.update_yaxes(title='concave points_worst')
fig.show()


# In[ ]:


sns.set_style("dark")
jp=sns.jointplot(x.loc[:,'concavity_worst'], x.loc[:,'concave points_worst'], kind="regg", color="#9b59b6")
fig = jp.fig
fig.subplots_adjust(top=0.9)
fig.suptitle('Jointplot for checking corr', fontsize=20, fontweight='bold');


# The above 2 graphs show that concave worst and concave points worst are correlated

# In[ ]:


y1={'M':1,'B':0}
y.replace(y1,inplace=True)


# In[ ]:


a=[x,y]
df_temp=pd.concat(a,axis=1)
df_temp.head()


# In[ ]:


f,ax = plt.subplots(figsize=(15,15))
sns.heatmap(df_temp.corr(), annot=True,ax=ax, linewidths = 0.5, fmt = '.2f',cmap="YlGnBu",annot_kws={"size": 8});
plt.title('Heatmap showing features of all vatiables', fontsize=20, fontweight='bold');


# Malignant tumors are correlated to concave_points, perimeter, radius (both worst and mean) (which makes sense intuitively as well)

# In[ ]:


sns.set(style="darkgrid",palette="muted")


# In[ ]:


fig=plt.figure(figsize=(10,10))
sns.swarmplot(x="factors", y="value", hue="diagnosis", data=data1)
plt.xticks(rotation=90)
plt.legend()
plt.xlabel('factors',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
fig.suptitle('swarmplot for first 10 features', fontsize=20, fontweight='bold');


# In[ ]:


fig=plt.figure(figsize=(10,10))
sns.swarmplot(x="factors", y="value", hue="diagnosis", data=data2)
plt.xticks(rotation=90)
plt.legend()
plt.xlabel('factors',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
fig.suptitle('swarmplot for next 10 features', fontsize=20, fontweight='bold');


# In[ ]:


fig=plt.figure(figsize=(10,10))
sns.swarmplot(x="factors", y="value", hue="diagnosis", data=data3)
plt.xticks(rotation=90)
plt.legend()
plt.xlabel('factors',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
fig.suptitle('swarmplot for last 10 features', fontsize=20, fontweight='bold');


# Since the plots show the actual distribution of data, it could be helpful to decide which factors clearly ditinguish B and M type of tumor. For examp, in area_worst and radius_worst, B and M can be (almost) distinguished completely, as compared to fractal_dimension_worst.
