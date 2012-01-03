import csv
import os

class DataReader(object):
    "Performs unified data reading over a set of given tweet dumps"

    def __init__(self, filenames=None):
        self._filenames = filenames or []

        if not self._files_exist(self._filenames):
            # check that the files exist before starting to avoid abrupt
            # interruptions in the middle of a computation
            err = "read error: %s doesn't exist or cannot be read"
            raise IOError(err % filename)

    def get_tweets(self):
        "Iterates over the whole list of tweets available"
        for filename in self._filenames:
            reader = csv.reader(open(filename, "rb"))

            for row in reader:
                sentiment, time, author, text = row
                yield {
                    "sentiment": sentiment,
                    "time": time,
                    "author": author,
                    "text": text,
                }

        raise StopIteration

    def _files_exist(self, filenames):
        "Check that the given list of filenames exist"
        for filename in filenames:
            if not os.path.exists(filename):
                return False
        return True

