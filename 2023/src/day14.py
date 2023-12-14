import numpy as np
import itertools
import argparse
from functools import cache


def tilt(map):
    t = np.array(map).transpose()
    res = []
    for column in t:
        # with no rocks at all
        new_column = [x if x != 1 else 0 for x in column]
        closest_border = 0
        for ix, x in enumerate(column):
            if x == 2:
                closest_border = ix + 1
                continue
            if x == 1:
                new_column[closest_border] = 1
                closest_border += 1
        res.append(new_column)
    return np.array(res).transpose()


def get_weight(map):
    w = 0
    l = len(map)
    for im, m in enumerate(map):
        rocks_in_line = (m == 1).sum()
        # print(f"{rocks_in_line} rocks in line {m} * {(l-im)}")
        w += rocks_in_line * (l - im)
    return w


def find_cycles(map):
    cycles = 1000  # 1000000000
    weights = []
    for i in range(cycles):
        map = tilt(map)  # North
        map = tilt(np.rot90(map, -1))  # West
        map = tilt(np.rot90(map, -1))  # South
        map = tilt(np.rot90(map, -1))  # East
        map = np.rot90(map, -1)
        w = get_weight(map)
        weights.append(w)
        for x in weights:
            if weights.count(x) == 4:
                pos = np.where(weights == x)[0]
                if pos[1] - pos[0] > 5:
                    if weights[pos[0]:pos[1]] == weights[pos[1]:pos[2]]:
                        return weights


def main():
    parser = argparse.ArgumentParser(description="Day14")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    file = "day14.txt"
    if args.ex:
        file = "day14ex.txt"

    map = []
    corr = {'O': 1, '#': 2, ".": 0}
    with open(file, "r") as f:
        for line in f.readlines():
            nums = np.array([corr[x] for x in line.strip()])
            map.append(nums)

    res = tilt(map)
    print(f"Part 1 res = {get_weight(res)}")
    map = np.array(map)

    weights = find_cycles(map)
    index = np.where(weights == weights[-1])[0]

    cycle = index[1] - index[0]
    print(f"{index}, cycle = {cycle}")
    wanted_cycles = 1000000000
    rem = (wanted_cycles - index[0]) % cycle

    print(f"Part 2 res = {weights[rem+index[0]-1]}")


if __name__ == "__main__":
    main()
