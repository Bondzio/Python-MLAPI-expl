
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib import style


# In[ ]:


df_results = pd.DataFrame()


# In[ ]:


def card_deal():
    
    df_play = pd.DataFrame(columns=['PlayerNo','card1','card2','card3','card4','card5','sumofcards','dealcard1','dealcard2',
                                'dealcard3','dealcard4','dealcard5','sumofdeal','blkjck','winloss','plybustbeat',
                                'dlbustbeat','plwinamt','dlwinamt','ply2cardsum'],index=range(6))
        
    cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]
    deck = cards*4*6
    no = 2
    i=1
    for a in range(6):
        random.shuffle(deck)
        play = random.sample(deck,no)
        deck.remove(play[0])
        deck.remove(play[1])
        df_play.loc[a].card1 = play[0]
        df_play.loc[a].card2 = play[1]
        df_play.loc[a].PlayerNo = 'Player' + str(i)
        i +=1
        
    return(df_play,deck)


# In[ ]:


def initvalues(df_play):
    df_play.card3 = 0
    df_play.card4 = 0
    df_play.card5 = 0
    df_play.dealcard3 = 0
    df_play.dealcard4 = 0
    df_play.dealcard5 = 0
    df_play.plwinamt = 0
    df_play.dlwinamt = 0
    df_play.ply2cardsum = 0
       
    for a,b in df_play.iterrows():
        if (b['card1'] == 1) and (b['card2'] >= 7):
            df_play.at[a,'card1'] = 11
    for a,b in df_play.iterrows():
        if (b['card2'] == 1) and (b['card1'] >= 7):
            df_play.at[a,'card2'] = 11
    
    df_play.sumofcards = df_play.card1 + df_play.card2
    
    for a,b in df_play.iterrows():
        if (b['sumofcards'] == 21):
            df_play.at[a,'blkjck'] = 'Win'
        else:
            df_play.at[a,'blkjck'] = 'nowin'
 
    return(df_play)


# In[ ]:


def dealercard(df_play,deck):
    deal = random.sample(deck,2)
    deck.remove(deal[0])
    deck.remove(deal[1])
    df_play.dealcard1 = deal[0]
    df_play.dealcard2 = deal[1]
    
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2
    return(df_play,deck)


# In[ ]:


def playcard3(df_play,deck):
    for a,b in df_play.iterrows():
        if (b['sumofcards']) <= 11:
            c = random.sample(deck,1)
            df_play.at[a,'card3'] = c[0]
            deck.remove(c[0])
            
    df_play.sumofcards = df_play.card1 + df_play.card2 + df_play.card3

    for a,b in df_play.iterrows():
        if (b['sumofcards'] <=11) and (b['card1'] == 1):
            df_play.at[a,'card1'] = 11
        elif (b['sumofcards'] <=11) and (b['card2'] == 1):
            df_play.at[a,'card2'] = 11
        elif (b['sumofcards'] <=11) and (b['card3'] == 1):
            df_play.at[a,'card3'] = 11
            
    df_play.sumofcards = df_play.card1 + df_play.card2 + df_play.card3
    return(df_play,deck)


# In[ ]:


def playcard4_5(df_play,deck):
    for a,b in df_play.iterrows():
        if (b.dealcard1 == 2 or b.dealcard1 == 3) and (b.sumofcards < 13):
            c = random.sample(deck,1)
            df_play.at[a,'card4'] = c[0]
            deck.remove(c[0])
        elif (b.dealcard1 == 4 or b.dealcard1 == 5 or b.dealcard1 == 6) and (b.sumofcards < 12):
            c = random.sample(deck,1)
            df_play.at[a,'card4'] = c[0]
            deck.remove(c[0])
        elif (b.dealcard1 == 7 or b.dealcard1 == 8 or b.dealcard1 == 9 or b.dealcard1 == 10 or b.dealcard1 == 1) and (b.sumofcards < 17):
            c = random.sample(deck,1)
            df_play.at[a,'card4'] = c[0]
            deck.remove(c[0])
    df_play.sumofcards = df_play.card1 + df_play.card2 + df_play.card3 + df_play.card4  

    for a,b in df_play.iterrows():
        if (b.dealcard1 == 2 or b.dealcard1 == 3) and (b.sumofcards < 13):
            c = random.sample(deck,1)
            df_play.at[a,'card5'] = c[0]
            deck.remove(c[0])
        elif (b.dealcard1 == 4 or b.dealcard1 == 5 or b.dealcard1 == 6) and (b.sumofcards < 12):
            c = random.sample(deck,1)
            df_play.at[a,'card5'] = c[0]
            deck.remove(c[0])
        elif (b.dealcard1 == 7 or b.dealcard1 == 8 or b.dealcard1 == 9 or b.dealcard1 == 10 or b.dealcard1 == 1) and (b.sumofcards < 17):
            c = random.sample(deck,1)
            df_play.at[a,'card5'] = c[0]
            deck.remove(c[0])
    df_play.sumofcards = df_play.card1 + df_play.card2 + df_play.card3 + df_play.card4 + df_play.card5
    return(df_play,deck)


