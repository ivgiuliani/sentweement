from sentweement import settings
from sentweement.datareader import DataReader
from sentweement.learning import features

import inspect

try:
    import cPickle as pickle
except ImportError:
    import pickle


class SentimentModel(object):
    "Sentiment classifier for tweets"
    SNT_POSITIVE = 1
    SNT_NEUTRAL = 0
    SNT_NEGATIVE = -1

    def __init__(self, model=None, preprocessors=None, feature_extractors=None):
        model = model or settings.PREDICTION_MODEL
        preprocessors = preprocessors or settings.PREPROCESSORS
        feature_extractors = feature_extractors or settings.FEATURE_EXTRACTORS

        self.preprocessors = preprocessors
        self.feature_extractors = feature_extractors

        if inspect.isclass(model):
            self.model = model(self.feature_extractors)
        else:
            # preloaded model, likely from a pickle load
            self.model = model

    def save(self, filename):
        "Serializes the current model to the specified file"
        save_obj = {
            "model": self.model,
            "preprocessors": self.preprocessors,
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

        preprocessors = load_obj["preprocessors"]
        feature_extractors = load_obj["feature_extractors"]
        model = load_obj["model"]

        return SentimentModel(model, preprocessors, feature_extractors)
    
    def preprocess(self, tweet_obj):
        """
        Run the set of defined tweet preprocessors and return the
        resulting tweet.
        """
        new_tweet = tweet_obj
        for preprocessor in self.preprocessors:
            new_tweet = preprocessor(new_tweet)
        return new_tweet

    def fit(self, tweet_obj, sentiment):
        """
        Updates the model by adding the given tweet with the tagged
        sentiment label. The sentiment must be one of SNT_POSITIVE,
        SNT_NEGATIVE or SNT_NEUTRAL.
        """
        tweet_obj = self.preprocess(tweet_obj)
        self.model.fit(tweet_obj, sentiment)

    def predict(self, tweet_obj):
        """
        Returns the predicted sentiment for the given tweet's text.
        The predicted sentiment will be one of SNT_POSITIVE,
        SNT_NEGATIVE or SNT_NEUTRAL.
        """
        tweet_obj = self.preprocess(tweet_obj)
        return self.model.predict(tweet_obj)


class ModelEvaluator(object):
    def __init__(self, model, datasets):
        self.model = model
        if not isinstance(datasets, (list, tuple)):
            datasets = [datasets]
        self.datasets = datasets
        self.gold, self.test = None, None
        self.sentiment_eval_cache = {
            SentimentModel.SNT_POSITIVE: {},
            SentimentModel.SNT_NEUTRAL: {},
            SentimentModel.SNT_NEGATIVE: {},
        }

    def get_gold_comparison(self):
        """
        Creates two lists, the former containing the gold standard
        and the latter containing the predicted labels for the given datasets.

        Both lists will have the same size, and items in the i-th
        position will contain the prediction the predicted label for that
        item.
        """
        if not self.gold and not self.test:
            # cache gold/test generation as it may be called from more
            # than one place and doesn't change unless the dataset
            # changes (and thus the class is initialized again)
            reader = DataReader(self.datasets)
            self.gold, self.test = [], []
            for item in reader.get_tweets():
                sentiment, tweet = item
                self.gold.append(sentiment)
                self.test.append(self.model.predict(tweet))

        return (self.gold, self.test)

    def evaluate(self):
        eval_summary = {}
        for sentiment in [SentimentModel.SNT_POSITIVE,
                          SentimentModel.SNT_NEUTRAL,
                          SentimentModel.SNT_NEGATIVE]:
            tp, tn, fp, fn = self.evaluate_wrt_sentiment(sentiment)
            precision = self.calc_precision(tp, tn, fp, fn)
            recall = self.calc_recall(tp, tn, fp, fn)
            fmeasure = self.calc_fmeasure(precision, recall)

            eval_summary[sentiment] = {
                "true-positives": tp,
                "true-negatives": tn,
                "false-positives": fp,
                "false-negatives": fn,
                "precision": precision,
                "recall": recall,
                "f-measure": fmeasure,
            }

        return eval_summary

    def evaluate_wrt_sentiment(self, sentiment):
        """
        Returns the number of true positives, true negatives, false
        positives and false negatives for the given sentiment value.

        The sentiment must be expressed as one of SNT_POSITIVE,
        SNT_NEUTRAL and SNT_NEGATIVE (both included in SentimentModel class)
        """
        if self.sentiment_eval_cache[sentiment]:
            # cache sentiment evaluation as it doesn't change unless
            # a new dataset is given and thus a new evaluator instance
            # is created
            return (
                self.sentiment_eval_cache[sentiment]["true-positives"],
                self.sentiment_eval_cache[sentiment]["true-negatives"],
                self.sentiment_eval_cache[sentiment]["false-positives"],
                self.sentiment_eval_cache[sentiment]["false-negatives"],
            )

        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0

        gold, test = self.get_gold_comparison()

        for gold_item, test_item in zip(gold, test):
            if gold_item == sentiment and gold_item == test_item:
                true_positives += 1
            elif gold_item != sentiment and test_item != sentiment:
                true_negatives += 1
            elif gold_item != sentiment and test_item == sentiment:
                false_positives += 1
            elif gold_item == sentiment and gold_item != test_item:
                false_negatives += 1

        self.sentiment_eval_cache[sentiment] = {
            "true-positives": true_positives,
            "true-negatives": true_negatives,
            "false-positives": false_positives,
            "false-negatives": false_negatives,
        }
        return (true_positives,
                true_negatives,
                false_positives,
                false_negatives)

    def calc_precision(self, tp, tn, fp, fn):
        """
        Calculate the precision for the given values of true positives,
        true negatives, false positives and false negatives
        """
        return tp / float(tp + fp)

    def calc_recall(self, tp, tn, fp, fn):
        """
        Calculate the recall for the given values of true positives,
        true negatives, false positives and false negatives
        """
        return tp / float(tp + fn)

    def calc_fmeasure(self, precision, recall):
        "Calculate the f-measure for the given precision and recall"
        return (2 * precision * recall) / (precision + recall)
