#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, math


def spirale(number):
    N=math.ceil(math.sqrt(number))
    if(N==2*math.floor(N/2)):
        N=N+1
    origin=math.floor(N/2)
    print(origin)
    D=N**2; #coin inferieur droit
    C=N**2-N+1 #coin inferieur gauche
    B=N**2-2*N+2 #coin supérieur gauche
    A=N**2-3*N+3

    if(number==D):
        x=N-1
        y=N-1
    else:
        if(number<=A):
            x=N-1;
            y=(A-number)
        elif(number<=B):
            y=0
            x=(B-number)
        elif(number<=C):
            x=0
            y=N-(C-number)
        else:
            y=N-1
            x=(number-C)

    print(N)
    print("N=%i, A=%i, B=%i, C=%i, D=%i"%(N,A,B,C,D))
    print("Position of %i = (%i,%i)"%(number,x,y))
    dx=abs(origin-x)
    dy=abs(origin-y)
    chemin=dx+dy
    return(chemin)

def spiral_1(n):
    dx,dy = 1,0            # Starting increments
    x,y = 0,0              # Starting location
    myarray = [[None]* n for j in range(n)]
    for i in range(n**2):
        myarray[x][y] = i
        nx,ny = x+dx, y+dy
        if 0<=nx<n and 0<=ny<n and myarray[nx][ny] == None:
            x,y = nx,ny
        else:
            dx,dy = -dy,dx
            x,y = x+dx, y+dy
    return myarray

def spiral_2(n):
    def spiral_part(x, y, n):
        if x == -1 and y == 0:
            return -1
        if y == (x+1) and x < (n // 2):
            return spiral_part(x-1, y-1, n-1) + 4*(n-y)
        if x < (n-y) and y <= x:
            return spiral_part(y-1, y, n) + (x-y) + 1
        if x >= (n-y) and y <= x:
            return spiral_part(x, y-1, n) + 1
        if x >= (n-y) and y > x:
            return spiral_part(x+1, y, n) + 1
        if x < (n-y) and y > x:
            return spiral_part(x, y-1, n) - 1

    array = [[0] * n for j in range(n)]
    for x in range(n):
        for y in range(n):
            array[x][y] = spiral_part(y, x, n)
    return array



#number_to_find=265149#1024
#chemin=spirale(number_to_find)
#print("For %i, path = %i"%(number_to_find,chemin))
print(spiral_1(5))
print(spiral_2(4))
