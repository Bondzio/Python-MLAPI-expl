#!/usr/bin/env python
# coding: utf-8

# This is a continuation of my earlier Kaggle notebook https://www.kaggle.com/allohvk/captivating-conversations-with-the-titanic-dataset which was all about data exploration. In this very short notebook of less than 25 lines, we tackle the missing values in the Titanic dataset. This is one of the most hotly discussed topic. My aim here is to use simple well documented code to impute missing values with adequate commentary for the reasoning behind the decisions. Though the code is extremely easy to follow, the approach taken is sufficiently advanced and matches and maybe betters, the standards of the leaderboard in this competition.
# 
# Even someone who is new to ML, Python or Pandas should be able to understand this code. Every first time I use a new Panda or Python command, I explain the logic behind it. So in that respect, it will be much easier to follow this notebook if you have read the data exploration part first using the above link which explains the logic and syntax behind a few key commands like dataframe filters, groupby etc which we will be re-using here.
# 
# In case you want a bit of theory before you start you can refer to the following interesting dicussion on various approaches from basic to advanced on filling the missing Ages: https://www.kaggle.com/c/titanic/discussion/157929
# 
# If you want a 1-line approach to filling in the missing ages, just try:
# 
# [df['Age'].fillna(df.groupby(['Pclass','Sex','Title'])['Age'].transform('mean'), inplace=True) for df in [train_data, test_data]]
# 
# I will explain this 1-liner shortly, but we can do much better than just this. Let us start by merging the test and training dataset as there are some missing values in test dataset as well

# In[ ]:


import pandas as pd
import numpy as np
pd.set_option("display.max_rows", None, "display.max_columns", None)

test_data = pd.read_csv ('/kaggle/input/titanic/test.csv')
train_data = pd.read_csv("/kaggle/input/titanic/train.csv")

combined=train_data.append(test_data)

##We discussed the below command in detail the data exploration notebook
print('Missing values Percentage: \n\n', round (combined.isnull().sum().sort_values(ascending=False)/len(combined)*100,1))


# The biggest missing one is the missing Cabin info. As discussed earlier, since 70%+ values are missing, it does not make sense for us to fill in missing values.. There would just be too much noise in the ML model and we may actually get a lower score because of this. There are couple of 'Embarked' ports missing and 1 fare but the biggest thing we must tackle is the AGE feature. It has lot of missing values! 
# 
# We discussed that AGE is an important factor in determing survival..particularly the age group..Kids in general have a better chance of survival and older adults have a lower chance. So it is important to get this right. 
# 
# The simplest approach is to use the mean or median to fill all the missing ages. The mean age is around 30 (train_data.describe() gives this). Median too is similar as there are no outliers. However, one would be more accurate in imputing missing ages by calculating mean age of a group of '*similar passengers*'. For e.g., one could choose to calculate mean of Pclass1 passengers and assign it to all Pclass1 missing ages..and likeways for Pclass2 and Pclass3.
# 
# But we can further improvise on this. It is quite likely that (say) females on Pclass3 have a diff mean age than females on Pclass 1. So an even better approach (the one that most good scorers have taken) is to group people based on Sex+PClass. If one wants to further refine it, one could make use of the 'Title' and the PClass and it should give a slightly better result than Sex and Pclass. The 'Title' can be extracted from the name easily. So basically you calculate mean age for each *Pclass+Title* combination and assign this value to the missing ages for that *Pclass+Title* combination. The 'Title' also contains the MASTER prefix which can be used to identify boy children who have missing ages. Let us analyze this.

# In[ ]:


display(combined[(combined.Age.isnull()) & (combined.Name.str.contains('Master'))])


# As explained in the data exploration notebook, we are using a simple filter on the 'combined' dataframe to return all rows which contain 'Master' in the 'Name' column where Age is null.
# 
# There are 8 children and all are pClass=3 and male. If we had taken the simple approach of applying the mean()
# for every missing entry, we would have entered their ages as 30. But we know that they are Children. So they should be < 14 for sure and definitely not 30. What value should we fill as their mean age? One good option is to take the avg age of 'male children & use this as the default value for missing male children age in that class.

