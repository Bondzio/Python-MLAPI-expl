#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# **Finding out winning parties of previous elections**
# 
# Lets start with figuring out the winning parties of 2002, 2008, and 2013 elections for every constitutency.

# In[ ]:


## 2002 Elections ## 
NA2002 = pd.read_csv("../input/National Assembly 2002 - Updated.csv", encoding = "ISO-8859-1")
Winner02 = pd.DataFrame([])

for i in range(272):
    Const = "NA-%d"%(i+1)
    NA02 = NA2002.loc[NA2002['Constituency_title']==Const, ['Party','Votes','Total_Votes', 'Seat']]
    if NA02.empty == True:
        print("2002 Missing:",Const) # missing constituency
    if NA02.empty == False:
        MAX = (NA02.loc[NA02['Votes'].idxmax()]) # party recieiving maximum votes is the winner
        temp = pd.DataFrame([Const,MAX['Party'],MAX['Votes'],MAX['Total_Votes'], MAX['Seat']]).T
        Winner02 = pd.concat([Winner02,temp])
Winner02 = Winner02.rename(columns = {0:'Constituency', 1:'Party', 2:'Votes', 3:'TotalVotes', 4:'Seat'}) # Winners of 2002 Elections


## 2008 Elections ##
NA2008 = pd.read_csv("../input/National Assembly 2008.csv", encoding = "ISO-8859-1")
Winner08 = pd.DataFrame([])

for i in range(272):
    Const = "NA-%d"%(i+1)
    NA08 = NA2008.loc[NA2008['ConstituencyTitle']==Const, ['Party','Votes','TotalVotes', 'Seat']]
    if NA08.empty == True:
        print("2008 Missing:",Const) # missing constituency
    if NA08.empty == False:
        MAX = (NA08.loc[NA08['Votes'].idxmax()])
        temp = pd.DataFrame([Const,MAX['Party'],MAX['Votes'],MAX['TotalVotes'], MAX['Seat']]).T
        Winner08 = pd.concat([Winner08,temp])
Winner08 = Winner08.rename(columns = {0:'Constituency', 1:'Party', 2:'Votes', 3:'TotalVotes', 4:'Seat'}) # Winners of 2008 Elections


## 2013 Elections ##
NA2013 = pd.read_csv("../input/National Assembly 2013 - Updated.csv", encoding = "ISO-8859-1")
Winner13 = pd.DataFrame([])

for i in range(272):
    Const = "NA-%d"%(i+1)
    NA13 = NA2013.loc[NA2013['ConstituencyTitle']==Const, ['Party','Votes','TotalVotes', 'Seat']]
    Votes = NA13['Votes'].astype('int64')
    NA13['Votes'] = Votes
    if NA13.empty == True:
        print("2013 Missing:",Const) # missing constituency
    if NA13.empty == False:
        MAX = (NA13.loc[NA13['Votes'].idxmax()])
        temp = pd.DataFrame([Const,MAX['Party'],MAX['Votes'],MAX['TotalVotes'], MAX['Seat']]).T
        Winner13 = pd.concat([Winner13,temp])
Winner13 = Winner13.rename(columns = {0:'Constituency', 1:'Party', 2:'Votes', 3:'TotalVotes', 4:'Seat'}) # Winners of 2013 Elections


# In[ ]:


Winner13


# In[ ]:


Total_Seats = 272
Winners = pd.DataFrame([])
Con = pd.DataFrame([])

for i in range(Total_Seats):
    Const = "NA-%d"%(i+1)
    if Const != "NA-8" and Const != "NA-119" and Const != "NA-207" and Const != "NA-235" and Const != "NA-266" and Const != "NA-83" and Const != "NA-254":
        tempCon = (Winner13.loc[Winner13['Constituency']==Const,['Constituency']])
        tempCon = tempCon.values.ravel()
        tempSeat = (Winner13.loc[Winner13['Constituency']==Const,['Seat']])
        tempSeat = tempSeat.values.ravel()
        temp13 = (Winner13.loc[Winner13['Constituency']==Const,['Party']])
        temp13 = temp13.values.ravel()
        temp08 = (Winner08.loc[Winner08['Constituency']==Const,['Party']])
        temp08 = temp08.values.ravel()
        temp02 = (Winner02.loc[Winner02['Constituency']==Const,['Party']])
        temp02 = temp02.values.ravel()
        temp = pd.DataFrame([tempCon, tempSeat, temp02,temp08,temp13])
        temp = temp.rename(columns = {0:'Winner'})
        Winners = pd.concat([Winners,temp], axis = 1)
        Con = pd.concat([Con,pd.DataFrame([Const])])


# In[ ]:


