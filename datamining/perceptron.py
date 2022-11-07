#https://en.wikipedia.org/wiki/Multilayer_perceptron

import numpy as np
import matplotlib.pyplot as plt

x = np.array([[1,1,1], [1,1,0], [1,0,1], [1,0,0]])
#Four Set's, [BIAS=AlwaysTrue, Binary2, Binary1]

t = np.array([1,0,0,0])
#Four Boolean's [Set1Target, Set2Target, Set3Target, Set4Target]

def inner_activation(activations, weights):
    inner_activation = np.sum(activations * weights, axis=1)
    return inner_activation
print(x, np.array([3.0,-3.0,-2.0]))
print(inner_activation(x, np.array([3.0,-3.0,-2.0])))

def g(activations, thresholds=0):
    #Falls nur ein Grenzwert angegeben wurde, 
    #nimm ihn für alle Eingaben an
    if type(thresholds) == int:
        thresholds = np.full(activations.size, thresholds)
    return np.greater_equal(activations, thresholds).astype(int)
print(g(np.array([-1,0])))
print(g(np.array([-1,0,1]),np.array([-1,0,1])))
print(g(np.array([-1,0,1]),np.array([-.9,.1,1.9])))

#Erzeuge Werte im offenen Intervall (-1,1)
values = (np.random.random(150)*2)-1
plt.scatter(values, g(values), color="black")
plt.show()

#FORWARD
def forward_pass(activations, weights, thresholds=0):
    return g(inner_activation(activations, weights), thresholds)
print("inputs", x, "weights", np.array([3.0,-3.0,-2.0]))
print("innerAct", inner_activation(x, np.array([3.0,-3.0,-2.0])))
print("output", forward_pass(x,np.array([3.0,-3.0,-2.0])))

#BACKWARD Rate is the propagation hyperparameter
def updateSingle(weights, teachers, inputs, outputs, rate=0.01):
    #w2 = w + rate*(t-y)*x
    weights = weights + rate*(teachers-outputs)*inputs
    return weights
print(updateSingle(np.array([0,0,0,0]),np.array([-1,1,-1,1]),np.array([0,0,1,1]),np.array([1,1,1,1]),0.3))
print("Entspricht Berechnungen @ Lecture09Page36!")

def update(weights, teacherSet, inputSet, outputSet, rate=0.01):
    for i in range(teacherSet.shape[0]):
        weights = updateSingle(weights, teacherSet[i], inputSet[i], outputSet[i], rate)
    return weights
print(update(np.array([0,0,0,0]), #weights
             np.array([[1,1,1,1], #teachers
                       [-1,1,-1,1],
                       [1,-1,1,-1]]), 
             np.array([[0,0,0,0], #inputs
                       [0,0,1,1],
                       [1,1,0,0]]), 
             np.array([[1,1,1,1],  #outputs
                       [1,1,1,1],
                       [1,1,1,1]]),
             0.3)) #rate
                       
w = np.array([3.0,-3.0,-2.0])

def training(weights, inputs, teachers, rate=0.01):
    for i in range(18):
        for j in range(25):
            outputs = forward_pass(inputs, weights)
            weights = update(weights, teachers, inputs, outputs, rate)
        print(weights)
    print("done!")
    return weights
print(w)
w = training(w,x,t)
print(w)

#Errorfunction
def error(teachers, predicts):
    res =  .5*np.sum((teachers - predicts)**2)
    return res
print(.5*np.sum((np.array([3,3,3])-np.array([0,1,2]))**2))
print(error(np.array([1,2,3]),np.array([1,2,4])))

# getting the prediction error for the whole dataset
preds = forward_pass(x,w)
print(error(t,preds))

def AND(a,b,log=False):
    #Ausgabenliste
    preds = forward_pass(x,w) #[1,0,0,0]
    #Eingabenliste
    teachers = x[:,1:] #[[1, 1],[1, 0],[0, 1],[0, 0]]
    bits = np.equal(teachers, np.array([a, b]))
    if log:
        print("bits:", bits)
    equal = np.bitwise_and(bits[:,0],bits[:,1])
    if log:
        print("equal:", equal)
    pos = np.where(equal == True)[0][0]
    if log:
        print("pos:", pos)
        print("LogEnds!")
    return preds[pos]

print(AND(0,0,log=True))
print(AND(0,1))
print(AND(1,0))
print(AND(1,1))

#Lustigerweise benutzt ich nun das np.bit_and um die Position meines AND-Results zu berechnen.