# In[ ]:


print(train_data[train_data.Name.str.contains('Master')]['Age'].mean())


# We only used train_data to prevent leakage of info from test to train data. We have used a filter to get all rows where Name contains 'Master'. We then use the .mean() function on this to get the mean value of age of all Male children in Pclass 3.
# 
# So 5 is a good average Age for these 8 boys which is a vast difference from the 30 we earlier wanted to go with.
# 
# Before we update the values for these 8 kids, let us do a quick sanity check. We know that these kids should ideally have non-zero Parch i.e. these small kids should not be travelling alone but travelling with at least 1 parent!

# In[ ]:


display((combined[(combined.Age.isnull()) & (combined.Name.str.contains('Master')) & (combined.Parch==0)]))


# In[ ]:


##So there are cases (just 1) where a child is travelling without either parents..
##Probably (travelling with nanny or relatives. We will just assume that the Child
##is little senior in age and cannot be 5. We will assign the max value of Master 
##which is around 14 for such cases.
test_data.loc[test_data.PassengerId==1231,'Age']=14


# We use the .loc command to update the value of 14 in the first case. The .loc function can be applied to a dataframe to access a group of rows and columns. Here we put a condition 'test_data.PassengerId==1231' to get the row we want and then update the column 'Age' with the value 14. 
# 
# If you are new to Panda but have experimented a little with filters and other basic commands, you may be tempted (like me) to try the below command:
# test_data[test_data.PassengerId==1231]['Age']=14
# 
# Unfortunately this will not work because we are NOT updating the actual dataframe but a 'copy' of the dataframe (which is temporarily created). Thankfully the error is pretty good and it actually asks you to use the .loc command to update the value. Unfortunately it is displayed the first time only.
# 
# The remaining ages will be filled up as a part of the common code. For that we need to extract the 'Title' from the name. This is achieved in 1 line of code

# In[ ]:


train_data['Title'], test_data['Title'] = [df.Name.str.extract         (' ([A-Za-z]+)\.', expand=False) for df in [train_data, test_data]]


# The code can be read from right to left and is a 'list comprehension' and is executed as follows:
# * 'for each dataframe df in list of dataframes'
# * 'extract title' 
# * 'store result in a new column in the 2 dataframes'
# 
# The first part is easily understandable: '*for each dataframe df in list of dataframes*'. Basically we have 2 dataframes the test_data and the train_data and we want to get the Title for both of those.
# 
# The second part is also understandable: "*extract title*". Here a regular regex filter is used to extract the Title and this function is run for every row of both the dataframes. No 'for' loop etc is needed. So now you have 2 lists generated. One list containing Title column for train_data and another for test_data.
# 
# The third part could be bit confusing: '*store result in a new column in the 2 dataframes*': Here the first list is stored as an additional column in the first dataframe - train_data and the second list is stored as an additional column in the second dataframe test_data. This is strictly ordered.. 
# 
# So if you do:
# 
# train_data['Title'], test_data['Title'] = [df.Name.str.extract(' ([A-Za-z]+)\.', expand=False) for df in [train_data, test_data]]
# 
# you end up with a mess and hours of debugging at a later stage. Try doing that and see how Pandas does not throw an error but just ignores the extra rows in the test_data and fills the extra rows in train_data with Nans.
# 
# Now let us print the avg age cross Titles and Pclass. We discussed the groupby Pandas command in detail in my data exploration notebook

# In[ ]:


train_data.groupby(['Title', 'Pclass'])['Age'].agg(['mean', 'count'])


# See how the mean age differs across Pclass. For e.g. avg age of 'Mrs' in Pclass 1 is 40 versus 33 in other Pclasses. We already discussed that for the Titanic dataset, it may not matter much, but these sort of differences could make all the difference between success and failure in other competitions. 
# 
# Also there are just too many titles. Let us consolidate and create a few important ones only else this will just unnecessarily cause too much noise. We do the consolidation in 1 line of code. Let us first create a Python dictionary to map the titles. The title to the right of the ':' are the final set of titles we will go with.

# In[ ]:


