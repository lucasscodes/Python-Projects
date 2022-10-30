#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as sk
import time
    
ape = sk.imread("./mandrill.png")

def varCheck(pic):
    return np.var(pic[:,:])

#Teilaufgabe 1
def var1(pic):
    shape = pic.shape
    divisor = shape[0]*shape[1]
    #Berechne Mittelwert
    mySum = 0
    for y in range(shape[0]):
        for x in range(shape[1]):
            mySum += pic[y,x]
    mean = mySum/divisor
    #Berechne Varianz
    mySum = 0
    for y in range(shape[0]):
        for x in range(shape[1]):
            mySum += (pic[y,x] - mean)**2
    var = mySum/divisor
    return var

print("Teilaufgabe 1 funktioniert 6-Stellen hinterm Komma:", (np.round(var1(ape),6) 
                                                              == np.round(varCheck(ape),6)))

#Teilaufgabe 2
def var2(pic):
    shape = pic.shape
    divisor = shape[0] * shape[1]
    #Berechne Mittelwert
    mySum = 0
    for y in range(shape[0]):
        for x in range(shape[1]):
            mySum += pic[y,x]
    mean = mySum/divisor
    #Berechne Varianz
    mySum = 0
    for y in range(shape[0]):
        for x in range(shape[1]):
            mySum += pic[y,x]**2
    var = mySum/divisor
    var = var - mean**2
    return var

print("Teilaufgabe 2 funktioniert:", (var2(ape) == varCheck(ape)))

#Teilaufgabe 3
n = 10
tic = time.time()
res = 0
print("Berechne jew.",n,"Durchläufe...")
for i in range(n-1):
    res = var1(ape)
toc = time.time()
t1 = toc-tic
print("Variante 1:", t1, "Sek")
print(res)
tic = time.time()
for i in range(n-1):
    res = var2(ape)
toc = time.time()
t2 = toc-tic
print("Variante 2:", t2, "Sek")
print(res)
tic = time.time()
for i in range(n-1):
    res = varCheck(ape)
toc = time.time()
print("Variante Numpy:", toc-tic, "Sek")
print(res)
print("Variante 2 war", t1-t2, "Sekunden schneller!")
#Variante2 braucht weniger Zeit
#Abweichung: Nur Var2 entspricht der Numpy Variante
#Erklärung: In Var1 und Var2 wird mean verwendet, dies hat aber einen Rundungsfehler aus einer 2D Summe.
#           Somit wird in einer weiteren 2D-Summe(Var1) jedesmal ein Rundungsfehler aufaddiert.
#           In Var2 wird der Rundungsfehler mit nur einer weiteren Zahl verechnet, mean*mean.
#           Somit haben wir nur 3 * 2D-Rundungsfehler und nicht Y * X * 2D-Rundungsfehler