from sentweement.datareader import DataReader
from sentweement.learning.model import SentimentModel
from sentweement.tweet import DummyTweet
from sentweement.commands.base import BaseCommand, InvalidParameters

import nltk

import os

TEXT_LABELS = {
    SentimentModel.SNT_POSITIVE: "positive",
    SentimentModel.SNT_NEUTRAL : "neutral",
    SentimentModel.SNT_NEGATIVE: "negative",
}

class PredictSingleCommand(BaseCommand):
    """
    Predict the sentiment outcome for a single sentence over an
    existing sentiment model.
    """

    def run(self):
        args = self.get_arguments()
        model_file = args[0]
        text = ' '.join(args[1:])

        if not os.path.exists(model_file):
            print("ERROR: model file '%s' doesn't exist" % model_file)
            return True

        dummytweet = DummyTweet(text)
        model = SentimentModel.load(model_file)
        label = TEXT_LABELS[model.predict(dummytweet)]

        print("Prediction:")
        print(" %10s: %s" % (label, text))

        return False


class PredictBatchCommand(BaseCommand):
    """
    Predict the sentiment outcome over the input dataset for the given
    entiment model.
    """
    def run(self):
        args = self.get_arguments()
        model_file = args[0]
        filenames = args[1:]

        if not os.path.exists(model_file):
            print("ERROR: model file '%s' doesn't exist" % model_file)
            return True

        model = SentimentModel.load(model_file)
        reader = DataReader(filenames)

        print("Prediction:")
        for item in reader.get_tweets():
            sentiment, tweet = item
            label = TEXT_LABELS[model.predict(tweet)]
            print(" %10s: %s" % (label, tweet.text))

        return False


class EvaluateCommand(BaseCommand):
    """
    Evaluate the model over a given dataset with respect to a gold
    standard.
    """
    def run(self):
        args = self.get_arguments()
        model_file = args[0]
        filenames = args[1:]

        if not os.path.exists(model_file):
            print("ERROR: model file '%s' doesn't exist" % model_file)
            return True

        model = SentimentModel.load(model_file)
        reader = DataReader(filenames)

        gold, test = [], []
        for item in reader.get_tweets():
            sentiment, tweet = item
            gold.append(sentiment)
            test.append(model.predict(tweet))

        print("Confusion matrix:")
        cm = nltk.ConfusionMatrix(gold, test)
        print(cm.pp(sort_by_count=True, show_percents=True))

        summary = {}
        for sentiment, label in TEXT_LABELS.items():
            summary[label] = {}
            true_positives = 0
            true_negatives = 0
            false_positives = 0
            false_negatives = 0

            for gold_item, test_item in zip(gold, test):
                if gold_item == sentiment and gold_item == test_item:
                    true_positives += 1
                elif gold_item != sentiment and test_item != sentiment:
                    true_negatives += 1
                elif gold_item != sentiment and test_item == sentiment:
                    false_positives += 1
                elif gold_item == sentiment and gold_item != test_item:
                    false_negatives += 1

            precision = (true_positives / float((true_positives + false_positives)))
            recall = (true_positives / float((true_positives + false_negatives)))
            fmeasure = (2 * precision * recall) / (precision + recall)

            summary[label]["true-positives"] = true_positives
            summary[label]["true-negatives"] = true_negatives
            summary[label]["false-positives"] = false_positives
            summary[label]["false-negatives"] = false_negatives
            summary[label]["precision"] = precision
            summary[label]["recall"] = recall
            summary[label]["f-measure"] = fmeasure

        labels = TEXT_LABELS.values()
        print("                TP     FP     TN     FP  precision  recall  f-measure")
        rowstr = "%(label)s %(tp)6s %(tn)6s %(fp)6s %(fn)6s  %(precision)2.5f   %(recall)2.5f   %(fmeasure)2.5f"
        for label in labels:
            print(rowstr % {
                "label": '%s:' % label.rjust(10),
                "tp": summary[label]["true-positives"],
                "fp": summary[label]["false-positives"],
                "tn": summary[label]["true-negatives"],
                "fn": summary[label]["false-negatives"],
                "precision": summary[label]["precision"],
                "recall": summary[label]["recall"],
                "fmeasure": summary[label]["f-measure"],
            })

        avg_precision = sum([summary[label]["precision"] for label in labels]) / len(labels)
        avg_recall = sum([summary[label]["recall"] for label in labels]) / len(labels)
        avg_fmeasure = sum([summary[label]["f-measure"] for label in labels]) / len(labels)

        print(rowstr % {
            "label": "average:".rjust(11),
            "tp": "", "fp": "", "tn": "", "fn": "",
            "precision": avg_precision,
            "recall": avg_recall,
            "fmeasure": avg_fmeasure,
        })

        return False
