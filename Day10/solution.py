from utils import load_input, get_numbers


def print_blocks(blocks, xmin, xmax, ymin, ymax):
    for x in range(ymin, ymax + 1):
        for y in range(xmin, xmax + 1):
            if (y, x) in blocks:
                print('#', end='')
            else:
                print('.', end='')
        print(' ', end='\n')


def main():
    # get the list of step orderings
    points = load_input('input.txt')
    positions = {}
    position_set = set()
    velocities = {}

    # extract the four digits out of each input line
    for (k, line) in enumerate(points):
        x, y, xv, yv = get_numbers(line)

        positions[k] = (x, y)
        position_set.add((x, y))
        velocities[k] = (xv, yv)

    m = 0
    while True:
        ymin = min(t[1] for t in position_set)
        ymax = max(t[1] for t in position_set)

        ht = abs(ymax - ymin)
        # the lights align perfectly when the height is 9
        # its unclear if this always achieves the correct result
        if ht == 9:
            xmin = min(t[0] for t in position_set)
            xmax = max(t[0] for t in position_set)
            print_blocks(position_set, xmin, xmax, ymin, ymax)
            break

        # move the lights by their velocities
        # updating the set of positions
        position_set = set()

        for idx in positions:
            positions[idx] = (positions[idx][0] + velocities[idx][0], positions[idx][1] + velocities[idx][1])
            position_set.add(positions[idx])

        m += 1
    return m


if __name__ == '__main__':
    m = main()
    print('Part 2:', m)
