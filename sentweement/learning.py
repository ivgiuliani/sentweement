from sentweement import tweet

from collections import defaultdict

import nltk
try:
    import cPickle as pickle
except ImportError:
    import pickle

class SentimentModel(object):
    "Sentiment classifier for tweets"
    TWITTER_USERNAME_PREFIX = "@"
    TWITTER_HASHTAG_PREFIX = "#"
    TWITTER_CHARS = "@#"

    SNT_POSITIVE = 1
    SNT_NEUTRAL  = 0
    SNT_NEGATIVE = -1

    def __init__(self, estimator=nltk.probability.ELEProbDist):
        self.estimator = estimator
        self.label_freqdist = nltk.probability.FreqDist()
        self.feature_freqdist = defaultdict(nltk.probability.FreqDist)
        self.feature_values = defaultdict(set)
        self.feature_names = set()

    def save(self, filename):
        "Serializes the current model to the specified file"
        fd = open(filename, "wb")
        pickle.dump(self, fd)
        fd.close()

    @staticmethod
    def load(filename):
        "Load an existing model from the given filename"
        fd = open(filename, "rb")
        model = pickle.load(fd)
        fd.close()
        return model

    def tokenize(self, text):
        """Splits a sentence into tokens

        This also takes in account twitter particular features,
        as @usernames and #hashtags by joining adjacent tokens
        when it makes sense so that for example '@' and 'username' are
        always a single token
        """

        nltk_tokens = nltk.wordpunct_tokenize(text)
        tokens = []
        for tok1, tok2 in zip(nltk_tokens, nltk_tokens[1:]):
            if tok1 in self.TWITTER_CHARS:
                tokens.append(tok1 + tok2)
            elif tok2 not in self.TWITTER_CHARS:
                tokens.append(tok2) 

        if len(nltk_tokens) > 0 and nltk_tokens[0] not in self.TWITTER_CHARS:
            tokens = [ nltk_tokens[0] ] + tokens
        return tokens

    def extract_features(self, tweet_obj):
        "Extracts a set of features from the given tweet"
        text = tweet.fix(tweet_obj["text"])
        text = tweet.remove_urls(text)

        tokens = self.tokenize(text)
        features = {}

        for token in tokens:
            if len(token) == 1:
                # skip punctuation marks or single letters as they
                # don't contribute much
                continue

            token = token.lower()
            if token.startswith(tuple(self.TWITTER_CHARS)):
                # skip @usernames and #hashtags
                continue
            features["has(%s)" % token] = True

        for letter in "abcdefghijklmnopqrstuwxyz":
            features["high_char_ratio(%s)" % letter] = text.lower().count(letter) / float(len(text)) > 0.1

        return features

    def fit(self, tweet_obj):
        """
        Updates the model by adding the given tweet with the tagged
        sentiment label. The sentiment must be one of SNT_POSITIVE,
        SNT_NEGATIVE or SNT_NEUTRAL.
        """
        sentiment = int(tweet_obj["sentiment"])

        # the following implementation is mostly copied from
        # nltk.NaiveBayesClassifier.train, but allows for incremental
        # training over the dataset
        features = self.extract_features(tweet_obj)
        self.label_freqdist.inc(sentiment)

        for fname, fval in features.iteritems():
            self.feature_freqdist[sentiment, fname].inc(fval)
            self.feature_values[fname].add(fval)
            self.feature_names.add(fname)

        # Assume None when a feature didn't have a value given for an
        # instance (wrt the whole feature set)
        for label in self.label_freqdist:
            num_samples = self.label_freqdist[label]
            for fname in self.feature_names:
                count = self.feature_freqdist[label, fname].N()
                self.feature_freqdist[label, fname].inc(None, num_samples-count)
                self.feature_values[fname].add(None)

    def get_classifier(self):
        label_probdist = self.estimator(self.label_freqdist)
        feature_probdist = {}
        for ((label, fname), freqdist) in self.feature_freqdist.iteritems():
            probdist = self.estimator(freqdist, bins=len(self.feature_values[fname]))
            feature_probdist[label,fname] = probdist

        return nltk.NaiveBayesClassifier(label_probdist, feature_probdist)

    def predict(self, tweet_obj):
        """
        Returns the predicted sentiment for the given tweet's text.
        The predicted sentiment will be one of SNT_POSITIVE,
        SNT_NEGATIVE or SNT_NEUTRAL.
        """
        if isinstance(tweet_obj, (str, unicode)):
            # allow direct text passing for easier testing
            tweet_obj = { "text": tweet_obj }

        return self.get_classifier().classify(self.extract_features(text))
