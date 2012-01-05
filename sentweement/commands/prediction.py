from sentweement.datareader import DataReader
from sentweement.learning import SentimentModel
from sentweement.commands.base import BaseCommand, InvalidParameters

import os

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
        label = predict_single(model, text)

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
            label = predict_single(model, tweet)
            print(" %10s: %s" % (label, tweet["text"]))

        return False


def predict_single(model, text):
    text_labels = {
        SentimentModel.SNT_POSITIVE: "positive",
        SentimentModel.SNT_NEUTRAL : "neutral",
        SentimentModel.SNT_NEGATIVE: "negative",
    }
    return text_labels[model.predict(text)]

