#!/usr/bin/env python
# coding: utf-8

# ## Importing libraries

# In[ ]:


import torch
import torchvision
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import figure


# ## Downloading Data

# In[ ]:


# Download training dataset
dataset = MNIST(root='data/', download=True, transform=transforms.ToTensor())


# In[ ]:


dataset[0]


# In[ ]:


print(type(dataset))
print(len(dataset))


# In[ ]:


test_dataset = MNIST(root='data/', train=False)
len(test_dataset)


# ## Split the dataset as train and validation (can also split as train, validation and test)

# In[ ]:


from torch.utils.data import random_split

train_ds, val_ds = random_split(dataset, [50000, 10000])
len(train_ds), len(val_ds)


# In[ ]:


from torch.utils.data import DataLoader

batch_size = 128

train_loader = DataLoader(train_ds, batch_size, shuffle=True)
val_loader = DataLoader(val_ds, batch_size)


# ## Make a sample model

# In[ ]:


import torch.nn as nn

input_size = 28*28
num_classes = 10

# Logistic regression model
model = nn.Linear(input_size, num_classes)


# We have 10 outputs so 10 rows. We have 784 inputs so 784 columns

# In[ ]:


print(model.weight.shape)
model.weight


# In[ ]:


print(model.bias.shape)
model.bias


# Total number of paramerters/weights are 10 * 784 + 10 = 7850

# In[ ]:


for images, labels in train_loader:
    print(labels)
    print(images.shape)
    outputs = model(images)
    break


# There is a type size missmatch. We have given a [3584 x 28] to multiply with [784 x 10]. This is happening because we are passing a batch here. To solve this we need to reshape the input tensor.

# In[ ]:


class MnistModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(input_size, num_classes)
        
    #this function is called when ever thr model is used..
    def forward(self, xb):
        xb = xb.reshape(-1, 784)
        out = self.linear(xb)
        return out
    
model = MnistModel()


# In[ ]:


print(model.linear.weight.shape, model.linear.bias.shape)
list(model.parameters())


# In[ ]:


for images, labels in train_loader:
    outputs = model(images)
    break

print('outputs.shape : ', outputs.shape)
print('Sample outputs :\n', outputs[:2].data)


# Different losses : https://ml-cheatsheet.readthedocs.io/en/latest/loss_functions.html#:~:text=Cross%2Dentropy%20loss%2C%20or%20log,diverges%20from%20the%20actual%20label.

# In[ ]:


import torch.nn.functional as F


# In[ ]:


# Apply softmax for each output row
probs = F.softmax(outputs, dim=1)

# Look at sample probabilities
print("Sample probabilities:\n", probs[:2].data)

# Add up the probabilities of an output row
print("Sum: ", torch.sum(probs[0]).item())


# In[ ]:


#max provides two results, maximum value and index with maximum value
max_probs, preds = torch.max(probs, dim=1)
print(preds)
print(max_probs)


# In[ ]:


labels


# In[ ]:


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))


# In[ ]:


accuracy(outputs, labels)


# In[ ]:


loss_fn = F.cross_entropy


# In[ ]:


# Loss for current batch of data
loss = loss_fn(outputs, labels)
print(loss)


# In[ ]:


#Dimension in pytorch : https://towardsdatascience.com/understanding-dimensions-in-pytorch-6edf9972d3be
class MnistModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(input_size, num_classes)
        
    def forward(self, xb):
        #reshaping
        xb = xb.reshape(-1, 784)
        out = self.linear(xb)
        return out
    
    def training_step(self, batch):
        images, labels = batch 
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss
    
    def validation_step(self, batch):
        images, labels = batch 
        out = self(images)                    # Generate predictions
        loss = F.cross_entropy(out, labels)   # Calculate loss
        acc = accuracy(out, labels)           # Calculate accuracy
        #returns a dictionary containg validation loss and validation accurracy
        return {'val_loss': loss, 'val_acc': acc}
        
    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        #stacks the batch loss over columns and do sum over columns. Dim 0 is columns and Dim 1 is row
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}
    
    def epoch_end(self, epoch, result):
        print("Epoch [{}], val_loss: {:.4f}, val_acc: {:.4f}".format(epoch, result['val_loss'], result['val_acc']))
    
model = MnistModel()


# In[ ]:


def evaluate(model, val_loader):
    #output contains a list of dictionaries with validation loass and validation accuracy
    outputs = [model.validation_step(batch) for batch in val_loader]
#     print(outputs)
    return model.validation_epoch_end(outputs)


# In[ ]:


