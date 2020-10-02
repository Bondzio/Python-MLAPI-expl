#!/usr/bin/env python
# coding: utf-8

# # M5 beginner EDA + CNN
# This notebook include some analyzing of the given data sets. And try to see things from different aspects and scales.<br/>
# In the end of this notebook, I use CNN to predict the trend of sales base on time.<br/>
# <br/>
# This is a forecasting competition, where we have to predict sales of 28 days in the future. So, first we will look at what data have been given. And do some simple EDA, try to find of what affects the sales.<br/>
# <br/>
# By the way, I'm not a english native speaker, so if there are sentences that you don't understand please tell me, thanks.
# 
# Please vote up if find this notebook helpful or interesting. Cheers.

# # Data

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from numpy import array
from numpy import hstack

import seaborn as sns
import matplotlib.pyplot as plt

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


train_sales = pd.read_csv('/kaggle/input/m5-forecasting-accuracy/sales_train_validation.csv')
sell_prices = pd.read_csv('/kaggle/input/m5-forecasting-accuracy/sell_prices.csv')
calendar = pd.read_csv('/kaggle/input/m5-forecasting-accuracy/calendar.csv')
submission_file = pd.read_csv('/kaggle/input/m5-forecasting-accuracy/sample_submission.csv')


# ## train_sales
# * id: validation id
# * item_id: item id
# * cat_id: category (ex. hobbies, household, foods)
# * store_id: from which store
# * state_id: in which state(ex. CA, TX, WI)

# In[ ]:


train_sales.head(3)


# ## sell_price
# * sell_price: price for the item in the week

# In[ ]:


sell_prices.head(3)


# ## calender
# * event_name: special day(ex. SuperBowl)
# * snap: The Supplemental Nutrition Assistance Program

# In[ ]:


calendar.head(10)


# ## submission

# In[ ]:


submission_file.head(3)


# # EDA
# ## At the scale state 

# * observe sales at the scale of ***state***
#     * California generally has better salls than the other two states.
#     * Apart from **foods** Texas is better than Wisconsin
#     * The total sales of the category is: Foods > household > hobbies

# In[ ]:


train_sales['total_sales'] = train_sales.sum(axis=1)
sns.catplot(x="cat_id", y="total_sales",
                hue="state_id",
                data=train_sales, kind="bar",
                height=8, aspect=1);


# Below is the population of California, Texas, and Wisconsin. As you can see the order of population is the same as sales. (CA > TX > WI)<br/>
# Eventhough the orders are the same, the difference gaps of sales between each state are not the same. For example, the population of Wisconsin is only 12.5% of California and 17% of Texas. But the sales of Wisconsin is only a bit less than the other states. <br/>
# So, maybe obersveing at the scale of state is not good enough.<br/>
# Next, we will look at the problem at a smaller scale<br/>

# ![](https://i.imgur.com/bUSEoMb.png)

# ## At the scale of stores
# Eventhough, California has the best sales, only CA_3 store has an out standing sales. The rest of California stores are just the same as other states, or even has the least sales(CA_4). <br/>
# It is quite interesting to see that, even in lease populated states, Walmart still manage to reach certain sales. Perhaps the location and the number of stores in the area are the real factors.
# 

# In[ ]:


sns.catplot(x="store_id", y="total_sales",
                hue="cat_id",
                data=train_sales, kind="bar",
                height=8, aspect=1);


# ## Perspective of Time

# In[ ]:


hobbies_state = train_sales.loc[(train_sales['cat_id'] == 'HOBBIES')].groupby(['state_id']).mean().T
hobbies_state = hobbies_state.rename({'CA': 'HOBBIES_CA', 'TX': 'HOBBIES_TX', 'WI': 'HOBBIES_WI'}, axis=1)
household_state = train_sales.loc[(train_sales['cat_id'] == 'HOUSEHOLD')].groupby(['state_id']).mean().T
household_state = household_state.rename({'CA': 'HOUSEHOLD_CA', 'TX': 'HOUSEHOLD_TX', 'WI': 'HOUSEHOLD_WI'}, axis=1)
foods_state = train_sales.loc[(train_sales['cat_id'] == 'FOODS')].groupby(['state_id']).mean().T
foods_state = foods_state.rename({'CA': 'FOODS_CA', 'TX': 'FOODS_TX', 'WI': 'FOODS_WI'}, axis=1)
nine_example = pd.concat([hobbies_state, household_state, foods_state], axis=1)
nine_example = nine_example.drop('total_sales')


