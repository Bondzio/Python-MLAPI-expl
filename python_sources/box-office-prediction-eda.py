#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis (EDA)

# ### **Importing the packages**

# In[ ]:


##Importing the packages
#Data processing packages
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

#Visualization packages
import matplotlib.pyplot as plt 
import seaborn as sns 
import datetime as dt
from wordcloud import WordCloud, STOPWORDS
from collections import OrderedDict

import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

#Machine Learning packages
from sklearn.svm import SVC,NuSVC
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix


# ### **Importing the data**

# In[ ]:


data = pd.read_csv("../input/train.csv")


# ### **Basic Analysis**

# In[ ]:


#Find the size of the data Rows x Columns
data.shape


# **COMMENTS:** The data consists of 3000 rows and 23 columns

# In[ ]:


#Display first 5 rows of Employee Attrition data
data.head()


# In[ ]:


#Find Basic Statistics like count, mean, standard deviation, min, max etc.
data.describe()


# In[ ]:


#Find the the information about the fields, field datatypes and Null values
data.info()


# **COMMENTS:**  Info fuction is used to list all the field names, their datatypes, count of elements in the field and if the field contacts Null values.

# ### **Dropping un-necessary columns which does not add value**

# In[ ]:


#first removing features which are irrelevant for our prediction
data.drop(['id', 'imdb_id', 'original_title', 'poster_path', 'title', 'Keywords'],axis=1,inplace=True)


# ### **Find column names, row count of non-null values, data-type**

# In[ ]:


data.info()


# **COMMENTS:**  From the above output we see that there are missing values in some fields like **belongs_to_collection, homepage** etc

# ### **Study the impact of _homepage_ on _revenue_**

# In[ ]:


#Converting null values in "homepage" to "0" and others to "1" and insert new column "has_homepage"
data['has_homepage'] = 0
data.loc[data['homepage'].isnull() == False, 'has_homepage'] = 1
data=data.drop(['homepage'],axis =1) #Drop the original column

#Homepage v/s Revenue
sns.catplot(x ='has_homepage', y ='revenue', data=data);
plt.title('Revenue for film with and without homepage');


# ### **Study the impact of _collection_ on _revenue_**

# In[ ]:


#Converting null values in "belongs_to_collection" to "0" and others to "1" and insert new column "collection"
data['collection'] = 0
data.loc[data['belongs_to_collection'].isnull() == False, 'collection'] = 1
data=data.drop(['belongs_to_collection'],axis =1) #Drop the original column

#collections v/s Revenue
sns.catplot(x= 'collection', y ='revenue', data=data);
plt.title('Revenue for film with and without collection');


# ### **Study the impact of _overview_ on _revenue_**

# In[ ]:


#Mapping overview present to 1 and nulls to 0
data['overview']=data['overview'].apply(lambda x: 0 if pd.isnull(x) else 1)

#overview v/s Revenue
sns.catplot(x='overview', y='revenue', data=data);
plt.title('Revenue for film with and without overview');


# ### **Study the impact of _budget_ on _revenue_**

# In[ ]:


#normalizing budget
a, b = 1, 100
m, n = data.budget.min(), data.budget.max()
data['budget'] = (data.budget - m) / (n - m) * (b - a) + a

#Budget vs Revenue
plt.figure(figsize=(24,6))
plt.subplot(121); sns.scatterplot(x="budget", y="revenue", data=data)
plt.subplot(122); sns.regplot(x="budget", y="revenue", data=data)


# **COMMENT:** The relation between budget and revenue are more or less Linear with some outliers

# ### **Correlation between _revenue, budget, popularity and runtime_**

# In[ ]:


#check correlation between variables
col = ['revenue','budget','popularity','runtime']
plt.subplots(figsize=(10, 8))
corr = data[col].corr()
sns.heatmap(corr, xticklabels=col,yticklabels=col, linewidths=.5, cmap="Reds")


# **COMMENT:** There is strong correlation between **Budget** and **Revenue** (Red color).  There is moderate correlation between **Budget** and **Popularity** (Light Red color)

