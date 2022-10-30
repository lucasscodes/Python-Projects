#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import skimage.filters as filt
import skimage.util as util
import matplotlib.pyplot as plt

#Alter Kram
def show(img,title="",col="gray",vmin=0,vmax=255):
    plt.title(title)
    plt.imshow(img,cmap=col,vmin=vmin,vmax=vmax)
    plt.show()
    
def reshape(img,max=255):
    #Untere Grenze auf 0
    img = img-np.min(img)
    #Obere Grenze auf 1
    img = img/np.max(img)
    #Obere Grenze auf 255
    return img*max

def cut(img, min=0, max=255):
    res = np.minimum(img, max)
    res = np.maximum(res, min)
    return reshape(res)


#Aufgabenteil-1
ape = io.imread("mandrill.png")
ape = reshape(ape,1)
ape2 = filt.gaussian(np.pad(ape,1,mode="edge"),3)[1:ape.shape[0]+1,1:ape.shape[1]+1]
ape3 = util.random_noise(ape,var=.01)

show(ape,"Original",vmin=0,vmax=1)
show(ape2,"Weich",vmin=0,vmax=1)
show(ape3, "Rauschen",vmin=0,vmax=1)


#Aufgabenteil-2
l = filt.laplace(ape)
l2 = filt.laplace(ape2)
l3 = filt.laplace(ape3)

show(l,"Laplace Original",vmin=np.min(l),vmax=np.max(l))
show(l2,"Laplace Weich",vmin=np.min(l2),vmax=np.max(l2))
show(l3, "Laplace Rauschen",vmin=np.min(l3),vmax=np.max(l3))
#1:Es werden alle Kanten als Wasserzeichen sichtbar, aber sehr schwach
#2:Das Wasserzeichen ist viel stärker zu erkennen, aber unscharf
#3:Scheint wie 1, heller und dadurch schlechterer Kontrast


#Aufgabenteil-3
l3smooth = filt.gaussian(l3,sigma=1)
show(l3smooth,"Laplace Rauschen Weich",vmin=np.min(l3smooth),vmax=np.max(l3smooth))
#Scheint nun wirklich besser geworden zu sein. Ist das schärfste und einfach sichtbar


#Aufgabenteil-4
def comp(a,b,threshold):
    return (((np.max([a,b])-np.min([a,b])) >= threshold) and #mind. Schwellwert
           (np.sign(a) != np.sign(b))) #Vorzeichenwechsel

def neighbours(y,x,pic,thr):
    #Oben Unten (falls nicht am Rand und Werte großen Nulldurchgang beschreiben)
    if (y>0 and y<(pic.shape[0]-1)) and comp(pic[y-1,x],pic[y+1,x],thr): return True
    #Links Rechts
    if (x>0 and x<(pic.shape[1]-1)) and comp(pic[y,x-1],pic[y,x+1],thr): return True
    #ObLi UnRe
    if ((x>0 and x<(pic.shape[1]-1)) and 
        (y>0 and y<(pic.shape[0]-1)) and 
        comp(pic[y-1,x-1],pic[y+1,x+1],thr)): return True
    #ObRe UnLi
    if ((x>0 and x<(pic.shape[1]-1)) and 
        (y>0 and y<(pic.shape[0]-1)) and 
        comp(pic[y-1,x+1],pic[y+1,x-1],thr)): return True
    return False
    
def getEdges(pic,thr=.005):
    res = np.zeros_like(pic)
    for ((y,x),_) in np.ndenumerate(l2):
        if neighbours(y,x,pic,thr): res[y,x] = 1
    return res

print("Berechne",l2.shape[0]*l2.shape[1],"Kanten...")
edges = getEdges(l2,.005)
show(edges,"Kanten mit Schwellwert 0.005",vmin=np.min(edges),vmax=np.max(edges))

#Aufgabenteil-5
edges2 = filt.sobel(l2,mode="nearest")
edges2 = np.where(edges2>=0.0025,edges,0)
show(edges2,"Sobel ab Schwellwert 0.0025",vmin=np.min(edges),vmax=np.max(edges))

#Sie unterscheiden sich eigentlich garnicht
