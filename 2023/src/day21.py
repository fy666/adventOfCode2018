import argparse
import queue
import copy
import re
import math
import numpy as np
from collections import deque
import time
import logging


def add(a, b):
    return (a[0]+b[0], a[1]+b[1])


def outOfBounds(pos, map_shape):
    for i in range(2):
        if pos[i] < 0 or pos[i] >= map_shape[i]:
            return True
    return False


def infinitePos(pos, map_shape):
    return (pos[0] % map_shape[0], pos[1] % map_shape[1])


def solve(garden, start, nsteps, infiniteMap=False):
    t = time.time()
    item = (start, 0)
    visited_pos = {}
    items = deque()
    items.append(item)

    while len(items) > 0:
        curr, steps = items.popleft()
        steps += 1
        for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = add(curr, dir)
            if not infiniteMap and outOfBounds(new_pos, garden.shape):
                continue
            if garden[infinitePos(new_pos, garden.shape)] == 1:
                continue
            if steps > nsteps:
                continue
            if new_pos not in visited_pos:
                visited_pos[new_pos] = steps
                items.append((new_pos, steps))
    ans = len([x for x in visited_pos.values() if x % 2 == 0])
    logging.debug(
        f"Start pos at {start}, max steps = {nsteps} : {ans} possibilities ({time.time()-t} s)")
    return ans


def main():
    parser = argparse.ArgumentParser(description="Day21")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()

    logging.basicConfig(level=args.logLevel,
                        format='%(levelname)s: %(message)s')
                        
    file = "./src/files/day21.txt"
    if args.ex:
        file = "./src/files/day21ex.txt"

    garden = []
    corr = {".": 0, "#": 1, 'S': 2}
    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            garden.append(np.array([corr[x] for x in line.strip()]))

    garden = np.array(garden)
    tmp = np.where(garden == 2)
    start_pos = (tmp[0][0], tmp[1][0])

    print(
        f"Part 1 = {solve(garden,start=start_pos, nsteps= 6 if args.ex else 64)}")

    # Part 2: stolen from Reddit... =_='
    # https://github.com/marcodelmastro/AdventOfCode2023/blob/main/Day21.ipynb
    if args.ex:
        for s in [50, 100, 500 , 1000]:
            print(
        f"Part 2, {s} steps = {solve(garden,start=start_pos, nsteps=s, infiniteMap=True)}")
        return
    gridsize = garden.shape[0]  # gridsize
    halfgrid = gridsize//2  # halfgrid

    # fully filled grids
    plots_oddsteps = solve(garden, start=(
        halfgrid, halfgrid), nsteps=3*gridsize)  # center
    plots_evensteps = solve(garden, start=(
        halfgrid, halfgrid), nsteps=2*gridsize)  # cross around center
    # diamonds extremes
    plots_corner_top = solve(garden, start=(0, halfgrid), nsteps=gridsize-1)
    plots_corner_bot = solve(garden, start=(
        gridsize-1, halfgrid), nsteps=gridsize-1)
    plots_corner_lef = solve(garden, start=(halfgrid,  0), nsteps=gridsize-1)
    plots_corner_rig = solve(garden, start=(
        halfgrid, gridsize-1), nsteps=gridsize-1)
    # smaller lateral gridsstart_pos
    plots_side_lef_bot_small = solve(
        garden, start=(gridsize-1,  0), nsteps=halfgrid-1)
    plots_side_rig_bot_small = solve(garden, start=(0,  0), nsteps=halfgrid-1)
    plots_side_lef_top_small = solve(garden, start=(
        gridsize-1, gridsize-1), nsteps=halfgrid-1)
    plots_side_rig_top_small = solve(
        garden, start=(0, gridsize-1), nsteps=halfgrid-1)
    # larger lateral grids
    plots_side_lef_bot_big = solve(garden, start=(
        gridsize-1,  0), nsteps=gridsize+halfgrid-1)
    plots_side_rig_bot_big = solve(
        garden, start=(0,  0), nsteps=gridsize+halfgrid-1)
    plots_side_lef_top_big = solve(garden, start=(
        gridsize-1, gridsize-1), nsteps=gridsize+halfgrid-1)
    plots_side_rig_top_big = solve(garden, start=(
        0, gridsize-1), nsteps=gridsize+halfgrid-1)

    nsteps = 26501365

    romboid_width = (nsteps - 65) // 131

    nfull_odd = (romboid_width//2*2 - 1) ** 2
    nfull_even = (romboid_width//2*2) ** 2

    nodd = plots_oddsteps
    neven = plots_evensteps

    ncorners = plots_corner_top+plots_corner_bot+plots_corner_lef+plots_corner_rig
    nsides_small = plots_side_lef_bot_small+plots_side_rig_bot_small + \
        plots_side_lef_top_small+plots_side_rig_top_small
    nsides_large = plots_side_lef_bot_big + plots_side_lef_top_big + \
        plots_side_rig_bot_big+plots_side_rig_top_big

    total = nfull_odd*nodd + nfull_even*neven + romboid_width * \
        nsides_small + (romboid_width-1)*nsides_large + ncorners

    print(f"Part 2 = {total}")
    # Correct ans = 609012263058042


if __name__ == "__main__":
    main()
