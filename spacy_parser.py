import spacy
import json
from pprint import pprint
from custom_utils import *


class SpacyParser:
    def __init__(self):
        self.nlp = spacy.load("en")
        self.result = list()

    def parse(self, sentence):
        document = self.nlp(sentence)

        edges = []
        for token in document:
            # FYI https://spacy.io/docs/api/token
            for child in token.children:
                edges.append(
                    (
                        "{0}-{1}".format(token.lower_, token.i),
                        "{0}-{1}".format(child.lower_, child.i),
                    )
                )

        self.result.append(edges)

    def export(self):
        export(self.result, "spacy_dependency_parsing_result.pickle")


if __name__ == "__main__":
    with open("dataset/test-dataset.json") as f:
        dataset = json.load(f)

    parser = SpacyParser()

    for data in dataset:
        parser.parse(data["sentence"])

    parser.export()
