#!/usr/bin/env python
# coding: utf-8

# ## Object detection with Detecto
# [Detecto](https://github.com/alankbi/detecto) is a Python library built on top of PyTorch that simplifies the process of building object detection models. Only a few lines of code is needed to train a model. Let's give it a spin on the Global Wheat Detection dataset.

# In[ ]:


import torch
import os, sys, ast
import pandas as pd
import numpy as np
import glob
import shutil
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Import annotation data
# Start by reading annotation data from the .csv file.

# In[ ]:


DATA = '/kaggle/input/global-wheat-detection/'
df=pd.read_csv(DATA+"train.csv")
df.bbox = df.bbox.apply(ast.literal_eval)
for i in range(len(df)):
    df.bbox.iloc[i][2]=df.bbox.iloc[i][0]+df.bbox.iloc[i][2] # xmax
    df.bbox.iloc[i][3]=df.bbox.iloc[i][1]+df.bbox.iloc[i][3] # ymax
df.sample(5)


# ## Copy a subset of training data
# Detecto wants training and validation data in separate folders. So below we will take a subset (to speed things up) of the training data and copy into local folders.

# In[ ]:


get_ipython().run_line_magic('mkdir', 'train')
get_ipython().run_line_magic('mkdir', 'validate')

files = glob.glob(DATA+"train/*")
train, validate, rest = np.split(files, [int(len(files)*0.2), int(len(files)*0.25)])
for i in range(len(train)):
    shutil.copy2(train[i], './train')
for i in range(len(validate)):
    shutil.copy2(validate[i], './validate')
len(train), len(validate), len(rest)


# ## Install Detecto
# Detecto is installed from a dataset, since internet is turned off. We also need the faster-rcnn pre-trained model, again fetched from a dataset.

# In[ ]:


get_ipython().run_cell_magic('capture', '', '!mkdir -p /tmp/pip/cache/\n!cp /kaggle/input/detecto-install/detecto-1.1.3.xyz /tmp/pip/cache/detecto-1.1.3.tar.gz\n!cp /kaggle/input/detecto-install/detecto-1.1.3-py3-none-any.whl /tmp/pip/cache/\n!pip install --no-index --find-links /tmp/pip/cache/ detecto\n!mkdir -p /root/.cache/torch/checkpoints/\n!cp /kaggle/input/faster-rcnn/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth /root/.cache/torch/checkpoints/')


# ## Visualize
# Let's start by visualizing a random image.

# In[ ]:


from detecto import utils, visualize, core

plt.rcParams['figure.figsize'] = (12.0, 12.0)

files = glob.glob("./train/*")
for i in range(len(files)):
    fid = files[i].replace('./train/', '').split('.')[0]
    bx = df[df.image_id == fid]
    if len(bx) > 0:
        boxes=torch.FloatTensor(bx.bbox.tolist())
        image = utils.read_image('./train/'+fid+'.jpg')
        visualize.show_labeled_image(image, boxes)
        break


# ## Create Pascal VOC data
# Detecto expects annotation data in Pascal VOC format. And thus we need to install the pascal-voc-writer.

# In[ ]:


get_ipython().run_cell_magic('capture', '', '# install Pascal VOC writer from dataset\n!cp /kaggle/input/detecto-install/pascal_voc_writer-0.1.4-py3.6.egg /tmp/pip/cache/\n!cp /kaggle/input/detecto-install/pascal_voc_writer-0.1.4-py2.py3-none-any.whl /tmp/pip/cache/\n!pip install --no-index --find-links /tmp/pip/cache/ pascal_voc_writer')


# Create Pascal VOC .xml files, one for each image:

# In[ ]:


from pascal_voc_writer import Writer

LABEL = "Wheat"
def create_voc(folder):
    files = glob.glob(folder+"/*")
    for i in range(len(files)):
        fid = files[i].replace(folder+'/','').split('.')[0]
        ldf=df[df.image_id == fid].reset_index()
        if len(ldf)> 0:
            width, height = ldf.width.iloc[0], ldf.height.iloc[0]
            writer = Writer(fid+'.jpg', width, height)
            for j in range(len(ldf)):
                writer.addObject(LABEL, 
                                 int(ldf.bbox.iloc[j][0]), 
                                 int(ldf.bbox.iloc[j][1]), 
                                 int(ldf.bbox.iloc[j][2]),
                                 int(ldf.bbox.iloc[j][3]))
            writer.save(folder+'/'+fid+'.xml')
        
create_voc("./validate")
create_voc("./train")


# ## Train model
# Training is super simple, just a few lines:

# In[ ]:


dataset = core.Dataset('./train/')
loader = core.DataLoader(dataset, batch_size=16, shuffle=True)
val_dataset = core.Dataset('./validate/')
model = core.Model([LABEL])
losses = model.fit(loader, val_dataset, epochs=2, learning_rate=0.001, lr_step_size=5, verbose=True)
print(losses)


# In[ ]:


#cleanup
get_ipython().system('rm -fr train')
get_ipython().system('rm -fr validate')


# ## Predict
# Then we can do predictions:

# In[ ]:


tfiles = glob.glob(DATA+"test/*")
predf=pd.DataFrame(columns=['image_id', 'PredictionString'])
for i in range(len(tfiles)):
    image = utils.read_image(tfiles[i])
    fid = tfiles[i].replace(DATA+'test/','').split('.')[0]
    predictions = model.predict(image)
    labels, boxes, scores = predictions
    b=boxes.numpy().astype(int)
    s=scores.numpy()
    pstr=''
    for i in range(len(b)):
        p=[b[i][0], b[i][1], b[i][2]-b[i][0], b[i][3]-b[i][1]]
        pstr=pstr+str(s[i])+' '+str(p[0])+' '+str(p[1])+' '+str(p[2])+' '+str(p[3])+' '
    predf=predf.append({'image_id': fid, 'PredictionString': pstr}, ignore_index=True)


# ## Submit
# And finally submit the data:

# In[ ]:


predf.to_csv('submission.csv', index=False)

