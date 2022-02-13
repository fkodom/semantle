from __future__ import annotations
import argparse

from dataclasses import dataclass
from functools import lru_cache
import sys
from typing import Dict, Optional, Sequence, Tuple

import numpy as np

from semantle.data import load_word_vectors
from semantle.game import SemantleStepInfo, _word_similarity


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
    def __init__(self, uncertainty: float = 0.01):
        self.words = load_word_vectors()
        self.uncertainty = uncertainty

    def recommend(self, max_alternatives: int = 5) -> WordRecommendations:
        if len(self.words) == len(load_word_vectors()):
            return WordRecommendations(
                recommended="object",
                alternatives=["person", "place", "action", "adjective"],
            )

        words = tuple(self.words.keys())
        words = _get_words_closest_to_mean(words, max_words=max_alternatives + 1)
        return WordRecommendations(
            recommended=words[0], alternatives=words[1 : max_alternatives + 1],
        )

    def update(self, step_info: SemantleStepInfo) -> str:
        self.words = _get_words_with_similarity(
            reference=step_info.guess,
            similarity=step_info.similarity,
            word_strings=tuple(self.words.keys()),
            max_delta=self.uncertainty,
        )
        return self.recommend().recommended


@lru_cache(maxsize=1024)
def _get_words_with_similarity(
    reference: str,
    similarity: float,
    word_strings: Optional[Tuple[str, ...]] = None,
    max_delta: float = 0.01,
) -> Dict[str, np.ndarray]:
    all_words = load_word_vectors()
    if word_strings is None:
        word_strings = tuple(all_words.keys())

    return {
        w: all_words[w]
        for w in word_strings
        if abs(_word_similarity(w, reference) - similarity) < max_delta
    }


def _get_words_closest_to_mean(
    word_strings: Tuple[str, ...], max_words: int = sys.maxsize
) -> Tuple[str, ...]:
    all_words = load_word_vectors()
    if word_strings is None:
        word_strings = tuple(all_words.keys())

    vectors = np.array([all_words[w] for w in word_strings])
    mean = vectors.mean(axis=0, keepdims=True)
    dist = np.linalg.norm(vectors - mean, axis=1)
    indices = np.argsort(dist)[:max_words]

    return tuple(word_strings[i] for i in indices)


class AssistiveSolver(Solver):
    def __init__(self, uncertainty: float = 0.01):
        super().__init__(uncertainty=uncertainty)
        self.step = 1

    def _get_input(self, prompt: str) -> str:
        return input(prompt).lower().strip().replace(" ", "").replace(",", "")

    def _get_step_info(self) -> SemantleStepInfo:
        guess = self._get_input("Enter your guess: ")
        similarity = float(self._get_input("What was the similarity? "))
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
                try:
                    self.update(info)
                    self.step += 1
                except KeyError:
                    print("\nWORD NOT RECOGNIZED. Please try again.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--uncertainty", type=float, default=0.01)
    args = parser.parse_args()

    AssistiveSolver(uncertainty=args.uncertainty).solve()


if __name__ == "__main__":
    main()
