import argparse
import queue
import copy
import re
import math
import numpy as np
from collections import deque
import time


def add(a, b):
    return (a[0]+b[0], a[1]+b[1])


def outOfBounds(pos, map_shape):
    for i in range(2):
        if pos[i] < 0 or pos[i] >= map_shape[i]:
            return True
    return False


def infinitePos(pos, map_shape):
    return (pos[0] % map_shape[0], pos[1] % map_shape[1])


def solve(garden, max_step, infinite_map, use_queue=False):
    tmp = np.where(garden == 2)
    start_pos = (tmp[0][0], tmp[1][0])
    # print(f"Start pos at {start_pos}, garden shape of {garden.shape}")

    item = (start_pos, 0)
    visited_pos = {}
    if use_queue:
        items = queue.Queue()
    else:
        items = deque()

    if use_queue:
        items.put(item)
    else:
        items.append(item)

    # count_possibilities = set()
    count_possibilities = 0
    if use_queue:
        def x(s): return not s.empty()
    else:
        def x(s): return len(s) > 0

    while x(items):
        if use_queue:
            curr, steps = items.get()
        else:
            curr, steps = items.popleft()

        if steps == max_step:
            count_possibilities += 1
            # count_possibilities.add(curr)
            continue
        steps += 1
        for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = add(curr, dir)
            if not infinite_map and outOfBounds(new_pos, garden.shape):
                continue
            if garden[infinitePos(new_pos, garden.shape)] == 1:
                continue
            if (new_pos in visited_pos and visited_pos[new_pos] < steps) or (new_pos not in visited_pos):
                visited_pos[new_pos] = steps
                if use_queue:
                    items.put((new_pos, steps))
                else:
                    items.append((new_pos, steps))
    return count_possibilities  # len(count_possibilities)


def main():
    parser = argparse.ArgumentParser(description="Day21")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    file = "./src/files/day21.txt"
    if args.ex:
        file = "./src/files/day21ex.txt"

    garden = []
    corr = {".": 0, "#": 1, 'S': 2}
    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            garden.append(np.array([corr[x] for x in line.strip()]))
    # print(garden)
    garden = np.array(garden)

    t = time.time()
    print(
        f"Part 1: {solve(garden, 6 if args.ex else 64, infinite_map=False)} steps ({time.time()-t} s)")
    t = time.time()
    print(
        f"Part 1 (queue): {solve(garden, 6 if args.ex else 64, infinite_map=False, use_queue=True)} steps ({time.time()-t} s)")

    t = time.time()
    print(
        f"Part 2: {solve(garden, 50 if args.ex else 26501365, infinite_map=True)} steps ({time.time()-t} s)")
    t = time.time()
    print(
        f"Part 2 (queue): {solve(garden, 50 if args.ex else 26501365, infinite_map=True, use_queue=True)} steps ({time.time()-t} s)")


if __name__ == "__main__":
    main()
