import regex as re
import numpy as np
import itertools
from functools import cache

def too_long(line):
    input_line, regex_scheme = line.strip().split(" ")
    regex_str = "(\.)*"
    regex_str += ".+".join(["(#){" + i + "}" for i in regex_scheme.split(",")])
    regex_str += "(\.)*"
    r = re.compile(regex_str)
    num_to_replace = input_line.count("?")
    num_hash = sum([int(i) for i in regex_scheme.split(",")]) - input_line.count("#")
    poss_vec = ["#" for _ in range(num_hash)] + [
        "." for _ in range(num_to_replace - num_hash)
    ]
    count = 0
    possibilities = set(itertools.permutations(poss_vec))
    print(f"{len(possibilities)} possibilities")
    for ip, poss in enumerate(possibilities):
        tmp = input_line
        for s in poss:
            tmp = tmp.replace("?", s, 1)
        if re.match(r, tmp):
            count += 1
    print(f"{line.strip()} -> {count} possibilities")
    return count

@cache
def solve(input, wanted_splits):

    if len(wanted_splits) == 0:
        if(input.count("#") == 0):
            return 1
        return 0
    # stop if impossible
    if input.count('#') + input.count('?') < sum(wanted_splits):
        return 0

    if input[0]=='.':
        return solve(input[1:], wanted_splits)

    possibilities = 0
    if input[0]=='?':
        possibilities+= solve(input[1:], wanted_splits)
    
    if (len(input)==wanted_splits[0] or (len(input) > wanted_splits[0] and input[wanted_splits[0]]!='#') ) and input[:wanted_splits[0]].count(".")==0:
        possibilities+=solve(input[wanted_splits[0]+1:], wanted_splits[1:])

    return possibilities

def main():
    result = 0
    part2 = 0
    with open("./src/files/day12.txt", "r") as f:
        for il, line in enumerate(f.readlines()):
            #print(f"Line {il}")
            #result += too_long(line)
            input_line, regex_scheme = line.strip().split(" ")
            num_groups = [x for x in input_line.split(".") if x != ""]
            num_groups_wanted = [int(x) for x in regex_scheme.split(",")]
            possibilities = solve(input_line, tuple(num_groups_wanted))
            #print(f"{input_line} {num_groups_wanted} -> {possibilities} possibilities")
            result += possibilities
            p2_line = "?".join([input_line for _ in range(5)])
            p2_possibilities = solve(p2_line, tuple(num_groups_wanted*5))
            #print(f"  P2 -> {p2_possibilities} possibilities")
            part2 += p2_possibilities
    print(f"Part 1 res = {result}")
    print(f"Part 2 res = {part2}")


if __name__ == "__main__":
    main()
