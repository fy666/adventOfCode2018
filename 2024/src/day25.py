import re
import numpy as np
import argparse


def my_parser(line):
    return np.array([1 if i == '#' else 0 for i in line])


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

    keys = []
    locks = []
    for m in raw_data.split("\n\n"):
        mymap = np.array([my_parser(x) for x in m.split('\n')])
        if np.all(mymap[0] == 1):
            keys.append(mymap)
        else:
            locks.append(mymap)

    print(f"Found {len(keys)} keys and {len(locks)} locks")
    match_found = 0
    for m1 in keys:
        for m2 in locks:
            s = m1+m2
            if not np.any(s == 2):
                match_found += 1
    print(f"Part 1 = {match_found}")


if __name__ == "__main__":
    main()
