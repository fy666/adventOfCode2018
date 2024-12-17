import re
import numpy as np
import argparse
import copy
import heapq
import datetime

DIRS = [np.array(x) for x in [[1, 0], [0, -1], [-1, 0], [0, 1]]]


def find_path(start_pos, my_map):
    past_pos = [(start_pos[0], start_pos[1])]
    points = [(0, start_pos[0], start_pos[1], 3, past_pos)]
    heapq.heapify(points)
    best_scores = {}
    best_score = None
    visited_path = []
    c = 0
    while len(points) > 0:
        score, pos_x, pos_y, pdir, visited_pos = heapq.heappop(points)
        if False:
            print(f"Poping {score} {pos_x}, {pos_y}, dir {pdir} {my_map[pos_x, pos_y]}, {visited_pos}")
            c += 1
            if c == 150:
                break

        # Check if at right position
        if my_map[pos_x, pos_y] == 'E':
            if best_score is None or best_score >= score:
                best_score = score
                visited_path += visited_pos

        for i in [0, -1, 1]:
            new_dir = (pdir+i) % 4
            new_pos = np.array([pos_x, pos_y]) + DIRS[new_dir]
            new_item = (int(new_pos[0]), int(new_pos[1]), new_dir)
            new_score = score+1 + abs(i) * 1000
            # if new_item in visited_pos:
            # print("Already visited")
            # continue
            if best_scores.get(new_item, None) and best_scores[new_item] < new_score:
                continue
            if my_map[*new_pos] != '#':
                best_scores[new_item] = new_score
                n_visited_pos = copy.copy(visited_pos)
                # n_visited_pos.add(new_item)
                n_visited_pos.append((int(new_pos[0]), int(new_pos[1])))
                heapq.heappush(
                    points, (score+1 + abs(i) * 1000, *new_item, n_visited_pos))

        # # Either turn - 90°
        # heapq.heappush(points, (score+1000, pos_x, pos_y, (pdir-1) % 4))
        # # Either move forward (if possible)
        # new_pos = np.array([pos_x, pos_y]) + DIRS[pdir]
        # # print(DIRS[pdir], new_pos)
        # if my_map[*new_pos] != '#':
        #     heapq.heappush(points, (score+1, new_pos[0], new_pos[1], pdir))
        # # Either move forward (if possible)

    return best_score, len(set(visited_path))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    parser.add_argument("-t2", "--test2", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"../data/test{day}.txt"
    elif args.test2:
        filename = f"../data/test{day}v2.txt"
    else:
        filename = f"../data/input{day}.txt"

    with open(f"{filename}", "r") as f:
        raw_data = f.read()

    my_map = np.array([list(x) for x in raw_data.split("\n")])
    print(f"Reading map of shape {my_map.shape}")

    start_pos = np.where(my_map == 'S')
    print(f"Start pos is {start_pos}")
    print(f"Started at {datetime.datetime.now()}")
    res = find_path((int(start_pos[0][0]), int(start_pos[1][0])), my_map)
    print(f"Part 1 = {res}")
    print(f"Finished at {datetime.datetime.now()}")


if __name__ == "__main__":
    main()
