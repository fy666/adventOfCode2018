#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, re

def create_scan():
    f = open("day13.txt",'r')
    #f=open("day13short.txt", 'r')
    wall=[];
    data=[];
    for i in range(100): # create empty list ?
        wall.append(0);
    for line in f:
        data=list(map(int,line.strip().split(":")))
        #print(data)
        wall[data[0]] = data[1]

    return(wall)

def traversee(wall):
    severity=0;
    for index in range(100):
        if(wall[index]!=0):
            #print("Wall range =%i, modulo = %i"%(wall[index], index%((wall[index]-1)*2)))
            if(index%((wall[index]-1)*2) == 0):
                severity += index * wall[index]
                print("Index = %i, range =%i"%(index,wall[index]))
                print(severity)
    return(severity)

def delayed_traversee(wall, delay):
    for index in range(100):
        if(wall[index]!=0):
            if((index+delay)%((wall[index]-1)*2) == 0):
                return(0)

    return(1)

## MAIN LOOP
wall=create_scan()
#print(wall)
#print("Severity = %i"%traversee(wall))
delay=1
while(delayed_traversee(wall, delay)==0):
    delay +=1
print("Delay =%i"%delay)
