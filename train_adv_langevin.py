#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from __future__ import print_function
#%matplotlib inline
import argparse
import os
import random
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.utils.data
import torchvision.utils as vutils
import matplotlib.animation as animation

from IPython.display import HTML

from MNISTDataset import *
from mnist_net import mnist_net

epochs = 10
epsilon = 0.1
n_lan = 100
n_iter = 200

#mnist_train = datasets.MNIST("../data", train=True, download=True, transform=transforms.ToTensor())
#mnist_test = datasets.MNIST("../data", train=False, download=True, transform=transforms.ToTensor())
#train_loader = DataLoader(mnist_train, batch_size = 100, shuffle=True)
#test_loader = DataLoader(mnist_test, batch_size = 100, shuffle=False)


path = "/content/sample_data/mnist_train_small.csv"
mnist_train_csv = pd.read_csv(path)

path = "/content/sample_data/mnist_test.csv"
mnist_test_csv = pd.read_csv(path)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

train_labels = mnist_train_csv.iloc[:, 0]
train_images = mnist_train_csv.iloc[:, 1:]

train_labels_avd = mnist_train_csv.iloc[:, 0]
train_images_avd = mnist_train_csv.iloc[:, 1:]

test_labels = mnist_test_csv.iloc[:, 0]
test_images = mnist_test_csv.iloc[:, 1:]

transform = transforms.Compose(
    [transforms.ToPILImage(),
     transforms.ToTensor(),
     transforms.Normalize((0.5, ), (0.5, ))
])

#Datasets

train_data = MNISTDataset(train_images, train_labels, transform)
test_data = MNISTDataset(test_images, test_labels, transform)
# dataloaders
trainloader = DataLoader(train_data, batch_size=100, shuffle=True)
testloader = DataLoader(test_data, batch_size=100, shuffle=True)

train_data_adv = MNISTDataset(train_images_adv, train_labels_adv, transform)
trainloader_adv = DataLoader(train_data_adv, batch_size=100, shuffle=True)


torch.manual_seed(0)   

model_cnn = model_mnist()

if torch.cuda.is_available():
    model_cnn.cuda()

def epoch_adversarial_lan(train_data_adv, model, n_lan, epsilon, n_iter, opt=None, **kwargs):
    """Adversarial training/evaluation epoch over the dataset"""
    total_loss, total_err = 0.,0.
    for  i in range(n_iter):
        X_old, y, idx = train_data_adv.get_sample(100)
        X_new,samples_lan,y_lan = Langevin(model,X_old,y,n_lan, epsilon, step=0.1)
        samples_lan  = samples_lan.to(device, dtype=torch.float)
        y_lan = y_lan.long()
        yp = model(samples_lan)
        loss = nn.CrossEntropyLoss()(yp,y_lan)

        total_err += (yp.max(dim=1)[1] != y_lan).sum().item()
        total_loss += loss.item() / (X_old.shape[0] * n_lan)
        print(total_err,total_loss)
        if opt:
            opt.zero_grad()
            loss.backward()
            opt.step()
        X_new = X_new.reshape(100,784)
        train_data_adv.update(pd.DataFrame(X_new).values, idx)
    return total_err / (train_data_adv.__len__()*n_lan ), total_loss / train_data_adv.__len__(), train_data_adv 

def train(epoch):
    opt = optim.SGD(model_cnn.parameters(), lr=0.01)
    model_cnn.cuda()
    for t in range(epoch):
        train_err, train_loss, train_data_adv = epoch_adversarial_lan(train_data_adv, model_cnn, n_lan ,epsilon, n_iter, opt)
    if t == 4:
        for param_group in opt.param_groups:
               param_group["lr"] = 1e-2
    print(*("{:.6f}".format(i) for i in (train_err, test_err, adv_err)), sep="\t")
    torch.save(model_cnn.state_dict(), "model_cnn.pt")
    
def plot(images_values, size):
    images = np.reshape(images,(size,28,28))
    plt.figure(figsize=(10,10))
    for i in range (25):
        plt.subplot(5,5,i+1)
        plt.imshow(train_images[i,:,:])
        plt.axis('off')
    plt.subplots_adjust(wspace=0.0, hspace=0.1) 
    

train(epochs)

if display:
    plot(train_data_adv.X.values)
