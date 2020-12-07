#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, re

def get_pos(init_pos, f):
    x,y = init_pos
    f=f.read()
    data=list(f.strip().split(","))
    for dir in data:
        #print(dir)
        if(dir=='s'):
            y -= 1
        elif(dir=='n'):
            y += 1
        elif(dir=='se'):
            x +=1
        elif(dir=='sw'):
            x -=1
            y -=1
        elif(dir=='ne'):
            x +=1
            y +=1
        elif(dir=='nw'):
            x -=1

    return((x,y))

def get_pos_max(init_pos, f):
    x,y = init_pos
    d=0
    f=f.read()
    data=list(f.strip().split(","))
    for dir in data:
        if(dir=='s'):
            y -= 1
        elif(dir=='n'):
            y += 1
        elif(dir=='se'):
            x +=1
        elif(dir=='sw'):
            x -=1
            y -=1
        elif(dir=='ne'):
            x +=1
            y +=1
        elif(dir=='nw'):
            x -=1
        dist=get_distance(init_pos,(x,y))
        print("new distance =%i"%dist)
        d=max(dist,d)

    return(d)

def get_distance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    dx= x2-x1
    dy = y2-y1
    dd = dy-dx
    D = max(abs(dx), abs(dy), abs(dd))
    return(D)

## MAIN LOOP
f = open("day11.txt",'r')
pos=get_pos((0,0),f)
print("pos = (%i,%i)"%pos)
#print("distance = %i"%get_distance((1,1),(0,3)))
print("distance = %i"%get_distance((0,0),pos))
f=open("day11.txt",'r')
print("Max pos = %i"%get_pos_max((0,0),f))
