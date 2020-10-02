#!/usr/bin/env python
# coding: utf-8

# # Parsing XML
# 
# Date: 28/03/2018
# 
# Version: 1.0
# 
# Environment: Python 3.6.2 and Jupyter notebook
# 
# Libraries used:
# * re (for regular expression) 
# * json (for creating json file) 

# ## 1.  Import libraries 

# In[ ]:


# Code to import libraries
import re
import json


# ## 2. Parse xml File

# In[ ]:


# Read the file
file = open("../input/australian-sport-thesaurus-student.xml", encoding = 'utf-8')


# In[ ]:


# Explore the file content
for text in file:
    print(text)


# ## 3. The Structure of the xml file is:
# ``` 
#   <Term>
#     
#      -Title
#         
#      -Description
#        
#      -Related Terms
#         
#            <Term>
#           
#               -Title
#               
#               -Relationship    
# ```              

# #### To match each key word is the xml file, we need the following regular expressions:
# 
# ```
# * match the <Term> and </Term> tags:  
#     roTotTermMatch = re.compile(r"^\s*<Terms>$")
#     endOfTermMatch = re.compile(r"^\s*</Term>\s*")
#    
# * match the <Title> and </Title> tags:  
#     titleMatch = re.compile(r"^\s*<Title>.*")
#  
# * match the <Description> tags:  
#     descriptionMatch =re.compile(r"\s*<Description>.*")
#     
# * match the <RelatedTerms> and </RelatedTerms> tags
#    relatedTermsMatch = re.compile(r"\s*<RelatedTerms>.*")
#    endOfRelatedTermMatch = re.compile(r"^\s*</RelatedTerms>\s*")
# 
# * match the <Relationship>tags:
#     relationshipMatch = re.compile(r"\s*<Relationship>.*")
# ```
# 

# #### Setup a switch to verify if the 'Term' is a root term of a child term
#     isRootTerm = False
#     
# #### Create lists and dictionaries to store the data
#     terms = []        - Contains everything
#     rootTerm = {}     - Contains the Root Terms and their children (in a list format) as keys and values
#     relatedTerm = []  - Contain all teh Related Terms (in a dictionary format) as elements
#     childTerm = {}    - Contains tile and relationship as keys and values of each child term

# In[ ]:


file = open("australian-sport-thesaurus-student.xml", encoding = 'utf-8')

terms = []
rootTerm = {}
relatedTerm = []
childTerm = {}
isRootTerm = False

rootTermMatch = re.compile(r"^\s*<Terms>$")
endOfTermMatch = re.compile(r"^\s*</Term>\s*")
titleMatch = re.compile(r"^\s*<Title>.*")
descriptionMatch =re.compile(r"\s*<Description>.*")
relatedTermsMatch = re.compile(r"\s*<RelatedTerms>.*")
endOfRelatedTermMatch = re.compile(r"^\s*</RelatedTerms>\s*")
relationshipMatch = re.compile(r"\s*<Relationship>.*")



for line in file:
    if rootTermMatch.match(line) != None:       # Hits the rootTerm tag: <Term>
        isRootTerm = True

    if isRootTerm and titleMatch.match(line) != None:
        rootTerm['Title'] = re.sub(r'(<Title>)|(</Title>)', '', line).strip()    # Remove the tags and white spaces
        
    if descriptionMatch.match(line) != None:
        rootTerm['Description'] = re.sub(r'(<Description>)|(</Description>)', '', line).strip()
        
    if relatedTermsMatch.match(line) !=None:     # Hits the childTerm tag after <RelatedTerms> tag
        isRootTerm = False
        rootTerm['RelatedTerms'] = []
    
    if not isRootTerm and titleMatch.match(line):
        childTerm['Title'] = re.sub(r'(<Title>)|(</Title>)', '', line).strip()
    
    if not isRootTerm and relationshipMatch.match(line):
        childTerm['Relationship'] = re.sub(r'(<Relationship>)|(</Relationship>)', '', line).strip()        
    
    if not isRootTerm and endOfTermMatch.match(line):
        childTerm = dict(sorted(childTerm.items(), key=lambda d:d[0]))  # Sort the dictionay by key
        rootTerm['RelatedTerms'].append(childTerm)                      # Add RelatedTerms list to the RootTerm dictionary
        childTerm = {}
        
        
    if endOfRelatedTermMatch.match(line):
        isRootTerm = True
    
    if isRootTerm and endOfTermMatch.match(line):
        rootTerm = dict(sorted(rootTerm.items(), key=lambda d:d[0]))  # Sort the dictionay by key 
        terms.append(rootTerm)                                        # Add RelatedTerms list to the Main dictionary
        rootTerm = {}
        


# In[ ]:


# Put everything into the output dcitionay and dump to a json file
dct = {"thesaurus" : terms}

with open('sport.dat', 'w') as fp:
    json.dump(dct, fp)


# ## 3. Summary
# Findings: 
# * Some RelatedTerm have no Title
# * Some RelatedTerms have more than 1 Terms
# * There are 7863 Terms in the terms list, each term is a dictionary
# * The example output json file shows a sorted keys in dictionary

# In[ ]:


# Total Terms:
len(terms)

