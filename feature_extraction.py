import pickle
from pprint import pprint
from custom_utils import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

lemmatizer = WordNetLemmatizer()

data_dir = "D:\Kuliah\TA\data"

with open(data_dir + "\\train\\frequent_term.pickle", "rb") as inp:
    frequent_term = pickle.load(inp)

stopwords = stopwords.words("english")


def read_input():
    with open(data_dir + "\\train\labelled_words.pickle", "rb") as inp:
        lst = pickle.load(inp)

    return lst


def penn_to_wn(tag):
    if tag.startswith("J"):
        return wn.ADJ
    elif tag.startswith("N"):
        return wn.NOUN
    elif tag.startswith("R"):
        return wn.ADV
    elif tag.startswith("V"):
        return wn.VERB

    return None


def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]
    governor_relation = ""
    dependent_relation = ""
    wn_postag = penn_to_wn(postag)

    if wn_postag == None:
        lemmatized = lemmatizer.lemmatize(word.lower())
    else:
        lemmatized = lemmatizer.lemmatize(word.lower(), wn_postag)

    if doc[i][2] != None:
        governor_relation = doc[i][2]

    if doc[i][3] != None:
        dependent_relation = doc[i][3]

    if len(word) >= 5:
        exceeding = True
    else:
        exceeding = False

    if word in frequent_term:
        frequent = True
    else:
        frequent = False

    if word in stopwords:
        stopword = True
    else:
        stopword = False

    # Common features for all words
    features = [
        "word=" + word,
        "word.lower=" + word.lower(),
        "word.lemmatize=" + lemmatized,
        "word.is_frequent_term=%s" % frequent,
        "word.is_stopword=%s" % stopword,
        # "word.length_exceeding_5=%s" % exceeding,
        # "word.suffix=" + word[-3:],
        # "word.prefix=" + word[0:3],
        # 'word[-2:]=' + word[-2:],
        # 'word.isupper=%s' % word.isupper(),
        # 'word.istitle=%s' % word.istitle(),
        # 'word.isdigit=%s' % word.isdigit(),
        "postag=" + postag,
        "governor_relation=" + governor_relation,
        "dependent_relation=" + dependent_relation,
    ]

    if i - 2 > 0:
        word1 = doc[i - 2][0]
        postag1 = doc[i - 2][1]
        features.extend(
            [
                "-2:word.lower=" + word1.lower(),
                # '-1:word.istitle=%s' % word1.istitle(),
                # '-1:word.isupper=%s' % word1.isupper(),
                # '-1:word.isdigit=%s' % word1.isdigit(),
                "-2:postag=" + postag1,
            ]
        )

    # Features for words that are not
    # at the beginning of a document
    if i > 0:
        word1 = doc[i - 1][0]
        postag1 = doc[i - 1][1]
        features.extend(
            [
                "-1:word.lower=" + word1.lower(),
                # '-1:word.istitle=%s' % word1.istitle(),
                # '-1:word.isupper=%s' % word1.isupper(),
                # '-1:word.isdigit=%s' % word1.isdigit(),
                "-1:postag=" + postag1,
            ]
        )
    else:
        # Indicate that it is the 'beginning of a document'
        features.append("BOS")

    if i + 2 < len(doc) - 1:
        word1 = doc[i + 2][0]
        postag1 = doc[i + 2][1]
        features.extend(
            [
                "+1:word.lower=" + word1.lower(),
                # '+1:word.istitle=%s' % word1.istitle(),
                # '+1:word.isupper=%s' % word1.isupper(),
                # '+1:word.isdigit=%s' % word1.isdigit(),
                "+1:postag=" + postag1,
            ]
        )

    # Features for words that are not
    # at the end of a document
    if i < len(doc) - 1:
        word1 = doc[i + 1][0]
        postag1 = doc[i + 1][1]
        features.extend(
            [
                "+1:word.lower=" + word1.lower(),
                # '+1:word.istitle=%s' % word1.istitle(),
                # '+1:word.isupper=%s' % word1.isupper(),
                # '+1:word.isdigit=%s' % word1.isdigit(),
                "+1:postag=" + postag1,
            ]
        )
    else:
        # Indicate that it is the 'end of a document'
        features.append("EOS")

    return features


def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]


def extract_labels(doc):
    return [
        label for (token, postag, governor_relation, dependent_relation, label) in doc
    ]


if __name__ == "__main__":
    docs = read_input()

    # pprint(docs[0])

    # for doc in docs:
    #     for i in range(len(doc)):
    #         word2features(doc, i)
    #         print()

    X = [extract_features(doc) for doc in docs]
    y = [extract_labels(doc) for doc in docs]

    export(X, "\\train\\features.pickle")
    export(y, "\\train\\labels.pickle")

