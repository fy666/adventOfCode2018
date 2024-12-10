import numpy as np
from itertools import permutations
import copy


def get_index(x, item):
    if item in x:
        return x.index(item)
    else:
        return None


def valid_update(rules, update):
    for d0, d1 in rules:
        if ((ix1 := get_index(update, d0)) is not None) & ((ix2 := get_index(update, d1)) is not None):
            if ix1 > ix2:
                return False
    return True


def make_valid_update(rules, update):
    tmp = copy.deepcopy(update)
    while not valid_update(rules, tmp):
        for d0, d1 in rules:
            if ((ix1 := get_index(tmp, d0)) is not None) & ((ix2 := get_index(tmp, d1)) is not None):
                if ix1 > ix2:
                    tmp[ix1], tmp[ix2] = tmp[ix2], tmp[ix1]

    return tmp


def get_valid_update(rules, update):
    for c in permutations(update, len(update)):
        if valid_update(rules, list(c)):
            return c


if __name__ == "__main__":
    test = False
    filename = "input" + "5.txt"
    if test:
        filename = "test" + "5.txt"
    with open(filename, "r") as f:
        d = f.read()
    rules, updates = d.split("\n\n")
    rules = [tuple(map(int, rule.split("|"))) for rule in rules.split("\n")]
    updates = [list(map(int, update.split(","))) for update in updates.split("\n")]

    sum_part1 = 0
    sum_part2 = 0
    for update in updates:
        res = valid_update(rules, update)
        if res:
            # print(f"Adding {update[int(np.floor(len(update) / 2))]}")
            sum_part1 += update[int(np.floor(len(update) / 2))]
        else:
            # ORDER IT
            fixed_update = make_valid_update(rules, update)
            # print(f"FIX {update} -> {fixed_update}")
            # print(f"Adding {fixed_update[int(np.floor(len(fixed_update) / 2))]}")
            sum_part2 += fixed_update[int(np.floor(len(fixed_update) / 2))]
        # print(f"{update} is {res}")

    print(f"Part 1 = {sum_part1}")
    print(f"Part 2 = {sum_part2}")
