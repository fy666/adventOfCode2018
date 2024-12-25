import re
import numpy as np
import argparse
import copy
from collections import defaultdict, deque

OPERATIONS = {"AND": lambda x, y: x & y, "OR": lambda x, y: x | y, "XOR": lambda x, y: x ^ y}


def test():
    pass


def run_p2(registers, operations):
    while np.any([res.startswith("z") for _, _, res, _, _ in operations]):
        keys = []
        new_op = []
        for (a, b, res, op, _) in operations:
            if a in registers and b in registers:
                registers[res] = op(registers[a], registers[b])
                keys.append(res)
            else:
                new_op.append((a, b, res, op, _))
        operations = new_op
        # print(keys)
    return registers


def run_p1(registers, operations):
    count = 1
    while (len(operations) or np.any([res.startswith("z") for _, _, res, _ in operations])):
        (a, b, res, op, _) = operations.popleft()
        if a in registers and b in registers:
            registers[res] = op(registers[a], registers[b])
        else:
            operations.append((a, b, res, op, _))
    return registers


def get_z(registers):
    p1 = 0
    for k, d in registers.items():
        if k.startswith('z'):
            ix = int(k[1:])
            p1 += (2**ix)*d
    return p1


def get_eq(key, operations):
    if key not in operations:
        return key
    v1, v2, op = operations[key]
    equation = f"({get_eq(v1, operations)} {op} {get_eq(v2, operations)})"
    return equation


def find_errors(operations, last_bit=45):
    swaps = set()
    for res, d in operations.items():
        v1, v2, op = d
        if res.startswith("z"):
            if op != "XOR":
                num = int(res[1:])
                if num != last_bit:
                    swaps.add(res)
        else:
            if not (v1[0] in ['x', 'y']) and not (v2[0] in ['x', 'y']):
                if not (op in ["AND", "OR"]):
                    swaps.add(res)

        if op == "XOR" and (v1[0] in ['x', 'y']) and (v2[0] in ['x', 'y']):
            found = False
            num = int(v1[1:])
            if num == 0:
                continue
            for _, dd in operations.items():
                if (dd[0] == res or dd[1] == res) and dd[2] == "XOR":
                    found = True
                    break
            if not found:
                swaps.add(res)

        if op == "AND" and (v1[0] in ['x', 'y']) and (v2[0] in ['x', 'y']):
            found = False
            num = int(v1[1:])
            if num == 0:
                continue
            for _, dd in operations.items():
                if (dd[0] == res or dd[1] == res) and dd[2] == "OR":
                    found = True
                    break
            if not found:
                swaps.add(res)
    print("Part 2 :", ",".join(sorted(swaps)))


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

    # Apply operations
    revesed_op = {}
    operations = deque()
    for l in ops.split("\n"):
        tmp = l.split(" ")
        operations.append((tmp[0], tmp[2], tmp[4], OPERATIONS[tmp[1]], tmp[1]))
        revesed_op[tmp[4]] = (tmp[0], tmp[2], tmp[1])

    if False:
        new_reg = run_p1(registers, operations)
        print(f"Part 1 : {get_z(new_reg)}")

    new_reg = run_p2(registers, operations)
    print(f"Part 1 : {get_z(new_reg)}")
    find_errors(revesed_op)


if __name__ == "__main__":
    # test()
    main()
