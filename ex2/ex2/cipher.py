import operator


def perm_to_trans(alephbet: str, perm: list[int]):
    permuted = "".join(alephbet[i] for i in perm)
    return str.maketrans(alephbet, permuted)


def encrypt(alephbet: str, plain: str, perm: list[int]):
    trans = perm_to_trans(alephbet, perm)
    return plain.translate(trans)


def decrypt(alephbet: str, ciphertext: str, perm: list[int]):
    tmp = [(perm[i], i) for i in perm]
    perm_rev = list(map(operator.itemgetter(1), sorted(tmp)))
    return encrypt(alephbet, ciphertext, perm_rev)
