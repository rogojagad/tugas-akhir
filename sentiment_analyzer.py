import pickle
import sys

from pprint import pprint
from tqdm import tqdm

from valueGetter.gi_lexicon_value_getter import GeneralInquirerLexiconValueGetter
from valueGetter.mpqa_value_getter import MPQALexiconValueGetter
from valueGetter.sentiwordnet_value_getter import SentiWordNetValueGetter
from valueGetter.bing_liu_value_getter import BingLiuLexiconValueGetter

from distanceGetter.token_distance_getter import TokenDistanceGetter
from distanceGetter.dependency_path_distance_getter import DependencyPathDistanceGetter

from custom_utils import export


class SentimentAnalyzer:
    def __init__(self):
        self.gi_lexicon_value_getter = GeneralInquirerLexiconValueGetter()
        self.mpqa_value_getter = MPQALexiconValueGetter()
        self.sentiwordnet_value_getter = SentiWordNetValueGetter()
        self.bing_liu_value_getter = BingLiuLexiconValueGetter()

        self.token_distance_getter = TokenDistanceGetter()
        self.dependency_path_distance_getter = DependencyPathDistanceGetter()

        self.negation_words = ["not", "no", "never", "until", "nt"]

        self.needed_pos_label = ["ADJ", "ADV", "VERB", "DET", "NOUN"]

        self.current_target_words_list = list()

        self.result = list()

    def analyze(self, doc, doc_idx):
        self.token_distance_getter.set_sentence(doc)
        self.current_target_words_list = self.token_distance_getter.aspect_words_list

        target_counter = 0

        doc_result = dict()
        temp = dict()
        doc_result["id"] = doc_idx
        # pprint(doc)
        # print(doc_idx)
        for idx, data in enumerate(doc):
            if data[2] == "B":
                backward_value = self.analyze_backward(doc, idx, doc_idx)
                forward_value = self.analyze_forward(doc, idx, doc_idx)
                total_polarity_value = backward_value + forward_value

                # if doc_idx == 347:
                #     print()
                #     print(
                #         "Word is : {} and backward value is {} and forward value is {}, total polarity score is {}".format(
                #             self.current_target_words_list[target_counter],
                #             backward_value,
                #             forward_value,
                #             total_polarity_value,
                #         )
                #     )

                if total_polarity_value > 0:
                    polarity = "positive"
                elif total_polarity_value < 0:
                    polarity = "negative"
                else:
                    polarity = "neutral"

                # print(
                #     "{} is {}".format(
                #         self.current_target_words_list[target_counter], polarity
                #     )
                # )

                temp[self.current_target_words_list[target_counter]] = polarity

                target_counter += 1

            doc_result["data"] = temp
        self.result.append(doc_result)

    def analyze_backward(self, doc, target_idx, doc_idx):
        i = target_idx - 1
        target_word = doc[target_idx][0]

        total_value = 0

        while i >= 0:
            # if doc_idx == 364:
            #     print(doc[i][0])
            # if doc[i][1] in self.needed_pos_label:
            opinion_word = doc[i][0]

            lexicon_value = self.get_lexicon_value_sum(
                opinion_word.lower(), doc[i], doc_idx
            )

            distance_value = self.get_distance_value_sum(
                target_word, target_idx, opinion_word, i, doc_idx
            )

            value = lexicon_value / distance_value

            # if doc_idx == 347:
            #     print()
            #     print(opinion_word)
            #     print(lexicon_value)

            if self.check_negation(i, doc):
                value *= -1

            total_value += value

            i -= 1

        return total_value

    def analyze_forward(self, doc, target_idx, doc_idx):
        total_value = 0
        target_word = doc[target_idx][0]

        for i in range(target_idx + 1, len(doc)):
            # print(doc[i][1])
            # if doc[i][1] in self.needed_pos_label:
            if doc[i][2] != "I":
                opinion_word = doc[i][0]

                lexicon_value = self.get_lexicon_value_sum(
                    opinion_word.lower(), doc[i], doc_idx
                )

                distance_value = self.get_distance_value_sum(
                    target_word, target_idx, opinion_word, i, doc_idx
                )

                # if doc_idx == 349:
                #     print("Target word : " + target_word)
                #     print("Opinion word : " + opinion_word)
                #     print(lexicon_value)
                #     print(distance_value)

                value = lexicon_value / distance_value

                if self.check_negation(i, doc):
                    value *= -1

                total_value += value

        return total_value

    def check_negation(self, i, doc):
        j = 1

        while j <= 3:
            idx = i + j
            if idx < len(doc):
                if doc[idx][0] in self.negation_words:
                    return True
            else:
                break

            j += 1

        j = 1

        while j <= 3:
            idx = i - j

            if idx >= 0:
                if doc[idx][0] in self.negation_words:
                    return True
            else:
                break

            j += 1

        # if doc[i - 1][0] in self.negation_words:
        #     return True

        # return False

    def get_lexicon_value_sum(self, opinion_word, token_data, idx):
        gi_lexicon_value = self.gi_lexicon_value_getter.get_value(opinion_word.lower())

        mpqa_value = self.mpqa_value_getter.get_value(opinion_word.lower())

        sentiwordnet_value = self.sentiwordnet_value_getter.get_value(token_data)

        bing_liu_value = self.bing_liu_value_getter.get_value(opinion_word.lower())

        # if idx == 349:
        #     print("GI Lexicon : {}".format(gi_lexicon_value))
        #     print("MPQA : {}".format(mpqa_value))
        #     print(sentiwordnet_value)
        #     print(bing_liu_value)

        return sentiwordnet_value + gi_lexicon_value + mpqa_value + bing_liu_value

    def get_distance_value_sum(self, target_word, target_idx, opinion_word, i, doc_idx):
        token_distance = self.token_distance_getter.get_distance_value(
            target_word, target_idx, opinion_word, i
        )

        dependency_distance = self.dependency_path_distance_getter.get_distance_value(
            target_word.lower(), target_idx, opinion_word.lower(), i, doc_idx
        )

        if token_distance == 0:
            token_distance += 1

        return token_distance

    def export_and_print(self):
        # pprint(self.result)

        export(self.result, "/test/sentiment_analyze_result.pickle")


def get_document():
    with open("D:\Kuliah/TA/data/test/prediction_result.pickle", "rb") as inp:
        return pickle.load(inp)


if __name__ == "__main__":
    sentiment_analyzer = SentimentAnalyzer()

    document = get_document()

    result = list()

    for i in tqdm(range(len(document))):
        result.append(sentiment_analyzer.analyze(document[i], i))

    sentiment_analyzer.export_and_print()

    # pprint(sentiment_analyzer.result)

    # sentiment_analyzer.analyze(document[48], 48)
