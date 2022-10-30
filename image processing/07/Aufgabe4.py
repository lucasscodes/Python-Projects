#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import skimage.filters as filters
import skimage.segmentation as seg
import matplotlib.pyplot as plt

def show(img, title = "", col = "gray", vmin=0, vmax=255):
    plt.title(title)
    plt.imshow(img,cmap=col,vmin=vmin,vmax=vmax)
    plt.show()


#Aufgabenteil-1
ballon = io.imread("./ballon.png")
show(ballon, "Original")
#Rasen, Segmente eines bunten Ballon's, Mensch, farbige Schatten
ballone = []
for i in [10,20,30,40,50]:
    ballone += [filters.gaussian(ballon, i, multichannel=True)]
show(ballone[0],"Sigma=10")
#Rasen, unscharfe Segmente, Punkt statt Mensch, farbige Schatten
show(ballone[1],"Sigma=20")
#Boden, unscharfer Wirbel
show(ballone[2],"Sigma=30")
#Boden, unschärferer Wirbel
show(ballone[3],"Sigma=40")
#-|-
show(ballone[4],"Sigma=50")
#-|-


#Aufgabenteil-2
glacier = io.imread("./gletscher.png")
show(glacier, "Original")

def trin(img, air=200, stone=130):
    res = np.array(img,copy=True,dtype=int)
    res = np.where(res>air-1,255,res)
    res = np.where(res<stone+1,0,res)
    res = np.where(np.logical_and(res<air, res>stone),127,res)
    return res
    
show(trin(glacier), "Trinarisiert")

print("Nun kommen nurnoch folgende Werte vor:",np.unique(trin(glacier)))

#Problematisch sind Überlappungen der Wertebereiche.
#Man wird immer in einem Bereich einen Wert eines anderen Bereiches vorfinden können.


#Aufgabenteil-3
def gauss(img, var=1.0):
    return filters.gaussian(img, var)

show(gauss(glacier, var=13.0),"Gaussches Rauschen var=13.0´",vmax=1)
trin = trin(gauss(glacier, var=13.0)*255,air=187,stone=110)
show(trin,"Gaussches Rauschen Trinarisiert")

#Nun gibt es gleichmäßigere Flächen und somit auch eine gleichmäßigere 
#Einteilung in die 3 Werte 0, 127 & 255.

#Der letzte bestehende Fehler ist nun ein Stein links unten im Fluss
#und etwas Fluss zwischen Stein und Himmel.


#Aufgabenteil-4
show(seg.mark_boundaries(glacier, trin), "Grenzen der Trinarisierung")
#Die Grenzen sind leider etwas veschoben, aber enthalten dafür sehr wenige Störungen
#Erhaltene Störungen sind die Grenze zwischen Himmel und Stein, 
#ein etwas verschobennes Ufer und ein "Stein" im Fluss

#