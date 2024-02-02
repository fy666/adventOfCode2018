import argparse
import queue
import copy
import re
import math
from collections import deque


def line_intersect(a, b):
    if a[0] >= b[0] and a[1] <= b[1]:
        return True
    if b[0] >= a[0] and b[1] <= a[1]:
        return True
    if a[0] <= b[1] and a[1] >= b[1]:
        return True
    if b[0] <= a[1] and b[1] >= a[1]:
        return True
    # if a[0] <= b[0] and a[1] >= b[0]:
    #     return True
    return False


class Cube:
    def __init__(self, line, name):
        a, b = line.strip().split("~")
        self.name = name
        self.x1, self.y1, self.z1 = list(map(int, a.split(",")))
        self.x2, self.y2, self.z2 = list(map(int, b.split(",")))
        if self.x1 > self.x2 or self.y1 > self.y2 or self.z1 > self.z2:
            print("Should sort")
        self.supports = []
        self.is_supported_by = []

    def intersect(self, other):
        return line_intersect((self.x1, self.x2), (other.x1, other.x2)) and line_intersect((self.y1, self.y2), (other.y1, other.y2))
        # return self.x1 < other.x2 and self.x2 > other.x1 and self.y1 < other.y2 and self.y2 > other.y1

    def add_to_ground(self, ground_map):
        z_min = 1
        for obj in ground_map:
            if self.intersect(obj):
                z_min = max(z_min, max(obj.z1, obj.z2)+1)
                # print(f"{self.name} intersect {obj.name}, z min is {z_min}")

        offset = min(self.z1, self.z2)
        self.z1 = self.z1 - offset + z_min
        self.z2 = self.z2 - offset + z_min

    def count_supports(self, ground_map):
        for obj in ground_map:
            if obj == self:
                continue
            # if z in contact:
            if self.z2 == (obj.z1-1):
                if self.intersect(obj):
                    self.supports.append(obj.name)
                    obj.is_supported_by.append(self.name)

    def __str__(self):
        return f"{self.x1}-{self.x2},{self.y1}-{self.y2},{self.z1}-{self.z2}"


def compute_chain_reaction(map, start):

    items_to_remove = deque()
    items_to_remove.append(start)
    count_removed_items = 0
    while len(items_to_remove) > 0:
        item_to_remove = items_to_remove.popleft()
        count_removed_items+=1
        for i in map[item_to_remove]["supports"]:
            map[i]["is supported"].remove(item_to_remove)
            if len(map[i]["is supported"]) == 0:
                items_to_remove.append(i)
    return count_removed_items-1
    
    

def main():
    parser = argparse.ArgumentParser(description="Day22")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    file = "./src/files/day22.txt"
    if args.ex:
        file = "./src/files/day22ex.txt"

    cubes = []
    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            new_cube = Cube(line, f"{il}")

            cubes.append(new_cube)
    
    cubes.sort(key=lambda x: min(x.z1, x.z2))
    for ix, c in enumerate(cubes):
        c.add_to_ground(cubes[:ix])
    cubes.sort(key=lambda x: [x.z1, x.z2]) 
    only_support = set()
    for c in cubes:
        c.count_supports(cubes)


    reactions_dict = {}
    for c in cubes:
        reactions_dict[c.name] = {"supports":c.supports, "is supported": c.is_supported_by}
        if len(c.is_supported_by) == 1:
            only_support.add(c.is_supported_by[0])

    could_be_removed = len(cubes) - len(only_support)
    print(f"Part 1: {could_be_removed} cubes could be dissintegrated")

    acc = 0
    for i in range(len(cubes)):
        var = copy.deepcopy(reactions_dict)
        ans = compute_chain_reaction(var, f"{i}")
        acc += ans
        #print(f"Removing {i} makes {ans} other bricks fall")
    print(f"Part 2: {acc}")



if __name__ == "__main__":
    main()
