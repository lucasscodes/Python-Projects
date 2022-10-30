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


#Aufgabenteil-1
opera = io.imread("./opera.png")
#show(opera, "Original")
opera2 = filt.gaussian(opera, 2, multichannel=True)
show(opera2, "Gauss-Varianz = 2.0")
opera3 = col.rgb2gray(opera2)*255 #Achtung nunWertebereich [0,1] nicht [0,255]
show(opera3, "Black&White")

operaH = filt.sobel_h(opera3)
operaV = filt.sobel_v(opera3)
operaE = np.sqrt(np.add(np.power(operaH,2)/2,
                        np.power(operaV,2)/2))
operaE = reshape(operaE)
show(operaE, "Gradienten-Magnituden")

#Es werden Kanten gefunden, an denen ein großer Kontrastsprung an der hor/vert. Achse stattfindet.
#Heller werden Kanten, an denen dieser Kontrastsprung einen gößeren Bereich überspringt 
#und dieser am besten auch in beide relevanten Achsen stattfindet.


#Aufgabenteil-2
#show(reshape(opera2[:,:,2]), "Blauanteil unbearbeitet") #Alleine recht nutzlos
#Blauheit = B-(R+G)/2
operaB = opera2[:,:,2]-(opera2[:,:,0]+opera2[:,:,1])/2 
#Auf [-255,255] mappen
operaB = reshape(operaB)*2-255
#Werte unter 0 abschneiden
operaB = np.where(operaB<0,0,operaB)
show(operaB, "Blauheit")
    


#Aufgabenteil-3
#Wiederhole Berechnungen
operaBH = filt.sobel_h(operaB)
operaBV = filt.sobel_v(operaB)
operaBE = np.sqrt(np.add(np.power(operaBH,2),
                        np.power(operaBV,2))/2)
operaBE = reshape(operaBE)

show(operaBE, "Blaue-Kanten")

#Nun sind die Kanten am hellsten, an denen viel Blau anlag,
#also haben wir nun den Himmel besser vom Gebäude abgegrenzt.
#Außerdem zeigen wir somit weniger Kanten innerhalb des Gebäudes auf.