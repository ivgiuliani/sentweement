import nltk

def extract_unigrams(tweet):
    "Extracts unigrams from the given tweet"
    text = (tweet.fix()
                 .remove_urls()
                 .remove_usernames()
                 .remove_retweets()
                 .text
                 .lower())

    tokens = nltk.wordpunct_tokenize(text)
    features = {}

    for token in tokens:
        features["has(%s)" % token] = True

    return features

def extract_bigrams(tweet):
    "Extracts bigrams from the given tweet"
    text = (tweet.fix()
                 .remove_urls()
                 .remove_usernames()
                 .remove_retweets()
                 .text
                 .lower())

    tokens = nltk.wordpunct_tokenize(text)
    features = {}

    for token1, token2 in zip(tokens, tokens[1:]):
        features["has(%s %s)" % (token1, token2)] = True

    return features
