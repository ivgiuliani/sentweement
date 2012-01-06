from sentweement import tweet

import csv
import sys
import os


class DataReader(object):
    "Performs unified data reading over a set of given tweet dumps"

    def __init__(self, filenames=None, on_file_start_cb=None,
                                       on_file_stop_cb=None):
        self.__filenames = filenames or []
        self.__on_file_start_cb = on_file_start_cb
        self.__on_file_stop_cb = on_file_stop_cb

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
            if self.__on_file_start_cb:
                self.__on_file_start_cb(filename)

            reader = csv.reader(open(filename, "rb"))
            for lineno, row in enumerate(reader):
                sentiment, tweet_id, author, text = row
                try:
                    ret = (int(sentiment), tweet.Tweet(tweet_id, author, text))
                except ValueError:
                    err_str = "WARNING: malformed line no. %d"
                    sys.stderr.write(err_str % (lineno + 1))
                    continue
                yield ret

            if self.__on_file_stop_cb:
                self.__on_file_stop_cb(filename)

        raise StopIteration

    def __files_exist(self, filenames):
        "Check that the given list of filenames exist"
        for filename in filenames:
            if not os.path.exists(filename):
                return False
        return True
