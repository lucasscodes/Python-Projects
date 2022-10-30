#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt

#Alter Kram
def show(img,title="",col="gray"):
    plt.title(title)
    plt.imshow(img,cmap=col)
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


#Aufgabenteil-1
hBars = io.imread("mandrill_hBars.png")
show(hBars, "Original")
hMag,hPha = fourrier(hBars)
show(np.log(hMag), "Fourrierspektrum")
show(hPha, "Phasenspektrum")
#Man sieht in den 4 Ecken jeweils eine Gruppe von 3-4 Punkten
#Scheinbar geht es aber um die 4Punkte(mit schwachen Linien) bei [256,:].
#Denn die Vertikalen Linen stellen die horizontalen aus dem Original dar.
#Die nähesten Punkte sind ca 105 Pixel über und unterm Mittelpunkt
#Also achte ich nun nurnoch auf Werte mit max. Distanz von 105-10=95.
hMagLow = lowpass(hMag,95)
show(np.log(hMagLow), "Tiefpass Fourrierspektrum")
hBars2 = combine(hMagLow,hPha)
show(hBars2, "Tiefpass bei 95")
#Nun sind die horizontalen Streifen alle verschwunden das Bild heller.
#Negativ ist aber, dass die hochfrequentesten Anteile entfernt wurden.


#Aufgabenteil-2
hMagManual = np.copy(hMag)
hMagManual[:70,253:261] = 1e-10
hMagManual[120:180,253:261] = 1e-10
hMagManual[(512-180):(512-120),253:261] = 1e-10
hMagManual[(512-70):512,253:261] = 1e-10
show(np.log(hMagManual), "Manuelles Fourrierspektrum")
hBars3 = combine(hMagManual, hPha)
show(hBars3, "Manueller Frequenzfilter")
#Nun ist das Bild weniger aufgehellt und enthält 
#auch noch die höchsten Frequenzanteile


#Aufgabenteil-3
hvBars = io.imread("mandrill_hvBars.png")
show(hvBars, "Original")
hvMag,hvPha = fourrier(hvBars)
show(np.log(hvMag), "Fourrierspektrum")

#Man kann nun wie zuvor entweder mit Tief/Hochpass-Filtern arbeiten,
#oder wieder manuell die passenden Frequenzen verdecken.

"""
#Einfach und schnell, aber mehr Fehler:
hvMag2 = lowpass(hvMag,80)
show(np.log(hvMag2), "Neues Frequenzspektrum1")
hvBars2 = combine(hvMag2, hvPha)
show(hvBars2, "Tiefpass bei 80")
"""

#Manuell, aber schärfer/hochfrequenter:
hvMag3 = np.copy(hvMag)
#vertikale
hvMag3[:70,253:261] = 1e-10
hvMag3[120:180,253:261] = 1e-10
hvMag3[(512-180):(512-120),253:261] = 1e-10
hvMag3[(512-70):512,253:261] = 1e-10
#horizontale
hvMag3[253:260,0:150] = 1e-10
hvMag3[253:260,(512-150):512] = 1e-10
show(np.log(hvMag3), "Neues Frequenzspektrum2")
hvBars3 = combine(hvMag3, hvPha)
show(hvBars3, "Manuell gefiltert")