# In[ ]:


def dealercard3(df_play,deck):
    df_play.loc[((df_play.sumofdeal >=7) & (df_play.dealcard1 == 1)),'dealcard1'] = 11
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2
    df_play.loc[((df_play.sumofdeal >=7) & (df_play.dealcard2 == 1)),'dealcard2'] = 11
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2

    c = random.sample(deck,1)
    df_play.loc[(df_play.sumofdeal < 17),'dealcard3'] = c[0]
    deck.remove(c[0])
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2 + df_play.dealcard3

    df_play.loc[((df_play.sumofdeal <=11) & (df_play.dealcard1 == 1)),'dealcard1'] = 11
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2 + df_play.dealcard3
    df_play.loc[((df_play.sumofdeal <= 11) & (df_play.dealcard2 == 1)),'dealcard2'] = 11
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2 + df_play.dealcard3
    df_play.loc[((df_play.sumofdeal <= 11) & (df_play.dealcard3 == 1)),'dealcard3'] = 11
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2 + df_play.dealcard3
    return(df_play,deck)


# In[ ]:


def dealercard4_5(df_play,deck):
    c = random.sample(deck,1)
    df_play.loc[(df_play.sumofdeal < 17),'dealcard4'] = c[0]
    deck.remove(c[0])
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2 + df_play.dealcard3 + df_play.dealcard4

    c = random.sample(deck,1)
    df_play.loc[(df_play.sumofdeal < 17),'dealcard5'] = c[0]
    deck.remove(c[0])
    df_play.sumofdeal = df_play.dealcard1 + df_play.dealcard2 + df_play.dealcard3 + df_play.dealcard4 + df_play.dealcard5
    return(df_play,deck)


# In[ ]:


def cardplayupd(df_play):
    for a,b in df_play.iterrows():
        if b.sumofcards > 21:
            df_play.at[a,'winloss'] = 'Loss'
            df_play.at[a,'plybustbeat'] = 'Bust'
            df_play.at[a,'dlbustbeat'] = 'PlBust'
        elif b.sumofdeal > 21:
            df_play.at[a,'winloss'] = 'Win'
            df_play.at[a,'plybustbeat'] = 'DlBust'
            df_play.at[a,'dlbustbeat'] = 'Bust'
        elif b.sumofdeal > b.sumofcards:
            df_play.at[a,'winloss'] = 'Loss'
            df_play.at[a,'plybustbeat'] = 'Beat'
            df_play.at[a,'dlbustbeat'] = 'Dlwin'
        elif b.sumofdeal < b.sumofcards:
            df_play.at[a,'winloss'] = 'Win'
            df_play.at[a,'plybustbeat'] = 'Plwin'
            df_play.at[a,'dlbustbeat'] = 'Beat'
        elif b.sumofdeal == b.sumofcards:
            df_play.at[a,'winloss'] = 'Push'
            df_play.at[a,'plybustbeat'] = 'Push'
            df_play.at[a,'dlbustbeat'] = 'Push'
    return(df_play)


# In[ ]:


