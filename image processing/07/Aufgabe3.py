#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

#Aufgabenteil-1
ls = np.array([1,2,5,9,8,3,6,7,9,9])
plt.plot(ls)
plt.title("Liste")
plt.show()


#Aufgabenteil-2
kern = np.array([1,1,1,1,1])
kern = kern/np.sum(kern)
#Berechnet ein mit n gepaddetes 1D-Bild
def pad(img, krn, n):
    pad = np.full(int(krn.shape[0]/2),n)
    return np.concatenate((pad,img,pad))
#Berechnet eine Faltung mit Kern, 1D-Bild und Wert zum Padding
def conv(img, krn, n):
    imgPad = pad(img, krn, n)
    res = np.zeros(img.shape)
    for x in range(img.shape[0]):
        res[x] = np.sum(krn[::-1]*imgPad[x:x+len(krn)])
    return res

plt.plot(ls)
plt.plot(conv(ls,kern,0))
plt.title("Original und Gefaltet, 0-Padding")
plt.show()
#Durch das Zeropadding zeigt der Graph an den 
#vom Padding betroffenen Werten eher nach unten!


#Aufgabenteil-3
plt.plot(ls)
plt.plot(conv(ls,kern,9))
plt.title("Original und Gefaltet, 9-Padding")
plt.show()
#Nun sind die äußeren beiden vom Padding betroffenen Werte 
#eher nach oben gezogen


#Aufgabenteil-4
#Berechnet ein replicated'tes 1D-Bild, repBreite=n
def rep(img,n):
    front = np.full(n,img[0])
    back = np.full(n,img[len(img)-1])
    return np.concatenate((front,img,back))
#Berechnet eine Faltung mit Kern, 1D-Bild
def conv2(img, krn):
    n = int(len(krn)/2)
    imgPad = rep(img, n)
    res = np.zeros(img.shape)
    for x in range(img.shape[0]):
        res[x] = np.sum(krn[::-1]*imgPad[x:x+len(krn)])
    return res

plt.plot(ls)
plt.plot(conv2(ls,kern))
plt.title("Original und Gefaltet, replicated-Padding")
plt.show()
#Hier werden die vom padding betroffenen Werte nach oben und unten gezogen
#Allgemein werden diese immer Richtung Anfang/Ende des G´raphen gezogen


#Aufgabenteil-5
def mir(img,n):
    front = img[0:n:][::-1]
    back = img[len(img)-n:len(img):][::-1]
    return np.concatenate((front,img,back))
#Berechnet eine Faltung mit Kern, 1D-Bild
def conv3(img, krn):
    n = int(len(krn)/2)
    imgPad = mir(img, n)
    res = np.zeros(img.shape)
    for x in range(img.shape[0]):
        res[x] = np.sum(krn[::-1]*imgPad[x:x+len(krn)])
    return res

plt.plot(ls)
plt.plot(conv3(ls,kern))
plt.title("Original und Gefaltet, mirror-Padding")
plt.show()
#Entspricht eigentlich dem replicated-Padding


#Aufgabenteil-6
def ref(img,n):
    front = img[1:n+1:][::-1]
    back = img[len(img)-(n+1):len(img)-1:][::-1]
    return np.concatenate((front,img,back))
#Berechnet eine Faltung mit Kern, 1D-Bild
def conv4(img, krn):
    n = int(len(krn)/2)
    imgPad = ref(img, n)
    res = np.zeros(img.shape)
    for x in range(img.shape[0]):
        res[x] = np.sum(krn[::-1]*imgPad[x:x+len(krn)])
    return res

plt.plot(ls)
plt.plot(conv4(ls,kern))
plt.title("Original und Gefaltet, reflected-Padding")
plt.show()
#Entspricht eigentlich dem mirror-Padding, 
#nur das jetzt der erste/letzte Wert weniger zählen