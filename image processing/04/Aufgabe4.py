#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt
import math

tv = ski.imread("./tv.png")

def show(img, title = ""):
    plt.title(title)
    plt.imshow(img,cmap="gray",vmin=np.min(img),vmax=np.max(img))
    plt.show()
    

#Aufgabe 1
def bilinearI(x, y, img):
    xmax = img.shape[1]-1
    ymax = img.shape[0]-1
    #Berechne beie x-Koordinaten und den Anteil von der unteren zur mittleren
    xleft = max(0,math.floor(x))
    xright = min(xmax, math.ceil(x))
    xpart = x-math.floor(x)
    #Berechne beie y-Koordinaten und den Anteil von der unteren zur mittleren
    yhigh = max(0,math.floor(y))
    ylow = min(ymax, math.ceil(y))
    ypart = y-math.floor(y)
    #Berechne für oberen Pixel gewichteten Mittelwert
    xTop = img[yhigh,xleft]*xpart + img[yhigh,xright]*(1-xpart)
    #Berechne für unteren Pixel gewichteten Mittelwert
    xBot = img[ylow,xleft]*xpart + img[ylow,xright]*(1-xpart)
    #Füge Mittelwerte zu gewichteter Summe zusammen
    middle = xTop*ypart + xBot*(1-ypart)
    #Konvertiere Floats
    return middle.astype(int)

def nearestN(x, y, img):
    #Runde zum nächsten x-Wert
    x = np.round(x).astype(int)
    #Verhindere OutOfBounds(einen Schritt zu weit)
    x = min(x,img.shape[1]-1)
    #Runde zum nächsten y-Wert
    y = np.round(y).astype(int)
    #Verhindere OutOfBounds(einen Schritt zu weit)
    y = min(y,img.shape[0]-1)
    #Gib den Nachbarn aus
    return img[y,x]

def scale(scale, img, bilinear):
    #Erfasse Format
    shape = np.array(img.shape)
    #Skaliere es hoch und Runde
    shape = np.round(shape * scale)
    #Forme floats zu ints um
    shape = shape.astype(int)
    #Erzeuge Zielmatrix
    res = np.zeros(shape)
    #Gehe über Zielbild
    if bilinear:
        for y in range(shape[0]):
            for x in range(shape[1]):
                res[y,x] = bilinearI(x/scale, y/scale, img)
    else:
        for y in range(shape[0]):
            for x in range(shape[1]):
                res[y,x] = nearestN(x/scale, y/scale, img)
    return res


#Aufgabe 2
show(tv, "unbearbeitet")
show(scale(0.8,tv,False),"downscale 80% NearestNeighbour")
show(scale(0.8,tv,True),"downscale 80% BilinearInterpolation")
#NearestNeighbour-Downscale hat Lücken in der Antenne
#BilinearInterpolation-Downscale ist Lückenlos aber etwas verwaschen
show(tv, "unbearbeitet")
show(scale(1.5,tv,False),"Upscale 150% NearestNeighbour")
show(scale(1.5,tv,True),"Upscale 150% BilinearInterpolation")
#NearestNeighbour-Upscale ist sehr scharf, aber starke Aliasing-Effekte
#BilinearInterpolation-Upscale ist weniger aliased, dafür aber stark verwaschen
