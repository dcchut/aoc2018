from Day7.solution import part1, part2
from collections import defaultdict

# set up our test tree
keys = set(['A', 'D', 'E', 'F', 'C', 'B'])

mapped_to = defaultdict(list)
mapped_to['A'] = ['C']
mapped_to['F'] = ['C']
mapped_to['B'] = ['A']
mapped_to['D'] = ['A']
mapped_to['E'] = ['B', 'D', 'F']


def test_part1():
    assert(part1(keys.copy(), mapped_to.copy()) == 'CABDFE')


def test_part2():
    assert(part2(keys.copy(), mapped_to.copy(), workers=2, base_time=0) == 15)