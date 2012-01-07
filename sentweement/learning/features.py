import nltk

ALPHABET = "abcdefghijklmnopqrstuwxyz"


def extract_unigrams(tweet):
    "Extracts unigrams from the given tweet"
    text = tweet.text

    tokens = nltk.wordpunct_tokenize(text)
    tokens = [token for token in tokens if token not in ALPHABET]
    features = {}

    for token in tokens:
        features["has(%s)" % token] = True

    return features


def extract_bigrams(tweet):
    "Extracts bigrams from the given tweet"
    text = tweet.text

    tokens = nltk.wordpunct_tokenize(text)
    tokens = [token for token in tokens if token not in ALPHABET]
    features = {}

    for token1, token2 in zip(tokens, tokens[1:]):
        features["has(%s %s)" % (token1, token2)] = True

    return features
