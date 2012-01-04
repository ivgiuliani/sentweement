#!/usr/bin/env python
import sys

from sentweement import auth
from sentweement import settings
from sentweement import stream
from sentweement import language

def searchCB(status, filter_language):
    author =status.author.screen_name
    text = status.text

    author = author.encode("utf-8")
    text = text.encode("utf-8")

    lang = language.get_language(text)
    if lang[1] == filter_language:
        print "%s: %s" % (author.rjust(21), text)
    return True

def main(args):
    try:
        language = args[1]
        search = args[2:]
    except (IndexError, KeyError):
        print "Usage: %s <language> <search terms>" % args[0]
        return True

    settings.use("settings.py")

    s = stream.SearchListener(auth.auth(), search, searchCB, cb_args=(language,))
    try:
        s.run()
    except KeyboardInterrupt:
        s.close()

    return False

if __name__ == "__main__":
    sys.exit(main(sys.argv))
