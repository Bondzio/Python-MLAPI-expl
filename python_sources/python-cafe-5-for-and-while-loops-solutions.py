#!/usr/bin/env python
# coding: utf-8

#  # Cafe 5 - For Loops and While Loops 

# Loops are a way to repeatedly execute some code! Today we will look at two types of loops:
# 
# 1. for loop
# 2. while loop
# 
# 
# 
# The for loop specifies
# 
# the variable name to use (in this case, planet)
# the set of values to loop over (in this case, planets)
# You use the word "in" to link them together.
# 
# The object to the right of the "in" can be any object that supports iteration. Basically, if it can be thought of as a group of things, you can probably loop over it. In addition to lists, we can iterate over the elements of a tuple

# # 1. For Loop
# 
# ### loops over a range of something - numbers, string, list, etc. 
# 
# - You know exactly the number of steps
# - You won't fall into an infinite
# - The index variable is automatically incremented
# 
# The for loop specifies
# 
# - the variable name to use
# - the set of values to loop over 
# - You use the word "in" to link them together.
# 
# The object to the right of the "in" can be any object that supports iteration. Basically, if it can be thought of as a group of things, you can probably loop over it. In addition to lists, we can iterate over the elements of a tuple
# 
# Let's try some examples! 

# In[ ]:


#Your Code Goes Here
#Looping through characters of a string

s2 = 'Toronto'

for x in s2:
    print(x)
    


# In[ ]:


#Your Code Goes Here
#Looping through a range of numbers using the range() function
#The range function - specify the number of times you loop through
#It returns a sequence of numbers, starting from 0, by default, and increments
# by 1, default, and ends at a specified number

for x in range(0, 7):
    print(x)


# In[ ]:


#Your Code Goes Here
for x in range(3, 100, 5):
    print(x)


# # 2. While Loop
# 
# ### loops until a specific condition is satisified
# 
# - You don't know the number of steps
# - You can fall into an infinite loop.
# - You must explicitely increment the index variable
# 
# Let's try some examples!
# 

# In[ ]:


### Your Code Goes Here
### With the while loop, we can execute a set of statements as long as a condition is true

i = 1
while (i < 6):
    print(i)
    i +=1
    #i = i+1


# # 3. Using break and continue in loops
# 
# You can also exit and skip parts of a loop using the `break` and `continue` command. This can be used on for loops and while loops 
# 

# In[ ]:


#Your Code Goes Here

i = 0
while(i < 6):
    print(i)
    if (i == 4):
        break
    else:
        i+=1


# In[ ]:


i = 0
while (i < 6):
    i+= 1
    if(i == 3):
        continue
    print(i)


# In[ ]:


x = 'Toronto'
for x in s2:
    print(x)
    if (x == 'o'):
        break


# # Putting it all Together
# 
# Create a program that translates the for loop code to do the same thing but using a while loop.
# 
# 

# In[ ]:


#Your Code Goes here
# Translate this code to do the same thing but in a while loop
# Hint run this code first to understand what it is doing for each iteration

for i in range(0, 6):
    
    if (i == 3 or i == 6):
        continue
    else:
        print(i)
        
##Answer
i = -1
while(i < 6):
    i +=1
    if (i == 3 or i == 6):
        continue
    else:
        print(i)

