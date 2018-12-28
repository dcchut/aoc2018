from utils import load_input, get_numbers
from elfcode import *

puzzle_input = load_input('input.txt')
og_instruction_pointer = get_numbers(puzzle_input[0])[0]
instruction_pointer = 0

instructions = []

for (k,line) in enumerate(puzzle_input[1:]):
    l = line.split(" ")
    instructions.append((eval(l[0]), *get_numbers(line)))

register = [0, 0, 0, 0, 0, 0]

while True:
    # write the value of the instruction pointer to the corresponding register
    register[og_instruction_pointer] = instruction_pointer

    # now do the code
    p, x, y, z = instructions[instruction_pointer]

    p(register,x,y,z)

    # now set the instruction pointer equal to the value of the corresponding register
    instruction_pointer = register[og_instruction_pointer]
    instruction_pointer += 1

    if instruction_pointer < 0 or instruction_pointer >= len(instructions):
        print('Out of range')
        break

print(register[0])