# ### **Study the impact of _Genre on _revenue_**

# In[ ]:


#Exploring Genres
#Finding the count of name field in the dictionary of the foramt [{'id': 18, 'name': 'Drama'}]
genres = {}
for i in data['genres']:
    if(not(pd.isnull(i))): #Do this only if value is not-null (there are 7 null values)
        if (eval(i)[0]['name']) not in genres: #if the word(genres) is not already already in the dictionary then initialize it to 1
            genres[eval(i)[0]['name']]=1
        else:
                genres[eval(i)[0]['name']]+=1 #if the word(genres) is in the dictionary then increment the count by 1
print(genres) #Print the Genres and their count

plt.figure(figsize = (12, 8))
wordcloud = WordCloud(background_color="white",width=1000,height=1000, max_words=10,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(genres)
plt.imshow(wordcloud)
plt.title('Top genres')
plt.axis("off")
plt.show()


# **COMMENT:** Top genres are Drama, Comedy, Action, Horror & Adventure

# In[ ]:


#adding number of genres for each movie
genres_count=[]
for i in data['genres']:
    if(not(pd.isnull(i))):
        genres_count.append(len(eval(i)))
    else:
        genres_count.append(0)
data['num_genres'] = genres_count


# In[ ]:


#Genres v/s revenue
sns.catplot(x='num_genres', y='revenue', data=data);
plt.title('Revenue for different number of genres in the film');


# **COMMENT:** If the number of genres are equal to "3" the Revenue is maximum.

# In[ ]:


#Dropping genres
data.drop(['genres'],axis=1, inplace = True)


# ### **Study the impact of _no. of Production Companies_ on _Revenue_**

# In[ ]:


#Production companies
#Adding production_companies count for  data
prod_comp_count=[]
for i in data['production_companies']:
    if(not(pd.isnull(i))):
        
        prod_comp_count.append(len(eval(i)))
        
    else:
        prod_comp_count.append(0)
data['num_prod_companies'] = prod_comp_count


# In[ ]:


#number of prod companies vs revenue
sns.catplot(x='num_prod_companies', y='revenue', data=data);
plt.title('Revenue for different number of production companies in the film');


# **COMMENT:** The **Revenue** is higher if the **no. of Production Companies** are between **2 to 5**

# ### **Study the impact of _no. of Production Countries_ on _Revenue_**

# In[ ]:


#Dropping production_companies
data.drop(['production_companies'],axis=1, inplace = True)


# In[ ]:


#production_countries
#Adding production_countries count for  data
prod_coun_count=[]
for i in data['production_countries']:
    if(not(pd.isnull(i))):
        
        prod_coun_count.append(len(eval(i)))
        
    else:
        prod_coun_count.append(0)
data['num_prod_countries'] = prod_coun_count


# In[ ]:


#number of prod countries vs revenue
sns.catplot(x='num_prod_countries', y='revenue', data=data);
plt.title('Revenue for different number of production countries in the film');


# **COMMENT:** The **Revenue** is higher if the **no. of Production Countries** are between **1 to 3**

# In[ ]:


#Dropping production_countries
data.drop(['production_countries'],axis=1, inplace = True)


# ### **Study the impact of _no. of Cast members_ on _Revenue_**

# In[ ]:


#cast
#Adding cast count for  data
total_cast=[]
for i in data['cast']:
    if(not(pd.isnull(i))):
        
        total_cast.append(len(eval(i)))
        
    else:
        total_cast.append(0)
data['cast_count'] = total_cast


# In[ ]:


#(No. of Cast members) vs Revenue
plt.figure(figsize=(24,6))
plt.subplot(121); 
sns.scatterplot(x="budget", y="revenue", data=data); 
plt.title('Number of cast members vs revenue');
plt.subplot(122); 
sns.regplot(x="budget", y="revenue", data=data);
plt.title('Number of cast members vs revenue');


# **COMMENT:** The relation between **no. of Cast members** and **Revenue** are more or less Linear with some outliers

# In[ ]:


#Dropping cast
data= data.drop(['cast'],axis=1)


# ### **Study the impact of _no. of Crew members_ on _Revenue_**

# In[ ]:


#crew
total_crew=[]
for i in data['crew']:
    if(not(pd.isnull(i))):
        
        total_crew.append(len(eval(i)))
        
    else:
        total_crew.append(0)
data['crew_count'] = total_crew


# In[ ]:


#(No. of Crew members) vs Revenue
plt.figure(figsize=(24,6))
plt.subplot(121); 
sns.scatterplot(x="crew_count", y="revenue", data=data); 
plt.title('Number of crew members vs revenue');
plt.subplot(122); 
sns.regplot(x="crew_count", y="revenue", data=data);
plt.title('Number of crew members vs revenue');


# **COMMENT:** The relation between **no. of Crew members** and **Revenue** are more or less Linear with some outliers

# In[ ]:


#Dropping crew
data= data.drop(['crew'],axis=1)


# ### **Study the impact of _no. of Languages_ on _Revenue_**

# In[ ]:


plt.figure(figsize=(24,6))
sns.barplot(x='original_language', y='revenue', data=data)
plt.title('Revenue by language');


# **COMMENT:** It can be seen from the above plot that **English(en)** and **Chinese(zh)** generate more **Revenue** as compared to other languages.

# In[ ]:


#Taking only en and zh into consideration as they are the highest grossing
data['original_language'] =data['original_language'].apply(lambda x: 1 if x=='en' else(2 if x=='zh' else 0))


# ### **Study the impact of _Release date_ on _Revenue_**

# In[ ]:


#Check how revenue depends of day
data['release_date']=pd.to_datetime(data['release_date'])


# In[ ]:


release_day = data['release_date'].value_counts().sort_index()
release_day_revenue= data.groupby(['release_date'])['revenue'].sum()
release_day_revenue.index=release_day_revenue.index.dayofweek
sns.barplot(release_day_revenue.index,release_day_revenue, data = data,ci=None)
plt.show()


# **COMMENT:** It can be seen from the above plot that the **Revenue** is higher if the **Release date** is **WED**.  (0-MON, 1-TUE, ... 6-SUN)

# In[ ]:


#adding day feature to the data
data['release_day']=data['release_date'].dt.dayofweek 


# In[ ]:


data.drop(['release_date'],axis=1,inplace=True)


# ### **Study the impact of _Status(Released/Rumored)_ on _Revenue_**

# In[ ]:


#status
print(data['status'].value_counts())
sns.catplot(x="status", y="revenue", data=data);


# **COMMENT:** From the above output it can be seen that **Released** generates more *Revenue*.  This is **but obvious** as without releasing the movie, revenue cannot be generated.  This feature is **irrelevant**

# In[ ]:


#Feature is irrelevant hence dropping
data=data.drop(['status'],axis=1)


# ### **Study the impact of _Tagline_ on _Revenue_**

# In[ ]:


#tagline
data['isTaglineNA'] = 0
data.loc[data['tagline'].isnull() == False, 'isTaglineNA'] = 1
data.drop(['tagline'],axis=1,inplace =True)

#Homepage v/s Revenue
sns.catplot(x='isTaglineNA', y='revenue', data=data);
plt.title('Revenue for film with and without tagline');


# **COMMENT:** From the above output, it is clear that movies with **tagline** generates more **revenue**

# ### **Study the impact of _Runtime_ on _Revenue_**

# In[ ]:


#runtime has 2 nulls; setting it to the mean
#filling nulls in test
data['runtime']=data['runtime'].fillna(data['runtime'].mean())


# In[ ]:


sns.scatterplot(x="runtime", y="revenue", data=data); 
plt.title('Runtime vs revenue');


# **COMMENT:** From the above output, it can be seen that maximum revenue is generated when the **runtime** is around **150mins**

# ### **Study the impact of _no. of Spoken Languages_ on _Revenue_**

# In[ ]:


#spoken languages
#adding number of spoken languages for each movie
spoken_count=[]
for i in data['spoken_languages']:
    if(not(pd.isnull(i))):
        
        spoken_count.append(len(eval(i)))
        
    else:
        spoken_count.append(0)
data['spoken_count'] = spoken_count

data.drop(['spoken_languages'],axis=1,inplace=True)#dropping spoken_languages


# In[ ]:


sns.scatterplot(x="spoken_count", y="revenue", data=data); 
plt.title('Spoken Count vs revenue');


# **COMMENT:** From the above output, it is seen that maximum **Revenue** is generated if the **no. of Spoken Languages** are between 1 to 2

# In[ ]:


data.info()


# Traning the model
# 

# In[ ]:


X = data.drop(['revenue'],axis=1)
y = data.revenue


# In[ ]:


X.head()


# ### **Scaling the data values to standardize the range of independent variables**

# In[ ]:


#Feature scaling is a method used to standardize the range of independent variables or features of data.
#Since the range of values of raw data varies widely, in some machine learning algorithms, objective functions will not work properly without normalization. 
from sklearn.preprocessing import StandardScaler
scale = StandardScaler()
X = scale.fit_transform(X)


# ### **Split the data into Training set and Testing set**

# In[ ]:


# Split the data into Training set and Testing set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size =0.2,random_state=42)


# ### **Function definition**

# In[ ]:


#Function to Train and Test Machine Learning Model
def train_test_ml_model(X_train,y_train,X_test,Model):
    model.fit(X_train,y_train) #Train the Model
    y_pred = model.predict(X_test) #Use the Model for prediction

    # Test the Model
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test,y_pred)
    accuracy = round(100*np.trace(cm)/np.sum(cm),1)

    #Plot/Display the results
    cm_plot(cm,Model)
    print('Accuracy of the Model' ,Model, str(accuracy)+'%')


