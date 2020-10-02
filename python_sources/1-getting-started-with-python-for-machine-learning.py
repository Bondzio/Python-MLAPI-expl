#!/usr/bin/env python
# coding: utf-8

# 
# 
# **Hi ! Welcome to my Kernel**
# 
# > **** This the first part of a series of kernels that wil familiarize you with the naunces of Machine Learning using Python
# 
# * I created this kernel so that beginners can use this to learn the syntax and data types in Python.
# 
# * Others may just use this code as a refresher !!
# 
# **We will look at the following topics in this kernel**
# 
# 1. Basic Operations in Python
# 2. Creating variables in Python and working with them
# 3. Python Lists, Functions and Packages
# 4. Introduction to Numpy
# 

# In[ ]:


# Basic Mathematic operations in Python



# Addition
print(7+10)

# Addition, subtraction
print(5 + 5)
print(5 - 5)

#Division
print(5 / 8)

# Multiplication, division, modulo, and exponentiation
print(3 * 5)
print(10 / 2)
print(18 % 7)
print(4 ** 2)

# How much is your $100 worth after 7 years?
a = (100*(1.1**7))
print(a)


# In[ ]:


# Create a variable savings

savings = 100

# Print out savings
print(savings)


# In[ ]:


# Create a variable savings
savings = 100

# Create a variable growth_multiplier

growth_multiplier = 1.1


# Calculate result


result = savings * growth_multiplier ** 7


# Print out result

print(result)


# In[ ]:


# Create a variable desc

desc = "compound interest"

# Create a variable profitable

profitable = True


# In[ ]:


savings = 100
growth_multiplier = 1.1
desc = "compound interest"

# Assign product of growth_multiplier and savings to year1

year1 = savings * growth_multiplier

# Print the type of year1

print(type(year1))

# Assign sum of desc and desc to 

doubledesc = desc + desc

# Print out doubledesc

print(doubledesc)


# In[ ]:


# Definition of savings and result
savings = 100
result = 100 * 1.10 ** 7

st_savings = str(savings)
st_result = str(result)

# Fix the printout
print("I started with $" + str(savings) + " and now have $" + str(result) + ". Awesome!")

# Definition of pi_string
pi_string = "3.1415926"

# Convert pi_string into float: pi_float

pi_float = float(pi_string)

print(pi_float)


# In[ ]:


# area variables (in square meters)
hall = 11.25
kit = 18.0
liv = 20.0
bed = 10.75
bath = 9.50

# Create list areas

areas = [hall,kit,liv,bed,bath]

# Print areas

print(areas)


# In[ ]:


# area variables (in square meters)
hall = 11.25
kit = 18.0
liv = 20.0
bed = 10.75
bath = 9.50

# Adapt list areas
areas = ["hallway",hall, "kitchen", kit, "living room", liv,"bedroom", bed, "bathroom", bath]

# Print areas

print(areas)


# In[ ]:


# area variables (in square meters)
hall = 11.25
kit = 18.0
liv = 20.0
bed = 10.75
bath = 9.50

# house information as list of lists
house = [["hallway", hall],
         ["kitchen", kit],
         ["living room", liv],
         ["bedroom", bed],
         ["bathroom", bath]]

# Print out house

print(house)

# Print out the type of house

print(type(house))


# In[ ]:


# Create the areas list
areas = ["hallway", 11.25, "kitchen", 18.0, "living room", 20.0, "bedroom", 10.75, "bathroom", 9.50]

# Print out second element from areas
print(areas[1])

# Print out last element from areas
print(areas[9])

# Print out the area of the living room
print(areas[5])


# In[ ]:


# Create the areas list
areas = ["hallway", 11.25, "kitchen", 18.0, "living room", 20.0, "bedroom", 10.75, "bathroom", 9.50]

# Sum of kitchen and bedroom area: eat_sleep_area

eat_sleep_area = areas[3]+areas[7]

# Print the variable eat_sleep_area

print(eat_sleep_area)


# In[ ]:


# Create the areas list
areas = ["hallway", 11.25, "kitchen", 18.0, "living room", 20.0, "bedroom", 10.75, "bathroom", 9.50]
# Use slicing to create downstairs

