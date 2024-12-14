import re
import numpy as np
import argparse
import heapq
import itertools
from collections import deque
from sympy import symbols
from sympy.matrices import Matrix


def parse_data(input):
    result = []
    res = re.finditer(r'''\w:[^0-9]*(\d+),[^0-9]*(\d+)''', input)
    for r in res:
        # print(r, r.group(1), r.group(2))
        result.append(np.array([int(r.group(1)), int(r.group(2))]))
    # print(res)
    return (result)


def run(machine, mul=0):
    machineA, machineB, goal = machine
    # print(goal+mul)
    res = np.linalg.solve(
        np.array([[machineA[0], machineB[0]], [machineA[1], machineB[1]]]), goal+mul)
    x, y = symbols("x,y")
    A = Matrix([[machineA[0]/x, machineB[0]/y],
               [machineA[1]/x, machineB[1]/y]])
    b = Matrix([goal[0]+mul, goal[1]+mul])
    scires = A.solve(b)
    if "/" in str(scires[0]) or "/" in str(scires[1]):
        return 0
    a = int(str(scires[0]).split("*x")[0])
    b = int(str(scires[1]).split("*y")[0])
    return 3*a+b

    if np.all(np.abs(res - np.round(res)) < 1e-6):
        if mul == 0 and (res[0] > 100 or res[1] > 100):
            return 0
        if mul != 0:
            print(f"{res} is valid ({np.round(res)}) {scires}")
        return 3*np.round(res[0]) + np.round(res[1])
    # print(res)
    print(f"{res[0]} {res[1]} NOT valid")
    return 0


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"../data/test{day}.txt"
    else:
        filename = f"../data/input{day}.txt"

    with open(f"{filename}", "r") as f:
        raw_data = f.read()

    money = 0
    money2 = 0
    for r in raw_data.split("\n\n"):
        # print(f"{r}")
        res = parse_data(r)
        money += run(res)
        money2 += run(res, mul=10000000000000)

    print(f"Part 1 money = {int(money)}")
    print(f"Part 2 money = {int(money2)}")
    # break


if __name__ == "__main__":
    main()
