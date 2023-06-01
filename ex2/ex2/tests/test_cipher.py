import random
import string

from cipher import decrypt, encrypt


def test_encrypt():
    assert encrypt("ABC", [0, 1, 2], "ABC") == "ABC"
    assert encrypt("ABC", [0, 2, 1], "ABC") == "ACB"
    assert encrypt("ABC", [0, 1, 2], ".ABC,") == ".ABC,"


def test_encrypt_decrypt():
    for _ in range(100):
        n = random.randint(1, 10)
        alephbet = string.ascii_lowercase[:n]
        length = random.randint(1, 10)
        plain = "".join(random.choices(alephbet, k=length))
        perm = list(range(len(alephbet)))
        random.shuffle(perm)
        ciphertext = encrypt(alephbet, perm, plain)
        assert decrypt(alephbet, perm, ciphertext) == plain
