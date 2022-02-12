import os
import pickle
from functools import lru_cache
from typing import Dict

import gdown
import numpy as np

WORDS_URL = (
    "https://drive.google.com/uc?id=1hJVHw0gdh9itJBtAn8ZPJGxP2jRe332k"
    # https://drive.google.com/file/d/1hJVHw0gdh9itJBtAn8ZPJGxP2jRe332k/view?usp=sharing
)
WORDS_PATH = os.path.join(
    os.path.dirname(__file__), os.path.pardir, "data", "words.pkl"
)


def _download_words():
    os.makedirs(os.path.dirname(WORDS_PATH), exist_ok=True)
    gdown.download(WORDS_URL, WORDS_PATH)


@lru_cache()
def load_word_vectors() -> Dict[str, np.ndarray]:
    if not os.path.exists(WORDS_PATH):
        _download_words()

    with open(WORDS_PATH, "rb") as f:
        words, vectors = pickle.load(f)
    return {w.lower(): v for w, v in zip(words, vectors.astype(np.float64))}
