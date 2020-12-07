#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, re

def clear_seq(seq):
    pass_next=0
    cleared=0
    new_seq=[]
    garbage=0
    for f in seq:
        if(pass_next):
            pass_next=0
        else:
            if(f=='<' and cleared==0):
                cleared=1
            elif(f == '>' and cleared==1):
                cleared=0
            elif(f == '!'):
                pass_next=1
            elif(cleared==0):
                new_seq.append(f)
            else:
                garbage +=1
    return(new_seq, garbage)

def score(seq):
    tmp_score=[0]
    score=0
    for f in seq:
        if(f=='}'):
            score+=tmp_score.pop()
        elif(f=='{'):
            tmp_score.append(tmp_score[-1]+1)
    return(score)



## MAIN LOOP
f = open("day9.txt",'r')
seq=f.read()

#seq='{{<ab>},{<ab>},{<ab>},{<ab>}}'
#seq='{{<!!>},{<!!>},{<!!>},{<!!>}}'
(cseq,garbage)=clear_seq(seq)
print('Old seq : ', seq)
print('Cleared seq :', cseq)
print("score = %i"%score(cseq))
print("Garbage = %i"%garbage)
