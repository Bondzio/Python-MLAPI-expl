#!/usr/bin/env python
# coding: utf-8

# For the neophytes in the Eurovision song festival, which will be few, comment that it is a television contest that is held every year and that involved the different televisions of mainly European countries. Win the country that gets the most votes and each country gives 12 points to the song they like the most, 10 to the second and then descending the points from 8 to 1.
# 
# Every year during and after the voting, there is a debate about the lack of impartiality of some countries in the allocation of the points since it seems that some participants have a tendency to vote among themselves.
# 
# I'm going to take a look at the voting data in Eurovision between 1975 and 2017.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3
import pandas.io.sql as psql
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import networkx as nx
import os

get_ipython().run_line_magic('matplotlib', 'inline')

print(os.listdir("../input"))


# In[ ]:


dt_eurovision=pd.read_excel('../input/eurovision_song_contest_1975_2017v4.xlsx')
dt_eurovision.head()


# In[ ]:


# Upload the data in a SQLite database to facilitate queries
conn = sqlite3.connect("eurovision_1975_2017.sl3")
curs = conn.cursor()
create_table_sql ="CREATE TABLE eurovision(YEAR character varying(50),FINAL_SEMI character varying(50), EDITION character varying(50),JURY_OR_TELEVOTING character varying(50), FROM_COUNTRY character varying(255), TO_COUNTRY character varying(255), POINTS integer, DUPLICATE character varying(50));"
curs.execute(create_table_sql)

for index, row in dt_eurovision.iterrows():
    curs.execute("INSERT INTO eurovision (YEAR, FINAL_SEMI, EDITION, JURY_OR_TELEVOTING, FROM_COUNTRY, TO_COUNTRY, POINTS, DUPLICATE) VALUES (:YEAR, :FINAL_SEMI, :EDITION, :JURY_OR_TELEVOTING, :FROM_COUNTRY, :TO_COUNTRY, :POINTS, :DUPLICATE)", 
                         {"YEAR": row[0], "FINAL_SEMI": row[1], "EDITION":row[2], "JURY_OR_TELEVOTING":row[3], "FROM_COUNTRY": row[4], "TO_COUNTRY": row[5], "POINTS": row[6], "DUPLICATE": row[7]})
conn.commit()


# List of countries that always or almost always give the highest score (12) to the same countries.

# In[ ]:


# Calculate the average of the points that each country gives to another
df_average = pd.read_sql("SELECT FROM_COUNTRY, TO_COUNTRY, SUM(POINTS) SUM_POINTS, count(POINTS) as N_PARTICIPATIONS, "
                         "SUM(POINTS)/count(POINTS) AS AVERAGE_POINTS " 
                         "FROM eurovision " 
                         "GROUP BY FROM_COUNTRY, TO_COUNTRY;", conn)
df_average.sort_values(by=['AVERAGE_POINTS', 'N_PARTICIPATIONS'], ascending=False).head(20)


# Show "curious" cases like Turkey that has always been able to give 12 points to Azerbaijan and vice versa. Although they are not the only ones with a clear bias in the votes, the list is extensive and an average above 5 is suspect.

# **Histogram of average values**
# 
# Distribution of the values of the averages (AVERAGE). For a system 100% random should be between 0 and 2.

# In[ ]:


mpl.rcParams['figure.figsize'] = (12.0, 9.0)
plt.hist(df_average.AVERAGE_POINTS.astype(int))
plt.show()


# We must bear in mind that voting on songs from other countries does not have to be random because there are countries with a greater musical trajectory, others with a greater or lesser number of inhabitants, others with more commercial music, others with more similar musical tastes but even taking these points into account it is not normal to have values greater than 5.

# **Matrix with the averages of votes between countries**

# In[ ]:


country_dict = {'Andorra': '0', 'Cyprus': '1', 'Turkey': '2', 'The Netherlands': '3', 'Switzerland': '4', 
                'Italy': '5', 'Hungary': '6', 'Russia': '7', 'Luxembourg': '8', 'Czech Republic': '9', 'Sweden': '10', 
                'Norway': '11', 'Armenia': '12', 'Belarus': '13', 'United Kingdom': '14', 'Netherlands': '15', 
                'Romania': '16', 'Montenegro': '17', 'Austria': '18', 'Australia': '19', 'Ireland': '20', 
                'Germany': '21', 'Macedonia': '22', 'Serbia': '23', 'San Marino': '24', 'Bosnia & Herzegovina': '25', 
                'Portugal': '26', 'Finland': '27', 'Malta': '28', 'Albania': '29', 'Ukraine': '30', 'Lithuania':'31', 
                'Bulgaria': '32', 'Spain': '33', 'Croatia': '34', 'Latvia': '35', 'Serbia & Montenegro': '36', 
                'Azerbaijan': '37', 'Slovenia': '38', 'Greece': '39', 'Georgia': '40', 'Morocco': '41', 
                'Belgium': '42', 'Moldova': '43', 'France': '44', 'Estonia': '45', 'Slovakia': '46', 'Monaco': '47', 
                'Israel': '48', 'Poland': '49', 'Iceland': '50', 'Yugoslavia': '51', 'Denmark': '52', 'F.Y.R. Macedonia': '53'} 
names, symbols = np.array(sorted(country_dict.items())).T


# In[ ]:


mpl.rcParams['figure.figsize'] = (12.0, 9.0)
country_average = np.zeros((names.size, names.size))

for index, row in df_average.iterrows():
    x = int(country_dict[row['FROM_COUNTRY']])
    y = int(country_dict[row['TO_COUNTRY']])
    country_average[x, y] = float(row['AVERAGE_POINTS'])
df_matrix_average = pd.DataFrame(country_average,index=country_dict.keys(),columns=country_dict.keys())
sns.heatmap(df_matrix_average, annot=True)


# **Graph with the countries groups according to the vote**
# 
# Here we show the groups of countries that have a clear tendency to vote among themselves and have an average of more than 9 points, have participated at least 5 times and we only have the scores of the finals.

# In[ ]:


mpl.rcParams['figure.figsize'] = (12.0, 9.0)

sql="SELECT FROM_COUNTRY, TO_COUNTRY, SUM(POINTS), count(POINTS), SUM(POINTS)/count(POINTS) AS average "     "FROM eurovision "     "WHERE FINAL_SEMI = 'f' "     "GROUP BY FROM_COUNTRY, TO_COUNTRY HAVING SUM(POINTS)/count(POINTS) >= 9 "     "AND count(POINTS) > 4 "     "ORDER BY SUM(POINTS) desc;"

cursor = conn.cursor()
cursor.execute(sql)
rows = cursor.fetchall()
list = []
for row in rows:
    list.append((row[0],row[1]))
cursor.close()

# Create a networkx graph object
my_graph = nx.Graph() 
my_graph.add_edges_from(list)
 
# Draw the resulting graph
nx.draw(my_graph, with_labels=True, font_weight='bold')

