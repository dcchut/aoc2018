from collections import defaultdict

from utils import load_input


def simulation(board, attack_power):

    b = defaultdict(bool)
    units = {}
    elves = []
    goblins = []
    k = 0

    # go through every position on the board, marking whether it is a valid/invalid position for a unit to be
    # we also determine where each unit begins
    for (y, line) in enumerate(board):
        for (x, e) in enumerate(line):
            entry = False
            if e == ".":
                entry = True
            if e == "E":
                entry = True
                units[(x,y)] = ('E',k,200)
                k += 1
                elves.append((x,y))
            if e == "G":
                entry = True
                units[(x,y)] = ('G',k,200)
                k += 1
                goblins.append((x,y))
            b[(x,y)] = entry

    elf_count_total = len(elves)
    game_over = False
    round_counter = 0

    while not game_over:
        round_counter += 1
        # STEP 1
        # determine the turn order by "reading order" at the start of the round
        ordered_units = sorted(list(units.keys()),key=lambda e: (e[1],e[0]))

        # if a unit dies during a round, it may still occur in our turn order,
        # so we keep track of units that we should skip
        dead_units = []

        for unit in ordered_units:
            if unit in dead_units:
                continue

            # combat ends when there are no targets remaining
            if len(elves) == 0 or len(goblins) == 0:
                game_over = True
                break

            # we set source and targets to be good guys/bad guys from the perspective of this unit
            if units[unit][0] == 'E':
                source = elves
                targets = goblins
            else:
                source = goblins
                targets = elves

            # FIRST CHECK - are there any target units adjacent to this unit?
            # at the same time we do this, we compute the set of all possible spots,
            # that is, valid spots adjacent to targets that are not currently occupied

            possible_spots = set()
            adjacent = False
            for target in targets:
                left = (target[0]-1,target[1])
                right = (target[0]+1,target[1])
                up = (target[0],target[1]-1)
                down= (target[0],target[1]+1)

                # if we are next to a target, we don't need to worry about possible spots,
                # so we can stop here
                if left == unit or right == unit or up == unit or down == unit:
                    adjacent = True
                    break

                # otherwise keep track of the valid unoccupied spots adjacent to targets
                if b[left] and left not in units:
                    possible_spots.add(left)
                if b[right] and right not in units:
                    possible_spots.add(right)
                if b[up] and up not in units:
                    possible_spots.add(up)
                if b[down] and down not in units:
                    possible_spots.add(down)
#
            # if the unit is not adjacent to a target and there are no possible spots,
            # then the unit ends its turn
            if not adjacent and len(possible_spots) == 0:
                continue

            if not adjacent and len(possible_spots) > 0:
                # if the unit is not adjacent to a target, it MOVES

                # first, find the shortest paths from the unit to a possible_spot
                shortest_paths = {unit : (0, [])}
                d = 1

                while True:
                    found_good_pt = []
                    next_shortest_paths = shortest_paths.copy()
                    # keep track of whether we found a new coordinate in this round,
                    changed = False

                    for pt in shortest_paths:
                        left = (pt[0]- 1, pt[1])
                        right = (pt[0] + 1, pt[1])
                        up = (pt[0], pt[1] - 1)
                        down = (pt[0], pt[1] + 1)

                        for q in [left, right, up, down]:
                            # if this is a valid spot, and if it is unoccupied
                            if b[q] and q not in units:
                                # if this is a possible_spot, write it down as reachable from the unit
                                if q in possible_spots:
                                    found_good_pt.append(q)
                                # if this node isn't in our shortest paths list already, then add it
                                if q not in next_shortest_paths:
                                    next_shortest_paths[q] = (d, [pt])
                                    changed = True
                                elif d == next_shortest_paths[q][0]:
                                    next_shortest_paths[q][1].append(pt)
                                    changed = True
                    shortest_paths = next_shortest_paths

                    # if we found a target spot, or if the list of shortest paths hasn't changed (i.e. there
                    # is no shorted path from the unit to a possible spot), then we stop our search
                    if len(found_good_pt) > 0 or not changed:
                        break
                    d += 1

                # if changed is true, then we found a possible spot that is reachable from unit
                if changed:
                    # get the position of the closest reachable target, in reading order
                    found_good_pt.sort(key=lambda e: (e[1], e[0]))
                    pt = found_good_pt[0]

                    # now we find the shortest path(s) from unit to the target
                    # using our shortest paths dict we created above
                    curr = [[pt]]
                    finished = False

                    while not finished:
                        new_curr = []
                        for qt in curr:
                            # get the last entry of qt
                            last = qt[-1]
                            # find all predecessors of this point
                            for prev in shortest_paths[last][1]:
                                new_curr.append(qt + [prev])
                                if prev == unit:
                                    finished = True
                        curr = new_curr

                    # now get the first step of each of the paths, and sort by reading order
                    first_steps = list(set([q[-2] for q in curr]))
                    first_steps.sort(key=lambda e: (e[1],e[0]))

                    # move the unit to first_steps[0]
                    e = units[unit]
                    del units[unit]
                    units[first_steps[0]] = e
                    source.remove(unit)
                    source.append(first_steps[0])
                    unit = first_steps[0]

            # after (possibly) moving, we check whether we have any adjacent targest to attack
            adjacent_targets = []
            left = (unit[0]-1,unit[1])
            right = (unit[0]+1,unit[1])
            up = (unit[0],unit[1]-1)
            down = (unit[0],unit[1]+1)

            if left in targets:
                adjacent_targets.append(left)
            if right in targets:
                adjacent_targets.append(right)
            if up in targets:
                adjacent_targets.append(up)
            if down in targets:
                adjacent_targets.append(down)

            if len(adjacent_targets) > 0:
                # find the adjacent targets with the minimum hp
                min_adjacent_hp = 0
                min_adjacent_targets = []
                for target in adjacent_targets:
                    if len(min_adjacent_targets) == 0 or units[target][2] < min_adjacent_hp:
                        min_adjacent_hp = units[target][2]
                        min_adjacent_targets = [target]
                    elif units[target][2] == min_adjacent_hp:
                        min_adjacent_targets.append(target)

                # there might be multiple adjacent targets with equal hp,
                # in which case we pick the target that comes first in reading order
                min_adjacent_targets.sort(key=lambda e: (e[1],e[0]))
                min_target = min_adjacent_targets[0]

                e = units[min_target]
                if units[unit][0] == 'E':
                    # if the unit is an elf, we attack with our attack_power
                    new_hp = e[2] - attack_power
                else:
                    # if the unit is a goblin, deal 3
                    new_hp = e[2] - 3

                # set the targets hp
                units[min_target] = (e[0],e[1],new_hp)

                # if the target died, then delete it from the appropriate lists
                if units[min_target][2] <= 0:
                    # this unit is dead!
                    targets.remove(min_target)
                    del units[min_target]
                    dead_units.append(min_target)
        # END OF ROUND

    # when the game is over, count (1) the number of elves that survived, and (2) the hp total
    elf_count = 0
    hp_total = 0
    for unit in units:
        hp_total += units[unit][2]
        if units[unit][0] == 'E':
            elf_count += 1

    # we return (1) whether all elves survived, and (2) the round outcome
    return elf_count == elf_count_total, hp_total * (round_counter - 1)


def main():
    board = load_input('input.txt')

    k = 3
    while True:
        all_elves_survived, outcome = simulation(board, k)
        if k == 3:
            print('Part 1:', outcome)
        elif all_elves_survived:
            # this is the first attack damage for which all elves survived
            print('Part 2:', outcome)
            break
        k += 1


if __name__ == '__main__':
    main()