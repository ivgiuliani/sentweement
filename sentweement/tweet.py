import string


class Tweet(object):
    """
    Represents a tweet.

    Tweet properties like the tweet id, the username and the text can
    only be assigned on initialization, afterwards they are set read-only.

    Every editing function will return a new tweet instance with the
    changes applied.
    """
    def __init__(self, tweet_id, username, text):
        self.__tweet_id = tweet_id
        self.__username = username
        self.__text = text

    def __str__(self):
        return self.__text

    @property
    def tid(self):
        return self.__tweet_id

    @property
    def username(self):
        return self.__username

    @property
    def text(self):
        return self.__text


class DummyTweet(Tweet):
    def __init__(self, text):
        Tweet.__init__(self, -1, "", text)
