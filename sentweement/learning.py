class Sentiment(object):
    "Sentiment classifier for tweets"

    SNT_POSITIVE = 1
    SNT_NEUTRAL  = 0
    SNT_NEGATIVE = -1

    def fit(self, text, sentiment):
        """
        Updates the model by adding the given text with the tagged
        sentiment label. The sentiment must be one of SNT_POSITIVE,
        SNT_NEGATIVE or SNT_NEUTRAL.
        """
        pass

    def predict(self, text):
        """
        Returns the predicted sentiment for the given tweet's text.
        The predicted sentiment will be one of SNT_POSITIVE,
        SNT_NEGATIVE or SNT_NEUTRAL.
        """
        pass
