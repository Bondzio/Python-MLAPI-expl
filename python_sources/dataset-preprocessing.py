#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import string
import json
import shutil

from pathlib import Path
import os
from os import listdir, mkdir
from os.path import isfile, isdir, join, exists, abspath
from keras.preprocessing import image
from keras.applications.resnet import ResNet152, preprocess_input
from sklearn.model_selection import train_test_split


# In[ ]:


# ! pip install git+https://github.com/crazyfrogspb/RedditScore.git > /dev/null


# ## Loading&Preprocessing Dataset

# In[ ]:


def _globalMaxPool1D(tensor):
    _,_,_,size = tensor.shape
    return [tensor[:,:,:,i].max() for i in range(size)]

def _getImageFeatures(model, img_path):
    img = image.load_img(img_path, target_size=None)

    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)

    feature_tensor = model.predict(img_data)
    get_img_id = lambda p: p.split('/')[-1].split('.')[0]
    return {
        "id": get_img_id(img_path),
        "features": _globalMaxPool1D(feature_tensor),
    }

def _getJSON(path):
    with open(path) as json_file:
        return json.loads(json.load(json_file))
    
def _clean_text(text):
    text = text.replace("\n", " ")
    # onyshchak: only checking first 1000 characters, will need to extract summary propely
    text = text[:1000].rsplit(' ', 1)[0]
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def _getTextFeatures(text_path):
    data = _getJSON(text_path)
    
    return {
        'id': data['id'],
        'text': _clean_text(data['text']),
        'title': data['title']
    }

def _getImagesMeta(path):
    data = _getJSON(path)['img_meta']
    for x in data:
        x['description'] = _clean_text(x['description'])
        x['title'] = _clean_text(x['title'])
    return data

def _getValidImagePaths(article_path):
    img_path = join(article_path, 'img/')
    return [join(img_path, f) for f in listdir(img_path) if isfile(join(img_path, f)) and f[-4:].lower() == ".jpg"]

def _dump(path, data):
    with open(path, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)

def GetArticleData(article_path):
    article_data = _getTextFeatures(join(article_path, 'text.json'))
    article_data["img"] = _getImagesMeta(join(article_path, 'img/', 'meta.json'))
    
    return article_data

def ReadArticles(data_path, pred=None, offset=0, limit=None):
    article_paths = [join(data_path, f) for f in listdir(data_path) if isdir(join(data_path, f))]
    limit = limit if limit else len(article_paths) - offset
    limit = min(limit, len(article_paths) - offset)
    
    articles = []
    for i in range(offset, offset + limit):
        path = article_paths[i]
        if (i - offset) % 300 == 0: print(i - offset, "articles have been read")
        article_data = GetArticleData(path)
        if pred and not pred(i, article_data): continue
        
        articles.append(article_data)
        if len(articles) >= limit: break  # useless?
        
    print(offset + limit, "articles have been read")
    return articles

def GenerateVisualFeatures(data_path, offset=0, limit=None, model=None):
    article_paths = [join(data_path, f) for f in listdir(data_path) if isdir(join(data_path, f))]
    limit = limit if limit else len(article_paths) - offset
    limit = min(limit, len(article_paths) - offset)
    model = model if model else ResNet152(weights='imagenet', include_top=False) 
    
    for i in range(offset, offset + limit):
        path = article_paths[i]
        print(i, path)
    
        meta_path = join(path, 'img/', 'meta.json')
        meta_arr = _getImagesMeta(meta_path)
        for meta in meta_arr:
            if 'features' in meta: continue
            if meta['filename'][-4:].lower() != ".jpg": continue
                
            img_path =  join(path, 'img/', meta['filename'])
            try:
                features = _getImageFeatures(model, img_path)['features']
                meta['features'] = [str(f) for f in features]
            except Exception as e:
                print("exception", str(e))
                print(img_path)
                continue
                
        _dump(meta_path, json.dumps({"img_meta": meta_arr}))


# In[ ]:


get_ipython().run_cell_magic('time', '', 'dataset_root = \'/kaggle/input/extended-wikipedia-multimodal-dataset/\'\narticles = ReadArticles(dataset_root + \'data_full/data/\', offset=0, limit=None)\nprocessed_titles = _getJSON(dataset_root + "parsed_titles.json")')


# ## Mapping Preprocessed Dataset into W2VV format

# In[ ]:


dataset_name = 'data_w2vv'
dataset_path = join('./', dataset_name)
if exists(dataset_path):
    shutil.rmtree(dataset_path)
    
mkdir(dataset_path)
subsets = {
    "train": {},
    "val": {},
    "test": {},
}

for k, v in subsets.items():
    v['name'] = dataset_name + k
    v['path'] = join(dataset_path, v['name'])
    mkdir(v['path'])
    
    v['feature_data_path'] = join(v['path'], 'FeatureData')
    if k == 'train':
        mkdir(v['feature_data_path'])
    else:
        dst = v['feature_data_path']
        os.symlink(os.path.relpath(subsets['train']['feature_data_path'], Path(dst).parent), dst)

    v["image_sets_path"] = join(v['path'], 'ImageSets')
    mkdir(v["image_sets_path"])

    v["text_data_path"] = join(v['path'], 'TextData')
    mkdir(v["text_data_path"])


# In[ ]:


def to_file(arr, filepath):
    with open(filepath, 'w') as f:
        for x in arr:
            f.write("%s\n" % x)


# In[ ]:


