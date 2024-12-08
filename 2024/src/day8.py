import re
import numpy as np
import copy
import argparse
import itertools
import re
import math


def is_in_map(pos,  size):
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= size[0] or pos[1] >= size[1]:
        return False
    return True


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--test',
                        action='store_true')  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"test{day}.txt"
    else:
        filename = f"input{day}.txt"

    with open(f"../data/{filename}", "r") as f:
        raw_data = f.read()

    antennas = set()
    for x in raw_data:
        if x != '\n' and x != '.' and x != '#':
            antennas.add(x)
    print(antennas)

    my_map = np.array([np.array(list(x)) for x in raw_data.split("\n")])

    # Part 1
    antinodes = set()
    for antenna in antennas:
        pos_x, pos_y = np.where(my_map == antenna)
        pos = [(int(x), int(y)) for x, y in zip(pos_x, pos_y)]
        for (p1, p2) in itertools.combinations(pos, 2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            for p, sign in zip([p1, p2], [-1, 1]):
                antinode = p[0] + sign*dx, p[1] + sign * dy
                if is_in_map(antinode, my_map.shape):
                    antinodes.add(antinode)
    print(f"Part 1: {len(antinodes)} antinodes found")

    # Part 2
    antinodes_part2 = set()
    for antenna in antennas:
        pos_x, pos_y = np.where(my_map == antenna)
        pos = [(int(x), int(y)) for x, y in zip(pos_x, pos_y)]
        for (p1, p2) in itertools.combinations(pos, 2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            pgcd = math.gcd(dx, dy)
            dx = dx/pgcd
            dy = dy/pgcd
            ix = 0
            dir_counter = np.array([True, True])
            while np.any(dir_counter):
                for idx, d in enumerate([-1, 1]):
                    antinode = p1[0] + d*ix*dx, p1[1] + d*ix*dy
                    if is_in_map(antinode, my_map.shape):
                        antinodes_part2.add(antinode)
                    else:
                        dir_counter[idx] = False
                ix += 1

    print(f"Part 2: {len(antinodes_part2)} antinodes found")


def tests():
    print(list(itertools.combinations([0, 1, 2], 2)))


if __name__ == "__main__":
    # tests()
    main()
