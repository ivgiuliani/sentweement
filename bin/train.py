#!/usr/bin/env python
import sys

from sentweement import tweet
from sentweement.datareader import DataReader
from sentweement.learning import SentimentModel

def train_over_dumps(filenames):
    model = SentimentModel()
    reader = DataReader(filenames)

    for tweet in reader.get_tweets():
        model.fit(tweet)

    return model

def usage(name):
    print("Usage: %s <output model> <input dump 1> ... <input dump N>" % name)

def main(args):
    try:
        model_output = args[1]
        dumps = [dump for dump in args[2:]]
    except (IndexError, KeyError):
        usage(args[0])
        return
    
    if not dumps:
        usage(args[0])
        return

    model = train_over_dumps(dumps)
    model.save(model_output)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