TitleDict = {"Capt": "Officer","Col": "Officer","Major": "Officer","Jonkheer": "Royalty",              "Don": "Royalty", "Sir" : "Royalty","Dr": "Royalty","Rev": "Royalty",              "Countess":"Royalty", "Mme": "Mrs", "Mlle": "Miss", "Ms": "Mrs","Mr" : "Mr",              "Mrs" : "Mrs","Miss" : "Miss","Master" : "Master","Lady" : "Royalty"}


# Doctor & Rev are not exactly Royalty but I tried matching age-group wherever possible. For this dataset we will make this assumption
# 
# Now we use list comprehensions as before. Here we do a mapping of the Title col to the corresponding value in the dictionary and retreieve the set of consolidated Titles in 1 simple line of code.

# In[ ]:


train_data['Title'], test_data['Title'] = [df.Title.map(TitleDict) for df in [train_data, test_data]]

##Let us now reprint the groups
train_data.groupby(['Title', 'Pclass'])['Age'].agg(['mean', 'count'])


# Much better. This is what will be fed to the missing ages. Let us check if all titles are covered...especially in test data set...esp since we created the dict based on values in the training_dataset

# In[ ]:


combined=train_data.append(test_data)
display(train_data[train_data.Title.isnull()])
display(test_data[test_data.Title.isnull()])

##There is Dona which is royalty which is not covered in test_data. Update the same
test_data.at[414,'Title'] = 'Royalty'


# Now all titles are in shape. We can groupby Pclass, Sex, Royalty and find the mean and then plug in all the missing Age values.
# 
# But let me ask a pertinent question. How much does the numerical value of age contribute to the survival? Let us say you spend hours writing some nifty code to arrive at an age of 31 instead of 38 for a missing age passenger (and it turns out her actual age happens to be 31). Will it make a lot of difference to her survival? The answer is NO. There are other factors which are far more important. HOWEVER the fact whether the person is a child or an adult or a senior citizen DOES play a critical role in survival. So long as one can categorize the missing ages as belonging to one of this group it is fine! In particular, we should be spending a lot more time worrying about whether the person in question (with the missing age) was a child or not? This makes a lot of difference to the survival chance. How do we do that? Well it is easy for male children because of the Title 'Master' which is prefixed to their names. But how do we identify a female child among the missing ages. There is no Title specific to female children. All unmarried females across all ages had the 'Miss' Title. So here is a simple way to identify such folks and impute their missing ages. I haven't seen it being used in any kernel so far (at least the ones I have gone thru' though). We can identify the such cases by checking the Parch flag. If Parch flag is >0 then they are most likely female children. 

# In[ ]:


print ("Avg age of 'Miss' Title", round(train_data[train_data.Title=="Miss"]['Age'].mean()))

print ("Avg age of 'Miss' Title travelling without Parents", round(train_data[(train_data.Title=="Miss") & (train_data.Parch==0)]['Age'].mean()))

print ("Avg age of 'Miss' Title travelling with Parents", round(train_data[(train_data.Title=="Miss") & (train_data.Parch!=0)]['Age'].mean()), '\n')


# See the HUGE difference! If we had used the average value without considering the Parch, we would have gone horribly wrong. Even here there is a huge gap between Pclasses and in our final age imputation which is 1 line of code, we impute the values based on Pclass, Sex and Title.
# We do this at the end..Before that let us quickly tackle the other missing values

# In[ ]:


##Let us turn our attention to the missing fare
display(combined[combined.Fare.isnull()])

##Let us get fare per person
for df in [train_data, test_data, combined]:
    df['PeopleInTicket']=df['Ticket'].map(combined['Ticket'].value_counts())
    df['FarePerPerson']=df['Fare']/df['PeopleInTicket']
##Valuecounts is the swissknife of Pandas and is deeply explained in my earlier notebook

##Just take the mean fare for the PORT S and the Pclass & fill it. Remember to consider FarePerPerson and not Fare
print('Mean fare for this category: ', train_data[(train_data.Embarked=='S') & (train_data.Pclass==3)]['FarePerPerson'].mean())


