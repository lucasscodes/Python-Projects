#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt

def scale(img):
    img = img - np.min(img)
    return (255/np.max(img))*(img-np.min(img))

def show(img):
    plt.imshow(img,cmap="gray",vmin=0,vmax=255)
    plt.show()

bild1 = scale(ski.imread("./ohneFehler.png"))
bild2 = scale(ski.imread("./mitFehler.png"))

show(bild1)
show(bild2)

#1
diff = scale(bild1-bild2)
show(diff)

#2
diff2 = (diff>0)
plt.imshow(diff2,cmap="gray",vmin=0,vmax=1)
plt.show()

#3
def deleteNeighbours(img,y,x):
    #Lege Arbeitskopie an
    img2 = img.copy()
    #Startkoordinaten-Tupel
    queue = [[y,x]]
    #Queue-Pointer
    i=0
    #Solange Koordinaten abzuarbeiten sind
    while (len(queue)-i)>0:  
        #Lies akt Koordinaten
        y=queue[i][0]
        x=queue[i][1]
        #Setze Pixel auf 0
        img2[y,x] = 0
        #Verschiebe Pointer hinter abgearbeitete
        i = i+1
        #Falls Nachbar Wert 1 hatte und noch nicht abgearbeitet wurde, merken:
        if img[y,x+1] and [y,x+1] not in queue:
            queue = queue+[[y,x+1]]
        if img[y+1,x+1] and [y+1,x+1] not in queue:
            queue = queue+[[y+1,x+1]]
        if img[y+1,x] and [y+1,x] not in queue:
            queue = queue+[[y+1,x]]
        if img[y+1,x-1] and [y+1,x-1] not in queue:
            queue = queue+[[y+1,x-1]]
        if img[y,x-1] and [y,x-1] not in queue:
            queue = queue+[[y,x-1]]
        if img[y-1,x-1] and [y-1,x-1] not in queue:
            queue = queue+[[y-1,x-1]]
        if img[y-1,x] and [y-1,x] not in queue:
            queue = queue+[[y-1,x]]
        if img[y-1,x+1] and [y-1,x+1] not in queue:
            queue = queue+[[y-1,x+1]]
    #Gib Bild ohne die angepeilte Gruppe aus
    return img2
             
def count(img):
    counter = 0
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y,x]:
                counter = counter+1
                print("Arbeite an Gruppe",counter,"...")
                img = deleteNeighbours(img,y,x)
                plt.imshow(img,cmap="gray",vmin=0,vmax=1)
                plt.show()
    return counter

"""part = diff2[100:200,250:350]
plt.imshow(part,cmap="gray",vmin=0,vmax=1)
plt.show()    
part=deleteNeighbours(part,56,47)
plt.imshow(part,cmap="gray",vmin=0,vmax=1)
plt.show()"""

print("Bild enthielt",count(diff2),"Änderungen!")
                

     