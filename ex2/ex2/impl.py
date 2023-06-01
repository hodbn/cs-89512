import functools
import random
import string
from typing import Optional

from cipher import decrypt
from genetic_algorithm import (GAMetrics, GeneticAlgorithm, Individual,
                               Population)
from perm import perm_crossover_pbx, perm_crossover_pmx, perm_mutate_inversion
from score import (combine_candidates_scores, combine_freq_scores, dict_score,
                   freq2_score, freq_score)


class Impl(GeneticAlgorithm):
    ALEPHBET = string.ascii_lowercase
    N = len(ALEPHBET)

    def __init__(
        self,
        objective: float,
        solutions_threshold: float,
        ciphertexts: list[str],
    ) -> None:
        super().__init__()
        self.objective = objective
        self.solutions_threshold = solutions_threshold
        self.ciphertexts = ciphertexts
        self._metrics = GAMetrics()

    def generate_individual(self) -> Individual:
        ind = list(range(self.N))
        random.shuffle(ind)
        return tuple(ind)

    def mutate(self, ind: Individual) -> Individual:
        # inversion permutation
        i = random.randint(0, self.N - 1)
        j = (i + random.randint(1, self.N - 1)) % self.N
        return perm_mutate_inversion(ind, i, j)

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        # i = random.randint(0, self.N - 1)
        # j = (i + random.randint(1, self.N - 1)) % self.N
        # return perm_crossover_pmx(parent1, parent2, i, j)

        mask = [random.randint(0, 1) for _ in range(self.N)]
        return perm_crossover_pbx(parent1, parent2, mask)

    def get_candidates(self, ind: Individual) -> list[str]:
        perm = list(ind)
        decrypt_with_perm = functools.partial(decrypt, self.ALEPHBET, perm)
        candidates = list(map(decrypt_with_perm, self.ciphertexts))
        return candidates

    @functools.cache
    def fitness(self, ind: Individual) -> float:
        self.metrics.fitness_calls += 1
        candidates = self.get_candidates(ind)
        # freq_scores = list(map(freq_score, candidates))
        freq2_scores = list(map(freq2_score, candidates))
        scores = freq2_scores
        # freq2_scores = list(freq_scores)
        # scores = list(
        # itertools.starmap(combine_freq_scores, zip(freq_scores, freq2_scores))
        # )
        score = combine_candidates_scores(scores)
        return score

    def get_oscore(self, ind: Individual):
        candidates = self.get_candidates(ind)
        scores = list(map(dict_score, candidates))
        return combine_candidates_scores(scores)

    def end_condition(self, pop: Population, gen: int) -> Optional[Individual]:
        k = int(len(pop) * self.solutions_threshold)
        topk = sorted(pop, key=self.fitness, reverse=True)[:k]
        oscores = list(map(self.get_oscore, topk))
        best_oscore = max(oscores)
        if best_oscore < self.objective:
            return None
        solution = topk[oscores.index(best_oscore)]
        return solution

    @property
    def metrics(self) -> GAMetrics:
        return self._metrics