# In[ ]:


from itertools import cycle
color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

fig, axs = plt.subplots(3,3, figsize=(10,10))
axs = axs.flatten()
ax_idx = 0
for item in nine_example.columns:
    nine_example[item].plot(title=item, color=next(color_cycle), ax=axs[ax_idx])
    ax_idx += 1
plt.tight_layout()
plt.show()


# The time length of the upper graph is 5 years long, from 2011 to 2016. It is interesting to that there are yearly patterns  in the sales. For example, you can see around every 360 days there is a day when the sale is 0.<br/>
# As you can see in the following parts, these results are costed by annual events. Like the 0 sales days I just mentioned are cost by Christmas. In the given data sets there are a lot of annual events, some have effects on the sales , and some do not.

# In[ ]:


nine_example.loc[nine_example['HOBBIES_CA'] == 0]


# In[ ]:


calendar.loc[calendar['d'].isin(['d_331', 'd_697', 'd_1062', 'd_1427', 'd_1792'])]


# ## Other special events 
# Since special events like Christmas affects the sales in every state, perhaps there are other events that also make the sales go lower or higher nationally. In file "calendar", there are 30 differert events. Including Superbowl, Valentines day, Presidents day, etc.<br/>
# Below, shows the stores mean sales in **HOBBIES** of each states, and points out the spacial events. It is pretty obvious that tehre are some events always appear in the same place compare to the sales trend. For instance, there are always two points beside the Christmas points(those equal to 0). Latter there is a clearer graph to show this.

# In[ ]:


event_date = calendar.loc[calendar['event_name_1'].isin(calendar.event_name_1.unique()[1:])].d
HOBBIES_event = train_sales.loc[(train_sales['cat_id'] == 'HOBBIES')].groupby(['state_id']).mean().T.reset_index()
HOBBIES_event = HOBBIES_event.loc[HOBBIES_event['index'].isin(event_date)]
plt.figure(figsize=(15, 10))
plt.subplot(3,1,1)
nine_example['HOBBIES_CA'].plot(title='HOBBIES_CA', color=next(color_cycle))
plt.scatter(HOBBIES_event.reset_index().level_0, HOBBIES_event['CA'],color=next(color_cycle), zorder=10)
plt.subplot(3,1,2)
nine_example['HOBBIES_TX'].plot(title='HOBBIES_TX', color=next(color_cycle))
plt.scatter(HOBBIES_event.reset_index().level_0, HOBBIES_event['TX'],color=next(color_cycle), zorder=10)
plt.subplot(3,1,3)
nine_example['HOBBIES_WI'].plot(title='HOBBIES_WI', color=next(color_cycle))
plt.scatter(HOBBIES_event.reset_index().level_0, HOBBIES_event['WI'],color=next(color_cycle), zorder=10)
plt.tight_layout()
plt.show()


# Here is the clearer graph, ss you can see "Thanksgiving", "Christmas", and "NewYear" always appear in the bottom of the trend in every year and every state. While there are events with patterns, there are also many hug events without patterns. In the graph, point "SuperBowl" appears on different sides of the trend. Sometimes it's at the top, but sometimes it's at the bottom. So, in prediction events like SuperBowl should not be taken into account.

# 
# ![](https://i.imgur.com/OlTQtrf.png)

# ## Inspect the data at different time scale

# In[ ]:


cal = calendar[['d', 'wday', 'month', 'year']]
cal = cal.rename(columns={'d': 'index'})
hobbies_state = train_sales.loc[(train_sales['cat_id'] == 'HOBBIES')].groupby(['state_id']).sum().T
hobbies_state = hobbies_state.reset_index()
hobbies_state = pd.merge(hobbies_state,cal, on='index')
household_state = train_sales.loc[(train_sales['cat_id'] == 'HOUSEHOLD')].groupby(['state_id']).sum().T
household_state = household_state.reset_index()
household_state = pd.merge(household_state,cal, on='index')
foods_state = train_sales.loc[(train_sales['cat_id'] == 'FOODS')].groupby(['state_id']).sum().T
foods_state = foods_state.reset_index()
foods_state = pd.merge(foods_state,cal, on='index')


