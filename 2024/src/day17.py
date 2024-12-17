import numpy as np
import argparse


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
            output += list(str(combo))

        op_ptr += 2

    print(registers, f"output = {output}, {','.join(output)}")


def run_copy(operations, registers):
    register_map = {4: "A", 5: "B", 6: "C"}
    # print(f"Running {operations} on register {registers}")
    op_ptr = 0
    output = []
    operation_str = list(map(str, operations))
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
            # if combo in [4, 5, 6]:
            # print(f"Out of reg {register_map[combo]}")
            combo = combo % 8
            output += list(str(combo))
            if len(output) > len(operation_str):
                # print(f"{output} too long")
                return False, output
            if output != operation_str[0 : len(output)]:
                # print(f"{output} different than { operation_str[0 : len(output)]}")
                return False, output

        op_ptr += 2

    # print(f"Output is {output}")
    if output == operation_str:
        return True, output
    return False, "".join(output)


def run_decoded(registers):
    output = []
    print(registers)
    while registers["A"] != 0:
        registers["B"] = registers["A"] % 8
        # print(registers)
        registers["B"] = registers["B"] ^ 5
        # print(registers)
        registers["C"] = int(registers["A"] / (2 ** registers["B"]))
        # print(registers)
        registers["B"] = registers["B"] ^ 6
        # print(registers)
        registers["A"] = int(registers["A"] / 8)
        # print(registers)
        registers["B"] = registers["B"] ^ registers["C"]
        to_print = list(str(registers["B"]))
        output += list(str(registers["B"]))
        print(f"Print = {registers} {to_print} {len(to_print)}")
    print(f"Final output = {len(output)} : {output}")


def run_once(A):
    x = (A % 8) ^ 5
    B = (x ^ 6) ^ int(A / 2**x)
    return B


def test():
    print("***** TESTS *****")
    run([2, 9], {"A": 0, "B": 0, "C": 9})
    run([5, 0, 5, 1, 5, 4], {"A": 10, "B": 0, "C": 0})
    run([0, 1, 5, 4, 3, 0], {"A": 2024, "B": 0, "C": 0})
    run([1, 7], {"A": 0, "B": 29, "C": 0})
    run([4, 0], {"A": 0, "B": 2024, "C": 43690})
    print("******************")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    if args.test:
        # 4: A, 5: B, 6: C
        registers = {"A": 729, "B": 0, "C": 0}
        operations = list(map(int, "0,1,5,4,3,0".split(",")))
        operations_p2 = list(map(int, "0,3,5,4,3,0".split(",")))
    else:
        registers = {"A": 51064159, "B": 0, "C": 0}
        operations = list(map(int, "2,4,1,5,7,5,1,6,0,3,4,6,5,5,3,0".split(",")))
        operations_p2 = operations

    # print(operations, registers)

    run(operations, registers)

    # found = run_copy(operations_p2, {"A": 9, "B": 0, "C": 0})
    print("************ P 2 ***********")
    run_decoded({"A": 8**5, "B": 0, "C": 0})
    # print(f"{found}")
    # found = False
    # for i in range(8**8, 8**9):
    #     found, res = run_copy(operations_p2, {"A": i, "B": 0, "C": 0})
    #     # print(f"{i} -> {res}")
    #     if found:
    #         print(f"A = {i}")
    #         break
    # print(f"{found}")

    a = 0
    for ix, i in enumerate(reversed(operations_p2)):
        print(f"Searching {i} between {a} and {a + 7}")
        tmp = [run_once(i) for i in range(a, a + 7)]
        print(tmp)
        a = (a + tmp.index(i)) * 8
        print(a)
    print(a)
    # print(a)
    # a = [run_once(i) for i in range(24, 28)]
    # print(a)
    # print(run_once(3 * 8 * 8 * 8 * 8))
    # run_decoded({"A": 3 * 8 * 8 * 8 * 8, "B": 0, "C": 0})


if __name__ == "__main__":
    test()
    main()
