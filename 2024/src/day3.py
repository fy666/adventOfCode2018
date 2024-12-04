import re
import numpy as np


def main():
    with open("../data/input3.txt", "r") as f:
        x = f.read()
    part1 = False
    if part1:
        res = re.findall(r'''mul\(([0-9]+),([0-9]+)\)''', x)
        sum = 0
        for r in res:
            sum += int(r[0])*int(r[1])
        print(f"Part 1 sum = {sum}")

    res = re.finditer(r'''mul\(([0-9]+),([0-9]+)\)''', x)
    do_index = np.array([x.span()[0] for x in re.finditer(r'''do\(\)''', x)])
    dont_index = np.array([x.span()[0]
                          for x in re.finditer(r'''don't\(\)''', x)])
    print(do_index)
    print(dont_index)
    sum = 0
    for r in res:
        dont_m = np.where(dont_index < r.span()[0])[0]
        print(dont_m)
        if len(dont_m):
            dont_m = dont_index[dont_m[-1]]
        else:
            dont_m = -1
        do_m = np.where(do_index < r.span()[0])[0]
        if len(do_m):
            do_m = do_index[do_m[-1]]
        else:
            do_m = 0
        print(f"Dont = {dont_m}, do = {do_m}")
        if do_m > dont_m:
            sum += int(r.group(1)) * int(r.group(2))
        print(r.span(), r.group(), r.group(1))

    print(f"Part 2 sum = {sum}")
    # for txt in x:
    #     print(x)
    #     res = re.findall("mul([0-9]*,[0-9]*)", txt)
    #     print(res)


if __name__ == "__main__":
    main()
