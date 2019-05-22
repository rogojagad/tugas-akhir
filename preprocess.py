import json
import pickle
import sys
import string
from pprint import pprint

import spacy
from tqdm import tqdm

import dependency_parser
from custom_utils import *

from spellchecker import SpellChecker

data_dir = "D:\Kuliah\TA\data"

spell = SpellChecker()

nlp = spacy.load("en")


def read_dataset_file():
    with open("dataset/test-dataset.json") as f:
        data = json.load(f)

    return data


def tokenize_and_pos_tagging(sentence):
    tokens = []
    pos_tag_labels = []

    translator = str.maketrans("", "", string.punctuation)
    sentence = sentence.strip("\n")

    docs = nlp(sentence.translate(translator))

    for idx, doc in enumerate(docs):
        tokens.append(doc.text)
        pos_tag_labels.append(doc.pos_)

    return tokens, pos_tag_labels


def entity_labelling(list_of_targets, tokenized):
    targets = get_target(list_of_targets)

    words = []

    for token in tokenized:
        label = get_word_label(token, words, targets)

        words.append((token, label))

    # pprint(words)
    return words


def get_word_label(word, words_data, list_of_targets):
    for targets in list_of_targets:
        if word in targets:
            if targets.index(word) > 0:
                if words_data[-1][1] == "B" or words_data[-1][1] == "I":
                    return "I"
            elif targets.index(word) == 0:
                return "B"
    else:
        return "O"


def get_target(targets):
    splitted_targets = []

    for target in targets:
        # print(target.split(' '))
        splitted_targets.append(target.split(" "))

    return splitted_targets


def labelling(data, dependency_parsing_result):
    labelling_result = []

    tokenized, pos_tag_labels = tokenize_and_pos_tagging(data["sentence"])

    entity_labelling_results = entity_labelling(data["target"], tokenized)

    governor_relation_dict = dependency_parser.get_governor_relation(
        tokenized, dependency_parsing_result
    )

    dependent_relation_dict = dependency_parser.get_dependent_relation(
        tokenized, dependency_parsing_result
    )

    for result, pos_label in zip(entity_labelling_results, pos_tag_labels):
        token = result[0]
        bio_label = result[1]

        if token in governor_relation_dict:
            governor_relation = governor_relation_dict[token]
        else:
            governor_relation = None

        if token in dependent_relation_dict:
            dependent_relation = dependent_relation_dict[token]
        else:
            dependent_relation = None

        labelling_result.append(
            (token, pos_label, governor_relation, dependent_relation, bio_label)
        )

    # print()
    # pprint(labelling_result)

    # sys.exit()

    return labelling_result


if __name__ == "__main__":
    dataset = read_dataset_file()

    docs = []

    with open(data_dir + "\\test_dependency_parsed.pickle", "rb") as f:
        dependency_parsing_results = pickle.load(f)

    for i in tqdm(range(len(dataset))):
        docs.append(labelling(dataset[i], dependency_parsing_results[i]))

    # pprint(docs)

    export(docs, "\\test\labelled_words.pickle")
