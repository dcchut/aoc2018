from utils import load_input


def treeverse(input):
    if len(input) == 0:
        return 0, 0

    # children
    children = input.pop(0)
    metadataentries = input.pop(0)

    v = {}
    s = 0
    r = 0

    # consume children recursively
    for k in range(0, children):
        tmp, v[k] = treeverse(input)
        s += tmp

    # now consume metadata entries
    for j in range(0, metadataentries):
        # get the metadata entry
        metadata = input.pop(0)

        s += metadata

        # For part 2, we add values slightly different depending on whether
        # this node has children or not
        if children == 0:
            r += metadata
        else:
            if metadata - 1 not in v:
                continue
            # increase the value by the value of the corresponding node
            r += v[metadata - 1]

    return s, r


def main():
    tree = load_input('input.txt')[0].split()
    tree = [int(q) for q in tree]

    part1, part2 = treeverse(tree)

    print('Part 1:', part1)
    print('Part 2:', part2)


if __name__ == '__main__':
    main()
