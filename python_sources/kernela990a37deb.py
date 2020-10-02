#!/usr/bin/env python
# coding: utf-8

# ## Table of Contents
# 1. [Importing Libraries](#importing_libs)
# 2. [Data Exploration](#data_exploration)
# 3. [Loading Data with Pandas as Dataframes](#load_as_df)

# * ## 1. Importing Libraries and Initializing Globals <a id="importing_libs_and_globals"></a>
# 

# In[ ]:


# Input data files are available in the "../input/" directory.

# Importing Useful Libs
import numpy as np
import pandas as pd
import os
import json
import glob

data_path = '../input/CORD-19-research-challenge'
json_files = glob.glob(f'{data_path}/**/**/*.json', recursive=True)
total_files = len(json_files)
print(f"There are {len(json_files)} total json files\n")
start_file = 0
end_file = start_file


# ## 2. Scanning JSON File Keys <a id="scanning_json_file_keys"></a>
# In order to debug why `pandas` was having such difficulty loading the JSON files into a `pandas.DataFrame`, I wrote this recursive `key_printer` function to find and print all the keys of a JSON file that hase been converted to a spider web of python dicts and lists. 

# In[ ]:


def key_printer(obj, name, show_items = True):
    '''Recursive Search Function for printing all keys
    Args:
        obj (dict or list): list or dict object to be searched for keys
        name (str): name of object to be searched

    Returns:
        None: Prints keys when found
    '''
    t = type(obj)
    if t == dict:
        keys = obj.keys()
        length = len(keys)
        print(f"{name} dict has {length} keys")
        print(f"{name} keys:\n{keys}\n")
        for k in keys:
            key_printer(obj[k], f"{name}['{k}']")
    elif t == list:
        length = len(obj)
        if length:
            print(f"{name} list has {length} items")
            for i in range(length):
                key_printer(obj[i], f"{name}[{i}]")
        else:
            print(f"{name} is empty\n")
    elif show_items:
        print(f"{name} is type: {t}")
        if obj:
            print(f"{name}:\n{obj}\n")
        else:
            print(f"{name} is empty\n")

for i, file in enumerate(json_files[start_file : end_file + 1]):
    with open(file) as f:
        j = json.load(f)
        key_printer(j, f"file_{i}")
        print("\n")


# ## 3. Loading Data with Pandas as Dataframes <a id="load_as_df"></a>
# So it looks like the complex nature of these JSON files does not easily fit into the table format of a `pandas.DataFrame`. The only way I could figure out how to get this to work with `pandas.read_json` is by using the `'index'` argument for the `orient` param. You'll see from that this basicly creates a single column `pandas.DataFrame`. This is liekly not what you are going to want, so you'll likely need to use the key information from the code block above to manually construct a `pandas.DataFrame` using just the keys you need. 

# In[ ]:


abc = []
for file in json_files[start_file : end_file + 1]:
    abc.append(pd.read_json(file, orient='index'))

df = pd.concat(abc, ignore_index=True)

print(f"shape: {df.shape}", end = "\n\n")
# print(df.describe()) pands.DataFrame.describe will throw a TypeError: unhashable type: 'dict' 
print(f"memory used:\n{df.memory_usage()}", end = "\n\n")
print(df.head(3))
print(df.tail(3))


# Using what we have learned about these files, lets try to build a `pandas.DataFrame` via a bit more manual process **(WARNING IT TOOK SEVERAL MINUTES TO RUN THIS BLOCK ON 100125 JSON FILES)**:

# In[ ]:


end_file = total_files

paper_ids = []
paper_titles = []
countries = []
authors = []
institutions = []
texts = []
count = -1
for file in json_files[start_file : end_file + 1]:
    count += 1
    with open(file) as f:
        j = json.load(f)
        paper_ids.append(j['paper_id'])
        _text = ""
        for d in j['body_text']:
            if d['section']:
                _text += f"[{d['section'].upper()}]: "
            else:
                _text += "[UNLABELED TEXT]: "
            _text += f"{d['text'].lower()} "
        texts.append(_text)
        paper_titles.append(j['metadata']['title'].lower())
        _authors = ""
        _countries = ""
        _institutions = ""
        for author_data in j['metadata']['authors']:
            try:
                a = f"{author_data['first'].lower()} {author_data['middle'][0].lower()+' ' if author_data['middle'] else ''}{author_data['last'].lower()}, "
            except AttributeError as e:
                print(count)
                print(author_data)
                raise e
            if not a.rstrip(", ") in _authors:
                _authors += a
            if author_data['affiliation']:
                if 'country' in author_data['affiliation']['location']:
                    c = f"{author_data['affiliation']['location']['country'].lower()}, "
                    if not c.rstrip(", ") in _countries:
                        _countries += c
                if author_data['affiliation']['laboratory'] and author_data['affiliation']['institution']:
                    i = f"{author_data['affiliation']['laboratory'].lower()} | {author_data['affiliation']['institution'].lower()}, "
                elif author_data['affiliation']['laboratory']:
                    i = f"{author_data['affiliation']['laboratory'].lower()}, "
                else:
                    i = f"{author_data['affiliation']['laboratory'].lower()}, "
                if not i.rstrip(", ") in _institutions:
                    _institutions += i
        authors.append(_authors)
        institutions.append(_institutions)
        countries.append(_countries)        


df = pd.DataFrame({
    'paper_id' : paper_ids,
    'paper_title' : paper_titles,
    'author' : authors,
    'institution' : institutions,
    'country' : countries,
    'text' : texts,
})

print(f"shape: {df.shape}", end = "\n\n")
print(f"memory used:\n{df.memory_usage()}", end = "\n\n")
print(df.describe())
print(df.head(3))
print(df.tail(3))

