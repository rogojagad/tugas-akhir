import json
import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from pprint import pprint
from custom_utils import *

save_path = "D:\Kuliah\TA\data"

def read_dataset_file():
    with open('dataset/test-dataset.json') as f:
        data = json.load(f)

    return data

def entity_labelling(data):
    targets = get_target(data['target'])
    
    words = []

    tokenizer = RegexpTokenizer(r'\w+')

    for word in tokenizer.tokenize(data['sentence']):        
        label = get_word_label(word, targets)

        words.append((word, label))

    # print(words)
    return words

def get_word_label(word, list_of_targets):
    for targets in list_of_targets:
        if word in targets:
            if targets.index(word) > 0:
                return "I"
            else:
                return "B"
    else:
        return "O"

def get_target(targets):
    splitted_targets = []

    for target in targets:
        # print(target.split(' '))
        splitted_targets.append(target.split(' '))

    return splitted_targets

def pos_tag_labelling(docs):
    data = []

    for i, doc in enumerate(docs):
        tokens = [t for t, label in doc]

        tagged = nltk.pos_tag(tokens)

        data.append([(w, pos, label) for (w, label), (word, pos) in zip(doc, tagged)])

    return data

if __name__ == "__main__":
##################################################
#   Bagian ini tidak perlu di-running ulang, cukup import dr pickle aja
#   Kalo ada perubahan di dataset baru dijalanin ulang

    dataset = read_dataset_file()

    docs = []

    for data in dataset:
        docs.append(entity_labelling(data))

    export(docs, "\\test\labelled_words.pickle")
################################################## 

    # with open(save_path + '\\train\labelled_words.pickle', 'rb') as inp:
    #     docs = pickle.load(inp)

    docs_pos_tagged = pos_tag_labelling(docs)

    export(docs_pos_tagged, "\\test\labelled_pos_tagged_words.pickle")