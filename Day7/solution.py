from collections import defaultdict

from utils import load_input


def part1(keys, mapped_to):
    word = ''

    while len(keys) > 0:
        # find the possible places that we could start next
        starting_points = []
        for k in keys:
            if k not in mapped_to or len(mapped_to[k]) == 0:
                starting_points.append(k)

        # arrange all possible starting points in alphabetical order
        starting_points.sort()

        # now choose the first starting point
        starting_point = starting_points.pop(0)
        word += starting_point

        # remove all occurrences of our starting point from mapped_to
        # this essentially means we consider starting_point as done,
        mapped_to = {k: list(filter(lambda x: x != starting_point, mapped_to[k])) for k in mapped_to}

        # remove the starting point from keys
        keys.remove(starting_point)

    return word


def letter_to_number(letter):
    return ord(letter.lower()) - 96


def part2(keys, mapped_to, workers=5, base_time=60):
    available_until = []
    time = 0

    while len(keys) > 0:
        starting_points = []
        for k in keys:
            if k not in mapped_to or len(mapped_to[k]) == 0:
                starting_points.append(k)

        # we don't want any starting points that we're already working on,
        # but that we haven't yet removed from mapped_to
        started_jobs = [q[0] for q in available_until]
        starting_points = [x for x in starting_points if x not in started_jobs]
        starting_points.sort()

        # for each available starting point, assign a worker (if available)
        while workers > 0 and len(starting_points) > 0:
            workers -= 1
            job =  starting_points.pop(0)
            # the job goes until time + base_time + job - 1
            available_until.append((job, time + base_time + letter_to_number(job) - 1))

        # for each finished job, free up a worker
        finished_jobs = [q[0] for q in available_until if q[1] == time]
        workers += len(finished_jobs)

        # get a new list of the unfinished jobs
        available_until = [q for q in available_until if q[1] != time]

        # remove all of the finished jobs from our graph
        mapped_to = { k : list(filter(lambda q: q not in finished_jobs, mapped_to[k])) for k in mapped_to }

        for job in finished_jobs:
            keys.remove(job)

        # increment the time counter
        time += 1

    return time

def main():
    # get the list of step orderings
    steps = load_input('input.txt')

    # write down the graph
    mapped_to = defaultdict(list)
    keys = set()
    for line in steps:
        x = line.split()

        # step a must be finished before step b
        a = x[1]
        b = x[7]

        # add the keys
        keys.add(a)
        keys.add(b)

        # a is mapped to b
        mapped_to[b].append(a)

    print('Part 1:', part1(keys.copy(), mapped_to.copy()))
    print('Part 2:', part2(keys.copy(), mapped_to.copy()))


if __name__ == '__main__':
    main()
