import json
from nltk.tokenize import RegexpTokenizer
from pprint import pprint

def read_dataset_file():
    with open('dataset/ABSA-15_Restaurants_Train_Final.json') as f:
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

if __name__ == "__main__":
    dataset = read_dataset_file()

    doc = []

    for data in dataset:
        doc.append(entity_labelling(data))

    pprint(doc)
    # pprint(dataset)