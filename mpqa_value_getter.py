import json


class MPQALexiconValueGetter:
    def __init__(self):
        with open("D:\Kuliah\TA\data\mpqa_lexicon\lexicon.json") as f:
            self.lexicon = json.load(f)

    def get_value(self, word):
        subjectivity = self.lexicon[word]["subjectivity"]
        polarity = self.lexicon[word]["polarity"]

        if subjectivity == "strongsubj":
            if polarity == "positive":
                return 1
            elif polarity == "negative":
                return -1
        elif subjectivity == "weaksubj":
            if polarity == "positive":
                return 0.5
            elif polarity == "negative":
                return -0.5


if __name__ == "__main__":
    getter = MPQALexiconValueGetter()

    print(getter.get_value("above"))
