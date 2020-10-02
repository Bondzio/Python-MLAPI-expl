#!/usr/bin/env python
# coding: utf-8

# ### EfficientNet-PyTorch
# 
# I am creatted EfficientNet-PyTorch and uploaded all pre-trained models.
# 
# ### Dataset : https://www.kaggle.com/gopidurgaprasad/efficientnetpytorch
# 
# This kernal was the Inference for above data :)
# 
# 
# I did some modification to load pre-trained weights form dataset directly.
# 
# from original documentation we need to add one extra perameter `model_path`.
# 
# Example:
# 
# `model = EfficientNet.from_pretrained("efficientnet-b1", model_path="../input/efficientnetpytorch/EfficientNet-PyTorch/")`
# 

# In[ ]:


get_ipython().run_cell_magic('writefile', 'create_folds.py', '\nimport pandas as pd\nfrom iterstrat.ml_stratifiers import MultilabelStratifiedKFold\n\nif __name__ == "__main__":\n    df = pd.read_csv("../input/train.csv")\n    print(df.head())\n    df.loc[:, \'kfold\'] = -1\n\n    df = df.sample(frac=1).reset_index(drop=True)\n\n    X = df.image_id.values\n    y = df[[\'grapheme_root\', \'vowel_diacritic\', \'consonant_diacritic\']].values\n\n    mskf = MultilabelStratifiedKFold(n_splits=5)\n\n    for fold, (trn_, val_) in enumerate(mskf.split(X, y)):\n        print("TRAIN: ", trn_, "VAL: ", val_)\n        df.loc[val_, "kfold"] = fold\n\n    print(df.kfold.value_counts())\n    df.to_csv("../input/train_folds.csv", index=False)')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'create_image_pickles.py', '\nimport pandas as pd\nimport joblib\nimport glob\nfrom tqdm import tqdm\n\nif __name__ == "__main__":\n    files = glob.glob("../input/train_*.parquet")\n    for f in files:\n        df = pd.read_parquet(f, engine=\'fastparquet\')\n        image_ids = df.image_id.values\n        df = df.drop("image_id", axis=1)\n        image_array = df.values\n        for j, image_id in tqdm(enumerate(image_ids), total=len(image_ids)):\n            joblib.dump(image_array[j, :], f"../input/image_pickles/{image_id}.pkl")')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'dataset.py', '\nimport pandas as pd\nimport albumentations\nimport joblib\nimport numpy as np\nimport torch\n\nfrom PIL import Image\n\nclass BengaliDatasetTrain:\n    def __init__(self, folds, img_height, img_width, mean, std):\n        df = pd.read_csv("../input/train_folds.csv")\n        df = df[["image_id", "grapheme_root", "vowel_diacritic", "consonant_diacritic", "kfold"]]\n\n        df = df[df.kfold.isin(folds)].reset_index(drop=True)\n        \n        self.image_ids = df.image_id.values\n        self.grapheme_root = df.grapheme_root.values\n        self.vowel_diacritic = df.vowel_diacritic.values\n        self.consonant_diacritic = df.consonant_diacritic.values\n\n        if len(folds) == 1:\n            self.aug = albumentations.Compose([\n                albumentations.Resize(img_height, img_width, always_apply=True),\n                albumentations.Normalize(mean, std, always_apply=True)\n            ])\n        else:\n            self.aug = albumentations.Compose([\n                albumentations.Resize(img_height, img_width, always_apply=True),\n                #albumentations.ShiftScaleRotate(shift_limit=0.0625,\n                #                                scale_limit=0.1, \n                #                                rotate_limit=5,\n                #                                p=0.9),\n                albumentations.Normalize(mean, std, always_apply=True)\n            ])\n\n\n    def __len__(self):\n        return len(self.image_ids)\n    \n    def __getitem__(self, item):\n        image = joblib.load(f"../input/image_pickles/{self.image_ids[item]}.pkl")\n        image = image.reshape(137, 236).astype(float)\n        image = Image.fromarray(image).convert("RGB")\n        image = self.aug(image=np.array(image))["image"]\n        image = np.transpose(image, (2, 0, 1)).astype(np.float32)\n\n        return {\n            "image": torch.tensor(image, dtype=torch.float),\n            "grapheme_root": torch.tensor(self.grapheme_root[item], dtype=torch.long),\n            "vowel_diacritic": torch.tensor(self.vowel_diacritic[item], dtype=torch.long),\n            "consonant_diacritic": torch.tensor(self.consonant_diacritic[item], dtype=torch.long)\n        }')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'models.py', '\nimport pretrainedmodels\nimport torch.nn as nn\nfrom torch.nn import functional as F\n\nclass ResNet34(nn.Module):\n    def __init__(self, pretrained):\n        super(ResNet34, self).__init__()\n        if pretrained is True:\n            self.model = pretrainedmodels.__dict__["resnet34"](pretrained="imagenet")\n        else:\n            self.model = pretrainedmodels.__dict__["resnet34"](pretrained=None)\n        \n        self.l0 = nn.Linear(512, 168)\n        self.l1 = nn.Linear(512, 11)\n        self.l2 = nn.Linear(512, 7)\n\n    def forward(self, x):\n        bs, _, _, _ = x.shape\n        x = self.model.features(x)\n        x = F.adaptive_avg_pool2d(x, 1).reshape(bs, -1)\n        l0 = self.l0(x)\n        l1 = self.l1(x)\n        l2 = self.l2(x)\n        return l0, l1, l2')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'efficientnet_model.py', '\nfrom efficientnet_pytorch import EfficientNet\nimport torch.nn as nn\nfrom torch.nn import functional as F\n\nclass EfficientNetB1(nn.Module):\n    def __init__(self, pretrained):\n        super(EfficientNetB1, self).__init__()\n\n        if pretrained is True:\n            self.model = EfficientNet.from_pretrained("efficientnet-b1")\n        \n        self.l0 = nn.Linear(1280, 168)\n        self.l1 = nn.Linear(1280, 11)\n        self.l2 = nn.Linear(1280, 7)\n\n    def forward(self, x):\n        bs, _, _, _ = x.shape\n        x = self.model.extract_features(x)\n        x = F.adaptive_avg_pool2d(x, 1).reshape(bs, -1)\n        l0 = self.l0(x)\n        l1 = self.l1(x)\n        l2 = self.l2(x)\n\n        return l0, l1, l2')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'model_dispatcher.py', '\nimport models\nimport efficientnet_model\n\nMODEL_DISPATCHER = {\n    "resnet34": models.ResNet34,\n    "efficientNetb1": efficientnet_model.EfficientNetB1\n}  ')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'train.py', '\nimport os\nimport ast\nimport torch\nimport torch.nn as nn\nimport numpy as np\nimport sklearn.metrics\n\nfrom model_dispatcher import MODEL_DISPATCHER\nfrom dataset import BengaliDatasetTrain\nfrom tqdm import tqdm\nfrom pytorchtools import EarlyStopping\n\n\nDEVICE = "cuda"\nTRAINING_FOLDS_CSV = os.environ.get("TRAINING_FOLDS_CSV")\n\nIMG_HEIGHT = int(os.environ.get("IMG_HEIGHT"))\nIMG_WIDTH = int(os.environ.get("IMG_WIDTH"))\nEPOCHS = int(os.environ.get("EPOCHS"))\n\nTRAIN_BATCH_SIZE = int(os.environ.get("TRAIN_BATCH_SIZE"))\nTEST_BATCH_SIZE = int(os.environ.get("TEST_BATCH_SIZE"))\n\nMODEL_MEAN = ast.literal_eval(os.environ.get("MODEL_MEAN"))\nMODEL_STD = ast.literal_eval(os.environ.get("MODEL_STD"))\n\nTRAINING_FOLDS = ast.literal_eval(os.environ.get("TRAINING_FOLDS"))\nVALIDATION_FOLDS = ast.literal_eval(os.environ.get("VALIDATION_FOLDS"))\nBASE_MODEL = os.environ.get("BASE_MODEL")\n\n\n\ndef macro_recall(pred_y, y, n_grapheme=168, n_vowel=11, n_consonant=7):\n    \n    pred_y = torch.split(pred_y, [n_grapheme, n_vowel, n_consonant], dim=1)\n    pred_labels = [torch.argmax(py, dim=1).cpu().numpy() for py in pred_y]\n\n    y = y.cpu().numpy()\n\n    recall_grapheme = sklearn.metrics.recall_score(pred_labels[0], y[:, 0], average=\'macro\')\n    recall_vowel = sklearn.metrics.recall_score(pred_labels[1], y[:, 1], average=\'macro\')\n    recall_consonant = sklearn.metrics.recall_score(pred_labels[2], y[:, 2], average=\'macro\')\n    scores = [recall_grapheme, recall_vowel, recall_consonant]\n    final_score = np.average(scores, weights=[2, 1, 1])\n    print(f\'recall: grapheme {recall_grapheme}, vowel {recall_vowel}, consonant {recall_consonant}, \'f\'total {final_score}, y {y.shape}\')\n    \n    return final_score\n\n\ndef loss_fn(outputs, targets):\n    o1, o2, o3 = outputs\n    t1, t2, t3 = targets\n    l1 = nn.CrossEntropyLoss()(o1, t1)\n    l2 = nn.CrossEntropyLoss()(o2, t2)\n    l3 = nn.CrossEntropyLoss()(o3, t3)\n    return (l1 + l2 + l3) / 3\n\n\n\ndef train(dataset, data_loader, model, optimizer):\n    model.train()\n    final_loss = 0\n    counter = 0\n    final_outputs = []\n    final_targets = []\n\n    for bi, d in tqdm(enumerate(data_loader), total=int(len(dataset)/data_loader.batch_size)):\n        counter = counter + 1\n        image = d["image"]\n        grapheme_root = d["grapheme_root"]\n        vowel_diacritic = d["vowel_diacritic"]\n        consonant_diacritic = d["consonant_diacritic"]\n\n        image = image.to(DEVICE, dtype=torch.float)\n        grapheme_root = grapheme_root.to(DEVICE, dtype=torch.long)\n        vowel_diacritic = vowel_diacritic.to(DEVICE, dtype=torch.long)\n        consonant_diacritic = consonant_diacritic.to(DEVICE, dtype=torch.long)\n        \n        print(image.shape)\n\n        optimizer.zero_grad()\n        outputs = model(image)\n        targets = (grapheme_root, vowel_diacritic, consonant_diacritic)\n        loss = loss_fn(outputs, targets)\n\n        loss.backward()\n        optimizer.step()\n\n        final_loss += loss\n\n        o1, o2, o3 = outputs\n        t1, t2, t3 = targets\n        final_outputs.append(torch.cat((o1,o2,o3), dim=1))\n        final_targets.append(torch.stack((t1,t2,t3), dim=1))\n\n        #if bi % 10 == 0:\n        #    break\n    final_outputs = torch.cat(final_outputs)\n    final_targets = torch.cat(final_targets)\n\n    print("=================Train=================")\n    macro_recall_score = macro_recall(final_outputs, final_targets)\n    \n    return final_loss/counter , macro_recall_score\n\n\n\ndef evaluate(dataset, data_loader, model):\n    with torch.no_grad():\n        model.eval()\n        final_loss = 0\n        counter = 0\n        final_outputs = []\n        final_targets = []\n        for bi, d in tqdm(enumerate(data_loader), total=int(len(dataset)/data_loader.batch_size)):\n            counter = counter + 1\n            image = d["image"]\n            grapheme_root = d["grapheme_root"]\n            vowel_diacritic = d["vowel_diacritic"]\n            consonant_diacritic = d["consonant_diacritic"]\n\n            image = image.to(DEVICE, dtype=torch.float)\n            grapheme_root = grapheme_root.to(DEVICE, dtype=torch.long)\n            vowel_diacritic = vowel_diacritic.to(DEVICE, dtype=torch.long)\n            consonant_diacritic = consonant_diacritic.to(DEVICE, dtype=torch.long)\n\n            outputs = model(image)\n            targets = (grapheme_root, vowel_diacritic, consonant_diacritic)\n            loss = loss_fn(outputs, targets)\n            final_loss += loss\n\n            o1, o2, o3 = outputs\n            t1, t2, t3 = targets\n            #print(t1.shape)\n            final_outputs.append(torch.cat((o1,o2,o3), dim=1))\n            final_targets.append(torch.stack((t1,t2,t3), dim=1))\n        \n        final_outputs = torch.cat(final_outputs)\n        final_targets = torch.cat(final_targets)\n\n        print("=================Train=================")\n        macro_recall_score = macro_recall(final_outputs, final_targets)\n\n    return final_loss/counter , macro_recall_score\n\n\n\ndef main():\n    model = MODEL_DISPATCHER[BASE_MODEL](pretrained=True)\n    model.to(DEVICE)\n\n    train_dataset = BengaliDatasetTrain(\n        folds=TRAINING_FOLDS,\n        img_height = IMG_HEIGHT,\n        img_width = IMG_WIDTH,\n        mean = MODEL_MEAN,\n        std = MODEL_STD\n    )\n\n    train_loader = torch.utils.data.DataLoader(\n        dataset=train_dataset,\n        batch_size= TRAIN_BATCH_SIZE,\n        shuffle=True,\n        num_workers=4\n    )\n\n    valid_dataset = BengaliDatasetTrain(\n        folds=VALIDATION_FOLDS,\n        img_height = IMG_HEIGHT,\n        img_width = IMG_WIDTH,\n        mean = MODEL_MEAN,\n        std = MODEL_STD\n    )\n\n    valid_loader = torch.utils.data.DataLoader(\n        dataset=valid_dataset,\n        batch_size= TEST_BATCH_SIZE,\n        shuffle=True,\n        num_workers=4\n    )\n\n    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)\n    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, \n                                                            mode="min", \n                                                            patience=5, \n                                                            factor=0.3,verbose=True)\n\n    early_stopping = EarlyStopping(patience=5, verbose=True)\n\n    #if torch.cuda.device_count() > 1:\n    #    model = nn.DataParallel(model)\n\n    best_score = -1\n\n    print("FOLD : ", VALIDATION_FOLDS[0] )\n    \n    for epoch in range(1, EPOCHS+1):\n\n        train_loss, train_score = train(train_dataset,train_loader, model, optimizer)\n        val_loss, val_score = evaluate(valid_dataset, valid_loader, model)\n\n        scheduler.step(val_loss)\n\n        \n\n        if val_score > best_score:\n            best_score = val_score\n            torch.save(model.state_dict(), f"{BASE_MODEL}_fold{VALIDATION_FOLDS[0]}.pth")\n\n        epoch_len = len(str(EPOCHS))\n        print_msg = (f\'[{epoch:>{epoch_len}}/{EPOCHS:>{epoch_len}}] \' +\n                     f\'train_loss: {train_loss:.5f} \' +\n                     f\'train_score: {train_score:.5f} \' +\n                     f\'valid_loss: {val_loss:.5f} \' +\n                     f\'valid_score: {val_score:.5f}\'\n                    )\n        \n        print(print_msg)\n\n        early_stopping(val_score, model)\n        if early_stopping.early_stop:\n            print("Early stopping")\n            break\n\n\nif __name__ == "__main__":\n    main()')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'run.sh', '\nexport IMG_HEIGHT=137\nexport IMG_WIDTH=236\nexport EPOCHS=50\nexport TRAIN_BATCH_SIZE=64\nexport TEST_BATCH_SIZE=64\nexport MODEL_MEAN="(0.485, 0.456, 0.406)"\nexport MODEL_STD="(0.229, 0.224, 0.225)"\nexport BASE_MODEL="efficientNetb1"\nexport TRAINING_FOLDS_CSV="../input/train_folds.csv"\n\n\nexport TRAINING_FOLDS="(0,1,2,3)"\nexport VALIDATION_FOLDS="(4,)"\npython3 train.py\n\nexport TRAINING_FOLDS="(0,1,2,4)"\nexport VALIDATION_FOLDS="(3,)"\npython3 train.py\n\nexport TRAINING_FOLDS="(0,1,3,4)"\nexport VALIDATION_FOLDS="(2,)"\npython3 train.py\n\nexport TRAINING_FOLDS="(0,2,3,4)"\nexport VALIDATION_FOLDS="(1,)"\npython3 train.py\n\nexport TRAINING_FOLDS="(1,2,3,4)"\nexport VALIDATION_FOLDS="(0,)"\npython3 train.py')


