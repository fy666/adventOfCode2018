#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time

f = open("day4.txt",'r')
sum=0
sum2=0;
#print(f.readlines())

def first():
    valid_pass=0
    repeat=0

    for line in f:
        repeat=0
        password = list(line.strip().split(" "))
        N=len(password)
        print(password)
        print(N)
        for i in range(N):
            for j in range(i+1,N):
                if(password[i]==password[j]):
                    repeat=1;
                    print("repetition")

        if(repeat==0):
            valid_pass=valid_pass+1
        print(valid_pass)

    print(valid_pass)

def second():
    valid_pass=0
    repeat=0

    for line in f:
        repeat=0
        password = list(line.strip().split(" "))
        N=len(password)
        print(password)
        print(N)
        list_lettre=[]
        for passw in password:
            list_lettre.append(letter_used(passw))
        print(list_lettre)
        for i in range(N):
            for j in range(i,N):
                if(i!=j):
                    if(list_lettre[i]==list_lettre[j]):
                        repeat=1;
                        print("repetition")

        if(repeat==0):
            valid_pass=valid_pass+1
        print(valid_pass)

    print(valid_pass)

def letter_used(mot):
    le=sorted(mot)
    NN=len(le)
    lettre=[]
    lettre.append(le[0])
    index=0
    for i in range(NN):
        if(le[i]!=lettre[index]):
            lettre.append(le[i])
            index=index+1
    return(lettre)


#print(letter_used("chatteard"))
second()

    #for pass in password:
