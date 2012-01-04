import nltk

class Sentiment(object):
    "Sentiment classifier for tweets"

    SNT_POSITIVE = 1
    SNT_NEUTRAL  = 0
    SNT_NEGATIVE = -1

    def tokenize(self, text):
        """Splits a sentence into tokens

        This also takes in account twitter particular features,
        as @usernames and #hashtags by joining adjacent tokens
        when it makes sense so that for example '@' and 'username' are
        always a single token
        """
        TWITTER_CHARS = "#@"

        nltk_tokens = nltk.wordpunct_tokenize(text)
        tokens = []
        for tok1, tok2 in zip(nltk_tokens, nltk_tokens[1:]):
            if tok1 in TWITTER_CHARS:
                tokens.append(tok1 + tok2)
            elif tok2 not in TWITTER_CHARS:
                tokens.append(tok2) 

        if len(nltk_tokens) > 0 and nltk_tokens[0] not in TWITTER_CHARS:
            tokens = [ nltk_tokens[0] ] + tokens
        return tokens

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
