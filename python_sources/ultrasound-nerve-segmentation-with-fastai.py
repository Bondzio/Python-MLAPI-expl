#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from fastai.vision import *


# In[ ]:


import pandas as pd
import glob


# In[ ]:


path_images = Path("../input/train")
path_lbl = path_images


# In[ ]:


fnames = glob.glob('../input/train/*[!_mask].tif')
print(fnames[:3])
len(fnames)


# In[ ]:


img_f = fnames[3]
img = open_image(img_f)
img.show(figsize=(5,5))


# In[ ]:


lbl_names = glob.glob('../input/train/*_mask.tif')
print(lbl_names[:3])
len(lbl_names)


# In[ ]:


def get_y_fn(x):
    x = Path(x)
    return path_lbl/f'{x.stem}_mask{x.suffix}'


# In[ ]:


get_y_fn(fnames[0])


# In[ ]:


mask = open_mask(get_y_fn(img_f),div=True)
mask.show()


# In[ ]:


src_size = np.array(mask.shape[1:])
src_size,mask.data


# In[ ]:


torch.max(mask.data)


# In[ ]:


filter_func = lambda x: str(x) in fnames


# In[ ]:


#size = src_size//4
size = 128


# In[ ]:


from fastai.utils.mem import *
#free = gpu_mem_get_free_no_cache()
# the max size of bs depends on the available GPU RAM
#if free > 8200: bs=8
#else:           bs=4
#print(f"using bs={bs}, have {free}MB of GPU RAM free")
bs=16


# In[ ]:


class SegLabelListCustom(SegmentationLabelList):
    def open(self, fn): return open_mask(fn, div=True)
class SegItemListCustom(SegmentationItemList):
    _label_cls = SegLabelListCustom


# In[ ]:


codes = ['0','1']
src = (SegItemListCustom.from_folder(path_images)
       .filter_by_func(filter_func)
       .random_split_by_pct()
       .label_from_func(get_y_fn,classes=codes))


# In[ ]:


data = (src.transform(get_transforms(), size=size, tfm_y=True)
        .databunch(bs=bs)
        .normalize(imagenet_stats))
data.path = Path('.')


# In[ ]:


#data.show_batch(2, figsize=(10,7))


# In[ ]:


def dice_func(input, target):
    smooth = 0
    input = input[:,1,:,:]
    iflat = input.flatten().float()
    tflat = target.flatten().float()
    intersection = (iflat * tflat).sum()
    return ((2. * intersection + smooth) /
              (iflat.sum() + tflat.sum() + smooth))

def dice(input:Tensor, targs:Tensor, iou:bool=False)->Rank0Tensor:
    "Dice coefficient metric for binary target. If iou=True, returns iou metric, classic for segmentation problems."
    n = targs.shape[0]
    #print(n)
    input = input.argmax(dim=1).view(n,-1)
    #print(n)
    targs = targs.view(n,-1)
    #print(targs)
    intersect = (input * targs).sum().float()
    union = (input+targs).sum().float()
    if not iou: return (2. * intersect / union if union > 0 else union.new([1.]).squeeze())
    else: return intersect / (union-intersect+1.0)


# In[ ]:


learn = unet_learner(data, models.resnet50, metrics=[dice], wd=1e-3)


# In[ ]:


lr_find(learn)
learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(20,max_lr = 1e-5)


# In[ ]:


learn.recorder.plot_losses()


# In[ ]:


learn.recorder.plot_metrics()


# In[ ]:


learn.unfreeze()


# In[ ]:


learn.lr_find()
learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(60,max_lr = slice(1e-6,1e-4))


# In[ ]:


learn.recorder.plot_losses()


# In[ ]:


learn.recorder.plot_metrics()

