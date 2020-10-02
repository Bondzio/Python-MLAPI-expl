#!/usr/bin/env python
# coding: utf-8

# # EDA 

# When you are the large US electrical appliances retailer with many branches, where the salesmen are given free will to sell the product at his profit margin, well there are going to smart salesmen who will do too good. we'll see what are salesman up to.
# The dataset is of sales where the salesmen are classified into three risk factors in attribute Suspicious -  'indeterminate' 'no' 'yes' by the company using this we'll do a EDA.
# 

# In[ ]:


# loading requred packages 
import numpy as np
import pandas as pd
import math 
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sns
import plotly.offline as pyoff
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import warnings                             # To ignore any warnings
warnings.filterwarnings('ignore') 
from sklearn import preprocessing
init_notebook_mode(connected=True)


# In[ ]:


#creating the layout for the polts

def generate_layout_bar(col_name):
    layout_bar = go.Layout(
        autosize=False, # auto size the graph? use False if you are specifying the height and width
        width=800, # height of the figure in pixels
        height=600, # height of the figure in pixels
        title = "Distribution of {} column".format(col_name), # title of the figure
        # more granular control on the title font 
        titlefont=dict( 
            family='Courier New, monospace', # font family
            size=14, # size of the font
            color='black' # color of the font
        ),
        # granular control on the axes objects 
        xaxis=dict( 
        tickfont=dict(
            family='Courier New, monospace', # font family
            size=14, # size of ticks displayed on the x axis
            color='black'  # color of the font
            )
        ),
        yaxis=dict(
#         range=[0,100],
            title='Percentage',
            titlefont=dict(
                size=14,
                color='black'
            ),
        tickfont=dict(
            family='Courier New, monospace', # font family
            size=14, # size of ticks displayed on the y axis
            color='black' # color of the font
            )
        ),
        font = dict(
            family='Courier New, monospace', # font family
            color = "white",# color of the font
            size = 12 # size of the font displayed on the bar
                )  
        )
    return layout_bar


# In[ ]:


dftrain = pd.read_csv("../input/us-electrical-appliances-explored-data-for-finial/Train.csv")
#dftest = pd.read_excel("Test.xlsx")


# In[ ]:


dftrain.head(5)


# In[ ]:


dftrain.info()


# In[ ]:


value,count=np.unique(dftrain['Suspicious'],return_counts=True)
percent=(count/dftrain.shape[0])*100
print(np.asarray([value,count,percent]).T)


# 'yes' says some fishy things are going on and it's at 0.42%. even though most of the sales fall into 'indeterminate' that still means there can be some fraud sales happening there too, where it's not popping up on the radar of the company and they didn't give us any info on how they classified salesman.

# In[ ]:


data1 = [
    go.Bar(
        x=value, # assign x as the dataframe column 'x'
        y=count,
        text = percent,
        textposition = 'auto'
    )
]

layout = go.Layout(
    barmode='stack',
    title='Distribution of the Traget attribute',
    xaxis=dict(title='TotalSumSalesValue'),
    yaxis=dict(title='Quantity')
)

fig = go.Figure(data=data1, layout=layout)

# IPython notebook
iplot(fig)


# let's derive more attributes to see if we can pull out some insights 

# In[ ]:


oneunitSalesValue = dftrain['TotalSalesValue']/dftrain['Quantity']
dftrain["OneUnitSalesValue"]=oneunitSalesValue
dftrain.head(10)


# In[ ]:


AvgSalesValue = dftrain['OneUnitSalesValue']/dftrain['TotalSalesValue']
dftrain["AvgUnitSales"]=AvgSalesValue
dftrain.head()


# In[ ]:


df1=dftrain.groupby(['SalesPersonID','ProductID']).mean()['Quantity']
df1 = (pd.DataFrame(df1))
df1 = df1.reset_index()
df1.columns


# In[ ]:


data=pd.merge(dftrain,df1,on=['SalesPersonID','ProductID'],how='left')


# In[ ]:


data = data.rename(index = str,columns ={'Quantity_y':'AvgQuantityperProductID','Quantity_x':'Quantity'})


# In[ ]:


df1=data.groupby(['SalesPersonID','ProductID']).mean()['TotalSalesValue']
df1 = (pd.DataFrame(df1))
df1 = df1.reset_index()
df1.columns


# In[ ]:


data=pd.merge(data,df1,on=['SalesPersonID','ProductID'],how='left')
data = data.rename(index = str,columns ={'TotalSalesValue_x':'TotalSalesValue','TotalSalesValue_y':'AvgSelingPrice'})
data = data.rename(index = str,columns ={'AvgUnitSales':'ratioOfcontribution'})
data.head()


