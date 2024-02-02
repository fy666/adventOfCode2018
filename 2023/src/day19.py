import argparse
import queue
import copy
import re


def parse_command(line):
    r = re.compile("(\\w+)\\{(.+)+,(\\w+)\\}")
    r_cond = re.compile("([xmas]+)([\\>\\<])+(\\d+):(\\w+)")
    m = re.search(r, line)
    if m:
        rule_name = m.group(1)
        rule_else = m.group(3)
        conditions = []
        for x in m.group(2).split(","):
            n = re.search(r_cond, x)
            conditions.append(
                (n.group(1), n.group(2), int(n.group(3)), n.group(4)))

        conditions.append(("a", ">", 0, rule_else))

    return rule_name, conditions


def parse_input(line):
    r = re.compile("\\{x=(\\-?\\d+),m=(\\-?\\d+),a=(\\-?\\d+),s=(\\-?\\d+)\\}")
    m = re.search(r, line)
    if m:
        res = {}
        for il, l in enumerate("xmas"):
            res[l] = int(m.group(il + 1))
        return res


def apply_rule(input, rule):
    for key_var, op, val, res in rule:
        if op == '<' and input[key_var] < val:
            return res
        if op == '>' and input[key_var] > val:
            return res


def apply_rule_inter(input, rule):
    next_intervals = []
    for key_var, op, val, res in rule:
        new_input = copy.deepcopy(input)
        if val != 0:
            if op == '<':
                if input[key_var][1] > val:
                    new_input[key_var][1] = val - 1
                    input[key_var][0] = val
                else:
                    print("Error doing intervals <")
            else:
                if input[key_var][0] < val:
                    new_input[key_var][0] = val + 1
                    input[key_var][1] = val
                else:
                    print(
                        f"Error doing intervals > {input} {key_var}{op}{val}")
        next_intervals.append((new_input, res))

    return next_intervals


def check_input(input, rules):
    next_rule_name = "in"
    while (next_rule_name != 'A' and next_rule_name != 'R'):
        next_rule_name = apply_rule(input, rules[next_rule_name])
    return next_rule_name == 'A'


def main():
    parser = argparse.ArgumentParser(description="Day19")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    file = "./src/files/day19.txt"
    if args.ex:
        file = "./src/files/day19ex.txt"
    do_parse_command = True
    commands = {}
    inputs = []

    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            if line == '\n':
                do_parse_command = False
                continue
            if do_parse_command:
                key, d = parse_command(line.strip())
                commands[key] = d
            else:
                inputs.append(parse_input(line.strip()))

    res = 0
    for input in inputs:
        if (check_input(input, commands)):
            for l in "xmas":
                res += input[l]
    print(f"Part 1 = {res}")

    res2 = 0
    N = 4000
    inter = {"x": [1, N], "m": [1, N], "a": [1, N], "s": [1, N]}

    intervals = queue.Queue()
    intervals.put((inter, "in"))
    winning_intervals = []

    while not intervals.empty():
        item = intervals.get()
        # print(f"Processing \"{item[1]}\" with it {item[0]}")
        res = apply_rule_inter(item[0], commands[item[1]])
        for r in res:
            # print(f"Got  {r[0]} -> {r[1]}")
            if r[1] == 'A':
                winning_intervals.append(r[0])
            elif r[1] != 'R':
                intervals.put(r)

    res2 = 0
    for w in winning_intervals:
        tmp = 1
        for k in "xmas":
            tmp *= (w[k][1] - w[k][0] + 1)
        res2 += tmp

    print(f"Part 2 = {res2}")

    if args.ex:
        wanted_res = 167409079868000
        if res2 < wanted_res:
            print(f"wanted_res is higher")
        elif res2 > wanted_res:
            print(f"wanted_res is smaller")
        else:
            print("Found correct res ! :)")


if __name__ == "__main__":
    main()
