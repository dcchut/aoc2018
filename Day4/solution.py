from datetime import datetime
from collections import Counter
from utils import load_input


def process_timetable(timetable):
    # first we turn the date strings into genuine datetime objects
    # which allows us to sort the timetable by date
    chronological = []

    for d in timetable:
        dt, desc = d.split(']')

        # get the minute from the datetime
        minute = dt[-2:]

        # process the date
        dt_obj = datetime.strptime(dt[1:],'%Y-%m-%d %H:%M')

        chronological.append((dt_obj,minute, desc[1:]))

    # sort the timetable by chronological order
    chronological.sort(key=lambda x: x[0])

    # now process the entire timetable
    guard = -1
    tmp_log = []
    log = []

    sleep_start_minute = -1

    for entry in chronological:
        _,minute,desc = entry

        if 'begins shift' in desc:
            if guard != -1:
                log.append((int(guard), tmp_log))
            # get the new guard id
            guard = desc.split(' ')[1][1:]
            tmp_log = []

        if 'falls asleep' in desc:
            sleep_start_minute = int(minute)

        if 'wakes up' in desc:
            for i in range(sleep_start_minute, int(minute)):
                tmp_log.append(i)

    # append the final entry
    if guard != -1:
        log.append((int(guard),tmp_log))

    return log


def part1(log):
    minutes_slept = {}
    # find the guard with the most sleep minutes
    for guard, entry in log:
        if guard not in minutes_slept:
            minutes_slept[guard] = 0

        minutes_slept[guard] += len(entry)

    # guard who spent the most time asleep
    guard = max(minutes_slept, key=minutes_slept.get)

    # now find the minute that they slept the most
    filtered_log = [x for t in list(filter(lambda x: int(x[0]) == guard,log)) for x in t[1]]

    c = Counter(filtered_log)
    m = max(c,key=c.get)

    return guard * m


def part2(log):
    minutes_by_guard = {}
    # for each guard, we create a list of the minutes that guard spent sleeping (with repeats)
    for guard, entry in log:
        # dont bother with empty entries
        if len(entry) == 0:
            continue

        if guard not in minutes_by_guard:
            minutes_by_guard[guard] = []

        minutes_by_guard[guard].extend(entry)

    # for each guard, counter the entries for each minute
    counter_by_guard = [(q,Counter(minutes_by_guard[q])) for q in minutes_by_guard]

    # find the guard with the most frequently occurring sleep minute overall
    max_guard = max(counter_by_guard, key=lambda q: q[1][max(q[1],key=q[1].get)])

    # find the corresponding maximum minute for that guard
    max_key = max(max_guard[1],key=max_guard[1].get)

    return max_guard[0] * max_key


if __name__ == '__main__':
    timetable = load_input('input.txt')
    log = process_timetable(timetable)

    print('Part 1:', part1(log))
    print('Part 2:', part2(log))