import cld


def get_language(text):
    """Returns the language of a given text as a tuple like
    (LANGUAGE, language-code)"""
    return cld.detect(text)[:2]
