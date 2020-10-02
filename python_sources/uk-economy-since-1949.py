#!/usr/bin/env python
# coding: utf-8

# Data comes from the Office of National Statistics (ONS) in the UK. Gross Domestic Product: Year on Year growth: Seasonally Adjusted % Change
# https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/qna
# I have also added ROI and Unemployment and merged onto a single csv. All data is year-on-year % change. Unemployment data starts in 1971.

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_csv("../input/uk_stats.csv")
data.head()


# In[ ]:


plt.figure(figsize=(18,8))
plt.plot(data["Year"], data["GDP"], label='GDP')
plt.annotate("Suez Crisis",xy=(1956,1.7),xytext=(1950,0.5),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Pound Devalued",xy=(1967,2.8),xytext=(1962,0.5),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Oil Crisis",xy=(1973,6.5),xytext=(1967,6),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("UK Joins EEC",xy=(1973,6.5),xytext=(1965,5),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Brexit Referendum 1.0",xy=(1975,-1.0),xytext=(1962,-3),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Oil Crisis II",xy=(1979,3.7),xytext=(1981,5),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Winter of discontent",xy=(1978,4.2),xytext=(1976,5.5),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Falklands Crisis",xy=(1982,2),xytext=(1984,1),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("US Fed Reserve acts to lower inflation",xy=(1988,5.7),xytext=(1991,6.1),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Black Monday",xy=(1987,5.4),xytext=(1981,6.3),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Black Friday",xy=(1989,2.6),xytext=(1991,4.3),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Gulf War",xy=(1990,0.7),xytext=(1984,-1.8),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Maastricht Treaty",xy=(1992,0.4),xytext=(1993,-1.8),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Black Wednesday",xy=(1992,0.4),xytext=(1995,1),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Dot Com peak",xy=(2000,3.4),xytext=(1995,5.5),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("9-11",xy=(2001,3),xytext=(1996,2.1),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Gulf War II",xy=(2003,3.3),xytext=(2005,5),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Financial Crisis",xy=(2007,2.4),xytext=(2010,4),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("2012 Olympics",xy=(2012,1.5),xytext=(2013,0.5),arrowprops=dict(facecolor='black',shrink=0.05))
plt.annotate("Brexit Referendum 2.0",(2016,1.9),xytext=(2018,3),arrowprops=dict(facecolor='black',shrink=0.02))

#Leaders
plt.annotate("Thatcher",(1982,-4),xytext=(1982,-3),arrowprops=dict(facecolor='blue',shrink=0.02))
plt.annotate("Major",(1992,-4.2),xytext=(1992,-3),arrowprops=dict(facecolor='blue',shrink=0.02))
plt.annotate("Blair",(2000,-4),xytext=(2000,-3),arrowprops=dict(facecolor='red',shrink=0.02))
plt.annotate("Brown",(2008,-4.2),xytext=(2005,-3),arrowprops=dict(facecolor='red',shrink=0.02))
plt.annotate("Cameron",(2012,-4),xytext=(2012,-3),arrowprops=dict(facecolor='blue',shrink=0.02))
plt.annotate("May",(2017,-4.2),xytext=(2017,-3),arrowprops=dict(facecolor='blue',shrink=0.02))
plt.annotate("Bojo",(2020,-4),xytext=(2020,-3),arrowprops=dict(facecolor='blue',shrink=0.02))

#Who's in power (red: Labour, blue: Conservative)
plt.plot([1948,1951], [-4,-4], 'r-')
plt.plot([1951,1964], [-4,-4], 'b-')
plt.plot([1964,1970], [-4,-4], 'r-')
plt.plot([1970,1974], [-4,-4], 'b-')
plt.plot([1974,1976], [-4,-4], 'r-')
plt.plot([1976,1979], [-4.2,-4.2], 'r-')
plt.plot([1979,1990], [-4,-4], 'b-')
plt.plot([1990,1997], [-4.2,-4.2], 'b-')
plt.plot([1997,2007], [-4,-4], 'r-')
plt.plot([2007,2010], [-4.2,-4.2], 'r-')
plt.plot([2010,2016], [-4,-4], 'b-')
plt.plot([2016,2019], [-4.2,-4.2], 'b-')
plt.plot([2019,2020], [-4,-4], 'b--')

#Trendlines
plt.plot([1988,2020], [5.9,2.1], 'g--')

#Plot general
plt.xlabel('Year')
plt.ylabel('%')
plt.title("UK GDP (% Change Year on Year)")
#plt.legend()
plt.grid(True)
plt.axhline(y=0,color='k')
plt.show()


# In[ ]:


plt.figure(figsize=(18,7))
#plt.plot(data["Year"], data["GDP"], label='GDP')
plt.plot(data["Year"], data["Inflation"], label='Inflation')
plt.plot(data["Year"], data["Unemployment"], label='Unemployment')

#Plot general
plt.xlabel('Year')
plt.ylabel('%')
plt.title("% Change Year on Year")
plt.legend()
plt.grid(True)
plt.axhline(y=0,color='k')
plt.show()


# **Commentary**
# 
# The period 1950 - 1970 is considered a time when we 'never had it so good'. Economic growth fluctated wildly but the lows were still higher than the average today. However, this masked an underlying weakness of the UK becoming increasingl uncompetitive whilst European and Asian countries were investing in and gaining benefit from new manufacturing technologies. The 'maintain the status quo' mindset led to the UK becoming an economic basket case by the end of the '70s.
# 
# The UK is very vulnerable to external shocks such as the oil crises, or major fiscal decisions made in the US, and these tend to happen at the worst possible time. The 1989 downturn was caused by the US Fed Reserve restricting money supply to reduce inflation, which was rising at very high levels at the time. They succeeded in this goal but crashed the western economies in the process. I remember this all too clearly as I graduated from university in this year and could not get a job.
# 
# Under Thatcher, the UK was painfully dragged, kicking and screaming into a more modern economic model. Economic growth peaked in 1988 and we have not matched that since. In fact, the long term trend since 1988 has been one of declining economic growth. Again, the UK was hit heavily by an external event, this time the 2007/8 Financial Crisis. More recently, growth has stagnated due to the lack of investment in the UK (actually, negative outflow of money) as a result of the Brexit Referendum.
