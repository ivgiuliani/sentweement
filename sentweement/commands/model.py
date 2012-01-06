from sentweement import tweet
from sentweement.datareader import DataReader
from sentweement.learning.model import SentimentModel, ModelEvaluator
from sentweement.commands.base import BaseCommand, InvalidParameters

import nltk

import os
import sys

TEXT_LABELS = {
    SentimentModel.SNT_POSITIVE: "positive",
    SentimentModel.SNT_NEUTRAL : "neutral",
    SentimentModel.SNT_NEGATIVE: "negative",
}

class ModelProcessing(BaseCommand):
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.__filenames = []

    def on_file_start(self, filename):
        tot = len(self.__filenames)
        curr = self.__filenames.index(filename) + 1
        sys.stdout.write("  [%3d/%-3d] %s... " % (curr, tot, filename))
        sys.stdout.flush()

    def on_file_stop(self, filename):
        sys.stdout.write(" done!\n")

    def train_over_dumps(self, model, filenames):
        # remove duplicate file names
        filenames = sorted(list(set(filenames)))

        self.__filenames = filenames
        reader = DataReader(filenames, on_file_start_cb=self.on_file_start,
                                       on_file_stop_cb=self.on_file_stop)

        sys.stdout.write("Processing %d files...\n" % len(filenames))
        for item in reader.get_tweets():
            sentiment, tweet = item
            model.fit(tweet, sentiment)

        return model


class CreateModelCommand(ModelProcessing):
    """
    Create a new sentiment model using the given datasets as input.
    If a model with the same name already exists, it will be overwritten.
    """

    def run(self):
        args = self.get_arguments()
        try:
            model_file = args[0]
            datasets = args[1:]
        except IndexError:
            raise InvalidParameters

        model = SentimentModel()
        model = self.train_over_dumps(model, datasets)
        model.save(model_file)

        return False


class UpdateModelCommand(ModelProcessing):
    """
    Update a new sentiment model using the given datasets as input.
    If the model doesn't exist yet, a new one will be created.
    """

    def run(self):
        args = self.get_arguments()
        try:
            model_file = args[0]
            datasets = args[1:]
        except IndexError:
            raise InvalidParameters

        model = SentimentModel.load(model_file)
        model = self.train_over_dumps(model, datasets)
        model.save(model_file)

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
        evaluator = ModelEvaluator(model, filenames)

        gold, test = evaluator.get_gold_comparison()

        print("Confusion matrix:")
        cm = nltk.ConfusionMatrix(gold, test)
        print(cm.pp(sort_by_count=True, show_percents=True))

        summary = evaluator.evaluate()
        precision_sum, recall_sum, fmeasure_sum = 0, 0, 0

        print("                TP     FP     TN     FP  precision  recall  f-measure")
        rowstr = "%(label)s %(tp)6s %(tn)6s %(fp)6s %(fn)6s  %(precision)2.5f   %(recall)2.5f   %(fmeasure)2.5f"
        for sentiment, label in TEXT_LABELS.items():
            print(rowstr % {
                "label": '%s:' % label.rjust(10),
                "tp": summary[sentiment]["true-positives"],
                "fp": summary[sentiment]["false-positives"],
                "tn": summary[sentiment]["true-negatives"],
                "fn": summary[sentiment]["false-negatives"],
                "precision": summary[sentiment]["precision"],
                "recall": summary[sentiment]["recall"],
                "fmeasure": summary[sentiment]["f-measure"],
            })

            precision_sum += summary[sentiment]["precision"]
            recall_sum += summary[sentiment]["recall"]
            fmeasure_sum += summary[sentiment]["f-measure"]

        precision_avg = precision_sum / len(TEXT_LABELS)
        recall_avg = recall_sum / len(TEXT_LABELS)
        fmeasure_avg = fmeasure_sum / len(TEXT_LABELS)

        print(rowstr % {
            "label": "average:".rjust(11),
            "tp": "", "fp": "", "tn": "", "fn": "",
            "precision": precision_avg,
            "recall": recall_avg,
            "fmeasure": fmeasure_avg,
        })

        return False
