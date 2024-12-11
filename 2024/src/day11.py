import argparse

def blink(stones):
    res = []
    for stone in stones:
        if stone == 0:
            res.append(1)
        elif (N := len(stone_str := str(stone))) % 2 == 0:
            h = int(N / 2)
            res.append(int(stone_str[:h]))
            res.append(int(stone_str[h:]))
        else:
            res.append(stone * 2024)
    return res


# Working recursion (still slow)
def blink_many(stone, N, cache):
    num_s = 0

    if N == 0:
        return 1

    if (item := (stone, N)) in cache:
        num_s += cache[item]
    else:
        r = blink([stone])
        for rr in r:
            n = blink_many(rr, N - 1, cache)
            num_s += n
    cache[(stone, N)] = num_s

    return num_s


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    if args.test:
        data = "125 17"
        # data = "1000 4"
    else:
        data = "2 72 8949 0 981038 86311 246 7636740"
    stones = list(map(int, data.split(" ")))

    res2 = 0
    res = 0
    cache = {}
    for stone in stones:
        res += blink_many(stone, 25, cache)
        res2 += blink_many(stone, 75, cache)
    print(f"After 25 iterations, {res} stones")
    print(f"After 75 iterations, {res2} stones")


if __name__ == "__main__":
    main()
