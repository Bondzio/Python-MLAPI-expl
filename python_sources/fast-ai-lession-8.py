#!/usr/bin/env python
# coding: utf-8

# In[ ]:



get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


from fastai.conv_learner import *
from fastai.dataset import *

from pathlib import Path
import json
from PIL import ImageDraw, ImageFont
from matplotlib import patches, patheffects


# In[ ]:


get_ipython().system('ls ../input/')


# In[ ]:


TMP_PATH = "/tmp/tmp"
MODEL_PATH = "/tmp/model/"


# In[ ]:


PATH = Path('../input/')
paths=list(PATH.iterdir())
paths


# In[ ]:


get_ipython().system('ls {str(paths[2])}/PASCAL_VOC')


# In[ ]:


trn_j = json.load((PATH/'pascal_voc/PASCAL_VOC/pascal_train2007.json').open())
trn_j.keys()


# In[ ]:


IMAGES, ANNOTATIONS, CATEGORIES = ['images', 'annotations', 'categories']
trn_j[IMAGES][:5]


# In[ ]:


trn_j[ANNOTATIONS][:5]


# In[ ]:


trn_j[CATEGORIES][:5]


# In[ ]:


FILE_NAME, ID, IMG_ID, CAT_ID, BBOX = 'file_name', 'id', 'image_id', 'category_id', 'bbox'

cats = {o[ID]:o['name'] for o in trn_j[CATEGORIES]}
trn_fns = {o[ID]:o[FILE_NAME] for o in trn_j[IMAGES]}
trn_ids = [o[ID] for o in trn_j[IMAGES]]


# In[ ]:


get_ipython().system('ls {paths[0]}/VOCdevkit/VOC2007')


# In[ ]:


list((PATH/'voctrainval_06-nov-2007/VOCdevkit/VOC2007').iterdir())


# In[ ]:


JPEGS = 'voctrainval_06-nov-2007/VOCdevkit/VOC2007/JPEGImages'


# In[ ]:


IMG_PATH = PATH/JPEGS
list(IMG_PATH.iterdir())[:5]


# In[ ]:


trn_anno = collections.defaultdict(lambda:[])
for o in trn_j[ANNOTATIONS]:
    if not o['ignore']:
        bb = o[BBOX]
        bb = np.array([bb[1], bb[0], bb[3]+bb[1]-1,bb[2]+bb[0]-1])
        trn_anno[o[IMG_ID]].append((bb, o[CAT_ID]))

len(trn_anno)


# In[ ]:


im0_d = trn_j[IMAGES][0]
im0_d[FILE_NAME], im0_d[ID]


# In[ ]:


im_a= trn_anno[im0_d[ID]];im_a


# In[ ]:


im0_a = im_a[0];im0_a


# In[ ]:


cats[7]


# In[ ]:


trn_anno[17]


# In[ ]:


cats[15], cats[13]


# In[ ]:


def bb_hw(a):
    """converts bounding box to height and width"""
    return np.array([a[1], a[0], a[3]-a[1]+1, a[2]-a[0]+1])


# In[ ]:


im = open_image(IMG_PATH/im0_d[FILE_NAME])


# In[ ]:


def show_img(im, figsize=None, ax=None):
    if not ax:
        fig,ax = plt.subplots(figsize=figsize)
    ax.imshow(im)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    return ax


# In[ ]:


def draw_outline(o, lw):
    o.set_path_effects([patheffects.Stroke(
        linewidth=lw, foreground='black'), patheffects.Normal()])


# In[ ]:


def draw_rect(ax, b):
    patch = ax.add_patch(patches.Rectangle(b[:2], *b[-2:], fill=False, edgecolor='white', lw=2))
    draw_outline(patch, 4)


# In[ ]:


def draw_text(ax, xy, txt, sz=14):
    text = ax.text(*xy, txt,
        verticalalignment='top', color='white', fontsize=sz, weight='bold')
    draw_outline(text, 1)


# In[ ]:


ax = show_img(im)
b = bb_hw(im0_a[0])
draw_rect(ax, b)
draw_text(ax, b[:2], cats[im0_a[1]])


