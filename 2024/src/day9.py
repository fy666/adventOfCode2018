import re
import numpy as np
import copy
import argparse
import itertools
import re
import math


def compute_checksum(disk_state):
    ix = 0
    checksum = 0
    for file_id, size in disk_state:
        # print(f"File_id is {file_id}, at ix = {ix}")
        if file_id == -1:
            file_id = 0
        for i in range(size):
            # print(f"{file_id} * {(i+ix)}")
            checksum += file_id * (i+ix)
        ix += size
    print(f"Checksum is {checksum}")
    return checksum


def create_index(txt):
    result = []
    file_index = 0
    for itx, t in enumerate(txt):
        if itx % 2 == 0:
            # file
            result.append([file_index, int(t)])
            file_index += 1
        else:
            result.append([-1, int(t)])

    print(result)
    return result


def simplify(disk_state):
    ix_empty = 0
    ix_full = len(disk_state)-1
    work_to_do = True
    while work_to_do:
        ix_empty = 0
        ix_full = len(disk_state)-1
        # print(f"Disk state = {disk_state}")
        while disk_state[ix_empty][0] != -1:
            ix_empty += 1
        while disk_state[ix_full][0] == -1:
            ix_full -= 1
        if ix_full < ix_empty:
            break
        empty_size = disk_state[ix_empty][1]
        file_id, file_size = disk_state[ix_full]
        # same size
        # print(f"Empty at {ix_empty}, file at {ix_full}")
        if empty_size == file_size:
            disk_state[ix_empty][0] = file_id
            del disk_state[ix_full]
        elif empty_size > file_size:
            # more empty space than file size
            disk_state.insert(ix_empty, [file_id, file_size])
            disk_state[ix_empty+1][1] -= file_size
            del disk_state[ix_full+1]
        else:
            # file size bigger than empty space
            disk_state[ix_empty][0] = file_id
            disk_state[ix_full][1] -= empty_size

        work_to_do = True
    return disk_state


def simplify_p2(disk_state):

    ix_full = len(disk_state)-1
    work_to_do = True
    if disk_state[-1][0] != -1:
        max_file_id = disk_state[-1][0]
    # print(f"Starting with max file id = {max_file_id}")
    for file_id in range(max_file_id, 0, -1):
        # print(f"Disk state = {disk_state}")
        ix_full = next(ix for ix in range(len(disk_state)-1, 0, -1)
                       if disk_state[ix][0] == file_id)
        # print(f"Max file id {file_id} at {ix_full}")
        file_size = disk_state[ix_full][1]
        ix_empty = 0
        while ix_empty < len(disk_state) and (disk_state[ix_empty][0] != -1 or (disk_state[ix_empty][0] == -1 and disk_state[ix_empty][1] < file_size)):
            ix_empty += 1
        # print(f"Candidate {ix_empty}")
        if ix_empty == len(disk_state) or disk_state[ix_empty][0] != -1 or ix_full < ix_empty:
            # print("No empty space found")
            continue

        empty_size = disk_state[ix_empty][1]
        # same size
        # print(f"Empty at {ix_empty}, file at {ix_full}")
        if empty_size == file_size:
            disk_state[ix_empty][0] = file_id
            disk_state[ix_full][0] = -1
        elif empty_size > file_size:
            # more empty space than file size
            disk_state.insert(ix_empty, [file_id, file_size])
            disk_state[ix_empty+1][1] -= file_size
            disk_state[ix_full+1][0] = -1
    print(f"Final disk state = {disk_state}")
    return disk_state


def part1(txt):
    print(f"Input is {txt}")
    res = create_index(txt)
    # print(res)
    simplified = simplify(res)
    # print(simplified)
    check_sum = compute_checksum(simplified)
    print(f"Part 1 checksum = {check_sum}")


def part2(txt):
    print(f"Input is {txt}")
    res = create_index(txt)
    # print(res)
    simplified = simplify_p2(res)
    # print(simplified)
    check_sum = compute_checksum(simplified)
    print(f"Part 2 checksum = {check_sum}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--test',
                        action='store_true')  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"test{day}.txt"
        raw_data = "2333133121414131402"
    else:
        filename = f"input{day}.txt"

        with open(f"../data/{filename}", "r") as f:
            raw_data = f.read()
    # print(raw_data)
    # part1(raw_data.strip())
    part2(raw_data.strip())


def tests():
    # res = create_index("12345")
    # simplified = simplify_p2(res)
    # print(simplified)
    # compute_checksum(simplified)
    res = create_index("2333133121414131402")
    simplified = simplify_p2(res)
    compute_checksum(simplified)
    # print(list(itertools.combinations([0, 1, 2], 2)))


if __name__ == "__main__":
    # tests()
    main()
