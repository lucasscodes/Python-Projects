#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import skimage.io as ski
import numpy as np
import matplotlib.pyplot as plt

def show(img, title = ""):
    plt.title(title)
    plt.imshow(img,cmap="gray",vmin=0,vmax=255)
    plt.show()

ape = ski.imread("./mandrill.png")
show(ape, "rgbOriginal")

def rgb2cmy(pic):
    print("Arbeits rgb nach cmy um....")
    return np.full(ape.shape, 255)-pic
#ape = rgb2cmy(ape)
#show(ape, "cmy")

def cmy2rgb(pic):
    print("Arbeits cmy nach rgb um....")
    return np.full(ape.shape, 255)-pic
#ape = cmy2rgb(ape)
#show(ape, "cmy->rgb")

def rgb2hsi(pic):
    res = np.zeros(pic.shape)
    print("Arbeite rgb nach hsi um....")
    for x,y in np.ndindex(pic.shape[:2]):
        r,g,b = pic[x,y]
        theta = np.rad2deg(np.arccos(((2*r-g-b)/2)/np.sqrt((r-g)**2+(r-b)*(g-b)+0.0001)))
        if(g<b):
            h = 360-theta
        else:
            h = theta
        s = 1 - (3/(r/255+g/255+b/255+0.0001))*np.min([r,g,b])/255
        i = (r/255+g/255+b/255)/3
        res[x,y] = [h,s,i]
    return res
#ape = rgb2hsi(ape)
#show(ape, "hsi")

def hsi2rgb(pic):
    res = np.zeros(pic.shape,dtype=np.uint8)
    print("Arbeite hsi nach rgb um....")
    for x,y in np.ndindex(pic.shape[0:2]):
        h,s,i = pic[x,y]
        if(0<=h and h<120):
            b = i*(1-s)
            r = i*(1+(s*np.cos(np.deg2rad(h)))
                   /(np.cos(np.deg2rad(60-h))))
            g = 3*i-(r+b)
        if(120<=h and h<240):
            h = h-120
            r = i*(1-s)
            g = i*(1+(s*np.cos(np.deg2rad(h)))
                   /(np.cos(np.deg2rad(60-h))))
            b = 3*i-(r+g)
        if(240<=h):
            h = h-240
            g = i*(1-s)
            b = i*(1+(s*np.cos(np.deg2rad(h)))
                   /(np.cos(np.deg2rad(60-h))))
            r = 3*i-(g+b)
        r,g,b = [255*r,255*g,255*b]
        res[x,y] = np.array(np.round([r,g,b]),dtype=np.uint8)
    return res
#ape = hsi2rgb(ape)
#show(ape, "hsi->rgb")

show(hsi2rgb(rgb2hsi(cmy2rgb(rgb2cmy(ape)))), "rgb=>cmy=>rgb=>hsi=>rgb")