# In[ ]:


plt.figure(figsize=(18, 18))
plt.subplot(3,3,1)
plt.title('hobbies')
plt.plot(range(1, 7 + 1 ,1), hobbies_state.groupby(['wday']).mean().CA, label='CA')
plt.plot(range(1, 7 + 1 ,1), hobbies_state.groupby(['wday']).mean().TX, label='TX')
plt.plot(range(1, 7 + 1 ,1), hobbies_state.groupby(['wday']).mean().WI, label='WI')
plt.legend(loc='upper right')
plt.subplot(3,3,2)
plt.title('household')
plt.plot(range(1, 7 + 1 ,1), household_state.groupby(['wday']).mean().CA, label='CA')
plt.plot(range(1, 7 + 1 ,1), household_state.groupby(['wday']).mean().TX, label='TX')
plt.plot(range(1, 7 + 1 ,1), household_state.groupby(['wday']).mean().WI, label='WI')
plt.legend(loc='upper right')
plt.subplot(3,3,3)
plt.title('foods')
plt.plot(range(1, 7 + 1 ,1), foods_state.groupby(['wday']).mean().CA, label='CA')
plt.plot(range(1, 7 + 1 ,1), foods_state.groupby(['wday']).mean().TX, label='TX')
plt.plot(range(1, 7 + 1 ,1), foods_state.groupby(['wday']).mean().WI, label='WI')
plt.legend(loc='upper right')
plt.subplot(3,3,4)
plt.title('hobbies')
plt.plot(range(1, 12 + 1 ,1), hobbies_state.groupby(['month']).mean().CA, label='CA')
plt.plot(range(1, 12 + 1 ,1), hobbies_state.groupby(['month']).mean().TX, label='TX')
plt.plot(range(1, 12 + 1 ,1), hobbies_state.groupby(['month']).mean().WI, label='WI')
plt.legend(loc='upper right')
plt.subplot(3,3,5)
plt.title('household')
plt.plot(range(1, 12 + 1 ,1), household_state.groupby(['month']).mean().CA, label='CA')
plt.plot(range(1, 12 + 1 ,1), household_state.groupby(['month']).mean().TX, label='TX')
plt.plot(range(1, 12 + 1 ,1), household_state.groupby(['month']).mean().WI, label='WI')
plt.legend(loc='upper right')
plt.subplot(3,3,6)
plt.title('foods')
plt.plot(range(1, 12 + 1 ,1), foods_state.groupby(['month']).mean().CA, label='CA')
plt.plot(range(1, 12 + 1 ,1), foods_state.groupby(['month']).mean().TX, label='TX')
plt.plot(range(1, 12 + 1 ,1), foods_state.groupby(['month']).mean().WI, label='WI')
plt.legend(loc='upper right')
plt.subplot(3,3,7)
plt.title('hobbies')
plt.plot(range(2011, 2016 + 1 ,1), hobbies_state.groupby(['year']).mean().CA, label='CA')
plt.plot(range(2011, 2016 + 1 ,1), hobbies_state.groupby(['year']).mean().TX, label='TX')
plt.plot(range(2011, 2016 + 1 ,1), hobbies_state.groupby(['year']).mean().WI, label='WI')
plt.legend(loc='upper right')
plt.subplot(3,3,8)
plt.title('household')
plt.plot(range(2011, 2016 + 1 ,1), household_state.groupby(['year']).mean().CA, label='CA')
plt.plot(range(2011, 2016 + 1 ,1), household_state.groupby(['year']).mean().TX, label='TX')
plt.plot(range(2011, 2016 + 1 ,1), household_state.groupby(['year']).mean().WI, label='WI')
plt.legend(loc='upper right')
plt.subplot(3,3,9)
plt.title('foods')
plt.plot(range(2011, 2016 + 1 ,1), foods_state.groupby(['year']).mean().CA, label='CA')
plt.plot(range(2011, 2016 + 1 ,1), foods_state.groupby(['year']).mean().TX, label='TX')
plt.plot(range(2011, 2016 + 1 ,1), foods_state.groupby(['year']).mean().WI, label='WI')
plt.legend(loc='upper right')

