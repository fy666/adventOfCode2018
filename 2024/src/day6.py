import re
import numpy as np
import copy

DIRS = [np.array(x) for x in [(-1, 0), (0, 1), (1, 0), (0, -1)]]


def is_out_next(pos, dir, size):
    new_pos = pos + dir
    if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= size[0] or new_pos[1] >= size[1]:
        # print(f"{new_pos} is out")
        return False
    return True


def run_once(pos, my_map):
    previous_pos = set()
    previous_pos_with_dir = set()
    dir_idx = 0
    previous_pos_with_dir.add(
        (pos[0], pos[1], DIRS[dir_idx][0], DIRS[dir_idx][1]))
    previous_pos.add(tuple(pos))

    while (is_out_next(pos, DIRS[dir_idx], my_map.shape)):
        new_pos = DIRS[dir_idx]+pos
        # print("NEW POS = ", new_pos,  my_map[*new_pos], type(new_pos))
        while my_map[*new_pos] == '#':
            dir_idx = (dir_idx+1) % len(DIRS)
            new_pos = DIRS[dir_idx]+pos
            # print(f"Turning at {pos}, new_dir = {dir_idx}")
        pos = new_pos
        item = (pos[0], pos[1], DIRS[dir_idx][0], DIRS[dir_idx][1])
        if item in previous_pos_with_dir:
            # print("Circling")
            return -1
        previous_pos.add(tuple(pos))
        previous_pos_with_dir.add(item)
    return previous_pos


def main():
    with open("../data/input6.txt", "r") as f:
        x = f.readlines()
    my_map = np.array([np.array([l for l in line.strip()]) for line in x])
    r = np.where(my_map == '^')
    pos = np.array([r[0][0], r[1][0]])
    my_map[*pos] = '.'

    res = run_once(pos, my_map)
    print(f"Part 1: {len(res)}")

    counter = 0
    for part in res:
        my_map[part[0], part[1]] = '#'
        # print(my_new_map)
        res = run_once(pos, my_map)
        if res == -1:
            counter += 1
        my_map[part[0], part[1]] = '.'
    print(f"Part 2: {counter}")


if __name__ == "__main__":
    main()
