# %% [markdown]
# # About DataSet
# Blog Authorship Corpus
# Over 600,000 posts from more than 19 thousand bloggers
# The Blog Authorship Corpus consists of the collected posts of 19,320 bloggers gathered from
# blogger.com in August 2004. The corpus incorporates a total of 681,288 posts and over 140 million
# words - or approximately 35 posts and 7250 words per person.
# Each blog is presented as a separate file, the name of which indicates a blogger id# and the
# blogger�s self-provided gender, age, industry, and astrological sign. (All are labeled for gender and
# age but for many, industry and/or sign is marked as unknown.)
# 
# 
# All bloggers included in the corpus fall into one of three age groups:
# 8240 "10s" blogs (ages 13-17),
# 8086 "20s" blogs(ages 23-27),
# 2994 "30s" blogs (ages 33-47)
# 
# For each age group, there is an equal number of male and female bloggers.
# Each blog in the corpus includes at least 200 occurrences of common English words. All formatting
# has been stripped with two exceptions. Individual posts within a single blogger are separated by the
# date of the following post and links within a post are denoted by the label urllink.
# Link to dataset: https://www.kaggle.com/rtatman/blog-authorship-corpus

# %% [code]
#Importing all libraries that are being used in the solution
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')
from collections import Counter
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score,classification_report
from sklearn.multiclass import OneVsRestClassifier

# %% [markdown]
# # Reading DataSet

# %% [code]
#df_temp=pd.read_csv('C:/Users/AbhishekDhingra/Downloads/blog-authorship-corpus/blogtext.csv',error_bad_lines=False)
df_temp=pd.read_csv('../input/blog-authorship-corpus/blogtext.csv')
# %% [markdown]
# # Dataset is humongous, with the current processing power , it is almost impossible to train on the whole dataset, hence I am picking up first 10000 data items for train and testing 

# %% [code]
df=df_temp.iloc[0:10000,]

# %% [markdown]
# # Displaying first 7 items from the data items

# %% [code]
df.head(7)

# %% [markdown]
# # Perfroming EDA, Where i tried to do the following 
# 1) Get Shape
# 2) Check if there is NULL or NA items in the dataset

# %% [code]
df.shape

# %% [code]
df['id'].nunique()

# %% [code]
df.isnull().sum()

# %% [code]
df.isna().sum()

# %% [code]
df.info()

# %% [markdown]
# # Removing special characters from the dataset 'text' using the 're" library

# %% [code]
df['text']=df['text'].apply(lambda x : re.sub('[@,.,^,$,*,?,\,/,\n,\t,<,>,&,:,\(,\),+,\-,!,+,-,\']','',x))

# %% [code]
df.head()

# %% [raw]
# Converting every character to lower case characters and striping spaces from each feature

# %% [code]
for col in df.columns:
    temp=df[col]
    if temp.dtype == object:
        df[col]=df[col].apply(lambda x : x.lower())
        df[col]=df[col].apply(lambda x : x.strip())
        

# %% [code]
df.head()

# %% [markdown]
# # Creating a new dataframe with a name "df_text" with only 'text' feature from the df dataset, later i will assiging this back to the orginal feature in the original dataset.
# Intention for the below procedure is to remove stopwords from the 'text' feature

# %% [code]
frame={'text' : df['text']}
df_text=pd.DataFrame(frame)

# %% [code]
df_text.head()

# %% [code]
df_text['text'][0]

# %% [markdown]
# # Below Logic will remove the stopwords from the feature 'text' in the new dataframe, however this will create a list of words instead of full sentence. Later i have another logic which will reconvert the list of words to the sentence

# %% [code]
word_tokens=[]
stop_words=set(stopwords.words('english'))
for i in range(0,df_text.shape[0]):
    fil=[]
    word_tokens=word_tokenize(df_text['text'][i])
    for w in word_tokens:
        if w not in stop_words:
            fil.append(w)
            
    df_text['text'][i]=fil

# %% [markdown]
# # Assiging list of words to the original dataset

# %% [code]
df['text']=df_text['text']

# %% [code]
df.head()

# %% [markdown]
# # Converting list of words to sentence in the original dataset, brining back data to its original form

# %% [code] {"scrolled":true}
for i in range(0,df.shape[0]):
    s=' '
    df['text'][i]=s.join(df['text'][i])
         

# %% [code]
df.head()

# %% [markdown]
# # Dropping Data from the original dataset

# %% [code]
df.drop('date',inplace=True,axis=1)

# %% [markdown]
# # Creating new feature in the original dataset with the name labels, This will contain the list generated by concatenating the follwoing four featurs
# 1) Gender
# 2) Age
# 3) Topic
# 4) Sign

# %% [code]
df['labels']=' '

# %% [code]
df.head()

# %% [markdown]
# # Age is Numeric , Converting it to str. This is required when leveraging  Multibinarizer

# %% [code]
df['age']=df['age'].astype('str')

# %% [markdown]
# # Below logic will create a list of items by concatenating "Gender", "Age", "Topic", "Sign" and assign it to the new label feature

# %% [code]
for i in range(0,df.shape[0]):
    new_label=[]
    new_label.append(df['gender'][i])
    new_label.append(df['age'][i])
    new_label.append(df['topic'][i])
    new_label.append(df['sign'][i])
    df['labels'][i]=new_label

