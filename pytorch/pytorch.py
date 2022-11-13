#Fashion MNIST Small Scale Visual Recognition Challenge

import time
import torch
import torch.nn as nn
import torchvision
torch.manual_seed(42)
import matplotlib.pyplot as plt
import numpy as np
#pip install torch torchvision

print(torch.cuda.is_available())
print(torch.cuda.current_device())
print(torch.cuda.device(0))
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))
torch.set_default_tensor_type('torch.cuda.FloatTensor')

# if, for some reason, you are not using a UNIX-based operating system, \
# you might need to adjust the path arguments
trainset = torchvision.datasets.FashionMNIST(root='./data', train=True,
                                        download=True, transform=torchvision.transforms.ToTensor())
testset = torchvision.datasets.FashionMNIST(root='./data', train=False,
                                       download=True, transform=torchvision.transforms.ToTensor())
label_names = {0:"T-shirt/top", 1:"Trouser", 2:"Pullover", 3:"Dress",
               4:"Coat", 5:"Sandal", 6:"Shirt", 7:"Sneaker", 8:"Bag", 
               9:"Ankle boot"}

#type(sample) => tuple
    #Set besteht aus 50.000 Trainigsdaten, jedes ist Tupel
    #Tupel besteht aus einem Tensor (in dem ein weiterer 28x28 Tensor steckt) und einem Int
    #0=Datas(torch)
        #sample[0].shape => torch.Size([1, 28, 28]) 
        #Also Graustufen mit 28x28Pixeln
    #1=Labels(int)
        #sample[1] => 9 (=> Ankle Boot)

anzahl = 0
for i in range(anzahl):
    index = np.round(np.random.rand()*(trainset.__len__()-1))
    sample = trainset.__getitem__(int(index))
    plt.title(label_names[sample[1]])
    plt.imshow(sample[0][0], cmap="gray")
    plt.show()

validation_size = 10000 # set the size of your validation set
trainset, valset = torch.utils.data.random_split(trainset, 
                                                 [len(trainset)-validation_size, validation_size], 
                                                 generator=torch.Generator(device='cuda').manual_seed(1337))

trainloader = torch.utils.data.DataLoader(trainset, batch_size=32,
                                          shuffle=True, generator=torch.Generator(device='cuda').manual_seed(1337))
testloader = torch.utils.data.DataLoader(testset, batch_size=32,
                                         shuffle=False, generator=torch.Generator(device='cuda').manual_seed(1337))
valloader = torch.utils.data.DataLoader(valset, batch_size=32,
                                         shuffle=False, generator=torch.Generator(device='cuda').manual_seed(1337))

model = nn.Sequential(#nn.Flatten(),
                      #nn.Linear(28*28, 20),
                      #nn.Sigmoid(),
                      #nn.Linear(20, 10),
                      #nn.Sigmoid()
                      nn.Flatten(),
                      nn.Linear(28*28, 40*40), #entspricht Inputgröße
                      nn.ReLU(),             #keine vanishing/exploding-Gradients
                      nn.Linear(40*40, 30*30), #Übergang
                      nn.ReLU(),
                      nn.Linear(30*30, 20*20), #Übergang
                      nn.ReLU(),
                      nn.Linear(20*20, 10),     #entspricht Outputgröße
                      nn.Sigmoid()
                      ).to('cuda')
        
learning_rate = 0.3
loss = nn.CrossEntropyLoss().to('cuda')
#optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
epochs = 17

def train(model, dataloader, optimizer, loss):
    epoch_loss = []
    model.train()
    correct = 0
    total = 0
    for img, lbl in dataloader:
        img = img.to('cuda')
        lbl = lbl.to('cuda')
        optimizer.zero_grad()
        out = model(img)
        logits, indices = torch.max(out, 1)
        correct += torch.sum(indices == lbl).item()
        total += len(lbl)
        batch_loss = loss(out, lbl) 
        batch_loss.backward() 
        optimizer.step() 
        epoch_loss.append(batch_loss.item()) 
    return np.mean(epoch_loss), correct/total

def evaluate(model, dataloader):
    model.eval()
    correct = 0
    total = 0
    for img, lbl in dataloader:
        img = img.to('cuda')
        lbl = lbl.to('cuda')
        out = model(img)
        logits, indices = torch.max(out, 1)
        correct += torch.sum(indices == lbl).item()
        total += len(lbl)
    return correct/total

def training(model, tloader=trainloader, vloader=valloader, opt=optimizer, lo=loss):
    #train(model, dataloader, optimizer, loss) => np.mean(epoch_loss), correct/total
    #It takes a model, a dataloader, and optimizer and a loss function, 
    #trains the model for one epoch and returns the mean loss over the epoch as well as the accuracy.
        
    #evaluate(model, dataloader) => correct/total
    #It takes a model and a dataloader and returns the accuracy.
    
    #Dataloader: trainloader, testloader, valloader
    lossAccVal = []
    
    print("Startwert =",evaluate(model, vloader))
    for i in range(epochs):
        start = time.perf_counter()
        lossAcc = train(model, tloader, opt, lo)
        val = evaluate(model, vloader)
        lossAccVal += [lossAcc[0], lossAcc[1], val]
        end = time.perf_counter()
        print("Epoche",i+1,"/",epochs,"=",val,"Time:",end-start,"sec")
    return lossAccVal

lossAccVal = training(model)

loss = np.array(lossAccVal[::3])
acc = np.array(lossAccVal[1::3])
epoch = np.arange(epochs)+1

plt.plot(epoch,loss)
plt.plot(epoch, acc)
plt.title("Training Loss and Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Loss(blue), Acc(yellow)")
plt.show()

val = lossAccVal[2::3]

plt.plot(epoch,val)
plt.title("Validation Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Validation")
plt.show()

test_acc = evaluate(model, testloader)
print("Your model correctly classified", round(test_acc*100,2), 
      "% of all samples.")

#print(testset) => 10.000 Elemente
#Gruppiere neue Testsets
testsets = [[],[],[],[],[],[],[],[],[],[]]
for i in range(10000):    
    testsets[testset[i][1]] += [testset[i]]
    
#Teste Aufteilung
for j in range(10):
    for i in range(len(testsets[j])):
        if(testsets[j][i][1] != j):
            print("Error expected",j,"got",testsets[j][i][1])
        
res = []
for tmpset in testsets:
    tmploader = torch.utils.data.DataLoader(tmpset, batch_size=32,
                                             shuffle=False)
    res += [round(evaluate(model, tmploader)*100,2)]

plt.plot([label_names[k] for k in range(10)],res)
plt.title("Class spec. Test Accuracy's")
plt.xlabel("Classes")
plt.xticks(rotation=-45)
plt.ylabel("Accuracy")
plt.show()