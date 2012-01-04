#!/usr/bin/env python
import sys
import time
import csv

from sentweement import auth
from sentweement import settings
from sentweement import stream
from sentweement import language

class Analyzer(object):
    def __init__(self, language, count, output):
        self.language = language
        self.count = count
        self.counter = 0

        self._output = csv.writer(open(output, "w"))

    def cb_search(self, status):
        author = status.author.screen_name
        text = status.text

        author = author.encode("utf-8")
        text = text.encode("utf-8")

        lang = language.get_language(text)
        if lang[1] == self.language:
            self._output.writerow([0, time.time(), author, text])
            self.counter += 1

        if self.counter < self.count:
            return True
        return False

def main(args):
    try:
        language = args[1]
        count = int(args[2])
        output = args[3]
    except (IndexError, KeyError, ValueError):
        print "Usage: %s <language> <tweet count> <output>" % args[0]
        return True

    settings.use("settings.py")

    anal = Analyzer(language, count, output)
    s = stream.SearchListener(auth.auth(), "", anal.cb_search)

    try:
        s.run()
    except KeyboardInterrupt:
        s.close()

    return False

if __name__ == "__main__":
    sys.exit(main(sys.argv))
