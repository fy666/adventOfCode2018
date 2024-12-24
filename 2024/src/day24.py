import re
import numpy as np
import argparse
import copy
import heapq
from collections import defaultdict, deque
from numpy.dtypes import StringDType
import functools


OPERATIONS = {"AND": lambda x, y: x & y, "OR": lambda x, y: x | y, "XOR": lambda x, y: x ^ y}


def test():
    pass


def run_p2(registers, operations):
    while np.any([res.startswith("z") for _, _, res, _ in operations]):
        keys = []
        new_op = []
        for (a, b, res, op) in operations:
            if a in registers and b in registers:
                registers[res] = op(registers[a], registers[b])
                keys.append(res)
            else:
                new_op.append((a, b, res, op))
        operations = new_op
        print(keys)
    return registers


def run_p1(registers, operations):
    count = 1
    while (len(operations) or np.any([res.startswith("z") for _, _, res, _ in operations])):
        # print(f"{len(operations)} operations, {np.sum([res.startswith('z') for _, _, res, _ in operations])}")
        (a, b, res, op) = operations.popleft()
        if a in registers and b in registers:
            registers[res] = op(registers[a], registers[b])
        else:
            operations.append((a, b, res, op))
    return registers


def get_z(registers):
    p1 = 0
    for k, d in registers.items():
        if k.startswith('z'):
            ix = int(k[1:])
            p1 += (2**ix)*d
    return p1


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    parser.add_argument("-t2", "--test2", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]

    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"../data/test{day}.txt"
    elif args.test2:
        filename = f"../data/test{day}v2.txt"
    else:
        filename = f"../data/input{day}.txt"

    with open(f"{filename}", "r") as f:
        raw_data = f.read()

    reg, ops = raw_data.split("\n\n")
    registers = {}
    for r in reg.split("\n"):
        register, state = r.split(": ")
        registers[register] = int(state)

    print(registers)

    # Apply operations

    operations = deque()
    for l in ops.split("\n"):
        tmp = l.split(" ")
        operations.append((tmp[0], tmp[2], tmp[4], OPERATIONS[tmp[1]]))

    print(f"{len(operations)} operations")
    if False:
        new_reg = run_p1(registers, operations)
        print(f"Part 1 : {get_z(new_reg)}")

    new_reg = run_p2(registers, operations)
    print(f"Part 1 : {get_z(new_reg)}")


if __name__ == "__main__":
    # test()
    main()
