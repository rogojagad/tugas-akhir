import pickle
import json
from pprint import pprint

with open("D://Kuliah/TA/data/test/sentiment_analyze_result.pickle", "rb") as inp:
    results = pickle.load(inp)

with open("D://Kuliah/TA/data/test/aspect_sentiment_truth.pickle", "rb") as inp:
    truths = pickle.load(inp)

with open("dataset/test-dataset.json") as f:
    dataset = json.load(f)

for truth, result, data in zip(truths, results, dataset):
    for aspect, sentiment in truth["data"].items():
        try:
            if result["data"][aspect] == sentiment:
                print(data["sentence"])
                print(result["id"])
                print(aspect)
                print("Truth")
                print(sentiment)
                print("Result")
                print(result["data"][aspect])
                print()

        except KeyError:

            continue
