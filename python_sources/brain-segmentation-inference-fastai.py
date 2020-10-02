#!/usr/bin/env python
# coding: utf-8

# # Use a pre-trained model to create segmentation masks
# 
# This notebook uses the models created by the v2 commit of https://www.kaggle.com/peter88b/brain-segmentation-fastai;
# https://www.kaggle.com/peter88b/brain-segmentation-fastai/output?scriptVersionId=24252708

# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from fastai.vision import *
from fastai.callbacks.hooks import *
from fastai.utils.mem import *


# In[ ]:


v2_model_path = Path('/kaggle/input/brain-segmentation-v2-models')
data_path = Path('/kaggle/input/lgg-mri-segmentation/kaggle_3m/')


# In[ ]:


# WARNING: If you used any customized classes when creating your learner, 
# you must first define these classes first before executing load_learner.
class SegmentationLabelListWithDiv(SegmentationLabelList): # TODO: rename
    def open(self, fn): return open_mask(fn, div=True)
class SegmentationItemListWithDiv(SegmentationItemList):
    _label_cls = SegmentationLabelListWithDiv


# In[ ]:


learn = load_learner(v2_model_path, 'stage-2-big-export.pkl')


# In[ ]:


# inference without target
data = DataBunch.load_empty(v2_model_path, 'big-databunch-export.pkl')
image_list = (ImageList.from_folder(data_path)
                .filter_by_func(lambda x: not x.name.endswith('_mask.tif')))
data.add_test(image_list, tfms=None, tfm_y=False)
data_items = data.test_ds


# In[ ]:


# inference with target
src = (SegmentationItemListWithDiv.from_folder(data_path, recurse=True)
       .filter_by_func(lambda x: not x.name.endswith('_mask.tif'))
       .split_by_rand_pct(0.2)
       .label_from_func(lambda x: x.parents[0] / (x.stem + '_mask' + x.suffix), classes=['n', 'y']))
data = (src # no transformations
        .databunch(bs=32)
        .normalize(imagenet_stats))
data_items = data.valid_ds


# The cell below will make a prediction (as we're doing segmentation, this means create a mask).
# 
# Run one of the cells above to either do;
# - inference without target or
# - inference with target

# In[ ]:


# pick an image at random - so you can re-run this cell to see different images
data_item = random.choice(data_items)
# or you could use a specific image
# data_item = data_items[0]
size = 5
img = data_item[0]
img.show(figsize=(size, size), title='input image')
target = data_item[1]
if not isinstance(target, EmptyLabel):
    print('inference with target')
    target.show(figsize=(size, size), title='target mask')
else:
    print('inference without target')
pred = learn.predict(img)
pred[0].show(figsize=(size, size), title='predicted mask')
if not isinstance(target, EmptyLabel):
    img.show(figsize=(size, size), y=target, title='input with target mask')
img.show(figsize=(size, size), y=pred[0], title='input with predicted mask')

