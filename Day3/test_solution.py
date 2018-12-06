from Day3.solution import part1, part2


def test_part1():
    assert (part1([[1, 1, 3, 4, 4],
                   [2, 3, 1, 4, 4],
                   [3, 5, 5, 2, 2]]) == 4)


def test_part2():
    assert (part2([[1, 1, 3, 4, 4],
                   [2, 3, 1, 4, 4],
                   [3, 5, 5, 2, 2]]) == 3)
