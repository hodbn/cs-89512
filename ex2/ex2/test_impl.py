from cipher import decrypt, encrypt
from genetic_algorithm import GAMetrics, GAParams
from impl import Impl

DICT_FN = "dict.txt"


def test_impl_fitness():
    ximpl = Impl(0, 0, ciphertexts=[])
    key = ximpl.generate_individual()
    english = open(DICT_FN, "r").read()
    enc_english = encrypt(ximpl.ALEPHBET, list(key), english)
    impl = Impl(1.0, 0.1, ciphertexts=[enc_english])
    c = 0
    n = 100
    for i in range(n):
        mkey = key
        for _ in range(5):
            mkey = ximpl.mutate(key)
        c += impl.fitness(key) > impl.fitness(mkey)
    assert c / float(n) > 0.95


def test_impl_fitness_with_random():
    ximpl = Impl(0, 0, ciphertexts=[])
    key = ximpl.generate_individual()
    key2 = ximpl.generate_individual()
    english = open(DICT_FN, "r").read()
    enc_english = encrypt(ximpl.ALEPHBET, list(key), english)
    impl = Impl(1.0, 0.1, ciphertexts=[enc_english])
    n = 100
    for i in range(n):
        assert impl.fitness(key) > impl.fitness(key2)


def test_impl_crossover():
    ximpl = Impl(0, 0, ciphertexts=[])
    n = 100
    c = 0
    for i in range(n):
        real_key = ximpl.generate_individual()
        key1 = ximpl.generate_individual()
        key2 = ximpl.generate_individual()
        better_offspring = ximpl.crossover(real_key, key2)
        offspring = ximpl.crossover(key1, key2)
        english = open(DICT_FN, "r").read()
        enc_english = encrypt(ximpl.ALEPHBET, list(real_key), english)
        impl = Impl(1.0, 0.1, ciphertexts=[enc_english])
        c += impl.fitness(better_offspring) > impl.fitness(offspring)
    assert float(c) / 100.0 > 0.8
