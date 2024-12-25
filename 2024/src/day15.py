import re
import numpy as np
import argparse
import copy
import heapq
from collections import defaultdict
from numpy.dtypes import StringDType
import functools
import sys

DIRS = {"^": [-1, 0], "v": [1, 0], ">": [0, 1], "<": [0, -1]}


def is_in_map(pos, size):
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= size[0] or pos[1] >= size[1]:
        return False
    return True


def print_map(start_pos, boxes, walls, shape):
    for i in range(shape[0]):
        st = ""
        for j in range(shape[1]):
            if i == start_pos[0] and j == start_pos[1]:
                st += "@"
            elif (i, j) in boxes:
                st += "O"
            elif (i, j) in walls:
                st += "#"
            else:
                st += "."
        print(st)


def move_to_next_free_spot(pos, walls, boxes, direction, shape):
    n_x = pos[0] + direction[0]
    n_y = pos[1] + direction[1]
    if (n_x, n_y) in walls:
        return False
    if (n_x, n_y) in boxes:
        if move_to_next_free_spot((n_x, n_y), walls, boxes, direction, shape):
            boxes.remove(pos)
            boxes.add((n_x, n_y))
            return True
        else:
            return False
    else:
        boxes.remove(pos)
        boxes.add((n_x, n_y))
        return True


def compute_score(boxes):
    sum_p1 = 0
    for x, y in boxes:
        sum_p1 += (x*100+y)
    return sum_p1


def run(start_pos, boxes, walls, moves, shape):
    pos_x, pos_y = start_pos
    for move in moves:
        next_x = pos_x + DIRS[move][0]
        next_y = pos_y + DIRS[move][1]
        if (next_x, next_y) in walls:
            continue
        elif (next_x, next_y) in boxes:
            moved = move_to_next_free_spot((next_x, next_y), walls, boxes, DIRS[move], shape)
            if not moved:
                continue

        pos_x = next_x
        pos_y = next_y

    print(f"Part 1 : {compute_score(boxes)}")

############################### PART 2 ################################


def compute_score2(boxes, boxes_link):
    sum_p1 = 0
    for x, y in boxes:
        bx, by = boxes_link[(x, y)]
        if y < by:
            sum_p1 += (x*100+y)
    return sum_p1


def get_boxes_moves(pos, walls, boxes, boxes_link, direction, shape):
    boxes_to_push = set()
    boxes_to_move = set()
    boxes_to_push.add(pos)
    while len(boxes_to_push):
        box = boxes_to_push.pop()
        nx, ny = box[0] + direction[0], box[1] + direction[1]
        other_box = boxes_link[box]
        mx, my = other_box[0] + direction[0], other_box[1] + direction[1]
        if (mx, my) in walls or (nx, ny) in walls:
            return []
        boxes_to_move.add(box)
        boxes_to_move.add(other_box)
        if (mx, my) in boxes and not (mx, my) in boxes_to_move:
            boxes_to_push.add((mx, my))
        if (nx, ny) in boxes and not (nx, ny) in boxes_to_move:
            boxes_to_push.add((nx, ny))

    return boxes_to_move


def run2(start_pos, boxes, boxes_link, walls, moves, shape):
    pos_x, pos_y = start_pos
    show_map = False
    for im, move in enumerate(moves):
        if show_map:
            print_map((pos_x, pos_y), boxes, walls, shape)
            print(f"---------------------\n{im} Next move: {move} {DIRS[move]}")
        show_map = False
        next_x = pos_x + DIRS[move][0]
        next_y = pos_y + DIRS[move][1]
        if (next_x, next_y) in walls:
            continue
        elif (next_x, next_y) in boxes:
            to_move = get_boxes_moves((next_x, next_y), walls, boxes, boxes_link, DIRS[move], shape)
            if len(to_move) == 0:
                continue
            boxes_to_add = set()
            new_box_link = {}
            for bx, by in to_move:
                nx = int(bx + DIRS[move][0])
                ny = int(by + DIRS[move][1])
                if (bx, by) in boxes:
                    boxes.remove((bx, by))
                boxes_to_add.add((nx, ny))
                other_box = boxes_link[(bx, by)]
                mx, my = other_box[0] + DIRS[move][0], other_box[1] + DIRS[move][1]
                new_box_link[(nx, ny)] = (mx, my)
                new_box_link[(mx, my)] = (nx, ny)
                boxes_to_add.add((mx, my))
                if (mx, my) in boxes:
                    boxes.remove((mx, my))

            boxes = boxes.union(boxes_to_add)
            boxes_link.update(new_box_link)

        pos_x = next_x
        pos_y = next_y

    print(f"Part 2 : {compute_score2(boxes, boxes_link)}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    parser.add_argument("-t2", "--test2", action="store_true")  # on/off flag
    parser.add_argument("-t3", "--test3", action="store_true")  # on/off flag

    args = parser.parse_args()

    filename = __file__.split("/")[-1]

    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"../data/test{day}.txt"
    elif args.test2:
        filename = f"../data/test{day}v2.txt"
    elif args.test3:
        filename = f"../data/test{day}v3.txt"
    else:
        filename = f"../data/input{day}.txt"

    with open(f"{filename}", "r") as f:
        raw_data = f.read()
    my_map, moves = raw_data.split("\n\n")
    moves = moves.replace("\n", "")
    my_map = np.array([list(x) for x in my_map.split("\n")])
    print(f"Found {len(moves)} moves and a map of shape {my_map.shape}")
    r = np.where(my_map == '@')
    start_pos = np.array([r[0][0], r[1][0]])

    boxes = set()
    walls = set()
    for x, y in zip(*np.where(my_map == 'O')):
        boxes.add((int(x), int(y)))

    for x, y in zip(*np.where(my_map == '#')):
        walls.add((int(x), int(y)))

    print(f"Starting at {start_pos} {len(boxes)} boxes {len(walls)} walls")
    run(start_pos, boxes, walls, moves, my_map.shape)

    # ********** PART 2 **************
    shape = my_map.shape
    walls_p2 = set()
    for x, y in zip(*np.where(my_map == '#')):
        walls_p2.add((int(x), 2*int(y)))
        walls_p2.add((int(x), 2*int(y)+1))

    boxes = set()
    boxes_link = {}
    for x, y in zip(*np.where(my_map == 'O')):
        b1 = (int(x), 2*int(y))
        b2 = (int(x), 2*int(y)+1)
        boxes.add(b1)
        boxes.add(b2)
        boxes_link[b1] = b2
        boxes_link[b2] = b1
    start_pos = np.array([r[0][0], 2*r[1][0]])
    run2(start_pos, boxes, boxes_link, walls_p2, moves, (shape[0], shape[1]*2))


if __name__ == "__main__":
    main()
