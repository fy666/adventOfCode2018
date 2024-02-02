import argparse
import copy
import math
import numpy as np
import time
import logging
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt


def vizualize(graph, nodes):
    G = nx.Graph()
    for n in nodes:
        G.add_node(n)

    for k, d in graph.items():
        for item in d:
            G.add_edge(k, item)
    nx.draw(G, with_labels=True)
    plt.show()


def cut_in_half(graph, nodes):
    G = nx.Graph()
    for n in nodes:
        G.add_node(n)
    for k, d in graph.items():
        for item in d:
            G.add_edge(k, item)
    x = nx.minimum_edge_cut(G)
    print(f"Edges to remove = {x}")
    G.remove_edges_from(x)
    a = nx.connected_components(G)
    sizes = [len(i) for i in a]
    print(f"Part 1 = {sizes[0]*sizes[1]}")


def valid_connexion(a, b, connexions_to_remove):
    for x, y in connexions_to_remove:
        if (x, y) == (a, b) or (x, y) == (b, a):
            logging.debug(f"Should skip {a},{b}")
            return False
    return True


def walktrough(graph, node, connexions_to_remove=[]):
    visited_nodes = set()
    nodes_to_visit = [node]
    while nodes_to_visit:
        n = nodes_to_visit.pop()
        visited_nodes.add(n)
        for d in graph.get(n, []):
            if d not in visited_nodes and valid_connexion(n, d, connexions_to_remove):
                nodes_to_visit.append(d)
    return len(visited_nodes)


def main():
    parser = argparse.ArgumentParser(description="Day25")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    logging.basicConfig(level=args.logLevel,
                        format='%(levelname)s: %(message)s')

    file = "./src/files/day25.txt"
    good_answer = 591890
    if args.ex:
        file = "./src/files/day25ex.txt"
        good_answer = 54

    graph = defaultdict(set)
    nodes = set()
    connexions = 0
    with open(file, "r") as f:
        for il, line in enumerate(f.readlines()):
            key, data = line.strip().split(": ")
            nodes.add(key)
            childs = data.split(" ")
            for c in childs:
                graph[key].add(c)
                nodes.add(c)
                graph[c].add(key)  # bidirectional
                connexions += 1

    print(f"{len(nodes)} nodes, {connexions} connexions")
    a = walktrough(graph, list(graph.keys())[0], [])
    print(f"First graph walkthrough = {a}")


    # Use networkx to vizualize graph, note the 3 connexions to cut
    # vizualize(graph, nodes)

    if args.ex:
        connexions_to_remove = [("hfx", "pzl"), ("bvb", "cmg"), ("nvd", "jqt")]
    else:
        connexions_to_remove = [("kkp", "vtv"), ("cmj", "qhd"), ("lnf", "jll")]

    sizes = set()
    for n in list(nodes):
        a = walktrough(graph, n, connexions_to_remove)
        sizes.add(a)
        if len(sizes) == 2:
            break
    s = list(sizes)
    print(s)
    ans = s[0]*s[1]
    msg = "correct" if ans == good_answer else "incorrect"
    print(f"Part 1 = {ans}: ({msg})")

    # Or using networking:
    cut_in_half(graph, nodes)


if __name__ == "__main__":
    main()
