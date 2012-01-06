from sentweement import tweet
from sentweement.learning.models import bayes

import inspect

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

    def __init__(self, model=bayes.NaiveBayesModel, feature_extractors=[]):
        if inspect.isclass(model):
            self.model = model(self.extract_features)
        else:
            # preloaded model, likely from a pickle load
            self.model = model
        # TODO: allow external list of feature extractors
        self.feature_extractors = [ self.extract_features ]

    def save(self, filename):
        "Serializes the current model to the specified file"
        save_obj = {
            "model": self.model,
            "feature_extractors": self.feature_extractors,
        }
        fd = open(filename, "wb")
        pickle.dump(save_obj, fd)
        fd.close()

    @staticmethod
    def load(filename):
        "Load an existing model from the given filename"
        fd = open(filename, "rb")
        load_obj = pickle.load(fd)
        fd.close()
        self.feature_extractors = load_obj["feature_extractors"]
        self.model = load_obj["model"]
        return SentimentModel(model)

    def extract_features(self, tweet_obj):
        "Extracts a set of features from the given tweet"
        text = (tweet_obj.fix()
                         .remove_urls()
                         .remove_usernames()
                         .remove_retweets()
                         .text)

        tokens = nltk.wordpunct_tokenize(text)
        features = {}

        for token1, token2 in zip(tokens, tokens[1:]):
            features["has(%s)" % token1] = True
            features["has(%s)" % token2] = True
            features["has(%s %s)" % (token1, token2)] = True

        return features

    def fit(self, tweet_obj, sentiment):
        """
        Updates the model by adding the given tweet with the tagged
        sentiment label. The sentiment must be one of SNT_POSITIVE,
        SNT_NEGATIVE or SNT_NEUTRAL.
        """
        self.model.fit(tweet_obj, sentiment)

    def predict(self, tweet_obj):
        """
        Returns the predicted sentiment for the given tweet's text.
        The predicted sentiment will be one of SNT_POSITIVE,
        SNT_NEGATIVE or SNT_NEUTRAL.
        """
        return self.predict(tweet_obj)
