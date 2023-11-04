#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, re
import math

def loop(knot, current, skip, lengths):
    for l in lengths:
        index=[]
        #print("Treating length %i"%l)
        for i in range(l):
            index.append((current+i)%L)
        #print("index =",index)
        Lh=math.ceil(l/2)
        for i in range(Lh):
            #print("%i swap with %i"%(i, l-1-i))
            (knot[index[i]],knot[index[l-i-1]])=(knot[index[l-i-1]],knot[index[i]])
        #print("Knot = ",knot)
        current = (current + l + skip)%L
        skip+=1
    return(knot, current, skip)

def convert_list_to_ascii(lengths):
    new_lengths=[]
    for l in lengths:
        new_lengths.append(ord(l))
    new_lengths.append(17)
    new_lengths.append(31)
    new_lengths.append(73)
    new_lengths.append(47)
    new_lengths.append(23)
    print(new_lengths)
    return(new_lengths)

def dense_hash(res):
    seq=[]
    x=0
    for index,i in enumerate(res):
        if(index%16==0):
            if(index!=0):
                seq.append(x)
            x=i
        else:
            x ^= i
    seq.append(x)
    print(seq)
    return(seq)

def hash(a):
    seq=''
    for i in a:
        tmp="{0:#0{1}x}".format(i,4)
        seq+=tmp[2:4]
    return(seq)
## MAIN LOOP
if(0):
    L=5
    lengths=[3, 4, 1, 5]
else :
    L=256
    lengths='31,2,85,1,80,109,35,63,98,255,0,13,105,254,128,33'

knot=list(range(L))

N=64
current=0
skip=0
new_lengths=convert_list_to_ascii(lengths)
for i in range(N):
    (knot, current, skip) = loop(knot, current, skip, new_lengths)
a=dense_hash(knot)
b=hash(a)
print(b)
#print("result=%i"%(knot[0]*knot[1]))
