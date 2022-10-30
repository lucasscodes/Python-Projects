#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import skimage.io as io
import skimage.filters as filt
import skimage.color as col
import matplotlib.pyplot as plt

#Alter Kram
def show(img,title="",col="gray",vmin=0,vmax=255):
    plt.title(title)
    plt.imshow(img,cmap=col,vmin=vmin,vmax=vmax)
    plt.show()
def reshape(img):
    #Untere Grenze auf 0
    img = img-np.min(img)
    #Obere Grenze auf 1
    img = img/np.max(img)
    #Obere Grenze auf 255
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
degree = np.round(np.degrees(np.arctan(operaBH/(operaBV+1e-10))),2)
degree = np.where(np.logical_and(degree<22.5,-22.5<=degree),0,degree)
degree = np.where(np.logical_and(degree<67.5,22.5<=degree),45,degree)
degree = np.where(np.logical_and(degree<-22.5,-67.5<=degree),-45,degree)
degree = np.where(degree>=67.5,90,degree)
degree = np.where(degree<-67.5,90,degree)
res = np.zeros(operaBE.shape)
def getNeighs(degs,y,x):
    res = []
    height, width = degs.shape
    if(degs[y,x] == -45):
        if(y+1<height and x-1>=0):
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
def thinner(mags,degs,target):
    for y,x in np.ndindex(target.shape):
        neighs = getNeighs(degs, y,x)
        magnitudes = []
        while len(neighs)>0:
            y2,x2 = neighs[0],neighs[1]
            neighs = neighs[2::]
            if(degs[y,x] == degs[y2,x2]):
                magnitudes += [mags[y2,x2]]
        if(len(magnitudes)>0):
            if(mags[y,x] >= np.max(magnitudes)):
                target[y,x] = operaBE[y,x]
            else:
                target[y,x] = -255
        else:
            target[y,x] = operaBE[y,x]
thinner(operaBE,degree,res)
res = reshape(res)
show(res,"vorheriges Ergebniss")


#Aufgabenteil-1
upper=72
lower=40
#Ignoriere Magnituden bis zur Rauschgrenze, somit sauberer
noiseThresh=17
#Wieviel sichere Kanten in unknown rein-überlappen, 
#sonst funktioniert Aufgabenteil2 nicht, 
#da unbekannte Kanten sonst nie sichere Kanten berühren
overlap = 10
#Extrahiere sicheren Bereich
needed = np.where(res>upper,255,0)
#Extrahiere sicher unnötigen Bereich
unnoetig = np.where(np.logical_and(res<lower, res>noiseThresh),255,0)
show(needed,"Notwendig ab "+str(upper))
show(unnoetig, "Unnötig bis "+str(lower))


#Aufgabenteil-2
#Hebe nicht zugeordneten Pixel hervor
unknown = np.where(np.logical_and(res<=upper+overlap, res>=lower),255,0)
#Zeige den Bereich der nicht zugeordneten Pixel
show(unknown, "Vllt. relevante Pixel, zwischen "+str(lower)+" und "+str(upper+overlap))
known = np.zeros(unknown.shape)
#Falls keine Pixel überlappen, wird der Aufruf nie neue Pixel hinzufügen
if(np.sum(np.where(np.logical_and(unknown==255,needed==255),1,0)) == 0):
    print("Keine eingefärbten Pixel aus unknown, berühren je eine sichere Kante!")

#Gibt alle Koordinaten einer angepeilten Gruppe von 255ern
def getCompCoords(img, y, x):
    if(img[y,x] != 255):
        return []
    #Zielvariable
    res = [[y,x]]
    #Warteschlange
    queue = [y,x]
    #Zeige auf erstes Element
    i = 0
    #Solange Schlange nicht abgearbeitet
    while len(queue)-i>0:
        #Hole Koordinaten
        y,x = queue[i+0],queue[i+1]
        i += 2
        #Für jeden Nachbar-Offset
        for tup in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]:
            #Falls Nachbar verbunden ist und noch nicht im Ergebniss
            if(img[y+tup[0],x+tup[1]] == 255 and [y+tup[0],x+tup[1]] not in res):
                #Füge ihn als verbundenne Kordinate hinzu
                res += [[y+tup[0],x+tup[1]]]
                #Füge ihn in Queue ein
                queue += [y+tup[0],x+tup[1]]
    #Gib alle Koordinaten der Zusammenhangskomponente
    return res
#Test:
    #part = unknown[266:290,167:172]
    #np.sum(np.where(part == 255,1,0)) => 22Coords
    #len(getCompCoords(part, 1,3))     => 22Coords

def activate(sichere, unbekannte, ziel):
    #Zähle ob neue Pixel übernommen werden
    counter=0
    #Für jeden Pixel
    for y,x in np.ndindex(ziel.shape):
        #falls noch unbekannt ist, ob er eine starke Kante berührt
        if(unbekannte[y,x]==255):
            #if(sichere[y,x]==255):
                #print("Error, unbekannter Pixel ist auch schon sicherer Pixel!!")
            #Hole alle verbundennen Pixel
            coords = getCompCoords(unbekannte,y,x)
            #Gucke für jede Koordinate
            for coord in coords:
                y2,x2 = coord
                #print(coord, sichere[y2,x2])
                #Falls eine der Koordinaten eine sichere Kante trifft
                if(sichere[y2,x2]==255):
                    #Dann ist die unbekannte Kante nun sicher geworden
                    ziel[y,x] = unbekannte[y,x]
                    #Der Rest ist nun egal geworden, (y,x) wurde abgearbeitet
                    coords = []
                    counter +=1
    if(not counter>0):
        print("Keine Pixel wurden hinzugefügt!")
#Test:
    #test0 = np.array([[0,0,0,0,0,0,0],
    #                  [0,0,0,0,0,255,0],
    #                  [0,0,0,0,0,0,0]])
    #test1 = np.array([[0,0,0,0,0,0,0],
    #                  [0,255,255,255,255,255,0],
    #                  [0,0,0,0,0,0,0]])
    #test2 = np.array([[0,0,0,0,0,0,0],
    #                  [0,0,0,0,0,0,0],
    #                  [0,0,0,0,0,0,0]])
    #activate(test0,test1,test2) => Es wurden 5 neue Pixel hinzugefügt!
    #test2 =>    array([[  0,   0,   0,   0,   0,   0,   0],
    #                   [  0, 255, 255, 255, 255, 255,   0],
    #                   [  0,   0,   0,   0,   0,   0,   0]])
    
activate(needed,unknown,known)

#Füge zugeordnete und schon sichere Pixel zusammen zu Kante
show(known, "Übernommenne vllt. relevante Pixel")
res = needed + known
show(res, "Kombinierter Kantenzug")