def fit(epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.SGD):
    history = []
    optimizer = opt_func(model.parameters(), lr)
    for epoch in range(epochs):
        # Training Phase 
        for batch in train_loader:
            loss = model.training_step(batch)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        # Validation phase
        result = evaluate(model, val_loader)
        model.epoch_end(epoch, result)
        history.append(result)
    return history


# In[ ]:


result0 = evaluate(model, val_loader)
result0


# In[ ]:


history1 = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history2 = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history3 = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history4 = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
history = [result0] + history1 + history2 + history3 + history4
accuracies = [result['val_acc'] for result in history]
plt.plot(accuracies, '-x', label='Base Model')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend(loc="lower right")
plt.grid()
plt.title('Accuracy vs. No. of epochs');


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
history = [result0] + history1 + history2 + history3 + history4
losses = [result['val_loss'] for result in history]
plt.plot(losses, '-x', label='Base Model')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc="lower right")
plt.grid()
plt.title('Loss vs. No. of epochs');


# ## Checking the result

# In[ ]:


# Define test dataset
test_dataset = MNIST(root='data/', 
                     train=False,
                     transform=transforms.ToTensor())


# In[ ]:


img, label = test_dataset[0]
plt.imshow(img[0], cmap='gray')
print('Shape:', img.shape)
print('Label:', label)


# In[ ]:


type(img)


# In[ ]:


img.unsqueeze(0).shape #we can see that one more dimension was added here.


# The unsqueeze method add a new dimension so the model see this as batch of data with batch size 1

# In[ ]:


def predict_image(img, model):
    xb = img.unsqueeze(0)
    yb = model(xb)
    _, preds  = torch.max(yb, dim=1)
    return preds[0].item()


# In[ ]:


