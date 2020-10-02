#!/usr/bin/env python
# coding: utf-8

# In[376]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[377]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

train=pd.read_csv('../input/train.csv')
test=pd.read_csv('../input/test.csv')
PassengerId=test['PassengerId']
all_data = pd.concat([train, test], ignore_index = True)

train.head()


# In[378]:


train.info()


# In[379]:


train['Survived'].value_counts()


# In[380]:


sns.barplot(x="Sex", y="Survived", data=train)


# In[381]:


sns.barplot(x="Pclass", y="Survived", data=train)


# In[382]:


sns.barplot(x="SibSp", y="Survived", data=train)


# In[383]:


sns.barplot(x="Parch", y="Survived", data=train)


# In[384]:


facet = sns.FacetGrid(train, hue="Survived",aspect=2)
facet.map(sns.kdeplot,'Age',shade= True)
facet.set(xlim=(0, train['Age'].max()))
facet.add_legend()
plt.xlabel('Age') 
plt.ylabel('density')


# In[385]:


train['Fare'].corr(train['Embarked'].dropna().map(lambda s: 0 if s == 'S' else 1))


# In[386]:


all_data['Title'] = all_data['Name'].apply(lambda x:x.split(',')[1].split('.')[0].strip())
Title_Dict = {}
Title_Dict.update(dict.fromkeys(['Capt', 'Col', 'Major', 'Dr', 'Rev'], 'Officer'))
Title_Dict.update(dict.fromkeys(['Don', 'Sir', 'the Countess', 'Dona', 'Lady'], 'Royalty'))
Title_Dict.update(dict.fromkeys(['Mme', 'Ms', 'Mrs'], 'Mrs'))
Title_Dict.update(dict.fromkeys(['Mlle', 'Miss'], 'Miss'))
Title_Dict.update(dict.fromkeys(['Mr'], 'Mr'))
Title_Dict.update(dict.fromkeys(['Master','Jonkheer'], 'Master'))

all_data['Title'] = all_data['Title'].map(Title_Dict)
sns.barplot(x="Title", y="Survived", data=all_data)


# In[387]:


all_data['FamilySize']=all_data['SibSp']+all_data['Parch']+1
sns.barplot(x="FamilySize", y="Survived", data=all_data)

all_data['FamilySize'].corr(all_data['Survived'])


# In[388]:


def Fam_label(s):
    if (s >= 2) & (s <= 4):
        return 2
    elif ((s > 4) & (s <= 7)) | (s == 1):
        return 1
    elif (s > 7):
        return 0
all_data['FamilyLabel']=all_data['FamilySize'].apply(Fam_label)
sns.barplot(x="FamilyLabel", y="Survived", data=all_data)

all_data['FamilyLabel'].corr(all_data['Survived'])


# In[389]:


all_data.info()


# In[390]:


all_data['Cabin'] = all_data['Cabin'].fillna('Unknown')
all_data['Deck']=all_data['Cabin'].str.get(0)
sns.barplot(x="Deck", y="Survived", data=all_data)


# In[391]:


Ticket_Count = dict(all_data['Ticket'].value_counts())
all_data['TicketGroup'] = all_data['Ticket'].apply(lambda x:Ticket_Count[x])
sns.barplot(x='TicketGroup', y='Survived', data=all_data)


# In[392]:


def Ticket_Label(s):
    if (s >= 2) & (s <= 4):
        return 2
    elif ((s > 4) & (s <= 8)) | (s == 1):
        return 1
    elif (s > 8):
        return 0

all_data['TicketGroup'] = all_data['TicketGroup'].apply(Ticket_Label)
sns.barplot(x='TicketGroup', y='Survived', data=all_data)

all_data['TicketGroup'].corr(all_data['Survived'])


# In[393]:


all_data.info()


# In[394]:


from sklearn.ensemble import RandomForestRegressor
age_df = all_data[['Age', 'Pclass','Sex','Title']]
age_df=pd.get_dummies(age_df)
known_age = age_df[age_df.Age.notnull()].as_matrix()
unknown_age = age_df[age_df.Age.isnull()].as_matrix()
y = known_age[:, 0]
X = known_age[:, 1:]
rfr = RandomForestRegressor(random_state=0, n_estimators=100, n_jobs=-1)
rfr.fit(X, y)
predictedAges = rfr.predict(unknown_age[:, 1::])
all_data.loc[ (all_data.Age.isnull()), 'Age' ] = predictedAges


