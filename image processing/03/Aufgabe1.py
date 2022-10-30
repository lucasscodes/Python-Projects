#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt

def scale(img):
    img = img - np.min(img)
    return (255/np.max(img))*(img-np.min(img))

BlueGreen = scale(ski.imread("./landsatBild/band1.png"))
Green = scale(ski.imread("./landsatBild/band2.png"))
Red = scale(ski.imread("./landsatBild/band3.png"))
NIR = scale(ski.imread("./landsatBild/band4.png"))
MIR = scale(ski.imread("./landsatBild/band5.png"))
Ther = scale(ski.imread("./landsatBild/band6.png"))
MIR2 = scale(ski.imread("./landsatBild/band7.png"))

#1
NDVI = np.zeros_like(Red)
NDVI = (NIR-Red)/(NIR+Red)
NDVI = scale(NDVI)
plt.imshow(NDVI, cmap="gray", vmin=0, vmax=255)

#2
"""
Die grünen Punkte scheinen wirklich lebendige Pflanzen zu sein. 
Bemerkenswert ist die hohe Helligkeit des Bildes, 
somit heben sich dunkle Stellen eher ab als helle.
Also zeigt dieses Bild nun scheinbar hervorgehoben die toten Stellen an.
"""