# Notice what happens when you replace the missing fare by the mean fare instead of mean fareperperson.
# 
# print(train_data[(train_data.Embarked=='S') & (train_data.Pclass==3)]['FarePerPerson'].mean())
# 
# The mean fare is almost DOUBLE the mean fareperperson for Port S Pclass3. This is because fare is actually the total fare for a group. These kind of small 'additional' efforts in determining the missing data will go a long way in helping with better results. However for the Titanic dataset, there is only one missing fare and in general fare does not play a very big role in survival (Pclass already accounts for that relationship). So this is more of an academic exercise.
# 
# In fact let us go the whole hog and consider mean fareperperson for Solo travellers (PeopleInTicket=1). This will retun an even more accurate result eliminating group discounts (if any). Of course in that case FarePerPerson=Fare

# In[ ]:


test_data.loc[test_data.Fare.isnull(), ['Fare','FarePerPerson']] = round(train_data[(train_data.Embarked=='S') & (train_data.Pclass==3) & (train_data.PeopleInTicket==1)]['Fare'].mean(),1)


# You may be interested to know that the fare changed from 7.8 to 8.1 as a result of us taking the mean of solo travellers. So indeed there was some discount for group travellers..Or maybe the fact was that children were charged less. Whatever be the reason, this gives a better imputation. Of course in the case of Titanic, this will play absolutely no role whatsoever in the final score..but these sort of small insights could make all the difference in a real competition where top 10 teams differ in scores by a mere 0.1%.
# 
# Also notice how we impute missing values from the train_data and not consider test_data to avoid information leakage from test to train. As far as possible we dont want to touch test_data for anything (Note: We will break this rule when building families in my next notebook)
# 
# Let us now tackle the 2 Embarked missing rows

# In[ ]:


display(combined[combined.Embarked.isnull()])


# In[ ]:


##Fare is 40 per person (80 for 2 people) for Pclass 1 for 2 adults. Where could they have Embarked from?

##Let us groupby Embarked and check some statistics
train_data[(train_data.Pclass==1)].groupby('Embarked').agg({'FarePerPerson': 'mean', 'Fare': 'mean', 'PassengerId': 'count'})


# In[ ]:


##Only 1 family got on at Q. Also fare is 30 per person and this is definitely not the case
##From the data below, it seems fairly obvious that the fareperperson of 40 for the 2 missing cases maps to Port C

##Let us check same data for groups of 2 adults
train_data[(train_data.Pclass==1) & (train_data.PeopleInTicket==2) & (train_data.Age>18)].groupby('Embarked').agg({'FarePerPerson': 'mean', 'Fare': 'mean', 'PassengerId': 'count'})


# There were 28 adult pairs from C with Pclass=1 with avg fareperperson=36 and 40 from S with avg fareperperon=30.5. From the above data also, we can guess that missing port is most likely to be "C"
# 
# The difference though narrows down considerably if we were to consider groups of 2 woman travellers. We just saw in my previous notebook that that sex had a small -ve impact on the fare. Another factor that can be considered is (non-missing)Cabin. The final diff is narrow and we can see from the dataset that there are folks in Port S who paid more and folks in port C who paid less..So there is a fair amount of noise here, but we will go ahead with the best fit and hope that works

# In[ ]:


print(train_data[(~train_data.Cabin.isnull()) & (train_data.Pclass==1) & (train_data.PeopleInTicket==2) & (train_data.Sex=="female") & (train_data.Age>18)].groupby('Embarked').agg({'FarePerPerson': 'mean', 'Fare': 'mean', 'PassengerId': 'count'}))

##Still port C comes out as a winner in all cases. We will go ahead with this
train_data.Embarked.fillna('C', inplace=True)


# Let us fill the remaining missing Ages with the mean values. This is deduced from the mean of similar passengers based on [Sex, Pclass, Title]. This is a 1 line code but there is one small complication. As discussed earlier, the mean Age for the Title 'Miss' fluctuates wildly based on whether she has Parch>1 or not (basically whether she is has a parent or not). We need to take care of this situation first. Let us add a new Title titled 'FemaleChild'. Before that let us take the mean ages once again as a reference.

