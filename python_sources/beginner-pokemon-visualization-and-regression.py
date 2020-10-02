#!/usr/bin/env python
# coding: utf-8

# ## Hello there, thank you for looking at my first notebook.
# ##### This is my first published notebook ever. Since I am beginner it would be awesome if you could write in the comments what can I change for it to be better. Or maybe some new visualizations that are good and I should implement them. Any feedback would be appreciated.
# 
# 
# ##### I am manly using matplotlib for now. At the end there is also a little bit of seaborn charts.

# In[ ]:




import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# #### What our data looks like

# In[ ]:


data = pd.read_csv("/kaggle/input/pokemon/Pokemon.csv")
data = data.drop("#",axis=1)
data.head()


# #### Descibe method on data

# In[ ]:


desc = data.drop(["Name","Type 1","Type 2","Generation","Legendary"],axis=1)
desc.describe()


# #### Now various bar plots of all pokemons

# In[ ]:


def autolabel(rects,h):
    for rect in rects:
        height = rect.get_height()
        if(height >h):
            rect.set_color("blue")
        ax.text(rect.get_x() + rect.get_width()/2., 1.01*height,'%d' % int(height),ha='center', va='bottom')

plt.figure(figsize=(5,5))
bars = plt.bar(data["Generation"].unique(), data.groupby("Generation").count()["Name"],color="lightgrey",alpha=0.8)
ax = plt.gca()
ax.axes.get_yaxis().set_visible(False)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.title('number of pokemons across generations')
autolabel(bars,150)
plt.show()


# In[ ]:


plt.figure(figsize=(20,5))
bars = plt.bar(data["Type 1"].unique(), data.groupby("Type 1").count()["Name"],color="lightgrey",alpha=0.8)
ax = plt.gca()
ax.axes.get_yaxis().set_visible(False)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.title('Number of pokemons across type 1')
autolabel(bars,90)
plt.show()


# In[ ]:


fig,((ax1,ax2,ax3), (ax4,ax5,ax6)) = plt.subplots(2, 3,figsize=(20, 10), sharex=False, sharey=True)
axs = [ax1,ax2,ax3,ax4,ax5,ax6]
i=1
for ax in axs:
    bars = ax.bar(data.groupby(["Generation","Type 1"]).count().loc[i].index, data.groupby(["Generation","Type 1"]).count().loc[i]["Name"],color="lightgrey",alpha=0.8)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_title("Generation "+str(i), y = 0.7)
    autolabel(bars,17)
    for spine in ax.spines.values():
        spine.set_visible(False)
    x = ax.xaxis
    i = i+1
    for item in x.get_ticklabels():
        item.set_rotation(90)
plt.show()


# #### Now we look on the legenadry

# In[ ]:


legendary = data[data["Legendary"]==True]
fig,(ax1,ax2) = plt.subplots(1, 2,figsize=(20, 10), sharex=False, sharey=True)
ax=ax1
ax.set_title("Legendary and Genaration",y = 1)
ba1 = ax.bar(legendary["Generation"].unique(), legendary.groupby("Generation").count()["Name"],color="lightgrey",alpha=0.8)
autolabel(ba1,17)
ax=ax2
ax.set_title("Legendary and Type 1",y = 1)
ba2 = ax.bar(legendary["Type 1"].unique(), legendary.groupby("Type 1").count()["Name"],color="lightgrey",alpha=0.8)
x = ax.xaxis
for item in x.get_ticklabels():
    item.set_rotation(45)
autolabel(ba2,12)
ax1.axes.get_yaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(False)
for spine in ax1.spines.values():
    spine.set_visible(False)
for spine in ax2.spines.values():
    spine.set_visible(False)
plt.show()


# ### I hope next graph is easy to understand. It is comparing mean of ordinary and legendary pokemon.

# In[ ]:


legendary = data[data["Legendary"]==True]
notlegendary = data[data["Legendary"]==False]
plt.figure(figsize=(15,10))

plt.plot(notlegendary.groupby("Type 1").mean().index,notlegendary.groupby("Type 1").mean()["Defense"],label="Nonlegendary Defence",alpha=0.6)
plt.plot(notlegendary.groupby("Type 1").mean().index,notlegendary.groupby("Type 1").mean()["Attack"],label="Nonlegendary Attack",alpha=0.6)

