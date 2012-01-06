SETTINGS_FILE = "settings.py"

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_ACCESS_TOKEN = ""
OAUTH_ACCESS_TOKEN_SECRET = ""

from sentweement.learning import models
PREDICTION_MODEL = models.NaiveBayesModel

from sentweement.learning import features
FEATURE_EXTRACTORS = [
    features.extract_unigrams,
    features.extract_bigrams,
]
