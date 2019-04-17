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


def entity_labelling(data):
    targets = get_target(data["target"])

    words = []
    translator = str.maketrans("", "", string.punctuation)
    sentence = data["sentence"]

    doc = nlp(sentence.translate(translator))

    for idx, token in enumerate(doc):
        label = get_word_label(token.orth_, idx, words, targets)

        words.append((token.text, label))

    # pprint(words)
    return words, doc


def get_word_label(word, idx, words_data, list_of_targets):
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

    entity_labelling_results, spacy_docs = entity_labelling(data)

    tokenized = [result[0] for result in entity_labelling_results]

    governor_relation_dict = dependency_parser.get_governor_relation(
        tokenized, dependency_parsing_result
    )

    dependent_relation_dict = dependency_parser.get_dependent_relation(
        tokenized, dependency_parsing_result
    )

    for result, spacy_doc in zip(entity_labelling_results, spacy_docs):
        token = result[0]
        bio_label = result[1]
        post_tag_label = spacy_doc.pos_

        if token in governor_relation_dict:
            governor_relation = governor_relation_dict[token]
        else:
            governor_relation = None

        if token in dependent_relation_dict:
            dependent_relation = dependent_relation_dict[token]
        else:
            dependent_relation = None

        labelling_result.append(
            (token, post_tag_label, governor_relation, dependent_relation, bio_label)
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
