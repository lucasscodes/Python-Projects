#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import math


#Aufgabenteil-1
sinFaktor1 = 1
sinFaktor2 = 1/10

def f(x):
    return (np.sin(x*sinFaktor1)*0.8
            +np.sin(x*sinFaktor2)
            +1)

plt.title("Sinusoide 1 und 1/27")
x = np.linspace(0, np.pi*10, 10000)
y = list(map(f, x))
plt.plot(x,y)
plt.xlabel("0 bis 10*Pi")
plt.ylabel("kummultive Sinusoide")
plt.show()