plt.show()


# Here we look at the sales from differnt perspectives. Week, month, and year.
# * week
#     * In every state and every product type, all the trends of sales are the same. Peak on Saterday , decrease till Thursday, and rise on Friday. Therefore,  form a deep valley.
#     * Maybe this is the reason why there is a dense oscillation between growth and recession of the sales through the years.
# * month
#     * There is an obvious hill in the curves of "household" and "food" between May and September.
#     * Coinsidently, summer vacation starts from June to August. So, maybe when people start to enjoy their vacations, the needs for food and household increase. And that's why the sales of household and food reach their peaks between June and August. Then strat decreasing in September, when summer vacation ends.
#     * Perhaps this kind of up and down is why when the sales increase everey years, there is an "S" shape trend. 
#     * Though there is an interesting thing to point out. While "household" and "food" increase in summer vacation. "hobbies" decreases in the exectly same period. And that is pretty weird, shouldn't people go outside and play?? Maybe some Americans can help me understand this.
# * year
#     * As the econemy grow in America, yearly sales in every state basically grow every year, except for year 2014. There is quite a bit of a set back in 2014. Perhaps something hug happened in that year.
#     * So here are a few things went on taht year: "Ebola Epidemic Becomes Global Health Crisis", "Rise of ISIS", "California facing extreme drought", "World cup", "Ferguson protests", "Bill Cosby rape"

# ## Perspective of price

# In[ ]:


plt.figure(figsize=(12, 12))
plt.subplot(2,1,1)
hobbies_1_prices = sell_prices.loc[sell_prices['item_id'].str.contains('HOBBIES_1')]
hobbies_1_prices_CA = hobbies_1_prices.loc[hobbies_1_prices['store_id'].str.contains('CA')]
hobbies_1_prices_TX = hobbies_1_prices.loc[hobbies_1_prices['store_id'].str.contains('TX')]
hobbies_1_prices_WI = hobbies_1_prices.loc[hobbies_1_prices['store_id'].str.contains('WI')]
grouped_CA = hobbies_1_prices_CA.groupby(['wm_yr_wk'])['sell_price'].mean()
plt.plot(grouped_CA.index, grouped_CA.values, label="CA")
grouped_TX = hobbies_1_prices_TX.groupby(['wm_yr_wk'])['sell_price'].mean()
plt.plot(grouped_TX.index, grouped_TX.values, label="TX")
grouped_WI = hobbies_1_prices_WI.groupby(['wm_yr_wk'])['sell_price'].mean()
plt.plot(grouped_WI.index, grouped_WI.values, label="WI")
plt.legend(loc=(1.0, 0.5))
plt.title('HOBBIES_1 mean sell prices by state');
plt.subplot(2,1,2)
cal = calendar[['wm_yr_wk', 'd']]
cal = cal.rename(columns={"d": "index"})
hobbies_1 = train_sales.loc[train_sales['item_id'].str.contains('HOBBIES_1')]
hobbies_1_CA = hobbies_1.loc[hobbies_1['store_id'].str.contains('CA')].drop(columns = ['id','item_id','dept_id','cat_id','store_id','state_id']).sum().reset_index().drop(1913)
hobbies_1_TX = hobbies_1.loc[hobbies_1['store_id'].str.contains('TX')].drop(columns = ['id','item_id','dept_id','cat_id','store_id','state_id']).sum().reset_index().drop(1913)
hobbies_1_WI = hobbies_1.loc[hobbies_1['store_id'].str.contains('WI')].drop(columns = ['id','item_id','dept_id','cat_id','store_id','state_id']).sum().reset_index().drop(1913)
hobbies_1_CA = pd.merge(hobbies_1_CA, cal, on='index')
hobbies_1_TX = pd.merge(hobbies_1_TX, cal, on='index')
hobbies_1_WI = pd.merge(hobbies_1_WI, cal, on='index')
grouped_CA = hobbies_1_CA.drop(columns = "index").groupby(['wm_yr_wk']).sum()
plt.plot(grouped_CA.index, grouped_CA.values, label="CA")
grouped_TX = hobbies_1_TX.drop(columns = "index").groupby(['wm_yr_wk']).sum()
plt.plot(grouped_TX.index, grouped_TX.values, label="TX")
grouped_WI = hobbies_1_WI.drop(columns = "index").groupby(['wm_yr_wk']).sum()
plt.plot(grouped_WI.index, grouped_WI.values, label="WI")
plt.legend(loc=(1.0, 0.5))
plt.title('HOBBIES_1 sum sales by state');


