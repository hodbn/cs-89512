import math


def bits(max: int):
    return math.ceil(math.log2(max))


def n2bs(n: int, max: int) -> str:
    b = bits(max)
    return str(bin(n))[2:].zfill(b)[:b]


def bs2n(bs: str, max: int) -> int:
    return int(bs, 2) % max


def lehmer_to_num(lehmer: list[int]) -> int:
    """
    Encode a Lehmer code to a number.
    """
    num = 0
    for i, n in enumerate(reversed(lehmer), 1):
        num *= i
        num += n

    return num


def num_to_lehmer(num: int, size: int) -> list[int]:
    """
    Decode a Lehmer code from a number.
    """
    lehmer = []
    for i in range(size):
        num, n = divmod(num, size - i)
        lehmer.append(n)

    return lehmer


def perm_to_lehmer(perm: list[int]) -> list[int]:
    """
    Encode a permutation to a number using Lehmer code.
    """
    max = len(perm)
    base = list(range(max))
    pos_map = {i: i for i in base}

    lehmer = []
    for i in range(max):
        d = pos_map[perm[i]] - i
        lehmer.append(d)

        if not d:
            continue
        j = pos_map[perm[i]]
        pos_map[base[i]], pos_map[base[j]] = pos_map[base[j]], pos_map[base[i]]
        base[i], base[j] = base[j], base[i]

    return lehmer


def lehmer_to_perm(lehmer: list[int]) -> list[int]:
    """
    Decode a permutation from a number using Lehmer code.
    """
    perm = list(range(len(lehmer)))
    for i in range(len(perm) - 1):
        j = lehmer[i]
        perm[i], perm[i + j] = perm[i + j], perm[i]

    return perm


def decode_perm(bs: str, max: int) -> list[int]:
    num = bs2n(bs, math.factorial(max))
    lehmer = num_to_lehmer(num, max)
    return lehmer_to_perm(lehmer)


def encode_perm(perm: list[int]) -> str:
    max = math.factorial(len(perm))
    lehmer = perm_to_lehmer(perm)
    num = lehmer_to_num(lehmer)
    return n2bs(num, max)