img, label = test_dataset[0]
plt.imshow(img[0], cmap='gray')
print('Label:', label, ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_dataset[101]
plt.imshow(img[0], cmap='gray')
print('Label:', label, ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_dataset[2340]
plt.imshow(img[0], cmap='gray')
print('Label:', label, ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_dataset[3478]
plt.imshow(img[0], cmap='gray')
print('Label:', label, ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_dataset[9755]
plt.imshow(img[0], cmap='gray')
print('Label:', label, ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_dataset[4512]
plt.imshow(img[0], cmap='gray')
print('Label:', label, ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_dataset[1839]
plt.imshow(img[0], cmap='gray')
print('Label:', label, ', Predicted:', predict_image(img, model))


# ## Test loss and accuracy

# In[ ]:


test_loader = DataLoader(test_dataset, batch_size=256)
result = evaluate(model, test_loader)
result


# In[ ]:


torch.save(model.state_dict(), 'mnist-logistic.pth')


# ## Experimenting with a small validation size (5%)

# In[ ]:


from torch.utils.data import random_split

train_ds, val_ds = random_split(dataset, [57000, 3000])
len(train_ds), len(val_ds)


# In[ ]:


batch_size = 128

train_loader = DataLoader(train_ds, batch_size, shuffle=True)
val_loader = DataLoader(val_ds, batch_size)


# In[ ]:


model = MnistModel()


# In[ ]:


result0vlow = evaluate(model, val_loader)
result0vlow


# In[ ]:


history1vlow = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history2vlow = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history3vlow = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history4vlow = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
historyvlow = [result0vlow] + history1vlow + history2vlow + history3vlow + history4vlow
accuraciesvlow = [result['val_acc'] for result in historyvlow]
plt.plot(accuracies, '-x', label='Base Model')
plt.plot(accuraciesvlow, '-o', label='Small Validation set')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend(loc="lower right")
plt.grid()
plt.title('Accuracy vs. No. of epochs');


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
historyvlow = [result0vlow] + history1vlow + history2vlow + history3vlow + history4vlow
lossesvlow = [result['val_loss'] for result in historyvlow]
plt.plot(losses, '-x', label='Base Model')
plt.plot(lossesvlow, '-o', label='Small Validation set')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc="lower right")
plt.grid()
plt.title('Loss vs. No. of epochs');


# ## Experimenting with a small validation size (40%)

# In[ ]:


train_ds, val_ds = random_split(dataset, [36000, 24000])
len(train_ds), len(val_ds)


# In[ ]:


batch_size = 128

train_loader = DataLoader(train_ds, batch_size, shuffle=True)
val_loader = DataLoader(val_ds, batch_size)

model = MnistModel()


# In[ ]:


result0vhigh = evaluate(model, val_loader)
result0vhigh


# In[ ]:


history1vhigh = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history2vhigh = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history3vhigh = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


history4vhigh = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
historyvhigh = [result0vhigh] + history1vhigh + history2vhigh + history3vhigh + history4vhigh
accuraciesvhigh = [result['val_acc'] for result in historyvhigh]
plt.plot(accuracies, '-x', label='Base Model')
plt.plot(accuraciesvlow, '-o', label='Small Validation set')
plt.plot(accuraciesvhigh, '-^', label='Higl Validation set')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend(loc="lower right")
plt.grid()
plt.title('Accuracy vs. No. of epochs');


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
historyvhigh = [result0vhigh] + history1vhigh + history2vhigh + history3vhigh + history4vhigh
lossesvhigh = [result['val_loss'] for result in historyvhigh]
plt.plot(losses, '-x', label='Base Model')
plt.plot(lossesvlow, '-o', label='Small Validation set')
plt.plot(lossesvhigh, '-^', label='Higl Validation set')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc="upper right")
plt.grid()
plt.title('Loss vs. No. of epochs');


# ## Low batch size 64

# In[ ]:


train_ds, val_ds = random_split(dataset, [50000, 10000])
len(train_ds), len(val_ds)

batch_size = 64

train_loader = DataLoader(train_ds, batch_size, shuffle=True)
val_loader = DataLoader(val_ds, batch_size)

model = MnistModel()

result0blow = evaluate(model, val_loader)
result0blow

history1blow = fit(5, 0.001, model, train_loader, val_loader)

history2blow = fit(5, 0.001, model, train_loader, val_loader)

history3blow = fit(5, 0.001, model, train_loader, val_loader)

history4blow = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
historyblow = [result0blow] + history1blow + history2blow + history3blow + history4blow
accuraciesblow = [result['val_acc'] for result in historyblow]
plt.plot(accuracies, '-x', label='Base Model')
plt.plot(accuraciesvlow, '-o', label='Small Validation set')
plt.plot(accuraciesvhigh, '-^', label='Higl Validation set')
plt.plot(accuraciesblow, '--', label='Low batch size')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend(loc="lower right")
plt.title('Accuracy vs. No. of epochs');
plt.grid()


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
historyblow = [result0blow] + history1blow + history2blow + history3blow + history4blow
lossesblow = [result['val_loss'] for result in historyblow]
plt.plot(losses, '-x', label='Base Model')
plt.plot(lossesvlow, '-o', label='Small Validation set')
plt.plot(lossesvhigh, '-^', label='Higl Validation set')
plt.plot(lossesblow, '--', label='Low batch size')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc="upper right")
plt.title('Loss vs. No. of epochs');
plt.grid()


# ## High batch size (512)

# In[ ]:


train_ds, val_ds = random_split(dataset, [50000, 10000])
len(train_ds), len(val_ds)

batch_size = 512

train_loader = DataLoader(train_ds, batch_size, shuffle=True)
val_loader = DataLoader(val_ds, batch_size)

model = MnistModel()

result0bhigh = evaluate(model, val_loader)
result0bhigh

history1bhigh = fit(5, 0.001, model, train_loader, val_loader)

history2bhigh = fit(5, 0.001, model, train_loader, val_loader)

history3bhigh = fit(5, 0.001, model, train_loader, val_loader)

history4bhigh = fit(5, 0.001, model, train_loader, val_loader)


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
historybhigh = [result0bhigh] + history1bhigh + history2bhigh + history3bhigh + history4bhigh
accuraciesbhigh = [result['val_acc'] for result in historybhigh]
plt.plot(accuracies, '-x', label='Base Model')
plt.plot(accuraciesvlow, '-o', label='Small Validation set')
plt.plot(accuraciesvhigh, '-^', label='Higl Validation set')
plt.plot(accuraciesblow, '--', label='Low batch size')
plt.plot(accuraciesbhigh, '--', label='High batch size')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend(loc="lower right")
plt.title('Accuracy vs. No. of epochs');
plt.grid()


# In[ ]:


# Replace these values with your results
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
historybhigh = [result0bhigh] + history1bhigh + history2bhigh + history3bhigh + history4bhigh
lossesbhigh = [result['val_loss'] for result in historybhigh]
plt.plot(losses, '-x', label='Base Model')
plt.plot(lossesvlow, '-o', label='Small Validation set')
plt.plot(lossesvhigh, '-^', label='Higl Validation set')
plt.plot(lossesblow, '--', label='Low batch size')
plt.plot(lossesbhigh, '--', label='High batch size')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc="lower right")
plt.grid()
plt.title('Accuracy vs. No. of epochs');


# In[ ]:




