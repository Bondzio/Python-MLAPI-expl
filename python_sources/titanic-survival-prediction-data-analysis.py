#!/usr/bin/env python
# coding: utf-8

# 
# 

# 

# ## 1 Importing the Libraries

# In[ ]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
sns.set(style="whitegrid")
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


# ML Libraries: 
from sklearn.preprocessing import OneHotEncoder

from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing


# In[ ]:


import plotly.figure_factory as ff
import plotly.offline as py 
import plotly.graph_objs as go 
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from plotly import tools 
py.init_notebook_mode (connected = True)

import cufflinks as cf
cf.go_offline()


# ## 2 Importing the Dataset and General View

# In[ ]:


dftrain = pd.read_csv("../input/train.csv")
dftest = pd.read_csv("../input/test.csv")


# ###### Lets Concatenate both the data frames for Exploratory Data Analysis :

# In[ ]:


df = pd.concat([dftrain, dftest], axis = 0 )


# In[ ]:


# Head of Training set:
dftrain.head(5)


# In[ ]:





# In[ ]:


# Breif information about the Data Sets
dftrain.info()
print("________________________________")
dftest.info()


# In[ ]:


# General Description about the Training Data set:
dftrain.drop(["PassengerId"], axis =1).describe()


# ##  3. Data Visualisation of Entire Data Frame (Training and Test Set)

# In[ ]:


classd= {1:"First Class", 2: "Second Class", 3: "Third Class"}
df["Class"] = df["Pclass"].map(classd)

first = df[df["Class"]=="First Class"]
sec = df[df["Class"]=="Second Class"]
thrd= df[df["Class"]=="Third Class"]

male= df[df["Sex"]=="male"]
female= df[df["Sex"]=="female"]


# ### 3. a.  SEX 

# In[ ]:


#1. Pie Chart for Sex count
sex_count = df["Sex"].value_counts()
print(sex_count)

colors = ['aqua', 'pink']

trace= go.Pie(labels = sex_count.index,
              values = sex_count.values, marker=dict(colors=colors))

layout = go.Layout(title = "Sex Distribution")

data = [trace]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# In[ ]:


# 1 Boxplot 
trace = go.Box(y = male["Fare"],fillcolor="aqua", name= "male" )
trace1 = go.Box(y = female["Fare"], fillcolor="pink", name= "female" )

layout = go.Layout(title="Fare distribution w.r.t Sex", yaxis=dict(title="Sex"), xaxis= dict(title="Fare"))

data=[trace, trace1]
fig = go.Figure(data = data, layout=layout)
py.iplot(fig)

# 2 Violin Plot 
trace1 = go.Violin( y = male["Fare"], fillcolor="aqua", name="Male")
trace2 = go.Violin( y = female["Fare"],fillcolor="pink", name="Female")

layout = go.Layout(title="Fare distribution w.r.t Sex", yaxis=dict(title="Fare"), xaxis= dict(title="Sex"))

data=[trace1, trace2]
fig = go.Figure(data = data, layout=layout)
py.iplot(fig)


# In[ ]:


#male= df[df["Sex"]=="male"]
#female= df[df["Sex"]=="female"]

# Box
trace = go.Box(y = male["Age"],fillcolor="aqua", name= "male" )
trace1 = go.Box(y = female["Age"], fillcolor="pink", name= "female" )
layout = go.Layout(title="Age w.r.t Sex", yaxis=dict(title="Age"), xaxis= dict(title="Sex"))

data=[trace, trace1]
fig = go.Figure(data = data, layout=layout)
py.iplot(fig)


# In[ ]:





# ### 2.b.  Class 

# In[ ]:


# Pie Chart
class_count = df["Class"].value_counts()
print(class_count)

colors = ["lightorange", "lightpurple", "lightgreen"]
trace = go.Pie( labels= class_count.index,values = class_count.values, marker = dict(colors = colors))

layout = go.Layout( title = "Total Class Distribution")

data= [trace]
fig = go.Figure(data= data, layout= layout)
py.iplot(fig)


# In[ ]:


# classd= {1:"First Class", 2: "Second Class", 3: "Third Class"}
#df["Class"] = df["Pclass"].map(classd)

# Bar Plot
trace1 = go.Bar(x=class_count.index, y= class_count.values, 
                marker=dict(
                color=dftrain["Age"],
                colorscale = 'Jet'))