def amtwin(df_play):
    for a,b in df_play.iterrows():
        if (b.winloss == 'Win') & (b.blkjck == 'nowin'):
            df_play.at[a,'plwinamt'] = 20
            df_play.at[a,'dlwinamt'] = 0
        elif (b.winloss == 'Win') & (b.blkjck == 'Win'):
            df_play.at[a,'plwinamt'] = 25
            df_play.at[a,'dlwinamt'] = 0
        elif (b.winloss == 'Push') & (b.blkjck == 'Win'):
            df_play.at[a,'plwinamt'] = 10
            df_play.at[a,'dlwinamt'] = 0
        elif (b.winloss == 'Push'):
            df_play.at[a,'plwinamt'] = 10
            df_play.at[a,'dlwinamt'] = 0
        else:
            df_play.at[a,'plwinamt'] = 0
            df_play.at[a,'dlwinamt'] = 10
        
    df_play.ply2cardsum = df_play.card1 + df_play.card2
    return(df_play)


# In[ ]:


for z in range(100):
    df_play,deck = card_deal()
    df_play = initvalues(df_play)
    df_play,deck = dealercard(df_play,deck)
    df_play,deck = playcard3(df_play,deck)
    df_play,deck = playcard4_5(df_play,deck)
    df_play,deck = dealercard3(df_play,deck)
    df_play,deck = dealercard4_5(df_play,deck)
    df_play = cardplayupd(df_play)
    df_play = amtwin(df_play)
    df_results = df_results.append(df_play)


# In[ ]:


def totalresult(df_results):
    rounds = df_results[df_results['PlayerNo']=='Player1']['card1'].count()
    TotalnumberofHandsPlayed = 6*rounds
    TotalPlayerWinAmt = df_results['plwinamt'].sum()
    TotalDealerWinAmt = df_results['dlwinamt'].sum()
    TotalBet = 10*6*rounds
    PlayerWintoBet_Ratio = (TotalPlayerWinAmt/TotalBet).round(2)
    TotalNumberofWins = df_results[df_results['winloss']=='Win']['winloss'].count()
    TotalWinPercent = np.around((TotalNumberofWins/TotalnumberofHandsPlayed)*100,2)
    TotalNumberofPush = df_results[df_results['winloss']=='Push']['winloss'].count()
    TotalPushPercent = np.around((TotalNumberofPush/TotalnumberofHandsPlayed)*100,2)
    TotalNumberofLoss = df_results[df_results['winloss']=='Loss']['winloss'].count()
    TotalLossPercent = np.around((TotalNumberofLoss/TotalnumberofHandsPlayed)*100,2)
    TotalNumberofBlkJcks = df_results[df_results['blkjck']=='Win']['blkjck'].count()
    BlkjckHitPercent = np.around((TotalNumberofBlkJcks/TotalnumberofHandsPlayed)*100,2)
    a = df_results[df_results['winloss']=='Win'][['card1','card2']].mode()
    
    print(' ')
    print('******* Entire Game (All 10,000*6 Hands) Statistics *******')
    print(' ')
    print('Total number of Hands Played : '+str(TotalnumberofHandsPlayed))
    print(' ')
    print('Total $Amt Bet : '+str(TotalBet))
    print('Total $Amt Won by All Players : '+str(TotalPlayerWinAmt))
    print('Total $Amt Won by Dealer : '+str(TotalDealerWinAmt))
    print(' ')
    print('Player $Amt Won to $Amt Bet Ratio : '+str(PlayerWintoBet_Ratio))
    print(' ')
    print('Total Number of Wins : '+str(TotalNumberofWins))
    print('Total Win % : '+str(TotalWinPercent)+'%')
    print(' ')
    print('Total Number of Push : '+str(TotalNumberofPush))
    print('Total Push % : '+str(TotalPushPercent)+'%')
    print(' ')
    print('Total Number of Loss : '+str(TotalNumberofLoss))
    print('Total Loss % : '+str(TotalLossPercent)+'%')
    print(' ')
    print('Total Number of BlackJacks Won : '+str(TotalNumberofBlkJcks))
    print('BlackJack Hit Percent :'+str(BlkjckHitPercent)+'%')
    print(' ')
    print('Luckiest Hands : '+str(a.card1.to_string(index=False))+' & '+str(a.card2.to_string(index=False)))
    
    return()


# In[ ]:


