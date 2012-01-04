#-!- encoding: utf-8
import csv
import os
import shutil
import tempfile
import unittest

from sentweement import datareader
from sentweement import learning
from sentweement import tweet

class TestTweets(unittest.TestCase):
    def testUsernameRemoval(self):
        tests = (
            # full text, expected text
            ("@test: test!", "test!"),
            ("@u1: @u2!", ""),
            ("@username: loved what @username said", "loved what said"),
            ("no usernames", "no usernames"),
        )

        for test, expected_value in tests:
            self.assertEqual(tweet.remove_usernames(test), expected_value)

    def testRetweetRemoval(self):
        tests = (
            # full text, expected text
            ("RT @username: ehi", "@username: ehi"),
            ("RT: test", "test"),
        )

        for test, expected_value in tests:
            self.assertEqual(tweet.remove_retweets(test), expected_value)

    def testUrlRemoval(self):
        tests = (
            # full text, expected text
            ("http://google.com", ""),
            ("besides http://google.com", "besides"),
            ("abcd http://www.google.com efgh", "abcd efgh"),
            ("1111 www.google.com 2222", "1111 2222"),
        )

        for test, expected_value in tests:
            self.assertEqual(tweet.remove_urls(test), expected_value)

    def testTweetFix(self):
        tests = (
            # full text, expected text
            ("» Hello «", ">> Hello <<"),
            ("RT: test &gt; test2", "RT: test > test2"),
            ("“hello world“", "\"hello world\""),
        )

        for test, expected_value in tests:
            self.assertEqual(tweet.fix(test), expected_value)


class TestReader(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        f1 = os.path.join(self.tmpdir, "data1")
        f2 = os.path.join(self.tmpdir, "data2")
        f3 = os.path.join(self.tmpdir, "data3")
        self.filenames = [ f1, f2, f3 ]

        writer = csv.writer(open(f1, "w"))
        writer.writerow([0, "1234567", "author1", "text1"])
        writer.writerow([0, "1234567", "author2", "text2"])
        writer.writerow([0, "1234567", "author3", "text3"])

        writer = csv.writer(open(f2, "w"))
        writer.writerow([0, "1234567", "author4", "text4"])
        writer.writerow([0, "1234567", "author5", "text5"])
        writer.writerow([0, "1234567", "author6", "text6"])

        writer = csv.writer(open(f3, "w"))
        writer.writerow([0, "1234567", "author7", "text7"])
        writer.writerow([0, "1234567", "author8", "text8"])
        writer.writerow([0, "1234567", "author9", "text9"])

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def testNoFailOnEmpty(self):
        reader = datareader.DataReader([])

    def testDataIteration(self):
        reader = datareader.DataReader(self.filenames)
        authors, text = [], []
        for tweet in reader.get_tweets():
            authors.append(tweet["author"])
            text.append(tweet["text"])
        self.assertEqual(authors, [ "author%d" % i for i in range(1, 10) ])
        self.assertEqual(text, [ "text%d" % i for i in range(1, 10) ])


class TestLearning(unittest.TestCase):
    def setUp(self):
        self.sentiment_model = learning.Sentiment()

    def testTweetTokenization(self):
        self.assertEqual(self.sentiment_model.tokenize("hello"),
                         ["hello"])
        self.assertEqual(self.sentiment_model.tokenize("hello world"),
                         ["hello", "world"])
        self.assertEqual(self.sentiment_model.tokenize("hello world :)"),
                         ["hello", "world", ":)"])
        self.assertEqual(self.sentiment_model.tokenize("hello... world..."),
                         ["hello", "...", "world", "..."])
        self.assertEqual(self.sentiment_model.tokenize("hello:) world:("),
                         ["hello", ":)", "world", ":("])
        self.assertEqual(self.sentiment_model.tokenize("hello...world..."),
                         ["hello", "...", "world", "..."])
        self.assertEqual(self.sentiment_model.tokenize("hello:-)world:-("),
                         ["hello", ":-)", "world", ":-("])
        self.assertEqual(self.sentiment_model.tokenize("@username: 1 2 3 hello"),
                         ["@username", ":", "1", "2", "3", "hello"])
        self.assertEqual(self.sentiment_model.tokenize("hello @username #hashtag!"),
                         ["hello", "@username", "#hashtag", "!"])
        self.assertEqual(self.sentiment_model.tokenize("@@@###"),
                         ["@@@###"])
        self.assertEqual(self.sentiment_model.tokenize("@username: the #hashtag!"),
                         ["@username", ":", "the", "#hashtag", "!"])

if __name__ == '__main__':
    unittest.main()
