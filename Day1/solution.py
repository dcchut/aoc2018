from utils import load_input


def part1(input):
    # the result frequency is simply the sum of the differences
    return sum(input)


def part2(input):
    s = len(input)

    # we don't want to be dealing with any silly situations
    assert(s > 1 or s == [0])

    # find the first frequency that occurs twice
    visited = set()
    curr = 0
    k = 0

    while curr not in visited:
        visited.add(curr)
        curr += input[k % s]
        k += 1

    return curr


if __name__ == '__main__':
    # process the input into a list of integers
    input = [int(q) for q in load_input('input.txt')]

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))