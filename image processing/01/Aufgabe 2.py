#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#1
code='arbreeivtdulnigb'
#print("Full:",code)
#2
a=code[:2]
#print("firstTwo:",a)
b=code[2:]
#print("Rest:",b)
#3
b_0 = b[::2]
#print("even:",b_0)
b_1 = b[1::2]
#rint("odd:",b_1)
#4
b_1 = b_1[::-1]
#print("reverse,odd:",b_1)
#5
print(b_1+a+b_0)