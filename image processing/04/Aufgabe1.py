#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt

town = ski.imread("./bildverbesserung/bild1.png")
water = ski.imread("./bildverbesserung/bild2.png")
land = ski.imread("./bildverbesserung/bild3.png")

def scale(img):
    img = img - np.min(img)
    img = (255/np.max(img))*(img-np.min(img))
    return img

def show(img, title = ""):
    plt.title(title)
    plt.imshow(img,cmap="gray",vmin=np.min(img),vmax=np.max(img))
    plt.show()
    
    
#1.Verbessert den Sichtbarkeit des Gebäudes unten links in Abbildung 1a 
#  und ermittelt, wie viele Fenster die vordere Front des Gebäudes im obersten 
#  Stockwerk hat. Der Bildbereich ist in Abbildung 1a grob markiert.

def myClip(img):
    res = np.maximum(img,0)
    res = np.minimum(res,255)
    return res

def powerLaw(img, c=1, y=1):
    res = np.power(img, y)
    res = res * c
    res = myClip(res)
    return res

#Kontrastverschiebung
show(town, "Unbearbeitet")
town2 = powerLaw(town, 1.0, 1.75)
show(town2, "powerLaw c=1.0 y=1.75")
#=> Das oberste Stockwerk hat 6 Fenster, 3 kleine und 3 doppelte Fenster


#2.Sorgt dafür, dass sich die Insekten und die Wasserpflanzen in 
#  Abbildung 1b besser vom milchigen Wasser abheben.

def cut(img, min=0, max=255):
    res = np.minimum(img, max)
    res = np.maximum(res, min)
    return res

#Unnötigen Farbbereich löschen
show(water, "Unbearbeitet")
water2 = cut(water,min=140,max=190)
show(water2,"Wertebereich 140-190")


#3.Verändert das Bild in Abbildung 1c so, dass in etwa der Bereich 
#  des Flusses (von oben rechts nach unten links) schwarz ist und 
#  der Rest des Bildes seine Graufärbung behält. Einzelne andere 
#  Pixel können ebenfalls verfärbt werden. Kein perfektes Ergebniss!
    
def negate(img):
    res = np.multiply(img, np.full(img.shape, -1))
    return scale(res)

#Maske * Original
show(land, "Unbearbeitet")
mask = negate(cut(land,min=160,max=170))
#show(mask)
land2 = scale(np.multiply(land, mask))
show(land2, "Water BlackMasked")