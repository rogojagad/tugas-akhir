import pickle


class GeneralInquirerLexiconValueGetter:
    def __init__(self):
        data_dir = "D://Kuliah/TA/data"

        with open(data_dir + "/general-inquirer/positive-words.pickle", "rb") as inp:
            self.positive_lex = pickle.load(inp)

        with open(data_dir + "/general-inquirer/negative-words.pickle", "rb") as inp:
            self.negative_lex = pickle.load(inp)

    def get_value(self, token):
        if self.is_positive(token):
            return 1
        elif self.is_negative(token):
            return -1

    def is_positive(self, word):
        for token in self.positive_lex:
            if token == word:
                return True

    def is_negative(self, word):
        for token in self.negative_lex:
            if token == word:
                return True


if __name__ == "__main__":
    getter = GeneralInquirerLexiconValueGetter()

    print(getter.get_value("victory"))