plt.scatter(legendary.groupby("Type 1").mean().index,legendary.groupby("Type 1").mean()["Attack"],alpha=1,color='red',label="Legendary attack")
plt.scatter(legendary.groupby("Type 1").mean().index,legendary.groupby("Type 1").mean()["Defense"],alpha=1,color='blue',label='Legendary defense')

ax = plt.gca()
ax.xaxis.grid(True,alpha=0.4)
ax.yaxis.grid(True,alpha=0.4)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.gca().fill_between(notlegendary.groupby("Type 1").mean().index, 
                       notlegendary.groupby("Type 1").mean()["Attack"], notlegendary.groupby("Type 1").mean()["Defense"], 
                       facecolor='grey', 
                       alpha=0.2)
plt.title("Pokemon mean attack and defense,legendary and nonlegendary")
plt.legend()
plt.show()


# ### Now basic histograms

# In[ ]:


fig, ((ax1,ax2,ax3), (ax4,ax5,ax6))  = plt.subplots(2, 3,figsize=(20,15) ,sharex=True,sharey=True)
axs = [ax1,ax2,ax3,ax4,ax5,ax6]
names = ["HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]
i=0
for ax in axs:
    ax.hist(data[names[i]])
    ax.yaxis.grid(True,alpha=0.4)
    ax.set_title(names[i])
    for spine in ax.spines.values():
        spine.set_visible(False)
    i = i+1
plt.show()


# In[ ]:


plt.figure()
plt.hist(data["Total"])
ax = plt.gca()
ax.yaxis.grid(True,alpha=0.4)
ax.set_title("Total")
for spine in ax.spines.values():
    spine.set_visible(False)
plt.show()


# ### Now some basic scatterplots. Maybe it is not so pretty but it does its job.

# In[ ]:



fig, (ax1,ax2)  = plt.subplots(1, 2,figsize=(14,8) ,sharex=True,sharey=True)
ax1.scatter(data["Total"],data["Attack"])
ax1.set_title("Total(x) and Attack(y)")
ax2.scatter(data["Total"],data["Defense"])
ax2.set_title("Total(x) adn Defense(y)")
plt.show()


# ### Now some 2d histograms. We clearly see most popular combination of those stats.

# In[ ]:


fig, (ax1,ax2)  = plt.subplots(1, 2,figsize=(15,6) ,sharex=False,sharey=False)
h = ax1.hist2d(data['Attack'], data['Defense'],bins=25 )
ax1.set_title("Attack(x) and Defense(y)")
plt.colorbar(h[3], ax=ax1)
h = ax2.hist2d(data['HP'], data['Total'],bins=25 )
ax2.set_title("HP(x) and Total(y)")
plt.colorbar(h[3], ax=ax2)
plt.show()


# ### And some boxplots. At first they were hard to understand, but they are useful.

# In[ ]:


plt.figure(figsize=(10,5))
box = plt.boxplot([data['HP'], data['Attack'],data["Defense"],data["Sp. Atk"],data["Sp. Def"],data["Speed"] ] , patch_artist=True)
ax = plt.gca()
ax.set_xticklabels(('HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def','Speed'))
for spine in ax.spines.values():
    spine.set_visible(False)
ax.yaxis.grid(True,alpha=0.4)
plt.setp(box["boxes"], facecolor="lightgrey")
plt.show()


# In[ ]:


plt.figure(figsize=(5,4))
box = plt.boxplot(data['Total'] ,patch_artist=True)
plt.setp(box["boxes"], facecolor="lightgrey")
ax = plt.gca()
ax.set_xticklabels(('Total',''))
ax.yaxis.grid(True,alpha=0.4)
for spine in ax.spines.values():
    spine.set_visible(False)
plt.show()


# ### And density function. Without it I would have not know that Total one has two peaks. I guess some pokemons are better than others.

# In[ ]:


ax=desc.plot.kde(figsize=(15,10))
for spine in ax.spines.values():
    spine.set_visible(False)
ax.yaxis.grid(True,alpha=0.4)


# ### Jointplots are easy to do but I do not know a way to show them in one row.

# In[ ]:


data2 = data.drop(["Name","Type 2","Type 1","Legendary","Generation"],axis=1)
sns.jointplot(data2["Total"], data2["HP"], kind='hex');
sns.jointplot(data2["Total"], data2["HP"], kind='kde');


# ### Violinplots are for now my most beloved boxplots.

# In[ ]:


plt.figure(figsize=(20,10))
plt.subplot(231)
sns.violinplot('Generation', 'Total', data=data);
plt.subplot(232)
sns.violinplot('Generation', 'HP', data=data);
plt.subplot(233)
sns.violinplot('Generation', 'Attack', data=data);
plt.subplot(234)
sns.violinplot('Generation', 'Defense', data=data);
plt.subplot(235)
sns.violinplot('Generation', 'Sp. Atk', data=data);
plt.subplot(236)
sns.violinplot('Generation', 'Sp. Def', data=data);


# #### At the end I wanted to see how much legendary pokemons are different that normal ones 

# In[ ]:


datax = data.drop(["Name","Type 1","Type 2","Generation"],axis=1)
_=sns.pairplot(datax, hue='Legendary', diag_kind='kde', height=2)
_=10


# ### I also started learning about Regresion , I would like to try predict Total 

# #### First thing correlations between feature. We see that Sp. Atk has the most corr. with Total.

# In[ ]:


df = pd.DataFrame(data,columns=['Total','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed'])
corrMatrix = df.corr()
f, ax = plt.subplots(figsize=(8, 6))
ax = sns.heatmap(corrMatrix, annot=True)
plt.show()


# In[ ]:


regresX = data.loc[:,"Sp. Atk":]
regresy = pd.DataFrame(data.loc[:,"Total"])


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(pd.DataFrame(regresX.loc[:,"Sp. Atk"]), regresy,
                                                   random_state = 0)
linreg = LinearRegression().fit(X_train, y_train)


# #### Linear regresion with one feature is easy to plot so I will start with it. Sp. Atk = feature , Total = target

# In[ ]:


x = np.array(regresX["Sp. Atk"])
plt.figure(figsize=(10,8))
plt.scatter(regresX.loc[:,"Sp. Atk"], regresy, marker= 'o', s=50, alpha=0.8)
plt.plot(regresX.loc[:,"Sp. Atk"], linreg.coef_ * x.reshape(-1,1) + linreg.intercept_, 'r-')
plt.title('Least-squares linear regression,R-squared score (test): {:.3f}'.format(linreg.score(X_test, y_test)))
plt.xlabel('Sp. Atk')
plt.ylabel('Total')
ax = plt.gca()
ax.xaxis.grid(True,alpha=0.4)
ax.yaxis.grid(True,alpha=0.4)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.show()


# #### I am interested how much different it is for generations and if pokemons are legendary or not.
# #### There is a big variance with legendary pokemons.

# In[ ]:


sns.set_style('whitegrid') 
_=sns.lmplot(x ='Sp. Atk', y ='Total', data = data,height=6,hue ='Legendary', markers =['o', 'v'],row ='Generation')


# In[ ]:


regresX2 = data.loc[data["Legendary"]==False,"Sp. Atk"]
regresy2 = data.loc[data["Legendary"]==False,"Total"]


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(pd.DataFrame(regresX2), pd.DataFrame(regresy2),
                                                   random_state = 0)
linreg = LinearRegression().fit(X_train, y_train)


# #### I would think that getting read of legendary pokemnos and doing regression only on ordinary pokemons will get me better score, but apparently this is not the case.

# In[ ]:


x = np.array(regresX2)
plt.figure(figsize=(10,8))
plt.scatter(regresX2, regresy2, marker= 'o', s=50, alpha=0.8)
plt.plot(regresX2, linreg.coef_ * x.reshape(-1,1) + linreg.intercept_, 'r-')
plt.title('Least-squares linear regression,R-squared score (test): {:.3f}'.format(linreg.score(X_test, y_test)))
plt.xlabel('Sp. Atk')
plt.ylabel('Total')
ax = plt.gca()
ax.xaxis.grid(True,alpha=0.4)
ax.yaxis.grid(True,alpha=0.4)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.show()


# In[ ]:




