#!/usr/bin/env python
# coding: utf-8

# # Python for Data 5: Lists
# [back to index](https://www.kaggle.com/hamelg/python-for-data-analysis-index)

# Most of the individual data values you work with will take the form of one of the basic data types we learned about in lesson 3, but data analysis involves working with sets of related records that need to be grouped together. Sequences in Python are data structures that hold objects in an ordered array. In this lesson, we'll learn about lists, one of the most common sequence data types in Python.

# # List Basics

# A list is a mutable, ordered collection of objects. "Mutable" means a list can be altered after it is created. You can, for example, add new items to a list or remove existing items. Lists are heterogeneous, meaning they can hold objects of different types.
# 
# Construct a list with a comma separated sequence of objects within square brackets:

# In[ ]:


my_list = ["Lesson", 5, "Is Fun?", True]

print(my_list)


# Alternatively, you can construct a list by passing some other iterable into the list() function. An iterable describes an object you can look through one item at a time, such as lists, tuples, strings and other sequences.

# In[ ]:


second_list = list("Life is Study")  # Create a list from a string

print(second_list)


# A list with no contents is known as the empty list:

# In[ ]:


empty_list = []

print( empty_list )


# You can add an item to an existing list with the list.append() function:

# In[ ]:


empty_list.append("I'm no longer empty!")

print(empty_list)


# Remove a matching item from a list with list.remove():

# In[ ]:


my_list.remove(5)

print(my_list)


# *Note: Remove deletes the first matching item only.*

# Join two lists together with the + operator:

# In[ ]:


combined_list = my_list + empty_list

print(combined_list)


# You can also add a sequence to the end of an existing list with the list.extend() function:

# In[ ]:


combined_list = my_list

combined_list.extend(empty_list)

print(combined_list)


# Check the length, maximum, minimum and sum of a list with the len(), max(), min() and sum() functions, respectively.

# In[ ]:


num_list = [1, 3, 5, 7, 9]
print( len(num_list))                # Check the length
print( max(num_list))                # Check the max
print( min(num_list))                # Check the min
print( sum(num_list))                # Check the sum
print( sum(num_list)/len(num_list))  # Check the mean*


# *Note: Python does not have a built in function to calculate the mean, but the numpy library we will introduce in upcoming lessons does.*
# 
# You can check whether a list contains a certain object with the "in" keyword:

# In[ ]:


1 in num_list


# Add the keyword "not" to test whether a list does not contain an object:

# In[ ]:


1 not in num_list


# Count the occurrences of an object within a list using the list.count() function:

# In[ ]:


num_list.count(3)


# Other common list functions include list.sort() and list.reverse():

# In[ ]:


new_list = [1, 5, 4, 2, 3, 6]      # Make a new list

new_list.reverse()                 # Reverse the list
print("Reversed list", new_list)

new_list.sort()                    # Sort the list
print("Sorted list", new_list)


# # List Indexing and Slicing

# Lists and other Python sequences are indexed, meaning each position in the sequence has a corresponding number called the index that you can use to look up the value at that position. Python sequences are zero-indexed, so the first element of a sequence is at index position zero, the second element is at index 1 and so on. Retrieve an item from a list by placing the index in square brackets after the name of the list:

# In[ ]:


another_list = ["Hello","my", "bestest", "old", "friend."]

print (another_list[0])
print (another_list[2])


# If you supply a negative number when indexing into a list, it accesses items starting from the end of the list (-1) going backward:

# In[ ]:


print (another_list[-1])
print (another_list[-3])


# Supplying an index outside of a lists range will result in an IndexError:

# In[ ]:


print (another_list[5])


# If your list contains other indexed objects, you can supply additional indexes to get items contained within the nested objects:

# In[ ]:


nested_list = [[1,2,3],[4,5,6],[7,8,9]]

print (nested_list[0][2])


# You can take a slice (sequential subset) of a list using the syntax [start:stop:step] where start and stop are the starting and ending indexes for the slice and step controls how frequently you sample values along the slice. The default step size is 1, meaning you take all values in the range provided, starting from the first, up to but not including the last:

# In[ ]:


my_slice =  another_list[1:3]   # Slice index 1 and 2
print(my_slice )


# In[ ]:


# Slice the entire list but use step size 2 to get every other item:

