#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import skimage.color as col
import skimage.filters as filt
import skimage.segmentation as seg
import matplotlib.pyplot as plt

#Alter Kram
def show(img,title="",col="gray",vmin=0,vmax=255):
    plt.title(title)
    plt.imshow(img,cmap=col)
    plt.show()
def reshape(img,max):
    #Untere Grenze auf 0
    img = img-np.min(img)
    #Obere Grenze auf 1
    img = img/np.max(img)
    #Obere Grenze auf max
    return img*max



#Aufgabenteil-1
adr = ["flugzeuge/000700569067.jpg",
       "flugzeuge/001200774065.jpg",
       "flugzeuge/001500782132.jpg",
       "flugzeuge/001900712417.jpg"]
n = len(adr)
cols = adr
for i in range(n): #Lade alle Bilder ins pics-Array
    cols[i] = io.imread(adr[i])
pics = np.array(cols,copy=True,dtype=object)
cols = np.array(cols,copy=True,dtype=object)

for i in range(n): #Farbtransformation
    pics[i] = reshape(col.rgb2gray(pics[i]),255)
#showAll(pics, "Flugzeug") #Zeige alle Bilder an

#Gib Histogramm aus
plt.title("Kumultatives Histogramm")
plt.xlabel("Pixelwert")
plt.ylabel("Anzahl")
for i in range(n):
    plt.hist(pics[i].flatten(),bins=256)
plt.show()
#Am meisten liegt unter 120
thres = 120

#Berechne die Labels
labels = np.array(pics,copy=True,dtype=object)
for i in range(n):
    labels[i] = labels[i]>thres

#Berechne Bilder mit Grenzen dazu
marked = np.array(cols,copy=True,dtype=object)
for i in range(n):
    marked[i] = seg.mark_boundaries(cols[i],
                                    labels[i],
                                    mode="thick")

#zeige alle Bilder+Grenzen an
for i in range(n):
        show(marked[i],"Händ. Grenze bei "+str(thres))
        show(labels[i],"Labels",vmax=1)



#Aufgabenteil-2
#Berechne die Otsu's
otsus = np.zeros((len(adr),1),dtype=float)
for i in range(n):
    otsus[i] = filt.threshold_otsu(pics[i])

#Berechne die Labels
labels2 = np.array(labels,copy=True,dtype=object)
for i in range(n):
    labels2[i] = pics[i]>otsus[i]

#Berechne die Bilder mit Grenzen
marked2 = np.array(pics,copy=True,dtype=object)
for i in range(n):
    marked2[i] = seg.mark_boundaries(cols[i],
                                     labels2[i],
                                     mode="thick")

#zeige alle Bilder+Grenzen an
for i in range(n):
        show(marked2[i],"Otsu-Grenze bei "+str(otsus[i][0]))
        show(labels2[i],"Labels",vmax=1)
#Scheinen sogar schlechter geworden zu sein, enthalten nun weniger vom Flieger!
#Nur beim vierten Bild scheinen die Labels besser geworden zu sein



#Aufgabenteil-3
def blueness(pic):
    res = pic[:,:,2]-pic[:,:,1]/2-pic[:,:,0]/2
    return reshape(res,255)

#Berechne Blauheiten
blues = np.array(pics, copy=True,dtype=object)
for i in range(n):
    blues[i] = blueness(cols[i])

#Berechne die Otsu's
otsus2 = np.zeros((len(adr),1),dtype=float)
for i in range(n):
    otsus2[i] = filt.threshold_otsu(blues[i])

#Berechne die Labels
labels3 = np.array(labels2,copy=True,dtype=object)
for i in range(n):
    labels3[i] = blues[i]>otsus2[i]

#Berechne Bilder mit Grenzen dazu
marked3 = np.array(blues,copy=True,dtype=object)
for i in range(n):
    marked3[i] = seg.mark_boundaries(cols[i],
                                     labels3[i],
                                     mode="thick")

#zeige alle Bilder+Grenzen an
for i in range(n):
        show(marked3[i],"Blauheits Otsu Grenze bei "+str(otsus2[i][0]))
        show(labels3[i],"Labels",vmax=1)
#Nun scheinen alle Flugzeuge die Labels auszufüllen, bestes Ergebniss!
        
        
        
#Aufgabenteil-4
#Extrahiere Blauheit jedes Farbbildes aus den Ecken
bluenesses = np.zeros(cols.shape[0])
for i in range(n):
    y,x = cols[i].shape[:2] #Bestimme max-Koords
    a = cols[i][0,0]/4 #Hole Eckpunkte
    b = cols[i][0,x-1]/4
    c = cols[i][y-1,0]/4
    d = cols[i][y-1,x-1]/4
    avg = a+b+c+d #Berechne Durchschnitt
    bluenesses[i] = avg[2]-avg[1]/2-avg[0]/2 #Berechne Blauheit

offset=75
labels4 = np.array(pics,copy=True,dtype=object)
for i in range(n): #Erzeuge Labels
    labels4[i] = blues[i] < bluenesses[i]+offset

marked4 = np.array(blues,copy=True,dtype=object)
for i in range(n): #Erzeuge Bilder mit Grenzen
    marked4[i] = seg.mark_boundaries(cols[i],
                                     labels4[i],
                                     mode="thick")

#zeige alle Bilder+Grenzen an
for i in range(n):
        show(marked4[i],"Blauheits Grenze bei "+str(bluenesses[i]+offset))
        show(labels4[i],"Labels",vmax=1)
#Bei Offset 100 erkennt er das erste Flugzeug perfekt, aber das dritte nicht.
#Bei Offset 50 erkennt er das dritte Flugzeug perfekt, aber das vierte nicht.
#Bei Offset 75 erkennt er drei schlecht und das erste nur teilweise.
#Also generell nicht sehr gut für versch. Bilder parallel geeignet!