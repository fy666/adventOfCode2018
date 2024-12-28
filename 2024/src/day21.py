import re
import numpy as np
import argparse
import copy
import functools

numpad = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2),
    "forbid": (3, 0)
}

moves = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, -1): "<",
    (0, 1): ">",
}

rev_moves = {d: k for k, d in moves.items()}

arrowpad = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "forbid": (0, 0)
}


def is_valid_seq(start_pos, sequence, keyboard):
    # we dont exit the keyboard during the moves
    pos = start_pos
    for move in sequence:
        mov = rev_moves[move]
        pos = pos[0]+mov[0], pos[1]+mov[1]
        if pos == keyboard["forbid"]:
            return False
    return True


def get_manhattan(a, b):
    return (b[0]-a[0]), (b[1]-a[1])


def find_path(a, b):
    if a in numpad and b in numpad:
        keyboard = numpad
    else:
        keyboard = arrowpad
    dx, dy = get_manhattan(keyboard[a], keyboard[b])
    moves_x, moves_y = [], []
    if dx != 0:
        dir_x = dx/abs(dx)
        moves_x = [moves[(dir_x, 0)] for _ in range(abs(dx))]
    if dy != 0:
        dir_y = dy/abs(dy)
        moves_y = [moves[(0, dir_y)] for _ in range(abs(dy))]

    results = set()
    res = moves_x + moves_y
    if is_valid_seq(keyboard[a], res, keyboard):
        results.add("".join(res)+'A')
    res = moves_y + moves_x
    if is_valid_seq(keyboard[a], res, keyboard):
        results.add("".join(res)+'A')
    return list(results)


def test():
    res = find_path("0", "9")
    print(f"From 0 to 9: {res}")
    res = find_path("3", "7")
    print(f"From 3 to 7: {res}")
    res = find_path("A", "<")
    print(f"From A to <: {res}")
    print("---")
    res = solve("029A", d=0, max_size=2)
    print(len(res))


@functools.cache
def solve(code, d=0, max_size=2):
    s = 'A'
    all_res = 0
    for c in code:
        res = find_path(s, c)
        if d == max_size:
            all_res += len(res[0])
        else:
            l = [solve(r, d=d+1, max_size=max_size) for r in res]
            all_res += min(l)
        s = c
    return all_res


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]

    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        codes = ["029A",
                 "980A",
                 "179A",
                 "456A",
                 "379A"]
    else:
        codes = ["480A",
                 "682A",
                 "140A",
                 "246A",
                 "938A"]

    part1 = 0
    part2 = 0
    for code in codes:
        num = int(code.replace("A", ""))
        seq = solve(code, d=0, max_size=2)
        part1 += num * seq
        seq2 = solve(code, d=0, max_size=25)
        part2 += num*seq2
    print(f"Part 1 = {part1}")
    print(f"Part 2 = {part2}")


if __name__ == "__main__":
    # test()
    # print("*********")
    main()
