from Day6.solution import part1, part2

testdata = [[1, 1], [1, 6], [8, 3], [3, 4], [5, 5], [8, 9]]


def test_part1():
    assert (part1(testdata) == 17)


def test_part2():
    assert (part2(testdata, boundary=10, limit=32) == 16)
