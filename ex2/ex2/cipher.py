import operator


def perm_to_trans(alephbet: str, perm: list[int]):
    permuted = "".join(alephbet[i] for i in perm)
    return str.maketrans(alephbet, permuted)


def encrypt(alephbet: str, perm: list[int], plain: str):
    trans = perm_to_trans(alephbet, perm)
    return plain.translate(trans)


def decrypt(alephbet: str, perm: list[int], ciphertext: str):
    tmp = [(perm[i], i) for i in perm]
    perm_rev = list(map(operator.itemgetter(1), sorted(tmp)))
    return encrypt(alephbet, perm_rev, ciphertext)
