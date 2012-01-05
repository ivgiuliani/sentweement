from sentweement import tweet
from sentweement.datareader import DataReader
from sentweement.learning import SentimentModel
from sentweement.commands.base import BaseCommand, InvalidParameters

import sys

class CreateModelCommand(BaseCommand):
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
        self.train_over_dumps(datasets)
        sys.stdout.write(" done!\n")

        return False

class UpdateModelCommand(BaseCommand):
    pass

