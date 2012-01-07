#-!- encoding: utf-8
import csv
import os
import shutil
import tempfile
import unittest

from sentweement import datareader
from sentweement import learning
from sentweement import tweet
from sentweement.learning import preprocessors


class TestPreprocessors(unittest.TestCase):
    def testUsernameRemoval(self):
        tests = (
            # full text, expected text
            ("@test: test!", "test!"),
            ("@u1: @u2!", ""),
            ("@username: loved what @username said", "loved what said"),
            ("no usernames", "no usernames"),
        )

        for test, expected_value in tests:
            t = tweet.Tweet(123456789, "username", test)
            self.assertEqual(preprocessors.remove_usernames(t).text, expected_value)

    def testRetweetRemoval(self):
        tests = (
            # full text, expected text
            ("RT @username: ehi", "@username: ehi"),
            ("RT: test", "test"),
        )

        for test, expected_value in tests:
            t = tweet.Tweet(123456789, "username", test)
            self.assertEqual(preprocessors.remove_retweets(t).text, expected_value)

    def testUrlRemoval(self):
        tests = (
            # full text, expected text
            ("http://google.com", ""),
            ("besides http://google.com", "besides"),
            ("abcd http://www.google.com efgh", "abcd efgh"),
            ("1111 www.google.com 2222", "1111 2222"),
        )

        for test, expected_value in tests:
            t = tweet.Tweet(123456789, "username", test)
            self.assertEqual(preprocessors.remove_urls(t).text, expected_value)

    def testTweetFix(self):
        tests = (
            # full text, expected text
            ("» Hello «", ">> Hello <<"),
            ("RT: test &gt; test2", "RT: test > test2"),
            ("“hello world“", "\"hello world\""),
        )

        for test, expected_value in tests:
            t = tweet.Tweet(123456789, "username", test)
            self.assertEqual(preprocessors.remap_characters(t).text, expected_value)

    def testEditChain(self):
        tests = (
            # full text, expected text
            ("» Hello www.google.com «", ">> Hello <<"),
            ("RT: test &gt; @test2", "test >"),
            ("RT: “hello world“", "\"hello world\""),
            ("RT: “hello www.google.com &gt; world“", "\"hello > world\""),
        )

        for test, expected_value in tests:
            t = tweet.Tweet(123456789, "username", test)

            preprocessors_list = [
                preprocessors.remap_characters,
                preprocessors.remove_usernames,
                preprocessors.remove_urls,
                preprocessors.remove_retweets
            ]
            for preprocessor in preprocessors_list:
                t = preprocessor(t)

            self.assertEqual(t.text, expected_value)


class TestReader(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        f1 = os.path.join(self.tmpdir, "data1")
        f2 = os.path.join(self.tmpdir, "data2")
        f3 = os.path.join(self.tmpdir, "data3")
        self.filenames = [f1, f2, f3]

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
        for item in reader.get_tweets():
            sentiment, tweet = item
            authors.append(tweet.username)
            text.append(tweet.text)
        self.assertEqual(authors, ["author%d" % i for i in range(1, 10)])
        self.assertEqual(text, ["text%d" % i for i in range(1, 10)])

    def testSentimentIsInteger(self):
        "Sentiment value must be converted to integers"
        reader = datareader.DataReader(self.filenames)
        for item in reader.get_tweets():
            sentiment, tweet = item
            self.assertTrue(isinstance(sentiment, int))


if __name__ == '__main__':
    unittest.main()
