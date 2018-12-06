from Day1.solution import part1, part2


def test_part1():
    assert(part1([1,-2,3,1]) == 3)
    assert(part1([1,1,1]) == 3)
    assert(part1([1,1,-2]) == 0)
    assert(part1([-1,-2,-3]) == -6)


def test_part2():
    assert(part2([1,-2,3,1]) == 2)
    assert(part2([1,-1]) == 0)
    assert(part2([3,3,4,-2,-4]) == 10)
    assert(part2([-6,3,8,5,-6]) == 5)
    assert(part2([7,7,2,-7,-4]) == 14)