# * Here are a few funny things in these two graphs. The upper one shows the prices of hobbies_1 through the time series. The lower one shows the sales through the time series. Here are the funny stuffs:
#     * Whenever there is a raise in price, there is a drop in sales. 
#     * After a drop in sales, it slowly climbs back. Then walmart raise it's price again, sales drops again. As this goes, walmart manages to get more money without losing customers in the long term.
#     * Walmart raise it's price nationally.

# ## Find the sales with different mean
# Here I use **simple moving average**, **weighted moving average**, and **exponential moving average** to find the tendency of sales in the close period.<br/>
# As you can see in the graph each mean method revealed different tendency. This might come handy in the feature.

# In[ ]:


def SMA(days, n):
    total = 0
    for i in range(n):
        total = total + days[i]
    return total/n

def count_SMA(orig, n):
    ret = np.zeros(len(orig) - n)
    for i in range(len(ret)):
        ret[i] = SMA(np.array(orig[i:i+n]), n)
    return ret

def WMA(days, n):
    total = 0
    dev = 0
    for i in range(n):
        total = total + (n-i)*days[i]
        dev = dev + (n-i)
    return total/dev

def count_WMA(orig, n):
    ret = np.zeros(len(orig) - n)
    for i in range(len(ret)):
        ret[i] = WMA(np.array(orig[i:i+n]), n)
    return ret

def EMA(days, n):
    total = 0
    a = 2/(n+1)
    for i in range(n):
        total = total + a*(days[i] - total)
    return total

def count_EMA(orig, n):
    ret = np.zeros(len(orig) - n)
    for i in range(len(ret)):
        ret[i] = EMA(np.array(orig[i:i+n]), n)
    return ret


# In[ ]:


hobbies_1_CA = hobbies_1_CA.rename(columns={0: "sales"})


# In[ ]:


CA_SMA_28 = count_SMA(hobbies_1_CA['sales'], 28)
CA_WMA_28 = count_WMA(hobbies_1_CA['sales'], 28)
CA_EMA_28 = count_EMA(hobbies_1_CA['sales'], 28)


# In[ ]:


plt.figure(figsize=(12, 6))
plt.subplot(3,1,1)
plt.plot(range(len(hobbies_1_CA['sales'])), hobbies_1_CA['sales'], label="original")
plt.plot(range(len(CA_SMA_28)), CA_SMA_28, label="SMA")
plt.legend(loc=(1.0, 0.5))
plt.subplot(3,1,2)
plt.plot(range(len(hobbies_1_CA['sales'])), hobbies_1_CA['sales'], label="original")
plt.plot(range(len(CA_WMA_28)), CA_WMA_28, label="WMA")
plt.legend(loc=(1.0, 0.5))
plt.subplot(3,1,3)
plt.plot(range(len(hobbies_1_CA['sales'])), hobbies_1_CA['sales'], label="original")
plt.plot(range(len(CA_EMA_28)), CA_EMA_28, label="EMA")
plt.legend(loc=(1.0, 0.5))
plt.show()


# # Modeling
# Frome the EDA we saw that there is obvious relationship between time(week day, month, year) and te sales. So, the training data attributes contains time. At the moment, these are the only attributre. Perhaps in the features there will be more attributes.

# In[ ]:


def melt_sales(df):
    df = df.drop(["item_id", "dept_id", "cat_id", "store_id", "state_id", "total_sales"], axis=1).melt(
        id_vars=['id'], var_name='d', value_name='demand')
    return df

sales = melt_sales(train_sales)


# In[ ]:


def map_f2d(d_col, id_col):
    eval_flag = id_col.str.endswith("evaluation")
    return "d_" + (d_col.str[1:].astype("int") + 1913 + 28 * eval_flag).astype("str")


