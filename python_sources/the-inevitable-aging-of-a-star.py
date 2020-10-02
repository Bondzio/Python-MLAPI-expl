#!/usr/bin/env python
# coding: utf-8

# # The inevitable aging of a star
# Kobe Bryant has been one of the most dominant players in the NBA through out the last two decades, arguably the best since the (2nd) retirement of Michael Jordan in 1998.  However, in this script I will claim that as a human being and despite his physical superiority, Bryant is not immune to the effect of aging. 
# 
# I will show that as the years go by, Kobe has increasingly preferred the long distance shot rather than the lay-up, as his amazing athleticism and speed slowly degrade. 
# 
# While this might simply imply an improvement of his style, and maybe in the overall NBA playing style, the fact that his overall field goals went down shows that this was a restriction that was imposed upon him by the inevitable advancement of his biological clock rather than a positive evolution of him as a player.
# 
# 
# 

# # Load Libraries

# In[ ]:


import pandas as pd #the whole data will be stored in a pandas data frame
import matplotlib.pyplot as plt  #for plotting the data
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib
matplotlib.style.use('fivethirtyeight')
import numpy as np #for numbers handling 


# # This Great script for drawing the courst was stolen from MichaelKrueger's excelent script:

# In[ ]:


def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax
    


# # Read the data and modify it

# In[ ]:


df = pd.read_csv('../input/data.csv')
df['numeric_season'] = 1
for row in df.index:
    df['numeric_season'][row] = df.season[row][len(df.season[row])-2:len(df.season[row])]


# # Kobe's average shooting position through out the years:

# In[ ]:


plt.figure(figsize = (10,10))
years = range(16)

average_x = years
average_y = years

ind = 0

for i,year in enumerate(years):

    x = np.mean(df.loc_x[df.numeric_season==year])
    y = np.mean(df.loc_y[df.numeric_season==year])
    dist = np.sqrt(np.power(x,2) + np.power(y,2))
    plt.plot(x,y,'ro',hold = True,markersize = ind+10, label = str(2000 +year))
    ind = ind + 1
         
plt.ylim([0,200])
plt.xlim([-100,100])
draw_court(outer_lines=True)
plt.legend(fontsize = 20,numpoints=1)
plt.show()


# # Kobe is getting away from the basket as years go by
# 
# 

# In[ ]:


df['Dist'] = np.power(df.loc_x,2)+np.power(df.loc_y,2)
df['Dist'] = np.sqrt(df.Dist)
years = [97,98,99,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
ind = 0
avg_dist = years
for year in years:

    avg_dist[ind] = np.mean(df.Dist[df.numeric_season==year])
    ind = ind + 1
avg_dist = np.divide(avg_dist,41.6)
years = [1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]
coff = np.polyfit(years,avg_dist, 1, rcond=None, full=False, w=None, cov=False)
x = np.linspace(1996,2018,100)
y = np.multiply(coff[0],x) + coff[1]

plt.figure(figsize = (10,10))
plt.xlim([1996,2017])
plt.xlabel('Year')
plt.ylabel('Average Shot Distance [m]')
plt.grid()
plt.plot(x,y,'r')
plt.plot(years,avg_dist,'o', markersize = 20)
plt.show()


# # Kobe's Average distance shot per year
# 
#  - We can see that Kobe's is getting consistently further from the basket
#  - In 18 years, he hot about 2 meters away from the basket on average. this doesn't tell the whole story of course. it is possible that kobe simply took similar shots but slightly further, or that the whole shot distribution has changed. let's further investigate this hypothesis
# 
# 

# # Kobe Shots Distribution over the years

# In[ ]:


shot_type = dict()
types = np.unique(df.combined_shot_type)
years = [97,98,99,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

for s_type in types:
    
    temp = list(range(len(years)))
    ind = 0
    
    for year in years:
        temp[ind] = np.true_divide(len(df[(df.combined_shot_type==s_type) & (df.numeric_season == year)]),len(df[df.numeric_season==year]))
        ind = ind + 1
              
    shot_type[s_type] = temp
    
plot_years = np.linspace(1997,2016,20)

plt.figure(figsize = (10,10))
plt.bar(plot_years,shot_type['Jump Shot'])
plt.bar(plot_years,shot_type['Layup'],bottom =shot_type['Jump Shot'], color = 'r' )  
bot = np.add(shot_type['Jump Shot'] ,shot_type['Layup'])
plt.bar(plot_years,shot_type['Dunk'],bottom = bot,color = 'g')  
plt.xlabel('Year')
plt.ylabel('% of shots')
plt.legend(['Jump Shot','Layup','Dunk'],loc = 3,fontsize = 25)
plt.ylim([0,1])
plt.xlim([1997,2017])
plt.show()


# # Kobe shot's distribution:
# 
# 1. In his early career, almost 40% of Kobe's shots were a results of a penetration (Lay-ups and Dunks)
# 2. in his last year, these kind of shots composed less than 20% of his total shots

# # Zoom in on one of his first and his last season tells the story

# In[ ]:


plt.figure(figsize = (10,10))
shot_hist_98 = np.histogram(df.shot_distance[df.numeric_season == 98],bins = 50)
shot_hist_16 = np.histogram(df.shot_distance[df.numeric_season == 16],bins = 50)
plt.plot(np.divide(shot_hist_98[1][1:],3.3),shot_hist_98[0],color = 'r')
plt.plot(np.divide(shot_hist_16[1][1:],3.3),shot_hist_16[0],color = 'b')
three_plot_x = [7.45,7.45]
three_plot_y = [0,350]

plt.plot(three_plot_x,three_plot_y, color = 'g')
plt.xlim([0,15])
plt.xlabel('Distance From Basket [m]')
plt.ylabel('Number of Shots')
plt.legend(['1998','2016','3 Points line'], loc = 1,fontsize = 20)

plt.show()


# As we can see, there is a huge difference between the two distributions:
# 
#  - In 1998, the most common shot distance was ~1m - which almost
#    necessarily represents a dunk or a lay-up shot, usually after passing
#    at least one defender
#  - In 2016, on the contrary, the most common shot was beyond the 3-points line, which usually doesn't require passing any defendant

# # But are these necessarily bad signs? could it be that Kobe simply mastered the shot for 3, rendering the penetration obsolete? 

# In[ ]:




years = [97,98,99,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
field_goals = []
for year in years:
    shots = len(df[df.numeric_season == year])
    shots_made = len(df[(df.numeric_season == year) & (df.shot_made_flag == 1)])
    field_goals.append(shots_made/shots)
    
plt.figure(figsize = (10,10))
plt.title('Field Goals over time')
plt.ylabel('Field Goals')
plt.xlabel('Year')
plt.plot(np.arange(1997,2017,1),field_goals,'-o', markersize = 20)


# # So was the transition to long distance shots an improvement or the sign of decay? the answer is both

#  - we can see that at the beginning of his career, Kobe's field goals improved despite the fact that as we have seen the average shot distance increases and the rate of lay-ups and dunks - which are treditionally considered to be easy shots - decreases. this means the ripe Kobe, form 2000 to 2008, is better than young Kobe. Either in terms of shot selection or simply aiming skills. 
# 
#  - However, after the year 2008 (when Kobe is still in his prime and the Lakers are the best team in the NBA), we start to see that Kobe's field goals start to go down, they eventually plummet quite dramatically at the end of his career
