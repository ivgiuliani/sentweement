from sentweement import tweet
from sentweement.datareader import DataReader
from sentweement.learning.model import SentimentModel
from sentweement.commands.base import BaseCommand, InvalidParameters

import sys

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
