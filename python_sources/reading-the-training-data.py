#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import os

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
# path to input files


# In[ ]:


train = []
with open('/kaggle/input/tensorflow2-question-answering/simplified-nq-train.jsonl', 'r') as file:
    for i in range(100):
        # read a sample of 100 json lines
        train.append(json.loads(file.readline()))


# In[ ]:


sample = train[0]
sample.keys()


# In[ ]:


test = []
with open('/kaggle/input/tensorflow2-question-answering/simplified-nq-test.jsonl', 'r') as file:
    for i in range(100):
        test.append(json.loads(file.readline()))

test[0].keys()

# test set does not have annotations, but it has the long_answer_candidates


# In[ ]:


sample['annotations']


# In[ ]:


for s in train:
    if len(s['annotations']) > 1:
        print('Found more than 1')

# didn't find any examples where there are more than 1 long_answer annotated


# In[ ]:


for s in train:
    if len(s['annotations'][0]['short_answers']) > 1:
        print('Found more than 1')
        
# on the other hand, found a few examples where there are more than 1 short_answers annotated


# In[ ]:


sample['question_text']


# In[ ]:


def get_long_answer(json_dict):
    document_text = json_dict['document_text']
    tokens = document_text.split(' ')
    # even though annotatations is an array, it seems to be all length of 1
    long_answer_key = json_dict['annotations'][0]['long_answer']
    long_answer = tokens[long_answer_key['start_token']:long_answer_key['end_token']]
    return " ".join(long_answer)

get_long_answer(sample)


# In[ ]:


def get_short_answers(json_dict):
    document_text = json_dict['document_text']
    tokens = document_text.split(' ')
    short_answer_keys = [short for short in json_dict['annotations'][0]['short_answers']]
    short_answers = [" ".join(tokens[key['start_token']:key['end_token']]) for key in short_answer_keys]
    return short_answers

get_short_answers(sample)


# In[ ]:


def print_long_short(train, i):
    s = train[i]
    print('question:')
    print(s['question_text'])
    print('')
    
    print('long answer:')
    print(get_long_answer(s))
    print('')
    
    print('short answer:')
    print("\n".join(get_short_answers(s)))


# In[ ]:


print_long_short(train, 0)


# In[ ]:


print_long_short(train, 1)


# In[ ]:


print_long_short(train, 2)


# In[ ]:


print_long_short(train, 90)


# In[ ]:


print_long_short(train, 91)


# In[ ]:


print_long_short(train, 92)


# In[ ]:




