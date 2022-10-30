#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt

#Alter Kram
def show(img,title="",col="gray",vmin=123456,vmax=123456):
    if(vmin and vmax == 123456):
        vmin = np.min(img)
        vmax = np.max(img)
    plt.title(title)
    plt.imshow(img,cmap=col,vmin=vmin,vmax=vmax)
    plt.show()
def reshape(img,max):
    #Untere Grenze auf 0
    img = img-np.min(img)
    #Obere Grenze auf 1
    img = img/np.max(img)
    #Obere Grenze auf max
    return img*max
def yxMid(shape):
    return np.round([(shape[0]-1)/2,
                     (shape[1]-1)/2]).astype(int)
def lowpass(mag,dmax=18):
    mag2 = np.copy(mag) #Erstelle Ergebnissvariable
    shape = mag.shape #Extrahiere Größe
    mid = yxMid(shape)#Berechne Mittelpunkt
    for y,x in np.ndindex(shape):
        #Berechne Entfernung zum Mittelpunkt
        d = np.sqrt((y-mid[0])**2
                    +(x-mid[1])**2)
        if d > dmax: ##Falls mehr als dmax Pixel entfernt
            mag2[y,x] = 1e-10 #Ignoriere Wert
    return mag2


#Aufgabenteil-1
def highpass(mag,dmin=18):
    mag2 = np.copy(mag) #Erstelle Ergebnissvariable
    shape = mag.shape #Extrahiere Größe
    mid = yxMid(shape)#Berechne Mittelpunkt
    for y,x in np.ndindex(shape):
        #Berechne Entfernung zum Mittelpunkt
        d = np.sqrt((y-mid[0])**2
                    +(x-mid[1])**2)
        if d <= dmin: ##Falls weniger/gleich dmax Pixel entfernt
            mag2[y,x] = 1e-10 #Ignoriere Wert
    return mag2
def fourrier(img):
    fourrier = np.fft.fft2(img) #Fourrier-Transformation
    fourrierCentered = np.fft.fftshift(fourrier) #Zentrierung
    magnitudes = np.abs(fourrierCentered) #Fourrierspektrum
    phases = np.angle(fourrierCentered) #Phasenspektrum
    return magnitudes,phases
def combine(mag,pha):
    fourrierCentered2 = mag * np.exp(1j*pha) #Kombiniere
    fourrier2 = np.fft.ifftshift(fourrierCentered2) #Dezentriere
    img = np.real(np.fft.ifft2(fourrier2)) #inverse Fourrier-Transformation
    return img

einstein = io.imread("einstein.jpg")
#show(einstein, "Original")
einMag,einPha = fourrier(einstein) #Hole Fourier- und Phasenspektrum
einMagHigh = highpass(einMag) #Hochpassfilter
einsteinHigh = combine(einMagHigh,einPha) #Füge Bild zusammen
show(einsteinHigh, "Hochpass")
einMagLow = lowpass(einMag) #Tiefpassfilter
einsteinLow = combine(einMagLow,einPha)
show(einsteinLow, "Tiefpass")

monroe = io.imread("monroe.jpg")
#show(monroe, "Original")
monMag,monPha = fourrier(monroe)
monMagHigh = highpass(monMag)
monroeHigh = combine(monMagHigh,monPha)
show(monroeHigh, "Hochpass")
monMagLow = lowpass(monMag)
monroeLow = combine(monMagLow,monPha)
show(monroeLow, "Tiefpass")

#Low+High ergibt wieder die Originale:
#Somit enthalten beide Bilder zusammen immernoch alle Informationen
#High enthält alle scharfen/hochfrequenten Kanten und Ringing
#Low enthält alle unscharfen/niederfrequente Kanten und gegensätzliches Ringing


#Aufgabenteil-2
einPhaHigh = highpass(einPha)
monPhaLow = lowpass(monPha)

"""
teil1 = combine(einMagHigh,einPhaHigh)
teil2 = combine(monMagLow,monPhaLow)
show(teil1, "Einsteins Hohe") #Einsteins-Anteil
show(teil2, "Monroes Tiefe") #Monroes-Anteil
"""

mixMag = einMagHigh+monMagLow
mixPha = einPhaHigh+monPhaLow
show(combine(mixMag,mixPha), "Einstein+Monroe")


#Aufgabenteil-3
#Wenn ich das Ergebniss genau betrachte, sehe ich Einstein.
#Aber wenn ich die Augen zusammenkneife, erkenne ich Monroe.
#Ich nehme an, dass zusammenkneifen einem Weichzeichnen entspricht und 
#somit die höheren Frequenzen rausgefiltert werden.
#Dann verdeckt Einstein nichtmehr die weniger dominanten Anteile Monroes.