from utils import load_input


def get_base_units(polymer):
    return set(list(polymer.lower()))


def build_replace_strings(base_units):
    replace_strings = []

    # build a list of strings that get annihilated during reaction
    for b in base_units:
        u = b.upper()
        replace_strings.append(b + u)
        replace_strings.append(u + b)

    return replace_strings


def react(polymer,base_units):
    # get the replacement strings
    replace_strings = build_replace_strings(base_units)
    length = len(replace_strings)

    # keep applying our replacement until no change occurs
    j = 0
    while j < length:
        current_length = len(polymer)
        for rs in replace_strings:
            polymer = polymer.replace(rs,'')

            # did a reaction occur?
            new_length = len(polymer)

            if new_length < current_length:
                # we set j to -1 here because we'll increment it y 1 at the end of the while loop
                j = -1
                break
        j += 1

    return polymer


def part1(polymer):
    # do the reaction, return the length
    return len(react(polymer, get_base_units(polymer)))


def part2(polymer):
    base_units = get_base_units(polymer)

    # it is safe to first react, then try removing each unit in turn
    polymer = react(polymer, base_units)

    # find the base unit that, when removed, gives the smallest polymer after reacting
    return min([len(react(polymer.replace(q,'').replace(q.upper(),''),base_units)) for q in base_units])


if __name__ == '__main__':
    polymer = load_input('input.txt')[0]

    print('Part 1:', part1(polymer))
    print('Part 2:', part2(polymer))
