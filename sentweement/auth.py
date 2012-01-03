from sentweement import settings

import sys

import tweepy

def _init():
    if not all([settings.CONSUMER_KEY, settings.CONSUMER_SECRET,
                settings.OAUTH_ACCESS_TOKEN, settings.OAUTH_ACCESS_TOKEN_SECRET]):
        sys.stderr.write("WARNING: empty oauth settings, twitter auth will fail\n")

    auth = tweepy.auth.OAuthHandler(settings.CONSUMER_KEY,
                                    settings.CONSUMER_SECRET)
    auth.set_access_token(settings.OAUTH_ACCESS_TOKEN,
                          settings.OAUTH_ACCESS_TOKEN_SECRET)
    return auth

_auth = _init()

def get_auth_token():
    return _auth
