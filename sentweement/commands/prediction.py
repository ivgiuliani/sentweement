from sentweement.datareader import DataReader
from sentweement.learning.model import SentimentModel, ModelEvaluator
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
