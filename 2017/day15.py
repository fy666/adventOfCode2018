#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, re

def com_bytes(A,B,mask):
    common=0
    short_A = mask & A
    short_B = mask & B
    #print("A = %i, binary A = %s, Ashort = %i, Ashort bin =%s"%(A, bin(A), short_A, bin(short_A)))
    #print("B = %i, binary B = %s, Bshort = %i, Bshort bin =%s"%(B, bin(B), short_B, bin(short_B)))
    return(short_A == short_B )

def common_16(number):
    common=0
    for i in range(16):
        if(number & (2**(i))):
            common += 1
        #print("and %i"%(number & (2**i)))
        #print("common =%i"%common)
    return(common)

def count_meth1(A,B,A_f,B_f,mask, m, N):
    count=0
    for i in range(N):
        A =(A * A_f)%m
        B = (B*B_f)%m
        if(com_bytes(A,B,mask)):
            count += 1
    return(count)

def count_meth2(A,B,A_f,B_f,mask,m,N):
    count=0
    for i in range(N):
        A = (A * A_f)%m
        while(A%4 != 0):
            A = (A * A_f)%m
        B = (B * B_f)%m
        while(B%8 != 0):
            B = (B * B_f)%m
        #print("A = %i, B = %i"%(A,B))
        if(com_bytes(A,B,mask)):
            count += 1
    return(count)


## MAIN LOOP
A_f=16807;
B_f=48271;
m=2147483647;
A=722;
#A=65;
B=354;
#B=8921;
mask = (1 << 16) - 1
count=0;
#1
#N=40000000
#print("count = %i"%count_meth1(A,B,A_f,B_f,mask, m, N))
#2
N=5000000
print("count = %i"%count_meth2(A,B,A_f,B_f,mask, m, N))
