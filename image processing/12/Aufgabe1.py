#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import skimage.color as col
import skimage.data as dat
import skimage.filters as filt
import skimage.segmentation as seg
import matplotlib.pyplot as plt

#Alter Kram
def show(img,title="",col="gray",vmin=0,vmax=255):
    plt.title(title)
    plt.imshow(img,cmap=col)
    plt.show()


#Aufgabenteil-1
brick = io.imread("brick.png")
thres = filt.threshold_otsu(brick)
binBrick = np.where(brick <= thres, 0, brick)
binBrick = np.where(binBrick > thres, 255, binBrick)
binBrick = binBrick/255
binBrick = np.array(np.where(binBrick==1,0,1),dtype=int)
show(binBrick, "Erzeugte Maske", vmax=1)


#Aufgabenteil-2&3
def labelBricks(img):
    res = np.zeros_like(img) #Ergebnisse
    i = 0 #Gruppenzähler
    for y in range(img.shape[0]):´
        for x in range(img.shape[1]):#Für jeden Pixel
            if img[y,x]==1: #Falls noch unbesuchte Gruppe gefunden wird
                label = seg.flood(img, seed_point=(y,x), tolerance=0) #Erzeuge ganze Gruppe
                img = img-label #Lösche diese aus dem Bild
                label = np.where(label==1,i+1,0) #Setze Gruppenindex ein
                res += label #Füge Gruppe ins Ergebniss ein
                i += 1 #Erhöhe Zähler für nächste Gruppe
    return res
labeled = labelBricks(binBrick)
show(col.label2rgb(labeled,brick,bg_label=-1), "Segmentierung")


#Aufgabenteil-4
binBrick2 = np.zeros_like(binBrick)
for y in range(binBrick.shape[0]):
    for x in range(binBrick.shape[1]):#Für jeden Pixel
        if(y>=2 and y<=binBrick.shape[0]-(1+2) and 
           x>=2 and x<=binBrick.shape[1]-(1+2)): #Falls Nachbarschaft vorhanden ist
            list = []
            for i in [-2,-1,0,1,2]:
                for j in [-2,-1,0,1,2]:
                    list += [binBrick[y+i,x+j]]
            value = np.min(list)
            binBrick2[y,x] = value
labeled = labelBricks(binBrick2)
show(binBrick2, "Abgewandelte Maske")
show(col.label2rgb(labeled,brick,bg_label=-1), "Abgewandelte Segmentierung")
#Jetzt sind die Ziegel wirklich besser getrennt
#Aber es sind Ränder entstanden, welche sie hervorheben
#Dies, da sie nun kleiner dargestellt werden als sie sind, und somit ein Teil hervorschaut