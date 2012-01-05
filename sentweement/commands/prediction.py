from sentweement.datareader import DataReader
from sentweement.learning import SentimentModel
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

        model = SentimentModel.load(model_file)
        label = text_labels[model.predict(text)]

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
        for tweet in reader.get_tweets():
            label = text_labels[model.predict(text)]
            print(" %10s: %s" % (label, tweet["text"]))

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
        for tweet in reader.get_tweets():
            gold.append(int(tweet["sentiment"]))
            test.append(model.predict(tweet))

        print("Confusion matrix:")
        cm = nltk.ConfusionMatrix(gold, test)
        print(cm.pp(sort_by_count=True, show_percents=True))


        for sentiment, label in TEXT_LABELS.items():
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

            print("Class: %s" % label)
            print("  true-positives: %d" % true_positives)
            print("  true-negatives: %d" % true_negatives)
            print("  false-positives: %d" % false_positives)
            print("  false-negatives: %d" % false_negatives)

            precision = (true_positives / float((true_positives + false_positives)))
            recall = (true_positives / float((true_positives + false_negatives)))
            fmeasure = (2 * precision * recall) / (precision + recall)

            print("  precision: %2.5f" % precision)
            print("  recall: %2.5f" % recall)
            print("  f-measure: %2.5f\n" % fmeasure)

        return False
