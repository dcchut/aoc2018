from Day8.solution import treeverse

tree = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]


def test_treeverse():
    s,r = treeverse(tree.copy())

    assert(s == 138)
    assert(r == 66)