layout1 = go.Layout(title = "Class Count" )

data= [trace1]
fig = go.Figure(data= data, layout= layout1)
py.iplot(fig)


#plt plot
plt.figure(figsize=(15,8))
sns.countplot(x= df["Class"], hue= df["Sex"], palette="seismic")
plt.title("Male/Sex per Class", fontsize = 18)
plt.xlabel("Class", fontsize = 18)
plt.ylabel("Count", fontsize = 18)
plt.show()



# In[ ]:


#first = dftrain[dftrain["Class"]=="First Class"]
#sec = dftrain[dftrain["Class"]=="Second Class"]
#thrd= dftrain[dftrain["Class"]=="Third Class"]

# Box plot
trace1 = go.Box( x = first["Fare"], fillcolor="yellow", name="First Class")
trace2 = go.Box( x = sec["Fare"],fillcolor="mediumpurple", name="Second Class")
trace3 = go.Box( x = thrd["Fare"], fillcolor="mistyrose", name="Third Class")

layout = go.Layout(title="Fare distribution w.r.t Class", yaxis=dict(title="Class"), xaxis= dict(title="Fare"))

data=[trace1, trace2, trace3]
fig = go.Figure(data = data, layout=layout)
py.iplot(fig)

# Violin Plot
trace1 = go.Violin( y = first["Fare"], fillcolor="yellow", name="First Class")
trace2 = go.Violin( y = sec["Fare"],fillcolor="mediumpurple", name="Second Class")
trace3 = go.Violin( y = thrd["Fare"], fillcolor="mistyrose", name="Third Class")

layout = go.Layout(title="Age distribution w.r.t Class", yaxis=dict(title="Fare"), xaxis= dict(title="Class"))

data=[trace1, trace2, trace3]
fig = go.Figure(data = data, layout=layout)
py.iplot(fig)

# violinplot
#plt.figure(figsize=(14,5))
#sns.violinplot(x = df["Class"], y=df["Age"], palette="magma")
#plt.xlabel("Class", fontsize =20)
#plt.ylabel("Age", fontsize =20)
#plt.title("Violin plot of Class w.r.t Age",fontsize =20)
#plt.show()


# In[ ]:


# Box Plot Age Vs Class
# Box plot
trace1 = go.Box( y = first["Age"], fillcolor="yellow", name="First Class")
trace2 = go.Box( y = sec["Age"],fillcolor="mediumpurple", name="Second Class")
trace3 = go.Box( y = thrd["Age"], fillcolor="lavender", name="Third Class")

layout = go.Layout(title="Age distribution w.r.t Class", yaxis=dict(title="Age"), xaxis= dict(title="Class"))

data=[trace1, trace2, trace3]
fig = go.Figure(data = data, layout=layout)
py.iplot(fig)


# ### 2.c. Age Distribution

# In[ ]:


# Age Bar plot 
age_count = df["Age"].dropna().value_counts()

trace = go.Bar(x = age_count.index,
              y = age_count.values, 
              marker = dict(color = df["Age"],
                           colorscale = "Jet", 
                           showscale = True))
layout = go.Layout(title = "Age Distribution", 
                  yaxis = dict(title = "Number of People"))
data = [trace]
fig = go.Figure(data = data, layout = layout)
py.iplot(fig)


# Age Vs Fare
'''trace=go.Scatter(x = df["Age"].dropna(), y=df["Fare"], mode = "markers", 
                marker = dict(size = 6, color = "lightgreen"))

layout = go.Layout(title ="Age to Fare Plot", xaxis= dict(title = "Age"), 
                   yaxis= dict(title = "Fare"))

data = [trace]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)'''

data = []
for i, j in zip(df['Class'].unique(), ['aqua', 'lime', 'tomato']):
    tempdf = df[df['Class'] == i]
    data.append(go.Scatter(x = tempdf['Age'].dropna(), y = tempdf['Fare'], mode = 'markers', 
                marker = dict(size = 6, color = j), name = i))

layout = go.Layout(title = 'Age to Fare Plot', xaxis = dict(title = 'Age'), 
                   yaxis = dict(title = 'Fare'))

fig = go.Figure(data = data, layout = layout)
py.iplot(fig)


# ###### 2.d. Joint plot: Distribution w.r.t to AGE & FARE

# In[ ]:



