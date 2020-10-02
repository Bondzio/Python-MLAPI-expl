#!/usr/bin/env python
# coding: utf-8

# **Diamonds Dataset - Project 2**

# In[ ]:


from IPython.display import Image
import os
get_ipython().system('ls ../input/')

Image("../input/inputimages/download.png")


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# First, we are reading data from diamond.csv file with read_csv() function.

# In[ ]:


diamond_data = pd.read_csv('../input/diamonds/diamonds.csv', encoding="windows-1252")


# head() method gives us the first 5 rows of the dataset.

# In[ ]:


diamond_data.head()


# tail() method gives us the last 5 rows of the dataset.

# In[ ]:


diamond_data.tail()


# With **describe()** method gives the information about just the numerical data.

# In[ ]:


diamond_data.describe()


# In[ ]:


diamond_data.info()


# With **info()** method we had the column names and types.

# In[ ]:


diamond_data.columns


# In this dataset we are given carat,cut,color,clarity,depth,table,price,x,y and z as a column.

# In[ ]:


print( diamond_data.carat.min() )

print( diamond_data.carat.max() )


# As we can see above the diamond can take the values between 0.2 and 5.01 in carat column.

# In[ ]:


print( diamond_data.cut.unique() )

print( diamond_data.color.unique() )

print( diamond_data.clarity.unique() )


# We can see ;
# 
# ->the types of cuts by using the **unique()** method.It can be **'Ideal', 'Premium', 'Good'**, **'Very Good'**  or **'Fair'**.<br>
# ->the types of colors are  **'E' 'I' 'J' 'H' 'F' 'G' 'D'** <br>
# ->the types of clarity are **'SI2' 'SI1' 'VS1' 'VS2' 'VVS2' 'VVS1' 'I1''IF'** <br>

# In[ ]:


diamond_data.depth.unique() #clear data


# In[ ]:


diamond_data.price.unique()


# In[ ]:


print( diamond_data.x.unique() )
print( diamond_data.y.unique() )
print( diamond_data.z.unique() ) #clear data


# In[ ]:


diamond_data.info()
#Here the Unnamed: 0 column is not necessarily required.
#diamond_data.drop(['Unnamed: 0'],, axis=1,inplace=True )


# In[ ]:


diamond_data.drop(['Unnamed: 0'], axis=1, inplace=True) # we delete the unnecessary column and get the info again

diamond_data.info()


# In[ ]:


diamond_data.corr()


# In[ ]:


import seaborn as sns