# In[ ]:


Yplot1=data.groupby(['Suspicious']).sum()['AvgQuantityperProductID']
Yplot1=pd.DataFrame(Yplot1)
Yplot1


# In[ ]:


data1 = [
    go.Bar(
        x=Yplot1.index, # assign x as the dataframe column 'x'
        y=Yplot1['AvgQuantityperProductID'],
        #text=data.groupby(['Suspicious']).sum()['AvgQuantityperProductID'],
        #textposition='auto'
    )
]

layout = go.Layout(
    barmode='stack',
    autosize=True,
    title='Distribution of AvgQuantity per ProductID W.R.T Traget'
)

fig = go.Figure(data=data1, layout=layout)

# IPython notebook
iplot(fig)


# In[ ]:


#total sum of Quantity, TotalSalesValue, OneUnitSalesValue, ratioOfcontribution, AvgQuantityperProductID, AvgSelingPrice W.R.T SalesPersonID
sumofpersonID=data.groupby(['Suspicious']).sum()
sumofpersonID.head()


# In[ ]:


v1=data.groupby(['SalesPersonID']).sum()
v1.head()


# In[ ]:


#top and last 10 quantity soled by a salesperson 
top_ten_quantity_by_SalesPersonID=v1.sort_values(by='Quantity',ascending=False).head(10)
last_ten_quantity_by_SalesPersonID=v1.sort_values(by='Quantity',ascending=False).tail(10)


# In[ ]:


top_ten_quantity_by_SalesPersonID


# In[ ]:


yes=data[data['Suspicious']=='Yes'].sum()
No=data[data['Suspicious']=='No'].sum()
indeterminate=data[data['Suspicious']=='indeterminate'].sum()


# In[ ]:


data1 = [
    go.Bar(
        x=top_ten_quantity_by_SalesPersonID.index, # assign x as the dataframe column 'x'
        y=top_ten_quantity_by_SalesPersonID['Quantity'],
        text=top_ten_quantity_by_SalesPersonID['Quantity'],
        textposition='auto'
    )
]

layout = go.Layout(
    barmode='stack',
    title='Top ten Quantity sold W.R.T salespersonID'
)

fig = go.Figure(data=data1, layout=layout)

# IPython notebook
iplot(fig)


# In[ ]:


yesm=data[data['Suspicious']=='Yes']
Nom=data[data['Suspicious']=='No']
indeterminatem=data[data['Suspicious']=='indeterminate']


# Looking for the hights salespersonID contribution, in the Suspicious column

# In[ ]:


yesm[yesm['SalesPersonID']=='C21636'].head()


# SalesPersonID - C21636 and the Product witch he like to sell - PR6444 Quantity sold 662 + 470 = 1132 hmm, lets have look at this guy.

# In[ ]:


indeterminatem[indeterminatem['SalesPersonID']=='C21636'].head()


# In[ ]:


Nom[Nom['SalesPersonID']=='C21636'].head()


# this guy C21636 likes to keep his product flying. well is it clean?mm

# In[ ]:


#sum of the total sales value
sumoftotalSales=data['TotalSalesValue'].sum()
sumoftotalSales


# In[ ]:


#sum of the total Quantity value
sumoftotalQuantitysold=data['Quantity'].sum()
sumoftotalQuantitysold


# In[ ]:


print((top_ten_quantity_by_SalesPersonID['Quantity']/sumoftotalSales)*100)
print((last_ten_quantity_by_SalesPersonID['Quantity']/sumoftotalSales)*100)


# In[ ]:


data1 = [
    go.Bar(
        x=top_ten_quantity_by_SalesPersonID.index, # assign x as the dataframe column 'x'
        y=((top_ten_quantity_by_SalesPersonID['Quantity']/sumoftotalSales)*100),
        text=((top_ten_quantity_by_SalesPersonID['Quantity']/sumoftotalSales)*100),
        marker=dict(
        color='rgb(0,200,0)',# Lava (#CC0E1D)
#         color = 'rgb(200,0,0)'   `
        ),
        textposition='auto',
        
    )
]

layout = go.Layout(
    barmode='stack',
    autosize=True,
    title='Percentage of total Quantity sold by salesperson, by total sales '
    
)

fig = go.Figure(data=data1, layout=layout)

# IPython notebook
iplot(fig)


# In[ ]:


