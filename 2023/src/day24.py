import argparse
import copy
import math
import numpy as np
import time
import logging
import sympy


def intersect2D(p1, p2, r_lim):
    x1, v1 = p1
    x2, v2 = p2
    a = np.array([[v1[0], -v2[0]], [v1[1], -v2[1]]])
    b = np.array([x2[0]-x1[0], x2[1]-x1[1]])
    try:
        t = np.linalg.solve(a, b)
    except:
        logging.debug(f"{p1} and {p2}: dont intersect")
        return False

    intersect = t[0] * v1 + x1
    if t[0] < 0 or t[1] < 0:
        logging.debug(f"{p1} and {p2}: intersect in the past")
        return False

    if intersect[0] >= r_lim[0] and intersect[0] <= r_lim[1] and intersect[1] >= r_lim[0] and intersect[1] <= r_lim[1]:
        logging.debug(f"{p1} and {p2}: intersect inside area ({intersect})")
        return True

    logging.debug(f"{p1} and {p2}: intersect outside area ({intersect})")
    return False


def main():
    parser = argparse.ArgumentParser(description="Day24")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    logging.basicConfig(level=args.logLevel,
                        format='%(levelname)s: %(message)s')

    file = "./src/files/day24.txt"
    search_area = [200000000000000, 400000000000000]
    if args.ex:
        file = "./src/files/day24ex.txt"
        search_area = [7, 27]

    stones = []
    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            a, b = line.strip().split(" @ ")
            pos = np.array([int(x) for x in a.split(", ")])
            speed = np.array([int(x) for x in b.split(", ")])
            stones.append((pos, speed))

    part1 = 0
    for il, p1 in enumerate(stones):
        for p2 in stones[il+1:]:
            if intersect2D(p1, p2, search_area):
                part1 += 1
    print(f"Part 1 = {part1}")

    x, y, z, vx, vy, vz, t1, t2, t3 = sympy.symbols('x y z vx vy vz t1 t2 t3')
    equations = []
    for (pi, vi), t in zip(stones[:3], [t1, t2, t3]):
        for i, p, v in zip([0, 1, 2], [x, y, z], [vx, vy, vz]):
            equations.append(p-pi[i]-t*vi[i] - t*v)

    ans = sympy.solve(equations)[0]
    logging.debug(ans)
    part2 = ans[x]+ans[y]+ans[z]
    print(f"Part 2 = {part2}")


if __name__ == "__main__":
    main()
