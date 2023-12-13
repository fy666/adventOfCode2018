import regex as re
import numpy as np
import itertools
from functools import cache


def get_symmetry(pattern, ftype):
    l = len(pattern[:][:])
    for ic, (l1, l2) in enumerate(zip(pattern[:], pattern[1:])):
        # print(l1,l2)
        if (l1 == l2).all():
            num_lines_sym = min(ic + 1, l - ic - 1)
            # print(f"Found two lines that are equal at {ic}, {num_lines_sym} lines")
            sub_mat = pattern[ic - num_lines_sym + 1: ic + 1]
            # check that the symmetry is complete
            f = np.flip(pattern[ic + 1: ic + num_lines_sym + 1], 0)
            if (sub_mat == f).all():
                #print(f"{ftype} symmetry confirmed at {ic}")
                return ic
    return None


def get_almost_symmetry(pattern, ftype):
    l = len(pattern[:][:])
    for ic, (l1, l2) in enumerate(zip(pattern[:], pattern[1:])):
        if (l1 == l2).sum() >= (len(l1)-1):
            num_lines_sym = min(ic + 1, l - ic - 1)
            sub_mat = pattern[ic - num_lines_sym + 1: ic + 1]
            f = np.flip(pattern[ic + 1: ic + num_lines_sym + 1], 0)
            if (sub_mat == f).sum() == (sub_mat.size-1):
                #print(f"{ftype} almost symmetry confirmed at {ic}")
                return ic
    return None


def process_pattern(pattern):
    pattern = np.array(pattern)
    h, v = None, None
    h = get_symmetry(pattern, "horizontal")
    t = pattern.transpose()
    v = get_symmetry(t, "vertical")
    #print(f"H = {h}, v = {v}")
    if h is not None:
        return (h + 1)*100
    if v is not None:
        return (v + 1) * 1
    return 0


def process_pattern2(pattern):
    pattern = np.array(pattern)
    h, v = None, None
    h = get_almost_symmetry(pattern, "horizontal")
    t = pattern.transpose()
    v = get_almost_symmetry(t, "vertical")
    #print(f"H = {h}, v = {v}")
    if h is not None:
        return (h + 1)*100
    if v is not None:
        return (v + 1) * 1
    return 0


def main():
    part1 = 0
    part2 = 0
    pattern = []
    with open("./src/files/day13.txt", "r") as f:
        for il, line in enumerate(f.readlines()):
            if line == "\n":
                part1 += process_pattern(pattern)
                part2 += process_pattern2(pattern)
                pattern = []
                pass
            else:
                nums = [0 if x == '.' else 1 for x in line.strip()]
                pattern.append(nums)
    part1 += process_pattern(pattern)
    part2 += process_pattern2(pattern)

    print(f"Part 1 res = {part1}")
    print(f"Part 2 res = {part2}")


if __name__ == "__main__":
    main()
