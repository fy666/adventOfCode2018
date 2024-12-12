import re
import numpy as np
import argparse
import cv2 as cv
import itertools
from collections import deque

DIRS = [np.array(x) for x in [[1, 0], [-1, 0], [0, 1], [0, -1]]]


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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"test{day}.txt"
    else:
        filename = f"input{day}.txt"

    # im = np.random.randint(0, 4, (10, 10), dtype="uint8")
    # # im2 = copy.copy(im)

    # P = np.array(((-1, -1), (-1, 1), (1, 1), (1, -1))) / 2  # contour through pixel edes
    # print(im)
    # a = cv.findContours((im == 0).astype("uint8"), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # print(a)
    # U = [
    #     np.squeeze(c)
    #     for i in range(1, 1 + np.max(im))
    #     for c in cv.findContours((im == i).astype("uint8"), cv.RETR_FLOODFILL, cv.CHAIN_APPROX_NONE)[0]
    # ]
    # sum = 0
    # for i in U:
    #     sum += len(i)
    # print(sum)
    # # U2 = [enhance_contour(u, P) for u in U]

    with open(f"{filename}", "r") as f:
        raw_data = f.read()

    my_map = np.array([list(x) for x in raw_data.split("\n")])
    print(f"Reading map of shape {my_map.shape}")

    visited_points = set()
    part1 = 0
    for pos in itertools.product(range(my_map.shape[0]), range(my_map.shape[1])):
        if pos in visited_points:
            continue
        res = find_area(np.array(pos), my_map)
        visited_points = visited_points.union(res)
        peri = compute_perimeter(res, my_map.shape)
        part1 += len(res) * peri
        print(f"{pos}, {my_map[tuple(pos)]}: {len(res)}, {peri}")
        # print(ix, iy)
    print(f"Part 1 = {part1}")


if __name__ == "__main__":
    main()