downstairs = areas[0:6]

# Use slicing to create upstairs

upstairs = areas[6:]

# Print out downstairs and upstairs

print(downstairs)

print(upstairs)


# In[ ]:


# Create the areas list
areas = ["hallway", 11.25, "kitchen", 18.0, "living room", 20.0, "bedroom", 10.75, "bathroom", 9.50]

# Alternative slicing to create downstairs

downstairs = areas[:6]

print(downstairs)

# Alternative slicing to create upstairs

upstairs = areas[6:]

print(upstairs)


# In[ ]:


# Create the areas list
areas = ["hallway", 11.25, "kitchen", 18.0, "living room", 20.0, "bedroom", 10.75, "bathroom", 9.50]

# Correct the bathroom area

areas[-1] = 10.50

# Change "living room" to "chill zone"

areas[4] = "chill zone"


# In[ ]:


# Create the areas list and make some changes
areas = ["hallway", 11.25, "kitchen", 18.0, "chill zone", 20.0,
         "bedroom", 10.75, "bathroom", 10.50]

# Add poolhouse data to areas, new list is areas_1
areas_1 = areas + ["poolhouse", 24.5]

# Add garage data to areas_1, new list is areas_2

areas_2 = areas_1 + ["garage", 15.45]


# In[ ]:


# Create list areas
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Create areas_copy
areas_copy = areas[:]

# Change areas_copy
areas_copy[0] = 5.0

# Print areas
print(areas)


# In[ ]:


# Create variables var1 and var2
var1 = [1, 2, 3, 4]
var2 = True

# Print out type of var1

print(type(var1))

# Print out length of var1

print(len(var1))

# Convert var2 to an integer: out2

out2 = int(var2)


# In[ ]:


# Create lists first and second
first = [11.25, 18.0, 20.0]
second = [10.75, 9.50]

# Paste together first and second: full

full = first + second

# Sort full in descending order: full_sorted

full_sorted = sorted(full,reverse=True)

# Print out full_sorted

print(full_sorted)


# In[ ]:


# string to experiment with: place
place = "poolhouse"

# Use upper() on place: place_up

place_up = place.upper()
# Print out place and place_up

print(place)
print(place_up)
# Print out the number of o's in place
print(place.count("o"))


# In[ ]:


# Create list areas
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Print out the index of the element 20.0

print(areas.index(20.0))

# Print out how often 9.50 appears in areas

print(areas.count(9.50))


# In[ ]:


# Create list areas
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Use append twice to add poolhouse and garage size

areas.append(24.5)
areas.append(15.45)



# Print out areas

print(areas)

# Reverse the orders of the elements in areas

areas.reverse()

# Print out areas
print(areas)


# In[ ]:


# Definition of radius
r = 0.43

# Import the math package
import math

# Calculate C
C = 2*(math.pi)*r

# Calculate A
A = math.pi*(r*r)

# Build printout
print("Circumference: " + str(C))
print("Area: " + str(A))


# In[ ]:


# Definition of radius
r = 192500

# Import radians function of math package

from math import radians

# Travel distance of Moon over 12 degrees. Store in dist.

phi = radians(12)

# Print out dist

dist = r*phi

print(dist)


# In[ ]:


# Create list baseball
baseball = [180, 215, 210, 210, 188, 176, 209, 200]

# Import the numpy package as np

import numpy as np

# Create a numpy array from baseball: np_baseball

np_baseball = np.array(baseball)

# Print out type of np_baseball

print(type(np_baseball))


# In[ ]:


# height is available as a regular list

# Import numpy

import numpy as np

height_in = [70.47, 80.13, 75.91, 89.12, 78.43, 75.32]

# Create a numpy array from height_in: np_height_in

np_height_in = np.array(height_in)

# Print out np_height_in

print(np_height_in)

# Convert np_height_in to m: np_height_m

np_height_m = np_height_in*0.0254

# Print np_height_m

print(np_height_m)


# In[ ]:


# height and weight are available as regular lists

