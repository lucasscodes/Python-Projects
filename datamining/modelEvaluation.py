#pip install torch
#pip install sklearn

import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
torch.manual_seed(0)

wine = load_wine()
data = wine["data"]

target = torch.from_numpy(wine["target"]).type(torch.LongTensor)

#scale the data to mean = 0 and var = 1
scaler = StandardScaler()
scaler.fit(data)
data = torch.from_numpy(scaler.transform(data)).float()

#Because the data is ordered we need to shuffle it
shuffle_seed = torch.randperm(data.shape[0])
data = data[shuffle_seed]
target = target[shuffle_seed]

attribute_count = data.shape[1]
label_count = len(wine["target_names"])

print(wine["DESCR"])

def create_model(hidden_layers = [],input_size = attribute_count, output_size = label_count, 
                 activation = torch.nn.ReLU(),output_activation = torch.nn.Identity()):
    #the list of sizes is usefull to manage the input and output sizes of the layers in our network
    sizes = [input_size] + hidden_layers + [output_size]
    #the list of layers will be combined by using nn.Sequential to easily create a feed forward network
    #from a list of layers and activation functions
    layers = []
    
    for i in range(len(sizes)-1):
        #choose the inner activation function for all layers except the last one
        act = activation if i < len(sizes) -2 else output_activation
        #concatenate a Linear layer and the activation function with our layer list
        layers+= [torch.nn.Linear(sizes[i],sizes[i+1]),act]
    #create the neural network from our layer list
    return torch.nn.Sequential(*layers)

def trainModel(model, data, target, epochs, lr = 0.01, batchsize = 20, shuffle = False):
    #How to calculate the Loss (here we use crossentropy) 
    criterion = torch.nn.CrossEntropyLoss()
    
    #The Optimization method for the weights Adam or Stochastic Gradient Descent (SGD) are feasible
    optimizer = torch.optim.Adam(model.parameters(),lr=lr)
    #Loop n times over the Dataset
    for epoch in range(epochs):
        #It may be helpful to shuffle your data every epoch, we don't do it here for reproducibility reasons
        if shuffle:
            seed = torch.randperm(data.shape[0])
            data = data[seed]
            target = target[seed]
        for index in range(0,len(data),batchsize):
            #create the batch
            batch_last = index + batchsize
            data_batch = data[index: batch_last] if batch_last < data.shape[0] else data[index: -1]
            target_batch = target[index: batch_last] if batch_last < target.shape[0] else target[index: -1]
            
            #forward pass
            #calculate the outputs
            scores = model(data_batch)
            #calculate the loss
            loss = criterion(scores, target_batch)
            #backpropagation
            #The gradient has to be set to zero before calculating the new gradients
            optimizer.zero_grad()
            #propagate the loss backwards through the network
            loss.backward()
            #update the weights
            optimizer.step()
    #return the trained model       
    return model
    

def predict(data,model):
    #if a single datapoint is given we have to unsqueeze it to handle more than one datapoint aswell
    if(len(data.shape)) == 1:
        data = data.unsqueeze(0)
    #find the output of our model that has the largest value and use it as our prediction
    #(torch.tensor.max() returns the largest value as the first return value and its index as the scond return value)
    _, prediction = model(data).max(1)
    return prediction

def calculate_accuracy(data, target, model):
    num_samples = data.shape[0]
    #switch to evaluation mode
    model.eval()
    with torch.no_grad():
        #generate the predictions for the data from our model
        prediction = predict(data,model)
        #sum up correct predictions (True = 1)
        num_correct = (prediction == target).sum()
        #calculate accuracy (proportion of correct predictions)
        return num_correct/num_samples

model = create_model([10])
model = trainModel(model, data, target, 50, lr = 0.01)
accuracy = calculate_accuracy(data,target, model)
print(f"Accuracy on training set: {accuracy*100:.2f} %")

def kfold_crossvalidation(k, data, target, hidden = [10], epochs  = 50, lr = 0.01):
    accuracies = torch.zeros([k, 1], dtype=torch.float32)
    #Für jedes der k-Sets
    for i in range(k):
        print("Iteration:",i+1, "von", k)
        #Nimm jedes k-te als Testdaten
        test = data[i::k,:]
        testTar = target[i::k]
        #Nimm jedes k+1-te als erste Trainingsdaten
        train = data[i+1::k,:]
        trainTar = target[i+1::k]
        #Füge alle anderen auch in die Trainingsdaten ein
        for j in range(2,k):
            train = torch.cat((train,data[i+j::k,:]),0)
            trainTar = torch.cat((trainTar, target[i+j::k]),0)
        #print(data.shape, test.shape, train.shape) #[178,13]=[18,13]+[160,13]
        #print(target.shape, testTar.shape, trainTar.shape) #[178]=[18]+[160]
        model = create_model(hidden)
        model = trainModel(model, train, trainTar, 50, lr = 0.01)
        accuracy = calculate_accuracy(test, testTar, model)
        accuracies[i] = accuracy*100.0
        #print(f"Accuracy on training set: {accuracy*100:.2f} %")
    #print(accuracies)
    avg = torch.mean(accuracies)
    #print(avg)
    return (accuracies, avg)

#print(data.shape)
#print(torch.cat((data,data),0).shape)

torch.manual_seed(0)
print(kfold_crossvalidation(10, data, target, [10], 10, 0.01))

def confusion_matrix(data,target,model):
    #Bestimme Anzahl der Klassen m
    uniq = torch.unique(target)
    #print("Uniques",uniq)
    m = uniq.shape[0]
    #Erzeuge Zielvariable
    confusion_matrix = torch.zeros([m, m], dtype=torch.uint8)
    #Berechne Vorhersagen
    pred = predict(data, model)
    #Lösche alle falschen
    right = torch.where(target == pred, pred, -123456)
    #Lösche alle richtigen
    wrong = torch.where(target != pred, pred, -123456)
    #Füge Vorhersagen und target in Zielvariable ein
    for y in range(m):
        for x in range(m):
            #Berechne wie oft richtig vorhergesagt wurde
            if y == x:
                confusion_matrix[y,x] = torch.sum(torch.where(right == y, 1, 0))
            #Berechne wie oft falsch vorhergesagt wurde
            else:
                #Lösche alle, die nicht fälschlicherweise y haben
                where = torch.where(wrong == y, True, False)
                #Lösche alle, die nicht x hätten sein sollen
                where2 = torch.where(target == x, True, False)
                #Per AND, bestimme welche Zahlen y waren, aber x sein sollten
                confusion_matrix[y,x] = torch.sum(torch.logical_and(where, where2))
    return confusion_matrix

torch.manual_seed(0)

training_data = data[0:120]
training_target = target[0:120]

test_data = data[120:-1]
test_target = target[120:-1]

model = create_model([10])
model = trainModel(model, training_data, training_target, 10, lr = 0.01)

print(confusion_matrix(test_data,test_target,model))

"""Es sind nur zwei Fehler aufgetreten, es wurden 2Sätze in Klasse-0 eingeordnet, 
   welche eigentlich in Klasse-1 gehörten. Dies waren predicted[15] & predicted[25]"""
pred = predict(test_data, model)
print("Vorhergesagt:",pred[:])
print("Erwartet:",test_target[:])
print("Gleich:",pred.eq(test_target))