my_slice =  another_list[0:6:2] 
print(my_slice )


# You can leave the starting or ending index blank to slice from the beginning or up to the end of the list respectively:

# In[ ]:


slice1 = another_list[:4]   # Slice everything up to index 4
print(slice1)


# In[ ]:



slice2 = another_list[3:]   # Slice everything from index 3 to the end
print(slice2)


# If you provide a negative number as the step, the slice steps backward:

# In[ ]:


# Take a slice starting at index 4, backward to index 2

my_slice =  another_list[4:2:-1] 
print(my_slice )


# If you don't provide a start or ending index, you slice of the entire list:

# In[ ]:


my_slice =  another_list[:]   # This slice operation copies the list
print(my_slice)


# Using a step of -1 without a starting or ending index slices the entire list in reverse, providing a shorthand to reverse a list:

# In[ ]:


my_slice =  another_list[::-1] # This slice operation reverses the list
print(my_slice)


# You can use indexing to change the values within a list or delete items in a list:

# In[ ]:


another_list[3] = "new"   # Set the value at index 3 to "new"

print(another_list)

del(another_list[3])      # Delete the item at index 3

print(another_list)


# You can also remove items from a list using the list.pop() function. pop() removes the final item in a list and returns it:

# In[ ]:


next_item = another_list.pop()

print(next_item)
print(another_list)


# Notice that the list resizes itself dynamically as you delete or add items to it. Appending items to lists and removing items from the end of list with list.pop() are very fast operations. Deleting items at the front of a list or within the body of a lists is much slower.

# # Copying Lists

# In the code above, we saw that we can slice an entire list using the [:] indexing operation. You can also copy a list using the list.copy() function:

# In[ ]:


list1 = [1,2,3]                        # Make a list

list2 = list1.copy()                   # Copy the list

list1.append(4)                        # Add an item to list 1

print("List1:", list1)                 # Print both lists
print("List2:", list2)


# As expected, the copy was not affected by the append operation we performed on the original list. The copy function (and slicing an entire list with [:]) creates what is known as a "shallow copy." A shallow copy makes a new list where each list element refers to the object at the same position (index) in the original list. This is fine when the list is contains immutable objects like ints, floats and strings, since they cannot change. Shallow copies can however, have undesired consequences when copying lists that contain mutable container objects, such as other lists.
# 
# Consider the following copy operation:

# In[ ]:


list1 = [1,2,3]                        # Make a list

list2 = ["List within a list", list1]  # Nest it in another list

list3 = list2.copy()                   # Shallow copy list2

print("Before appending to list1:")
print("List2:", list2)
print("List3:", list3, "\n")

list1.append(4)                        # Add an item to list1
print("After appending to list1:")
print("List2:", list2)
print("List3:", list3)


# Notice that when we use a shallow copy on list2, the second element of list2 and its copy both refer to list1. Thus, when we append a new value into list1, the second element of list2 and the copy, list3, both change. When you are working with nested lists, you have to make a "deepcopy" if you want to truly copy nested objects in the original to avoid this behavior of shallow copies.
# 
# You can make a deep copy using the deepcopy() function in the copy library:

# In[ ]:


import copy                            # Load the copy module

list1 = [1,2,3]                        # Make a list

list2 = ["List within a list", list1]  # Nest it in another list

list3 = copy.deepcopy(list2)           # Deep copy list2

print("Before appending to list1:")
print("List2:", list2)
print("List3:", list3, "\n")

list1.append(4)                        # Add an item to list1
print("After appending to list1:")
print("List2:", list2)
print("List3:", list3)


# This time list3 is not changed when we append a new value into list1 because the second element in list3 is a copy of list1 rather than a reference to list1 itself.

# # Wrap Up

# Lists are one of the most ubiquitous data structures in Python, so it is important to be familiar with them, even though specialized data structures available in libraries are often better suited for data analysis tasks. Despite some quirks like the shallow vs. deep copy issue, lists are very useful as simple data containers.
# 
# In the next lesson, we'll cover two more built in sequence objects, tuples and strings.

# # Next Lesson: [Python for Data 6: Tuples and Strings](https://www.kaggle.com/hamelg/python-for-data-6-tuples-and-strings)
# [back to index](https://www.kaggle.com/hamelg/python-for-data-analysis-index)
