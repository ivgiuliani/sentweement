# -!-: coding: utf-8

import re

RE_USERNAME = re.compile(r"@\w+[:,;! ]*")
RE_RETWEET = re.compile(r"RT[:, ]*")
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
        ":)": ":-)",
        ":(": ":-(",
        ":D": ":-D",
    }

    text = tweet.text
    for key, val in mapping.iteritems():
        text = text.replace(key, val)

    while re.search(r"  ", text):
        text = re.sub(r"  ", " ", text)

    return Tweet(tweet.tid, tweet.username, text.strip())


def remove_usernames(tweet):
    "Remove @usernames from the given text"
    text = tweet.text
    while RE_USERNAME.search(text):
        text = re.sub(RE_USERNAME, "", text)
    return Tweet(tweet.tid, tweet.username, text.strip())


def remove_retweets(tweet):
    "Remove RT: retweets from the given text"
    text = tweet.text
    while RE_RETWEET.search(text):
        text = re.sub(RE_RETWEET, "", text)
    return Tweet(tweet.tid, tweet.username, text.strip())


def remove_urls(tweet):
    "Remove urls from the given text"
    text = tweet.text
    while RE_URLS.search(text):
        text = re.sub(RE_URLS, "", text)
    return Tweet(tweet.tid, tweet.username, text.strip())
