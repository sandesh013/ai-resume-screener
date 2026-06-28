"""
NLP text preprocessing pipeline.

The app should start cleanly even when NLTK corpora are not installed or
network access is unavailable, so this module uses lightweight fallbacks.
"""
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


FALLBACK_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has',
    'have', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'to',
    'was', 'were', 'with', 'you', 'your'
}


def _has_nltk_resource(path):
    try:
        nltk.data.find(path)
        return True
    except LookupError:
        return False


HAS_PUNKT = _has_nltk_resource('tokenizers/punkt')
HAS_STOPWORDS = _has_nltk_resource('corpora/stopwords')
HAS_WORDNET = _has_nltk_resource('corpora/wordnet')


def clean_text(text):
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{6,}', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s\.\+\#\-\/]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text):
    cleaned = clean_text(text).lower()
    if HAS_PUNKT:
        try:
            return word_tokenize(cleaned)
        except LookupError:
            pass
    return re.findall(r'[a-z0-9\+\#][a-z0-9\+\#\-\/\.]*', cleaned)


def remove_stopwords(tokens):
    keep = {'c', 'r', 'go', 'no', 'not'}
    if HAS_STOPWORDS:
        try:
            stop_words = set(stopwords.words('english'))
        except LookupError:
            stop_words = FALLBACK_STOPWORDS
    else:
        stop_words = FALLBACK_STOPWORDS
    return [t for t in tokens if t not in stop_words or t in keep]


def lemmatize(tokens):
    if not HAS_WORDNET:
        return tokens
    lem = WordNetLemmatizer()
    try:
        return [lem.lemmatize(t) for t in tokens]
    except LookupError:
        return tokens


def preprocess(text):
    return lemmatize(remove_stopwords(tokenize(text)))


def preprocess_to_string(text):
    return ' '.join(preprocess(text))
