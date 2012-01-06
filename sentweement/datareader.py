from sentweement import tweet

import csv
import os

class DataReader(object):
    "Performs unified data reading over a set of given tweet dumps"

    def __init__(self, filenames=None, file_changed_callback=None):
        self.__filenames = filenames or []
        self.__file_changed_callback = file_changed_callback

        for filename in self.__filenames:
            if not self.__files_exist(self.__filenames):
                # check that the files exist before starting to avoid abrupt
                # interruptions in the middle of a computation
                err = "read error: %s doesn't exist or cannot be read"
                raise IOError(err % filename)

    def get_tweets(self):
        """
        Iterates over the whole list of tweets available and returns
        a tuple like (sentiment_label, tweet instance) for each entry
        """
        for filename in self.__filenames:
            if self.__file_changed_callback:
                self.__file_changed_callback(filename)

            reader = csv.reader(open(filename, "rb"))

            for row in reader:
                sentiment, time, author, text = row
                yield (
                    int(sentiment),
                    tweet.Tweet(time, author, text),
                )

        raise StopIteration

    def __files_exist(self, filenames):
        "Check that the given list of filenames exist"
        for filename in filenames:
            if not os.path.exists(filename):
                return False
        return True