# In[ ]:


print(train_data.groupby(['Pclass','Sex','Title'])['Age'].agg({'mean', 'median', 'count'}))

for df in [train_data, test_data, combined]:
    df.loc[(df.Title=='Miss') & (df.Parch!=0) & (df.PeopleInTicket>1), 'Title']="FemaleChild"

display(combined[(combined.Age.isnull()) & (combined.Title=='FemaleChild')])


# I added a condition that 'femalechild' should be non-solo traveller. Observe that we have identified 9 possible 'ADDITIONAL' minors with the 'femalechild' title. Without this, we would have imputed values of 30, 22 & 16 to the 'Miss' title across Pclass 1,2,3 respectively. Thus we would NOT have added any minor as part of the missing Age identification. Also observe by reprinting:
# print(train_data.groupby(['Pclass','Sex','Title'])['Age'].agg({'mean', 'median', 'count'}))
# how the Miss mean age changes.
# 
# This approach ideally should help increase the score of the model by a little bit (not much..maybe a decimal of a percentage) but in a serious competition this could make all the difference between a 10th position and 1st. In Pclass 3 'age group' is not that strong a factor for survival so this may not matter much..but if these missing rows were from Pclass 1 or Pclass 2, the score would have gone up significantly because being a child mattered a lot in those classes
# 
# Let us now fillin the missing ages based on Pclass, Sex and Title. Most people use the transform function

# In[ ]:


##[df['Age'].fillna(df.groupby(['Pclass','Sex','Title'])['Age'].transform('mean'), inplace=True) for df in [train_data, test_data]]


# It is commented because I dont reccomend this. Here we are leaking values from the test dataset. In case you are interested in how the command works - The 'for' loop runs on all dataframes in the list. The action it does is to fill all the NA's with 'something'. What is this 'something'. This is determined by the 'transform' function which computes the 'mean' for each of the group and returns the value needed to the fillNA function depending on the group that missing age is from.
# inplace=True is needed else all these changes will be saved on a view of a copy.
# 
# Try printing train_data.groupby(['Pclass','Sex','Title'])['Age'].transform('mean'). It returns a 'series' which has the same size as the original data. Each row contains the mean 'age' for that group. All the look-ups are internally done by the transform function. If you want to debug the function to understand a little better on what it does etc, you could experiment and print statements like:
# 
# def letusseewhatallhappensinsidetransform (x):
# * Try printing (type(x))
# * Try display(x)
# 
# train_data.groupby(['Pclass','Sex','Title'])['Age'].transform(letusseewhatallhappensinsidetransform)
# 
# My preferred way of imputing the missing ages is as below (3 lines)..but explained in detail because this covers a lot of important topics in Python/Pandas that will help you in future competitions

# In[ ]:


##Define a group containing all the parameters you want, do a mean
##You can print the below group. This will be our lookup table
grp = train_data.groupby(['Pclass','Sex','Title'])['Age'].mean()
print(grp)


# In[ ]:


##Though it looks like a nice lookup table this will be difficult to
##'lookup'. This is because this table is actually just a series object
##like a list of ages and the index is Pclass, Sex, Title.
print('\n', 'This so called lookup table is actually similar to a list: ', type(grp))
##So the below kind of lookup will fail miserably with an error
##Try: print(grp[(grp.Pclass==2) & (grp.Sex=='male') & (grp.Title=='Master')]['Age'])


# In[ ]:


##So let us convert this 'series' object into a 'dataframe' 
##We use the re-index feature. This is an important tool
grp = train_data.groupby(['Pclass','Sex','Title'])['Age'].mean().reset_index()[['Sex', 'Pclass', 'Title', 'Age']]

print('\n', 'We converted the series object to: ', type(grp))


# In[ ]:


##Now below statement works almost like a charm
print('\n', 'Lookup works like a charm now but not quite: ', grp[(grp.Pclass==2) & (grp.Sex=='male') & (grp.Title=='Master')]['Age'])


# In[ ]:


