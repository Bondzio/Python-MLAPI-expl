#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# One stepping stone to the future energy grid is the roll out of smart meters. Smart meter's record conumption while communicating the measured data to the electricity supplier for monitoring and billing. Communication in both ways from electricity supplier to consumer and vice versa are both possible enabling the intelligent control of the energy grid. In addition, the consumer can call up his or her energy consumption at any time with time resolution (f.e. via an mobile-app). With direct feedback of energy consumption, consumers tend to archive higher energy savings for electricity and gas consumption. 
# 
# In 2014 the dutch goverment decided to roll out smart meters to every home and aim at 3 million households with smart meters by 2016. By 2020 the goverment aims to reach at least 80%, but preferably 100% installed. 
# 
# ![Smart meter example](https://asset.re-in.de/isa/160267/c1/-/de/1404245_BB_00_FB/GEO-PCK-MP-003-Energiekosten-Messgeraet-beleuchtete-Anzeige-Kostenprognose-LCD-Farbdisplay-Stromtarif-einstellbar-inkl.jpg?x=225&y=225&ex=225&ey=225&align=center)
# 
# This kernel aims to investigate the roll-out of smart meters by use of Longitude and Latitude data for cities and other additional data sets.
# 
# I hope you enjoy my first kernel and some of the ideas I put to the "Energy consumption of the Netherlands"-Dataset.
# 
# **Work in Progress**

# In[ ]:


import numpy as np 
import pandas as pd 
import os
import re
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("white")


# **Load all Data from the Dataset aswell as Longitude and Latitude data: **

# In[ ]:


## got parts of this from NMenezes Kernel couldnt figure importing all csv at once out!

#Dataset: 
csv_array =[] # Saving a list of all possible csv names

dict_df = dict()
for file in os.listdir("../input/dutch-energy/dutch-energy/Electricity/"):
    
    company = file.split('_')[0]
    year = re.findall('2+[0-9]+',file.split('_')[2])[0]
    dict_df[company+year] = pd.read_csv("../input/dutch-energy/dutch-energy/Electricity/"+file)
    csv_array.append(company+year)

#Long / Lat data:    
df_cities = pd.read_csv("../input/long-and-latitude-of-most-nl-towns/nl_towns.csv",delimiter=";", encoding = "ISO-8859-1")  

# convert city names to lowercase
df_cities["city"] = df_cities["city"].str.lower()
for file_name in csv_array:
    dict_df[file_name]["city"]= dict_df[file_name]["city"].str.lower()


# In[ ]:


dict_df["enexis2018"].head()


# In[ ]:


df_cities.drop(df_cities[df_cities["long"]<30].index,inplace=True) #Drop Long/lat data from nl colonies
sns.scatterplot(y="long",x="lat",data=df_cities)


# Merge Dataframe with Energy consumption and Long Lat data + additional features:

# In[ ]:


for file_name in csv_array:
    dict_df[file_name] = pd.merge(dict_df[file_name],df_cities,how='left', on='city')
    dict_df[file_name][['long', 'lat']] = dict_df[file_name][['long', 'lat']].fillna(0)
    dict_df[file_name]["produced_energy"] =  dict_df[file_name]["delivery_perc"]*dict_df[file_name]["annual_consume"] #Self produces energy



# In[ ]:


#data cleanup: 
dict_df["enexis2018"]["pop"][dict_df["enexis2018"]["city"]=="zwolle"] = 111805.0
dict_df["enexis2018"]["pop"][dict_df["enexis2018"]["city"]=="boekel"] = 5480.0
dict_df["enexis2018"]["pop"][dict_df["enexis2018"]["city"]=="gennep"] = 16642.0
dict_df["stedin2018"]["pop"][dict_df["stedin2018"]["city"]=="weert"] = 48662.0


# In[ ]:


missing_gis = 0 
for file_name in csv_array:
    df_in_question = dict_df[file_name].groupby("city").mean()
    missing_gis += len(df_in_question[df_in_question["long"]==0])
print("Currently we have: "+str(missing_gis)+" missing values for Longitude and Latitude") 


