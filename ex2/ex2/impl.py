import functools
import itertools
import math
import string
from typing import Optional

from cipher import decrypt
from genetic_algorithm import GeneticAlgorithm, Individual, Population
from perm import decode_perm
from score import (combine_candidates_scores, combine_freq_scores, dict_score,
                   freq2_score, freq_score)


class Impl(GeneticAlgorithm):
    ALEPHBET = string.ascii_lowercase
    N = math.factorial(len(ALEPHBET))
    BITS = math.ceil(math.log2(N))

    def __init__(
        self, objective: float, solutions_threshold: float, ciphertexts: list[str]
    ) -> None:
        super().__init__()
        self.objective = objective
        self.solutions_threshold = solutions_threshold
        self.ciphertexts = ciphertexts

    @property
    def bits(self):
        return self.BITS

    def get_candidates(self, ind: Individual) -> list[str]:
        perm = decode_perm(ind, self.N)
        decrypt_with_perm = functools.partial(decrypt, self.ALEPHBET, perm)
        candidates = list(map(decrypt_with_perm, self.ciphertexts))
        return candidates

    def fitness(self, ind: Individual) -> float:
        candidates = self.get_candidates(ind)
        freq_scores = map(freq_score, candidates)
        freq2_scores = map(freq2_score, candidates)
        scores = list(
            itertools.starmap(combine_freq_scores, zip(freq_scores, freq2_scores))
        )
        score = combine_candidates_scores(scores)
        return score

    def get_oscore(self, ind: Individual):
        candidates = self.get_candidates(ind)
        scores = list(map(dict_score, candidates))
        return combine_candidates_scores(scores)

    def end_condition(self, pop: Population, gen: int) -> Optional[Individual]:
        k = len(pop) * self.solutions_threshold
        topk = sorted(pop, key=self.fitness, reverse=True)[:k]
        oscores = list(map(self.get_oscore, topk))
        best_oscore = max(oscores)
        if best_oscore < self.objective:
            return None
        solution = topk[oscores.index(best_oscore)]
        return solution
