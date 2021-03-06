from enum import Enum
import tweepy
import pytz
import re
from textblob.classifiers import NaiveBayesClassifier, DecisionTreeClassifier, NLTKClassifier
from textblob.utils import strip_punc
from datetime import datetime
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def twitter_time_to_datetime(twitter_time):
    return datetime.strptime(twitter_time,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)

class Classifications(Enum):
	democrat = 1
	republican = 2
	third = 3

class MyClassifier(NLTKClassifier):
    nltk_class = SklearnClassifier(LogisticRegression())

class Pclassifier:
    def __init__(self, filename, wordset):
        self.filename = filename
        self.wordset = wordset
        self.classifier = None

    def normalize(self, t):
        return strip_punc(t, all=True).lower()

    def custom_extractor(self, document, train_set):
        tokens = document.split()
        tokens = [self.normalize(t) for t in tokens]
        features = dict(((u'contains({0})'.format(word), (word in tokens))
                                            for word in self.wordset))
        return features

    def train(self, train_set):
        self.classifier = MyClassifier(train_set, self.custom_extractor)

    def classify(self, text):
        return self.classifier.classify(text)

    def probs(self, text):
        probs = {}
        prob_dist = self.classifier.prob_classify(text)
        for label in self.classifier.labels():
            probs[str(label)] = prob_dist.prob(label)
        return probs


    def notable_features(self):
        self.classifier.show_informative_features()

    def test(self, test_set):
        print(self.classifier.accuracy(test_set))

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
