#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import pandas as pd
df=pd.read_csv('../input/covid19-global-forecasting-week-5/train.csv')
test=pd.read_csv('../input/covid19-global-forecasting-week-5/train.csv')
df.head()


# In[ ]:


df.describe()


# In[ ]:


df['Target'].value_counts()


# In[ ]:


l=[]
for i in range(len(df)):
    if(df['Target'][i]=='ConfirmedCases'):
        l.append(0)
    else:
        l.append(1)


# In[ ]:


m=[]
for i in range(len(df)):
    if(test['Target'][i]=='ConfirmedCases'):
        m.append(0)
    else:
        m.append(1)
        


# In[ ]:


test['Target_val']=m


# In[ ]:


test.shape


# In[ ]:


df['Target_val']=l
df.head()


# **DATA_VISUALIZATION**

# In[ ]:


import seaborn as sns
sns.lmplot(x='Population',y='TargetValue',fit_reg=False,hue='Country_Region',data=df)


# In[ ]:


sns.boxplot(df['Weight']).set_title('Weight')


# In[ ]:


sns.distplot(df['Weight'])


# > **As We Can See Here The Histogram Of Population Is Right_Skewed So Can Act As Outlier In Higher Ranges**

# In[ ]:


sns.distplot(df['Population'])


# IT can be visualized from boxplot

# In[ ]:


sns.boxplot(df['Population'])


# **HERE WE ARE VISUALIZING HOW POPULATION AND WEIGHT AFFECTS TARGET VALUE**

# In[ ]:


import plotly
import plotly.graph_objs as go
from plotly.offline import *
trace1=go.Scatter(
    x=df.TargetValue,
    y=df.Population,
    mode='lines',
    name='Population',
    marker=dict(color='rgba(16,112,2,0.8)'),
    text=df.Country_Region

)

trace2=go.Scatter(
    x=df.TargetValue,
    y=df.Weight,
    mode='lines+markers',
    name='Weight',
    marker=dict(color='rgba(80, 26, 80, 0.8)'),
    text=df.Country_Region
)

data=[trace1,trace2]
layout=dict(title='Comparing Population and Weight with respect to TargetValue', xaxis= dict(title= 'TargetValue',ticklen= 5,zeroline= False))
figure=dict(data=data,layout=layout)
iplot(figure)


# ***MODEL_BUILDING***

# In[ ]:


from sklearn.model_selection import train_test_split
import numpy as np
X=np.asanyarray(df[['Population','Weight','Target_val']],dtype=np.float64)
y=np.asanyarray(df['TargetValue'],dtype=np.float64)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=333)
print('Train size :: ',X_train.shape)
print('Test size :: ',X_test.shape)


# # INITIALIZING MODEL BY DEFAULT K=4

# In[ ]:


from sklearn import neighbors
from sklearn.metrics import mean_squared_error
k=4
model=neighbors.KNeighborsRegressor(n_neighbors=k)
model.fit(X_train,y_train)


# # CHECKING FOR WHICH K IT GIVES OPTIMAL ANSWER

# In[ ]:


from math import sqrt
rms_value=[]
for k in range(1,21):
    model=neighbors.KNeighborsRegressor(n_neighbors=k)
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    error=sqrt(mean_squared_error(y_test,pred))
    rms_value.append(error)
    print(error)


# In[ ]:


min_val=min(rms_value)


val=rms_value.index(min_val)
k=val+1


# In[ ]:


curve=pd.DataFrame(rms_value)
curve.plot()


# ***SO_HERE WE GOT BEST RESULT FOR K=18***

# In[ ]:


##SO TAKING K=10
import numpy as np
model=neighbors.KNeighborsRegressor(n_neighbors=k)
model.fit(X_train,y_train)
pred=model.predict(X_test)
error=sqrt(mean_squared_error(y_test,pred))
rms_value.append(error)
print(error)


# In[ ]:





# In[ ]:


print(model.score(X_test,y_test))


# In[ ]:


final_prediction=model.predict(test[['Population','Weight','Target_val']])


# In[ ]:


final_prediction.shape


# In[ ]:


op = [int(x) for x in final_prediction]

out = pd.DataFrame({'Id': df.index, 'TargetValue': op})
print(out)
out.shape


# **HERE I AM USING STANDARD QUANTILE VALUES** 
# 
# 1.First_quantile-->0.25
# 
# 2.Second_quantile-->0.5(Mean)
# 
# 3.Third_quantile-->0.75

# In[ ]:


col1=out.groupby(['Id'])['TargetValue'].quantile(q=0.25).reset_index()
col2=out.groupby(['Id'])['TargetValue'].quantile(q=0.5).reset_index()
col3=out.groupby(['Id'])['TargetValue'].quantile(q=0.75).reset_index()
col1.shape


# In[ ]:


col1.columns=['Id','q0.25']
col2.columns=['Id','q0.5']
col3.columns=['Id','q0.75']
col1=pd.concat([col1,col2['q0.5'],col3['q0.75']],1)
col1['q0.25']=col1['q0.25'].clip(0,10000)
col1['q0.5']=col2['q0.5'].clip(0,10000)
col1['q0.75']=col3['q0.75'].clip(0,10000)


# In[ ]:


col1.shape


# In[ ]:


submission=pd.melt(col1, id_vars=['Id'], value_vars=['q0.25','q0.5','q0.75'])
submission['variable']=submission['variable'].str.replace("q","", regex=False)
submission['ForecastId_Quantile']=submission['Id'].astype(str)+'_'+submission['variable']
submission['TargetValue']=submission['value']
submission=submission[['ForecastId_Quantile','TargetValue']]


# In[ ]:


key=[]
for i in range(0,2264802):
    key.append(i)


# In[ ]:


submission.head()


# In[ ]:


submission.shape


# In[ ]:


submission=submission[submission['Index']<935010]


# In[ ]:


submission.shape


# In[ ]:


submission.drop(['Index'],inplace=True,axis=1)


# In[ ]:



submission.to_csv("submission.csv",index=False)


# In[ ]:


submission.head()

