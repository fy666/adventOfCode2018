#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys, os, requests,urllib
from random import randint
import numpy as np
import time, re, operator

L=16 #number of programs

class program:
    def __init__(self):
        self.dico=dict()
        self.word=[]
        self.rule=[]
        self.new_word = ['a' for x in range(L)]
        #self.op=None
        for i in range(L):
            self.dico[chr(97+i)] = i
            self.word.append(chr(97+i))
            self.rule.append(1)

    def spin(self,step):
        for i in range(L):
            self.dico[chr(97+i)] = (self.dico[chr(97+i)] + step)%L

    def partner(self, char):
        char1,char2 = char
        self.dico[char1],self.dico[char2] = self.dico[char2],self.dico[char1]

    def exchange(self,pos):
        pos1,pos2 = pos
        self.update_word();
        char1=self.word[pos1]
        char2=self.word[pos2]
        self.partner((char1,char2))

    def update_word(self):
        for key in self.dico:
            self.word[self.dico[key]]=key

    def print(self):
        self.update_word()
        s=''
        for i in self.word :
            s+=i
        #print(self.word)
        print(s)

    def print_alone(self):
        s=''
        for i in self.word :
            s+=i
        print(s)

    def deduce_rule(self):
        self.update_word()
        for i in range(L):
            self.rule[i]=self.word.index(chr(97+i))
        #self.op=operator.itemgetter((self.rule))

    def apply_rule(self):
        #print(self.op)
        #self.word =self.op(self.word)
        #print(self.word)
        for i in range(L):
            self.new_word[self.rule[i]]=self.word[i]
        self.word = self.new_word.copy()

    #def apply_fast_rule(self):

def read_dance():
    moves=[]
    f = open("day16.txt",'r')
    for line in f:
        data=list(line.strip().split(","))
        for instr in data:
            #print(instr)
            #game.print()
            if instr[0]=='s':
                regex=re.search("([a-z])(\d+)",instr)
                #game.spin(int(regex.group(2)))

                moves.append((game.spin,(int(regex.group(2)))))

                #print("Spin of %i"%int(regex.group(2)))
            elif instr[0]=='p':
                regex=re.search("([a-z])([a-z])/([a-z])",instr)
                #game.partner(regex.group(2),regex.group(3))
                moves.append((game.partner,(regex.group(2),regex.group(3))))
                #print("Partner %s and %s"%(regex.group(2),regex.group(3)))
            elif instr[0]=='x':
                regex=re.search("([a-z])(\d+)/(\d+)",instr)
                #game.exchange(int(regex.group(2)),int(regex.group(3)))
                moves.append((game.exchange,(int(regex.group(2)),int(regex.group(3)))))
                #print("Exchange %s and %s"%(int(regex.group(2)),int(regex.group(3))))
            #game.print()
            #input('couocu')
    return(moves)

    #game.print()

## MAIN LOOP : exploit the repetition patten 
game=program()
moves=read_dance()
N=1000000000
result=[];
result.append(game.word.copy())
print(0, result[0])
for n in range(N):
    for i in moves:
        i[0](i[1])

    game.update_word()
    for ix,j in enumerate(result):
        if(j==game.word):
            #print(n,j)
            print("%i repeat same as %i"%(n+1,ix))
            print("same as 1 billion after %i operations"%(N%(n+1)))
            print(result[N%(n+1)])
            input("end")
    result.append(game.word.copy())
    print(n+1, result[n+1])

game.print()
