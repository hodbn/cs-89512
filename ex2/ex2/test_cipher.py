import random
import string

from cipher import decrypt, encrypt


def test_encrypt():
    assert encrypt("ABC", "ABC", [0, 1, 2]) == "ABC"
    assert encrypt("ABC", "ABC", [0, 2, 1]) == "ACB"
    assert encrypt("ABC", ".ABC,", [0, 1, 2]) == ".ABC,"


def test_encrypt_decrypt():
    for _ in range(100):
        n = random.randint(1, 10)
        alephbet = string.ascii_lowercase[:n]
        length = random.randint(1, 10)
        plain = "".join(random.choices(alephbet, k=length))
        perm = list(range(len(alephbet)))
        random.shuffle(perm)
        ciphertext = encrypt(alephbet, plain, perm)
        assert decrypt(alephbet, ciphertext, perm) == plain
