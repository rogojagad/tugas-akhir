import os
from nltk.parse import stanford
from pprint import pprint
from custom_utils import *
from nltk.tokenize import RegexpTokenizer
import json
import sys
from tqdm import tqdm

def parse(sentence):
    os.environ['JAVAHOME'] = "C:\Program Files\Java\jdk1.8.0_151\\bin"

    jar_path = "D:\Stanford Core NLP\stanford-corenlp-full-2018-10-05\stanford-corenlp-3.9.2.jar"
    model_path = "D:\Stanford Core NLP\stanford-corenlp-full-2018-10-05\stanford-corenlp-3.9.2-models.jar"

    parser = stanford.StanfordDependencyParser(path_to_jar=jar_path, path_to_models_jar=model_path)

    sentences = parser.raw_parse(sentence)

    dep = sentences.__next__()
    parsed = list(dep.triples())

    # pprint(parsed)

    # export(parsed, "test_result.pickle")

    return parsed

def get_governor_relation(tokenized, results):
    needed_relation = ['amod', 'nsubj', 'dependent']
    rel = {}

    for token in tokenized:
        for data in results:
            if data[0][0] == token and data[1] in needed_relation:
                if token in rel:
                    if data[1] not in rel[token].split(';'):
                        rel[token] += ';' + data[1]
                else:
                    rel[token] = data[1]

    return rel

def get_dependent_relation(tokenized, results):
    rel = {}
    for token in tokenized:
        for data in results:
            if data[2][0] == token:
                if token in rel:
                    if data[1] not in rel[token].split(';'):
                        rel[token] += ';' + data[1]
                else:
                    rel[token] = data[1]

    return rel

if __name__ == "__main__":
    with open('dataset/test-dataset.json') as f:
        dataset = json.load(f)

    result = []

    for i in tqdm(range(len(dataset))):
        result.append(parse(dataset[i]['sentence']))

    export(result, "\\test_dependency_parsed.pickle")