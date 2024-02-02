import argparse
import queue
import copy
import re
import math
import numpy as np
from collections import defaultdict
import time
import heapq


ALL_DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
SLOPE = {'>': [(0, 1)], '^': [(-1, 0)], 'v': [(1, 0)], '<': [(0, -1)]}


def add(a, b):
    return (a[0]+b[0], a[1]+b[1])


def outOfBounds(pos, map_shape):
    for i in range(2):
        if pos[i] < 0 or pos[i] >= map_shape[i]:
            return True
    return False


def solve_part1(garden, part2=False):
    start_pos = (0, np.where(garden[0] == '.')[0][0])
    last = len(garden)-1
    end_pos = (last, np.where(garden[last] == '.')[0][0])
    print(
        f"Start pos at {start_pos}, end pose at {end_pos} garden shape of {garden.shape}")

    item = (0, start_pos, set(start_pos))
    items = []
    heapq.heappush(items, item)

    max_path = 0

    paths = {}

    while len(items) > 0:
        trail_score, curr, previous = heapq.heappop(items)
        if curr == end_pos:
            max_path = max(max_path, len(previous)-2)
            continue

        if not part2 and garden[curr] in ["<", "^", ">", "v"]:
            dirs = SLOPE[garden[curr]]
        else:
            dirs = ALL_DIRS

        for dir in dirs:
            new_pos = add(curr, dir)
            if outOfBounds(new_pos, garden.shape):
                continue
            if garden[new_pos] == '#':
                continue
            if new_pos not in previous:
                new_prev = copy.copy(previous)
                new_prev.add(new_pos)
                heapq.heappush(items, (trail_score-1, new_pos, new_prev))

    return max_path


def solve_graph(garden_graph, start_pos, end_pos):
    item = (0, start_pos, set(start_pos))
    items = []
    items.append(item)

    max_path = 0


    while len(items) > 0:
        trail_score, curr, previous = items.pop()
        if curr == end_pos:
            max_path = max(max_path, trail_score)
            continue

        for child, length in garden_graph[curr].items():
            if child not in previous:
                new_prev = copy.copy(previous)
                new_prev.add(child)
                items.append((trail_score+length, child, new_prev))

    return max_path


def main():
    parser = argparse.ArgumentParser(description="Day23")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    file = "./src/files/day23.txt"
    if args.ex:
        file = "./src/files/day23ex.txt"

    garden = []
    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            garden.append(list(line.strip()))
    garden = np.array(garden)
    print(f"Part 1 = {solve_part1(garden, part2=False)}")
    if False and args.ex:
        print(f"Part 2 = {solve_part1(garden, part2=True)}")  # Too slow

    # Convert map to graph
    graph = defaultdict(dict)
    for il, line in enumerate(garden):
        for ic, col in enumerate(line):
            if col == '#':
                continue
            for dir in ALL_DIRS:
                new_pos = add((il, ic), dir)
                if outOfBounds(new_pos, garden.shape):
                    continue
                if garden[new_pos] == '#':
                    continue
                graph[(il, ic)][new_pos] = 1

    start_pos = (0, np.where(garden[0] == '.')[0][0])
    last = len(garden)-1
    end_pos = (last, np.where(garden[last] == '.')[0][0])

    # Reduce graph
    for key, data in graph.items():
        if len(data) == 2:
            dict_as_list = list(data.items())
            pos_in, steps_in = dict_as_list[0]
            pos_out, steps_out = dict_as_list[1]
            graph[pos_in][pos_out] = steps_out + graph[pos_in][key]
            del(graph[pos_in][key])
            graph[pos_out][pos_in] = steps_in + graph[pos_out][key]
            del(graph[pos_out][key])

    ans = solve_graph(graph, start_pos, end_pos)
    print(f"Part 2 = {ans}")

if __name__ == "__main__":
    main()
