#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt

def show(img, title = "", col = "gray"):
    plt.title(title)
    plt.imshow(img,cmap=col,vmin=0,vmax=255)
    plt.show()

def histEq(pic, L=256):
    hist = np.histogram(pic, bins=L)
    hist = hist[0]/(pic.shape[0]*pic.shape[1]), hist[1]
    tVals = []
    sums = []
    for i in range(0,L):
        sums += [hist[0][i]]
        val = (L-1)*np.sum(sums)
        tVals += [val]
    tVals = np.round(np.array(tVals))
    pic2 = np.zeros(pic.shape)
    for y,x in np.ndindex(pic.shape):
        pic2[y,x] = tVals[pic[y,x]]
    return pic2

def scale(img):
    img = img - np.min(img)
    return (255/np.max(img)+0.0001)*(img-np.min(img))


#Teilaufgabe-1
moon = io.imread("./moon.png")
show(moon, "Original")
show(histEq(moon), "Angeglichen")


#Teilaufgabe-2
#Zerteile Bild in Subbilder, n gibt an wie oft Achse unterteilt wird
def divide(pic,n):
    #Bereche Seitenlänge eine Unterbildes
    part = pic.shape[0]/n
    #Erzeuge Liste für Unterbilder
    res = []
    #Für jedes Unterbild 0,0 -> n,m
    for n,m in np.ndindex((n,n)):
        #Schneide passenden Teil aus und konkateniere ihn ans Ergebniss
        res += [pic[int(n*part):int((n+1)*part),int(m*part):int((m+1)*part)]]
    return res
#parts = divide(moon,2)
#for i in range(4):
#    show(parts[i],"Stück:"+str(i))
    
def merge(lst,n):
    #Erzeuge Zielarray, welches ursprüngliche größe hat
    res = np.zeros(np.array(lst[0].shape)*n)
    #Finde Breite der Unterbilder
    step = lst[0].shape[0]
    #Erzeuge Index für Unterbilder
    i = 0
    #Für jedes Unterbild
    for n,m in np.ndindex((n,n)):
        #print(i,n*step,(n+1)*step,m*step,(m+1)*step)
        #Fülle passenden Bereich mit Unterbild
        res[n*step:(n+1)*step,m*step:(m+1)*step] = lst[i]
        #Zeige aufs nächste Unterbild
        i += 1
    return res
#show(merge(parts,2),"Zusammengefügt")

def histEqPatches(pic, n):
    #Zerteile Original
    parts = divide(pic,n)
    #Für jedes Unterbild:
    for i in range(len(parts)):
        #Gleiche es aus
        parts[i] = histEq(parts[i])
        #parts[i] = scale(histEq(parts[i]))
        #Gib nach außen Fortschritt in Prozent an, nach jedem 750en Stück
        if i%750 == 0 and not(i == 0):
            print(str(np.round((i+1)/len(parts)*100,2))+"%")
    #Füge Original wieder zusammen
    res = merge(parts,n)
    return res

show(histEqPatches(moon,4), "4x4")
#Man erkennt eigentlich weniger, die Transformationen waren zu divers


#Teilaufgabe-3
show(histEqPatches(moon,8), "8x8")
show(histEqPatches(moon,16), "16x16")
print("Berechne 32x32 Patches...")
show(histEqPatches(moon,32), "32x32")
print("Berechne 64x64 Patches...")
show(histEqPatches(moon,64), "64x64")
print("1Berechne 28x128 Patches...")
show(histEqPatches(moon,128), "128x128")

#Das Ergebniss wird zuerst immer schlimmer
#Meiner Vermutung nach, da wir immer kleinere 
#Bereiche betrachten und somit die Vorhersagen auch nurnoch für immer kleiner 
#werdende Bereiche gedacht sind.
#Somit sind die Vorhersagen zwar lokal immer besser aber global irrelevant.
#Bei winzigen patches erkennt man aber wieder etwas mehr.
#Außerdem bleiben Extreme Übergänge besser erhalten als der Rest.