f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(diamond_data.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


g = sns.jointplot(diamond_data.carat[:150], diamond_data.price[:150], kind="kde", height=7) #CPU couldn't handle 53000 values
#so just to show we took the first 150 values
p= sns.jointplot( x='carat',y='price',data=diamond_data,linewidth=0.1 ,ratio=3 ,height=8 )
#plt.savefig('graph.png')
plt.show()


# A carat is a unit of weight for diamonds and other gemstones.The higher the carat, the more expensive the diamond is going to be.

# In[ ]:



ax = sns.violinplot(x="cut", y="price", data=diamond_data,height=15 )


# In[ ]:


diamond_data.head()


# In[ ]:



#ax = sns.countplot(x="depth", hue="cut", data=diamond_data[:5],palette="Paired")
g = sns.catplot( x='color',hue="cut", data=diamond_data[:150],kind="count",height=10)


# In the above graph we can see each color separately with their cut types.<br>
# In color **E** , we have 'Very Good' cut type mostly and 'Fair'cut type at least.<br>
# In color **I** , we have 'Ideal' cut type mostly and 'Good'cut type at least.<br>
# In color **J** , we have 'Very Good' cut type mostly and 'Premium' type at least.<br>
# In color **H** , we have 'Fair-Ideal' cut type mostly and 'Premium-Very Good'cut type at least.<br>
# In color **F** , we have 'Very Good' cut type mostly and 'Good'cut type at least.<br>
# In color **G** , we have 'Ideal' cut type mostly and 'Fair' type at least.<br>
# In color **D** , we have 'Very Good' cut type mostly and 'Premium-Good' type at least.<br>
# 
# 

# In[ ]:


#Find the most valuable color of diamond 
diamond_color=list( diamond_data.color.unique() )

diamond_color # first we extracted the unique colors of diamonds in the dataset 

average_prices_ofEachColor=[] # created an empty list of average prices of each color

for each in diamond_color:
    x=diamond_data[ diamond_data['color']==each ] #extract the same color from the dataframe
    current_avg=sum( x.price ) / len( x ) #calculate the average by dividing sum to it's length
    average_prices_ofEachColor.append( current_avg ) # append list what we've found in the previous row
    
print( average_prices_ofEachColor )

new_frame1=pd.DataFrame({"Color_Of_Diamond":diamond_color,"Average_Price_Of_Diamond":average_prices_ofEachColor })
#created a new framework which indicates the color of diamond and the average prices of each
#print( new_frame1 ) #see what we've found

y=new_frame1.Average_Price_Of_Diamond.max() # find the maximum value in the Average Price Of Diamond Column
z=new_frame1[ new_frame1['Average_Price_Of_Diamond']==y ] #extract the name of the value

most_valuable_color=str( z.Color_Of_Diamond ).split()[1] 
print("\nMost valuable type of diamond according to Colors is ",str( z.Color_Of_Diamond ).split()[1] )

new_frame1


# In[ ]:


diamond_data.head()


# In[ ]:


#Find the most valuable cut type of diamond 

cut_types_list=list( diamond_data.cut.unique() ) #First extract the unique types of cuts

cut_types_list # see what are these types

average_prices_list=[] # created an empty list of average_prices_list

for each in cut_types_list: 
    x=diamond_data[ diamond_data['cut']==each ] # extract the same type of cut for each type in the list cut_types_list 
    current_avg=sum( x.price )/len( x ) #calculate averages
    average_prices_list.append( current_avg ) # append result to the  average_prices_list
new_frame2=pd.DataFrame({"Cut_Type_Of_Diamond":cut_types_list,"Average_Price_Of_Diamond":average_prices_list })
#created a new dataframe which contains Cut_Type_Of_Diamond and Average_Price_Of_Diamond as a column
#print( new_frame2 )
y=new_frame2.Average_Price_Of_Diamond.max() # find the maximum value in the Average Price Of Diamond Column
z=new_frame2[ new_frame2['Average_Price_Of_Diamond']==y ] #extract the name of the value
print("\nMost valuable type of diamond according to Cut Types is ",str( z.Cut_Type_Of_Diamond ).split()[1] )

most_valuable_cutType=str( z.Cut_Type_Of_Diamond ).split()[1] 
new_frame2  


# In[ ]:


#Find the most valuable clarity of diamond

clarity_list=list( diamond_data.clarity.unique() )

average_prices_list=[]

for each in clarity_list:
    x=diamond_data[ diamond_data['clarity']==each ]
    current_avg=sum( x.price )/len( x )
    average_prices_list.append( current_avg )
    
new_frame3=pd.DataFrame({"Clarity_Of_Diamond":clarity_list,"Average_Price_Of_Diamond":average_prices_list})

y=new_frame3['Average_Price_Of_Diamond'].max()
z=new_frame3[ new_frame3["Average_Price_Of_Diamond"]==y ]

print("Most valuable type of diamond according to clarity is: ",str( z.Clarity_Of_Diamond ).split()[1] )

most_valuable_clarity=str( z.Clarity_Of_Diamond ).split()[1] 
new_frame3
  


# In[ ]:


valuable=diamond_data[(diamond_data['cut']==most_valuable_cutType ) & (diamond_data['color']==most_valuable_color) & (diamond_data['clarity']==most_valuable_clarity) ]
z=valuable.carat.max()

valuable[ valuable['carat']==z ]

#According to the average results we've found here' are the diamonds 


# In[ ]:


#most common three cut types of diamonds
#most common three colors of diamonds
#most common three clarities of diamonds
#most common three depths of diamonds

from collections import Counter

color_count=Counter( list( diamond_data.color ) )
most_common_colors = color_count.most_common(3)  

cut_count=Counter( list( diamond_data.cut) )
most_common_cuts=cut_count.most_common(3)

clarity_count=Counter( list( diamond_data.clarity ) )
most_common_clarity=clarity_count.most_common(3)

depth_count=Counter( list( diamond_data.depth ) )
most_common_depth=depth_count.most_common(3)

x1,y1 = zip(*most_common_colors)
x1,y1 = list(x1),list(y1)

x2,y2 = zip(*most_common_cuts )
x2,y2 = list(x2),list(y2)

x3,y3 = zip(*most_common_clarity )
x3,y3 = list(x3),list(y3)

x4,y4 = zip(*most_common_depth )
x4,y4 = list(x4),list(y4)

fig, axes = plt.subplots(nrows=2, ncols=2)



sns.barplot(ax=axes[0,0],x=x1, y=y1,palette = sns.cubehelix_palette(len(x)))
sns.barplot(ax=axes[0,1],x=x2, y=y2,palette = sns.cubehelix_palette(len(x)))
sns.barplot(ax=axes[1,0],x=x3, y=y3,palette = sns.cubehelix_palette(len(x)))
sns.barplot(ax=axes[1,1],x=x4, y=y4,palette = sns.cubehelix_palette(len(x)))


# In the [0,0] graph we can see the **most common color of diamonds is 'G'.**<br>
# In the [0,1] graph we can see the **most common cut type of diamonds is 'Ideal'.**<br>
# In the [1,0] graph we can see the **most common clarity of diamonds is 'SI1'.**<br>
# In the [1,1] graph we can see the **most common depth of diamonds is '61.8'.**<br>
# 

# In[ ]:


diamond_data.color.unique()


# In[ ]:


#Percentage of Colors In Each Cut Type
#First we create empty lists for each type of colors
colorE=[]
colorI=[]
colorJ=[]

colorH=[]
colorF=[]
colorG=[]
colorD=[]

#we have already found the unique cut types 
for each in cut_types_list:
    x=diamond_data[ diamond_data['cut']==each ]  #for each type we are looking for each number of colors  
    colorE.append( len( x[ x['color']=='E'] ) )
    colorI.append( len( x[ x['color']=='I'] ) )
    colorJ.append( len( x[ x['color']=='J'] ) )
    colorH.append( len( x[ x['color']=='H'] ) )
    colorF.append( len( x[ x['color']=='F'] ) )
    colorG.append( len( x[ x['color']=='G'] ) )
    colorD.append( len( x[ x['color']=='D'] ) )
    
f,ax = plt.subplots(figsize = (10,10))
sns.barplot(x=colorE,y=cut_types_list,color='red',alpha = 0.5,label='E' )
sns.barplot(x=colorI,y=cut_types_list,color='blue',alpha = 0.7,label='I')
sns.barplot(x=colorJ ,y=cut_types_list,color='cyan',alpha = 0.6,label='J')
sns.barplot(x=colorH,y=cut_types_list,color='pink',alpha = 0.6,label='H')
sns.barplot(x=colorF,y=cut_types_list,color='yellow',alpha = 0.6,label='F')
sns.barplot(x=colorG,y=cut_types_list,color='green',alpha = 0.6,label='G')
sns.barplot(x=colorD,y=cut_types_list,color='purple',alpha = 0.6,label='D')


ax.legend(loc='lower right',frameon = True)     # legendlarin gorunurlugu
ax.set(xlabel=' Percentage Of Colors', ylabel='Types Of Cuts',title = "Percentage of Colors In Each Cut Type ")
    


# In[ ]:



labels = diamond_data.cut.value_counts().index
colors = ['grey','blue','red','yellow','green']
explode = [0,0,0,0,0]
sizes = diamond_data.cut.value_counts().values

# visual
plt.figure(figsize = (7,7))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Diamonds According To Cut Types',color = 'blue',fontsize = 15)


# In[ ]:


diamond_data.head()


# In[ ]:


sns.boxplot(x="cut", y="carat", hue="color", data=diamond_data[:1000], palette="PRGn")
plt.show()


# In[ ]:


sns.swarmplot(x="clarity", y="carat",hue="cut", data=diamond_data[:1000],palette="PRGn")
plt.show()


# In[ ]:




