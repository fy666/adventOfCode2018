#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, copy




def count_it(f):
    nb_it=1
    dl=0
    steps=[]
    for line in f:
        memory = list(map(int,line.strip().split("\t")))
    #memory=[0,2,7,0]

    steps.append(arrange(memory))
    (dl,same)=same_list(steps)
    while(same==0):
        steps.append(arrange(steps[nb_it-1]))
        (dl,same)=same_list(steps)
        nb_it+=1;
        #print(nb_it)


    #print(steps)
    return(nb_it,dl)

def same_list(matrix):
    same=0
    dl=0
    l=len(matrix)
    for b in range(l-2):
        if(matrix[l-1]==matrix[b]):
            same=1;
            dl=b-l+1
            print("line %i and line %i are the same"%(b,l-1))
            break;
    #print("same is %i"%same)
    return(dl,same)



def arrange(line):
    m=max(line)
    index=[i for i, j in enumerate(line) if j == m]
    ix=min(index)
    n=line[ix]
    N=len(line)
    newline=copy.copy(line);
    newline[ix]=0
    a=1
    while(n>0):
        newline[(ix+a)%N]+=1
        n-=1
        a+=1
    #print(line)
    #print(newline)
    return(newline)

f = open("day6.txt",'r')
(nb,dl)=count_it(f)
print("number of iteration = %i, repeat afer %i cycles"%(nb,dl))
