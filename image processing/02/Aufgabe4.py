#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt

img = ski.imread("./mandrill.png")
#plt.imshow(img, cmap="gray", vmin=0, vmax=255)

#Gaußsches-Rauschen(int, image)
def gaußschesRauschen(Standartabweichung, Bild):
    kopie = Bild.copy()
    rauschen = np.random.normal(0,Standartabweichung,kopie.size).reshape(kopie.shape)
    kopie = np.clip((kopie + rauschen), 0, 255)
    return kopie
#plt.imshow(gaußschesRauschen(510, img), cmap="gray", vmin=0, vmax=255)

#Salt and Pepper-Rauschen(float, image)
def saltAndPepperRauschen(Wahrscheinlichkeit, Bild):
    kopie = Bild.copy()
    rauschen = (np.random.choice(3, Bild.size, p=[Wahrscheinlichkeit/2, 
                                                  1-Wahrscheinlichkeit, 
                                                  Wahrscheinlichkeit/2]) -1).reshape(kopie.shape)*255
    return np.clip((kopie+rauschen),0,255)
#plt.imshow(saltAndPepperRauschen(1.0, img), cmap="gray", vmin=0, vmax=255)
verrauscht = saltAndPepperRauschen(0.8, img)
n = 1000
for i in range(n-1):
    verrauscht += saltAndPepperRauschen(0.8, img)
verrauscht = verrauscht/n
plt.imshow(verrauscht, cmap="gray", vmin=0, vmax=255)

"""In der Grauwertdarstellung sind sich beide vom Aussehen her sehr änhlich.
Standartabweichung: Ist komplexer als das andere Modell. 
Weniger stark abfallende Erkennbarkeit und man erkennt erst bei einer Abweichung 
vom doppelten Pixelbereich (2*255=510) wenig bis nichts mehr. 
Scheinbar eine asymptotische Annäherung an ein reines Rauschen.

Wahrscheinlichkeit: Kann man interpretieren als: "Wie viele Prozent des Bildes fehlen", 
somit direkter inverser Zusammenhang zur Darstellungstreue.
Erkennbarkeit wird schnell verloren, in einer klar eingegrenzten linearen Annäherung an ein reines Rauschen. 
Ab ~80% erkennt man sehr wenig bis nichts."""