##There is still one minor change. The above lookup returns a series object
##You can print the type() and see for yourself.
##Even though the series object has only ONE row, however Python does not know
##all that and if you try assigning that series object to the 'age' col of a 
##'single' row, it will crib BIG-TIME. So we do one last thing..read the value
##of the first (and only row). This will be a single number
print('\n', 'Aah! Perfect: ', grp[(grp.Pclass==2) & (grp.Sex=='male') & (grp.Title=='Master')]['Age'].values[0])


# In[ ]:


##Now the above lookup works perfectly. Pass it the Pclass, Sex, Title
##It can then tell you the (mean) age for that group. Let us use it

##Define a function called fill_age. This will lookup the combination
##passed to it using above lookup table and return the value of the age associated
def fill_age(x):
    return grp[(grp.Pclass==x.Pclass)&(grp.Sex==x.Sex)&(grp.Title==x.Title)]['Age'].values[0]
##Here 'x' is the row containing the missing age. We look up the row's Pclass
##Sex and Title against the lookup table as shown previously and return the Age
##Now we have to call this fill_age function for every missing row for test, train

train_data['Age'], test_data['Age'] = [df.apply(lambda x: fill_age(x) if np.isnan(x['Age']) else x['Age'], axis=1) for df in [train_data, test_data]]
##This line is explained in the next cell

##End by combining the test and training data
combined=train_data.append(test_data)


# **train_data['Age'], test_data['Age'] = [df.apply(lambda x: fill_age(x) if np.isnan(x['Age']) else x['Age'], axis=1) for df in [train_data, test_data]]
# **
# 
# We already know one part of it..the outermost part - the 'for' loop as we have used it before. For each df in [list], do an 'action' and assign the o/p's (which in this case is a series object containing Ages for all rows in the df) to the LHS of the equation in specified order (in this case there are 2 o/p's and the first is assigned to train_data['Age'] and second to test_data['Age']
# 
# Now let us look at the 'action'. This is:
# 
# *[df.apply(lambda x: fill_age(x) if np.isnan(x['Age']) else x['Age']*****
# 
# We use the dataframe 'apply' feature. It applies a lamda function to each and every row. The row is assigned to a variable x above and passed to the lambda function. Here the lambda function is fill_age. This is only called if Age is null. The o/p is assigned back to Age column. Let us read this from right to left in regular English.
# 
# <*do something and return the o/p*> if [*condition*] else [*return something else*]
#     
# fill_age(x) if np.isnan(x['Age']) else x['Age']
# 
# This completely fills all the missing ages based on the lookup table we created earlier. The single liner packs a punch. We have used ternary operators, df.apply feature, list comprehensions and lambda functions. It may appear initially difficult to follow, but once you get the jist of how to interpret the list comprehensions, it is actually straightforward and extremely convinient to use.
# 
# Here we used the train_data averages to impute the missing values in test_data which is a good practice. I havent seen many good kernels do this. It is very easy and tempting to use the 'transform' feature in 1 line to fill in the missing values in both test and train_data. This is Wrong! Of course for the Titanic dataset this is more of an academic exercise but this is the practice which strictly needs to be followed for other competitions to avoid leakage from test to train.
# 
# We could also do a grouping based on all columns: train_data.groupby(['Pclass','Sex','Title', 'Embarked', 'Parch', 'SibSp', 'Survived'])['Age'].agg({'mean', 'median', 'count'}). Of course something like this could also introduce unnecessary noise and be an overkill. This is also the reason I avoided using an ML model to guess the missing ages. There are far too many clues in the dataset for an human mind to use and we will call upon the machines to only do the final serious number crunching at which it is exceptionally good at.
# 
# Next tutorial will answer interesting questions like
# - How many families on the Titanic
# - How many spouses?
# - How many siblings travelled on the Titanic
# - Who all are related to whom
# - Errors in the dataset
# 
# and other such interesting questions...
# 
# These have a SERIOUS bearing on the mortality and will help us push our scores well into the 80's. The top score in this competition is of Chris Deotte at around 84%. Chris is current Kaggle number 1 in discussion and Kaggle number 2 on Notebooks. We will make an attempt to go close to his score. 
# 
# Your upvotes will motivate me to document the code well and make it more interesting to read 
