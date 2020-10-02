#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from torch.utils.data import Dataset
from pathlib import Path
from PIL import Image


class IMAGE_Dataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir)
        self.x = []
        self.y = []
        self.transform = transform
        self.num_classes = 0
        #print(self.root_dir.name)
        for i, _dir in enumerate(self.root_dir.glob('*')):
            for file in _dir.glob('*'):
                self.x.append(file)
                self.y.append(i)

            self.num_classes += 1
            #print(self.num_classes)
        #print(self.num_classes)
    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        image = Image.open(self.x[index]).convert('RGB')
        if self.transform:
            image = self.transform(image)

        return image, self.y[index]


# In[ ]:


import torch.nn as nn
import math


class VGG16(nn.Module):
    def __init__(self, num_classes=1000):
        super(VGG16, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.classifier = nn.Sequential(
            # input shape: (batch_size, 3, 224, 224) and
            # downsampled by a factor of 2^5 = 32 (5 times maxpooling)
            # So features' shape is (batch_size, 7, 7, 512)
            nn.Linear(in_features=7 * 7 * 512, out_features=4096),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(in_features=4096, out_features=4096),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(in_features=4096, out_features=num_classes)
        )

        # initialize parameters
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                n = module.kernel_size[0] * module.kernel_size[1] * module.out_channels
                module.weight.data.normal_(0, math.sqrt(2. / n))
                module.bias.data.zero_()
            elif isinstance(module, nn.Linear):
                module.weight.data.normal_(0, 0.01)
                module.bias.data.zero_()

    def forward(self, x):
        x = self.features(x)
        # flatten
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


# In[ ]:


import torch
import torch.nn as nn


from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
from pathlib import Path
import copy

##REPRODUCIBILITY
torch.manual_seed(10)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

#args = parse_args()
#CUDA_DEVICES = args.cuda_devices
#DATASET_ROOT = args.path
CUDA_DEVICES = torch.cuda.current_device()
DATASET_ROOT ='../input/seg_train/seg_train/'
losses=[]
acces=[]

def train():
	data_transform = transforms.Compose([
		transforms.Resize((224,224)),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
	])
	#print(DATASET_ROOT)
	train_set = IMAGE_Dataset(Path(DATASET_ROOT), data_transform)
	data_loader = DataLoader(dataset=train_set, batch_size=16, shuffle=True, num_workers=1)
	#print(train_set.num_classes)
	model = VGG16(num_classes=train_set.num_classes)
	model = model.cuda(CUDA_DEVICES)
	model.train()

	best_model_params = copy.deepcopy(model.state_dict())
	best_acc = 0.0
	num_epochs = 60
	criterion = nn.CrossEntropyLoss()
	optimizer = torch.optim.SGD(model.parameters(), 0.003,0.9)

	for epoch in range(num_epochs):
		print(f'Epoch: {epoch + 1}/{num_epochs}')
		print('-' * len(f'Epoch: {epoch + 1}/{num_epochs}'))

		training_loss = 0.0
		training_corrects = 0

		for i, (inputs, labels) in enumerate(data_loader):
			inputs = Variable(inputs.cuda(CUDA_DEVICES))
			labels = Variable(labels.cuda(CUDA_DEVICES))			

			optimizer.zero_grad()

			outputs = model(inputs)
			_, preds = torch.max(outputs.data, 1)
			loss = criterion(outputs, labels)

			loss.backward()
			optimizer.step()

			training_loss += loss.item() * inputs.size(0)
			#revise loss.data[0]-->loss.item()
			training_corrects += torch.sum(preds == labels.data)
			#print(f'training_corrects: {training_corrects}')

		training_loss = training_loss / len(train_set)
		training_acc =training_corrects.double() /len(train_set)
		#print(training_acc.type())
		#print(f'training_corrects: {training_corrects}\tlen(train_set):{len(train_set)}\n')
		losses.append(training_loss)
		acces.append(training_acc)
		print(f'Training loss: {training_loss:.4f}\taccuracy: {training_acc:.4f}\n')

		if training_acc > best_acc:
			best_acc = training_acc
			best_model_params = copy.deepcopy(model.state_dict())

	model.load_state_dict(best_model_params)
	torch.save(model, f'model-{best_acc:.02f}-best_train_acc.pth')


if __name__ == '__main__':
	train()


# In[ ]:


import numpy as np
np.save("losses.npy",losses)
np.save("acces.npy",acces)


# In[ ]:


acces


# In[ ]:


import matplotlib.pyplot as plt
plt.plot(losses)
plt.ylabel("losses")
plt.show()


# In[ ]:



plt.plot(acces)
plt.ylabel("acc")
plt.show()


# In[ ]:


get_ipython().system('ls')


# In[ ]:


import torch
from torch.autograd import Variable
from torchvision import transforms
from pathlib import Path
from PIL import Image
from torch.utils.data import DataLoader
DATASET_ROOT =  '../input/seg_test/seg_test/'
PATH_TO_WEIGHTS = './model-1.00-best_train_acc.pth'


def test():
    data_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225])
    ])
    test_set = IMAGE_Dataset(Path(DATASET_ROOT), data_transform)
    data_loader = DataLoader(
        dataset=test_set, batch_size=16, shuffle=True, num_workers=1)
    classes = [_dir.name for _dir in Path(DATASET_ROOT).glob('*')]

    model = torch.load(PATH_TO_WEIGHTS)
    model = model.cuda(CUDA_DEVICES)
    model.eval()

    total_correct = 0
    total = 0
    class_correct = list(0. for i in enumerate(classes))
    class_total = list(0. for i in enumerate(classes))
    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs = Variable(inputs.cuda(CUDA_DEVICES))
            labels = Variable(labels.cuda(CUDA_DEVICES))
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            # totoal
            total += labels.size(0)
            total_correct += (predicted == labels).sum().item()
            c = (predicted == labels).squeeze()
            # batch size
            for i in range(labels.size(0)):
                label =labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1

    print('Accuracy on the ALL test images: %d %%'
          % (100 * total_correct / total))

    for i, c in enumerate(classes):
        print('Accuracy of %5s : %2d %%' % (
        c, 100 * class_correct[i] / class_total[i]))


if __name__ == '__main__':
    test()


# In[ ]:


get_ipython().system('ls')

