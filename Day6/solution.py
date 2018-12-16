import multiprocessing
from collections import Counter

from joblib import Parallel, delayed

from utils import load_input, get_numbers


def distance(p, q):
    return abs(q[0] - p[0]) + abs(q[1] - p[1])


def find_closest(q, point_list):
    min_distance = None
    min_k = None
    min_multi = False

    for (k, p) in enumerate(point_list):
        d = distance(p, q)
        if min_distance is None or d < min_distance:
            min_distance = distance(p, q)
            min_k = k
            min_multi = False
        elif d == min_distance:
            # if we have equality, then this coordinate has (at least two) equidistant points
            min_multi = True

    # multiple points were equidistant to this one
    if min_multi:
        return None

    return min_k


def part1_worker(point_list, i, j_list):
    closest = {}
    for j in j_list:
        closest[(i, j)] = find_closest((i, j), point_list)
    return closest


def part1(point_list):
    xmin = -2 * min(q[0] for q in point_list)
    xmax = 2 * max(q[0] for q in point_list)
    ymin = -2 * min(q[1] for q in point_list)
    ymax = 2 * max(q[1] for q in point_list)

    parallel_inputs = [(i, range(ymin, ymax + 1)) for i in range(xmin, xmax + 1)]
    num_cores = multiprocessing.cpu_count()

    # find the closest point to each coordinate in our region
    results = Parallel(n_jobs=num_cores)(delayed(part1_worker)(point_list, *q) for q in parallel_inputs)

    # merge all of the results together
    closest = {}
    for k in results:
        closest.update(k)

    # anything that lies on the boundary is part of an infinite region,
    # so we ignore these points
    invalid = set()
    for j in range(ymin, ymax + 1):
        invalid.add(closest[(xmin, j)])
        invalid.add(closest[(xmax, j)])

    for i in range(xmin, xmax + 1):
        invalid.add(closest[(i, ymin)])
        invalid.add(closest[(i, ymax)])

    # filter out the invalid values
    values = filter(lambda q: q not in invalid, closest.values())

    # get the largest non-infinite region
    return max(Counter(values).values())


def part2_worker(point_list, limit, i, j_list):
    # we can save a little time by checking that
    # s doesn't exceed 10000 already here
    s = sum([abs(p[0] - i) for p in point_list])
    if s >= limit:
        return 0

    inc = 0
    for j in j_list:
        t = s
        for p in point_list:
            t += abs(p[1] - j)
            # if the sum exceeds 10000, then we're done
            if t >= limit:
                break
        # otherwise this coordinate is within 10,000 of every point
        if t < limit:
            inc += 1

    return inc


def part2(point_list, boundary=1000, limit=10000):
    # create a list of all the different coordinate ranges, and them apply our worker
    # function in parallel to count how many points within each range
    # have sum manhattan distance less than limit
    parallel_inputs = [(i, range(-boundary, boundary)) for i in range(-boundary, boundary)]

    num_cores = multiprocessing.cpu_count()
    return sum(Parallel(n_jobs=num_cores)(delayed(part2_worker)(point_list, limit, *q) for q in parallel_inputs))


def main():
    # get the list of points
    points = [get_numbers(q) for q in load_input('input.txt')]

    print('Part 1:', part1(points))
    print('Part 2:', part2(points))


if __name__ == '__main__':
    main()
