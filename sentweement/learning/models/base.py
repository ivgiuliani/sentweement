class ModelBase(object):
    def __init__(self, feature_extractors):
        if not isinstance(feature_extractors, (list, tuple)):
            feature_extractors = [ feature_extractors ]
        self.feature_extractors = feature_extractors

    def extract_features(self, tweet):
        features = {}
        for feature_extractor in self.feature_extractors:
            features.update(feature_extractor(tweet))
        return features

    def fit(self, tweet, sentiment):
        raise NotImplementedError

    def predict(self, tweet):
        raise NotImplementedError
