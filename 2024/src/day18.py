import re
import numpy as np
import argparse
import copy
import heapq
import datetime

DIRS = [np.array(x) for x in [[1, 0], [0, -1], [-1, 0], [0, 1]]]


def out_of_map(x, y, shape):
    return x < 0 or y < 0 or x > shape[0] or y > shape[1]


def find_path(start_pos, end_pos, shape, obstacles):
    v = set()
    v.add((0, 0))
    points = [(0, 0, start_pos[0], start_pos[1])]
    heapq.heapify(points)
    scores = {}
    # print(f"From {start_pos} -> {end_pos}, shape of {shape}, {len(obstacles)} obstacles")
    while len(points) > 0:
        score, steps, pos_x, pos_y = heapq.heappop(points)
        if pos_x == end_pos[0] and pos_y == end_pos[1]:
            return steps
        for d in DIRS:
            new_pos_x = pos_x + int(d[0])
            new_pos_y = pos_y + int(d[1])
            if out_of_map(new_pos_x, new_pos_y, shape):
                continue
            if not ((new_pos_x, new_pos_y) in obstacles):
                new_score = abs(end_pos[0] - new_pos_x) + abs(end_pos[1] - new_pos_y)+steps
                if new_score < scores.get((new_pos_x, new_pos_y), 1e9):
                    scores[(new_pos_x, new_pos_y)] = new_score
                    heapq.heappush(
                        points, (new_score+steps, steps+1, new_pos_x, new_pos_y))
    return None


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    parser.add_argument("-t2", "--test2", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"../data/test{day}.txt"
        end_goal = (6, 6)
        num = 12
    else:
        filename = f"../data/input{day}.txt"
        end_goal = (70, 70)
        num = 1024

    with open(f"{filename}", "r") as f:
        raw_data = f.read()

    obstacles = [tuple(map(int, x.split(","))) for x in raw_data.split("\n")]
    print(f"Reading {len(obstacles)} obstacles")
    res = find_path((0, 0), end_goal, end_goal, set(obstacles[:num]))
    print(f"Part 1: {res} steps")

    while res is not None:
        num += 1
        res = find_path((0, 0), end_goal, end_goal, set(obstacles[:num]))
    print(f"Part 2: {obstacles[num-1]}")


if __name__ == "__main__":
    main()
