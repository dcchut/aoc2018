from utils import load_input


def north(pos):
    return pos[0],pos[1]+1


def south(pos):
    return pos[0],pos[1]-1


def east(pos):
    return pos[0]+1,pos[1]


def west(pos):
    return pos[0]-1,pos[1]


class Room(object):
    def __init__(self, _pos):
        self.pos = _pos
        self.neighbours = set()

    def add_neighbour(self,other):
        self.neighbours.add(other)

    def __repr__(self):
        s = f"Room @ {self.pos[0],self.pos[1]} w/ neighbours: "
        s += ' '.join([str(q.pos) for q in self.neighbours])
        s += '.'
        return s


def map_doors(pos, puzzle_input):
    door = []
    level = 0
    branch = {0: pos}
    branch_pos = {0: pos}

    for q in puzzle_input:
        if q == 'N':
            door.append((branch_pos[level],north(branch_pos[level])))
            branch_pos[level] = north(branch_pos[level])
        elif q == 'S':
            door.append((branch_pos[level],south(branch_pos[level])))
            branch_pos[level] = south(branch_pos[level])
        elif q == 'E':
            door.append((branch_pos[level],east(branch_pos[level])))
            branch_pos[level] = east(branch_pos[level])
        elif q == 'W':
            door.append((branch_pos[level],west(branch_pos[level])))
            branch_pos[level] = west(branch_pos[level])
        elif q == '(':
            level += 1
            branch_pos[level] = branch_pos[level-1]
            branch[level] = branch_pos[level]
        elif q == '|':
            branch_pos[level] = branch[level]
        elif q == ')':
            level -= 1
    return door


def main():
    door = map_doors((0,0), load_input('input.txt')[0])
    rooms = {}

    # link up each of the rooms
    for start, end in door:
        if start not in rooms:
            rooms[start] = Room(start)
        if end not in rooms:
            rooms[end] = Room(end)
        rooms[start].add_neighbour(rooms[end])
        rooms[end].add_neighbour(rooms[start])

    # compute the shortest distance from (0,0) to every room
    distances = {(0,0): 0}
    to_process = set([rooms[(0,0)]])

    while len(to_process) > 0:
        room = to_process.pop()

        for adjacent_room in room.neighbours:
            if adjacent_room.pos not in distances:
                distances[adjacent_room.pos] = distances[room.pos]+1
                to_process.add(adjacent_room)
            else:
                if distances[room.pos] + 1 < distances[adjacent_room.pos]:
                    distances[adjacent_room.pos] = distances[room.pos]+1
                    to_process.add(adjacent_room)

    c = 0
    for pos in distances:
        # count the number of points that are at least a distance 1000 away
        if distances[pos] >= 1000:
            c += 1

    m = max(distances,key=distances.get)
    print('Part 1:', distances[m])
    print('Part 2:', c)


if __name__ == '__main__':
    main()