def playerstats(df_results):
    
    winamt = df_results.groupby('PlayerNo', as_index = False).agg({'plwinamt':'sum','dlwinamt':'sum'}).rename(columns={'plwinamt':'TotalWinAmt','dlwinamt':'TotalDealWin'})
    winamt['PlayerwintoDealerWin'] = (winamt['TotalWinAmt']/winamt['TotalDealWin']).round(2)

    rounds = df_results[df_results['PlayerNo']=='Player1']['card1'].count()
    winamt['Moneybet'] = rounds *10
    winamt['WintoBet Ratio'] = (winamt['TotalWinAmt']/winamt['Moneybet']).round(2)

    wincount = df_results[df_results['winloss']=='Win'].groupby('PlayerNo',as_index=False).agg({'winloss':'count'}).rename(columns={'winloss':'PlayerNoofWins'})
    wincount['Win %'] = ((wincount['PlayerNoofWins']/rounds)*100).round(2)

    pushcount =df_results[df_results['winloss']=='Push'].groupby('PlayerNo',as_index=False).agg({'winloss':'count'}).rename(columns={'winloss':'NoofPush'})
    pushcount['Push %'] = ((pushcount['NoofPush']/rounds)*100).round(2)

    blkjk = df_results[df_results['blkjck']=='Win'].groupby('PlayerNo', as_index = False).agg({'blkjck':'count'})
    blkjk['HitRatio %'] = ((blkjk.blkjck/rounds)*100).round(2)

    plbuststat = df_results[df_results['plybustbeat']=='Bust'].groupby('PlayerNo',as_index=False).agg({'plybustbeat':'count'}).rename(columns={'plybustbeat':'BustCount'})
    plbuststat['Bust %'] = ((plbuststat.BustCount/rounds)*100).round(2)

    plbeatstat = df_results[df_results['plybustbeat']=='Beat'].groupby('PlayerNo',as_index=False).agg({'plybustbeat':'count'}).rename(columns={'plybustbeat':'BeatCount'})
    plbeatstat['Beat %'] = ((plbeatstat.BeatCount/rounds)*100).round(2)

    dlbuststat = df_results[df_results['dlbustbeat']=='Bust'].groupby('PlayerNo',as_index=False).agg({'dlbustbeat':'count'}).rename(columns={'dlbustbeat':'dlBustCount'})
    dlbuststat['DealBust %'] = ((dlbuststat.dlBustCount/rounds)*100).round(2)

    df1 = winamt.merge(wincount,on='PlayerNo',how='outer')
    df2 =df1.merge(pushcount,on='PlayerNo',how='outer')
    player_stat_win= df2.merge(blkjk,on='PlayerNo',how='outer')
    player_stat_win.fillna(0,inplace=True)

    df3 = plbuststat.merge(plbeatstat,on='PlayerNo',how='outer')
    player_stat_loss = df3.merge(dlbuststat,on='PlayerNo',how='outer')
    player_stat_loss.fillna(0,inplace=True)
    
    print('***** Each Players Winning Statistics *******')
    print(player_stat_win)
    print('***** Each Players Losing Statistics *******')
    print(player_stat_loss)
    
    return()


# In[ ]:


def carddetails(df_results):
    carddetail = df_results.groupby(['ply2cardsum'],as_index = False).agg({'card1':'count','plwinamt':'sum','dlwinamt':'sum'}).rename(columns={'ply2cardsum':'Sumof2cards','card1':'NoofTimesDealt','plwinamt':'TotalAmtPlayerWins','dlwinamt':'TotalAmtDealerWins'})
    carddetail['Player to Dealer Win Ratio'] = (carddetail['TotalAmtPlayerWins']/carddetail['TotalAmtDealerWins']).round(2)
    df = df_results[df_results['winloss']=='Win'].groupby('ply2cardsum',as_index = False).agg({'card1':'count'}).rename(columns={'ply2cardsum':'Sumof2cards','card1':'CardWins'})
    carddetail = carddetail.merge(df,on='Sumof2cards',how='outer')
    carddetail.fillna(0,inplace=True)
    newcardet = carddetail[['Sumof2cards','NoofTimesDealt','CardWins']].copy()
    print('****** Details of Cards and their Win ******')
    print(newcardet)


# In[ ]:


