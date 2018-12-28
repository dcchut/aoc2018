from utils import load_input, get_numbers


class Army(object):
    def __init__(self, _type, _units, _hp, _dmg, _dmg_type,  _initiative, _weakness, _immunity):
        self.type = _type
        self.units = int(_units)
        self.hp = int(_hp)
        self.dmg = int(_dmg)
        self.dmg_type = _dmg_type
        self.initiative = int(_initiative)
        self.weakness = _weakness
        self.immunity = _immunity

    def effective_power(self):
        return self.units * self.dmg

    def dmg_to(self, other):
        # compute the damage that self would deal to other army, accounting for weaknesses and immunities
        if (self.dmg_type in other.immunity):
            return 0

        if (self.dmg_type in other.weakness):
            return 2 * self.effective_power()

        return self.effective_power()

    def __repr__(self):
        return str((self.type, self.units, self.hp, self.dmg, self.dmg_type, self.initiative, self.weakness, self.immunity))


def parse_army(line):
    units, hp, dmg, initiative = get_numbers(line)

    # damage type?
    dmg_type = line.split(" damage")[0].split(" ")[-1]

    # weaknesses
    weaknesses = []
    if ('weak' in line):
        weaknesses = line.split('weak to ')[1]
        if (';' in weaknesses):
            weaknesses = weaknesses.split(';')[0]
        elif (')' in weaknesses):
            weaknesses = weaknesses.split(')')[0]
        weaknesses = weaknesses.split(', ')

    # immunities
    immunities = []
    if ('immune' in line):
        immunities = line.split('immune to ')[1]
        if (';' in immunities):
            immunities = immunities.split(';')[0]
        elif (')' in immunities):
            immunities = immunities.split(')')[0]
        immunities = immunities.split(', ')

    return units, hp, dmg, dmg_type, initiative, weaknesses, immunities


def simulate(puzzle_input, boost):
    puzzle_input = '\n'.join(puzzle_input).split('Infection:')
    immune_system = puzzle_input[0].split("\n")[1:-2]
    infection = puzzle_input[1].split("\n")[1:]

    armys = []

    for army in immune_system:
        a = Army('immune', *parse_army((army)))
        a.dmg += boost
        armys.append(a)

    for army in infection:
        a = Army('infection', *parse_army((army)))
        armys.append(a)

    while True:
        # now find the army with the highest effective power!
        armys.sort(key=lambda q: (q.effective_power(), q.initiative), reverse=True)

        targeted = set()
        targets = {}
        unit_was_killed = False

        for army in armys:
            # find a target for this army
            potential_target = None
            potential_max_dmg = 0

            for target in armys:
                # cannot target already targeted unit
                if target in targeted:
                    continue

                # no friendly fire
                if target.type == army.type:
                    continue

                # compute the dmg we would deal to target
                dmg_to = army.dmg_to(target)

                # if we wouldn't deal any damage to the target, just skip it instead
                if dmg_to == 0:
                    continue

                # now maximise the potential_max damage, breaking ties by looking at the target's
                # effective power, and then breaking further ties by looking at the target's initiative
                if dmg_to < potential_max_dmg:
                    continue
                elif potential_target is not None and dmg_to == potential_max_dmg:
                    if target.effective_power() > potential_target.effective_power():
                        potential_target = target
                        potential_max_dmg = dmg_to
                    elif target.effective_power() == potential_target.effective_power():
                        if target.initiative > potential_target.initiative:
                            potential_target = target
                            potential_max_dmg = dmg_to
                else:
                    potential_target = target
                    potential_max_dmg = dmg_to

            # no target
            if potential_target is None or potential_max_dmg == 0:
                continue

            # otherwise add the target to targeted
            targeted.add(potential_target)
            targets[army] = potential_target

        # now sort the armies that have targets in initiative order (decreasing)
        k = list(targets.keys())
        k.sort(key=lambda q:q.initiative, reverse=True)

        for army in k:
            target = targets[army]
            dmg_to = army.dmg_to(target)

            # kill the right number of units
            units_killed = min(dmg_to // target.hp, target.units)
            if (units_killed > 0):
                unit_was_killed = True

            target.units -= units_killed

        # now how many armies have survived?
        surviving_armies = []

        for army in armys:
            if army.units > 0:
                surviving_armies.append(army)

        armys = surviving_armies

        if not unit_was_killed:
            # which army won?
            types = set()

            c = 0
            for a in armys:
                types.add(a.type)
                c += a.units

            # stalemate
            if len(types) == 2:
                return 'infection-sm', c
            elif 'immune' in types:
                return 'immune', c
            else:
                return 'infection', c


def main():
    puzzle_input = load_input('input.txt')

    _, pts = simulate(puzzle_input, 0)
    print('Part 1:', pts)

    # look for the smallest boost where the immune system outright wins
    boost = 0
    while True:
        winner, c = simulate(puzzle_input, boost)
        if winner == 'immune':
            print('Part 2:', c)
            break
        boost += 1


if __name__ == '__main__':
    main()