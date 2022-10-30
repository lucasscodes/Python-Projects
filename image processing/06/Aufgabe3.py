#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
from skimage.exposure import equalize_hist #zum testen!
import matplotlib.pyplot as plt

#Zeigt ein Bild an
def show(img, title = "", col="gray"):
    plt.title(title)
    plt.imshow(img,cmap=col,vmin=np.min(img),vmax=np.max(img))
    plt.show()

#Zeigt ein Numpy-Histogram an
def showHist(hist, title):
    hist,bins = hist
    width = np.diff(bins)
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.title(title)
    plt.show()

bild1 = io.imread("./bildverbesserung/bild1.png")
bild2 = io.imread("./bildverbesserung/bild2.png")


#Teilaufgabe-1
def init(pic, name):
    show(pic,name+" Unbearbeitet")
    hist = np.histogram(pic, bins = 256, range = (0,256), density = False)
    histNorm = hist[0]/(bild1.shape[0]*bild1.shape[1]), hist[1]
    plt.title(name+" Histogramm")
    plt.hist(pic.flatten(), bins = 256, range = (0,256), density=True)
    plt.show()
    return hist, histNorm

hist1, hist1Norm = init(bild1, "Bild1")
hist2, hist2Norm = init(bild2, "Bild2")


#Teilaufgabe-2
def histEq(pic, L=256):
    #Erzeuge Histogramm-Tupel
    hist = np.histogram(pic, bins=L)
    #showHist(hist, "Histogramm")
    #Normiere die Werte
    hist = hist[0]/(pic.shape[0]*pic.shape[1]), hist[1]
    #showHist(hist, "Normiert")
    #Erzeuge Variablen für Transformationsfunktion und Summanden
    tVals = []
    sums = []
    #Für jeden Grauwert von 0-255:
    for i in range(0,L):
        #Füge aktuelles Element an Summanden an
        sums += [hist[0][i]]
        #Berechne Transformationsvariable
        val = (L-1)*np.sum(sums)
        #Füge Variable an Transformationsfunktion an
        tVals += [val]
    #showHist((tVals,hist[1]), "Transformations-Funktion")
    #Runde die Floats
    tVals = np.round(np.array(tVals))
    #showHist((tVals,hist[1]), "Gerundete Transformations-Funktion")
    #Erzeuge Zielbild
    pic2 = np.zeros(pic.shape)
    #Verrechne Tranformationsfunktion mit dem Bild
    for y,x in np.ndindex(pic.shape):
        pic2[y,x] = tVals[pic[y,x]]
    #showHist(np.histogram(pic2, bins=L), "Ausgeglichenes Histogramm")
    #Zeige Ziel Histogramm
    #plt.hist(histEqTest(pic).flatten(), bins=256)
    #plt.title("Ziel Histogramm")
    #plt.show()
    return pic2, (tVals, hist[1])

def histEqTest(pic):
    #aus skimage.exposure, nur zum testen!
    return equalize_hist(pic, nbins = 256)*256

show(histEq(bild1)[0],"Bild1 Bearbeitet")
#show(histEqTest(bild1),"Bild1 Testergebniss")
plt.title("Bild1 Neues Histogramm")
plt.hist(histEq(bild1)[0].flatten(), bins = 256, range = (0,256), density=True)
plt.show()
#plt.title("Bild1 Test Histogramm")
#plt.hist(histEqTest(bild1).flatten(), bins = 256, range = (0,256), density=True)
#plt.show()

show(histEq(bild2)[0], "Bild2 Bearbeitet")
#show(histEqTest(bild2), "Bild2 Testergebniss")
plt.title("Bild2 Neues Histogramm")
plt.hist(histEq(bild2)[0].flatten(), bins = 256, range = (0,256), density=True)
plt.show()
#plt.title("Bild2 Test Histogramm")
#plt.hist(histEqTest(bild2).flatten(), bins = 256, range = (0,256), density=True)
#plt.show()

#Die Histogramme wurden über den ganzen Bereich von 0-255 verteilt, es hat 
#somit zwar Lücken bekommen, ist aber besser über den ganzen Bereich verteilt.


#Teilaufgabe 3
#Ich hatte schon eine showHist()-Funktion, diese bekommt ein hist-Tupel,
#welches von numpy.hist() erzeugt wird und plottet dieses
#Wie schon zum debuggen in Nr2, nutze ich selbe Parameter und Funktion zum Plotten.
#Nun gibt histEq(pic) -> Bild, Tupel
showHist(histEq(bild1)[1], "Bild1 Transformationsfunktion")
def f(x):
    return 255*((x/255)**0.3)
plt.plot(range(len(np.arange(256))),np.array(list(map(f,np.arange(256)))))
plt.title("Intensitätstransformation a)")
plt.show()

showHist(histEq(bild2)[1], "Bild2 Transformationsfunktion")
def g(x):
    top = 255*(np.e**((x/255)*16-10))
    bottom = 1+np.e**((x/255)*16-10)
    return top/bottom
plt.plot(range(len(np.arange(256))),np.array(list(map(g,np.arange(256)))))
plt.title("Intensitätstransformation b)")
plt.show()

#Vergleich zu Musterlösung aus Aufgabe 1 (Blatt4):
#Meine Histogramm-Ausgeglichenen Bilder sind überbelichtet, aber sehr ähnlich
#Die Transformationsfunktionen entsprechen grob den Intensitätstransformationen