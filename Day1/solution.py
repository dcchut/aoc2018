def process_input(filename):
    # load the input data
    with open(filename,'r') as fh:
        data = fh.readlines()

    # interpret each entry as an integer
    return [int(q) for q in data]


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
    input = process_input('input.txt')

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))