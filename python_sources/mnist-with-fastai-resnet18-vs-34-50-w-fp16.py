#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from fastai import *
from fastai.vision import *
from fastai.metrics import *
from fastai.data_block import *
import numpy as np
import pandas as pd

path = Path("../input/digit-recognizer")


# # Preprocessing the data
# We take the custom image list detailed in [this kernel](https://www.kaggle.com/tanlikesmath/oversampling-mnist-with-fastai).

# In[ ]:


class CustomImageList(ImageList):
    def open(self, fn):
        img = fn.reshape(28,28)
        img = np.stack((img,)*3, axis=-1)
        return Image(pil2tensor(img, dtype=np.float32))
    
    @classmethod
    def from_csv_custom(cls, path:PathOrStr, csv_name:str, imgIdx:int=1, header:str='infer', **kwargs)->'ItemList': 
        df = pd.read_csv(Path(path)/csv_name, header=header)
        res = super().from_df(df, path=path, cols=0, **kwargs)
        
        res.items = df.iloc[:,imgIdx:].apply(lambda x: x.values / 255.0, axis=1).values
        
        return res
    
    @classmethod
    def from_df_custom(cls, path:PathOrStr, df:DataFrame, imgIdx:int=1, header:str='infer', **kwargs)->'ItemList': 
        res = super().from_df(df, path=path, cols=0, **kwargs)
        
        res.items = df.iloc[:,imgIdx:].apply(lambda x: x.values / 255.0, axis=1).values
        
        return res


# This allows us to create a fastai DataBunch, which is an all-ready packaged data set, split into train and validation, with transforms attached, and everything ready to train.

# In[ ]:


test = CustomImageList.from_csv_custom(path=path, csv_name="test.csv", imgIdx=0)
test


# In[ ]:


data = (CustomImageList.from_csv_custom(path=path, csv_name="train.csv", imgIdx=1)
        .split_by_rand_pct(0.2)
        .label_from_df(cols='label')
        .add_test(test, label=0)
        .transform(get_transforms(do_flip=False))
        .databunch(bs=128)
        .normalize(imagenet_stats))


# In[ ]:


data.show_batch(rows=3, figsize=(5,5))


# Now that we have the databunch, we'll try training with a Resnet18 first.

# # Resnet18

# In[ ]:


learn = cnn_learner(data, models.resnet18, metrics=accuracy, model_dir="/kaggle/working/models")
learn.lr_find()
learn.recorder.plot(suggestion=True)


# Now we're ready to fit one cycle. We'll use 1e-02 as the learning rate, around there loss is still decreasing and continues to do so past 1e-01.

# In[ ]:


learn.fit_one_cycle(1, max_lr=1e-02)


# 97% accuracy just after one cycle, not bad! Keep in mind we only trained the latest layer (the head) so far -- now we should unfreeze the backbone of the model (pretrained on Imagenet) to fine-tune the earlier layers too.

# In[ ]:


learn.save('mnist-resnet18-1')


# In[ ]:


learn.load('mnist-resnet18-1')


# Fine-tuning time! Let's unfreeze the backbone of the model see where our learning rate stands.

# In[ ]:


learn.unfreeze()
learn.lr_find()
learn.recorder.plot(suggestion=True)


# In[ ]:


max_lr = 1e-6
learn.fit_one_cycle(10, max_lr=max_lr)


# The last 2 epochs seemed to get it worse.

# In[ ]:


learn.save('mnist-resnet18-2')


# Let's try with a larger resnet (34), and using mixed precision training.

# # Resnet34 with mixed precision

# In[ ]:


learn = cnn_learner(data, models.resnet34, metrics=accuracy, model_dir="/kaggle/working/models").to_fp16()
learn.lr_find()
learn.recorder.plot(suggestion=True)


# In[ ]:


learn.fit_one_cycle(1, max_lr=1e-02)


# A little bit better from the get go. Let's save this first attempt, unfreeze and fine-tune.

# In[ ]:


learn.save('mnist-resnet34-fp16-1')


# In[ ]:


learn.unfreeze()
learn.lr_find()
learn.recorder.plot(suggestion=True)


# In[ ]:


learn.fit_one_cycle(6, max_lr=slice(1e-05, 1e-04))


# We see that in the beginning, even though the training loss is similar to the latest stages of our resnet18, the validation loss is lower. This could mean our model generalizes better! Possibly due to both our net being larger on one side, but also because we used mixed precision training.

# In[ ]:


learn.save('mnist-resnet34-fp16-2')


# # Resnet50 with mixed precision

# Let's see if we can do better with a larger resnet --resnet50.

# In[ ]:


learn = cnn_learner(data, models.resnet50, metrics=accuracy, model_dir="/kaggle/working/models").to_fp16()
learn.lr_find()
learn.recorder.plot(suggestion=True)


# In[ ]:


learn.fit_one_cycle(1, max_lr=1e-02)


# In[ ]:


learn.save('mnist-resnet50-fp16-1')


# In[ ]:


learn.unfreeze()
learn.lr_find()
learn.recorder.plot(suggestion=True)


# In[ ]:


learn.fit_one_cycle(6, max_lr=slice(1e-06, 1e-05))


# It seems that we're doing worse than with resnet34. I'm not sure why, but I'd guess it's because it's too complex a model for the amount of data we have?

# # Submitting results
# We'll go back to our best model so far, the `resnet34-fp16`, and submit the results to the competition.

# In[ ]:


learn = cnn_learner(data, models.resnet34, metrics=accuracy, model_dir="/kaggle/working/models").to_fp16().load('mnist-resnet34-fp16-2')


# In[ ]:


predictions, *_ = learn.get_preds(DatasetType.Test)
labels = np.argmax(predictions, 1)
submission_df = pd.DataFrame({'ImageId': list(range(1,len(labels)+1)), 'Label': labels})
submission_df.to_csv(f'submission.csv', index=False)