# Making a visualisation of the smart_meter spreading:
# ![Smart meter spread](https://i.imgur.com/ANBpQYd.gif )

# In[ ]:


#code for creating the gif is based of Bojk's kernel: https://www.kaggle.com/bberghuis/dutch-electricity-a-first-look
#kind = "_smartmeter_perc"
#for i in range(2010,2019):
#    f = plt.figure(figsize=(15,15))
#    y=str(i)
#
#    sns.scatterplot(y="long",x="lat",data=dict_df['enexis'+y].groupby("city").mean(),label="Enexis",s=dict_df['enexis'+y].groupby("city").mean()["smartmeter_perc"])
#    sns.scatterplot(y="long",x="lat",data=dict_df['liander'+y].groupby("city").mean(),label="Liander",s=dict_df['liander'+y].groupby("city").mean()["smartmeter_perc"])
#    sns.scatterplot(y="long",x="lat",data=dict_df['stedin'+y].groupby("city").mean(),label="Stedin",s=dict_df['stedin'+y].groupby("city").mean()["smartmeter_perc"])
#    
#
#    plt.title(y,fontsize=18)
#    plt.ylabel('Longitude')
#    plt.ylim(50.5,54)
#    plt.xlabel('Latitude')
#    plt.xlim(3.9,7.5)
#    lgnd = plt.legend(['Enexis','Liander','Stedin'],loc='lower right')
#    lgnd.legendHandles[0]._sizes = [50]
#    lgnd.legendHandles[1]._sizes = [50]
#    lgnd.legendHandles[2]._sizes = [50]
#    f.savefig(y+kind+'.png')
#    plt.close(f)


#import imageio
#import glob
#files = glob.glob("*"+kind+'.png')
#files = np.sort(files)
#from shutil import copyfile
#for file in files:
#    copyfile(file, file.split('.')[0]+'_1.png')
#files = glob.glob("*"+kind+"_1"+'.png')
#filey = glob.glob("*"+kind+'.png')
#files = filey+files
#files = np.sort(files)
#images = []
#for file in files:
#    images.append(imageio.imread(file))
#imageio.mimsave('smartmeter-spread.gif', images)
#
# step 3: prep the gif for display in notebook 
#from IPython.display import Image
#Image("smartmeter-spread.gif")


# In[ ]:


# Calculate the rate of smart meter roll out:
# smart_meter%[year+1]-smart_meter%[year]:
energy_supplier = ["enexis","liander","stedin"]
for supplier in energy_supplier:
    for year in range(2010,2019):
        y = str(supplier+str(year))
        if y == supplier+"2010":
          dict_df[y]["smartmeter_rate"] = 0
        else:
          dict_df[y]["smartmeter_rate"] = dict_df[y]["smartmeter_perc"]-dict_df[str(supplier+str(year-1))]["smartmeter_rate"]
    


# In the next gif you can see the roll out rate for each town. The rate increases with the years!
# 
# ![Smart meter spread](https://i.imgur.com/CF8VSbO.gif )
# 

# In[ ]:


#code for creating the gif is based of Bojk's kernel: https://www.kaggle.com/bberghuis/dutch-electricity-a-first-look

#kind = "_smartmeter_rate"
#for i in range(2010,2019):
#    f = plt.figure(figsize=(15,15))
#    y=str(i)

#    sns.scatterplot(y="long",x="lat",data=dict_df['enexis'+y].groupby("city").mean(),label="Enexis",s=dict_df['enexis'+y].groupby("city").mean()["smartmeter_rate"])
#    sns.scatterplot(y="long",x="lat",data=dict_df['liander'+y].groupby("city").mean(),label="Liander",s=dict_df['liander'+y].groupby("city").mean()["smartmeter_rate"])
#    sns.scatterplot(y="long",x="lat",data=dict_df['stedin'+y].groupby("city").mean(),label="Stedin",s=dict_df['stedin'+y].groupby("city").mean()["smartmeter_rate"])
    

