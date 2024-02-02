import numpy as np
import itertools
import argparse
import copy
import time


class Beam:
    def __init__(self, pos, dir, map_shape):
        self.pos = pos
        self.dir = dir
        self.map_shape = map_shape

    def __str__(self):
        return f"{self.pos}, {self.dir}"

    def get_state(self):
        return (self.pos[0], self.pos[1], self.dir[0], self.dir[1])

    def move(self):
        self.pos = (self.pos[0]+self.dir[0], self.pos[1]+self.dir[1])

    def is_finished(self):
        if self.pos[0] < 0 or self.pos[1] < 0 or self.pos[0] >= self.map_shape[0] or self.pos[1] >= self.map_shape[1]:
            return True
        return False

    def modif_dir(self, obstacle):
        if obstacle == '|':
            if abs(self.dir[1]) == 1:
                self.dir = [-1, 0]
                return Beam(self.pos, [1, 0], self.map_shape)
        elif obstacle == '-':
            if abs(self.dir[0]) == 1:
                self.dir = [0, -1]
                return Beam(self.pos, [0, 1], self.map_shape)
        elif obstacle == '/':
            self.dir = [-self.dir[1], -self.dir[0]]  # swap
        elif obstacle == '\\':
            self.dir = [self.dir[1], self.dir[0]]  # swap
        elif obstacle != '.':
            print(f"Should not append ! {obstacle}")


def move(beam):
    return (beam[0]+beam[2], beam[1]+beam[3], beam[2], beam[3])


def is_out_of_bounds(beam, map_shape):
    if beam[0] < 0 or beam[1] < 0 or beam[0] >= map_shape[0] or beam[1] >= map_shape[1]:
        return True
    return False


def get_new_from_obstacle(beam, obstacle):
    if obstacle == '|':
        if abs(beam[3]) == 1:
            return [(beam[0], beam[1], 1, 0), (beam[0], beam[1], -1, 0)]
    elif obstacle == '-':
        if abs(beam[2]) == 1:
            return [(beam[0], beam[1], 0, 1), (beam[0], beam[1], 0, -1)]
    elif obstacle == '/':
        return [(beam[0], beam[1], -beam[3], -beam[2])]
    elif obstacle == '\\':
        return [(beam[0], beam[1], beam[3], beam[2])]
    elif obstacle != '.':
        print(f"Should not append ! {obstacle}")

    return [(beam[0], beam[1], beam[2], beam[3])]


def print_map_state(map, pos):
    new_map = copy.copy(map)
    for p in pos:
        new_map[p] = '#'
    print(new_map)


def solve(map, init_beam):
    t = time.time()
    beams = [init_beam]
    beams_states = set()
    ix = 0
    while (beams):
        b = beams.pop()
        b.move()
        ix += 1

        if b.is_finished():
            continue

        state = b.get_state()
        if state in beams_states:
            continue
        beams_states.add(state)

        if (other_beam := b.modif_dir(map[b.pos])) != None:
            beams.append(other_beam)
        beams.append(b)

    pos = [(x[0], x[1]) for x in beams_states]
    pos = set(pos)
    dt = time.time()-t
    print(f"After {ix} iterations ({dt/1e9} s), found {len(pos)}")
    return len(pos)


def solve_fast(map, init_beam):
    t = time.time()
    beams = [init_beam]
    beams_states = set()
    ix = 0
    while (beams):
        b = beams.pop()
        b = move(b)
        ix += 1

        if is_out_of_bounds(b, map.shape):
            continue

        if b in beams_states:
            continue
        beams_states.add(b)

        for n in get_new_from_obstacle(b, map[b[0], b[1]]):
            beams.append(n)

    pos = [(x[0], x[1]) for x in beams_states]
    pos = set(pos)
    dt = time.time()-t
    print(f"After {ix} iterations ({dt/1e9} s), found {len(pos)}")
    return len(pos)


def main():
    parser = argparse.ArgumentParser(description="Day16")
    parser.add_argument("--ex", help="Run on example", action='store_true')
    parser.add_argument("--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level", default="WARNING")
    args = parser.parse_args()
    file = "./src/files/day16.txt"
    if args.ex:
        file = "./src/files/day16ex.txt"

    map = []
    with open(file, "r") as f:
        for line in f.readlines():
            nums = np.array([x for x in line.strip()])
            map.append(nums)
    map = np.array(map)
    print(map.shape)

    solutions = []
    t = time.time()
    if False:
        # On lines
        for ix in range(map.shape[1]):
            solutions.append(solve(map, Beam((ix, -1), [0, 1], map.shape)))
            solutions.append(
                solve(map, Beam((ix, map.shape[1]), [0, -1], map.shape)))

        # On columns
        for ix in range(map.shape[0]):
            solutions.append(solve(map, Beam((-1, ix), [1, 0], map.shape)))
            solutions.append(
                solve(map, Beam((map.shape[0], ix), [-1, 0], map.shape)))

    else:
        # On lines
        for ix in range(map.shape[1]):
            solutions.append(solve_fast(map, (ix, -1, 0, 1)))
            solutions.append(
                solve_fast(map, (ix, map.shape[1], 0, -1)))
        # On columns
        for ix in range(map.shape[0]):
            solutions.append(solve_fast(map, (-1, ix, 1, 0)))
            solutions.append(
                solve_fast(map, (map.shape[0], ix, -1, 0)))

    print(f"Time {(time.time()-t)} s)")
    print(f"Part 1 = {solutions[0]}")
    print(f"Part 2 = {max(solutions)}")


if __name__ == "__main__":
    main()
