from sentweement import tweet
from sentweement.learning.models import bayes
from sentweement.learning import features

import inspect

try:
    import cPickle as pickle
except ImportError:
    import pickle

class SentimentModel(object):
    "Sentiment classifier for tweets"
    SNT_POSITIVE = 1
    SNT_NEUTRAL  = 0
    SNT_NEGATIVE = -1

    def __init__(self, model=bayes.NaiveBayesModel, feature_extractors=[]):
        # TODO: allow external list of feature extractors
        self.feature_extractors = [ features.extract_unigrams,
                                    features.extract_bigrams ]

        if inspect.isclass(model):
            self.model = model(self.feature_extractors)
        else:
            # preloaded model, likely from a pickle load
            self.model = model

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

        feature_extractors = load_obj["feature_extractors"]
        model = load_obj["model"]

        return SentimentModel(model, feature_extractors)

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
        return self.model.predict(tweet_obj)