# # Inference

# In[ ]:


import sys
pt_models = "../input/pretrained-models/pretrained-models.pytorch-master/"
sys.path.insert(0, pt_models)
import pretrainedmodels


# In[ ]:


ef_models = "../input/efficientnetpytorch/EfficientNet-PyTorch/"
sys.path.insert(0, ef_models)
from efficientnet_pytorch import EfficientNet


# In[ ]:


import glob
import torch
import albumentations
import pandas as pd
import numpy as np

from tqdm import tqdm
from PIL import Image
import joblib
import torch.nn as nn
from torch.nn import functional as F


# In[ ]:



MODEL_MEAN = (0.485, 0.456, 0.406)
MODEL_STD = (0.229, 0.224, 0.225)
IMG_HEIGHT = 137
IMG_WIDTH = 236
DEVICE="cuda"


# In[ ]:


class ResNet34(nn.Module):
    def __init__(self, pretrained):
        super(ResNet34, self).__init__()
        if pretrained is True:
            self.model = pretrainedmodels.__dict__["resnet34"](pretrained="imagenet")
        else:
            self.model = pretrainedmodels.__dict__["resnet34"](pretrained=None)
        
        self.l0 = nn.Linear(512, 168)
        self.l1 = nn.Linear(512, 11)
        self.l2 = nn.Linear(512, 7)

    def forward(self, x):
        bs, _, _, _ = x.shape
        x = self.model.features(x)
        x = F.adaptive_avg_pool2d(x, 1).reshape(bs, -1)
        l0 = self.l0(x)
        l1 = self.l1(x)
        l2 = self.l2(x)
        return l0, l1, l2


