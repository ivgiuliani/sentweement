from sentweement import settings

import sys

import tweepy


def auth():
    if not all([settings.CONSUMER_KEY,
                settings.CONSUMER_SECRET,
                settings.OAUTH_ACCESS_TOKEN,
                settings.OAUTH_ACCESS_TOKEN_SECRET]):
        err_str = "WARNING: empty oauth settings, twitter auth will fail\n"
        sys.stderr.write(err_str)

    auth = tweepy.auth.OAuthHandler(settings.CONSUMER_KEY,
                                    settings.CONSUMER_SECRET)
    auth.set_access_token(settings.OAUTH_ACCESS_TOKEN,
                          settings.OAUTH_ACCESS_TOKEN_SECRET)
    return auth
