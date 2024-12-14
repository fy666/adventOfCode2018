import re
import numpy as np
import argparse
from collections import defaultdict
from matplotlib import pyplot as plt
import matplotlib
from scipy.ndimage import label
import copy


class Robot():
    def __init__(self, r):
        self.pos = np.array([int(r.group(1)), int(r.group(2))])
        self.speed = np.array([int(r.group(3)), int(r.group(4))])

    def __str__(self):
        return f"Robot at {list(self.pos)} with speed {list(self.speed)}"

    def run(self, N, shape):
        self.pos = self.pos + N*self.speed
        for i in range(2):
            self.pos[i] = self.pos[i] % shape[i]

    def get_quadrant(self, shape):
        quad = 1
        for i in range(2):
            mid = int(shape[i]/2)
            if self.pos[i] < mid:
                quad += 0
            elif self.pos[i] > shape[i]/2:
                quad += (i+1)
            if self.pos[i] == mid:
                return 0
        return quad


def parse_data(input):
    result = []
    res = re.search(r'''p=(\d+),(-?\d+) v=(-?\d+),(-?\d+)''', input)
    return Robot(res)


def show_map(robots, N, shape):
    mat = np.zeros((shape))
    for r in robots:
        mat[*r.pos] = 255  # (0, 255, 0)

    labeled_array, no_feats = label(mat)
    if no_feats > 200:
        return False

    print(N)
    cmap = matplotlib.colors.ListedColormap(['black', 'green'])
    plt.imshow(mat, cmap=cmap)
    plt.title(f"{N} seconds")
    plt.show()
    return True


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"../data/test{day}.txt"
        tile_shape = (11, 7)  # wide, tall
    else:
        filename = f"../data/input{day}.txt"
        tile_shape = (101, 103)

    with open(f"{filename}", "r") as f:
        raw_data = f.read()

    robots = []
    for r in raw_data.split("\n"):
        # print(f"{r}")
        robot = parse_data(r)
        robots.append(robot)
    print(f"{len(robots)} robots found")
    robots_p2 = copy.deepcopy(robots)

    if True:
        quad_counter = defaultdict(lambda: 0)
        N = 100
        for r in robots:
            r.run(N, tile_shape)
            q = r.get_quadrant(tile_shape)
            quad_counter[q] += 1
        part1 = 1
        for k, d in quad_counter.items():
            if k != 0:
                part1 *= d
        print(f"Part 1 = {part1}")

    for i in range(10000):
        for r in robots_p2:
            r.run(1, tile_shape)
        if show_map(robots_p2, i+1, tile_shape):
            break


if __name__ == "__main__":
    main()
