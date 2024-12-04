import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.ndimage import rotate


def count_lines(data, to_find=np.array([ord(y) for y in "XMAS"])):
    counter = 0
    for xdata in data:
        for ix in range(len(xdata) - 3):
            if np.all(xdata[ix: ix + 4] == to_find):
                counter += 1
    return counter


def get_diagonal_lines(data):
    out = [np.diag(data, k=0)]
    ix = 1
    while len(np.diag(data, k=ix)) > 3:
        out.append(np.diag(data, k=ix))
        out.append(np.diag(data, k=-ix))
        ix += 1
    return out


if __name__ == "__main__":
    test = False

    file_n = "input"
    if test:
        file_n = "test"
    filename = f"../data/{file_n}4.txt"

    with open(filename, "r") as f:
        d = np.array([np.array([ord(y) for y in list(x.strip())])
                     for x in f.readlines()])

    xmas_counter = 0

    for dir in range(4):
        angle = dir * 90
        xx = rotate(d, angle=angle)
        xmas_counter += count_lines(xx)
        out = get_diagonal_lines(xx)
        xmas_counter += count_lines(out)

    print(f"Part1: Counted {xmas_counter} xmas")

    part2_count = 0

    for x in sliding_window_view(d, window_shape=(3, 3)):
        for y in x:
            if y[1][1] == ord("A"):
                extr = [y[0][0], y[0][2], y[2][2], y[2][0]]
                for word in ["MMSS", "SMMS", "SSMM", "MSSM"]:
                    word_num = [ord(c) for c in word]
                    if np.all(extr == word_num):
                        part2_count += 1

    print(f"Part2: Counted {part2_count} xmas")
