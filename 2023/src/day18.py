import numpy as np
import itertools
import argparse
import copy
import time
import cv2
import math
from matplotlib import pyplot as plt


def get_contour(file, part1):
    pos = [0, 0]
    contour = [pos]
    directions = ["R", "D", "L", "U"]
    peri = 0
    with open(file, "r") as f:
        for line in f.readlines():
            dir, steps, col = line.strip().split(" ")
            if part1:
                steps = int(steps)
            else:
                col = col.replace("(", "").replace(")", "").replace("#", "")
                steps = int(col[:-1], 16)
                dir = directions[int(col[-1])]
                # print(f"{line.strip()} -> {real_dir} {real_step}")
            if dir == "U":
                pos = [pos[0]-steps, pos[1]]
            elif dir == "D":
                pos = [pos[0]+steps, pos[1]]
                peri += steps
            elif dir == "R":
                pos = [pos[0], pos[1]+steps]
            elif dir == "L":
                pos = [pos[0], pos[1]-steps]
                peri += steps
            contour.append(pos)
    return contour, peri+1


def doudou_le_goat(contour):
    s = 0
    for p1, p2 in zip(contour, contour[1:]):
        s += (p1[1] + p2[1]) * (p1[0] - p2[0])
    s *= 0.5
    print(s)
    return abs(s)


def scale_contour(contour):
    d = 0
    sizes = [[], []]
    for a, b in zip(contour, contour[1:]):
        for i in range(2):
            d = abs(a[i]-b[i])
            if d != 0:
                sizes[i].append(d)
        # size_h.append(abs(a[0]-b[0]))
        # size_w.append(abs(a[1]-b[1]))
        # = max(d, abs(a[0]-b[0]) + abs(a[1]-b[1]))

    print(f"Max d = {sizes[0]}; {sizes[1]}")
    print(math.gcd(*sizes[0]))
    print(math.gcd(*sizes[1]))


def main():
    parser = argparse.ArgumentParser(description="Day18")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    file = "./src/files/day18.txt"
    if args.ex:
        file = "./src/files/day18ex.txt"

    # print(contour)
    contour, p = get_contour(file, False)  # Part 1
    s = doudou_le_goat(contour)
    print(f"Doudou le goat {s} = {s+p}")
    # scale_contour(contour)
    return
    w = max([x[0] for x in contour]) - min([x[0] for x in contour])+1
    h = max([x[1] for x in contour]) - min([x[1] for x in contour])+1
    offset_w = min(0, min([x[0] for x in contour]))
    offset_h = min(0, min([x[1] for x in contour]))
    converted_contour = [
        [x[0]+abs(offset_w), x[1]+abs(offset_h)] for x in contour]

    print(f"{w}, {h}, -> {offset_w} {offset_h}")
    # print(converted_contour)
    img = np.zeros((w, h, 3), dtype=np.uint8)  # * (255, 255, 255)
    # img = np.zeros((100,100,3), dtype=np.uint8)

    cv_contour = np.array([[x[1], x[0]]
                          for x in converted_contour]).astype(int)
    image = cv2.polylines(img, pts=[cv_contour],
                          isClosed=True, color=(255, 0, 0))
    # thickness=cv2.FILLED)
    image = cv2.fillPoly(img, pts=[cv_contour], color=(255, 255, 0))
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image[0][0] = (0, 255, 0)
    # print(image.shape)
    # print(image_gray)
    area = (image_gray != 0).sum()
    print(f"My area = {area}")
    plt.imshow(image)
    plt.draw()
    plt.show()
    area = cv2.contourArea(cv_contour)
    print(f"CV area = {area}")
    print(f"Part 1 = {42}")
    print(f"Part 2 = {42}")


if __name__ == "__main__":
    main()