Final = Winners.T
Final = Final.rename(columns = {0: 'Constituency', 1: 'Seat', 2:'2002', 3:'2008', 4:'2013'})
Final['2002'] = Final['2002'].replace(['Indepndent'], 'Independent')
#Final['2002'] = Final['2002'].replace(['Muttahidda Majlis-e-Amal Pakistan'], 'MUTTAHIDA MAJLIS-E-AMAL PAKISTAN')
Final['2002'] = Final['2002'].replace(['Muttahidda Majlis-e-Amal'], 'Muttahidda Majlis-e-Amal Pakistan')
Final['2002'] = Final['2002'].replace(['Pakistan Mulim League(QA)'], 'Pakistan Muslim League(QA)')
Final['2002'] = Final['2002'].replace(['Pakistan Peoples Party Parliamentarian'], 'Pakistan Peoples Party Parliamentarians')
Final['2002'] = Final['2002'].replace(['Pakistan Peoples Party Parlimentarians'], 'Pakistan Peoples Party Parliamentarians')
Final['2002'] = Final['2002'].replace(['Pakistan peoples Party Parlimentarians'], 'Pakistan Peoples Party Parliamentarians')
Final['2002'] = Final['2002'].replace(['Muttahida Qaumi Moment'], 'Muttahida Qaumi Movement Pakistan')
Final['2008'] = Final['2008'].replace(['MUTTHIDA\xa0MAJLIS-E-AMAL\xa0PAKISTAN'], 'Muttahidda Majlis-e-Amal Pakistan')
Final['2008'] = Final['2008'].replace(['Pakistan Muslim League'], 'Pakistan Muslim League(QA)')
Final['2013'] = Final['2013'].replace(['Pakistan Muslim League'], 'Pakistan Muslim League(QA)')
#np.unique(Final['2013'])


# **List of Winners**
# 
# So, finally we can observe the winners from every constituency in the following table.

# In[ ]:


Final


# **Finding Safe Seats**
# 
# First lets try to find the constituencies for which the same party won the elections in 2002, 2008 and 2013.
# It can be observed that out of 265 constitutencies analyzed *(accounting  for the 8 constituencies for which the results were not available in the dataset)*, 42 can be categorized as safe seats i.e. the seats that have been won by same party in previous 3 elections. By analyzing bit more we can see that only *Independent Candidates*, *Muttahida Qaumi Movement Pakistan(MQM-P)* and *Pakistan Peoples Party Parliamentarians (PPPP)* are the parties to achieve the consecutive 3 times winning streak. Of these 23 seats belong to *PPPP*, 11 belong to *MQM-P*  and remaining 8 seats were won be *Independent Candidates*. Out of these 8 *Independent Candidates* 7 belong to **Tribal Areas**, only 1 seat is outside of Tribal Areas and that belongs to **Jhang District** (*NA-90*). All other seats that have remained consistent in previous 3 elections came from **Sindh** province. For *MQM-P* all seats have come from **Karachi** except for the one in **Hyderabad**(*NA-219*), for *PPPP* all seats come from rest of the Sindh province, except for *NA-248 Karachi* which *PPPP* has won consecutively 3 times.   

# In[ ]:


Total_Seats = 272
Safe = pd.DataFrame([])
for i in range(Total_Seats):
    Const = "NA-%d"%(i+1)
    if Const != "NA-8" and Const != "NA-119" and Const != "NA-207" and Const != "NA-235" and Const != "NA-266" and Const != "NA-83" and Const != "NA-254":
        tempCon = (Final.loc[Final['Constituency']==Const,['Constituency']])
        tempCon = tempCon.values[0][0]
        tempSeat = (Final.loc[Final['Constituency']==Const,['Seat']])
        tempSeat = tempSeat.values[0][0]
        Party = (Final.loc[Final['Constituency']==Const,['2002']])
        Party = Party.values[0][0]
        Num = len(np.unique(Final.loc[Final['Constituency'] == Const]))-2
        temp = pd.DataFrame([tempCon, tempSeat, Party, Num]).T
        Safe = pd.concat([Safe,temp])

#Safe
Safe_Const = Safe[Safe[3]==1]
PPPP_Safe = (Safe_Const[2]=='Pakistan Peoples Party Parliamentarians').sum()
MQMP_Safe = (Safe_Const[2]=='Muttahida Qaumi Movement Pakistan').sum()
Ind_Safe =  (Safe_Const[2]=='Independent').sum()

x = np.arange(len(np.unique(Safe_Const[2])))
value = [PPPP_Safe, MQMP_Safe, Ind_Safe]

pp, mq, nd = plt.bar(x,value)
pp.set_facecolor('r')
mq.set_facecolor('g')
nd.set_facecolor('b')
plt.xticks(x,('PPPP', 'MQM-P', 'Ind'))
plt.show()

Safe_Const

