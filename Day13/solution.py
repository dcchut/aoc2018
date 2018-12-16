from collections import defaultdict

from utils import load_input


def tick(board, carts):
    done_already = set()

    # sort the carts
    sorted_cart_keys = sorted(carts.keys(), key=lambda e: (e[1], e[0]))
    deleted_keys = []

    for (x, y) in sorted_cart_keys:
        # if this cart has been destroyed, then we don't move it
        if (x, y) in deleted_keys:
            continue

        direction, state, id = carts[(x, y)]

        # if we've already moved this cart this round somehow,
        # just skip it
        if id in done_already:
            continue

        # find the coordinate of the place this cart is moving to
        tx = x
        ty = y

        if direction == 'N':
            ty -= 1
        elif direction == 'S':
            ty += 1
        elif direction == 'E':
            tx += 1
        elif direction == 'W':
            tx -= 1

        new_carts = carts.copy()

        # is there a cart at the target position?
        if (tx, ty) in carts:
            # remove the two carts from the simulation
            del new_carts[(x, y)]
            del new_carts[(tx, ty)]
            deleted_keys.append((tx, ty))
            deleted_keys.append((x, y))
            carts = new_carts
            continue

        # if there is no cart at the target position, determine if a change in direction is necessary
        target_board_state = board[(tx, ty)]

        piece_mappings = {3: {'N': 'E', 'S': 'W', 'E': 'N', 'W': 'S'},
                          4: {'N': 'W', 'S': 'E', 'E': 'S', 'W': 'N'},
                          5: [{'N': 'W', 'S': 'E', 'E': 'N', 'W': 'S'},
                              {},
                              {'N': 'E', 'S': 'W', 'E': 'S', 'W': 'N'}]}

        new_direction = direction
        new_state = state

        if target_board_state == 3 or target_board_state == 4:
            new_direction = piece_mappings[target_board_state][direction]
        elif target_board_state == 5:
            if direction in piece_mappings[5][state]:
                new_direction = piece_mappings[5][state][direction]
            new_state = (state + 1) % 3

        del new_carts[(x, y)]
        new_carts[(tx, ty)] = [new_direction, new_state, id]
        done_already.add(id)
        carts = new_carts
    return carts, deleted_keys


def main():
    # get the list of step orderings
    track = load_input('input.txt')
    board = defaultdict(int)
    carts = {}
    k = 0

    for (y, line) in enumerate(track):
        for (x, c) in enumerate(line):
            b = None
            if c == '|':
                b = 1
            if c == '-':
                b = 2
            if c == '/':
                b = 3
            if c == '\\':
                b = 4
            if c == '+':
                b = 5
            if c == '^':
                carts[(x, y)] = ['N', 0, k]
                b = 1
                k += 1
            if c == 'v':
                carts[(x, y)] = ['S', 0, k]
                b = 1
                k += 1
            if c == '>':
                carts[(x, y)] = ['E', 0, k]
                b = 2
                k += 1
            if c == '<':
                carts[(x, y)] = ['W', 0, k]
                b = 2
                k += 1
            if b is not None:
                board[(x, y)] = b

    has_crashed = False
    while True:
        carts, deleted_keys = tick(board, carts)
        # when the first crash occurs, we obtain our solution to part 1
        if not has_crashed and len(deleted_keys) > 0:
            has_crashed = True
            print("Part 1:", deleted_keys[0])

        # when only one cart remains, we have our solution to part 2
        if len(carts) == 1:
            print("Part 2:", list(carts.keys())[0])
            break


if __name__ == '__main__':
    main()
