# -!-: coding: utf-8
from sentweement.tweet import Tweet

import re

RE_USERNAME = re.compile(r"@\w+[:,;! ]*")
RE_RETWEET = re.compile(r"RT[:, ]*")
RE_HASHTAGS = re.compile(r"#(\w+)")
RE_URLS = re.compile(r"([\w-]+://[\w.-/]+|www.[\w.-/]+)[ ]*")


def convert_to_lowercase(tweet):
    "Convert a tweet to an equivalent lowercase representation"
    return Tweet(tweet.tid, tweet.username, tweet.text.lower())


def remap_characters(tweet):
    """Fix a tweet by converting it in a proper and equivalent text
    format for easier successive analysis.
    """
    mapping = {
        "\r": " ",
        "\n": " ",
        "\t": " ",
        "&gt;": ">",
        "&lt;": "<",
        "&#39;": "'",
        "&quot;": "\"",
        "“": "\"",
        "’": "'",
        "»": ">>",
        "«": "<<",
        ":)": ":-)", "(:": ":-)",
        ":(": ":-(", "):": ":-(",
        ":@": ":-@", "@:": ":-@",
        ":D": ":-D",
        ":d": ":-D",
        ":P": ":-p",
        ":p": ":-p",
        ":O": ":-O", "O:": ":-O",
        ":o": ":-O", "o:": ":-O",
    }

    text = tweet.text
    for key, val in mapping.iteritems():
        text = text.replace(key, val)

    while re.search(r"  ", text):
        text = re.sub(r"  ", " ", text)

    return Tweet(tweet.tid, tweet.username, text.strip())


def remove_usernames(tweet):
    "Remove @usernames from the given tweet"
    text = tweet.text
    while RE_USERNAME.search(text):
        text = re.sub(RE_USERNAME, "", text)
    return Tweet(tweet.tid, tweet.username, text.strip())


def remove_retweets(tweet):
    "Remove RT: retweets from the given tweet"
    text = tweet.text
    while RE_RETWEET.search(text):
        text = re.sub(RE_RETWEET, "", text)
    return Tweet(tweet.tid, tweet.username, text.strip())


def remove_urls(tweet):
    "Remove urls from the given tweet"
    text = tweet.text
    while RE_URLS.search(text):
        text = re.sub(RE_URLS, "", text)
    return Tweet(tweet.tid, tweet.username, text.strip())


def remove_hashtags(tweet):
    "Remove hashtags from the given tweet"
    text = tweet.text
    while RE_HASHTAGS.search(text):
        text = re.sub(RE_HASHTAGS, "", text)
    return Tweet(tweet.tid, tweet.username, text.strip())