# In[ ]:


#from efficientnet_pytorch import EfficientNet
import torch.nn as nn
from torch.nn import functional as F

class EfficientNetB3(nn.Module):
    def __init__(self, pretrained):
        super(EfficientNetB3, self).__init__()

        if pretrained is True:
            self.model = EfficientNet.from_pretrained("efficientnet-b3", model_path=ef_models)
        
        self.l0 = nn.Linear(1536, 168)
        self.l1 = nn.Linear(1536, 11)
        self.l2 = nn.Linear(1536, 7)

    def forward(self, x):
        bs, _, _, _ = x.shape
        x = self.model.extract_features(x)
        x = F.adaptive_avg_pool2d(x, 1).reshape(bs, -1)
        l0 = self.l0(x)
        l1 = self.l1(x)
        l2 = self.l2(x)

        return l0, l1, l2


# In[ ]:


class BengaliDatasetTest:
    def __init__(self, df, img_height, img_width, mean, std):
        
        self.image_ids = df.image_id.values
        self.img_arr = df.iloc[:, 1:].values

        self.aug = albumentations.Compose([
            albumentations.Resize(img_height, img_width, always_apply=True),
            albumentations.Normalize(mean, std, always_apply=True)
        ])


    def __len__(self):
        return len(self.image_ids)
    
    def __getitem__(self, item):
        image = self.img_arr[item, :]
        img_id = self.image_ids[item]
        
        image = image.reshape(137, 236).astype(float)
        image = Image.fromarray(image).convert("RGB")
        image = self.aug(image=np.array(image))["image"]
        image = np.transpose(image, (2, 0, 1)).astype(np.float32)
        

        return {
            "image": torch.tensor(image, dtype=torch.float),
            "image_id": img_id
        }


