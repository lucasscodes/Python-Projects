#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import skimage.filters as filt
import skimage.color as col
import matplotlib.pyplot as plt

#Alter Kram
def show(img, title = "", col = "gray", vmin=0, vmax=255):
    plt.title(title)
    plt.imshow(img,cmap=col,vmin=vmin,vmax=vmax)
    plt.show()
def reshape(img):
    img = img-np.min(img)
    img = img/np.max(img)
    return img*255
def cut(img, min=0, max=255):
    res = np.minimum(img, max)
    res = np.maximum(res, min)
    return reshape(res)
opera = io.imread("./opera.png")
opera2 = filt.gaussian(opera, 2, multichannel=True)
operaB = opera2[:,:,2] - (opera2[:,:,0]+opera2[:,:,1])/2
operaB = reshape(operaB)*2-255
operaB = np.where(operaB<0,0,operaB)
operaBH = filt.sobel_h(operaB)
operaBV = filt.sobel_v(operaB)
operaBE = np.sqrt(np.add(np.power(operaBH,2),
                        np.power(operaBV,2))/2)
operaBE = reshape(operaBE)*2-255
show(operaBE, "Blaue-Kanten", vmin=-255)


#Aufgabenteil-1
#Berechne Gradientenorientierung
degree = np.round(np.degrees(np.arctan(operaBH/(operaBV+1e-10))),2)
show(degree,"Orientierungen n-Stufen", vmin=-90,vmax=90)

degree = np.where(np.logical_and(degree<22.5,-22.5<=degree),0,degree)
degree = np.where(np.logical_and(degree<67.5,22.5<=degree),45,degree)
degree = np.where(np.logical_and(degree<-22.5,-67.5<=degree),-45,degree)
degree = np.where(degree>=67.5,90,degree)
degree = np.where(degree<-67.5,90,degree)
show(degree,"Orientierungen 4-Stufen", vmin=-90,vmax=90)

res = np.zeros(operaBE.shape)


#Aufgabenteil-2&3
#show(degree[100:140,350:400],"Deg Ausschnitt [100:140,350:400]", vmin=-45,vmax=90)
#show(operaBE[100:140,350:400],"Int Ausschnitt [100:140,350:400]", vmin=-255)
#print("Schwarz hat Wert:",operaBE[120,380])
#print("Schwarz hat Orientierung:",degree[120,380])

#Hole Koordinaten von relevanten Nachbarn, wenn im Bild vorhanden
def getNeighs(degs,y,x):
    #Erzeuge Ergebnissvariable
    res = []
    #Hole Bildhöhe und Breite
    height, width = degs.shape
    #Falls Orientierung, suche passenden 2 Nachbarn raus
    if(degs[y,x] == -45):
        #Falls Werte nicht zu klein/groß werden
        if(y+1<height and x-1>=0):
            #füge Koordinaten hinzu
            res += [y+1,x-1]
        if(y-1>=0 and x+1<width):
            res += [y-1,x+1]
    if(degs[y,x] == 0):
        if(x-1>=0):
            res += [y,x-1]
        if(x+1<width):
            res += [y,x+1]
    if(degs[y,x] == 45):
        if(x-1>=0 and y-1>=0):
            res += [y-1,x-1]
        if(y+1<height and x+1<width):
            res += [y+1,x+1]
    if(degs[y,x] == 90):
        if(y-1>=0):
            res += [y-1,x]
        if(y+1<height):
            res += [y+1,x]
    return res
    
#Berechne engere Kanten mit GradientMagnituden, GradientDegree und leerem Bild
def thinner(mags,degs,target):
    #Für jeden Pixel
    for y,x in np.ndindex(target.shape):
        #Hole dir alle echten Nachbarkoordinaten
        neighs = getNeighs(degs, y,x)
        #Erzeuge Liste für die anderen Magnituden
        magnitudes = []
        #Solange ich noch Koordinaten habe
        while len(neighs)>0:
            #Extrahiere zwei Koordinaten und lösche sie
            y2,x2 = neighs[0],neighs[1]
            neighs = neighs[2::]
            #Wenn gleiche Orientierung
            if(degs[y,x] == degs[y2,x2]):
                #Füge Magnitude in Liste ein
                magnitudes += [mags[y2,x2]]
        #print(magnitudes)
        #Wenn akt Magnitude die Größte ist, übernimm Wert
        if(len(magnitudes)>0):
            if(mags[y,x] >= np.max(magnitudes)):
                target[y,x] = operaBE[y,x]
            else:
                target[y,x] = -255
        else:
            target[y,x] = operaBE[y,x]
            
#Berechne neues Magnitudenbild
thinner(operaBE,degree,res)
res = reshape(res)
show(res,"Verengte Kanten")

#Ja dies hatte Erfolg, nun sieht das Bild mit verengten Kanten echt besser aus


#Aufgabenteil-4
res = np.where(res<=72,0,255)
show(res,"Binarisiert ab 72")