# Import numpy
import numpy as np

# Create array from height_in with metric units: np_height_m
np_height_m = np.array(height_in) * 0.0254

# Create array from weight_lb with metric units: np_weight_kg

weight_lb = [170.47, 180.13, 175.91, 189.12, 178.43, 175.32]

np_weight_kg = np.array(weight_lb)*0.453592

# Calculate the BMI: bmi

bmi = np_weight_kg / np_height_m **2

print(bmi)


# Print out bmi


# In[ ]:


# height and weight are available as a regular lists

# Import numpy
import numpy as np

# Calculate the BMI: bmi
np_height_m = np.array(height_in) * 0.0254
np_weight_kg = np.array(weight_lb) * 0.453592
bmi = np_weight_kg / np_height_m ** 2

# Create the light array

light = bmi<21

# Print out light

print(light)

# Print out BMIs of all baseball players whose BMI is below 21

print(bmi[light==True])


# In[ ]:


# height and weight are available as a regular lists

# Import numpy
import numpy as np

# Store weight and height lists as numpy arrays
np_weight_lb = np.array(weight_lb)
np_height_in = np.array(height_in)

# Print out the weight at index 5

print(weight_lb[5])

# Print out sub-array of np_height_in: index 2 up to and including index 5

print(np_height_in[2:6])


# In[ ]:


# Create baseball, a list of lists
baseball = [[180, 78.4, 1],
            [215, 102.7, 1],
            [210, 98.5, 1],
            [188, 75.2, 1]]

# Import numpy
import numpy as np

# Create a 2D numpy array from baseball: np_baseball
np_baseball = np.array(baseball)

# Print out the type of np_baseball
print(type(np_baseball))


# Print out the shape of np_baseball
print(np_baseball.shape)


# In[ ]:


# baseball is available as a regular list of lists

# Import numpy package
import numpy as np

# Create a 2D numpy array from baseball: np_baseball
np_baseball = np.array(baseball)

# Print out the shape of np_baseball
print(np_baseball.shape)


# In[ ]:


# baseball is available as a regular list of lists

# Import numpy package
import numpy as np

# Create np_baseball (2 cols)
np_baseball = np.array(baseball)

# Print out the 4th row of np_baseball
print(np_baseball[3,:])

# Select the entire second column of np_baseball: np_weight_lb

np_weight_lb = np_baseball[:,1]

# Print out height of 3rd player

print(np_baseball[3,0])


# In[ ]:


# baseball is available as a regular list of lists
# updated is available as 2D numpy array

# Import numpy package
import numpy as np

# Create np_baseball (3 cols)
np_baseball = np.array(baseball)

# Print out addition of np_baseball and updated
#print(np_baseball+updated)

# Create numpy array: conversion

conversion = np.array([0.0254,0.453592,1])


# Print out product of np_baseball and conversion

print(np_baseball*conversion)


# In[ ]:


# np_baseball is available

# Import numpy
import numpy as np

# Print mean height (first column)
avg = np.mean(np_baseball[:,0])
print("Average: " + str(avg))

# Print median height. Replace 'None'
med = np.median(np_baseball[:,0])
print("Median: " + str(med))

# Print out the standard deviation on height. Replace 'None'
stddev = np.std(np_baseball[:,0])
print("Standard Deviation: " + str(stddev))

# Print out correlation between first and second column. Replace 'None'
corr = np.corrcoef(np_baseball[:,0],np_baseball[:,1])
print("Correlation: " + str(corr))


# In[ ]:


# heights and positions are available as lists

# Import numpy
import numpy as np

np_positions = np.array(["GK", "F", "D", "GK", "F", "D"])
np_heights = np_height_in

# Heights of the goalkeepers: gk_heights
gk_heights = np_heights[np_positions == 'GK']

# Heights of the other players: other_heights

other_heights = np_heights[np_positions != 'GK']

# Print out the median height of goalkeepers. Replace 'None'
print("Median height of goalkeepers: " + str(np.median(gk_heights)))

# Print out the median height of other players. Replace 'None'
print("Median height of other players: " + str(np.median(other_heights)))

