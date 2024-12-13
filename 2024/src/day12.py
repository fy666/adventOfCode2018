import re
import numpy as np
import argparse
import cv2 as cv
import itertools
from collections import deque

DIRS = [np.array(x) for x in [[1, 0], [-1, 0], [0, 1], [0, -1]]]
dir_names = ["x", "x", "y", "y"]

DIR_IX = [1, 1, 0, 0]
DIR_PIX = [0, 0, 1, 1]
DIR_ADD = [1, 0, 1, 0]


def is_in_map(pos, size):
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= size[0] or pos[1] >= size[1]:
        return False
    return True


def find_area(init_pos, my_map):
    points_in_area = set()
    points_to_visit = deque()
    points_to_visit.append(init_pos)

    while len(points_to_visit) > 0:
        point = points_to_visit.pop()
        points_in_area.add(tuple(point))
        for d in DIRS:
            new_pos = point + d
            if (
                is_in_map(new_pos, my_map.shape)
                and my_map[tuple(new_pos)] == my_map[tuple(init_pos)]
                and tuple(new_pos) not in points_in_area
            ):
                points_to_visit.append(new_pos)

    return points_in_area


def compute_perimeter(pos_list, shape):
    perimeter = 0
    for pos in pos_list:
        for d in DIRS:
            new_pos = np.array(pos) + d
            if not is_in_map(new_pos, shape) or tuple(new_pos) not in pos_list:
                perimeter += 1
    return perimeter


def find_perp(segments, seg):
    # segment: dir, ligne, start, stop
    d = "x"
    if seg[0] == "x":
        d = "y"
    for nseg in segments:
        if nseg[0:2] == [d, seg[3]]:
            if nseg[2] == seg[1] or nseg[3] == seg[1]:
                return True
    return False


def merge_segs(segments):
    need_to_merge = True
    while need_to_merge:
        found = False
        for i, j in itertools.product(range(len(segments)), range(len(segments))):
            if i == j:
                continue
            seg_i = segments[i]
            seg_j = segments[j]

            if seg_i[0:2] == seg_j[0:2]:
                if seg_i[3] == seg_j[2] and not find_perp(segments, seg_i):
                    seg_i[3] = seg_j[3]
                    found = True
                elif seg_i[2] == seg_j[3] and not find_perp(segments, seg_j):
                    seg_i[2] = seg_j[2]
                    found = True
            if found:
                del segments[j]
                break
        need_to_merge = (found == True)

    return segments


def compute_sides(pos_list, shape):
    perimeter = 0
    segments = []
    for pos in pos_list:
        pos = list(map(int, pos))
        # print(f"{pos}, Segment list = {segments}")
        for d_ix, d in enumerate(DIRS):
            new_pos = np.array(pos) + d
            if not is_in_map(new_pos, shape) or tuple(new_pos) not in pos_list:
                seg_s = pos[DIR_IX[d_ix]]
                seg_e = pos[DIR_IX[d_ix]] + 1
                seg = [dir_names[d_ix], pos[DIR_PIX[d_ix]] +
                       DIR_ADD[d_ix], seg_s, seg_e]
                segments.append(seg)
    segments = merge_segs(segments)
    return len(segments)


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

    my_map = np.array([list(x) for x in raw_data.split("\n")])
    print(f"Reading map of shape {my_map.shape}")

    visited_points = set()
    part1 = 0
    part2 = 0
    for pos in itertools.product(range(my_map.shape[0]), range(my_map.shape[1])):
        if pos in visited_points:
            continue
        res = find_area(np.array(pos), my_map)
        visited_points = visited_points.union(res)
        peri = compute_perimeter(res, my_map.shape)
        sides = compute_sides(res, my_map.shape)
        part1 += len(res) * peri
        part2 += sides * len(res)
        print(f"{pos}, {my_map[tuple(pos)]}: {len(res)}, {peri}, {sides}")
    print(f"Part 1 = {part1}")
    print(f"Part 2 = {part2}")


if __name__ == "__main__":
    main()
