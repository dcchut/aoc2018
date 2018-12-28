from utils import load_input, get_numbers, manhattan_distance


def main(puzzle_input):
    points = []

    for line in puzzle_input:
        points.append(tuple(get_numbers((line))))

    # compute the distance between every pair of points
    distances = { p : { q : manhattan_distance(p,q) for q in points} for p in points}

    # for each point, find the constellation of points that it contains
    constellations = 0
    points_in_constellation = set()
    points_remaining = set(points)
    # basically we pick a point that isn't in a constellation, and then keep working
    # away from that point until we've found the entire constellation
    while True:
        # no more points remaining!
        if len(points_remaining) == 0:
            break

        p = points_remaining.pop()
        to_process = set([p])
        points_in_constellation.add(p)

        while len(to_process) > 0:
            p = to_process.pop()

            # get all the points that are within a distance of 3 of our current processing points
            qs = { q for q in points_remaining if distances[p][q] <= 3}

            points_remaining = points_remaining.difference(qs)
            points_in_constellation = points_in_constellation.union(qs)
            to_process = to_process.union(qs)

        constellations += 1

    return constellations

if __name__ == '__main__':
    print('Part 1:', main(load_input('input.txt')))
