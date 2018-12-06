from utils import load_input


def part1(differences):
    # the result frequency is simply the sum of the differences
    return sum(differences)


def part2(differences):
    s = len(differences)

    # we don't want to be dealing with any silly situations
    assert (s > 1 or s == [0])

    # find the first frequency that occurs twice
    visited = set()
    curr = 0
    k = 0

    while curr not in visited:
        visited.add(curr)
        curr += differences[k % s]
        k += 1

    return curr


def main():
    # process the input into a list of integers
    differences = [int(q) for q in load_input('input.txt')]

    print('Part 1:', part1(differences))
    print('Part 2:', part2(differences))


if __name__ == '__main__':
    main()
