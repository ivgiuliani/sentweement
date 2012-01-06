from sentweement.learning.models import base

from collections import defaultdict

import nltk

class NaiveBayesModel(base.ModelBase):
    def __init__(self, *args, **kwargs):
        base.ModelBase.__init__(self, *args, **kwargs)
        self.estimator = nltk.probability.ELEProbDist
        self.label_freqdist = nltk.probability.FreqDist()
        self.feature_freqdist = defaultdict(nltk.probability.FreqDist)
        self.feature_values = defaultdict(set)
        self.feature_names = set()

    def fit(self, tweet, sentiment):
        # the following implementation is mostly copied from
        # nltk.NaiveBayesClassifier.train, but allows for incremental
        # training over the dataset
        features = self.extract_features(tweet)
        self.label_freqdist.inc(sentiment)

        for fname, fval in features.iteritems():
            self.feature_freqdist[sentiment, fname].inc(fval)
            self.feature_values[fname].add(fval)
            self.feature_names.add(fname)

        # Assume None when a feature don't have a value given for an
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


    def predict(self, tweet):
        classifier = self.get_classifier()
        return int(classifier.classify(self.extract_features(tweet)))

