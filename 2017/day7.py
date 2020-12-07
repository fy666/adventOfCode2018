#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, copy, re



class node:
    def __init__(self, m_name,m_size=0):
        self.size=m_size
        self.name=m_name
        self.parent=[]
        self.sons=[]
        self.sons_name=[]

    def add_son(self,son):
        self.sons_name.append(son)

    def print(self, sym="_"):
        print(sym+"node name = %s"%(self.name))
        print(sym+"node size = %i"%self.size)
        #print(sym+"sons names :", self.sons_name)
        for son in self.sons:
            print(sym + "Sons nodes:")
            son.print(sym+sym+sym)

def read(f):
    list_of_orphans=[]
    list_of_parents=[]

    for line in f:
        memory = list(line.strip().split(" "))
        size=memory[1]
        regex=re.search("[(](\d+)[)]",size).group(1)

        new_node=node(memory[0], int(regex))
        N=len(memory)
        sons_names=[]
        if(N>3):
            for i in range(3,N):
                text=[]
                text=memory[i].split(",")
                new_node.add_son(text[0])
            list_of_parents.append(new_node)
        else:
            list_of_orphans.append(new_node)

    return(list_of_parents,list_of_orphans)

def print_lists(list_of_parents,list_of_orphans):
    print("Orphans are:")
    for orphan in list_of_orphans:
        orphan.print()

    print("parents are:")
    for p in list_of_parents:
        #print("--------------")
        p.print("_")

def print_list(list_of_orphans):
    for orphan in list_of_orphans:
        orphan.print("_")


def associate_nodes(list_of_parents,list_of_orphans):
    for io,orphan in enumerate(list_of_orphans):

        for ifa,father in enumerate(list_of_parents):
            for i,name in enumerate(father.sons_name):
                if(orphan.name==name):
                    list_of_parents[ifa].sons.append(orphan)
                    del list_of_parents[ifa].sons_name[i]
                    #print(orphan.name)

    list_of_orphans=[]
    new_list_of_fathers=[]

    for father in (list_of_parents):
        if(len(father.sons_name)!=0):
            new_list_of_fathers.append(father)
        else:
            list_of_orphans.append(father)


    return(new_list_of_fathers,list_of_orphans)

def branch_weight(branch):
    weight=branch.size;
    if(len(branch.sons)!=0): # top
        for root in branch.sons:
            weight+=branch_weight(root)
    return(weight)

def balance(tree):

    w=subweight(tree);
    ix=duplicate(w)
    # print("next")
    # subweight(tree.sons[0])
    # print("next")
    # subweight(tree.sons[0].sons[0])
    print("Unbalanced branch %i"%ix)


    while(ix!=-1):
        tree=tree.sons[ix]
        w=subweight(tree)
        ix=duplicate(w)
        ix=ix
        print("Unbalanced branch %i"%ix)


def subweight(branch):
    w=[]
    for son in branch.sons:
        weight=branch_weight(son)
        w.append(weight)
        print("Sub-branch %s weights %i, own weight = %i"%(son.name,weight, son.size))
    return(w)

def duplicate(l):
    for index,i in enumerate(l):
        count=0
        for j in l:
            if(i!=j):
                count+=1;
        if(count>1):
            return(index)
    return(-1)



f = open("day7.txt",'r')
#print("-----First step-----")
(list_of_parents,list_of_orphans)=read(f)
#print_lists(list_of_parents,list_of_orphans)
(list_of_parents,list_of_orphans)=associate_nodes(list_of_parents,list_of_orphans)
while(len(list_of_orphans)!=1):
    (list_of_parents,list_of_orphans)=associate_nodes(list_of_parents,list_of_orphans)
#print_list(list_of_orphans)
print(list_of_orphans[0].name)
balance(list_of_orphans[0])
