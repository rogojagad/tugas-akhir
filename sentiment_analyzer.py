import pickle
import sys

from pprint import pprint
from tqdm import tqdm

from valueGetter.gi_lexicon_value_getter import GeneralInquirerLexiconValueGetter
from valueGetter.mpqa_value_getter import MPQALexiconValueGetter
from valueGetter.sentiwordnet_value_getter import SentiWordNetValueGetter

from distanceGetter.token_distance_getter import TokenDistanceGetter
from distanceGetter.dependency_path_distance_getter import DependencyPathDistanceGetter


class SentimentAnalyzer:
    def __init__(self):
        self.gi_lexicon_value_getter = GeneralInquirerLexiconValueGetter()
        self.mpqa_value_getter = MPQALexiconValueGetter()
        self.sentiwordnet_value_getter = SentiWordNetValueGetter()

        self.token_distance_getter = TokenDistanceGetter()
        self.dependency_path_distance_getter = DependencyPathDistanceGetter()

        self.negation_words = ["not", "no"]

    def analyze(self, doc, doc_idx):
        self.token_distance_getter.set_sentence(doc)

        for idx, data in enumerate(doc):
            if data[2] == "B":
                backward_value = self.analyze_backward(doc, idx, doc_idx)
                # forward_value = self.analyze_forward(doc, idx)

        sys.exit()

    def analyze_backward(self, doc, target_idx, doc_idx):
        i = target_idx - 1
        target_word = doc[target_idx][0]

        total_value = 0

        while i >= 0:
            opinion_word = doc[i][0]

            lexicon_value = self.get_lexicon_value_sum(opinion_word.lower(), doc[i])

            distance_value = self.get_distance_value_sum(
                target_word, target_idx, opinion_word, i, doc_idx
            )

            total_value += lexicon_value / distance_value
            i -= 1

        return total_value

    def analyze_forward(self, doc, target_idx):
        # for i in range(target_idx + 1, len(doc)):
        #     if doc[i][2] != "I":
        #         pprint(doc[i][0])
        pass

    def get_lexicon_value_sum(self, opinion_word, token_data):
        gi_lexicon_value = self.gi_lexicon_value_getter.get_value(opinion_word.lower())

        mpqa_value = self.mpqa_value_getter.get_value(opinion_word.lower())

        sentiwordnet_value = self.sentiwordnet_value_getter.get_value(token_data)

        print(gi_lexicon_value)
        print(mpqa_value)
        print(sentiwordnet_value)

        return gi_lexicon_value + mpqa_value + sentiwordnet_value

    def get_distance_value_sum(self, target_word, target_idx, opinion_word, i, doc_idx):
        token_distance = self.token_distance_getter.get_distance_value(
            target_word, target_idx, opinion_word, i
        )

        dependency_distance = self.dependency_path_distance_getter.get_distance_value(
            target_word, target_idx, opinion_word.lower(), i, doc_idx
        )

        return token_distance + dependency_distance


def get_document():
    with open("D:\Kuliah/TA/data/test/prediction_result.pickle", "rb") as inp:
        return pickle.load(inp)


if __name__ == "__main__":
    sentiment_analyzer = SentimentAnalyzer()

    document = get_document()

    result = list()

    for i in tqdm(range(len(document))):
        print()
        result.append(sentiment_analyzer.analyze(document[i], i))
