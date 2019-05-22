import pickle
import json


class GeneralInquirerLexiconValueGetter:
    def __init__(self):
        data_dir = "D://Kuliah/TA/data"

        # with open(data_dir + "/general-inquirer/positive-words.pickle", "rb") as inp:
        #     self.positive_lex = pickle.load(inp)

        with open(data_dir + "/general-inquirer/lexicon.json") as inp:
            self.lexicon = json.load(inp)

        print("General Lexicon Value Getter instantiated...")

    def get_value(self, token):
        try:
            polarity = self.lexicon[token]

            if polarity == "positive":
                return 1
            elif polarity == "negative":
                return -1
            else:
                return 0
        except KeyError:
            return 0


if __name__ == "__main__":
    getter = GeneralInquirerLexiconValueGetter()

    print(getter.get_value("complete"))
