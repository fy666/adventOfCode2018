import json
import argparse
import functools


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return "continue"
        else:
            return a < b
    if isinstance(a, list) and isinstance(b, list):
        for aa, bb in zip(a, b):
            res = compare(aa, bb)
            if res != "continue":
                return res
        if len(a) == len(b):
            return "continue"
        else:
            return len(a) < len(b)

    elif isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    elif isinstance(a, int) and isinstance(b, list):
        return compare([a], b)
    print(f"{a} vs {b} not covered")


def compareLambda(a, b):
    res = compare(a, b)
    if res == True:
        return -1
    else:
        return 1


def main():
    print("Doing day 13 in python")
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action='store_true')
    args = parser.parse_args()
    pairs = []

    input = "./inputs/day13.txt"
    if args.test:
        input = "./inputs/day13_test.txt"
    with open(input) as f:
        tmp = []
        for l in f.readlines():
            l = l.strip()
            if len(l) == 0:
                pairs.append(tmp)
                tmp = []
            else:
                tmp.append(json.loads(l))
        pairs.append(tmp)
    print(f"Found {len(pairs)} pairs")

    part1Count = 0
    for ix, (a, b) in enumerate(pairs):
        res = compare(a, b)
        tmp = "in order" if res else "not in order"
        # print(f"{ix+1} {a} and {b}: {tmp}")
        if res == True:
            part1Count += (ix+1)
    print(f"Part 1 = {part1Count}")

    part2Items = []
    for(a, b) in pairs:
        part2Items.append(a)
        part2Items.append(b)
    part2Items.append([[2]])
    part2Items.append([[6]])
    print(f"Found {len(part2Items)} messages to sort for part 2")

    part2Items = sorted(part2Items, key=functools.cmp_to_key(compareLambda))

    part2Result = 1
    for ix, a in enumerate(part2Items):
        if a == [[2]] or a == [[6]]:
            part2Result = part2Result*(ix+1)
    print(f"Part 2 = {part2Result}")


if __name__ == "__main__":
    main()
