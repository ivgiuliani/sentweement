from sentweement import tweet
from sentweement.datareader import DataReader
from sentweement.learning import SentimentModel
from sentweement.commands.base import BaseCommand, InvalidParameters

import sys

class CreateModelCommand(BaseCommand):
    """
    Create a new sentiment model using the given datasets as input.
    If a model with the same name already exists, it will be overwritten.
    """

    def train_over_dumps(self, filenames):
        model = SentimentModel()
        reader = DataReader(filenames)

        for tweet in reader.get_tweets():
            model.fit(tweet)

        return model

    def run(self):
        args = self.get_arguments()
        try:
            model_file = args[0]
            datasets = args[1:]
        except IndexError:
            raise InvalidParameters

        sys.stdout.write("Processing %d files... " % len(datasets))
        sys.stdout.flush()
        model = self.train_over_dumps(datasets)
        model.save(model_file)
        sys.stdout.write(" done!\n")

        return False

class UpdateModelCommand(BaseCommand):
    """
    Update a new sentiment model using the given datasets as input.
    If the model doesn't exist yet, a new one will be created.
    """

    def train_over_dumps(self, model_file, filenames):
        model = SentimentModel.load(model_file)
        reader = DataReader(filenames)

        for tweet in reader.get_tweets():
            model.fit(tweet)

        return model

    def run(self):
        args = self.get_arguments()
        try:
            model_file = args[0]
            datasets = args[1:]
        except IndexError:
            raise InvalidParameters

        sys.stdout.write("Processing %d files... " % len(datasets))
        sys.stdout.flush()
        model = self.train_over_dumps(model_file, datasets)
        model.save(model_file)
        sys.stdout.write(" done!\n")

        return False

