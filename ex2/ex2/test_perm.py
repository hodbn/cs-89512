from perm import perm_crossover_pmx, perm_mutate_inversion

trans = lambda x: ord(x) - ord("A")


def test_mutate_inversion():
    assert perm_mutate_inversion(tuple(map(trans, "ABCDEFG")), 5, 1) == tuple(
        map(trans, "GFCDEBA")
    )
    assert perm_mutate_inversion(tuple(map(trans, "ABCDEFG")), 1, 5) == tuple(
        map(trans, "AFEDCBG")
    )


def test_crossover_pmx():
    assert perm_crossover_pmx(
        tuple(map(trans, "ABCDEFGH")), tuple(map(trans, "CGEAFHBD")), 3, 5
    ) == tuple(map(trans, "CGHDEFBA"))
