import pickle
from pprint import pprint
from custom_utils import *

data_dir = "D:\Kuliah\TA\data"

def read_input():
    with open( data_dir + "\\test\labelled_pos_tagged_words.pickle", "rb") as inp:
        lst = pickle.load(inp)

    return lst

def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]

    # Common features for all words
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag
    ]

    # Features for words that are not
    # at the beginning of a document
    if i > 0:
        word1 = doc[i-1][0]
        postag1 = doc[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:word.isdigit=%s' % word1.isdigit(),
            '-1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'beginning of a document'
        features.append('BOS')

    # Features for words that are not
    # at the end of a document
    if i < len(doc)-1:
        word1 = doc[i+1][0]
        postag1 = doc[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:word.isdigit=%s' % word1.isdigit(),
            '+1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'end of a document'
        features.append('EOS')

    return features

def extract_features(doc):
    return [word2features(doc,i) for i in range(len(doc))]

def extract_labels(doc):
    return [label for (token, postag, label) in doc]

if __name__ == "__main__":
    docs = read_input()

    # pprint(docs[0])

    # for doc in docs:
    #     for i in range(len(doc)):
    #         word2features(doc, i)
    #         print()

    X = [extract_features(doc) for doc in docs]
    y = [extract_labels(doc) for doc in docs]

    export(X, '\\test\\features.pickle')
    export(y, '\\test\\labels.pickle')