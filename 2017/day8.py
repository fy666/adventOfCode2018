#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, re

def dict_check(dico,key):
    value=dico.get(key, "ERROR")
    if(value=="ERROR"):
        dico[key]=0;
        value=dico.get(key,"ERROR")
    return(dico,value)

def cond_check(value1, value2,str_cond):
    if(str_cond=='=='):
        return(value1 == value2)
    if(str_cond=='>='):
        return(value1 >= value2)
    if(str_cond=='<='):
        return(value1 <= value2)
    if(str_cond=='!='):
        return(value1 != value2)
    if(str_cond=='<'):
        return(value1 < value2)
    if(str_cond=='>'):
        return(value1 > value2)


def do_instr():
    add=False; # 1 add, 0 substract
    cond=False;
    dico=dict();
    max_val=0;
    for line in f:
        print(dico)
        regex=re.search("([a-z]+) ([a-z]+) (\d+|-\d+) if ([a-z]+) (\W+) (\d+|-\d+)",line)
        print(line)
        #print(regex.groups())
        var_name=regex.group(1)
        add=(regex.group(2)=='inc')
        value=int(regex.group(3))
        var_cond=regex.group(4)
        logic=regex.group(5)
        val_logic=int(regex.group(6))
        print("Add logic = %i, value= %i"%(add,value))
        ## COND
        (dico,var_value)=dict_check(dico,var_name)
        (dico,cond_value)=dict_check(dico,var_cond)
        if(cond_check(cond_value, val_logic,logic)):
            if(add==0):
                value=-value
            dico[var_name]=var_value + value
        max_val=max(max_val,max(dico.values()))
    return(dico,max_val)

## MAIN LOOP
f = open("day8.txt",'r')
(dico,max_val)=do_instr()
print(dico.values())
print("Max value %i"%max(dico.values()))
print(max_val)
