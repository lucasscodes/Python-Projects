#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt

tv = ski.imread("./tv.png")

def show(img, title = ""):
    plt.title(title)
    plt.imshow(img,cmap="gray",vmin=np.min(img),vmax=np.max(img))
    plt.show()
    

#Aufgabe 1
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

def scaleNN(scale, img):
    #Erfasse Format
    shape = np.array(img.shape)
    #Skaliere es hoch und Runde
    shape = np.round(shape * scale)
    #Forme floats zu ints um
    shape = shape.astype(int)
    #Erzeuge Zielmatrix
    res = np.zeros(shape)
    #Gehe über Zielbild
    for y in range(shape[0]):
        for x in range(shape[1]):
            #Berechne für jeden Pixel nächsten Nachbarn
            #Dafür zurückrechnen ins Shape vom Original
            res[y,x] = nearestN(x/scale, y/scale, img)
    return res


#Aufgabe 2
show(tv, "unbearbeitet")
show(scaleNN(2.0,tv), "verdoppelt")
#In meinem Beispiel scheinen sogar eher Informationen verloren zu gehen.
#Dies ist auch unter Retrogamern bekannt, diese benutzen lieber alte originale
#Hardware und sehen die Pixel scharf, als sich mit Upscales zufrieden zu geben.
#Außerdem bräuchte man mehrere (ähnliche & unscharfe) Bilder, damit man 
#aus denen wieder ein schärferes Bild gewinnen kann.

#Aufgabe 3
show(scaleNN(2.0,scaleNN(0.5, tv)), "halbiert und verdoppelt")
#Dieses Bild hat beim Downscaling Informationen für immer verloren,
#der Upscale wird diese Informationen aus keiner wieder Quelle gewinnen können.
#=> Also bleibt nach Scale's immer nur die Information aus dem kleinsten Scale.

#ZUSATZAUFGABE NICHT WIE GEFORDERT HIER, SONDERN IN VIERTER DATEI!!!