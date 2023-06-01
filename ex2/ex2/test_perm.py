from perm import perm_crossover_pbx, perm_crossover_pmx, perm_mutate_inversion

trans = lambda x: ord(x) - ord("A")


def test_mutate_inversion():
    assert perm_mutate_inversion(tuple(map(trans, "ABCDEFG")), 5, 1) == tuple(
        map(trans, "GFCDEBA")
    )
    assert perm_mutate_inversion(tuple(map(trans, "ABCDEFG")), 1, 5) == tuple(
        map(trans, "AFEDCBG")
    )
    # res = perm_mutate_inversion(
    #     (
    #         7,
    #         21,
    #         18,
    #         11,
    #         4,
    #         12,
    #         22,
    #         3,
    #         0,
    #         10,
    #         19,
    #         14,
    #         16,
    #         6,
    #         25,
    #         13,
    #         1,
    #         20,
    #         5,
    #         17,
    #         24,
    #         9,
    #         15,
    #         23,
    #         2,
    #         8,
    #     ),
    #     23,
    #     19,
    # )
    # print(res)
    # assert res == None


def test_crossover_pmx():
    assert perm_crossover_pmx(
        tuple(map(trans, "ABCDEFGH")), tuple(map(trans, "CGEAFHBD")), 3, 5
    ) == tuple(map(trans, "CGHDEFBA"))


def test_crossover_pbx():
    assert perm_crossover_pbx(
        tuple(map(trans, "314675298")),
        tuple(map(trans, "347129685")),
        [0, 1, 0, 1, 0, 0, 1, 1, 0],
    ) == tuple(map(trans, "314678295"))
