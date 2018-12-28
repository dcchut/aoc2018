from utils import load_input, get_numbers
from collections import defaultdict, Counter


def down(p):
    return p[0], p[1]+1


def up(p):
    return p[0], p[1]-1


def left(p):
    return p[0]-1, p[1]


def right(p):
    return p[0]+1, p[1]


def main():
    puzzle_input = load_input('input.txt')
    spring = defaultdict(str)
    spring[(500,0)] = '|'

    for line in puzzle_input:
        char = line[0]
        pos, a, b = get_numbers(line)
        if char == 'x':
            for y in range(a,b+1):
                spring[(pos,y)] = '#'
        else:
            for x in range(a,b+1):
                spring[(x,pos)] = '#'
    spring[(500,1)] = '|'

    ymaxx = max(q[1] for q in spring)

    # now how do we want to do this
    current_sources = set([(500,1)])

    while len(current_sources) > 0:
        source = current_sources.pop()

        # if we're past the maximum y, just stop
        if source[1] > ymaxx+10:
            continue

        # if there is no spot underneath, just move down
        d = down(source)
        if spring[d] == '':
            spring[d] = '|'
            current_sources.add(d)
            continue

        # if there is a '|' underneath, probably just ignore this?
        if spring[d] == '|':
            continue

        # there is a spot underneath - try to flow as far left & right as possible
        left_wall = None
        right_wall = None

        x, y = source
        current_x = x+1
        while True:
            current_x -= 1
            pos = (current_x,y)

            # if there's a source block above this point
            # then don't do anything further in this direction
            if pos != source and up(pos) in current_sources:
                left_wall = current_x+1
                break

            if pos != source and (pos in current_sources):
                break

            if pos != source and (spring[down(pos)] == '|' or down(pos) in current_sources):
                break

            spring[pos] = '|'

            # if there is a spot below, then we can flow there
            if spring[down(pos)] == '':
                spring[down(pos)] = '|'
                current_sources.add(down(pos))
                break

            # if theres a wall to our left, then we can't flow any further
            if spring[left(pos)] == '#':
                left_wall = current_x
                break

        current_x = x-1
        while True:
            current_x += 1
            pos = (current_x, y)

            # if there's a source block above this point
            # then don't do anything further in this direction
            if pos != source and up(pos) in current_sources:
                right_wall = current_x - 1
                break

            if pos != source and pos in current_sources:
                break

            if pos != source and (spring[down(pos)] == '|' or down(pos) in current_sources):
                break

            spring[pos] = '|'

            if spring[down(pos)] == '':
                spring[down(pos)] = '|'
                current_sources.add(down(pos))
                break


            # if theres a wall to oru right, then we can't flow any further
            if spring[right(pos)] == '#':
                right_wall = current_x
                break

        # we have a still water layer
        # mark all flowing water blocks above our still layer
        # as potential sources
        if left_wall is not None and right_wall is not None:
            for current_x in range(left_wall,right_wall+1):
                pos = (current_x, y)
                spring[pos] = '~'
                if spring[up(pos)] == '|':
                    current_sources.add(up(pos))

    c = Counter([spring[q] for q in spring if q[1] >= 0 and q[1] < ymaxx])

    print('Part 1:', c['|'] + c['~'])
    print('Part 2:', c['~'])

if __name__ == '__main__':
    main()