plt.figure(figsize=(14,5))
sns.jointplot(x=df["Age"], y=df["Fare"], kind="reg",
              color="purple", ratio=3, height=7,dropna= True)
plt.xlabel("Age", fontsize =16)
plt.ylabel("Fare", fontsize =16)
plt.title("Fare vs Age",fontsize =16)
plt.show()


# ### 2.e. Survived Plots

# In[ ]:


df["Survived"].value_counts()


# In[ ]:


# Survival count
sur_count = df["Survived"].value_counts()
trace1 = go.Bar(x=sur_count.index, y= sur_count.values, 
                marker=dict(
                color=df["Age"],
                colorscale = 'Portland'))

layout1 = go.Layout(title = "Class Count" )

data= [trace1]
fig = go.Figure(data= data, layout= layout1)
py.iplot(fig)


#  Looks like 1098 people did not survive, while around 684 people in both the dataset survived

# In[ ]:


# Survival with hue of Sex

fig, (ax1, ax2) = plt.subplots(2, figsize= (16,7))
sns.countplot(x="Survived", hue="Sex",  data=df, palette="magma", ax=ax1)
sns.countplot(x="Survived", hue="Class",  data=df, palette="magma", ax=ax2)

plt.show()
plt.tight_layout()


# We can see a trend here. It looks like people who couldn't survived were much more like to be male. While on the other hand people who survived are more likely to be female. 

# In[ ]:


plt.figure(figsize= (16,7))
sns.scatterplot(data=df, x="Age", y="Fare", hue="Sex")
plt.show()
plt.figure(figsize= (16,7))
sns.scatterplot(data=df, x="Age", y="Fare", hue="Survived")
plt.show()


# In[ ]:





# ### 2.f. Sibling and Spouse on board

# In[ ]:


sib_count = df["SibSp"].value_counts()
trace1 = go.Bar(x=sib_count.index, y= sib_count.values, 
                marker=dict(
                color=df["Age"],
                colorscale = 'Electric'))

layout1 = go.Layout(title = "Sibling and Spouse  Count" )

data= [trace1]
fig = go.Figure(data= data, layout= layout1)
py.iplot(fig)


# ###  2. g. Parent and child on board

# In[ ]:


# Count plot for number of sibling or Spouse aboard
par_count = df["SibSp"].value_counts()
trace1 = go.Bar(x=par_count.index, y= par_count.values, 
                marker=dict(
                color=df["Age"],
                colorscale = 'Cividis'))

layout1 = go.Layout(title = "Sibling and Spouse  Count" )

data= [trace1]
fig = go.Figure(data= data, layout= layout1)
py.iplot(fig)


# In[ ]:


data = [dftrain,dftest]
for dataset in data:
    dataset['relatives'] = dataset['SibSp'] + dataset['Parch']
    dataset.loc[dataset['relatives'] > 0, 'not_alone'] = 0
    dataset.loc[dataset['relatives'] == 0, 'not_alone'] = 1
    dataset['not_alone'] = dataset['not_alone'].astype(int)
dftrain['not_alone'].value_counts()


# In[ ]:


axes = sns.factorplot('relatives','Survived', 
                      data=dftrain, aspect = 2.5, )


# ###  3. g. Embarked Ship 

# In[ ]:


em_count = df["Embarked"].value_counts()
trace1 = go.Bar(x=em_count.index, y= em_count.values, 
                marker=dict(
                color=df["Age"],
                colorscale = 'Viridis'))

layout1 = go.Layout(title = "Sibling and Spouse  Count" )

data= [trace1]
fig = go.Figure(data= data, layout= layout1)
py.iplot(fig)


# In[ ]:


FacetGrid = sns.FacetGrid(df, row='Embarked', size=4.5, aspect=1.6)
FacetGrid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette=None,  order=None, hue_order=None )
FacetGrid.add_legend()


# ## 4 Data Visualisation for Data Preprocessing

# In[ ]:


fig, (ax1,ax2) = plt.subplots (2, figsize = (15,10))
sns.heatmap(dftest.isnull(), cmap="viridis", yticklabels=False
           ,cbar = False, ax= ax1) 
sns.heatmap(dftrain.isnull(), cmap="viridis", yticklabels=False
           ,cbar = False, ax= ax2)
plt.tight_layout()


