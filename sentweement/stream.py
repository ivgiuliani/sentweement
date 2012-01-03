import tweepy

class SearchListener(tweepy.StreamListener):
    def __init__(self, auth, search_terms, status_callback,
                                           error_callback=None,
                                           limit_callback=None,
                                           cb_args=None):
        tweepy.StreamListener.__init__(self)

        self.search_terms = search_terms
        self.cb_status = status_callback
        self.cb_error = error_callback or None
        self.cb_limit = limit_callback or None
        self.cb_args = cb_args or []
        self.stream = tweepy.Stream(auth=auth,
                                    listener=self,
                                    timeout=300)

    def run(self):
        if self.search_terms:
            self.stream.filter(track=self.search_terms)
        else:
            self.stream.sample()

    def close(self):
        self.stream.disconnect()

    def on_status(self, status):
        if not self.cb_status(status, *self.cb_args):
            self.close()

    def on_limit(self, track):
        if self.cb_limit:
            self.cb_limit(track)

    def on_error(self, status_code):
        if self.cb_error:
            self.cb_error(status_code)
