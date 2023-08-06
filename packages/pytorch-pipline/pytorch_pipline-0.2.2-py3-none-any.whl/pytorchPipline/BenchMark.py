import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
import numpy as np
from tqdm import trange
from pytorchPipline.Pipline import TrainModel, TestModel, FitModel
from timeit import default_timer as timer

def BenchMark(epoch=10, batch_size = 256, progressBar=True):
    
    start = timer()
    trainLoader = datasets.MNIST(
        root="./",
        train=True,
        download=True,
        transform=transforms.ToTensor()
        )
    testLoader = datasets.MNIST(
        root="./",
        train=False,
        download=True,
        transform=transforms.ToTensor()
        )
    
    trainLoader = DataLoader(trainLoader, batch_size=batch_size)
    testLoader = DataLoader(testLoader, batch_size=batch_size)
    
    device = torch.device('mps')
    
    class mainConvModel(nn.Module):
    
        def __init__(self):
            super(mainConvModel, self).__init__()
            self.to64conv = nn.Sequential(
                nn.Conv2d(1, 4, (3, 3)),
                nn.ReLU(),
                nn.Conv2d(4, 4, (3, 3)),
                nn.ReLU(),
                nn.Conv2d(4, 16, (3, 3)),
                nn.ReLU(),
                nn.Conv2d(16, 64, (3, 3)),
                nn.ReLU()
            )
            self.conv64 = nn.Sequential(
                nn.Conv2d(64, 64, (3, 3)),
                nn.ReLU()
            )
            self.pool = nn.Sequential(
                nn.AvgPool2d(3, 3)
            )
            self.end = nn.Sequential(
                nn.Conv2d(64, 8, (3, 3)),
                nn.ReLU(),
                nn.Flatten(),
                nn.Linear(288, 25)
            )
        def forward(self, x):
            x = self.to64conv(x)
            x = self.conv64(x)
            x = self.conv64(x)
            x = self.conv64(x)
            x = self.conv64(x)
            x = self.conv64(x)
            x = self.conv64(x)
            x = self.end(x)
            return x
         
    model = mainConvModel()
    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = optim.Adam(model.parameters())
    
    # model, criterion, optimizer, trainLoss, trainAccuracy = TrainModel(trainLoader, model, criterion, optimizer, device=device, progressBar = True)
    
    # testLoss, testAccuracy = TestModel(testLoader, model, criterion, device=device, progressBar=True)
    
    model, callback = FitModel(epoch, trainLoader, testLoader, model, criterion, optimizer, device=device, progressBar=progressBar, trainingMetrics=False)
    time = timer() - start
    return time