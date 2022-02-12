import pickle

import gensim.downloader
import numpy as np
from gensim.matutils import unitvec

from semantle.data import WORDS_PATH


print("Loading word2vec data...")
word2vec = gensim.downloader.load("word2vec-google-news-300")
words = [w for w in word2vec.index_to_key if w.lower() == w]


print("Normalizing....")
words = [w for w in word2vec.index_to_key if w.lower() == w and w.isalpha()]
vectors = np.array([unitvec(word2vec[w]) for w in words])

print("Saving to file...")
out = {k: v for k, v in zip(words, vectors)}
with open(WORDS_PATH, "wb") as f:
    pickle.dump((words, vectors), f)