# In[ ]:


model = EfficientNetB3(pretrained=True)
model.load_state_dict(torch.load("../input/resnet34-weights/efficientnetB3_fold4.pth"))
model.to(DEVICE)
model.eval()


# In[ ]:


TEST_BATCH_SIZE = 32


predictions = []

for file_idx in range(4):
    df = pd.read_parquet(f"../input/bengaliai-cv19/test_image_data_{file_idx}.parquet")
    
    dataset = BengaliDatasetTest(df=df,
                                img_height=IMG_HEIGHT,
                                img_width=IMG_WIDTH,
                                mean=MODEL_MEAN,
                                std=MODEL_STD)
    
    data_loader = torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size= TEST_BATCH_SIZE,
        shuffle=False,
        num_workers=4
    )
    
    for bi, d in enumerate(data_loader):
        image = d["image"]
        img_id = d["image_id"]
        image = image.to(DEVICE, dtype=torch.float)
        
        g, v, c = model(image)
        g = np.argmax(g.cpu().detach().numpy(), axis=1)
        v = np.argmax(v.cpu().detach().numpy(), axis=1)
        c = np.argmax(c.cpu().detach().numpy(), axis=1)
        
        for ii, imid in enumerate(img_id):
            predictions.append((f"{imid}_grapheme_root", g[ii]))
            predictions.append((f"{imid}_vowel_diacritic", v[ii]))
            predictions.append((f"{imid}_consonant_diacritic", c[ii]))
            
            


# In[ ]:


sub = pd.DataFrame(predictions, columns=["row_id", "target"])


# In[ ]:


sub.head()


# In[ ]:


sub.to_csv("submission.csv", index=False)


# In[ ]:


sub.shape


# In[ ]:




