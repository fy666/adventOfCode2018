import re
import numpy as np
import argparse

DIRS = [np.array(x) for x in [[1, 0], [-1, 0], [0, 1], [0, -1]]]


def is_in_map(pos, size):
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= size[0] or pos[1] >= size[1]:
        return False
    return True


def find_paths(my_map, pos):
    end_paths = []
    if my_map[tuple(pos)] == 9:
        return [tuple(pos)]

    for d in DIRS:
        new_pos = pos + d
        if is_in_map(new_pos, my_map.shape) and (my_map[tuple(new_pos)] - my_map[tuple(pos)]) == 1:
            end_paths += find_paths(my_map, new_pos)
    return end_paths


def get_int(val):
    if val == ".":
        return 11
    else:
        return int(val)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"../data/test{day}.txt"
    else:
        filename = f"../data/input{day}.txt"

    with open(f"{filename}", "r") as f:
        raw_data = f.read()

    my_map = np.array([list(map(get_int, x)) for x in raw_data.split("\n")])
    print(f"Reading map of shape {my_map.shape}")
    if args.test:
        print(my_map)

    start_points = np.where(my_map == 0)

    score = 0
    rating = 0
    for pos in zip(start_points[0], start_points[1]):
        res = find_paths(my_map, np.array(pos))
        score += len(set(res))
        rating += len(res)

    print(f"Score =  {score}")
    print(f"Rating =  {rating}")


if __name__ == "__main__":
    main()
