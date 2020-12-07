#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, re

N=10

def create_mat(f):
    mat=np.zeros((N,N), dtype=np.int)
    for line in f:
        line=line.replace('<->',',')
        data=list(map(int,line.strip().split(",")))
        print(data)
        for i in range(1,len(data)):
            mat[data[0]][data[i]]=1
        mat[data[0]][data[0]]=1
    return(mat)

def read_pr(f):
    mat=[]
    for line in f:
        line=line.replace('<->',',')
        data=list(map(int,line.strip().split(",")))

        data=list(set(data))
        mat.append(data)

    #print(mat)
    return(mat)

def count_mat(mat, line):
    linked=mat[line].copy();
    validated=[]
    print("Treating line %i"%line)
    while(len(linked)!=0):
        element=linked[0]
        if (element in validated) == 0:
            new_elements=mat[element]
            for n in new_elements:
                if (n in validated) ==0:
                    if(n in linked) == 0:
                        linked.append(n)
            validated.append(element)
            linked.pop(0)
    return(validated)

def is_in_list(i, list):
    for l in list:
        if(i in l):
            return(True)
    return(False)


def find_groups(mat):
    groups=[]
    groups.append(count_mat(mat,0))
    N=len(mat[:])
    for i in range(1,N):
        print("Treating %i"%i)
        if(is_in_list(i,groups)==False):
            print("Append new group")
            groups.append(count_mat(mat,i))
    return(groups)

## MAIN LOOP
f = open("day12.txt",'r')
#f = open("day12short.txt",'r')
mat=read_pr(f)
valid=count_mat(mat,0)
print("Valid =",valid)
print("Number = %i"%len(valid))

groups=find_groups(mat)
print("Groups are:",groups)
print("Number of groups: %i "%len(groups[:]))
#print("linked to %i programs"%count_mat(mat,0))