def playerallcards(df_results):
    newcardwinmatrix = df_results.groupby(['sumofcards','dealcard1'],as_index = False).agg({'card1':'count'}).rename(columns={'card1':'NoOfCardsDealt','sumofcards':'PlayersSumofCards','dealcard1':'DealersfaceupCard'})
    newdf5 = df_results[df_results['winloss']=='Win'].groupby(['sumofcards','dealcard1'],as_index = False).agg({'card1':'count'}).rename(columns={'sumofcards':'PlayersSumofCards','card1':'NoOfCardWins','dealcard1':'DealersfaceupCard'})
    newcardwinmatrix = newcardwinmatrix[newcardwinmatrix['PlayersSumofCards']<22]
    newdf5 = newdf5[newdf5['PlayersSumofCards']<22]
    newcardwinmatrix= newcardwinmatrix.merge(newdf5,on=['PlayersSumofCards','DealersfaceupCard'],how='outer')
    newcardwinmatrix.fillna(0,inplace=True)
    newcardwinmatrix['Win%'] = (newcardwinmatrix['NoOfCardWins']/newcardwinmatrix['NoOfCardsDealt']*100).round(2)
    newfin_matrix = newcardwinmatrix.pivot(index='PlayersSumofCards', columns='DealersfaceupCard', values='Win%')
    newfin_matrix.fillna(0,inplace=True)
    print(' ***** Below is the % Win Matrix based on the sum of all the cards a Player is dealt *****')
    print(newfin_matrix)


# In[ ]:


def player2card(df_results):
    cardwinmatrix = df_results.groupby(['ply2cardsum','dealcard1'],as_index = False).agg({'card1':'count'}).rename(columns={'card1':'NoOfCardsDealt','ply2cardsum':'PlayersSumof2cards','dealcard1':'DealersfaceupCard'})
    df5 = df_results[df_results['winloss']=='Win'].groupby(['ply2cardsum','dealcard1'],as_index = False).agg({'card1':'count'}).rename(columns={'ply2cardsum':'PlayersSumof2cards','card1':'NoOfCardWins','dealcard1':'DealersfaceupCard'})
    cardwinmatrix= cardwinmatrix.merge(df5,on=['PlayersSumof2cards','DealersfaceupCard'],how='outer')
    cardwinmatrix.fillna(0,inplace=True)
    cardwinmatrix['Win%'] = (cardwinmatrix['NoOfCardWins']/cardwinmatrix['NoOfCardsDealt']*100).round(2)
    fin_matrix = cardwinmatrix.pivot(index='PlayersSumof2cards', columns='DealersfaceupCard', values='Win%')
    fin_matrix.fillna(0,inplace=True)
    
    print(' ***** Below is the % Win Matrix based on the first two cards a Player is dealt *****')
    print(fin_matrix)


# In[ ]:


totalresult(df_results)


# In[ ]:


playerstats(df_results)


# In[ ]:


carddetails(df_results)


# In[ ]:


playerallcards(df_results)


# In[ ]:


player2card(df_results)


# In[ ]:


newcardwinmatrix = df_results.groupby(['sumofcards'],as_index = False).agg({'card1':'count'}).rename(columns={'card1':'Hands Lost/Push','sumofcards':'PlayersSumofCards'})
newdf5 = df_results[df_results['winloss']=='Win'].groupby(['sumofcards'],as_index = False).agg({'card1':'count'}).rename(columns={'sumofcards':'PlayersSumofCards','card1':'Hands Won'})
newcardwinmatrix = newcardwinmatrix[newcardwinmatrix['PlayersSumofCards']<22]
newcardwinmatrix = newcardwinmatrix[newcardwinmatrix['PlayersSumofCards']>10]
newcardwinmatrix['Ratio'] = (newcardwinmatrix['Hands Won']/newcardwinmatrix['Hands Lost/Push'])*100


# In[ ]:


get_ipython().magic('matplotlib inline')
style.use('ggplot')
fig, ax = plt.subplots(figsize=(7,4))
hist1 = newcardwinmatrix.plot.bar(x='PlayersSumofCards',y='Hands Lost/Push',ax=ax,alpha =0.3,color='teal')#,legend ='Hands Lost')
hist2 = newdf5.plot.bar(x='PlayersSumofCards',y='Hands Won',ax=ax,alpha =1,color='teal')#,legend =None)
ax.grid(False)
plt.title('Number of Wins by Players Sum of Cards',fontsize=13,fontweight='bold')
plt.xlabel('Players Sum of Cards', fontsize=12)
plt.ylabel('Number of Hands Dealt', fontsize=12)
plt.xticks(rotation='horizontal')
plt.tight_layout()
#labels = 'No of Wins'
#handles,labels = ax.get_legend_handles_labels()
plt.show()

