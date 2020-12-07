#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time

f = open("day1.txt",'r')
line=f.readline() #player number
N=len(line)
H=int(N/2)
sum_1=0
sum_2=0
last_index1=line[0]
print(N)
print(H)
print(last_index1)
for i in range(N):
    if(line[(i+1)%N]==last_index1):
        sum_1=sum_1+int(last_index1)
    else:
        last_index1=line[(i+1)%N]

    last_index2=line[i]
    if(line[(i+H)%N]==last_index2):
        sum_2=sum_2+int(last_index2)

print(sum_1)
print(sum_2)
