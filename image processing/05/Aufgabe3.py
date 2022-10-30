#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skimage.io as io
import skimage.color as color
import matplotlib.pyplot as plt

def show(img, title = "", col = "gray"):
    plt.title(title)
    if(col == "hsv"):
        plt.imshow(img,cmap=col,vmin=0,vmax=1)
    else:
        plt.imshow(img,cmap=col,vmin=np.min(img),vmax=np.max(img))
    plt.show()
    
#flowerN = [Color, Mask, (Gray), (AvgMask), (hsv), (avgH)]
f1 = [io.imread("./blumen/image_02881.jpg"),io.imread("./blumen/image_02881_maske.png"),[],[],[],[]]
f2 = [io.imread("./blumen/image_02890.jpg"),io.imread("./blumen/image_02890_maske.png"),[],[],[],[]]
f3 = [io.imread("./blumen/image_04650.jpg"),io.imread("./blumen/image_04650_maske.png"),[],[],[],[]]
f4 = [io.imread("./blumen/image_04666.jpg"),io.imread("./blumen/image_04666_maske.png"),[],[],[],[]]

#Aufgabenteil 1, bestimme gray's
f1[2] = color.rgb2gray(f1[0])
f1[3] = np.sum(f1[2]*f1[1])/np.sum(f1[1])

f2[2] = color.rgb2gray(f2[0])
f2[3] = np.sum(f2[2]*f2[1])/np.sum(f2[1])

f3[2] = color.rgb2gray(f3[0])
f3[3] = np.sum(f3[2]*f3[1])/np.sum(f3[1])

f4[2] = color.rgb2gray(f4[0])
f4[3] = np.sum(f4[2]*f4[1])/np.sum(f4[1])

#Aufgabenteil 2
f1[4] = color.rgb2hsv(f1[0])
f1[5] = np.sum(f1[4][:,:,0]*f1[1])/np.sum(f1[1])

f2[4] = color.rgb2hsv(f2[0])
f2[5] = np.sum(f2[4][:,:,0]*f2[1])/np.sum(f2[1])

f3[4] = color.rgb2hsv(f3[0])
f3[5] = np.sum(f3[4][:,:,0]*f3[1])/np.sum(f3[1])

f4[4] = color.rgb2hsv(f4[0])
f4[5] = np.sum(f4[4][:,:,0]*f4[1])/np.sum(f4[1])


#Aufgabenteil 3
show(f1[0], "1 Farbe")
show(f1[2]*f1[1], "1 Grauton="+str(f1[3]))
show(f1[4][:,:,0]*f1[1], "1 Hue="+str(f1[5]), "hsv")

show(f2[0], "2 Farbe")
show(f2[2]*f2[1], "2 Grauton="+str(f2[3]))
show(f2[4][:,:,0]*f2[1], "2 Hue="+str(f2[5]), "hsv")

show(f3[0], "3 Farbe")
show(f3[2]*f3[1], "3 Grauton="+str(f3[3]))
show(f3[4][:,:,0]*f3[1], "3 Hue="+str(f3[5]), "hsv")

show(f4[0], "4 Farbe")
show(f4[2]*f4[1], "4 Grauton="+str(f4[3]))
show(f4[4][:,:,0]*f4[1], "4 Hue="+str(f4[5]), "hsv")

"""Man erkennt größere Unterschiede in den Hue's, da man dort die Farben unterscheiden kann:
        Spanne: Bei den Grauwerten hat man nur eine Spanne von 0.47-0.79, bei den Hue's aber 0.15-0.93.
        Gruppierung: Außerdem Gruppieren sich ähnliche Farben enger zusammen: 
                        Gelb: davor 0.65-0.79, danach 0.15-0.16
                        Pink: davor 0.47-0.49, danach 0.92-0.93"""