is_valid_img = lambda i: 'features' in i
has_valid_img = lambda a: len([i for i in a['img'] if is_valid_img(i)]) > 0
articles = [a for a in articles if has_valid_img(a)]
len(articles)


# In[ ]:


list2str = lambda l: " ".join([str(x) for x in l])
get_img_id = lambda i: os.path.splitext(i['filename'])[0]  # removing file extention

img_features = set(['{} {}'.format(get_img_id(i), list2str(i['features'])) for a in articles for i in a['img'] if is_valid_img(i)])
print("len(img_features) = ", len(img_features))

raw_features_file_path = join(subsets['train']["feature_data_path"], subsets['train']['name'] + ".features.txt")
to_file(img_features, raw_features_file_path)


# In[ ]:


def map_data(articles):
    seen = set()
    res = []
    for a in articles:
        for i in a['img']:
            if 'features' not in i: continue
                
            img_id = os.path.splitext(i['filename'])[0]  # removing file extention
            if img_id in seen:
                # onyshchak: if image used in 2 articles, we only take the first one for simplicity
                # TODO: use all the infomation without breaking the model
                continue
                
            seen.add(img_id)
            res.append({
                "filename": img_id,
                'article_id': a['id'],
                'article_title': a['title'],
                "title": os.path.splitext(i['title'])[0],
                "description": i['description'],
                "text": a['text'],
                "features": i['features'],
            })
            
    return res


# In[ ]:


ARTICLE_LEVEL_SPLIT = True
seed = 1234

if ARTICLE_LEVEL_SPLIT:
    train, test = train_test_split(articles, test_size=0.04, random_state=seed)
    train, val = train_test_split(train, test_size=0.043, random_state=seed)

    subsets['train']['data'] = map_data(train)
    subsets['val']['data'] = map_data(val)
    subsets['test']['data'] = map_data(test)
else:
    mapped_images = map_data(articles)
    # 2325 test, 2057 val
    train, test = train_test_split(mapped_images, test_size=1000, random_state=seed)
    train, val = train_test_split(train, test_size=1000, random_state=seed)
    
    subsets['train']['data'] = train
    subsets['val']['data'] = val
    subsets['test']['data'] = test

subset_split_info = str([(k, len(v['data'])) for k, v in subsets.items()]).replace("(", "").replace(")", "")
subset_split_info


# In[ ]:


ids = [x['article_id'] for x in subsets['test']['data']]
to_file(ids, join(subsets['test']['path'], "test_articles_ids.txt"))


# In[ ]:


for v in subsets.values():
    ids = [x['filename'] for x in v['data']]
    to_file(ids, join(v["image_sets_path"], v['name'] + ".txt"))


# In[ ]:


# from redditscore.tokenizer import CrazyTokenizer

# tokenizer = CrazyTokenizer(hashtags='split')

# def split_hashtag_words(text):
#     global tokenizer
#     return " ".join(tokenizer.tokenize("#" + text))

# def remove_auxiliary_words(text):
#     aux = ["jpeg", "jpg", "png"] # only 1 valid word can contain png, other - image extention trash
#     for a in aux:
#         if a == text[-len(a):]:
#             text = text[:-len(a)]
#             break
                    
#     return text

# process_title = lambda x: split_hashtag_words(remove_auxiliary_words(x))


# In[ ]:


get_ipython().run_cell_magic('time', '', '# onyshchak: originally ID also contained file extention e.g. *.jpg. but not in image_sets_path\ndef get_description(z):\n    if z[\'description\']: return z[\'description\']\n    elif z[\'filename\'] in processed_titles: return processed_titles[z[\'filename\']]\n    else: \n        print("Missing title", z[\'filename\'])\n        return z[\'title\']\n\nfor v in subsets.values():\n    text_data = sorted(\n        [\'{}#enc#0 {}\'.format(x[\'filename\'], x[\'text\']) for x in v[\'data\']] +\n        [\'{}#enc#1 {}\'.format(x[\'filename\'], get_description(x)) for x in v[\'data\']]\n    )\n\n    to_file(text_data, join(v["text_data_path"], v[\'name\'] + ".caption.txt"))')


# In[ ]:


del articles
del text_data
del train
del val
del ids
del test
del img_features
for k,v in subsets.items():
    del v['data']


# In[ ]:


get_ipython().system(' apt install --assume-yes python-pip > /dev/null')
get_ipython().system(' python2 -m pip install --user numpy scipy matplotlib ipython jupyter pandas nose > /dev/null')


# In[ ]:


IS_FILE_LIST = 0
FEATURE_DIMENTION = 2048
feature_data_path = subsets['train']["feature_data_path"]
bin_features_path = join(feature_data_path, "pyresnet152-pool5os/")

get_ipython().system(' python2 /kaggle/input/w2vv-scripts/simpleknn/txt2bin.py $FEATURE_DIMENTION $raw_features_file_path $IS_FILE_LIST $bin_features_path --overwrite 1')


# In[ ]:


get_ipython().system(' mv $dataset_name/* ./')
get_ipython().system(' rmdir $dataset_name')


# In[ ]:


version_notes = "version_notes.txt"
get_ipython().system(' echo article level = $ARTICLE_LEVEL_SPLIT > $version_notes')
get_ipython().system(' echo seed = $seed >> $version_notes')
get_ipython().system(' echo "caption 0 = article summary" >> $version_notes')
get_ipython().system(' echo "caption 1 = description(or parsed titles)" >> $version_notes')
get_ipython().system(' echo split = $subset_split_info >> $version_notes')

get_ipython().system(' cat $version_notes')

