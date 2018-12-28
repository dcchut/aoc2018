from utils import load_input, get_numbers, memoize
from collections import defaultdict


@memoize
def geologic_index(x,y):
    if x == 0 and y == 0:
        r = 0
    elif x == 0:
        r = y * 48271
    elif y == 0:
        r = x * 16807
    elif x == targetX and y == targetY:
        r = 0
    else:
        r = erosion(x-1, y) * erosion(x, y-1)

    return r


def erosion(x,y):
    return (geologic_index(x,y) + depth) % 20183


def region_type(x,y):
    e = erosion(x,y) % 3
    return e


def risk(xmax,ymax):
    r = 0
    # the risk of a given rctangle is the sum of the numerical region types
    # within that rectangle
    for y in range(ymax+1):
        for x in range(xmax+1):
            r += region_type(x,y)
    return r


def is_valid(p):
    return p[0] >= 0 and p[1] >= 0


puzzle_input = load_input('input.txt')

depth = get_numbers(puzzle_input[0])[0]
targetX, targetY = get_numbers(puzzle_input[1])

# this is a (rough) upper bound for the maximum length of the shortest path to the target point
maxTime = 8 * targetX + 8 * targetY

print('Part 1:',risk(targetX,targetY))

# PART 2
print('Computing geologic index...')
gi = {}
# we precompute some geologic indices to overcome the recursion limit of python
for x in range(1000):
    for y in range(1000):
       gi[(x,y)] = geologic_index(x,y)
print('done')

pathtime = defaultdict(dict)
pathtime[(0,0)] = {1: 0}

process = set([(1, (0,0))])
visited = set()

# equipment
# 0 = neither, 1 = torch, 2 = climbing gear
equipment = [0,1,2]

# region restrictions
# 0 = rocky - can only use climbing gear or torch
# 1 = web - can only use climbing gear or neither
# 2 = narrow - can only use torch or neither

# current_shortest_path_length holds the distance of the shortest (currently known) path to the target
current_shortest_path_length = maxTime

# the basic way we do this is to turn this into a 3D shortest path problem
# i.e. instead of thinking about the shortest path to a point (x,y),
# we think about the shortest path to a point (x,y) where you end up equipped with equipment z,
# our solution is then be the shortest path to (targetX, targetY, 1)
while len(process) > 0:
    # we pick the point in our process queue that is "closest", in the sense that
    # total length of path + manhattan distance to target is minimal
    equipped, p = min(process, key=lambda q: pathtime[q[1]][q[0]] + abs(q[1][0]-targetX)+abs(q[1][1]-targetY))
    process.remove((equipped,p))

    # ignore paths which are longer than the length of our current shortest path
    if pathtime[p][equipped] > current_shortest_path_length:
        continue

    current_region_type = region_type(*p)

    # there are two possible actions we could take -
    # either we change equipment,
    for target_equipped in equipment:
        if target_equipped == equipped:
            continue
        # cannot have neither equipped in rocky
        if target_equipped == 0 and current_region_type == 0:
            continue
        # cannot have torch equipped in web
        if target_equipped == 1 and current_region_type == 1:
            continue
        # cannot have climbing gear equipped in narrow
        if target_equipped == 2 and current_region_type == 2:
            continue

        # otherwise, figure out if this gives us a new shortest path to a particular point
        if target_equipped in pathtime[p]:
            if pathtime[p][equipped] + 7 < pathtime[p][target_equipped]:
                pathtime[p][target_equipped] = pathtime[p][equipped] + 7
                process.add((target_equipped, p))
        else:
            pathtime[p][target_equipped] = pathtime[p][equipped] + 7
            process.add((target_equipped, p))

    # or we move to an adjacent spot
    left = (p[0]-1,p[1])
    right = (p[0]+1,p[1])
    up = (p[0],p[1]-1)
    down = (p[0],p[1]+1)

    for q in [left,right,up,down]:
        if not is_valid(q):
            continue

        # do we have the right equipment to move here?
        target_region_type = region_type(*q)

        if equipped == target_region_type:
            continue
        else:
            if equipped in pathtime[q]:
                if pathtime[p][equipped]+1 < pathtime[q][equipped]:
                    pathtime[q][equipped] = pathtime[p][equipped]+1
                    process.add((equipped,q))
            else:
                pathtime[q][equipped] = pathtime[p][equipped]+1
                process.add((equipped,q))

    if (targetX,targetY) in pathtime and 1 in pathtime[(targetX,targetY)]:
        target_path_length = pathtime[(targetX, targetY)][1]

        if target_path_length < current_shortest_path_length:
            current_shortest_path_length = target_path_length
            print(target_path_length)