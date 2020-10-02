#!/usr/bin/env python
# coding: utf-8

# # Usable & complete data loading utility
# 
# This kernel is an alternative to my own previous kernel : https://www.kaggle.com/guillaumedesforges/loading-the-cropped-dogs-seamlessly-with-pytorch
# 
# There were many images with more than one dog, by leveraging the annotation added to the competition we can get around 1500 more dogs (credits to @ddrbcn).
# 
# Plus, this kernel loads the images to the RAM, giving a huge boost in performance !

# In[ ]:


# required imports
import os
import xml.etree.ElementTree as ET
import torchvision
from tqdm import tqdm_notebook as tqdm


# In[ ]:


class FullCroppedDogsFolderDataset(torchvision.datasets.vision.VisionDataset):
    def __init__(self, root, transform=None, target_transform=None):
        super().__init__(root, transform=transform, target_transform=target_transform)
        self.transform = transform
        self.target_transform = target_transform
        
        self.samples = self._load_subfolders_images(self.root)
        if len(self.samples) == 0:
            raise RuntimeError("Found 0 files in subfolders of: {}".format(self.root))
            
    def _load_subfolders_images(self, root):
        IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')

        def is_valid_file(x):
            return torchvision.datasets.folder.has_file_allowed_extension(x, IMG_EXTENSIONS)

        required_transforms = torchvision.transforms.Compose([
            torchvision.transforms.Resize(64),
            torchvision.transforms.CenterCrop(64),
        ])

        imgs = []

        paths = []
        for root, _, fnames in sorted(os.walk(root)):
            for fname in sorted(fnames):
                path = os.path.join(root, fname)
                paths.append(path)

        pbar = tqdm(paths, desc='Loading cropped images')

        for path in pbar:
            if is_valid_file(path):
                # Load image
                img = torchvision.datasets.folder.default_loader(path)

                # Get bounding boxes
                annotation_basename = os.path.splitext(os.path.basename(path))[0]
                annotation_dirname = next(dirname for dirname in os.listdir('../input/annotation/Annotation/') if dirname.startswith(annotation_basename.split('_')[0]))
                annotation_filename = os.path.join('../input/annotation/Annotation', annotation_dirname, annotation_basename)
                tree = ET.parse(annotation_filename)
                root = tree.getroot()
                objects = root.findall('object')
                for o in objects:
                    bndbox = o.find('bndbox')
                    xmin = int(bndbox.find('xmin').text)
                    ymin = int(bndbox.find('ymin').text)
                    xmax = int(bndbox.find('xmax').text)
                    ymax = int(bndbox.find('ymax').text)

                    bbox = (xmin, ymin, xmax, ymax)

                    object_img = required_transforms(img.crop(bbox))
                    imgs.append(object_img)
                
                pbar.set_postfix_str("{} cropped images loaded".format(len(imgs)))

        return imgs
    
    def __getitem__(self, index):
        sample = self.samples[index]
        target = 1
        
        if self.transform is not None:
            sample = self.transform(sample)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return sample, target

    def __len__(self):
        return len(self.samples)


# In[ ]:


dataset = FullCroppedDogsFolderDataset(
    '../input/all-dogs/',
    transform=torchvision.transforms.Compose([
        torchvision.transforms.RandomHorizontalFlip(),
        torchvision.transforms.ToTensor(),
    ])
)


# In[ ]:


len(dataset)


# In[ ]:


dataset[0]


# In[ ]:


# Benchmark against previous loader
# https://www.kaggle.com/guillaumedesforges/loading-the-cropped-dogs-seamlessly-with-pytorch
# I had 5.43 ms (against 4.6 ms for vanilla ImageFolder)
%%timeit
dataset[0]


# Memory usage is ~= 2GB.

# I hope you'll find this kernel helpful ! I tried to come up with something flexible enough but give a boost in performance.
# 
# Let me know if you can think of any improvements. :-)
# 
# If you'll use this loader, a +1 is always welcome ! ;-)
# 
# 
# Cheers,
# 
# Guillaume
