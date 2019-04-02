import pickle
import json
import sys
from pprint import pprint
from nltk.tokenize import RegexpTokenizer
from custom_utils import *

with open("dataset/test-dataset.json") as f:
    dataset = json.load(f)

with open("D:\\Kuliah/TA/data/test_dependency_parsed.pickle", "rb") as f:
    dependency_parsing_results = pickle.load(f)

tokenizer = RegexpTokenizer(r"\w+")
headword_result = []

for data, result in zip(dataset, dependency_parsing_results):
    token_list = tokenizer.tokenize(data["sentence"])

    temp = []

    for token in token_list:
        match_item = 0

        for item in result:
            if item[2][0] == token:
                match_item = result.index(item)
                temp.append((token, item[0][0], item[0][1]))
                break
        else:
            temp.append((token, None, None))

        if len(result) != 0:
            del result[match_item]

    headword_result.append(temp)

# pprint(headword_result)

export(headword_result, "/test/headword_pair.pickle")