# In[ ]:


#Function to plot Confusion Matrix
def cm_plot(cm,Model):
    plt.clf()
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Wistia)
    classNames = ['Negative','Positive']
    plt.title('Comparison of Prediction Result for '+ Model)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    tick_marks = np.arange(len(classNames))
    plt.xticks(tick_marks, classNames, rotation=45)
    plt.yticks(tick_marks, classNames)
    s = [['TN','FP'], ['FN', 'TP']]
    for i in range(2):
        for j in range(2):
            plt.text(j,i, str(s[i][j])+" = "+str(cm[i][j]))
    plt.show()


# ### **PERFORM PREDICTIONS USING MACHINE LEARNING ALGORITHMS**

# In[ ]:


from sklearn.svm import SVC,NuSVC  #Import packages related to Model
Model = "SVC"
model=SVC() #Create the Model

train_test_ml_model(X_train,y_train,X_test,Model)


# In[ ]:


from xgboost import XGBClassifier  #Import packages related to Model
Model = "XGBClassifier()"
model=XGBClassifier() #Create the Model

train_test_ml_model(X_train,y_train,X_test,Model)


# model 1 - linear Regression

# In[ ]:


#from sklearn.linear_model import LinearRegression
#clf = LinearRegression()
#scores = cross_val_score(clf, X, y, scoring="neg_mean_squared_error", cv=10)
#rmse_scores = np.sqrt(-scores)
#print(rmse_scores.mean())


# Model 2 - Random forest regression

# In[ ]:


#from sklearn.ensemble import RandomForestRegressor
#regr = RandomForestRegressor(max_depth=2, random_state=0,n_estimators=100)
#scores = cross_val_score(regr, X, y, scoring="neg_mean_squared_error", cv=10)
#rmse_scores = np.sqrt(-scores)
#print(rmse_scores.mean())


# In[ ]:


#data.head()


# In[ ]:


#data.describe()


# In[ ]:


#regr.fit(X,y)
#y_pred2=regr.predict(X)
#importances = regr.feature_importances_


# In[ ]:


#importances

