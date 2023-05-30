import random
from string import ascii_lowercase

from score import freq2_score, freq_score

DICT_FN = "dict.txt"


def test_freq_score():
    english = open(DICT_FN, "r").read()
    gibberish = "".join(random.choice(ascii_lowercase) for _ in english)
    english_score = freq_score(english)
    gibberish_score = freq_score(gibberish)
    assert english_score > gibberish_score


def test_freq2_score():
    english = open(DICT_FN, "r").read()
    gibberish = "".join(random.choice(ascii_lowercase) for _ in english)
    english_score = freq2_score(english)
    gibberish_score = freq2_score(gibberish)
    assert english_score > gibberish_score
