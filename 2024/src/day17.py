import numpy as np
import argparse
from collections import deque


def get_value(operations, op_ptr, register_map, registers):
    combo = operations[op_ptr + 1]
    if combo in [4, 5, 6]:
        combo = registers[register_map[combo]]
    return combo


def run(operations, registers):
    register_map = {4: "A", 5: "B", 6: "C"}
    op_ptr = 0
    output = []
    while op_ptr < len(operations):
        opcode = operations[op_ptr]

        if opcode in [0, 6, 7]:
            register_correspondence = {0: "A", 6: "B", 7: "C"}
            num = registers["A"]
            den = 2 ** (get_value(operations, op_ptr, register_map, registers))
            res = int(num / den)
            registers[register_correspondence[opcode]] = res
        elif opcode == 1:
            # bitwise XOR: ^
            combo = operations[op_ptr + 1]  # literal operand
            registers["B"] = registers["B"] ^ combo
        elif opcode == 2:
            combo = get_value(operations, op_ptr, register_map, registers) % 8
            registers["B"] = combo
        elif opcode == 3 and registers["A"] != 0:
            val = get_value(operations, op_ptr, register_map, registers)
            op_ptr = val
            continue
        elif opcode == 4:
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:
            combo = get_value(operations, op_ptr, register_map, registers) % 8
            output.append(combo)
        op_ptr += 2

    # print(registers, f"output = {output}, {','.join(output)}")
    return registers, output


def run_once(A):
    x = (A % 8) ^ 5
    B = (x ^ 6) ^ int(A / 2**x)
    return B % 8


def run_test(*args):
    registers, output = run(*args)
    print(f"{registers}, output = {output}")


def test():
    print("***** TESTS *****")
    run_test([2, 9], {"A": 0, "B": 0, "C": 9})
    run_test([5, 0, 5, 1, 5, 4], {"A": 10, "B": 0, "C": 0})
    run_test([0, 1, 5, 4, 3, 0], {"A": 2024, "B": 0, "C": 0})
    run_test([1, 7], {"A": 0, "B": 29, "C": 0})
    run_test([4, 0], {"A": 0, "B": 2024, "C": 43690})
    print("******************")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    if args.test:
        # 4: A, 5: B, 6: C
        registers = {"A": 729, "B": 0, "C": 0}
        operations = list(map(int, "0,1,5,4,3,0".split(",")))
    else:
        registers = {"A": 51064159, "B": 0, "C": 0}
        operations = list(map(int, "2,4,1,5,7,5,1,6,0,3,4,6,5,5,3,0".split(",")))
        operations_p2 = operations

    new_reg, output = run(operations, registers)
    ans = ",".join([str(i) for i in output])
    print(f"Part 1 : {ans}")

    if args.test:
        return

    possible_ans = []
    input_to_test = deque()
    input_to_test.append((len(operations_p2)-1, 0))
    while len(input_to_test) > 0:
        ix, a = input_to_test.pop()
        wanted_out = operations_p2[ix]
        tmp = [run_once(i) for i in range(a, a + 8)]
        # tmp = [run(operations, {"A": i, "B": 0, "C": 0})[1][0] for i in range(a, a + 8)]
        for it, t in enumerate(tmp):
            if t == wanted_out:
                if ix == 0:
                    part2 = a+it
                    _, ans = run(operations, {"A": part2, "B": 0, "C": 0})
                    if ans != operations_p2:
                        print("Error")
                    possible_ans.append(part2)
                input_to_test.append((ix-1, (a+it)*8))
    # print(possible_ans)
    print(f"Part 2 = {min(possible_ans)}")


if __name__ == "__main__":
    test()
    main()
