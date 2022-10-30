#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt

#Aufgabe 1
img = ski.imread("./mandrill.png")
plt.imshow(img, cmap="gray", vmin=0, vmax=255)
augenpartie = img[25:100,100:400]
plt.imshow(augenpartie, cmap="gray", vmin=0, vmax=255)
ski.imsave("./augenpartie.png", augenpartie)

#Aufgabe 2
kopie = img.copy()
kopie[45, 75] = 0
plt.imshow(kopie, cmap="gray", vmin=0, vmax=255)
kopie2 = img.copy()
kopie2[360:400,220:260] = 0
plt.imshow(kopie2, cmap="gray", vmin=0, vmax=255)

#Aufgabe 3
var1 = img[:,::-1].copy()
var2 = img[::-1,:].copy()
var3 = img[::-1,::-1].copy()

länge = var1.shape[0]
neu = np.zeros((2*länge,2*länge))

neu[länge:2*länge:,0:länge] = img.copy()
neu[länge:2*länge,länge:2*länge] = var1
neu[0:länge,0:länge] = var2
neu[0:länge,länge:2*länge] = var3

plt.imshow(neu, cmap="gray", vmin=0, vmax=255)

#Aufgabe 4
augenpartie2 = img[25:100,100:400]

plt.imshow(augenpartie2, cmap="gray", vmin=0, vmax=255)

print(augenpartie2[0,0]) #=205
print(img[25,100]) #=205
augenpartie[0,0] = 0
print(augenpartie2[0,0]) #=0
print(img[25,100]) #=0
#Ja Änderungen werden bis zum Original propagiert, 
#sonst Array-Kopie mit arr.copy() anlegen und speichern

#Aufgabe 5
maske = np.zeros(img.shape)
maske[25:100,100:400] = 1
plt.imshow(maske, cmap="gray", vmin=0, vmax=1)
summe = np.array(maske * img)
plt.imshow(summe, cmap="gray", vmin=0, vmax=255)