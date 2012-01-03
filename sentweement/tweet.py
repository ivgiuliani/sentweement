# -!-: coding: utf-8

import re
import string

def fix(text):
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

    for key, val in mapping.iteritems():
        text = text.replace(key, val)

    while re.search(r"  ", text):
        text = re.sub(r"  ", " ", text)

    return text.strip()

RE_USERNAME = re.compile(r"@\w+[:,;! ]*")
def remove_usernames(text):
    "Remove @usernames from the given text"
    while RE_USERNAME.search(text):
        text = re.sub(RE_USERNAME, "", text)
    return text.strip()

RE_RETWEET = re.compile(r"RT[:, ]*")
def remove_retweets(text):
    "Remove RT: retweets from the given text"
    while RE_RETWEET.search(text):
        text = re.sub(RE_RETWEET, "", text)
    return text.strip()

RE_URLS = re.compile(r"([\w-]+://[\w.-/]+|www.[\w.-/]+)[ ]*")
def remove_urls(text):
    "Remove urls from the given text"
    while RE_URLS.search(text):
        text = re.sub(RE_URLS, "", text)
    return text.strip()

