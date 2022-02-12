import os
from concurrent.futures import ProcessPoolExecutor
import random
from typing import Dict, Iterator, Optional

from tqdm import tqdm

from semantle.data import load_word_vectors
from semantle.game import Semantle
from semantle.solver import Solver

BENCHMARKS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "benchmarks.jsonl"
)


def solve_game(word: str, first_guess: str) -> int:
    game = Semantle(silent=True)
    game._word = word
    solver = Solver()
    guess = first_guess

    while guess != game._word:
        info = game.step(guess)
        guess = solver.update(info)

    return game._step


def test_solver_with_first_guess(first_guess: str, num_games: int = 25) -> Dict:
    words = list(load_word_vectors().keys())
    random.shuffle(words)
    words = words[:num_games]
    results = [solve_game(w, first_guess) for w in tqdm(words)]

    return {
        "first_guess": first_guess,
        "average_turns": sum(r for r in results) / len(results),
        "max_turns": max(r for r in results),
    }


def test_first_guesses(
    start_idx: int = 0, num_workers: Optional[int] = None,
) -> Iterator[Dict]:
    words = sorted(load_word_vectors().keys())[start_idx:]
    if num_workers is None or num_workers > 1:
        pool = ProcessPoolExecutor(max_workers=num_workers)
        results = pool.map(test_solver_with_first_guess, words)
    else:
        results = map(test_solver_with_first_guess, words)

    return (r for r in tqdm(results, total=len(words)))


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--first-guess", type=str, default=None)
    parser.add_argument("--start-idx", type=int, default=0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--num-workers", type=int, default=None)
    args = parser.parse_args()

    if args.first_guess is not None:
        result = test_solver_with_first_guess(args.first_guess)
        print(json.dumps(result, indent=2))
    else:
        results = test_first_guesses(
            start_idx=args.start_idx, num_workers=args.num_workers
        )
        os.makedirs(os.path.dirname(BENCHMARKS_PATH), exist_ok=True)
        mode = "w" if args.overwrite else "a"

        with open(BENCHMARKS_PATH, mode) as f:
            for i, result in enumerate(results):
                line = json.dumps(result)
                f.write(f"{line}\n")
