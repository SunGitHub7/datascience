#Run this file after Train_Classifiers.py, where training and pickling happens.
#Or you can also use the saved pickles for running this file, as provided in this repository.
#Creating the sentiment analysis module.


import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

# Here, redefine class and requisite find_feature() for convenience


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers  # Here we will have tuple of classifier

    def classify(self, features):  # Here, comment is qualitatively return pos or neg class of
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):  # Here, we return quantitative analysis of comment for above class
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


with open("documents.pickle", "rb") as documents_f:
    documents = pickle.load(documents_f)

with open("word_features5k.pickle", "rb") as word_features5k_f:
    word_features = pickle.load(word_features5k_f)


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


with open("featuresets.pickle", "rb") as featuresets_f:
    featuresets = pickle.load(featuresets_f)


random.shuffle(featuresets)
print(len(featuresets))

testing_set = featuresets[10000:]
training_set = featuresets[:10000]

#

with open("originalnaivebayes5k.pickle", "rb") as open_file:
     classifier = pickle.load(open_file)


with open("MNB_classifier5k.pickle", "rb") as open_file:
      MNB_classifier = pickle.load(open_file)

with open("BernoulliNB_classifier5k.pickle", "rb") as open_file:
    BernoulliNB_classifier = pickle.load(open_file)


with open("LogisticRegression_classifier5k.pickle", "rb") as open_file:
    LogisticRegression_classifier = pickle.load(open_file)


with open("LinearSVC_classifier5k.pickle", "rb") as open_file:
    LinearSVC_classifier = pickle.load(open_file)

with open("SGDC_classifier5k.pickle", "rb") as open_file:
    SGDC_classifier = pickle.load(open_file)

voted_classifier = VoteClassifier(
                                  classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

# Sentiment function only takes one parameter text.
# From there, we break down the features with the find_features function.


def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)