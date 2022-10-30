#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import skimage.filters as filters
import skimage.util as util
import matplotlib.pyplot as plt
import scipy.ndimage as ndi

def show(img, title = "", col = "gray", vmin=0, vmax=255):
    plt.title(title)
    plt.imshow(img,cmap=col,vmin=vmin,vmax=vmax)
    plt.show()


#Aufgabenteil-1
einstein = io.imread("./einstein.png")
show(einstein, "Original")

einstein = einstein/255
einstein2 = util.random_noise(einstein, mode="gaussian", var=.01)
show(einstein2, "Gaussches Rauschen", vmax=1)


#Aufgabenteil-2
def meanDiff(img,img2):
    return np.mean(np.abs(img-img2))
print("Random mittlerer Unterschied beträgt:",meanDiff(einstein, einstein2))


#Aufgabenteil-3
def conv(img, n):
    krn = np.ones((n,n))
    krn = krn/np.sum(krn)
    return ndi.convolve(img, krn)

convolved = [conv(einstein2,3),
             conv(einstein2,5),
             conv(einstein2,7),
             conv(einstein2,9),
             conv(einstein2,11)]

show(convolved[0], "Box Filter 3x3", vmax=1)
#show(convolved[1], "5x5:"+str(meanDiff(einstein, convolved[1])), vmax=1)
#show(convolved[2], "7x7:"+str(meanDiff(einstein, convolved[2])), vmax=1)
#show(convolved[3], "9x9:"+str(meanDiff(einstein, convolved[3])), vmax=1)
#show(convolved[4], "11x11:"+str(meanDiff(einstein, convolved[4])), vmax=1)

print("Box Filter",meanDiff(einstein, convolved[0]))


#Aufgabenteil-4
def gauss(img, var):
    return filters.gaussian(img, var)

vals = [0.1]
#(np.arange(20)+1)/10
for i in range(19):
    vals += [round(vals[i]+.1,1)]
#Zielarray
gaussed = np.full((len(vals),2),np.array([0,0],dtype="object"),dtype="object")

for i in range(20):
    gaussed[i,0] = gauss(einstein2, vals[i])
    gaussed[i,1] = meanDiff(einstein, gaussed[i,0])

print("Gausscher Filter", np.min(gaussed[:,1]))
show(gaussed[9,0],"Gausscher Filter 1.0",vmax=1)

#Sichtbarer Unterschied ist minimalst, nachm GaussFilter vielleicht weicher


#Aufgabenteil-5
einstein3 = util.random_noise(einstein, mode="s&p", amount=0.1)
show(einstein3,"Salt&Pepper",vmax=1)
print("S&P mittlerer Unterschied beträgt:",meanDiff(einstein, einstein3))

spGaussed = gaussed

for i in range(20):
    spGaussed[i,0] = gauss(einstein3, vals[i])
    spGaussed[i,1] = meanDiff(einstein, spGaussed[i,0])

print("Gausscher Filter S&P", np.min(gaussed[:,1]))
show(spGaussed[9,0],"Gausscher Filter 1.0",vmax=1)


#Aufgabenteil-6
def med(img):
    res = img
    img = np.pad(img, 1)
    for y in range(res.shape[0]):
        for x in range(res.shape[1]):
            a = y+1
            b = x+1
            res[y-1,x-1] = np.median([img[a-1,b-1], img[a-1,b], img[a-1,b+1],
                                  img[a,b-1], img[a,b], img[a,b+1],
                                  img[a+1,b-1], img[a+1,b], img[a+1,b+1]])
    return res
show(med(einstein3),"Median Filter",vmax=1)
print("Median mittlerer Unterschied beträgt:",meanDiff(einstein, med(einstein3)))

#Zahlentheoretisch ist die medianvariante mit 0.052 als meanDiff sogar schlechter
#Nichtdestotrotz ist das Ergebniss mit Abstand am nähesten ans Original gekommen´