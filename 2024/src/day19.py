import argparse
import copy
import re
import functools


@functools.cache
def find_word(word, index, towels):
    res = 0
    if index == len(word):
        return 1

    for to in towels:
        if word[index:index+len(to)] == to:
            res += find_word(word, index+len(to), towels)
    return res


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

    towels, words = raw_data.split("\n\n")
    towels = towels.split(", ")
    words = words.split("\n")

    sum_p1 = 0
    sum_p2 = 0
    for word in words:
        res = find_word(word, 0, tuple(towels))
        sum_p2 += res
        if res != 0:
            sum_p1 += 1
    print(f"Part 1 = {sum_p1}")
    print(f"Part 2 = {sum_p2}")


if __name__ == "__main__":
    main()
