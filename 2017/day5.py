#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time

def load_list():
    f = open("day5.txt",'r')
    instr=[]

    for line in f:
        #print(line)
        instr.append(int(line.strip()))
    print(instr)
    return(instr)


def exit1():
    step=0
    index=0
    tmp=0
    instr=[(0), 3 , 0,  1,  -3 ]
    instr=load_list()
    N=len(instr)
    print(instr)
    print(N)
    while(index<N and index>=0):
        #print("index is %i"%index)
        #print("instr is ")
        #print(instr)
        tmp=index
        index=index+instr[index]
        instr[tmp]+=1
        step+=1
    print(step)
    return(step)

def exit2():
    step=0
    index=0
    tmp=0
    #instr=[(0), 3 , 0,  1,  -3 ]
    instr=load_list()
    N=len(instr)
    print(instr)
    print(N)
    while(index<N and index>=0):
        #print("index is %i"%index)
        #print("instr is ")
        #print(instr)
        tmp=index
        index=index+instr[index]
        if(instr[tmp]>=3):
            instr[tmp]-=1
        else:
            instr[tmp]+=1
        step+=1
    print(step)
    return(step)

exit2()