# In[ ]:


def draw_im(im, ann):
    ax = show_img(im, figsize=(16, 8))
    for b, c in ann:
        b = bb_hw(b)
        draw_rect(ax, b)
        draw_text(ax, b[:2], cats[c], sz=16)


# In[ ]:


def draw_idx(i):
    im_a = trn_anno[i]
    im = open_image(IMG_PATH/trn_fns[i])
    print(im.shape)
    draw_im(im, im_a)


# In[ ]:


draw_idx(17)


# In[ ]:


def get_lrg(b):
    if not b: raise Exception()
    b = sorted(b, key = lambda x: np.product(x[0][-2:]-x[0][:2]), reverse=True)
    return b[0]


# In[ ]:


trn_lrg_anno = {a: get_lrg(b) for a, b in trn_anno.items()}


# In[ ]:


b,c = trn_lrg_anno[23]
b = bb_hw(b)
ax = show_img(open_image(IMG_PATH/trn_fns[23]), figsize=(5,10))
draw_rect(ax, b)
draw_text(ax, b[:2], cats[c], sz=16)


# In[ ]:


get_ipython().system('mkdir {TMP_PATH}')
CSV = Path(TMP_PATH + '/lrg.csv')


# In[ ]:


df = pd.DataFrame({'fn': [trn_fns[o] for o in trn_ids],
                  'cat': [cats[trn_lrg_anno[o][1]] for o in trn_ids]}, columns=['fn', 'cat']
                 )
df.to_csv(CSV, index=False)


# In[ ]:


get_ipython().system('ls {TMP_PATH}')


# In[ ]:


f_model = resnet34
sz=224
bs=64


# In[ ]:


tfms = tfms_from_model(f_model, sz, aug_tfms=transforms_side_on,crop_type=CropType.NO)
md = ImageClassifierData.from_csv(PATH, JPEGS, CSV, tfms=tfms, bs=bs)


# In[ ]:


x,y = next(iter(md.val_dl))


# In[ ]:


show_img(md.val_ds.denorm(to_np(x))[0]);


# In[ ]:


learn = ConvLearner.pretrained(f_model, md,metrics=[accuracy], tmp_name=TMP_PATH, models_name=MODEL_PATH)


# In[ ]:


learn.opt_fn = optim.Adam


# In[ ]:


lrf = learn.lr_find(1e-5,100)


# In[ ]:


learn.sched.plot()


# In[ ]:


learn.sched.plot(n_skip=5, n_skip_end=1)


# In[ ]:


lr = 2e-2


# In[ ]:


learn.fit(lr, 1, cycle_len=1)


# In[ ]:


lrs = np.array([lr/1000,lr/100,lr])


# In[ ]:


learn.freeze_to(-2)


# In[ ]:


lrf=learn.lr_find(lrs/1000)
learn.sched.plot(1)


# In[ ]:


learn.fit(lrs/5, 1, cycle_len=1)


# In[ ]:


learn.unfreeze()


# In[ ]:


learn.fit(lrs/5, 1, cycle_len=2)


# In[ ]:


learn.save('clas_one')


# In[ ]:


learn.load('clas_one')


# In[ ]:


x,y = next(iter(md.val_dl))
probs = F.softmax(predict_batch(learn.model, x), -1)
x,preds = to_np(x),to_np(probs)
preds = np.argmax(preds, -1)


# In[ ]:


fig, axes = plt.subplots(3, 4, figsize=(12, 8))
for i,ax in enumerate(axes.flat):
# pdb.set_trace()
    ima=md.val_ds.denorm(x)[i]
    b = md.classes[preds[i]]
    ax = show_img(ima, ax=ax)
    draw_text(ax, (0,0), b)
plt.tight_layout()


# In[ ]:


BB_CSV = Path(TMP_PATH + '/bb.csv')


# In[ ]:


bb = np.array([trn_lrg_anno[o][0] for o in trn_ids])
bbs = [' '.join(str(p) for p in o) for o in bb]

df = pd.DataFrame({'fn': [trn_fns[o] for o in trn_ids], 'bbox': bbs}, columns=['fn','bbox'])
df.to_csv(BB_CSV, index=False)


