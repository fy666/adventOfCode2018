import argparse
import queue
import copy
import re
import math
# False -> low / off
# True -> high / on

# Need to rewritte conjonction !!! check state from ALL outputs !!


def push_once(routing, first_cmd, part2=None):

    modules_to_process = queue.Queue()
    modules_to_process.put(first_cmd)
    pulse_counter = [0, 0]
    while not modules_to_process.empty():
        item, signal, prev = modules_to_process.get()
        if part2 is not None and (item, signal, prev) == part2:
            return True
        #print(f"{prev} -> {signal} -> {item}")
        if signal:
            pulse_counter[0] += 1
        else:
            pulse_counter[1] += 1
        if item not in routing:
            continue
        if routing[item]["type"] == "broadcaster":
            for i in routing[item]["childs"]:
                modules_to_process.put((i, signal, item))
        elif routing[item]["type"] == "flip":
            if signal:
                continue
            prev_state = routing[item]["state"]
            for i in routing[item]["childs"]:
                modules_to_process.put((i, not prev_state, item))
            routing[item]["state"] = not prev_state
        elif routing[item]["type"] == "conj":
            routing[item]["inputs"][prev] = signal
            new_sig = not all(routing[item]["inputs"].values())
            for i in routing[item]["childs"]:
                modules_to_process.put((i, new_sig, item))
    if part2:
        return False
    return pulse_counter


def run_until(routing, stop_condition):
    local_routing = copy.deepcopy(routing)
    index = 0
    p = False
    while(not p):
        p = push_once(local_routing, ("broadcaster", False, "button"), part2=stop_condition)
        index+=1
    return index

def main():
    parser = argparse.ArgumentParser(description="Day20")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    file = "./src/files/day20.txt"
    if args.ex:
        file = "./src/files/day20ex.txt"

    routing = {}

    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            name, childs = line.strip().split(" -> ")
            clean_name = name.replace("&", "").replace("%", "")
            if '%' in name:
                m_type = "flip"
            elif '&' in name:
                m_type = "conj"
            else:
                m_type = "broadcaster"
                print("broadcaster")

            routing[clean_name] = {"childs": childs.split(
                ", "), "state": False, "type": m_type, "inputs": {}}

    for key, data in routing.items():
        for c in data["childs"]:
            if c not in routing:
                continue
            if routing[c]["type"] == "conj":
                routing[c]["inputs"][key] = False
    
    routing_part2 = copy.deepcopy(routing)
    res = [0, 0]
    count = 0
    N = 1000
    for _ in range(N):
        count += 1
        #print(f"-----{count}----")
        p = push_once(routing, ("broadcaster", False, "button"))
        res[0] += p[0]
        res[1] += p[1]
        # for k, d in routing.items():
        #     print(f"{k} state {d['state']}")
        # print(routing)
    print(f"{res} pulses")
    print(res[0]*res[1])

    print(routing_part2["lx"]["inputs"])
    sub = []
    for c in routing_part2["lx"]["inputs"]:
        s = run_until(routing_part2, ("lx", True, c ))
        print(s)
        sub.append(s)
    part2_res = math.lcm(*sub)
    print(f"Part 2 {part2_res} pushes")
    


if __name__ == "__main__":
    main()