#    plt.title(y,fontsize=18)
#    plt.ylabel('Longitude')
#    plt.ylim(50.5,54)
#    plt.xlabel('Latitude')
#    plt.xlim(3.9,7.5)
#    lgnd = plt.legend(['Enexis','Liander','Stedin'],loc='lower right')
#    lgnd.legendHandles[0]._sizes = [50]
#    lgnd.legendHandles[1]._sizes = [50]
#    lgnd.legendHandles[2]._sizes = [50]
#    f.savefig(y+kind+'.png')
#    plt.close(f)



#import imageio
#import glob
#files = glob.glob("*"+kind+'.png')
#files = np.sort(files)
#from shutil import copyfile
#for file in files:
#    copyfile(file, file.split('.')[0]+'_1.png')
#    copyfile(file, file.split('.')[0]+'_1_1.png')
#files = glob.glob("*"+kind+"_1"+'.png')
#filey = glob.glob("*"+kind+'.png')
#fileyy = glob.glob("*"+kind+"_1"+"_1"+'.png')
#files = filey+files+fileyy
#files = np.sort(files)
#images = []
#for file in files:
#    images.append(imageio.imread(file))
#imageio.mimsave('smartmeter-rate.gif', images)

#from IPython.display import Image
#Image("smartmeter-rate.gif")


# **I decided to add the location of charger stations in the netherlands: **

# In[ ]:


import json
import requests


# In[ ]:


response = requests.get("https://api.openchargemap.io/v2/poi/?output=json&countrycode=NL&maxresults=1000000&compact=true&verbose=false&opendata=true")
data_chargers = json.loads(response.text)


# In[ ]:


#save all town and lat long from smart charger stations:
n_results = len(data_chargers)

df_chargers = pd.DataFrame(columns=["city","long","lat"])
dict_chargers=[]
for i in range(n_results):
    if "Town" in data_chargers[i]["AddressInfo"] and data_chargers[i]["AddressInfo"]["CountryID"]==159:
        dict_chargers.append(dict(zip(["city","long","lat"],[data_chargers[i]["AddressInfo"]["Town"].lower(),data_chargers[i]["AddressInfo"]["Longitude"],data_chargers[i]["AddressInfo"]["Latitude"]])))
df_chargers = pd.DataFrame(data=dict_chargers)


# **Quite a lot long and lat data from the query are out of bounds for the netherlands:**

# In[ ]:


plt.figure(figsize=(5,5))
sns.scatterplot(y="lat",x="long",data=df_chargers[(df_chargers["lat"]>50)&(df_chargers["lat"]<55)])


# Constraining the data set by filtering with maximum lat and long values: 

# In[ ]:


plt.figure(figsize=(5,5))
df_chargers = df_chargers[(df_chargers["lat"]>50)&(df_chargers["lat"]<55)&(df_chargers["long"]<7.3)]
sns.scatterplot(y="lat",x="long",data=df_chargers)


# As in case of the wrong lat long data we'll keep them for now since I am not sure how to effectivly remove them from the dataset.
# 
# Some are classified with the wrong country code, see: 
# 

# In[ ]:


import mplleaflet
from random import randint

fig, ax = plt.subplots()
x = [df_chargers["long"][3000:4000]]
y = [df_chargers["lat"][3000:4000]]
ax.plot(x, y, 'bo')
mplleaflet.display(fig=fig)


# In[ ]:


print("Start: Number of remaining Data points: "+ str(len(df_chargers)))
s1 = pd.Series(df_chargers["city"].value_counts().index)
s2 = pd.Series(df_chargers["city"].value_counts().values)
df = pd.concat([s1, s2], axis=1)
df.columns = ["city","count"]
df_chargers = pd.merge(df_chargers,df,how="left",on="city")
df_chargers.drop_duplicates(inplace=True,subset=["city"])

print("End: Number of remaining Data points: "+ str(len(df_chargers)))


# Distribution of charger stations, size represents the number of charger stations in given city:

# In[ ]:


plt.figure(figsize=(10,10))
df_chargers = df_chargers[(df_chargers["lat"]>50)&(df_chargers["lat"]<55)&(df_chargers["long"]<7.3)]
sns.scatterplot(y="lat",x="long",data=df_chargers,s =df_chargers["count"]*1 )
plt.text(y=52.070499,x=4.420700,s= "Den Haag",horizontalalignment='left', size='medium', color='black')
plt.text(y=52.370216,x=4.895168,s= "Amsterdam",horizontalalignment='left', size='medium', color='black')
plt.text(y=51.924419,x=4.527733,s= "Rotterdam",horizontalalignment='left', size='medium', color='black')


