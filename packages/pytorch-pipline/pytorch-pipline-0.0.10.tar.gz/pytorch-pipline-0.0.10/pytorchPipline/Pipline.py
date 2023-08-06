import torch
import numpy as np
from tqdm import tqdm, trange

def TrainModel(dataLoader, model, criterion, optimizer, device=torch.device('cpu'), progressBar = False):
    model = model.to(device)
    criterion = criterion.to(device)
    
    trainLoss = 0
    length = 0
    if progressBar:
        dataLoader = tqdm(dataLoader)
    for batch in dataLoader:
        X, y = batch
        X = X.to(device)
        y = y.to(device)
        outputs = model(X)
        loss = criterion(outputs, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        trainLoss += loss.item()
        length += len(X)
        
    trainLoss /= length
    
    return model, criterion, optimizer, trainLoss
        
def TestModel(dataLoader, model, criterion, device=torch.device('cpu'), progressBar=False):
    model = model.to(device)
    criterion = criterion.to(device)
    
    Loss = 0
    Accuracy = 0
    length = 0
    if progressBar:
        dataLoader = tqdm(dataLoader)
    model.eval()
    for batch in dataLoader:
        X, y = batch
        X = X.to(device)
        y = y.to(device)
        outputs = model(X)
        predicted = torch.argmax(outputs, axis=1)
        loss = criterion(outputs, y)
        
        Loss += loss.item()
        Accuracy += (predicted == y).float().sum()
        length += len(X)
    
    Loss /= length
    Accuracy /= length
    Accuracy = Accuracy.item()
    
    return Loss, Accuracy

def FitModel(num_epochs, trainLoader, testLoader, model, criterion, optimizer, device=torch.device('cpu'), progressBar=False, trainingMetrics=True):
    model = model.to(device)
    criterion = criterion.to(device)
    
    trainingLossGraph = []
    trainingMinLoss = 1e100
    
    trainLossGraph = []
    testLossGraph = []
    
    trainAccuracyGraph = []
    testAccuracyGraph = []
    
    trainMinLoss = 1e100
    testMinLoss = 1e100
    
    trainMaxAccuracy = 0
    testMaxAccuracy = 0
    
    if progressBar:
        epochs = trange(num_epochs)
    else:
        epochs = np.linspace(0, num_epochs-1, num_epochs-1)

    for epoch in epochs:
        model, criterion, optimizer, trainingLoss = TrainModel(trainLoader, model, criterion, optimizer, device=device)
        
        if trainingMetrics:
            assert trainingMetrics == True
            trainLoss, trainAccuracy = TestModel(trainLoader, model, criterion)
            
        testLoss, testAccuracy = TestModel(testLoader, model, criterion)
        
        trainingLossGraph.append(trainingLoss)
        trainingMinLoss = min(trainingMinLoss, trainingLoss)
        
        if trainingMetrics:
            trainLossGraph.append(trainLoss)
            trainMinLoss = min(trainMinLoss, trainLoss)
        
        testLossGraph.append(testLoss)
        testMinLoss = min(testMinLoss, testLoss)
        
        if trainingMetrics:
            trainAccuracyGraph.append(trainAccuracy)
            trainMaxAccuracy = max(trainMaxAccuracy, trainAccuracy)
        
        testAccuracyGraph.append(testAccuracy)
        testMaxAccuracy = max(testMaxAccuracy, testAccuracy)
    
    callback = {
        "trainingLossGraph":trainingLossGraph,
        "trainingMinLoss":trainingMinLoss,
        "trainLossGraph":trainLossGraph,
        "trainMinLoss":trainMinLoss,
        "testLossGraph":testLossGraph,
        "testMinLoss":testMinLoss,
        "trainAccuracyGraph":trainAccuracyGraph,
        "trainMaxAccuracy":trainMaxAccuracy,
        "testAccuracyGraph":testAccuracyGraph,
        "testMaxAccuracy":testMaxAccuracy
        
        }
    return model, callback
    
    
    
    