# In[ ]:


submission = submission_file.melt(id_vars="id", var_name="d", value_name="demand").assign( demand=np.nan, d = lambda df: map_f2d(df.d, df.id))
submission.head()


# In[ ]:


sales_trend = train_sales.drop(columns = ['id','item_id','dept_id','cat_id','store_id','state_id', 'total_sales']).mean().reset_index()
sales_trend.plot()


# In[ ]:


sales_trend.rename(columns={'index':'d', 0: 'sales'}, inplace=True)
sales_trend = sales_trend.merge(calendar[["wday","month","year","d"]], on="d",how='left')
sales_trend = sales_trend.drop(columns = ["d"])


# In[ ]:


def split_sequences(sequences, n_steps):
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the dataset
        if end_ix > len(sequences):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, -1]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


# In[ ]:


in_seq1 = array(sales_trend['wday'])
in_seq2 = array(sales_trend['month'])
in_seq3 = array(sales_trend['year'])
out_seq = array(sales_trend['sales'])
in_seq1 = in_seq1.reshape((len(in_seq1), 1))
in_seq2 = in_seq2.reshape((len(in_seq2), 1))
in_seq3 = in_seq3.reshape((len(in_seq3), 1))
out_seq = out_seq.reshape((len(out_seq), 1))
dataset = hstack((in_seq1, in_seq2, in_seq3, out_seq))
n_steps = 7
X, y = split_sequences(dataset, n_steps)


# In[ ]:


train_x = X[:-30]
train_y = y[:-30]
test_x = X[-30:]
test_y = y[-30:]


# In[ ]:


n_features = train_x.shape[2]


# ## CNN

# Reference: https://machinelearningmastery.com/how-to-develop-convolutional-neural-network-models-for-time-series-forecasting/

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Flatten
from keras.layers import TimeDistributed
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D


# In[ ]:


model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')


# In[ ]:


model.fit(train_x, train_y, epochs=400, verbose=0)


# In[ ]:


last_30_400 = np.zeros(30)
i = 0
for test in test_x:
    test = test.reshape((1, n_steps, n_features))
    last_30_400[i] = model.predict(test, verbose=0)
    i = i + 1


# ## Results
# Below are the results of the trained CNN with different epochs. As you can see, CNN starts to the learn the trend in 50 epochs. After 300 epochs, the predicted trend and real trend has exectly the same ups and downs.<br/>
# The result of this method is pretty bad. The score is 2.33440. I will keep work on this and see if I can do anything to improve it.
# ![](https://i.imgur.com/qevsAxX.png)

# In[ ]:


subs = submission.groupby(['d']).mean().reset_index()
result = subs 


# In[ ]:


subs = subs.merge(calendar[["wday","month","year","d"]], on="d",how='left')
subs = subs.drop(columns = ["d", "demand"])
subs = pd.concat([sales_trend, subs], ignore_index=True, sort=False)


# In[ ]:


in_seq1 = array(subs['wday'])
in_seq2 = array(subs['month'])
in_seq3 = array(subs['year'])
out_seq = array(np.zeros(1969))
in_seq1 = in_seq1.reshape((len(in_seq1), 1))
in_seq2 = in_seq2.reshape((len(in_seq2), 1))
in_seq3 = in_seq3.reshape((len(in_seq3), 1))
out_seq = out_seq.reshape((len(out_seq), 1))
dataset = hstack((in_seq1, in_seq2, in_seq3, out_seq))
n_steps = 7
X, y = split_sequences(dataset, n_steps)


# In[ ]:


subs = X[-56:]


# In[ ]:


i = 0
for sub in subs:
    sub = sub.reshape((1, n_steps, n_features))
    result['demand'][i] = model.predict(sub, verbose=0)
    i = i + 1


# In[ ]:


for i in range(1,29):
    submission_file.loc[submission_file.id.str.contains("validation"), "F" + str(i)] = result["demand"][i-1]
    submission_file.loc[submission_file.id.str.contains("evaluation"), "F" + str(i)] = result["demand"][i + 28-1]


# In[ ]:


submission_file.to_csv('submission.csv', index=False)


# In[ ]:




