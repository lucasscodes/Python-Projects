#!/usr/bin/env python3
# -*- coding: utf-8 -*-
image = [2,3,4]
kernel1 = [0,1,2]
kernel2 = [2,3,4]

#Alles gerade
def cor(img, krn):
    res = []
    for i in range(3):
        res += [krn[0]*img[i] + krn[1]*img[i+1] + krn[2]*img[i+2]]
    return [0]+res+[0]

#Faltung = gespiegelter Kernel
def conv(img, krn):
    res = []
    for i in range(3):
        res += [krn[2]*img[i] + krn[1]*img[i+1] + krn[0]*img[i+2]]
    return [0]+res+[0]

print(cor([0]+image+[0], kernel1))
print(cor([0]+kernel1+[0], image))
print(conv([0]+image+[0], kernel1))
print(conv([0]+kernel1+[0], image))