# In[ ]:


BB_CSV.open().readlines()[:5]


# In[ ]:


f_model=resnet34
sz=224
bs=64


# In[ ]:


augs = [RandomFlip(), 
        RandomRotate(30),
        RandomLighting(0.1,0.1)]


# In[ ]:


tfms = tfms_from_model(f_model, sz, crop_type=CropType.NO, aug_tfms=augs)
md = ImageClassifierData.from_csv(PATH, JPEGS, BB_CSV, tfms=tfms, continuous=True, bs=4)


# In[ ]:


idx=3
fig,axes = plt.subplots(3,3, figsize=(9,9))
for i,ax in enumerate(axes.flat):
    x,y=next(iter(md.aug_dl))
    ima=md.val_ds.denorm(to_np(x))[idx]
    b = bb_hw(to_np(y[idx]))
    print(b)
    show_img(ima, ax=ax)
    draw_rect(ax, b)


# In[ ]:


augs = [RandomFlip(tfm_y=TfmType.COORD),
        RandomRotate(30, tfm_y=TfmType.COORD),
        RandomLighting(0.1,0.1, tfm_y=TfmType.COORD)]


# In[ ]:


tfms = tfms_from_model(f_model, sz, crop_type=CropType.NO, tfm_y=TfmType.COORD, aug_tfms=augs)
md = ImageClassifierData.from_csv(PATH, JPEGS, BB_CSV, tfms=tfms, continuous=True, bs=4)


# In[ ]:


idx=3
fig,axes = plt.subplots(3,3, figsize=(9,9))
for i,ax in enumerate(axes.flat):
    x,y=next(iter(md.aug_dl))
    ima=md.val_ds.denorm(to_np(x))[idx]
    b = bb_hw(to_np(y[idx]))
    print(b)
    show_img(ima, ax=ax)
    draw_rect(ax, b)


# In[ ]:


tfm_y = TfmType.COORD
augs = [RandomFlip(tfm_y=tfm_y),
        RandomRotate(3, p=0.5, tfm_y=tfm_y),
        RandomLighting(0.05,0.05, tfm_y=tfm_y)]

tfms = tfms_from_model(f_model, sz, crop_type=CropType.NO, tfm_y=tfm_y, aug_tfms=augs)
md = ImageClassifierData.from_csv(PATH, JPEGS, BB_CSV, tfms=tfms, bs=bs, continuous=True)


# In[ ]:



512*7*7


# In[ ]:


head_reg4 = nn.Sequential(Flatten(), nn.Linear(25088,4))
learn = ConvLearner.pretrained(f_model, md, custom_head=head_reg4, tmp_name=TMP_PATH, models_name=MODEL_PATH)
learn.opt_fn = optim.Adam
learn.crit = nn.L1Loss()


# In[ ]:


learn.summary()


# In[ ]:


learn.lr_find(1e-5,100)
learn.sched.plot(5)


# In[ ]:


lr=2e-3


# In[ ]:


learn.fit(lr, 2, cycle_len=1, cycle_mult=2)


# In[ ]:


lrs = np.array([lr/100, lr/10, lr])


# In[ ]:


learn.freeze_to(-2)


# In[ ]:


lrf = learn.lr_find(lrs/1000)
learn.sched.plot(1)


# In[ ]:


learn.fit(lrs, 2, cycle_len=1, cycle_mult=2)


# In[ ]:


learn.freeze_to(-3)


# In[ ]:


learn.fit(lrs, 1, cycle_len=2)


# In[ ]:


learn.save('reg4')


# In[ ]:


x,y =next(iter(md.val_dl))
learn.model.eval()
preds = to_np(learn.model(VV(x)))


# In[ ]:


fig, axes = plt.subplots(3, 4, figsize=(12, 8))
for i,ax in enumerate(axes.flat):
    ima=md.val_ds.denorm(to_np(x))[i]
    b = bb_hw(preds[i])
    ax = show_img(ima, ax=ax)
    draw_rect(ax, b)
plt.tight_layout()


# In[ ]:




