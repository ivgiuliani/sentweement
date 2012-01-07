from sentweement import auth
from sentweement import settings
from sentweement import stream
from sentweement import language
from sentweement.tweet import Tweet
from sentweement.learning.model import SentimentModel
from sentweement.commands.base import BaseCommand
from sentweement.commands.base import get_commands
from sentweement.commands.base import InvalidParameters

import csv

TEXT_LABELS = {
    SentimentModel.SNT_POSITIVE: "positive",
    SentimentModel.SNT_NEUTRAL: "neutral",
    SentimentModel.SNT_NEGATIVE: "negative",
}


class SampleDumper(object):
    def __init__(self, language, count, output):
        self.language = language
        self.count = count
        self.counter = 0

        self._output = csv.writer(open(output, "w"))

    def cb_search(self, status):
        tweet_id = status.id_str
        author = status.author.screen_name
        text = status.text

        author = author.encode("utf-8")
        text = text.encode("utf-8")

        lang = language.get_language(text)
        if lang[1] == self.language:
            self._output.writerow([0, tweet_id, author, text])
            self.counter += 1

        if self.counter < self.count:
            return True
        return False


class FilterSearch(object):
    def cb_search(self, status, filter_language):
        author = status.author.screen_name
        text = status.text

        author = author.encode("utf-8")
        text = text.encode("utf-8")

        lang = language.get_language(text)
        if lang[1] == filter_language:
            print "%s: %s" % (author.rjust(21), text)
        return True


class SaveSampleCommand(BaseCommand):
    """
    Save an unlabeled twitter dataset sample. The numer of saved tweets
    will be equal to the specified tweet count, and only tweets whose
    language matches the language code (ex: 'en' or 'it') will be saved.
    """

    def run(self):
        arguments = self.get_arguments()
        try:
            language = arguments[0]
            count = int(arguments[1])
            output = arguments[2]
        except (IndexError, ValueError):
            raise InvalidParameters

        dumper = SampleDumper(language, count, output)
        s = stream.SearchListener(auth.auth(), "", dumper.cb_search)

        try:
            s.run()
        except KeyboardInterrupt:
            s.close()

        return False


class SearchTweetsCommand(BaseCommand):
    """
    Show the real-time stream of tweets that match the given keywords
    for the specified language code (i.e.: 'en' or 'it').
    """

    def run(self):
        arguments = self.get_arguments()
        try:
            language = arguments[0]
        except (IndexError, ValueError):
            raise InvalidParameters

        search_terms = arguments[1:]
        if not search_terms:
            raise InvalidParameters

        tfilter = FilterSearch()
        s = stream.SearchListener(auth.auth(),
                                  search_terms,
                                  tfilter.cb_search,
                                  cb_args=(language, ))

        try:
            s.run()
        except KeyboardInterrupt:
            s.close()

        return False


class RealtimePredictionCommand(BaseCommand):
    """
    Show the real-time stream of tweets that match the given keywords
    for the specified language code (i.e.: 'en' or 'it') and automatically
    tries to predict the sentiment outcome for each of them using the
    pre-trained model in input..
    """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.model = None

    def run(self):
        arguments = self.get_arguments()
        try:
            model_file = arguments[0]
            language = arguments[1]
        except (IndexError, ValueError):
            raise InvalidParameters

        search_terms = arguments[2:]
        if not search_terms:
            raise InvalidParameters

        self.model = SentimentModel.load(model_file)
        s = stream.SearchListener(auth.auth(),
                                  search_terms,
                                  self.cb_search,
                                  cb_args=(language, ))

        try:
            s.run()
        except KeyboardInterrupt:
            s.close()

        return False

    def cb_search(self, status, filter_language):
        author = status.author.screen_name
        text = status.text

        author = author.encode("utf-8")
        text = text.encode("utf-8")

        lang = language.get_language(text)
        if lang[1] == filter_language:
            tweet = Tweet(status.id_str, author, text)

            sentiment = self.model.predict(tweet)
            sentiment = ("[%s] " % TEXT_LABELS[sentiment]).rjust(11)
            print "%s %s: %s" % (sentiment, author.rjust(15), text)
        return True
