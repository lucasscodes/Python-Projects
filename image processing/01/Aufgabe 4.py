#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
#1
u = np.zeros(100)
#print(len(u))
#2
v = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
#print(v)
#3
m = np.reshape(v,(4,3))
#print(m)
#print(type(m))
#4
m = m*1.2
#print(m)
#5
m = m.astype(int)
#print(m)
#print(type(m))
#6
m = m*1.2
#print(type(m))
#print(m)
#7
m = m*m
#print(m)

