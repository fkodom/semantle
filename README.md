# semantle

Fastest [Semantle](https://semantle.novalis.org/) solver this side of the Mississippi.

* Roughly 3 average turns to win
* **Measured against (part of) the `word2vec-google-news-300` vocabulary**

NOTES:
* There are a lot of English words, and it would take a long time to exhaustively test against all of them.
* For that reason, I haven't bothered to test the vast majority of words.
* The "average turns to win" benchmark is based on a handful of my empirical observations.


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

Semantle uses Word2Vec [[Wiki](https://en.wikipedia.org/wiki/Word2vec)][[Docs](https://radimrehurek.com/gensim/models/word2vec.html)] to compute the similarity between the target word and each guess. How it works, at a very high level:
* Using a large corpus of text (Google News), create a vector embedding for each possible word.
* Note that words with similar semantic meanings are close together in the embedding space.
* Numerically compute the semantic similarity of words from the [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) of their embedding vectors.

Cosine similarity scores are **commutative**, which means that:
```python
similarity(word1, word2) == similarity(word2, word1)
```
The solver uses that to efficiently search through all possible words. **If a candidate word doesn't give the same similarity score, it can't possibly be the answer.** 

1. Takes the user's guess, and the reported similarity from Semantle
2. Finds all remaining words that have (approximately) the same similarity to the user's guess. (Needs to be approximate to allow for rounding and floating point errors.)
3. Recommends one of those words, and then repeats from step (1) if the puzzle isn't solved yet.

With each guess, the solver eliminates a **tremendous** amount of possible solutions. There are roughly 150,000 possible answers (unique English words made up of only lowercase letters), but the solver wins in about 3 turns on average. :)  