data1 = [
    go.Bar(
        x=last_ten_quantity_by_SalesPersonID.index, # assign x as the dataframe column 'x'
        y=((last_ten_quantity_by_SalesPersonID['Quantity']/sumoftotalSales)*100),
        text=((last_ten_quantity_by_SalesPersonID['Quantity']/sumoftotalSales)*100),
        marker=dict(
        color='rgb(200,100,0)',# Lava (#CC0E1D)
#         color = 'rgb(0,0,0)'   `
        ),
        textposition='auto'
    )
]

layout = go.Layout(
    barmode='stack',
    autosize=True,
    title='Percentage of last 10 Quantity sold by salesperson by total sales'
    
)

fig = go.Figure(data=data1, layout=layout)

# IPython notebook
iplot(fig)


# In[ ]:


yesm[yesm['SalesPersonID']=='C21887'].head()


# In[ ]:


indeterminatem[indeterminatem['SalesPersonID']=='C21887'].head()


# In[ ]:


Nom[Nom['SalesPersonID']=='C21887'].head()


# In[ ]:


prod=data.groupby(['ProductID']).sum()


# In[ ]:


top_ten_quantity_by_ProductID=prod.sort_values(by='Quantity',ascending=False).head(10)
last_ten_quantity_by_ProductID=prod.sort_values(by='Quantity',ascending=False).tail(10)


# In[ ]:


((top_ten_quantity_by_ProductID['Quantity']/sumoftotalQuantitysold)*100)
((last_ten_quantity_by_ProductID['Quantity']/sumoftotalQuantitysold)*100)


# In[ ]:


data1 = [
    go.Bar(
        x=top_ten_quantity_by_ProductID.index, # assign x as the dataframe column 'x'
        y=((top_ten_quantity_by_ProductID['Quantity']/sumoftotalQuantitysold)*100),
        text=((top_ten_quantity_by_ProductID['Quantity']/sumoftotalQuantitysold)*100),
        marker=dict(
        color='rgb(200,2000,0)',# Lava (#CC0E1D)
#         color = 'rgb(0,0,0)'   `
        ),
        textposition='auto'
    )
]

layout = go.Layout(
        autosize=True,
        title='Top performers based on productID Quantity',
        xaxis=dict(title='ProductID'),
        yaxis=dict(title='Quantity percentage')
)

fig = go.Figure(data=data1, layout=layout)

# IPython notebook
iplot(fig)


# Looking for the hights ProductID contribution, in the Suspicious column

# In[ ]:


indeterminatem[indeterminatem['ProductID']=='PR6550'].head()


# In[ ]:


yesm[yesm['ProductID']=='PR6550'].head()


# In[ ]:


Nom[Nom['ProductID']=='PR6550'].head()


# In[ ]:


percentageoftotalSaleswhenyes=((yes['TotalSalesValue']/sumoftotalSales)*100)
percentageoftotalSaleswhenyes


# In[ ]:


percentageoftotalSaleswhenNo=((No['TotalSalesValue']/sumoftotalSales)*100)
percentageoftotalSaleswhenNo


# In[ ]:


percentageoftotalSaleswhenindeterminate=((indeterminate['TotalSalesValue']/sumoftotalSales)*100)
percentageoftotalSaleswhenindeterminate


# In[ ]:


sumoftotalQuantity=data['Quantity'].sum()
sumoftotalQuantity


# In[ ]:


percentageoftotalQuantitywhenyes=((yes['Quantity']/sumoftotalQuantitysold)*100)
percentageoftotalQuantitywhenyes


# In[ ]:


percentageoftotalQuantitywhenNo=((No['Quantity']/sumoftotalQuantitysold)*100)
percentageoftotalQuantitywhenNo


# In[ ]:


percentageoftotalQuantitywhenindeterminate=((indeterminate['Quantity']/sumoftotalQuantitysold)*100)
percentageoftotalQuantitywhenindeterminate


# In[ ]:


df1 = dftrain.groupby(['SalesPersonID'])[['TotalSalesValue']].mean()
df1 = df1.rename(columns={'TotalSalesValue': 'Average Transactions SalesP'})
dftrain = dftrain.join(df1,on = ['SalesPersonID'])


# In[ ]:


dftrain.head()


# In[ ]:


value=np.unique(dftrain['Suspicious'])
count = dftrain.groupby(['Suspicious'])[['Average Transactions SalesP']].mean()
#percent=(count/dftrain.shape[0])*100
print(np.asarray([value,count,percent]).T)
#dftrain.groupby(['Suspicious'])[['Average Transactions SalesP']].mean().plot.bar(color = "#b53856")

