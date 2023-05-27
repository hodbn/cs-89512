import math
import re
from string import punctuation
import string


def calculate_score(frequencies1: dict, frequencies2: dict) -> float:
    numerator = 0.0
    sum_freq1_squared = 0.0
    sum_freq2_squared = 0.0

    # Compare frequency tables and create a score  using cosine similarity
    for letter, frequency in frequencies1.items():
        if letter in frequencies2:
            numerator += frequency * frequencies2[letter]
        sum_freq1_squared += frequency ** 2

    for letter, frequency in frequencies2.items():
        sum_freq2_squared += frequency ** 2

    denominator = math.sqrt(sum_freq1_squared) * math.sqrt(sum_freq2_squared)

    if denominator == 0.0:
        return 0.0

    score = numerator / denominator
    return score


def create_frequency_table(text: str) -> dict:
    # Create and return a frequency table for English letters in the text
    frequencies = {}
    total_letters = len(text)

    for letter in text.lower():
        if letter.isalpha():
            frequencies[letter] = frequencies.get(letter, 0) + 1

    for letter, count in frequencies.items():
        frequencies[letter] = (count / total_letters)
    import math
    import re
    from string import punctuation
    import string

    def calculate_score(frequencies1: dict, frequencies2: dict) -> float:
        numerator = 0.0
        sum_freq1_squared = 0.0
        sum_freq2_squared = 0.0

        # Compare frequency tables and create a score  using cosine similarity
        for letter, frequency in frequencies1.items():
            if letter in frequencies2:
                numerator += frequency * frequencies2[letter]
            sum_freq1_squared += frequency ** 2

        for letter, frequency in frequencies2.items():
            sum_freq2_squared += frequency ** 2

        denominator = math.sqrt(sum_freq1_squared) * math.sqrt(sum_freq2_squared)

        if denominator == 0.0:
            return 0.0

        score = numerator / denominator
        return score

    def create_frequency_table(text: str) -> dict:
        # Create and return a frequency table for English letters in the text
        frequencies = {}
        total_letters = len(text)

        for letter in text.lower():
            if letter.isalpha():
                frequencies[letter] = frequencies.get(letter, 0) + 1

        for letter, count in frequencies.items():
            frequencies[letter] = (count / total_letters)

        return frequencies
        
    def pairwise(iterable):
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)
    
    def create_pair_freq_table(text: str) -> dict:
        # Create and return a frequency table for English letters in the text
        frequencies = {}
        total_letters = len(text)

        def pairwise(iterable):
            # pairwise('ABCDEFG') --> AB BC CD DE EF FG
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)
        
        for letter in text.lower():
            if letter.isalpha():
                frequencies[letter] = frequencies.get(letter, 0) + 1

        for letter, count in frequencies.items():
            frequencies[letter] = (count / total_letters)

        return frequencies

    def read_frequencies(filename: str) -> dict:
        # Load letter frequency data from a file
        frequencies = {}

        with open(filename) as f:
            for line in f:
                m = re.match(r'(\d+\.\d+)\s+([a-zA-Z]+)', line)
                if m:
                    frequency = float(m.group(1))
                    letter = m.group(2).lower()
                    frequencies[letter] = frequency

        return frequencies

    def drop_pairs_with_spaces(frequencies: dict) -> dict:
        # Drop pairs with spaces from the frequency table
        return {pair: frequency for pair, frequency in frequencies.items() if " " not in pair}

    def freq_score(text: str) -> float:
        # Remove punctuation and spaces from the text
        text = re.sub(f"[{re.escape(punctuation)}\s]+", "", text)

        # Create a frequency table for English letters in the text
        # todo is it encoded or decoded
        encoded_frequencies = create_frequency_table(text)

        # Read real English frequency table from Letter_Freq.txt
        real_frequencies = read_frequencies("Letter_Freq.txt")

        # Compare the tables and create a score
        score = calculate_score(encoded_frequencies, real_frequencies)

        return score

    def freq2_score(text: str) -> float:
        # Remove punctuation from the text
        text = re.sub(f"[{re.escape(punctuation)}]", "", text)

        # Create a frequency table for pairs of English letters in the text
        english_frequencies = create_frequency_table(text)

        # Drop pairs with spaces
        english_frequencies = drop_pairs_with_spaces(english_frequencies)

        # Read real English frequency table from Letter2_Freq.txt
        real_frequencies = read_frequencies("Letter2_Freq.txt")

        # Compare the tables and create a score
        score = calculate_score(english_frequencies, real_frequencies)

        return score

    def dict_score(text: str) -> float:
        # Remove punctuation from the text
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Split the text into words
        words = text.split()

        # Read the dictionary words from dict.txt
        with open('dict.txt', 'r') as file:
            dictionary_words = set(line.strip() for line in file)

        # Calculate the ratio of words that exist in the dictionary
        word_count = len(words)
        valid_word_count = sum(1 for word in words if word.upper() in dictionary_words)
        ratio = valid_word_count / word_count if word_count > 0 else 0.0

        return ratio

    return frequencies

