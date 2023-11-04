#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
import requests
import urllib
from random import randint
import numpy as np
import time

f = open("day1.txt", 'r')
line = f.readline().strip("\n")  # player number
N = len(line)
H = int(N/2)
sum_1 = 0
sum_2 = 0
last_index1 = line[0]
print(line)
print(f"{N} chars")
print(H)
print(last_index1)
for i in range(N):
    if(line[(i+1) % N] == last_index1):
        sum_1 = sum_1+int(last_index1)
    else:
        last_index1 = line[(i+1) % N]

    last_index2 = line[i]
    if(line[(i+H) % N] == last_index2):
        sum_2 = sum_2+int(last_index2)

print(f"First sum {sum_1}")
print(f"Second sum {sum_2}")