# So we can check out that we're missing some age information and we are missing a lot of Cabin information. Roughly about 20 percent of that age data is missing and the proportion of age missing is likely small enough for a reasonable replacement of some form of imputation meaning I can actually use the knowledge of the other columns to fill in reasonable values for that age column. 
# Looking at the cabin column however it looks like we're just missing too much of that data to do something useful with it at a basic level. We're going to go ahead and probably drop this later or change it to send up some other feature like

# In[ ]:


total = df.isnull().sum().sort_values(ascending =False)
total.head(6)


# In[ ]:


# Creating a table of missing of values in the entire data frame: 
percentage = df.isnull().sum()/df.isnull().count()*100 
perc = (round(percentage,2)).sort_values(ascending = False)

missing = pd.concat([total, perc], axis = 1, keys=["Values", "Percentage %"])

missing.head()


# #### We can see from the above table the maximum missing values are in Cabin column followed by Age column. 

# In[ ]:





# # 5 Data Preprocessing

# ### 5.a.  Dealing with MISSING VALUES:

# In[ ]:


# on the basis of the box plot of age vs class. 
# We can impute the average age on the basis of that plot
def imput_age(col):
    Age = col[0]
    Pclass = col[1]
    
    if pd.isnull(Age):
        if Pclass == 1:
            return 37
        elif Pclass == 2:
            return 29 
        else:
            return 24
    else:
        return Age

dftrain["Age"] = dftrain[["Age", "Pclass"]].apply (imput_age, axis=1)
dftest["Age"] = dftest[["Age", "Pclass"]].apply (imput_age, axis=1)


# I tried to fill the missing values based of my age columns for both the data set ( Trainind & Test Set) 

# In[ ]:





# In[ ]:


fig, (ax1,ax2) = plt.subplots (2, figsize = (15,10))
sns.heatmap(dftest.isnull(), cmap="viridis", yticklabels=False
           ,cbar = False, ax= ax1) 
sns.heatmap(dftrain.isnull(), cmap="viridis", yticklabels=False
           ,cbar = False, ax= ax2)
plt.tight_layout()


# In[ ]:


dftest.head(5)


# ###### 5.B. ENCODING: Categorical Data

# In[ ]:


import re
deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "U": 8}
data = [dftrain, dftest]

for dataset in data:
    dataset['Cabin'] = dataset['Cabin'].fillna("U0")
    dataset['Deck'] = dataset['Cabin'].map(lambda x: re.compile("([a-zA-Z]+)").search(x).group())
    dataset['Deck'] = dataset['Deck'].map(deck)
    dataset['Deck'] = dataset['Deck'].fillna(0)
    dataset['Deck'] = dataset['Deck'].astype(int)


# In[ ]:





# In[ ]:


sex = pd.get_dummies(dftrain["Sex"], drop_first=True)
embark = pd.get_dummies(dftrain["Embarked"], drop_first=True)
clss = pd.get_dummies(dftrain["Pclass"], drop_first=True)


sext = pd.get_dummies(dftest["Sex"], drop_first=True)
embarkt = pd.get_dummies(dftest["Embarked"], drop_first=True)
clsst = pd.get_dummies(dftest["Pclass"], drop_first= True)


# In[ ]:


# Concatinating the new features to the Clear Trainig set:
train = pd.concat([dftrain, sex, embark, clss], axis =1)
train.head(1)


# In[ ]:


# Concatinating the new features to the Test set:
test = pd.concat([dftest, sext, embarkt, clsst], axis =1)
test.head(1)


# In[ ]:





# In[ ]:


data = [dftrain, dftest]
for dataset in data:
    dataset['Fare'] = dataset['Fare'].fillna(0)
    dataset['Fare'] = dataset['Fare'].astype(int)


# In[ ]:


# Dropping columns which are not required from training set
train.drop(["PassengerId", "Pclass","Name", "Sex","Ticket", "Cabin", "Embarked"], axis = 1,inplace = True)
train.head(1)


# In[ ]:


# Dropping columns which are not required from training set
test.drop(["PassengerId", "Pclass","Name" ,"Ticket","Sex", "Cabin", "Embarked"], axis = 1,inplace = True)
test.head(1)


# In[ ]:





# In[ ]:


fig, (ax1, ax2) = plt.subplots(2, figsize = (15,10))
sns.heatmap(train.corr(), annot= True, cmap= "magma", ax=ax1)
sns.heatmap(test.corr(), annot= True, cmap= "magma", ax=ax2)

