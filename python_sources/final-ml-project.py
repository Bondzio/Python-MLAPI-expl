#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.backends.cudnn as cudnn

torch.manual_seed(5501778496583098492)
torch.cuda.manual_seed(5501778496583098492)
np.random.seed(832645)
random.seed(5678)

cudnn.deterministic = True
cudnn.benchmark = False


# model hyper-parameters
image_size=32
num_classes=10
alpha_s=0.5
alpha_t=0.8
beta_c=1
beta_sep=1.5
beta_p=4

# training hyper-parameters
train_iters=1000
pretrain_iters=20000
batch_size=64
lr=0.0004
lr_d=0.0004
beta1=0.5
beta2=0.999

# misc
mode='train'
model_path='./models'
mnist_path='../data/mnist'
svhn_path='../data/svhn'
log_step=10

source='svhn'
target='mnist'


# In[ ]:


import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models


class Net(nn.Module):
    def __init__(self, latent_dim=512, office=False):
        super(Net, self).__init__()
        self.office = False
        if not office:
            conv_dim = 64
            self.conv1 = conv(3, conv_dim, 5, 2, 2)
            self.conv2 = conv(conv_dim, conv_dim * 2, 5, 2, 2)
            self.conv3 = conv(conv_dim * 2, conv_dim * 4, 5, 2, 2)
            self.conv4 = conv(conv_dim * 4, conv_dim * 8, 4, 1, 0)
            self.conv2_drop = nn.Dropout2d()
            self.fc1 = nn.Linear(512, 256)
            self.fc2 = nn.Linear(256, 128)
            self.dense1_bn = nn.BatchNorm1d(128)
            self.fc3 = nn.Linear(128, 50)
            self.fc4 = nn.Linear(50, 10)

    def forward(self, x):
        if not self.office:
            # Encoder
            x = F.leaky_relu(self.conv1(x), 0.05)
            x = F.leaky_relu(self.conv2(x), 0.05)

            x = F.leaky_relu(self.conv3(x), 0.05)
            x = F.leaky_relu(self.conv4(x), 0.05)
            x = x.view(x.shape[0], -1)

            # Classifier
            x_c = F.relu(self.fc1(x))
            x_c = F.dropout(x_c, training=self.training)
            x_c = self.dense1_bn(self.fc2(x_c))
            x_c = F.relu(F.dropout(x_c, training=self.training))
            x_c = self.fc3(x_c)
            x_c = F.dropout(x_c, training=self.training)
            x_c = self.fc4(x_c)

            return x, F.softmax(x_c, dim=1)


class Net_D(nn.Module):
    def __init__(self, latent_dim=512):
        super(Net_D, self).__init__()
        self.fc1 = nn.Linear(latent_dim, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 50)
        self.fc4 = nn.Linear(50, 1)

    def forward(self, x):
        # Discriminator
        x_d = F.relu(self.fc1(x))
        x_d = F.dropout(x_d, training=self.training)
        x_d = self.fc2(x_d)
        x_d = F.dropout(x_d, training=self.training)
        x_d = self.fc3(x_d)
        x_d = F.dropout(x_d, training=self.training)
        x_d = self.fc4(x_d)

        return torch.sigmoid(x_d)


def conv(c_in, c_out, k_size, stride=2, pad=1, bn=True):
    """Custom convolutional layer for simplicity."""
    layers = []
    layers.append(nn.Conv2d(c_in, c_out, k_size, stride, pad, bias=True))  # bias=False
    if bn:
        layers.append(nn.BatchNorm2d(c_out))
    return nn.Sequential(*layers)


# In[ ]:


from torchvision import datasets
import gzip
import os
import pickle
import urllib

import numpy as np
import torch
import torch.utils.data as data
from torchvision import transforms
     
      
def get_loader():
    svhn_transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.Grayscale(num_output_channels=3),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    mnist_transform = transforms.Compose([
        transforms.Resize(32),
        transforms.Grayscale(num_output_channels=3),
        transforms.ColorJitter(brightness=30, contrast=30, saturation=30, hue=0.5),
        transforms.RandomApply([transforms.RandomRotation(30)]),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))])

    svhn = datasets.SVHN(root=svhn_path, split='train', download=True, transform=svhn_transform)
    svhn_val = datasets.SVHN(root=svhn_path, split='test', download=True, transform=svhn_transform)

    mnist = datasets.MNIST(root=mnist_path, download=True, transform=mnist_transform)
    mnist_val = datasets.MNIST(root=mnist_path, train=False, download=True, transform=mnist_transform)

    svhn_loader = torch.utils.data.DataLoader(dataset=svhn,
                                              batch_size=batch_size,
                                              shuffle=True,
                                              num_workers=2)
    svhn_val_loader = torch.utils.data.DataLoader(dataset=svhn_val,
                                              batch_size=batch_size,
                                              shuffle=True,
                                              num_workers=2)

    mnist_loader = torch.utils.data.DataLoader(dataset=mnist,
                                               batch_size=batch_size,
                                               shuffle=True,
                                               num_workers=2)
    mnist_val_loader = torch.utils.data.DataLoader(dataset=mnist_val,
                                                   batch_size=500,
                                                   shuffle=False,
                                                   num_workers=2)
    return svhn_loader, svhn_val_loader, mnist_loader, mnist_val_loader
       