# In[395]:


all_data[all_data['Embarked'].isnull()]


# In[396]:


all_data.groupby(by=["Pclass","Embarked"]).Fare.median()


# In[397]:


all_data['Embarked'] = all_data['Embarked'].fillna('C')


# In[398]:


all_data[all_data['Fare'].isnull()]


# In[399]:


fare=all_data[(all_data['Embarked'] == "S") & (all_data['Pclass'] == 3)].Fare.median()
all_data['Fare']=all_data['Fare'].fillna(fare)


# In[400]:


all_data['Surname']=all_data['Name'].apply(lambda x:x.split(',')[0].strip())
Surname_Count = dict(all_data['Surname'].value_counts())
all_data['FamilyGroup'] = all_data['Surname'].apply(lambda x:Surname_Count[x])
Female_Child_Group=all_data.loc[(all_data['FamilyGroup']>=2) & ((all_data['Age']<=12) | (all_data['Sex']=='female'))]
Male_Adult_Group=all_data.loc[(all_data['FamilyGroup']>=2) & (all_data['Age']>12) & (all_data['Sex']=='male')]


# In[401]:


Female_Child=pd.DataFrame(Female_Child_Group.groupby('Surname')['Survived'].mean().value_counts())
Female_Child.columns=['GroupCount']
Female_Child


# In[402]:


sns.barplot(x=Female_Child.index, y=Female_Child["GroupCount"]).set_xlabel('AverageSurvived')


# In[403]:


Male_Adult=pd.DataFrame(Male_Adult_Group.groupby('Surname')['Survived'].mean().value_counts())
Male_Adult.columns=['GroupCount']
Male_Adult


# In[404]:


Female_Child_Group=Female_Child_Group.groupby('Surname')['Survived'].mean()
Dead_List=set(Female_Child_Group[Female_Child_Group.apply(lambda x:x==0)].index)
print(Dead_List)
Male_Adult_List=Male_Adult_Group.groupby('Surname')['Survived'].mean()
Survived_List=set(Male_Adult_List[Male_Adult_List.apply(lambda x:x==1)].index)
print(Survived_List)


# In[405]:


train=all_data.loc[all_data['Survived'].notnull()]
test=all_data.loc[all_data['Survived'].isnull()]
test.loc[(test['Surname'].apply(lambda x:x in Dead_List)),'Sex'] = 'male'
test.loc[(test['Surname'].apply(lambda x:x in Dead_List)),'Age'] = 60
test.loc[(test['Surname'].apply(lambda x:x in Dead_List)),'Title'] = 'Mr'
test.loc[(test['Surname'].apply(lambda x:x in Survived_List)),'Sex'] = 'female'
test.loc[(test['Surname'].apply(lambda x:x in Survived_List)),'Age'] = 5
test.loc[(test['Surname'].apply(lambda x:x in Survived_List)),'Title'] = 'Miss'


# In[406]:


all_data=pd.concat([train, test])
all_data=all_data[['Survived','Pclass','Sex','Age','Fare','Embarked','Title','FamilyLabel','Deck']]
all_data=pd.get_dummies(all_data, drop_first=True)
train=all_data[all_data['Survived'].notnull()]
test=all_data[all_data['Survived'].isnull()].drop('Survived',axis=1)


# In[ ]:


from keras.utils import to_categorical

X = train.as_matrix()[:, 1:]
y = train.as_matrix()[:,0].reshape((X.shape[0],1))


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, BatchNormalization

model = Sequential()
model.add(Dense(output_dim=X.shape[1], input_dim=X.shape[1]))
model.add(BatchNormalization())
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(output_dim=128))
model.add(Activation("relu"))
model.add(Dense(output_dim=64))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(output_dim=32))
model.add(Dense(input_dim=32, output_dim=1))
model.add(Activation("sigmoid"))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# In[ ]:


model.fit(X, y, epochs=500, batch_size=32)


# In[ ]:


pred = np.round(model.predict(test)).astype(int)


# In[ ]:


raw_test = pd.read_csv('../input/test.csv')
pred_with_id = pd.concat(
    [
        raw_test['PassengerId'],
        pd.DataFrame(pred, columns=['Survived']),
    ], 
    axis=1,
)


# In[ ]:


pred_with_id.to_csv('submit.csv', index=False)

