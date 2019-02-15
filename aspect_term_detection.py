import pycrfsuite
import pickle
from pprint import pprint
from custom_utils import *

data_dir = "D:\Kuliah\TA\data"

def load_train_data():
    with open(data_dir + "\\train\\features.pickle", "rb") as inp:
        feature = pickle.load(inp)

    with open(data_dir + "\\train\\labels.pickle", "rb") as inp:
        labels = pickle.load(inp)

    return feature, labels

def train(X_train, y_train):
    trainer = pycrfsuite.Trainer()

    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1' : 10,
        'c2' : 0.01,
        'feature.possible_transitions': True,
    })

    trainer.train('crf.model')

def load_test_data():
    with open(data_dir + "\\test\\features.pickle", "rb") as inp:
        feature = pickle.load(inp)

    with open(data_dir + "\\test\\labels.pickle", "rb") as inp:
        labels = pickle.load(inp)

    return feature, labels

def predict(X_test):
    print("=========== NOW DETECTING ASPECT TERM ON TEST DATA ===============\n")

    tagger = pycrfsuite.Tagger('crf.model')

    tagger.open('crf.model')
    
    result = [tagger.tag(xseq) for xseq in X_test]

    print("===========               FINISH                   ===============\n")

    return result

def make_result(y_result):
    with open(data_dir + "\\test\\labelled_words.pickle", "rb") as inp:
        words = pickle.load(inp)

    prediction_result = []

    for data in zip(words, y_result):
        temp = []

        for i in range(len(data[0])):
            word = data[0][i][0]
            label = data[1][i]

            temp.append((word, label))
        
        prediction_result.append(temp)

    return prediction_result

if __name__ == "__main__":
    xseq, yseq = load_train_data()

    train(xseq, yseq)

    X_test, y_test = load_test_data()

    y_result = predict(X_test)

    export(y_result, "\\test\prediction_labels.pickle")

    prediction_result = make_result(y_result)

    export(prediction_result, "\\test\prediction_result.pickle")