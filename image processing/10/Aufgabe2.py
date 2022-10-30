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
def reshape(img,m=255):
    #Untere Grenze auf 0
    img = img-np.min(img)
    #Obere Grenze auf 1
    img = img/np.max(img)
    #Obere Grenze auf 255
    return img*m


#Aufgabenteil-1
ape = io.imread("mandrill.png")
show(ape,"Original")
apeFourrier = np.fft.fft2(ape) #Fourrier-Transformation
apeFourrierCentered = np.fft.fftshift(apeFourrier) #Zentrierung
apeMagnitudes = np.abs(apeFourrierCentered) #Fourrierspektrum
apePhases = np.angle(apeFourrierCentered) #Phasenspektrum
show(np.log(apeMagnitudes),"Fourrierspektrum")
show(apePhases, "Phasenspektrum")


#Aufgabenteil-2
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
apeMagnitudesLowpass = lowpass(apeMagnitudes)


#Aufgabenteil-3
apeFourrierCentered2 = apeMagnitudesLowpass * np.exp(1j*apePhases) #Kombiniere
apeFourrier2 = np.fft.ifftshift(apeFourrierCentered2) #Dezentriere
ape2 = np.real(np.fft.ifft2(apeFourrier2)) #inverse Fourrier-Transformation
show(ape2, "Ergebniss nach Tiefpass")
#Man erkennt eine Weichzeichnung und Ringing


#Aufgabenteil-4
def gauss2d(x, y, mx, my, s):
    return 1. / (2. * np.pi * s * s) * np.exp(-((x - mx)**2. / (2. * s**2.) + (y- my)**2. / (2. * s**2.)))
def gaussian(mag, s=10):
    gauss = np.zeros_like(mag) #Hier speichere ich die Gausswerte ab
    shape = mag.shape #Größe
    mid = yxMid(shape) #Mitte
    for y,x in np.ndindex(shape):
        gauss[y,x] = gauss2d(x,y,mid[1],mid[0],s) #Berechne Gausswert
    mag2 = mag * gauss #Führe F'=F*G aus
    return mag2
apeMagnitudesGaussian = gaussian(apeMagnitudes)


#Aufgabenteil-5
apeFourrierCentered3 = apeMagnitudesGaussian * np.exp(1j*apePhases) #Kombiniere
apeFourrier3 = np.fft.ifftshift(apeFourrierCentered3) #Dezentriere
ape3 = np.real(np.fft.ifft2(apeFourrier3)) #inverse Fourrier-Transformation
ape3 = reshape(ape3,1)
show(ape3, "Ergebniss nach Gauss")
#Man erkennt eine Weichzeichnung, aber nun ohne Ringing!