# In[ ]:


import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from termcolor import colored
from torch import optim
from torch.autograd import Variable


def accuracy(true_labels, predicted_labels):
    _, pred = torch.max(predicted_labels, 1)

    correct = np.squeeze(pred.eq(true_labels.data.view_as(pred)))
    return correct.float().mean()


def xavier_weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.xavier_uniform_(m.weight, gain=np.sqrt(2))
        nn.init.constant_(m.bias, 0.1)


def pseudo_labeling(target, c, m=1):
    indexes = c[range(len(c)), torch.argmax(c, dim=1)] >= m
    indexes = np.array(np.nonzero(indexes.cpu().numpy())).flatten()
    pseudo_labels = c[indexes].clone()
    pseudo_labels = (pseudo_labels == pseudo_labels.max(dim=1, keepdim=True)[0]).long()
    _, pseudo_labels = torch.max(pseudo_labels, 1)
    uni = np.array(np.unique(pseudo_labels.cpu().numpy(), return_counts=True))
    mi = np.min(uni[1])
    if len(uni[1]) < 10:
        mi = 0
    ma = np.max(uni[1])
    return target[indexes], pseudo_labels, indexes, (mi + 1) / (ma + 1)


class Solver(object):
    def __init__(self, source_loader, source_val_loader, target_loader, target_val_loader):
        self.source_loader = source_loader
        self.source_val_loader = source_val_loader
        self.target_loader = target_loader
        self.target_val_loader = target_val_loader
        self.net = None
        self.net_optimizer = None
        self.net_d = None
        self.net_optimizer_d = None
        self.beta1 = beta1
        self.beta2 = beta2
        self.train_iters = train_iters
        self.pretrain_iters = pretrain_iters
        self.batch_size = batch_size
        self.lr = lr
        self.lr_d = lr_d
        self.alpha_s = alpha_s
        self.alpha_t = alpha_t
        self.beta_c = beta_c
        self.beta_sep = beta_sep
        self.beta_p = beta_p
        self.log_step = log_step
        self.model_path = model_path
        self.num_classes = num_classes
        self.build_model()

    def build_model(self):
        """Builds a generator and a discriminator."""
        self.net = Net()
        self.net_d = Net_D()

        net_params = list(self.net.parameters())
        net_d_params = list(self.net_d.parameters())
        self.net_optimizer = optim.Adam(net_params, self.lr, [self.beta1, self.beta2])
        self.net_optimizer_d = optim.Adam(net_d_params, self.lr_d, [self.beta1, self.beta2])

        if torch.cuda.is_available():
            self.net.cuda()
            self.net_d.cuda()

    def to_var(self, x):
        """Converts numpy to variable."""
        if torch.cuda.is_available():
            x = x.cuda()
        return Variable(x, requires_grad=False)

    def to_data(self, x):
        """Converts variable to numpy."""
        if torch.cuda.is_available():
            x = x.cpu()
        return x.data.numpy()

    def reset_grad(self):
        """Zeros the gradient buffers."""
        self.net_optimizer.zero_grad()
        self.net_optimizer_d.zero_grad()

    def separability_loss(self, labels, latents, imbalance_parameter=1):
        criteria = torch.nn.modules.loss.CosineEmbeddingLoss()
        loss_up = 0
        one_cuda = torch.ones(1).cuda()
        mean = torch.mean(latents, dim=0).cuda().view(1, -1)
        loss_down = 0
        for i in range(self.num_classes):
            indexes = labels.eq(i)
            mean_i = torch.mean(latents[indexes], dim=0).view(1, -1)
            if str(mean_i.norm().item()) != 'nan':
                for latent in latents[indexes]:
                    loss_up += criteria(latent.view(1, -1), mean_i, one_cuda)
                loss_down += criteria(mean, mean_i, one_cuda)
        loss = (loss_up / loss_down) * imbalance_parameter
        return loss

    def initialisation(self):
        self.net.apply(xavier_weights_init)
        self.net_d.apply(xavier_weights_init)
        source_iter = iter(self.source_loader)
        target_iter = iter(self.target_loader)
        target_val_iter = iter(self.target_val_loader)
        source_val_iter = iter(self.source_val_loader)
        source_per_epoch = len(source_iter)
        target_per_epoch = len(target_iter)
        targetval_per_epoch = len(target_val_iter)
        sourceval_per_epoch = len(source_val_iter)
        print(source_per_epoch, sourceval_per_epoch, target_per_epoch, targetval_per_epoch)

        criterion = nn.CrossEntropyLoss()

        f_labels = torch.LongTensor(128)
        f_labels[...] = 10

        t_labels = torch.LongTensor(128)
        t_labels[...] = 1

        # pretrain
        log_pre = 50
        source_iter = iter(self.source_loader)
        target_iter = iter(self.target_loader)
        return criterion, source_per_epoch, target_per_epoch, target_iter, source_iter, log_pre

    def train(self):
        criterion, source_per_epoch, target_per_epoch, target_iter, source_iter, log_pre = self.initialisation()

        pre_train = not os.path.exists(os.path.join(self.model_path, 'pre_train.pth'))

        print("Pretrain:\n*********")
        if pre_train:
            for step in range(self.pretrain_iters + 1):
                # ============ Initialization ============#
                # refresh
                if (step + 1) % (source_per_epoch) == 0:
                    source_iter = iter(self.source_loader)
                if (step + 1) % (target_per_epoch) == 0:
                    target_iter = iter(self.target_loader)
                # load the data
                source, s_labels = source_iter.next()
                target, t_labels = target_iter.next()
                target_rgb = target
                target, t_labels = self.to_var(target_rgb), self.to_var(t_labels).long().squeeze()
                source, s_labels = self.to_var(source), self.to_var(s_labels).long().squeeze()

                # ============ Training ============ #
                self.reset_grad()
                # forward
                latent, c = self.net(source)
                # loss
                loss_source_class = criterion(c, s_labels)

                # one step
                loss_source_class.backward()
                self.net_optimizer.step()
                self.reset_grad()
                # ============ Validation ============ #
                if (step + 1) % log_pre == 0:
                    _, c_source = self.net(source)
                    _, c_target = self.net(target)
                    print("[%d/20000] classification loss: %.4f" % (
                        step + 1, loss_source_class.item()))
                    print("source accuracy  %.4f;  target accuracy %.4f" % (
                        accuracy(s_labels, c_source),
                        accuracy(t_labels, c_target)))

            self.save_model()
        else:
            self.load_model()

        # ============ Initialization ============ #
        source_iter = iter(self.source_loader)
        target_iter = iter(self.target_loader)
        maxacc = 0.0
        maximum_acc = 0.0
        max_iter = 0
        net_params = list(self.net.parameters())
        net_d_params = list(self.net_d.parameters())

        self.net_optimizer = optim.Adam(net_params, self.lr, [self.beta1, self.beta2])
        self.net_optimizer_d = optim.Adam(net_d_params, self.lr_d, [self.beta1, self.beta2])
        print("Second:\n******")
        self.svhn_test()
        self.validate()

        for step in range(self.train_iters):
            # ============ Initialization ============#

            # refresh
            if (step + 1) % (target_per_epoch) == 0:
                target_iter = iter(self.target_loader)
            if (step + 1) % (source_per_epoch) == 0:
                source_iter = iter(self.source_loader)
            # load the data
            source, s_labels = source_iter.next()
            source, s_labels = self.to_var(source), self.to_var(s_labels).long().squeeze()  # must squeeze
            target, t_labels = target_iter.next()
            target_rgb = target
            target, t_labels = self.to_var(target_rgb), self.to_var(t_labels).long().squeeze()

            # ============ train D ============#
            self.reset_grad()

            latent_source, c = self.net(source)
            d = self.net_d(latent_source)
            loss_d_s1 = F.binary_cross_entropy(d, torch.ones_like(d, dtype=torch.float32))
            loss_d_s0 = F.binary_cross_entropy(d, torch.zeros_like(d, dtype=torch.float32))
            loss_c_source = criterion(c, s_labels)

            latent_target, c = self.net(target)
            d = self.net_d(latent_target)
            loss_d_t0 = F.binary_cross_entropy(d, torch.zeros_like(d, dtype=torch.float32))

            loss_p = loss_d_s0
            loss_d = loss_d_s1 + loss_d_t0
            # ============ train pseudo labeling ============#

            chosen_target, pseudo_labels, indexes, imbalance_parameter = pseudo_labeling(target, c)

            if chosen_target is not None:
                loss_c_target = criterion(c[indexes], pseudo_labels)

                latent_target = latent_target[indexes]
                # ============ class loss  ============#
                loss_sep = self.separability_loss(torch.cat((s_labels, pseudo_labels)),
                                                  torch.cat((latent_source, latent_target)),
                                                  imbalance_parameter=imbalance_parameter)
            else:
                loss_c_target = 0
                loss_sep = 0
            loss = self.beta_c * (self.alpha_s * loss_c_source + self.alpha_t * loss_c_target) +                    self.beta_p * loss_p +                    self.beta_sep * loss_sep

            loss.backward(retain_graph=True)
            self.net_optimizer.step()

            loss_d.backward()
            self.net_optimizer_d.step()

            self.reset_grad()

            # ============ Validation ============ #
            if (step + 1) % self.log_step == 0:
                print("max accuracy:", colored(maximum_acc, "green"), "iteration", max_iter)
                _, c_source = self.net(source)
                _, c_target = self.net(target)
                svhn_train = accuracy(s_labels, c_source)*100
                print("SVHN train  accuracy  %.2f;  Target accuracy %.4f" % (
                    svhn_train, accuracy(t_labels, c_target)*100))
                self.svhn_test()
                acc = self.validate()
                if acc > maximum_acc:
                    maximum_acc = acc
                    max_iter = step

                if acc > maxacc:
                    maxacc = acc
                    torch.save(self.net, "./model_c_" + str(step) + '_' + str(acc) + ".pth")
                    torch.save(self.net_d, "./model_d_" + str(step) + '_' + str(acc) + ".pth")
            self.reset_grad()
        # ============ Save the model ============ #
        torch.save(self.net, "./model_c_final.pth")
        torch.save(self.net_d, "./model_d_final.pth")

    def validate(self, ):
        class_correct = [0] * self.num_classes
        class_total = [0.] * self.num_classes
        classes = [str(i) for i in range(self.num_classes)]
        self.net.eval()  # prep model for evaluation

        for data, target in self.target_val_loader:

            # forward pass: compute predicted outputs by passing inputs to the model
            data, target = self.to_var(data), self.to_var(target).long().squeeze()

            data = data.cuda()
            target = target.cuda()

            latent, output = self.net(data)
            _, pred = torch.max(output, 1)
            correct = np.squeeze(pred.eq(target.data.view_as(pred)))
            # calculate test accuracy for each object class
            for i in range(len(target.data)):
                label = target.data[i]
                class_correct[label] += correct[i].item()
                class_total[label] += 1
    
        print("MNIST Test Accuracy (Overall): ", end="")
        print(colored('%2d%% ' % (100. * np.sum(class_correct) / np.sum(class_total)), "red"), end="")
        print("(", end="")
        print(colored(str(int(np.sum(class_correct))), "red"), end=" ")
        print('/%2d)' % (np.sum(class_total)))
        self.net.train()
        return 100. * np.sum(class_correct) / np.sum(class_total)
    
    def svhn_test(self, ):
        class_correct = [0] * self.num_classes
        class_total = [0.] * self.num_classes
        classes = [str(i) for i in range(self.num_classes)]
        self.net.eval()  # prep model for evaluation

        for data, target in self.source_val_loader:

            # forward pass: compute predicted outputs by passing inputs to the model
            data, target = self.to_var(data), self.to_var(target).long().squeeze()

            data = data.cuda()
            target = target.cuda()

            latent, output = self.net(data)
            _, pred = torch.max(output, 1)
            correct = np.squeeze(pred.eq(target.data.view_as(pred)))
            # calculate test accuracy for each object class
            for i in range(len(target.data)):
                label = target.data[i]
                class_correct[label] += correct[i].item()
                class_total[label] += 1
        print("\nSVHN Test Accuracy (Overall): ", end="")
        print(colored('%2d%% ' % (100. * np.sum(class_correct) / np.sum(class_total)), "red"), end="")
        print("(", end="")
        print(colored(str(int(np.sum(class_correct))), "red"), end=" ")
        print('/%2d)' % (np.sum(class_total)))

    def save_model(self):
        torch.save(self.net, os.path.join(self.model_path, 'pre_train.pth'))

    def load_model(self):
        self.net = torch.load(os.path.join(self.model_path, 'pre_train.pth'))


# In[ ]:



import os

from torch.backends import cudnn

def main():
    svhn_loader, svhn_val_loader, mnist_loader, mnist_val_loader = get_loader()
    print("loaded")
    solver = Solver(svhn_loader, svhn_val_loader, mnist_loader, mnist_val_loader)
    cudnn.benchmark = True

    # create directories if not exist
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    if mode == 'train':
        solver.train()


# In[ ]:



main()

