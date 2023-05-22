import random

from perm import (bs2n, decode_perm, encode_perm, lehmer_to_num,
                  lehmer_to_perm, n2bs, num_to_lehmer, perm_to_lehmer)


def test_n2bs():
    assert n2bs(0, 8) == "0" * 3
    assert n2bs(0, 9) == "0" * 4
    assert n2bs(7, 8) == "111"
    assert n2bs(7, 9) == "0111"


def test_bs2n():
    assert bs2n("000", 8) == 0
    assert bs2n("000", 9) == 0
    assert bs2n("0000", 9) == 0
    assert bs2n("111", 8) == 7
    assert bs2n("111", 9) == 7
    assert bs2n("0111", 9) == 7
    assert bs2n("1111", 8) == 7
    assert bs2n("1111", 9) == 6


def test_bs2n_n2bs():
    for _ in range(100):
        bits = random.randint(1, 8)
        max = 2**bits
        n = random.randint(0, max - 1)
        assert bs2n(n2bs(n, max), max) == n


KNOWN_ENC = [
    ([0, 0, 0], 0),
    ([1, 0, 0], 1),
]


def test_num_to_lehmer():
    for lehmer, num in KNOWN_ENC:
        assert num_to_lehmer(num, len(lehmer)) == lehmer


def test_lehmer_to_num():
    for lehmer, num in KNOWN_ENC:
        assert lehmer_to_num(lehmer) == num


def test_lehmer_and_num():
    for _ in range(100):
        l = random.randint(1, 8)
        lehmer = [random.randint(0, l - i - 1) for i in range(l)]
        assert num_to_lehmer(lehmer_to_num(lehmer), len(lehmer)) == lehmer


PERM2LEHMER = [
    ([0, 1, 2, 3], [0, 0, 0, 0]),
    ([1, 0, 2, 3], [1, 0, 0, 0]),
    ([0, 1, 3, 2], [0, 0, 1, 0]),
]


def test_perm_to_lehmer():
    for perm, lehmer in PERM2LEHMER:
        assert perm_to_lehmer(perm) == lehmer


def test_lehmer_to_perm():
    for perm, lehmer in PERM2LEHMER:
        assert lehmer_to_perm(lehmer) == perm


def test_encode_decode_perm():
    for _ in range(100):
        n = 4
        perm = list(range(n))

        random.shuffle(perm)
        print(f"perm: {perm}")
        encoded = encode_perm(perm)
        print(f"encoded: {encoded}")
        decoded = decode_perm(encoded, len(perm))
        print(f"decoded: {decoded}")
        assert decoded == perm
