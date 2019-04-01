import json
from pprint import pprint


class DatasetFilterer:
    def __init__(self, path):
        self.dataset = self.dataset_opener(path)
        self.result = list()

    def dataset_opener(self, path):
        with open(path) as f:
            return json.load(f)

    def filter(self):
        counter = 0

        for data in self.dataset:
            if all(target == "NULL" for target in data["target"]):
                counter += 1
            else:
                self.result.append(data)

        self.export()

    def export(self):
        with open("dataset/train-dataset.json", "w") as output:
            json.dump(self.result, output)


if __name__ == "__main__":
    filterer = DatasetFilterer("dataset/train-dataset-ori.json")

    filterer.filter()
