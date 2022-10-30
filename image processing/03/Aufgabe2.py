#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt

def scale(img):
    img = img - np.min(img)
    return (255/np.max(img))*(img-np.min(img))

def show(img):
    plt.imshow(img, cmap="gray", vmin=0, vmax=255)
    plt.show()

#1
bild1 = scale(ski.imread("./serienbild/bild1.png"))
bild2 = scale(ski.imread("./serienbild/bild2.png"))
bild3 = scale(ski.imread("./serienbild/bild3.png"))
bild4 = scale(ski.imread("./serienbild/bild4.png"))
bild5 = scale(ski.imread("./serienbild/bild5.png"))
bilder = [bild1, bild2, bild3, bild4, bild5]

#Berechnet Durschnittsbild aus mehreren Bildern
def average(lst):
    res = np.zeros_like(lst[0])
    for i in range(len(lst)):
        res = res+lst[i]
    res = res/len(lst)
    return res

avg = average(bilder)
show(avg)
#Durch ghosting nicht direkt nutzbar, zu kleine Anzahl gegeben!

#2
#Extrahiert den Hintergrund aus einer Bilderserie
def background(lst):
    #Berechne Durchschnittsbild
    avg = average(lst)
    #Erzeuge Zielbild
    res = np.zeros_like(avg)
    #Erzeuge leere Distanzliste, mit einem Eintrag pro Bild
    distances = list(range(len(lst)))
    #Für jede Pos (y,x) im Bild
    for x in range(avg.shape[1]):
        for y in range(avg.shape[0]):
            #Berechne Abweichungen von jedem Bild zum Durchschnitt
            for i in range(len(lst)):
                distances[i] = max(lst[i][y,x], avg[y,x])-min(lst[i][y,x], avg[y,x])
            #Bestimme Index vom Bild, welches am nähesten am Durchschnitt ist
            nearest = distances.index(np.min(distances))
            #Füge den dazugehörigen Pixel in das Ergebniss ein
            res[y,x] = lst[nearest][y,x]
    return res

back = background(bilder)
show(back)

#3
def difference(img, back, threshold=0):
    diff = img-back
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            if diff[y,x] <= threshold:
                diff[y,x] = 0
    return diff
show(difference(bild1, back, 15))

#4
def combine(lst):
    back = background(lst)
    res = back.copy()
    for i in range(len(lst)):
        res = res+difference(lst[i],back,10)
    return scale(res)

combined = combine(bilder)
show(combined)
ski.imsave("./kombiniert.png", combined.astype(np.uint8))

#5
