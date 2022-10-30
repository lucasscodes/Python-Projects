#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#1
l=[]
for e in range(100,201):
    l.append(e)
print(l)
#2
def listSum(list):
    sum = 0
    for e in list:
        sum += e
    return sum
print(listSum(l))
#3
def listMean(list):
    return listSum(l)/len(l)
print(listMean(l))
#4
def countEvenOdd(list):
    even = 0
    odd = 0
    for elem in list:
       if elem%2 == 0:
           even += 1
       else:
           odd += 1
    return (even, odd)
print(countEvenOdd(l))
#5
def isPrime(int):
    if int < 2:
        return False
    for i in range(2,int):
        if (int/float(i))%1 == 0.0:
            return False
    return True
#for i in range(100,201):
#    if isPrime(i):
#        print(i,isPrime(i))
def countPrimes(list):
    counter = 0
    for e in list:
        if isPrime(e):
            counter+=1
    return counter
#l2 = []
#for i in range(0,31):
#    l2.append(i)
#print(countPrimes(l2))
print(countPrimes(l))