# %% [code]
df.head()

# %% [code]
df.info()

# %% [markdown]
# # Droping the following features from the dataset
# 1) ID
# 
# 2) Gender
# 
# 3) Age
# 
# 4) Topic
# 
# 5) Sign

# %% [code]
df.drop(['id','gender','age','topic','sign'],inplace=True,axis=1)

# %% [code]
#for i in range(0,df.shape[0]):
#    new_label=[]
#    new_label.append([df['gender'][i],df['age'][i],df['topic'][i],df['sign'][i]])
#    df['labels'][i]=list(new_label)

# %% [markdown]
# # Now Orginal dataset is left with only 2 features.
# 
# 1) text
# 
# 2) labels

# %% [code]
df.head()

# %% [markdown]
# #  Segregating dataset into Independent and dependent features

# %% [code]
X=df['text']
y=df['labels']

# %% [markdown]
# 
# # Splitting dataset with default values

# %% [code]
X_train,X_test,y_train,y_test=train_test_split(X,y)

# %% [markdown]
# # Using Count vectorizer to create tokens from the data. requirement is tos use ngram range (1,2) 

# %% [code]
vect=CountVectorizer(ngram_range=(1,2))

# %% [markdown]
# # Creating  Document term matrix of Train and Test data

# %% [code]
X_train_dtm=vect.fit_transform(X_train)

# %% [code]
X_test_dtm=vect.transform(X_test)

# %% [code]
type(df["labels"][0])

# %% [markdown]
# # Below Logic will create frequency count of the unique label data. This logic will make use of collections library

# %% [code]
new_dict=dict()
gender=[]
age=[]
occ=[]
sign=[]

# %% [code]
for item in df['labels']:
    i=0
    for value in item:
        if i==0:
            gender.append(value)
        if i==1:
            age.append(value)
        if i==2:
            occ.append(value)
        if i==3:
            sign.append(value)
        i+=1
            
        

# %% [code]
dict_age=Counter(age)
dict_gender=Counter(gender)
dict_occ=Counter(occ)
dict_sign=Counter(sign)

# %% [code]
def merge_two_dicts(a, b, c, d):
    z = a.copy()   # start with x's keys and values
    z.update(b)    # modifies z with y's keys and values & returns None
    z.update(c)
    z.update(d)
    return z

# %% [markdown]
# # Below printed is the frequency of unique labels in the data, thisshows data is highly imbalance, that is why when calculating recall , precision ad f1 score, micro average is more suitable

# %% [code]
merge_two_dicts(dict_age, dict_gender, dict_occ, dict_sign)

# %% [code]
X_train.sample(5)

# %% [code]
X_test.sample(5)

# %% [markdown]
# # Document term matrix is the sparse matrix created on X_train and X_test data. Total tokens are 528134 

# %% [code]
X_train_dtm

# %% [code]
X_test_dtm

# %% [code]
y_train

# %% [markdown]
# # Implementing MultiLabelBinarizer to create binary labels from the list in the labels dataset

# %% [code]
mlb=MultiLabelBinarizer()

# %% [code]
y_train_mlb=mlb.fit_transform(y_train)

# %% [code]
y_test_mlb=mlb.transform(y_test)

# %% [markdown]
# # Below are the unique labels in the labels features. Count of unique labels are 64 (in 10000 dataset). It may change when you have less or more number of dataset 

# %% [code]
mlb.classes_

# %% [code]
y_test.head()

# %% [code]
y_test_mlb.shape

# %% [code]
mlb.classes_

# %% [markdown]
# # Creating Model using Logistic regression and onevsrestclassifier on top of the logistic regression

# %% [code]
LogReg_pipeline=Pipeline([('clf',OneVsRestClassifier(LogisticRegression(solver='lbfgs')))])

# %% [code]
LogReg_pipeline.fit(X_train_dtm,y_train_mlb)

# %% [code]
prediction = LogReg_pipeline.predict(X_test_dtm)

# %% [markdown]
# # Accuracy on the test data

# %% [code]
accuracy_score(y_test_mlb,prediction)

# %% [markdown]
# # Printing inverse data from the predicted labels

# %% [code]
mlb.inverse_transform(prediction[0:5,])

# %% [code]
y_test.head(5)

# %% [markdown]
# # Printing Recall, Precision and F1 Score from the data

# %% [raw]
# Default Precision, recall and fi_score works with Binary classification, Here requirement is to work with multiple labels, hence default values wont work. Hence 'micro' and 'macro' will be used. 
# Refernce https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html
# macro does not takes the imbalance classes into consideration and hence micro that is weighted matrics is considered more suitable

# %% [code]
recall_score(y_test_mlb,prediction,average='micro')

# %% [code]
recall_score(y_test_mlb,prediction,average='macro')

# %% [code]
precision_score(y_test_mlb,prediction,average='micro')

# %% [code]
precision_score(y_test_mlb,prediction,average='macro')

# %% [code]
f1_score(y_test_mlb,prediction,average='micro')

# %% [code]
f1_score(y_test_mlb,prediction,average='macro')

# %% [code]
print(classification_report(y_test_mlb,prediction))

# %% [markdown]
# # Printing True label and predicted Label for first 5 examples

# %% [code]
mlb.inverse_transform(prediction[10:15])

# %% [code]
y_test[10:15]