from utils import load_input


def process_input(line):
    s = line.split()

    x, y = s[2][:-1].split(',')
    w, h = s[3].split('x')
    i = s[0][1:]

    return int(i), int(x), int(y), int(w), int(h)


def fill_board_entry(board, _, x, y, w, h):
    for i in range(x, x + w):
        for j in range(y, y + h):
            if (i, j) not in board:
                board[(i, j)] = 0
            board[(i, j)] += 1


def fill_board(entries):
    board = {}

    for entry in entries:
        fill_board_entry(board, *entry)

    return board


def part1(entries):
    board = fill_board(entries)

    # count overlaps
    return sum(1 if board[p] > 1 else 0 for p in board)


def part2(entries):
    board = fill_board(entries)

    for entry in entries:
        id_, x, y, w, h = entry
        overlap = False
        for i in range(x, x + w):
            for j in range(y, y + h):
                if board[(i, j)] > 1:
                    overlap = True
                    break
            if overlap:
                break
        # no overlap found!
        if not overlap:
            return id_

    # how did we get here?
    assert False


def main():
    processed_input = [process_input(q) for q in load_input('input.txt')]

    print('Part 1:', part1(processed_input))
    print('Part 2:', part2(processed_input))


if __name__ == '__main__':
    main()
