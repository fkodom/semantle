from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Optional, Sequence, Tuple

import numpy as np

from semantle.data import load_word_vectors
from semantle.game import SemantleStepInfo


@dataclass
class WordRecommendations:
    recommended: str
    alternatives: Sequence[str]

    def __str__(self) -> str:
        return (
            f"Recommended: {self.recommended}\n"
            f"Alternatives: [" + ", ".join(self.alternatives) + "]"
        )


class Solver:
    def __init__(self):
        self.words = load_word_vectors()

    def recommend(self, max_alternatives: int = 5) -> WordRecommendations:
        if len(self.words) == len(load_word_vectors()):
            return WordRecommendations(
                recommended="slate", alternatives=["blast", "tapir", "ralph"],
            )

        words = tuple(self.words.keys())
        return WordRecommendations(
            recommended=words[0], alternatives=words[1 : max_alternatives + 1],
        )

    def update(self, step_info: SemantleStepInfo) -> str:
        self.words = _get_words_with_similarity(
            reference=step_info.guess,
            similarity=step_info.similarity,
            word_strings=tuple(self.words.keys()),
        )
        return self.recommend().recommended


def _word_similarity(guess: str, target: str) -> float:
    vectors = load_word_vectors()
    v1, v2 = vectors[guess], vectors[target]
    out = np.dot(v1, v2)
    return out.item() * 100


@lru_cache(maxsize=1024)
def _get_words_with_similarity(
    reference: str,
    similarity: float,
    word_strings: Optional[Tuple[str, ...]] = None,
    max_delta: float = 1.0,
) -> Dict[str, np.ndarray]:
    all_words = load_word_vectors()
    if word_strings is None:
        word_strings = tuple(all_words.keys())

    return {
        w: all_words[w]
        for w in word_strings
        if abs(_word_similarity(w, reference) - similarity) < max_delta
    }


class AssistiveSolver(Solver):
    def __init__(self):
        super().__init__()
        self.step = 1

    def _get_input(self, prompt: str) -> str:
        return input(prompt).lower().strip().replace(" ", "").replace(",", "")

    def _get_step_info(self) -> SemantleStepInfo:
        guess = self._get_input("Enter your guess: ")
        similarity = float(self._get_input("What was the similarity?: "))
        success = similarity > 99.99
        return SemantleStepInfo(guess=guess, similarity=similarity, success=success)

    def solve(self):
        print("Semantle Solver!")

        while True:
            print(f"\nStep {self.step}")
            print("-" * 16)
            print(f"{len(self.words)} solutions remaining")
            recommendations = self.recommend()
            print(recommendations)
            print("-" * 16)
            info = self._get_step_info()
            if info.success:
                print("You win! :)")
                break
            else:
                self.update(info)
                self.step += 1


def main():
    AssistiveSolver().solve()


if __name__ == "__main__":
    main()