def create_pair_freq_table(text: str) -> dict:
    # Create and return a frequency table for English letters in the text
    frequencies = {}
    total_letters = len(text)

    for letter in text.lower():
        if letter.isalpha():
            frequencies[letter] = frequencies.get(letter, 0) + 1

    for letter, count in frequencies.items():
        frequencies[letter] = (count / total_letters)

    return frequencies


def read_frequencies(filename: str) -> dict:
    # Load letter frequency data from a file
    frequencies = {}

    with open(filename) as f:
        for line in f:
            m = re.match(r'(\d+\.\d+)\s+([a-zA-Z]+)', line)
            if m:
                frequency = float(m.group(1))
                letter = m.group(2).lower()
                frequencies[letter] = frequency

    return frequencies


def drop_pairs_with_spaces(frequencies: dict) -> dict:
    # Drop pairs with spaces from the frequency table
    return {pair: frequency for pair, frequency in frequencies.items() if " " not in pair}


def freq_score(text: str) -> float:
    # Remove punctuation and spaces from the text
    text = re.sub(f"[{re.escape(punctuation)}\s]+", "", text)

    # Create a frequency table for English letters in the text
    #todo is it encoded or decoded
    encoded_frequencies = create_frequency_table(text)

    # Read real English frequency table from Letter_Freq.txt
    real_frequencies = read_frequencies("Letter_Freq.txt")

    # Compare the tables and create a score
    score = calculate_score(encoded_frequencies, real_frequencies)

    return score


def freq2_score(text: str) -> float:
    # Remove punctuation from the text
    text = re.sub(f"[{re.escape(punctuation)}]", "", text)

    # Create a frequency table for pairs of English letters in the text
    english_frequencies = create_frequency_table(text)

    # Drop pairs with spaces
    english_frequencies = drop_pairs_with_spaces(english_frequencies)

    # Read real English frequency table from Letter2_Freq.txt
    real_frequencies = read_frequencies("Letter2_Freq.txt")

    # Compare the tables and create a score
    score = calculate_score(english_frequencies, real_frequencies)

    return score


def dict_score(text: str) -> float:
    # Remove punctuation from the text
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Split the text into words
    words = text.split()

    # Read the dictionary words from dict.txt
    with open('dict.txt', 'r') as file:
        dictionary_words = set(line.strip() for line in file)

    # Calculate the ratio of words that exist in the dictionary
    word_count = len(words)
    valid_word_count = sum(1 for word in words if word.upper() in dictionary_words)
    ratio = valid_word_count / word_count if word_count > 0 else 0.0

    return ratio



def freq_score(text: str) -> float:
    
    """
    go over the text
    remove punctuation including spaces
    create a frequency table for english letter
    read real english frequency table from Letter_Freq.txt
    compare the tables and create a score (???)
    """
    pass


def freq2_score(text: str) -> float:
    """
    go over the text
    remove punctuation
    create a frequency table for pairs of english letters
    drop all pairs with spaces
    read real english frequency table from Letter2_Freq.txt
    compare the tables and create a score (???)
    """
    pass


def combine_freq_scores(f1score: float, f2score: float) -> float:
    return (f1score + f2score) / 2


def combine_candidates_scores(scores: list[float]) -> float:
    return sum(scores) / len(scores)


def dict_score(text: str) -> float:
    """
    go over text
    remove punctuation
    split to words
    return the ratio of words that exist in dict.txt
    """
    pass
