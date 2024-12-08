import re
import numpy as np
import copy
import argparse
import itertools
import re


def add(a, b):
    return a+b


def mul(a, b):
    return a*b


def my_concat(a, b):
    order = len(str(b))
    return (a*10**order)+b


def apply_operation(data, operators):
    res = data[0]
    for val, op in zip(data[1:], operators):
        res = op(res, val)
    return res


def equation_possible(result, data, operation_list=[add, mul]):
    for c in itertools.product(operation_list, repeat=len(data)-1):
        operation_res = apply_operation(data, c)
        if operation_res == result:
            return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day')      # option that takes a value

    parser.add_argument('-t', '--test',
                        action='store_true')  # on/off flag
    args = parser.parse_args()

    print(args.test, args.day)
    if args.test:
        filename = f"test{args.day}.txt"
    else:
        filename = f"input{args.day}.txt"

    with open(f"../data/{filename}", "r") as f:
        x = [line.strip() for line in f.readlines()]
    sum_p1 = 0
    sum_p2 = 0
    for line in x:
        res = list(map(int, re.findall(r'''([0-9]+)''', line)))
        if equation_possible(res[0], res[1:], operation_list=[add, mul]):
            sum_p1 += res[0]
        if equation_possible(res[0], res[1:], operation_list=[add, mul, my_concat]):
            sum_p2 += res[0]

    print(f"Part 1 = {sum_p1}")
    print(f"Part 2 = {sum_p2}")


def tests():
    res = my_concat(15, 6)
    print(res)
    res = my_concat(12, 345)
    print(res)
    res = apply_operation([81, 40, 27], [add, mul])
    print(res)

    res = apply_operation([81, 40, 27], [mul, add])
    print(res)

    res = apply_operation([11, 6, 16, 20], [add, mul, add])
    print(res)

    r = itertools.product('AB', repeat=4)
    print(list(r))

    r = equation_possible(190, [10, 19])
    print(r)


if __name__ == "__main__":
    # tests()
    main()
