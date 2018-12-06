from Day2.solution import part1, part2


def test_part1():
    assert(part1(['abcdef','bababc','abbcde','abcccd','aabcdd','abcdee','ababab']) == 12)


def test_part2():
    assert(part2(['abcde','fghij','klmno','pqrst','fguij','axcye','wvxyz']) == 'fgij')