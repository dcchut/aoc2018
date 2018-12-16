from collections import defaultdict

from utils import load_input


def is_hash(x):
    if x == '#':
        return True
    else:
        return False


def step(state, rules):
    # simulate a step, applying the rules to our state
    mi = min(state.keys()) - 3
    mx = max(state.keys()) + 3

    new_state = defaultdict(bool)
    # we generate a 'signature' for each state - this allows us to easily detect whether
    # two states are the same, up to a shift
    signature = ''

    for k in range(mi, mx):
        # is there a rule that applies to this situation?
        t = (state[k - 2], state[k - 1], state[k], state[k + 1], state[k + 2])
        if t in rules and rules[t]:
            new_state[k] = rules[t]
            signature += '#'
        else:
            # we use a space here so that trailing/leading spaces are removed from the signature
            # via the strip() method below
            signature += ' '

    # maybe resize state?
    return new_state, signature.strip()


def setup(lines):
    initial_state = lines[0][15:]
    moves = lines[2:]

    # parse the moves into a set of understandable rules
    rules = {}
    for move in moves:
        q = tuple([is_hash(move[k]) for k in range(5)])
        target = is_hash(move[-1])
        rules[q] = target

    # setup the initial state
    state = defaultdict(bool)
    state.update({k: is_hash(x) for (k, x) in enumerate(initial_state)})

    return rules, state


def state_sum(state):
    s = 0
    for q in state:
        if state[q]:
            s += q
    return s


def part1(lines):
    rules, state = setup(lines)

    # mutate for 20 generations
    for k in range(0, 20):
        state, _ = step(state, rules)

    # now compute the sum
    return state_sum(state)


def part2(lines):
    rules, state = setup(lines)
    old_signature = None

    k = 0
    while True:
        updated, signature = step(state, rules)
        if signature == old_signature:
            # we have convergence - now the signature will remain unchanged forever,
            # but the plants may shift in a particular direction
            old_sum = state_sum(state)
            new_sum = state_sum(updated)
            # delta is the amount that the signature changes by every step
            delta = new_sum - old_sum
            return old_sum + (50000000000 - k) * delta
        else:
            old_signature = signature
            state = updated
            k += 1


def main():
    lines = load_input('input.txt')

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == '__main__':
    main()
