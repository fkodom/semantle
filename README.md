# semantle

Fastest [Semantle](https://semantle.novalis.org/) solver this side of the Mississippi.

* Roughly 3 average turns to win
* **Measured against (part of) the `word2vec-google-news-300` vocabulary!**

NOTES:
* There are a lot of words, and I haven't bothered to test a the vast majority of them.
* The "average turns to win" benchmark is based on my rough observations.


![fast car](https://media.giphy.com/media/msboPDDziG50Anu8hz/giphy.gif)


## Install

Install directly from this repository:
```bash
pip install git+https://github.com/fkodom/semantle.git
```

## Solve

Launch the assistive solver:
```bash
solve-semantle
```

In some situations, you may want to increase the solver's uncertainty:
* To get more "realistic" looking answers -- don't immediately solve the puzzle :)
* Playing a different, third-party Semantle implementation, which may use a different trained version of Word2Vec.

It will take longer to solve the puzzle, but the solver will be more robust to discrepancies in word similarities. For example, to allow for differences of ±5 similarity score:
```bash
solve-semantle --uncertainty 5
```

## Play

Play a command line game:
```bash
play-semantle
```
**NOTE:** I believe the word bank is much larger than in the official Semantle game. You may get some obscure target words. ¯\\_(ツ)_/¯


## How It Works

[TODO]