# **Top 10 cites by number of charger stations:**

# In[ ]:


top10_cities = df_chargers[["city","count"]].sort_values(by =["count"],axis=0,ascending=False).head(10)

for city in top10_cities["city"]:
    sns.scatterplot(y="lat",x="long",data=df_chargers[df_chargers["city"]==city],s =df_chargers["count"][df_chargers["city"]==city],label=city )
plt.legend(loc='center right', bbox_to_anchor=(1.5, 0.5), ncol=1)
plt.text(y=52.070499,x=4.420700,s= "Den Haag",horizontalalignment='left', size='medium', color='red')
plt.text(y=52.370216,x=4.895168,s= "Amsterdam",horizontalalignment='right', size='medium', color='red')
plt.text(y=51.924419,x=4.527733,s= "Rotterdam",horizontalalignment='left', size='medium', color='red')


# **Roll out of smart meters and cities with highest amount of electric chargers:**
# ![](https://i.imgur.com/TaeVTXo.gif)

# Just looking at the gif it seems like there isn't a correlation between charger station distribution and the number of charger stations. Possibly a nominalisation with population (chargers/pop) is better here! 

# In[ ]:


#Add chargers to data frames:
for file_name in csv_array:
    dict_df[file_name] = pd.merge(dict_df[file_name],df_chargers.drop(["lat","long"],axis=1),how='left', on='city')
    dict_df[file_name].fillna(0).replace(np.inf, 0)


# In[ ]:


# calculate chargers / citizens

for file_name in csv_array:
    dict_df[file_name]["chargers_pop"] =  dict_df[file_name]["count"]/ dict_df[file_name]["pop"]
    dict_df[file_name]["chargers_pop"].replace(np.inf, 0,inplace=True)


# In[ ]:


dict_df["enexis2018"].head()


# In[ ]:


y=str(2018)
sns.scatterplot(y="long",x="lat",data=dict_df['enexis'+y].groupby("city").mean(),label="Enexis",s=dict_df['enexis'+y].groupby("city").mean()["chargers_pop"]*1000)
sns.scatterplot(y="long",x="lat",data=dict_df['liander'+y].groupby("city").mean(),label="Liander",s=dict_df['liander'+y].groupby("city").mean()["chargers_pop"]*1000)
sns.scatterplot(y="long",x="lat",data=dict_df['stedin'+y].groupby("city").mean(),label="Stedin",s=dict_df['stedin'+y].groupby("city").mean()["chargers_pop"]*1000)
plt.title("Chargers per Citizens in the Netherlands")


# In[ ]:


print("Cities with the highest share of chargers in their population:")
print(dict_df["enexis2018"][["city","chargers_pop"]].drop_duplicates().sort_values(by=["chargers_pop"],axis =0,ascending=False).head(3))
print(dict_df["liander2018"][["city","chargers_pop"]].drop_duplicates().sort_values(by=["chargers_pop"],axis =0,ascending=False).head(3))
print(dict_df["stedin2018"][["city","chargers_pop"]].drop_duplicates().sort_values(by=["chargers_pop"],axis =0,ascending=False).head(3))


# Zwolle almost has one charger for each of their citizens!! Since their citizen count is above 100k it seems rather unrealistic to believe that they have 100k electric chargers!
# 
# 
# Zwolle has the population wrongfully allocated every second line. 
# Since we are using the mean() function to group by city for further calculations the wrongful allocation of population to zwolle results in an error for the share of chargers per citizen:

# In[ ]:


dict_df["enexis2018"][["city","pop"]][dict_df["enexis2018"]["city"]=="zwolle"].head()


# Future work includes:
# 
# -  Data clean up
# 
# - Connecting lat long data for smart meter spread and charger stations
#   
# - Additional feature calculations
#   
# - Code cleanup & Improvements

# In[ ]:


dict_df["enexis2018"].corr()


# In[ ]:




