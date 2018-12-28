from utils import load_input
from collections import defaultdict, Counter

def get_adjacent(land, x, y):
    return [land[q] for q in [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]]


def simulate(land, target_k):
    k = 0
    land_size = 50
    visited = {}

    while True:
        if k == target_k:
            break

        # we keep track of whether the lumber collection area has been in this state before
        q = tuple(list(land.values()))
        if q in visited:
            # delta_k is the number of iterations since we last hit this state
            delta_k = k - visited[q]

            # we can keep increasing k by this difference as long as we'd still be below the target
            while k + delta_k < target_k:
                k += delta_k
        else:
            visited[q] = k

        k += 1

        new_land = land.copy()

        # we compute the next state of the lumber operations
        for x in range(0,land_size):
            for y in range(0,land_size):
                c = Counter(get_adjacent(land,x,y))
                if land[(x,y)] == 0:
                    if 1 in c and c[1] >= 3:
                        new_land[(x,y)] = 1
                elif land[(x,y)] == 1:
                    if 2 in c and c[2] >= 3:
                        new_land[(x,y)] = 2
                elif land[(x,y)] == 2:
                    if 1 in c and 2 in c and c[1] >= 1 and c[2] >= 1:
                        pass
                    else:
                        new_land[(x,y)] = 0
        land = new_land

    c = Counter(list(land.values()))
    return c[1] * c[2]


def main():
    land = defaultdict(int)
    for (y, line) in enumerate(load_input('input.txt')):
        for (x, char) in enumerate(line):
            if char == '.':
                w = 0
            elif char == '|':
                w = 1
            elif char == '#':
                w = 2
            land[(x,y)] = w

    print('Part 1:', simulate(land,10))
    print('Part 2:', simulate(land,1000000000))


if __name__ == '__main__':
    main()