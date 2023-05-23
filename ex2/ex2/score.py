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
