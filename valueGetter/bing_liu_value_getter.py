import pickle


class BingLiuLexiconValueGetter:
    def __init__(self):
        data_dir = "D://Kuliah/TA/data"

        with open(
            data_dir + "/bing-liu-opinion-lexicon/positive-words.pickle", "rb"
        ) as inp:
            self.positive_lex = pickle.load(inp)

        with open(
            data_dir + "/bing-liu-opinion-lexicon/negative-words.pickle", "rb"
        ) as inp:
            self.negative_lex = pickle.load(inp)

        print("Bing Liu Value Getter instantiated...")

    def get_value(self, token):
        if token in self.positive_lex:
            return 1
        elif token in self.negative_lex:
            return -1
        else:
            return 0


if __name__ == "__main__":
    getter = BingLiuLexiconValueGetter()

    print(getter.get_value("unwelcoming"))
