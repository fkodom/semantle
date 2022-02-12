import random
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np

from semantle.data import load_word_vectors


@dataclass
class SemantleStepInfo:
    guess: str
    similarity: float
    success: bool = False

    def __hash__(self) -> int:
        return hash(f"{self.guess}{self.similarity:.2f}{self.success}")


def _word_similarity(guess: str, target: str) -> float:
    vectors = load_word_vectors()
    v1, v2 = vectors[guess], vectors[target]
    out = np.dot(v1, v2)
    return abs(round(out.item() * 100, 2))


def _choose_random_word(seed: Optional[int] = None) -> str:
    word_bank = list(load_word_vectors().keys())
    if seed is None:
        seed = int(time.time())
    random.seed(seed)
    return random.choice(word_bank)


class Semantle:
    def __init__(self, seed: Optional[int] = None, silent: bool = False):
        self._word = _choose_random_word(seed=seed)
        self.silent = silent

        self._step = 1
        self._success = False

    def _print_step_info(self, info: SemantleStepInfo):
        print(f"Similarity: {info.similarity:.2f}")
        print("\n")
        if info.success:
            print("You win! :)")

    @property
    def done(self):
        return self._success

    def step(self, guess: str) -> SemantleStepInfo:
        self._success = guess == self._word
        similarity = _word_similarity(guess, self._word)
        info = SemantleStepInfo(
            guess=guess, similarity=similarity, success=self._success,
        )

        if not self._success:
            self._step += 1
        if not self.silent:
            self._print_step_info(info)

        return info

    def play(self):
        print("Semantle!\n")

        while not self.done:
            print(f"Step {self._step}")
            guess = input("Enter a guess: ").lower().strip()
            _ = self.step(guess)


# class StreamlitSemantle(Semantle):
#     def _render_step_info_streamlit(self, info: SemantleStepInfo):
#         import streamlit as st

#         columns = st.columns(5)
#         letters = info.letters

#         for column, letter in zip(columns, letters):
#             if letter.text == "_":
#                 color = "Gray"
#             elif letter.in_correct_position:
#                 color = "Green"
#             elif letter.in_word:
#                 color = "Yellow"
#             else:
#                 color = "Red"
#             with column:
#                 st.markdown(
#                     MARKDOWN_LETTER_TEMPLATE.format(
#                         color=color, letter=letter.text.upper()
#                     ),
#                     unsafe_allow_html=True,
#                 )

#     def _render_empty_step_streamlit(self):
#         self._render_step_info_streamlit()

#     def render_streamlit(self):
#         for step in self.history:
#             self._render_step_info_streamlit(step)

#         remaining_steps = STEPS_PER_GAME - len(self.history)
#         for _ in range(remaining_steps):
#             self._render_step_info_streamlit(info=EMPTY_STEP_INFO)


def main():
    Semantle().play()


if __name__ == "__main__":
    main()
