import re
import numpy as np
import argparse
import copy
from collections import defaultdict
import itertools


def find_biggest(nodes):
    graphs = set()
    for node, connexions in nodes.items():
        graph = set()
        graph.add(node)
        graph = None
        for i in range(len(connexions), 1, -1):
            if graph is not None:
                break
            for sub_conn in itertools.combinations(connexions, i):
                connected = np.all([n1 in nodes[n2] for n1, n2 in itertools.combinations(sub_conn, 2)])
                if connected:
                    graph = [node] + list(sub_conn)
                    break
        if graph is not None:
            graphs.add(tuple(sorted(graph)))

    biggest = 0
    password = ""
    for nodes in graphs:
        if len(nodes) > biggest:
            biggest = len(nodes)
            password = ",".join(nodes)
    print("Part 2 = ", biggest, password)


def find_trios(nodes):
    trios = set()
    for node, connexions in nodes.items():
        if not node.startswith("t"):
            continue
        if len(connexions) >= 2:
            # find all connexions
            for n1, n2 in itertools.combinations(connexions, 2):
                if n2 in nodes[n1]:
                    # found pair
                    node_list = sorted([node, n1, n2])
                    node_str = ",".join(node_list)
                    trios.add(node_str)
    print(f"Part 1 = {len(trios)}")


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

    # Construct dict
    nodes = defaultdict(list)
    for r in raw_data.split("\n"):
        a, b = r.split("-")
        nodes[a].append(b)
        nodes[b].append(a)
    if args.test:
        print(nodes)
    print(f"Found {len(nodes)} nodes")
    find_trios(nodes)

    find_biggest(nodes)


if __name__ == "__main__":
    main()
