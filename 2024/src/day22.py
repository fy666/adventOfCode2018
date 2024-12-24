import re
import numpy as np
import argparse
import copy
from collections import defaultdict


def next_secret(secret):
    secret = mix(secret, secret*64)
    secret = prune(secret)
    secret = mix(secret, int(secret/32))
    secret = prune(secret)
    secret = mix(secret, secret*2048)
    secret = prune(secret)
    return secret


def mix(a, b):
    return a ^ b


def prune(a):
    return a % 16777216


def run_N(secret, N):
    for i in range(N):
        secret = next_secret(secret)
    return secret


def construct_seq_d(secret, N):
    seq = {}
    prices = generate_sequence(secret, N)
    d = np.diff(prices)
    # print("Prices: ", prices)
    # print("Seq: ", d)
    for i in range(len(d)-3):
        seq_local = d[i:i+4]
        gain = prices[i+4]
        seq_str = ",".join([str(i) for i in seq_local])
        # print(seq_local, seq_str)
        if not seq_str in seq:
            seq[seq_str] = gain
    return seq


def generate_sequence(secret, N):
    prices = [int(str(secret)[-1])]
    for i in range(N):
        secret = next_secret(secret)
        prices.append(int(str(secret)[-1]))
    return prices


def part2(numbers):
    all_res = defaultdict(lambda: 0)
    for n in numbers:
        res = construct_seq_d(n, 2000)
        for k, d in res.items():
            all_res[k] += d

    d_max = 0
    k_max = ""
    for k, d in all_res.items():
        if d > d_max:
            d_max = d
            k_max = k
    print(f"Sequence {k_max} is  {d_max}")


def test():
    res = prune(100000000)
    assert res == 16113920, f"Res = {res}"
    res = mix(42, 15)
    assert res == 37, f"Res = {res}"

    for x in [1, 10, 100, 2024]:
        res = run_N(x, 2000)
        print(f"secret {x} after N: {res}")

    d_res = construct_seq_d(123, 2000)
    print(d_res["-1,-1,0,2"])
    part2([1, 2, 3, 2024])
    print("***********")


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

    numbers = list(map(int, raw_data.split("\n")))
    print(f"Reading numbers {len(numbers)}")

    sum_p1 = 0
    for i in numbers:
        sum_p1 += run_N(i, 2000)
    print(f"Part 1 : {sum_p1}")
    part2(numbers)


if __name__ == "__main__":
    test()
    main()
