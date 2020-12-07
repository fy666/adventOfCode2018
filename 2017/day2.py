#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time

f = open("day2.txt",'r')
sum=0
sum2=0;
#print(f.readlines())

for line in f:
    #print(line)
    numbersInt = list(map(int, line.split("\t")))
    #print(numbersInt)
    #print(max(numbersInt))
    #print(min(numbersInt))
    sum=sum+max(numbersInt)-min(numbersInt)
    N=len(numbersInt)
    for i in range(N):
        for j in range(N):
            if(j!=i):
                div=numbersInt[i]/numbersInt[j];
                #print("Division = %i"%div)
                #print("Round=%i"%round(div))
                #print(isinstance(div, int))
                #print(div)
                if(div-int(div)==0):
                    sum2=sum2+div;
                    print(div)
                    break;


print(sum)
print(sum2)
