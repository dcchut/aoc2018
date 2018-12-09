from Day9.solution import winning_score


def test_winning_score():
    assert (winning_score(9, 25) == 32)
    assert (winning_score(10, 1618) == 8317)
    assert (winning_score(13, 7999) == 146373)
    assert (winning_score(17, 1104) == 2764)
    assert (winning_score(21, 6111) == 54718)
    assert (winning_score(30, 5807) == 37305)