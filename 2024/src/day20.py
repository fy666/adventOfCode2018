import re
import numpy as np
import argparse
import copy
import heapq
from collections import defaultdict
from numpy.dtypes import StringDType
import functools

DIRS = [np.array(x) for x in [[1, 0], [0, -1], [-1, 0], [0, 1]]]


def out_of_map(x, y, shape):
    return x < 0 or y < 0 or x >= shape[0] or y >= shape[1]


def find_best_path(start_pos, end_pos, my_map):
    v = set()
    v.add((0, 0))
    points = [(0, 0, start_pos[0], start_pos[1], [(start_pos[0], start_pos[1])])]
    heapq.heapify(points)
    scores = {(start_pos[0], start_pos[1]): 0}
    # print(f"From {start_pos} -> {end_pos}, shape of {shape}, {len(obstacles)} obstacles")
    while len(points) > 0:
        score, steps, pos_x, pos_y, positions = heapq.heappop(points)
        if pos_x == end_pos[0] and pos_y == end_pos[1]:
            return steps, positions, scores
        for d in DIRS:
            new_pos_x = pos_x + int(d[0])
            new_pos_y = pos_y + int(d[1])
            if out_of_map(new_pos_x, new_pos_y, my_map.shape):
                continue
            new_steps = steps + 1
            if my_map[new_pos_x, new_pos_y] != '#':
                new_score = new_steps  # abs(end_pos[0] - new_pos_x) + abs(end_pos[1] - new_pos_y)+new_steps
                if new_score < scores.get((new_pos_x, new_pos_y), 1e9):
                    new_positions = copy.copy(positions)
                    new_positions.append((new_pos_x, new_pos_y))
                    scores[(new_pos_x, new_pos_y)] = new_score
                    heapq.heappush(
                        points, (new_score, new_steps, new_pos_x, new_pos_y, new_positions))
    return None


@functools.cache
def get_manhattan(d):
    pts = set()
    for i in range(d):
        for j in range(d-i+1):
            if i == 0 and j == 0:
                continue
            pts.add((i, j))
            pts.add((j, i))

            pts.add((-i, -j))
            pts.add((-j, -i))

            pts.add((-i, j))
            pts.add((j, -i))

            pts.add((i, -j))
            pts.add((-j, i))
    return pts


def get_jumps(pos_x, pos_y, d, my_map):
    res = []
    for x, y in get_manhattan(d):
        nx = pos_x + x
        ny = pos_y + y
        if not out_of_map(nx, ny, my_map.shape) and my_map[nx, ny] != '#':
            res.append((pos_x, pos_y, nx, ny))
    return res


def test():
    res = get_manhattan(1)
    print(res, len(res))
    res = get_manhattan(2)
    print(res, len(res))
    res = get_manhattan(3)
    print(res, len(res))
    res = get_manhattan(4)
    print(res, len(res))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    parser.add_argument("-t2", "--test2", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]

    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"../data/test{day}.txt"
        diff = 50
    else:
        filename = f"../data/input{day}.txt"
        diff = 100

    with open(f"{filename}", "r") as f:
        raw_data = f.read()

    my_map = np.array([list(x) for x in raw_data.split("\n")],  dtype=StringDType())
    print(f"Reading map of shape {my_map.shape}")

    start_pos = np.where(my_map == 'S')
    start_pos = (int(start_pos[0][0]), int(start_pos[1][0]))
    print(f"Start pos is {start_pos}")

    end_pos = np.where(my_map == 'E')
    end_pos = (int(end_pos[0][0]), int(end_pos[1][0]))
    print(f"End pos is {end_pos}")

    original_time, best_path, scores_dep = find_best_path(start_pos, end_pos, my_map)
    _, _, scores_arr = find_best_path(end_pos, start_pos, my_map)

    tiles = np.where(my_map != '#')
    N = 20
    jumps = []
    sum_p1 = 0
    for ix, (x, y) in enumerate(zip(tiles[0], tiles[1])):
        jumps += get_jumps(x, y, N, my_map)
    print(f"Found {len(jumps)} jumps")

    saved_time_d = defaultdict(lambda: 0)
    for start_x, start_y, stop_x, stop_y in jumps:
        if (stop_x, stop_y) not in scores_arr:
            print(f"{stop_x}, {stop_y} Not found")
        if (start_x, start_y) not in scores_dep:
            print(f"{start_x}, {start_y} Not found")
        manathan_d = int(abs(start_x-stop_x) + abs(start_y-stop_y))
        new_time = scores_dep[(start_x, start_y)] + manathan_d + scores_arr[(stop_x, stop_y)]
        saved_time = original_time - new_time
        if saved_time >= 100:
            sum_p1 += 1
        if args.test and saved_time > 0:
            saved_time_d[saved_time] += 1
    if args.test:
        for x in [2, 4, 6, 8, 10, 12, 20, 36, 38, 40, 64]:
            print(f"{saved_time_d[x]} cheats save {x} picoseconds")
        print(saved_time_d)
    print(f"Part 1 = {sum_p1}")


if __name__ == "__main__":
    # test()
    main()
