# -!-: coding: utf-8

import re
import string

class Tweet(object):
    """
    Represents a tweet

    Tweet properties like the timestamp, the username and the text can
    only be assigned on initialization, afterwards they are set read-only.

    Every editing function will return a new tweet instance with the
    changes applied.
    """
    RE_USERNAME = re.compile(r"@\w+[:,;! ]*")
    RE_RETWEET = re.compile(r"RT[:, ]*")
    RE_URLS = re.compile(r"([\w-]+://[\w.-/]+|www.[\w.-/]+)[ ]*")

    def __init__(self, timestamp, username, text):
        self.__timestamp = timestamp
        self.__username = username
        self.__text = text

    def __str__(self):
        return self.__text

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def username(self):
        return self.__username

    @property
    def text(self):
        return self.__text

    def fix(self):
        """Fix a tweet by converting it in a proper and equivalent text
        format for easier successive analysis.
        """
        mapping = {
            "\r": " ",
            "\n": " ",
            "\t": " ",
            "&gt;" : ">",
            "&lt;" : "<",
            "&#39;": "'",
            "&quot;": "\"",
            "“": "\"",
            "’": "'",
            "»": ">>",
            "«": "<<",
        }

        text = self.text
        for key, val in mapping.iteritems():
            text = text.replace(key, val)

        while re.search(r"  ", text):
            text = re.sub(r"  ", " ", text)

        return Tweet(self.timestamp, self.username, text.strip())

    def remove_usernames(self):
        "Remove @usernames from the given text"
        text = self.text
        while self.RE_USERNAME.search(text):
            text = re.sub(self.RE_USERNAME, "", text)
        return Tweet(self.timestamp, self.username, text.strip())

    def remove_retweets(self):
        "Remove RT: retweets from the given text"
        text = self.text
        while self.RE_RETWEET.search(text):
            text = re.sub(self.RE_RETWEET, "", text)
        return Tweet(self.timestamp, self.username, text.strip())

    def remove_urls(self):
        "Remove urls from the given text"
        text = self.text
        while self.RE_URLS.search(text):
            text = re.sub(self.RE_URLS, "", text)
        return Tweet(self.timestamp, self.username, text.strip())