plt.show()
plt.tight_layout()


# In[ ]:


fig, (ax1, ax2) = plt.subplots(2, figsize = (15,10))
sns.heatmap(train.isnull(), ax=ax1, yticklabels=False)
sns.heatmap(test.isnull(), yticklabels=False)
plt.show()


# ### 5.C. Creating Train & Test Split

# In[ ]:


X_train = train.drop("Survived", axis=1)
y_train = train["Survived"]
X_test = test.fillna(value = 7 )


# ### Features Scaling

# In[ ]:


columns = X_train.columns
column_test = X_test.columns


# In[ ]:



scaler = preprocessing.Normalizer()
X_train = scaler.fit_transform(X_train)
X_train = pd.DataFrame(X_train, columns=columns)

X_test = scaler.transform(X_test)
X_test = pd.DataFrame(X_test, columns=column_test)


# In[ ]:





# ## 6. Modeling 

# In[ ]:





# ### 6. a. Logistic Regression

# In[ ]:


log = LogisticRegression()
log.fit(X_train, y_train)

pred_log = log.predict(X_test)

log.score(X_train, y_train)
logistic_score = round(log.score(X_train, y_train)*100,2)
logistic_score


# In[ ]:





# ### 6.b. Random Forest

# In[ ]:


#from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
pred_random = rf.predict(X_test)

rf.score(X_train, y_train)

random_score = round(rf.score(X_train, y_train)*100,2)
random_score


# In[ ]:





# ### Decision Tree

# In[ ]:


tree = DecisionTreeClassifier()
tree.fit(X_train, y_train)

pred_tree = tree.predict(X_test)

tree.score(X_train, y_train)
tree_score = round(tree.score(X_train, y_train)*100,2)
tree_score


# In[ ]:





# ### 6.c KNN 

# In[ ]:


knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)
pred_knn = knn.predict(X_test)

knn.score(X_train, y_train)
knn_score = round(knn.score(X_train, y_train)*100,2)
knn_score


# ### Use Elbow Method to find the best value of k to get maximum accuracy:

# In[ ]:





# ### 6.d  Gaussian Naive Bayes

# In[ ]:


gaus = GaussianNB()
gaus.fit(X_train, y_train)
pred_gaus = gaus.predict(X_test)

gaus.score(X_train, y_train)
gaus_score = round(gaus.score(X_train, y_train)*100,2)
gaus_score


# In[ ]:





# ### 6.e. Perceptron:

# In[ ]:


per = Perceptron(max_iter=5)
per.fit(X_train, y_train)

perd_per = per.predict(X_test)

per.score(X_train, y_train)
perceptron_score = round(per.score(X_train, y_train) * 100, 2)
perceptron_score


# In[ ]:





#  ### 6.f Linear Support Vector Machine:

# In[ ]:


svc = LinearSVC()
svc.fit(X_train, y_train)

pred_svc = svc.predict(X_test)

svc.score(X_train, y_train)
svc_score = round(svc.score(X_train, y_train) * 100, 2)
svc_score


# In[ ]:





# In[ ]:





# ## Creating Data Frame of models scores:
# 

# In[ ]:


df_score = pd.DataFrame({"Models": ['Support Vector Machines', 'KNN', 'Logistic Regression', 
              'Random Forest', 'Naive Bayes', 'Perceptron',
              'Decision Tree'], 
                       "Score": [svc_score, knn_score, logistic_score, random_score, gaus_score, 
                                 perceptron_score, tree_score]})


# In[ ]:


df_score.sort_values(by= "Score", ascending=False)


# ## 7. Model Evaluation

# In[ ]:


from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# In[ ]:





# ##### Next step in order to increase the precision and get more accuracy. I will be doing more feature engineering such as trying to grab the title of the names, cabin letter and ticket information. 

# In[ ]:





# In[ ]:


rf = RandomForestClassifier()
rf.fit(X_train, y_train)
subm = rf.predict(X_test)


for_score = round(rf.score(X_train,y_train)*100,2)
for_score


# In[ ]:


'''sub_rep = pd.DataFrame({"PassengerId": dftest["PassengerId"], 
                       "Survived" : subm})
sub_rep.to_csv("TitSub.csv", index = False)'''


# In[ ]:





# In[ ]:





# In[ ]:




