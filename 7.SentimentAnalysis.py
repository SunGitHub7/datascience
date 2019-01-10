import nltk
import pandas as pd
from nltk.corpus import movie_reviews, stopwords
from nltk.classify import NaiveBayesClassifier
import string


# nltk.download('movie_reviews')  # This is the one time command, hence place in comment
# nltk.download('punkt')
# nltk.download('stopwords')
uslss_wrds = stopwords.words('english')+list(string.punctuation)  # ['i','you','they','me','myself'..]+[',','!','(',..]


def emotional_word_bag(words):
    word_dict = {word: 1 for word in words if word not in uslss_wrds}
    return word_dict


def emotional_word_list(words):
    word_list = [word for word in words if word not in uslss_wrds]
    return word_list


# print(movie_reviews.fileids())  # file Name in List form


negtv = movie_reviews.fileids('neg')  # 1000 .txt files with neg name
postv = movie_reviews.fileids('pos')  # 1000 .txt file with pos name

words1 = movie_reviews.words(fileids=postv[0])  # create word list (words1) from first postv review files (postv)
nit_words1 = emotional_word_bag(words1)  # only sentimental words is preferred from words1 list


# Create Dictinary of all the Negtv and Postv word seperately with label neg and pos respectively----------------------
# create the list of 1000 ( No. of File ) tuples having dictionary of word (each file) as key and 1 as value with neg
# [1000(No. of File) * tuple( dict{random('word': 1)},'neg') ]
negtv_ftrs = [(emotional_word_bag(movie_reviews.words(fileids=[f])), 'neg') for f in negtv]
postv_ftrs = [(emotional_word_bag(movie_reviews.words(fileids=[f])), 'pos') for f in postv]
print(pd.DataFrame(negtv_ftrs))

# Use Simplest supervised ML classifier is NaiveBayesClassifier ( It gives pretty good accuracy w.r.t. simplicity )
split = int(0.8*len(negtv_ftrs))  # using 80% of data for training the NBC
sntmnt_clssfr = NaiveBayesClassifier.train(postv_ftrs[:split]+negtv_ftrs[:split])

accrcy = nltk.classify.util.accuracy(sntmnt_clssfr,postv_ftrs[split:]+negtv_ftrs[split:])*100  # Accuracy is 71.75 %
imprtnt_ftrs = sntmnt_clssfr.show_most_informative_features()  # Gives most Informative words for pos/neg sentiments
print(imprtnt_ftrs)


