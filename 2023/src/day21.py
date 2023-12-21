import argparse
import queue
import copy
import re
import math
import numpy as np


def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def outOfBounds(pos, map_shape):
    for i in range(2):
        if pos[i] < 0 or pos[i] >= map_shape[i]:
            return True
    return False

def infinitePos(pos, map_shape):
    return (pos[0]%map_shape[0], pos[1]%map_shape[1])

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
    corr = {".": 0 , "#": 1 , 'S':2}
    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            garden.append(np.array([corr[x] for x in line.strip()]))
    #print(garden)
    garden = np.array(garden)
    print(garden)
    tmp = np.where(garden == 2)
    start_pos = (tmp[0][0], tmp[1][0])
    print(start_pos)
    print(garden[start_pos])
    
    max_step = 64
    max_step = 500 #26501365

    item = {"curr": start_pos, "steps": 0, "prev": {}}
    visited_pos = {}
    items = queue.Queue()
    items.put(item)
    
    count_possibilities = set()
    while not items.empty():
        item = items.get()
        if item["steps"] == max_step:
            count_possibilities.add(item["curr"])
            continue
        item["steps"] += 1
        for dir in [(0,1),(1,0),(0,-1), (-1,0)]:
            new_item = copy.copy(item)
            new_pos = add(item["curr"], dir)
            # if outOfBounds(new_pos, garden.shape):
            #     continue
            if garden[infinitePos(new_pos, garden.shape)] == 1:
                continue
            if (new_pos in visited_pos and visited_pos[new_pos] < new_item["steps"]) or (new_pos not in visited_pos):
                new_item["curr"] = new_pos
                visited_pos[new_pos] = new_item["steps"]
                items.put(new_item)
    print(f"Part 1 {len(count_possibilities)}")

    

if __name__ == "__main__":
    main()
