from utils import load_input, intersection, get_numbers#import utils
from Day16.operations import *


def check(before,after,operation,operations):
    # construct a list of all possible operations that this opcode could be
    possible = []
    for (k, op) in enumerate(operations):
        register = before.copy()
        af = op(register,*operation)
        if af == after:
            possible.append(k)
    return possible


def main():
    operations = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

    puzzle = load_input('input.txt')

    before = None
    instruction = None
    part1_count = 0
    possible_int = {}

    for (k,line) in enumerate(puzzle):
        if k % 4 == 0:
            before = get_numbers(line)
        if k % 4 == 1:
            instruction = get_numbers(line)
        if k % 4 == 2:
            after = get_numbers(line)
            opcode = instruction[0]

            # get the operations that this instruction could correspond to
            possible = check(before,after,instruction[1:], operations)

            # count the number of samples that behave like three or more opcodes
            if len(possible) >= 3:
                part1_count += 1

            # we keep intersecting the list of possible operations based on the result of each input
            if opcode not in possible_int:
                possible_int[opcode] = possible
            else:
                possible_int[opcode] = intersection(possible_int[opcode],possible)

    # for part 1, count how many sample in our input behave like three or more opcodes
    print('Part 1:', part1_count)

    secured = []
    # for part 2, we need to figure out which opcode corresponds to which operation
    # at each stage, there is always (at least) one opcode that we can deduce
    while len(secured) < 15:
        for key in possible_int:
            # if we've already figured this one out, skip it
            if key in secured:
                continue

            # if there's only 1 possibility for what this opcode could be, then we're done!
            if len(possible_int[key]) == 1:
                secured.append(key)
                new_possible_int = possible_int.copy()
                # remove this operation as a possibility for all other opcodes
                for k in possible_int:
                    if k == key:
                        continue
                    if possible_int[key][0] in new_possible_int[k]:
                        new_possible_int[k].remove(possible_int[key][0])
                possible_int = new_possible_int
                break

    # apply the operations to our puzzle input
    registers = [0,0,0,0]
    for line in load_input('input2.txt'):
        op, a, b, c = get_numbers(line)
        registers = operations[possible_int[op][0]](registers,a,b,c)

    print('Part 2:', registers[0])


if __name__ == '__main__':
    main()
